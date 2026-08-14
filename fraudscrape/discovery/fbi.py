"""FBI: national and field-office press releases.

fbi.gov has no date- or topic-filtered listing API, but it publishes a complete
gzipped sitemap. Candidate URLs are keyword-matched on their slug, then each
candidate page is fetched once (and cached) so its published date can be read.
"""

from __future__ import annotations

import datetime as dt
import gzip
import logging
import re
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup

from .. import config, net, pagefetch
from ..models import Doc, parse_date

log = logging.getLogger(__name__)

SITEMAP = "https://www.fbi.gov/sitemap.xml.gz"
SITEMAP_CACHE = config.CACHE_DIR / "fbi_sitemap.xml"

NEWS_PATTERNS = (
    "/news/press-releases/",
    "/news/stories/",
    "/news/speeches-and-testimony/",
)
FIELD_OFFICE_NEWS = re.compile(r"/contact-us/field-offices/[^/]+/news/")

CURATED = [
    ("https://www.fbi.gov/investigate/white-collar-crime/healthcare-fraud",
     "FBI - Health Care Fraud", "program page"),
    ("https://www.fbi.gov/investigate/white-collar-crime",
     "FBI - White-Collar Crime", "program page"),
]


def _sitemap_urls() -> list[str]:
    if SITEMAP_CACHE.exists() and SITEMAP_CACHE.stat().st_size > 0:
        xml = SITEMAP_CACHE.read_text(encoding="utf-8", errors="replace")
    else:
        raw = net.get_bytes(SITEMAP, timeout=180)
        if not raw:
            log.error("FBI: sitemap download failed")
            return []
        xml = gzip.decompress(raw).decode("utf-8", "replace")
        SITEMAP_CACHE.parent.mkdir(parents=True, exist_ok=True)
        SITEMAP_CACHE.write_text(xml, encoding="utf-8")
    return re.findall(r"<loc>(.*?)</loc>", xml)


def _candidates(urls: list[str]) -> list[str]:
    out = []
    for u in urls:
        if not (any(p in u for p in NEWS_PATTERNS) or FIELD_OFFICE_NEWS.search(u)):
            continue
        slug = u.rstrip("/").rsplit("/", 1)[-1]
        if config.is_healthcare_fraud(slug.replace("-", " "), relaxed=True):
            out.append(u)
    return sorted(set(out))


def _office(url: str) -> str:
    m = re.search(r"/field-offices/([^/]+)/", url)
    return f"FBI {m.group(1).replace('-', ' ').title()}" if m else "FBI National Press Office"


def _parse_page(url: str) -> Doc | None:
    html = pagefetch.fetch(url)
    if not html:
        return None
    soup = BeautifulSoup(html, "html.parser")

    title = ""
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(" ", strip=True)
    if not title and soup.title:
        title = soup.title.get_text(" ", strip=True).split(" — ")[0]

    date = ""
    for sel in ('meta[name="DC.date.issued"]', 'meta[property="article:published_time"]',
                'meta[name="publish_date"]', 'meta[itemprop="datePublished"]'):
        tag = soup.select_one(sel)
        if tag and tag.get("content"):
            date = parse_date(tag["content"])
            if date:
                break
    if not date:
        for sel in ("time[datetime]", "p.documentFirstHeading + p", ".documentByLine",
                    ".news-item-date", "span.date", "p.date"):
            tag = soup.select_one(sel)
            if tag:
                date = parse_date(tag.get("datetime") or tag.get_text(" ", strip=True))
                if date:
                    break
    if not date:
        date = parse_date(soup.get_text(" ", strip=True)[:1500])

    body = soup.get_text(" ", strip=True)[:6000]
    if not (config.is_healthcare_fraud(title, relaxed=True)
            or config.is_healthcare_fraud(f"{title} {body}")):
        return None

    return Doc(
        source="FBI", url=url, title=title, date=date, doc_type="html",
        category="press release" if "press-releases" in url else "news",
        subsource=_office(url),
        summary=body[:400],
    )


def discover(since, limit: int | None = None, workers: int = 6, **_) -> list[Doc]:
    urls = _sitemap_urls()
    cands = _candidates(urls)
    log.info("FBI: %s sitemap URLs -> %s health-care-fraud candidates", len(urls), len(cands))
    for u, t, c in CURATED:
        cands.append(u)

    docs: list[Doc] = []
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for doc in pool.map(_safe_parse, cands):
            done += 1
            if done % 100 == 0:
                log.info("FBI: %s/%s candidate pages read, %s kept", done, len(cands), len(docs))
            if doc is None:
                continue
            if doc.date and dt.date.fromisoformat(doc.date) < since:
                continue
            docs.append(doc)
            if limit and len(docs) >= limit:
                break

    for url, title, cat in CURATED:
        if not any(d.url == url for d in docs):
            docs.append(Doc(source="FBI", url=url, title=title, date="", doc_type="html",
                            category=cat, subsource="FBI"))
    log.info("FBI: %s documents discovered", len(docs))
    return docs


def _safe_parse(url: str) -> Doc | None:
    try:
        return _parse_page(url)
    except Exception as exc:  # noqa: BLE001
        log.debug("FBI parse failed %s: %r", url, exc)
        return None
