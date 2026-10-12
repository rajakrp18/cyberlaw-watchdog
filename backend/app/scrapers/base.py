"""
BaseRegulatoryScraper — Abstract base class for all Indian legal source scrapers.

Features:
- Rate limiting (configurable delay between requests)
- Exponential-backoff retry logic via tenacity
- SHA-256 content hashing for deduplication
- Playwright support for JS-heavy government sites
- robots.txt compliance
"""
from __future__ import annotations

import asyncio
import hashlib
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)


@dataclass
class ScrapedDocument:
    """Raw document discovered by a scraper — pre-ingestion."""
    title: str
    original_url: str
    authority: str
    raw_text: str
    content_hash: str
    publication_date: Optional[datetime] = None
    document_type: str = "UNKNOWN"
    local_file_path: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def compute_hash(cls, content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()


class RateLimiter:
    """Simple token-bucket rate limiter."""

    def __init__(self, min_delay_seconds: float = 2.0):
        self.min_delay = min_delay_seconds
        self._last_request: float = 0.0

    async def acquire(self) -> None:
        elapsed = time.monotonic() - self._last_request
        wait = self.min_delay - elapsed
        if wait > 0:
            await asyncio.sleep(wait)
        self._last_request = time.monotonic()


class BaseRegulatoryScraper(ABC):
    """
    Abstract base for all LexSentry source scrapers.

    Subclasses implement `discover_documents` to return a list of ScrapedDocuments.
    The base class handles rate limiting, retries, and robot compliance.
    """

    source_name: str = "UnknownSource"
    base_url: str = ""
    min_request_delay: float = 2.0  # seconds between requests
    max_retries: int = 3

    def __init__(self) -> None:
        self._rate_limiter = RateLimiter(self.min_request_delay)
        self._robots: Optional[RobotFileParser] = None
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "BaseRegulatoryScraper":
        self._client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "User-Agent": "LexSentry/0.1 (Legal Intelligence Agent; contact@yourfirm.com)",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
            follow_redirects=True,
        )
        await self._load_robots()
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._client:
            await self._client.aclose()

    async def _load_robots(self) -> None:
        """Load and parse robots.txt for the base URL."""
        if not self.base_url:
            return
        robots_url = urljoin(self.base_url, "/robots.txt")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(robots_url)
            if resp.status_code == 200:
                parser = RobotFileParser()
                parser.set_url(robots_url)
                parser.read()  # type: ignore[attr-defined]
                self._robots = parser
        except Exception:
            logger.debug(f"Could not load robots.txt for {self.base_url}")

    def _is_allowed(self, url: str) -> bool:
        """Check if the URL is allowed by robots.txt."""
        if self._robots is None:
            return True
        return self._robots.can_fetch("LexSentry", url)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException)),
        reraise=True,
    )
    async def _fetch(self, url: str, **kwargs: Any) -> httpx.Response:
        """Rate-limited, retrying HTTP GET."""
        if not self._is_allowed(url):
            raise PermissionError(f"Blocked by robots.txt: {url}")
        await self._rate_limiter.acquire()
        assert self._client is not None
        response = await self._client.get(url, **kwargs)
        response.raise_for_status()
        return response

    async def _fetch_feed(self, feed_url: str) -> List[Dict[str, Any]]:
        """Fetch and parse an RSS/Atom feed."""
        import feedparser
        resp = await self._fetch(feed_url)
        parsed = feedparser.parse(resp.text)
        return parsed.get("entries", [])

    @abstractmethod
    async def discover_documents(self) -> List[ScrapedDocument]:
        """
        Main scraping method — implemented by each source scraper.
        Returns a list of ScrapedDocuments ready for ingestion.
        """
        ...

    async def run(self) -> List[ScrapedDocument]:
        """Entry point: opens HTTP client and runs discovery."""
        async with self:
            try:
                docs = await self.discover_documents()
                logger.info(f"[{self.source_name}] Discovered {len(docs)} documents")
                return docs
            except Exception as exc:
                logger.error(f"[{self.source_name}] Scrape failed: {exc}", exc_info=True)
                return []
