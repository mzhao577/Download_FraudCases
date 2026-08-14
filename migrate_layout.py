#!/usr/bin/env python3
"""One-off: move an existing corpus from downloaded/<Source>/<year>/ to
downloaded/<year>/<Source>/.

Safe to run twice - anything already in the new layout is left alone. Nothing is
re-downloaded; files are moved on disk.
"""

from __future__ import annotations

import argparse
import shutil
import sys

from fraudscrape import config

KNOWN_SOURCES = {"DOJ", "HHS-OIG", "FBI", "CMS", "GAO"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = config.DOWNLOAD_DIR
    if not root.exists():
        print("nothing to migrate")
        return 0

    moves = []
    for top in sorted(p for p in root.iterdir() if p.is_dir()):
        if top.name not in KNOWN_SOURCES:
            continue                      # already a year directory
        for year_dir in sorted(p for p in top.iterdir() if p.is_dir()):
            moves.append((year_dir, root / year_dir.name / top.name))

    if not moves:
        print("already in downloaded/<year>/<Source>/ layout")
        return 0

    print(f"{len(moves)} directories to move")
    for src, dst in moves:
        rel_s = src.relative_to(root)
        rel_d = dst.relative_to(root)
        n = sum(1 for _ in src.rglob("*") if _.is_file())
        print(f"  {rel_s}  ->  {rel_d}   ({n:,} files)")
        if args.dry_run:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            for item in src.iterdir():     # merge into an existing target
                target = dst / item.name
                if target.exists():
                    shutil.rmtree(target) if target.is_dir() else target.unlink()
                shutil.move(str(item), str(target))
            src.rmdir()
        else:
            shutil.move(str(src), str(dst))

    if not args.dry_run:
        for top in sorted(p for p in root.iterdir() if p.is_dir()):
            if top.name in KNOWN_SOURCES and not any(top.iterdir()):
                top.rmdir()
        print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
