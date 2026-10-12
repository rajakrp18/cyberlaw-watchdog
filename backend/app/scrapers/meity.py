"""
MeitY (Ministry of Electronics and Information Technology) Scraper
Monitors: https://www.meity.gov.in/
Focus: IT Act amendments, data protection rules, CERT-In advisories,
       intermediary guidelines, cybercrime advisories.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.scrapers.base import BaseRegulatoryScraper, ScrapedDocument

logger = logging.getLogger(__name__)


class MeitYScraper(BaseRegulatoryScraper):
    source_name = "Ministry of Electronics and Information Technology"
    base_url = "https://www.meity.gov.in"
    min_request_delay = 3.0

    WHATS_NEW_URL = "https://www.meity.gov.in/whats-new"
    ACTS_URL = "https://www.meity.gov.in/acts-rules-regulations"

    async def discover_documents(self) -> List[ScrapedDocument]:
        documents: List[ScrapedDocument] = []

        for url, doc_type in [
            (self.WHATS_NEW_URL, "NOTIFICATION"),
            (self.ACTS_URL, "GUIDELINE"),
        ]:
            try:
                resp = await self._fetch(url)
                soup = BeautifulSoup(resp.text, "lxml")

                # MeitY uses a standard Drupal content listing
                links = soup.select("div.view-content .views-row a, article a, div.field-items li a")
                for link in links[:25]:
                    title = link.get_text(strip=True)
                    href = link.get("href", "")
                    if not href or not title or len(title) < 10:
                        continue

                    full_url = urljoin(self.base_url, href)
                    text_content = await self._fetch_page_text(full_url)
                    if not text_content:
                        continue

                    content_hash = ScrapedDocument.compute_hash(text_content)
                    documents.append(ScrapedDocument(
                        title=title,
                        original_url=full_url,
                        authority="MeitY",
                        raw_text=text_content,
                        content_hash=content_hash,
                        publication_date=None,
                        document_type=doc_type,
                        metadata={"source_page": url},
                    ))

            except Exception as exc:
                logger.error(f"[MeitYScraper] Failed for {url}: {exc}")

        return documents

    async def _fetch_page_text(self, url: str) -> Optional[str]:
        try:
            resp = await self._fetch(url)
            soup = BeautifulSoup(resp.text, "lxml")
            content = soup.select_one("div.field-items") or soup.select_one("article") or soup.select_one("main")
            if content:
                return content.get_text(separator="\n", strip=True)[:12000]
            return soup.get_text(separator="\n", strip=True)[:12000]
        except Exception as exc:
            logger.debug(f"[MeitYScraper] {url}: {exc}")
            return None


class CERTInScraper(BaseRegulatoryScraper):
    """
    CERT-In Advisories Scraper.
    CERT-In publishes security advisories and vulnerability notes publicly.
    """
    source_name = "CERT-In"
    base_url = "https://www.cert-in.org.in"
    min_request_delay = 3.0

    ADVISORIES_URL = "https://www.cert-in.org.in/s2cMainServlet?pageid=PUBVLNOTES01"

    async def discover_documents(self) -> List[ScrapedDocument]:
        documents: List[ScrapedDocument] = []
        try:
            resp = await self._fetch(self.ADVISORIES_URL)
            soup = BeautifulSoup(resp.text, "lxml")

            rows = soup.select("table tr")[1:16]  # Latest 15
            for row in rows:
                cells = row.find_all("td")
                if len(cells) < 3:
                    continue

                link_tag = cells[0].find("a")
                if not link_tag:
                    continue

                title = link_tag.get_text(strip=True)
                href = link_tag.get("href", "")
                url = urljoin(self.base_url, href)
                date_text = cells[2].get_text(strip=True) if len(cells) > 2 else ""

                text_content = await self._fetch_advisory_text(url)
                if not text_content:
                    continue

                content_hash = ScrapedDocument.compute_hash(text_content)
                documents.append(ScrapedDocument(
                    title=f"CERT-In Advisory: {title}",
                    original_url=url,
                    authority="CERT-In",
                    raw_text=text_content,
                    content_hash=content_hash,
                    publication_date=self._parse_date(date_text),
                    document_type="ADVISORY",
                    metadata={"advisory_id": title},
                ))

        except Exception as exc:
            logger.error(f"[CERTInScraper] Failed: {exc}")

        return documents

    async def _fetch_advisory_text(self, url: str) -> Optional[str]:
        try:
            resp = await self._fetch(url)
            soup = BeautifulSoup(resp.text, "lxml")
            content = soup.select_one("div#advisory") or soup.select_one("div.content") or soup.find("body")
            if content:
                return content.get_text(separator="\n", strip=True)[:10000]
            return None
        except Exception:
            return None

    @staticmethod
    def _parse_date(date_str: str) -> Optional[datetime]:
        for fmt in ["%d %B %Y", "%d-%m-%Y", "%B %d, %Y"]:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        return None
