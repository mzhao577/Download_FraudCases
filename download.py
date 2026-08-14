#!/usr/bin/env python3
"""Step 2 - download everything in state/manifest.jsonl into ./downloaded/<Source>/.

Web pages are saved as .html and a .pdf rendering of that same saved page;
documents that are already PDFs (or CSV/ZIP data files) are saved as-is.
Linked exhibits (indictments, settlement agreements, full-text report PDFs) land
in a `<document>_attachments/` folder next to the page.

The run is resumable: anything already on disk is skipped unless --force.

Examples
--------
    python download.py                       # everything in the manifest
    python download.py --sources DOJ         # one source
    python download.py --workers 6           # more parallel Chrome instances
    python download.py --no-pdf              # HTML only (much faster)
"""

from __future__ import annotations

import argparse
import logging
import sys
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

from fraudscrape import browser, config, fetch
from fraudscrape.models import read_manifest

log = logging.getLogger("download")

_counter_lock = threading.Lock()
_counts = {"ok": 0, "skipped": 0, "partial": 0, "error": 0, "done": 0}


def _bump(status: str, total: int) -> None:
    with _counter_lock:
        _counts[status] = _counts.get(status, 0) + 1
        _counts["done"] += 1
        done = _counts["done"]
    if done % 25 == 0 or done == total:
        log.info("progress %s/%s  ok=%s skipped=%s partial=%s error=%s",
                 done, total, _counts["ok"], _counts["skipped"],
                 _counts["partial"], _counts["error"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sources", nargs="*", default=None)
    ap.add_argument("--years", nargs="*", default=None,
                    help="only documents published in these years, e.g. --years 2026 2025. "
                         "Use 'undated' for program/index pages that carry no date.")
    ap.add_argument("--workers", type=int, default=4,
                    help="parallel workers; each one runs its own headless Chrome")
    ap.add_argument("--limit", type=int, default=None, help="stop after N documents")
    ap.add_argument("--force", action="store_true", help="re-download files that already exist")
    ap.add_argument("--no-pdf", action="store_true", help="skip PDF rendering of HTML pages")
    ap.add_argument("--no-attachments", action="store_true",
                    help="do not follow links to PDFs/exhibits on the page")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    config.ensure_dirs()

    docs = read_manifest()
    if not docs:
        log.error("manifest is empty - run discover.py first")
        return 2
    if args.sources:
        wanted = set(args.sources)
        docs = [d for d in docs if d.source in wanted]
    if args.years:
        years = set(args.years)
        docs = [d for d in docs if d.year in years]
    if args.limit:
        docs = docs[: args.limit]
    if not docs:
        log.error("nothing to download for that filter")
        return 1

    by_year = Counter(d.year for d in docs)
    log.info("downloading %s documents with %s workers (pdf=%s)",
             len(docs), args.workers, not args.no_pdf)
    log.info("by year: %s", ", ".join(f"{y}={n}" for y, n in sorted(by_year.items())))
    started = time.time()
    records = []
    total = len(docs)
    try:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {
                pool.submit(
                    fetch.download, d,
                    force=args.force,
                    make_pdf=not args.no_pdf,
                    with_attachments=not args.no_attachments,
                ): d
                for d in docs
            }
            for fut in as_completed(futures):
                d = futures[fut]
                try:
                    rec = fut.result()
                except Exception as exc:  # noqa: BLE001
                    rec = {"source": d.source, "url": d.url, "status": "error",
                           "error": repr(exc)[:300]}
                records.append(rec)
                _bump(rec.get("status", "error"), total)
                if len(records) % 200 == 0:
                    fetch.append_log(records)
                    records = []
    except KeyboardInterrupt:
        log.warning("interrupted - flushing log")
    finally:
        if records:
            fetch.append_log(records)
        browser.shutdown()

    log.info("finished in %.1f min: ok=%s skipped=%s partial=%s error=%s",
             (time.time() - started) / 60, _counts["ok"], _counts["skipped"],
             _counts["partial"], _counts["error"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
