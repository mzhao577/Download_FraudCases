#!/usr/bin/env python3
"""Run the whole pipeline: discover -> download -> summarize.

    python run_all.py                    # full run (hours; resumable)
    python run_all.py --limit 20         # smoke test, 20 documents per source
    python run_all.py --sources DOJ FBI
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(script: str, extra: list[str]) -> int:
    cmd = [sys.executable, str(ROOT / script), *extra]
    print(f"\n$ {' '.join(cmd)}\n", flush=True)
    return subprocess.call(cmd)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sources", nargs="*", default=None)
    ap.add_argument("--since", default=None)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--no-pdf", action="store_true")
    ap.add_argument("--skip-discovery", action="store_true")
    args = ap.parse_args()

    common: list[str] = []
    if args.sources:
        common += ["--sources", *args.sources]

    if not args.skip_discovery:
        disc = list(common)
        if args.since:
            disc += ["--since", args.since]
        if args.limit:
            disc += ["--limit", str(args.limit)]
        rc = run("discover.py", disc)
        if rc != 0:
            return rc

    dl = list(common) + ["--workers", str(args.workers)]
    if args.limit:
        dl += ["--limit", str(args.limit * max(1, len(args.sources or [1, 2, 3, 4, 5])))]
    if args.no_pdf:
        dl.append("--no-pdf")
    rc = run("download.py", dl)
    if rc != 0:
        return rc

    return run("summarize.py", [])


if __name__ == "__main__":
    sys.exit(main())
