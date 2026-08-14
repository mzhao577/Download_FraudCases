"""One way in for HTML pages: disk cache -> plain HTTP -> headless Chrome.

Discovery and download both go through here, so a page that discovery already
had to read (to learn its date) is not fetched a second time.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path

from . import browser, config, net

log = logging.getLogger(__name__)

PAGE_CACHE = config.CACHE_DIR / "pages"

# Hosts where plain HTTP is pointless: they answer bot walls to non-browsers.
BROWSER_ONLY_HOSTS = {"www.justice.gov", "justice.gov", "www.cms.gov", "www.gao.gov"}


def _cache_path(url: str) -> Path:
    h = hashlib.sha1(url.encode("utf-8")).hexdigest()
    return PAGE_CACHE / h[:2] / f"{h}.html"


def cached(url: str) -> str | None:
    p = _cache_path(url)
    if p.exists() and p.stat().st_size > 0:
        return p.read_text(encoding="utf-8", errors="replace")
    return None


def store(url: str, html: str) -> None:
    p = _cache_path(url)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8", errors="replace")


def fetch(url: str, *, force: bool = False, allow_browser: bool = True) -> str | None:
    """Return page HTML, using the cache when possible."""
    if not force:
        hit = cached(url)
        if hit is not None:
            return hit

    host = url.split("/")[2].lower() if "://" in url else ""
    html = None
    if host not in BROWSER_ONLY_HOSTS:
        html = net.get_text(url)

    if html is None and allow_browser:
        net.throttle(url)          # be as polite in Chrome as over plain HTTP
        html, _ = browser.open_page(url)

    if html:
        store(url, html)
    return html
