"""DOJ: press releases from Main Justice and every U.S. Attorney's Office.

justice.gov serves an official JSON feed of all press releases. It cannot be
filtered server-side by topic, so the feed is walked newest-first until it drops
below the coverage cut-off and each item is then matched on the "Healthcare
Fraud" topic tag (or, for items published before that taxonomy existed, on
health-care-fraud keywords).
"""

from __future__ import annotations

import datetime as dt
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor

from .. import config, net
from ..models import Doc

log = logging.getLogger(__name__)

API = "https://www.justice.gov/api/v1/press_releases.json"
PAGE_SIZE = 50
HEALTHCARE_TOPIC_UUID = "cce5d791-6b0b-462d-9a42-768179164d43"
HEALTHCARE_TOPIC_NAMES = {"healthcare fraud", "health care fraud"}

CACHE = config.CACHE_DIR / "doj_api"

# Landing pages that collect DOJ's recurring health-care-fraud publications.
CURATED = [
    ("https://www.justice.gov/criminal/criminal-fraud/health-care-fraud-unit",
     "Criminal Division - Health Care Fraud Unit", "program page"),
    ("https://www.justice.gov/civil/false-claims-act",
     "Civil Division - False Claims Act", "program page"),
    ("https://www.justice.gov/criminal/criminal-fraud/health-care-fraud-unit/strike-force-operations",
     "Health Care Fraud Strike Force Operations", "program page"),
]


def _page_path(page: int):
    return CACHE / f"page_{page:05d}.json"


def _get_page(page: int, force: bool = False) -> list[dict]:
    p = _page_path(page)
    if p.exists() and not force:
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    params = {"pagesize": PAGE_SIZE, "page": page, "sort": "date", "direction": "DESC"}
    for attempt in range(4):
        try:
            # The feed is paged in parallel; a short fixed pause per worker keeps
            # the aggregate request rate modest without serialising every page.
            time.sleep(0.25)
            r = net.get(API, params=params, timeout=90, rate_limit=False)
            if r.status_code == 200:
                results = r.json().get("results", [])
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(json.dumps(results), encoding="utf-8")
                return results
            log.warning("DOJ api page %s -> HTTP %s", page, r.status_code)
        except Exception as exc:  # noqa: BLE001
            log.warning("DOJ api page %s failed: %r", page, exc)
        time.sleep(2 * (attempt + 1))
    return []


def _item_date(item: dict) -> str:
    raw = item.get("date")
    if not raw:
        return ""
    try:
        return dt.datetime.fromtimestamp(int(raw), dt.UTC).date().isoformat()
    except (TypeError, ValueError):
        return ""


def _names(item: dict, key: str) -> list[str]:
    val = item.get(key) or []
    if isinstance(val, dict):
        val = [val]
    return [v.get("name", "") for v in val if isinstance(v, dict)]


def _is_healthcare(item: dict) -> bool:
    topics = item.get("topic") or []
    if isinstance(topics, dict):
        topics = [topics]
    for t in topics:
        if not isinstance(t, dict):
            continue
        if t.get("uuid") == HEALTHCARE_TOPIC_UUID:
            return True
        if (t.get("name") or "").strip().lower() in HEALTHCARE_TOPIC_NAMES:
            return True
    blob = " ".join(
        [item.get("title") or "", item.get("teaser") or "", (item.get("body") or "")[:4000]]
    )
    return config.is_healthcare_fraud(blob)


def _first_page_date(page: int) -> dt.date | None:
    results = _get_page(page)
    if not results:
        return None
    d = _item_date(results[0])
    return dt.date.fromisoformat(d) if d else None


def cutoff_page(since, max_pages: int) -> int:
    """Binary-search the last feed page that still contains items >= `since`.

    The feed is ~2,250 pages deep for a 2021 cut-off; finding the end first means
    the pages can then be fetched in parallel instead of one at a time.
    """
    lo, hi = 0, max_pages
    while lo < hi:
        mid = (lo + hi) // 2
        d = _first_page_date(mid)
        if d is None or d < since:
            hi = mid
        else:
            lo = mid + 1
    log.info("DOJ: coverage ends at feed page %s", lo)
    return lo


def _to_doc(item: dict) -> Doc | None:
    date = _item_date(item)
    url = item.get("url") or ""
    if not url or not _is_healthcare(item):
        return None
    return Doc(
        source="DOJ",
        url=url,
        title=(item.get("title") or "").strip(),
        date=date,
        doc_type="html",
        category="press release",
        subsource="; ".join(_names(item, "component")),
        summary=(item.get("teaser") or "").strip()[:600],
        extra={
            "topics": _names(item, "topic"),
            "release_number": item.get("number") or "",
            "api_body": item.get("body") or "",
            "uuid": item.get("uuid") or "",
        },
    )


def discover(since, limit: int | None = None, max_pages: int = 4000,
             workers: int = 6, **_) -> list[Doc]:
    last = cutoff_page(since, max_pages)
    pages = list(range(last + 1))
    docs: list[Doc] = []
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for results in pool.map(_get_page, pages):
            done += 1
            for item in results:
                date = _item_date(item)
                if date and dt.date.fromisoformat(date) < since:
                    continue
                doc = _to_doc(item)
                if doc:
                    docs.append(doc)
            if done % 100 == 0:
                log.info("DOJ: %s/%s feed pages, %s health-care-fraud releases so far",
                         done, len(pages), len(docs))
            if limit and len(docs) >= limit:
                break

    for url, title, cat in CURATED:
        docs.append(
            Doc(source="DOJ", url=url, title=title, date="", doc_type="html",
                category=cat, subsource="Department of Justice")
        )

    log.info("DOJ: %s documents discovered", len(docs))
    return docs[:limit] if limit else docs
