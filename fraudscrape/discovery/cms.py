"""CMS: newsroom items and program-integrity publications.

cms.gov blocks plain HTTP clients on its search pages, but the newsroom sitemap
is served to anyone. Candidate URLs are keyword-matched on their slug and then
rendered with headless Chrome to read the published date.
"""

from __future__ import annotations

import datetime as dt
import logging
import re
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup

from .. import config, net, pagefetch
from ..models import Doc, parse_date

log = logging.getLogger(__name__)

SITEMAP_INDEX = "https://www.cms.gov/sitemap-newsroom.xml"

CURATED = [
    ("https://www.cms.gov/about-cms/contact/newsroom", "CMS Newsroom", "index page"),
    ("https://www.cms.gov/data-research/monitoring-programs/medicare-fee-service-compliance-programs",
     "Medicare Fee-for-Service Compliance Programs", "program page"),
    ("https://www.cms.gov/data-research/monitoring-programs/improper-payment-measurement-programs",
     "Improper Payment Measurement Programs", "program page"),
    ("https://www.cms.gov/data-research/monitoring-programs/medicaid-and-chip-compliance-programs",
     "Medicaid and CHIP Compliance Programs", "program page"),
    ("https://www.cms.gov/data-research/monitoring-programs/medicare-fee-service-compliance-programs/medicare-fee-service-recovery-audit-program",
     "Medicare Fee-for-Service Recovery Audit Program", "program page"),
]

CATEGORY_BY_PATH = {
    "press-releases": "press release",
    "fact-sheets": "fact sheet",
    "news-alert": "news alert",
    "cms-roundup": "roundup",
    "blog": "blog",
}


def _sitemap_urls() -> list[str]:
    idx = net.get_text(SITEMAP_INDEX, timeout=90)
    if not idx:
        log.error("CMS: newsroom sitemap index unavailable")
        return []
    pages = re.findall(r"<loc>(.*?)</loc>", idx)
    urls: list[str] = []
    for p in pages:
        body = net.get_text(p, timeout=90)
        if body:
            urls += re.findall(r"<loc>(.*?)</loc>", body)
    return urls


def _candidates(urls: list[str]) -> list[str]:
    out = []
    for u in urls:
        slug = u.rstrip("/").rsplit("/", 1)[-1].replace("-", " ")
        if config.is_healthcare_fraud(slug, relaxed=True):
            out.append(u)
    return sorted(set(out))


def _category(url: str) -> str:
    parts = url.split("/newsroom/")
    if len(parts) > 1:
        return CATEGORY_BY_PATH.get(parts[1].split("/")[0], "newsroom item")
    return "publication"


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
        title = soup.title.get_text(" ", strip=True).split("|")[0].strip()

    # cms.gov shows the publication date in `.create-date` next to the title. The
    # <time> elements further down belong to the "related items" rail, so they must
    # not be consulted before that - they date other pages, not this one.
    date = ""
    for sel in (".create-date", 'meta[property="article:published_time"]',
                'meta[name="dcterms.created"]', 'meta[name="date"]'):
        tag = soup.select_one(sel)
        if tag:
            date = parse_date(tag.get("content") or tag.get("datetime")
                              or tag.get_text(" ", strip=True))
            if date:
                break
    if not date and h1:
        # fall back to the header block that wraps the title
        block = h1
        for _ in range(3):
            if block.parent:
                block = block.parent
        date = parse_date(block.get_text(" | ", strip=True)[:200])

    return Doc(source="CMS", url=url, title=title, date=date, doc_type="html",
               category=_category(url), subsource="CMS",
               summary=soup.get_text(" ", strip=True)[:400])


def discover(since, limit: int | None = None, workers: int = 3, **_) -> list[Doc]:
    urls = _sitemap_urls()
    cands = _candidates(urls)
    log.info("CMS: %s newsroom URLs -> %s candidates", len(urls), len(cands))

    docs: list[Doc] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for doc in pool.map(_safe_parse, cands):
            if doc is None:
                continue
            if doc.date and dt.date.fromisoformat(doc.date) < since:
                continue
            docs.append(doc)
            if limit and len(docs) >= limit:
                break

    for url, title, cat in CURATED:
        docs.append(Doc(source="CMS", url=url, title=title, date="", doc_type="html",
                        category=cat, subsource="CMS"))
    log.info("CMS: %s documents discovered", len(docs))
    return docs


def _safe_parse(url: str) -> Doc | None:
    try:
        return _parse_page(url)
    except Exception as exc:  # noqa: BLE001
        log.debug("CMS parse failed %s: %r", url, exc)
        return None
