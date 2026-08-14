#!/usr/bin/env python3
"""Step 1 - find every medical / health care fraud document published since the
cut-off date by the sources listed in sources.json, and write state/manifest.jsonl.

Examples
--------
    python discover.py                       # all enabled sources, from 2021-01-01
    python discover.py --sources DOJ FBI     # just those two
    python discover.py --since 2023-01-01
    python discover.py --limit 50            # quick smoke test (per source)
"""

from __future__ import annotations

import argparse
import datetime as dt
import logging
import sys
import time

from fraudscrape import browser, config
from fraudscrape.discovery import REGISTRY
from fraudscrape.models import dedupe, read_manifest, write_manifest

log = logging.getLogger("discover")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sources", nargs="*", default=None,
                    help="source keys to run (default: every enabled source in sources.json)")
    ap.add_argument("--since", default=config.DEFAULT_SINCE.isoformat(),
                    help="earliest publication date to keep (yyyy-mm-dd)")
    ap.add_argument("--limit", type=int, default=None,
                    help="stop after N documents per source (smoke testing)")
    ap.add_argument("--append", action="store_true",
                    help="merge into the existing manifest instead of replacing it")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    config.ensure_dirs()

    since = dt.date.fromisoformat(args.since)
    keys = args.sources or config.source_keys()
    unknown = [k for k in keys if k not in REGISTRY]
    if unknown:
        log.error("unknown source key(s): %s (known: %s)", unknown, sorted(REGISTRY))
        return 2

    docs = read_manifest() if args.append else []
    for key in keys:
        started = time.time()
        log.info("=" * 70)
        log.info("discovering %s (since %s)", key, since)
        try:
            found = REGISTRY[key](since=since, limit=args.limit)
        except KeyboardInterrupt:
            raise
        except Exception:  # noqa: BLE001
            log.exception("%s discovery failed - continuing with the other sources", key)
            continue
        # keep undated items (program/index pages) but drop anything too old
        kept = [d for d in found
                if not d.date or dt.date.fromisoformat(d.date) >= since]
        docs += kept
        log.info("%s: %s kept in %.1f min", key, len(kept), (time.time() - started) / 60)
        # Write after every source, not just at the end, so download.py can start
        # working on what is already found while the remaining sources are walked.
        write_manifest(dedupe(docs))
        log.info("manifest updated: %s documents so far", len(docs))

    docs = dedupe(docs)
    path = write_manifest(docs)
    log.info("=" * 70)
    log.info("manifest: %s documents -> %s", len(docs), path)
    by_source: dict[str, int] = {}
    for d in docs:
        by_source[d.source] = by_source.get(d.source, 0) + 1
    for k, v in sorted(by_source.items()):
        log.info("   %-10s %6d", k, v)
    browser.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
