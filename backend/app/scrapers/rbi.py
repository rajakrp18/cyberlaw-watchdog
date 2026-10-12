"""
RBI (Reserve Bank of India) Scraper
Monitors: https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx
Focus: Cybercrime-related circulars, guidelines on bank account freezes,
       mule accounts, digital fraud, and payment system advisories.
"""
from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.scrapers.base import BaseRegulatoryScraper, ScrapedDocument

logger = logging.getLogger(__name__)

CYBER_KEYWORDS = [
    "cyber", "fraud", "phishing", "account freeze", "lien", "mule",
    "digital arrest", "NCRP", "UPI", "payment", "debit freeze",
    "restitution", "victim", "CERT-In", "I4C", "cybercrime",
    "OTP", "unauthorized transaction", "chargeback",
]


def _is_cyber_relevant(text: str) -> bool:
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in CYBER_KEYWORDS)


class RBIScraper(BaseRegulatoryScraper):
    source_name = "Reserve Bank of India"
    base_url = "https://www.rbi.org.in"
    min_request_delay = 3.0

    # RBI provides press releases in a searchable list; we target the
    # cyber-regulation category which has a stable URL pattern.
    PRESS_RELEASE_URL = "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx"
    CIRCULAR_FEED = "https://www.rbi.org.in/scripts/rss.aspx?id=42"  # Circulars RSS

    async def discover_documents(self) -> List[ScrapedDocument]:
        documents: List[ScrapedDocument] = []

        # ── 1. Parse RSS feed for circulars ──────────────────
        try:
            entries = await self._fetch_feed(self.CIRCULAR_FEED)
            for entry in entries[:20]:  # Latest 20
                title = entry.get("title", "")
                link = entry.get("link", "")
                if not link or not _is_cyber_relevant(title):
                    continue

                text_content = await self._fetch_document_text(link)
                if not text_content:
                    continue

                pub_date = self._parse_date(entry.get("published", ""))
                content_hash = ScrapedDocument.compute_hash(text_content)

                documents.append(ScrapedDocument(
                    title=title.strip(),
                    original_url=link,
                    authority="Reserve Bank of India",
                    raw_text=text_content,
                    content_hash=content_hash,
                    publication_date=pub_date,
                    document_type="CIRCULAR",
                    metadata={"feed": "rbi_circulars", "category": "cyber"},
                ))

        except Exception as exc:
            logger.warning(f"[RBIScraper] RSS feed failed: {exc}")

        # ── 2. Fallback: scrape press release listing page ───
        if not documents:
            documents = await self._scrape_press_releases()

        return documents

    async def _fetch_document_text(self, url: str) -> Optional[str]:
        """Fetch and extract text from an RBI circular/press release page."""
        try:
            resp = await self._fetch(url)
            soup = BeautifulSoup(resp.text, "lxml")
            # RBI uses a main content div
            content = soup.find("div", {"id": "divContents"}) or soup.find("div", class_="content")
            if content:
                return content.get_text(separator="\n", strip=True)
            return soup.get_text(separator="\n", strip=True)[:10000]
        except Exception as exc:
            logger.debug(f"[RBIScraper] Could not fetch document {url}: {exc}")
            return None

    async def _scrape_press_releases(self) -> List[ScrapedDocument]:
        """Fallback scraper for the press release listing page."""
        documents: List[ScrapedDocument] = []
        try:
            resp = await self._fetch(self.PRESS_RELEASE_URL)
            soup = BeautifulSoup(resp.text, "lxml")
            table = soup.find("table", class_="tablebg")
            if not table:
                return []

            for row in table.find_all("tr")[1:21]:  # Skip header, take 20
                cells = row.find_all("td")
                if len(cells) < 2:
                    continue
                link_tag = cells[1].find("a")
                if not link_tag:
                    continue

                title = link_tag.get_text(strip=True)
                href = link_tag.get("href", "")
                url = urljoin(self.base_url, href) if href else ""

                if not url or not _is_cyber_relevant(title):
                    continue

                text_content = await self._fetch_document_text(url)
                if not text_content:
                    continue

                # Try to extract date from the first cell
                date_text = cells[0].get_text(strip=True) if cells else ""
                pub_date = self._parse_date(date_text)
                content_hash = ScrapedDocument.compute_hash(text_content)

                documents.append(ScrapedDocument(
                    title=title,
                    original_url=url,
                    authority="Reserve Bank of India",
                    raw_text=text_content,
                    content_hash=content_hash,
                    publication_date=pub_date,
                    document_type="CIRCULAR",
                ))

        except Exception as exc:
            logger.error(f"[RBIScraper] Press release scrape failed: {exc}")

        return documents

    @staticmethod
    def _parse_date(date_str: str) -> Optional[datetime]:
        formats = ["%B %d, %Y", "%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%dT%H:%M:%SZ"]
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        return None
