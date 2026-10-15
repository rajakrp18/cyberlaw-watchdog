"""
IndianKanoon Scraper
Monitors: https://indiankanoon.org/search/?formInput=cyber+fraud+bank+freeze
Focus: Supreme Court, High Court judgments on cyber fraud, bank freeze, mule accounts.
IndianKanoon is the most accessible public Indian legal database — no auth required.
"""
from __future__ import annotations

import hashlib
import logging
import re
from datetime import datetime
from typing import List, Optional
from urllib.parse import urljoin, quote

from bs4 import BeautifulSoup

from app.scrapers.base import BaseRegulatoryScraper, ScrapedDocument

logger = logging.getLogger(__name__)

# Search queries — each brings different relevant judgments
SEARCH_QUERIES = [
    "cyber fraud bank account freeze",
    "NCRP mule account freeze",
    "digital arrest restitution",
    "bank freeze section 102 crpc",
    "UPI fraud restitution victim",
]

# Only include judgments mentioning these terms
RELEVANCE_KEYWORDS = [
    "cyber", "fraud", "freeze", "mule", "NCRP", "bank account",
    "digital arrest", "UPI", "OTP", "lien", "IT Act", "cybercrime",
    "section 66", "section 43", "restitution", "victim", "phishing",
]


def _is_relevant(text: str) -> bool:
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in RELEVANCE_KEYWORDS)


def _extract_court(title: str, snippet: str) -> str:
    """Guess the court from title/snippet text."""
    combined = (title + " " + snippet).lower()
    if "supreme court" in combined:
        return "Supreme Court of India"
    for hc in ["bombay", "delhi", "calcutta", "madras", "allahabad",
               "telangana", "andhra", "karnataka", "kerala", "gujarat",
               "rajasthan", "punjab", "himachal", "orissa", "patna"]:
        if hc in combined:
            return f"High Court of {hc.title()}"
    return "Indian Court"


class IndianKanoonScraper(BaseRegulatoryScraper):
    source_name = "Indian Kanoon"
    base_url = "https://indiankanoon.org"
    check_robots = False
    min_request_delay = 2.0   # Respectful crawl delay

    async def discover_documents(self) -> List[ScrapedDocument]:
        documents: List[ScrapedDocument] = []
        seen_urls: set = set()

        for query in SEARCH_QUERIES:
            try:
                encoded = quote(query)
                search_url = f"{self.base_url}/search/?formInput={encoded}&pagenum=1"
                logger.info(f"[IndianKanoon] Searching: {query}")
                resp = await self._fetch(search_url)
                soup = BeautifulSoup(resp.text, "lxml")

                results = soup.select("div.result")
                if not results:
                    results = soup.select("div.docsource_main")

                for result in results[:5]:   # Top 5 per query
                    # Extract title + link
                    link_tag = result.select_one("a[href]")
                    if not link_tag:
                        continue
                    href = link_tag.get("href", "")
                    if not href.startswith("/doc/"):
                        continue
                    doc_url = urljoin(self.base_url, href)
                    if doc_url in seen_urls:
                        continue
                    seen_urls.add(doc_url)

                    title = link_tag.get_text(strip=True)
                    snippet = result.get_text(separator=" ", strip=True)[:500]

                    if not _is_relevant(title + " " + snippet):
                        continue

                    # Fetch full document text
                    doc_text = await self._fetch_doc_text(doc_url)
                    if not doc_text or len(doc_text) < 200:
                        continue

                    content_hash = hashlib.sha256(doc_url.encode()).hexdigest()[:32]
                    court = _extract_court(title, snippet)
                    pub_date = self._extract_date(doc_text) or datetime.utcnow()

                    documents.append(ScrapedDocument(
                        title=title[:250],
                        original_url=doc_url,
                        authority=court,
                        raw_text=doc_text[:15000],
                        content_hash=content_hash,
                        publication_date=pub_date,
                        document_type="JUDGMENT",
                        metadata={"source": "indiankanoon", "query": query},
                    ))
                    logger.info(f"[IndianKanoon] Found: {title[:80]}")

            except Exception as exc:
                logger.warning(f"[IndianKanoon] Query '{query}' failed: {exc}")

        logger.info(f"[IndianKanoon] Total discovered: {len(documents)}")
        return documents

    async def _fetch_doc_text(self, url: str) -> Optional[str]:
        try:
            resp = await self._fetch(url)
            soup = BeautifulSoup(resp.text, "lxml")
            # IndianKanoon main content div
            content = (
                soup.select_one("div#judgments") or
                soup.select_one("div.judgments") or
                soup.select_one("div#doc_content") or
                soup.select_one("div.doc_content")
            )
            if content:
                return content.get_text(separator="\n", strip=True)
            return soup.get_text(separator="\n", strip=True)[:15000]
        except Exception as exc:
            logger.debug(f"[IndianKanoon] Doc fetch failed {url}: {exc}")
            return None

    @staticmethod
    def _extract_date(text: str) -> Optional[datetime]:
        patterns = [
            r"(\d{1,2}(?:st|nd|rd|th)?\s+\w+\s+\d{4})",
            r"(\d{4}-\d{2}-\d{2})",
            r"(\d{1,2}/\d{1,2}/\d{4})",
        ]
        for pat in patterns:
            m = re.search(pat, text[:500])
            if m:
                for fmt in ["%d %B %Y", "%d %b %Y", "%Y-%m-%d", "%d/%m/%Y"]:
                    try:
                        raw = re.sub(r"(st|nd|rd|th)", "", m.group(1)).strip()
                        return datetime.strptime(raw, fmt)
                    except ValueError:
                        continue
        return None
