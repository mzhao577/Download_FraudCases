"""HHS-OIG: enforcement actions, audits/evaluations, MFCU material, LEIE data.

oig.hhs.gov paginates 20 items per page, newest first, so each listing is walked
until it falls below the coverage cut-off.
"""

from __future__ import annotations

import datetime as dt
import logging
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .. import config, pagefetch
from ..models import Doc, parse_date

log = logging.getLogger(__name__)

BASE = "https://oig.hhs.gov"
ENFORCEMENT = BASE + "/fraud/enforcement/"
REPORTS = BASE + "/reports/all/"

# Small curated set: recurring publications and bulk data that no listing paginates.
CURATED = [
    (BASE + "/fraud/enforcement/", "HHS-OIG Enforcement Actions (index)", "index page", "html"),
    (BASE + "/fraud/medicaid-fraud-control-units-mfcu/",
     "Medicaid Fraud Control Units (MFCU)", "program page", "html"),
    (BASE + "/exclusions/", "LEIE - Exclusions Program", "program page", "html"),
    (BASE + "/exclusions/exclusions_list.asp", "LEIE Downloadable Databases", "program page", "html"),
    ("https://oig.hhs.gov/exclusions/downloadables/UPDATED.csv",
     "LEIE - List of Excluded Individuals and Entities (full database, CSV)",
     "exclusions data", "csv"),
    (BASE + "/reports-and-publications/hcfac/", "Health Care Fraud and Abuse Control Program reports",
     "program page", "html"),
    (BASE + "/reports-and-publications/semiannual/", "OIG Semiannual Reports to Congress",
     "program page", "html"),
]

# Report titles worth keeping: OIG publishes thousands of routine audits, so the
# report listing is keyword-filtered while the enforcement listing is taken whole.
REPORT_KEEP = re.compile(
    r"fraud|abuse|kickback|false\s+claim|improper\s+payment|overpayment|"
    r"unallowable|did\s+not\s+comply|noncompliance|non-?compliance|"
    r"program\s+integrity|excluded|exclusion|enrollment|"
    r"upcod|billing|risk\s+adjustment|medicare|medicaid|telehealth|opioid",
    re.IGNORECASE,
)


def _cards(html: str):
    return BeautifulSoup(html, "html.parser").select("li.usa-card")


def _card_link(card):
    a = card.select_one("h2 a[href], h3 a[href], .usa-card__heading a[href]")
    return a


def _card_date(card) -> str:
    span = card.select_one("span.text-base-dark")
    if span:
        d = parse_date(span.get_text(" ", strip=True))
        if d:
            return d
    for dd in card.select("dd.pep-metadata__def"):
        d = parse_date(dd.get_text(" ", strip=True))
        if d:
            return d
    return parse_date(card.get_text(" ", strip=True))


def _card_tags(card) -> list[str]:
    return [t.get_text(" ", strip=True) for t in card.select("li.usa-tag, .usa-tag")]


def _card_meta(card) -> dict:
    meta = {}
    for div in card.select("dl.pep-metadata div.grid-col, dl.pep-metadata > div"):
        dt_ = div.find("dt")
        dd_ = div.find("dd")
        if dt_ and dd_:
            meta[dt_.get_text(" ", strip=True)] = dd_.get_text(" ", strip=True)
    return meta


def _walk(listing_url: str, since: dt.date, max_pages: int, label: str):
    """Yield (card, url, title, date) newest-first until dates drop below `since`."""
    page = 0
    consecutive_old = 0
    while page < max_pages:
        url = listing_url if page == 0 else f"{listing_url}?page={page + 1}"
        html = pagefetch.fetch(url)
        if not html:
            log.warning("%s: could not fetch listing page %s", label, page)
            break
        cards = _cards(html)
        if not cards:
            log.info("%s: no cards on page %s - stopping", label, page)
            break
        page_old = 0
        for card in cards:
            a = _card_link(card)
            if not a:
                continue
            date = _card_date(card)
            if date and dt.date.fromisoformat(date) < since:
                page_old += 1
                continue
            yield card, urljoin(BASE, a["href"]), a.get_text(" ", strip=True), date
        if page_old == len(cards):
            consecutive_old += 1
            if consecutive_old >= 2:
                log.info("%s: past cut-off at page %s - stopping", label, page)
                break
        else:
            consecutive_old = 0
        if page % 25 == 0:
            log.info("%s: listing page %s", label, page)
        page += 1


def discover(since, limit: int | None = None, max_pages: int = 700, **_) -> list[Doc]:
    docs: list[Doc] = []

    # 1. Enforcement actions (criminal, civil, CMP, state MFCU cases)
    for card, url, title, date in _walk(ENFORCEMENT, since, max_pages, "OIG-enforcement"):
        tags = _card_tags(card)
        docs.append(
            Doc(source="HHS-OIG", url=url, title=title, date=date, doc_type="html",
                category="enforcement action",
                subsource="; ".join(tags) or "HHS-OIG",
                extra={"tags": tags})
        )
        if limit and len(docs) >= limit:
            break
    log.info("HHS-OIG: %s enforcement actions", len(docs))

    # 2. Audits / evaluations / inspections, keyword-filtered
    if not (limit and len(docs) >= limit):
        before = len(docs)
        for card, url, title, date in _walk(REPORTS, since, max_pages, "OIG-reports"):
            meta = _card_meta(card)
            blob = " ".join([title, " ".join(meta.values())])
            if not (REPORT_KEEP.search(blob) or config.is_healthcare_fraud(blob)):
                continue
            docs.append(
                Doc(source="HHS-OIG", url=url, title=title, date=date, doc_type="html",
                    category="report", subsource=meta.get("HHS Agency", "HHS-OIG"),
                    extra={"metadata": meta})
            )
            if limit and len(docs) >= limit:
                break
        log.info("HHS-OIG: %s reports", len(docs) - before)

    for url, title, cat, kind in CURATED:
        docs.append(
            Doc(source="HHS-OIG", url=url, title=title, date="", doc_type=kind,
                category=cat, subsource="HHS-OIG")
        )

    log.info("HHS-OIG: %s documents discovered", len(docs))
    return docs
