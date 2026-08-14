"""GAO: reports and testimony on health care program integrity.

The reports-and-testimonies listing is filtered server-side to the "Health Care"
topic (topic id 206), walked newest-first until the coverage cut-off, then
keyword-filtered down to fraud / improper-payment / program-integrity products.
gao.gov rejects plain HTTP clients, so pages come from headless Chrome.
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

BASE = "https://www.gao.gov"
HEALTH_CARE_TOPIC = 206
LISTING = BASE + "/reports-testimonies?topic%5B{t}%5D={t}&page={p}"

KEEP = re.compile(
    r"fraud|improper\s+payment|program\s+integrity|overpayment|kickback|"
    r"false\s+claim|abuse|waste|oversight|internal\s+control|"
    r"unallowable|risk\s+adjustment|upcod|enrollment\s+screening|"
    r"medicare|medicaid",
    re.IGNORECASE,
)

CURATED = [
    (BASE + "/health-care", "GAO - Health Care topic page", "program page"),
    (BASE + "/high-risk-list", "GAO High-Risk List (Medicare & Medicaid)", "program page"),
]


def _rows(html: str):
    return BeautifulSoup(html, "html.parser").select(".views-row")


def discover(since, limit: int | None = None, max_pages: int = 400, **_) -> list[Doc]:
    docs: list[Doc] = []
    page = 0
    old_streak = 0
    while page < max_pages:
        html = pagefetch.fetch(LISTING.format(t=HEALTH_CARE_TOPIC, p=page))
        if not html:
            log.warning("GAO: listing page %s unavailable", page)
            break
        rows = _rows(html)
        if not rows:
            log.info("GAO: no rows on page %s - stopping", page)
            break
        page_old = 0
        for row in rows:
            a = row.select_one("h4 a[href], a[href^='/products/']")
            if not a:
                continue
            times = row.select("time[datetime]")
            date = parse_date(times[0].get("datetime")) if times else ""
            if date and dt.date.fromisoformat(date) < since:
                page_old += 1
                continue
            title = a.get_text(" ", strip=True)
            num_tag = row.select_one("span.d-block.text-small")
            number = num_tag.get_text(" ", strip=True) if num_tag else ""
            if not (KEEP.search(title) or config.is_healthcare_fraud(title)):
                continue
            docs.append(
                Doc(source="GAO", url=urljoin(BASE, a["href"]), title=title, date=date,
                    doc_type="html", category="report or testimony", subsource="GAO",
                    extra={"report_number": number})
            )
        if page_old == len(rows):
            old_streak += 1
            if old_streak >= 2:
                log.info("GAO: past cut-off at page %s - stopping", page)
                break
        else:
            old_streak = 0
        if limit and len(docs) >= limit:
            break
        page += 1

    for url, title, cat in CURATED:
        docs.append(Doc(source="GAO", url=url, title=title, date="", doc_type="html",
                        category=cat, subsource="GAO"))
    log.info("GAO: %s documents discovered", len(docs))
    return docs
