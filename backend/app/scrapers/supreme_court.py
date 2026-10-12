"""
Supreme Court of India Scraper
Monitors: https://www.sci.gov.in/judgments/
Focus: Cybercrime judgments — bank account freeze orders, digital fraud,
       jurisdiction disputes, BNSS/BNS/IT Act interpretations.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.scrapers.base import BaseRegulatoryScraper, ScrapedDocument

logger = logging.getLogger(__name__)

CYBER_KEYWORDS = [
    "cyber", "fraud", "bank account", "freeze", "lien", "mule",
    "digital", "NCRP", "information technology", "IT Act",
    "BNSS", "BNS", "cybercrime", "arrest", "victim restitution",
    "police powers", "jurisdiction", "section 66", "section 43",
    "intermediary", "payment", "UPI", "CERT",
]


def _is_cyber_relevant(text: str) -> bool:
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in CYBER_KEYWORDS)


class SupremeCourtScraper(BaseRegulatoryScraper):
    source_name = "Supreme Court of India"
    base_url = "https://www.sci.gov.in"
    min_request_delay = 4.0  # Be respectful of judicial servers

    JUDGMENTS_URL = "https://www.sci.gov.in/judgments/"
    # SCI provides a downloadable judgment search — we use the public listing
    RECENT_JUDGMENTS_URL = "https://www.sci.gov.in/judgments/?p=1"

    async def discover_documents(self) -> List[ScrapedDocument]:
        """
        SCI does not provide a reliable RSS feed, so we scrape the
        judgments listing page and filter for cyber-relevant entries.
        """
        documents: List[ScrapedDocument] = []

        try:
            resp = await self._fetch(self.RECENT_JUDGMENTS_URL)
            soup = BeautifulSoup(resp.text, "lxml")

            # SCI judgment list entries
            judgment_links = soup.select("div.view-content div.views-row a")
            if not judgment_links:
                judgment_links = soup.select("table.views-table tbody tr td a")

            for link in judgment_links[:30]:
                title = link.get_text(strip=True)
                href = link.get("href", "")
                if not href or not title:
                    continue

                url = urljoin(self.base_url, href)
                if not _is_cyber_relevant(title):
                    continue

                text_content = await self._fetch_judgment_text(url)
                if not text_content:
                    continue

                content_hash = ScrapedDocument.compute_hash(text_content)
                documents.append(ScrapedDocument(
                    title=title,
                    original_url=url,
                    authority="Supreme Court of India",
                    raw_text=text_content,
                    content_hash=content_hash,
                    publication_date=None,  # Extracted by NLP pipeline
                    document_type="JUDGMENT",
                    metadata={"court": "Supreme Court of India"},
                ))

        except Exception as exc:
            logger.error(f"[SupremeCourtScraper] Failed: {exc}", exc_info=True)

        logger.info(f"[SupremeCourtScraper] Found {len(documents)} cyber-relevant judgments")
        return documents

    async def _fetch_judgment_text(self, url: str) -> Optional[str]:
        """Fetch judgment page and extract readable text."""
        try:
            resp = await self._fetch(url)
            soup = BeautifulSoup(resp.text, "lxml")

            # Try different content selectors used by SCI
            for selector in ["div.field-items", "div.view-content", "div#content", "article"]:
                content = soup.select_one(selector)
                if content:
                    return content.get_text(separator="\n", strip=True)[:15000]

            return soup.get_text(separator="\n", strip=True)[:15000]
        except Exception as exc:
            logger.debug(f"[SupremeCourtScraper] Fetch failed for {url}: {exc}")
            return None
