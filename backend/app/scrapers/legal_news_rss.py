"""
Legal News RSS Scraper
Monitors LiveLaw.in and BarAndBench.com RSS feeds.
Both are major Indian legal news publications with open RSS feeds — very accessible.
Focuses on cyber law, bank fraud, digital arrest, and regulatory updates.
"""
from __future__ import annotations

import hashlib
import logging
import re
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import List, Optional

from bs4 import BeautifulSoup

from app.scrapers.base import BaseRegulatoryScraper, ScrapedDocument

logger = logging.getLogger(__name__)

CYBER_KEYWORDS = [
    "cyber", "fraud", "bank account freeze", "mule account", "digital arrest",
    "NCRP", "UPI fraud", "IT Act", "cybercrime", "account lien", "CERT-In",
    "I4C", "phishing", "OTP fraud", "bank freeze", "restitution", "RBI circular",
    "data breach", "ransomware", "section 66", "section 43", "BNSS",
]

RSS_SOURCES = [
    {
        "name": "Bar and Bench",
        "url": "https://www.barandbench.com/feed",
        "authority_prefix": "Bar and Bench",
        "doc_type": "LEGAL_NEWS",
    },
    {
        "name": "Google News (India Cyber Crime & Freeze)",
        "url": "https://news.google.com/rss/search?q=cyber+fraud+bank+freeze+OR+digital+arrest+OR+NCRP+when:7d&hl=en-IN&gl=IN&ceid=IN:en",
        "authority_prefix": "High Court / Regulator",
        "doc_type": "JUDGMENT",
    },
    {
        "name": "Google News (Bank Accounts & CrPC 102)",
        "url": "https://news.google.com/rss/search?q=Section+102+CrPC+bank+freeze+OR+mule+accounts+High+Court+when:7d&hl=en-IN&gl=IN&ceid=IN:en",
        "authority_prefix": "High Court",
        "doc_type": "JUDGMENT",
    },
]


def _is_cyber_relevant(text: str) -> bool:
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in CYBER_KEYWORDS)


def _parse_rss_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        return parsedate_to_datetime(date_str).replace(tzinfo=None)
    except Exception:
        pass
    for fmt in ["%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%dT%H:%M:%S%z"]:
        try:
            return datetime.strptime(date_str.strip(), fmt).replace(tzinfo=None)
        except ValueError:
            continue
    return None


class LegalNewsRSSScraper(BaseRegulatoryScraper):
    source_name = "Legal News RSS (Bar & Bench & Live Feeds)"
    base_url = "https://www.barandbench.com"
    check_robots = False
    min_request_delay = 1.0

    async def discover_documents(self) -> List[ScrapedDocument]:
        documents: List[ScrapedDocument] = []
        seen_urls: set = set()

        for source in RSS_SOURCES:
            try:
                logger.info(f"[LegalNewsRSS] Fetching feed: {source['name']}")
                entries = await self._fetch_feed(source["url"])

                for entry in entries[:15]:  # Latest 15 per feed
                    title = entry.get("title", "")
                    link  = entry.get("link", "")
                    summary = entry.get("summary", entry.get("description", ""))

                    if not link or not title:
                        continue
                    if link in seen_urls:
                        continue
                    seen_urls.add(link)

                    if not _is_cyber_relevant(title + " " + summary):
                        continue

                    # Fetch full article text or construct from summary
                    article_text = None
                    try:
                        # Only try direct fetch for non-google links or fast responses
                        if "news.google.com" not in link:
                            article_text = await self._fetch_article_text(link)
                    except Exception:
                        pass

                    clean_summary = BeautifulSoup(summary or "", "html.parser").get_text(strip=True)
                    if not article_text or len(article_text) < 60:
                        article_text = f"{title}\n\nLegal Intelligence Summary: {clean_summary}\nSource: {source['name']}\nDirect Reference: {link}"

                    content_hash = hashlib.sha256(link.encode()).hexdigest()[:32]
                    pub_date = _parse_rss_date(
                        entry.get("published", entry.get("updated", ""))
                    ) or datetime.utcnow()

                    documents.append(ScrapedDocument(
                        title=title.strip()[:250],
                        original_url=link,
                        authority=self._detect_authority(title, article_text, source["authority_prefix"]),
                        raw_text=article_text[:12000],
                        content_hash=content_hash,
                        publication_date=pub_date,
                        document_type=source["doc_type"],
                        metadata={"feed": source["name"], "feed_url": source["url"]},
                    ))
                    logger.info(f"[LegalNewsRSS] Found: {title[:70]}")

            except Exception as exc:
                logger.warning(f"[LegalNewsRSS] Feed '{source['name']}' failed: {exc}")

        logger.info(f"[LegalNewsRSS] Total discovered: {len(documents)}")
        return documents

    async def _fetch_article_text(self, url: str) -> Optional[str]:
        try:
            resp = await self._fetch(url)
            soup = BeautifulSoup(resp.text, "lxml")
            # Remove nav/header/footer clutter
            for tag in soup(["nav", "header", "footer", "script", "style", "aside"]):
                tag.decompose()
            # Try article body selectors common to LiveLaw / Bar & Bench
            content = (
                soup.select_one("div.article-content") or
                soup.select_one("div.post-content") or
                soup.select_one("article") or
                soup.select_one("div.entry-content") or
                soup.select_one("main")
            )
            if content:
                return content.get_text(separator="\n", strip=True)
            return soup.get_text(separator="\n", strip=True)[:12000]
        except Exception as exc:
            logger.debug(f"[LegalNewsRSS] Article fetch failed {url}: {exc}")
            return None

    @staticmethod
    def _detect_authority(title: str, text: str, default: str) -> str:
        combined = (title + " " + text[:500]).lower()
        if "supreme court" in combined:
            return "Supreme Court of India"
        if "high court" in combined:
            for hc in ["bombay", "delhi", "calcutta", "madras", "allahabad",
                       "telangana", "karnataka", "kerala", "gujarat", "rajasthan"]:
                if hc in combined:
                    return f"High Court of {hc.title()}"
            return "High Court"
        if "reserve bank" in combined or "rbi" in combined:
            return "Reserve Bank of India"
        if "cert-in" in combined or "cert in" in combined:
            return "CERT-In (MeitY)"
        if "mha" in combined or "ministry of home" in combined or "i4c" in combined:
            return "Ministry of Home Affairs / I4C"
        return default
