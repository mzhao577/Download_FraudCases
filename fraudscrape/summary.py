"""Build the download summary: documents per year and per source."""

from __future__ import annotations

import csv
import datetime as dt
import json
from collections import Counter, defaultdict
from pathlib import Path

from . import config
from .models import read_manifest

BINARY_SUFFIXES = {".pdf", ".csv", ".zip", ".xlsx", ".xls", ".doc", ".docx", ".txt"}


def scan() -> dict:
    """Walk ./downloaded and count what is actually on disk."""
    stats: dict[str, dict[str, dict]] = defaultdict(lambda: defaultdict(
        lambda: {"documents": 0, "html": 0, "pdf": 0, "other": 0,
                 "attachments": 0, "bytes": 0}
    ))
    doc_keys: dict[tuple[str, str], set] = defaultdict(set)

    if not config.DOWNLOAD_DIR.exists():
        return {}

    # layout is downloaded/<year>/<Source>/
    for year_dir in sorted(p for p in config.DOWNLOAD_DIR.iterdir() if p.is_dir()):
        year = year_dir.name
        for source_dir in sorted(p for p in year_dir.iterdir() if p.is_dir()):
            source = source_dir.name
            cell = stats[source][year]
            for path in source_dir.rglob("*"):
                if not path.is_file():
                    continue
                size = path.stat().st_size
                cell["bytes"] += size
                if "_attachments" in path.parent.name:
                    cell["attachments"] += 1
                    continue
                suffix = path.suffix.lower()
                if suffix == ".html":
                    cell["html"] += 1
                elif suffix == ".pdf":
                    cell["pdf"] += 1
                elif suffix in BINARY_SUFFIXES:
                    cell["other"] += 1
                doc_keys[(source, year)].add(path.stem)
            cell["documents"] = len(doc_keys[(source, year)])
    return {s: dict(y) for s, y in stats.items()}


def manifest_breakdown() -> dict:
    """Category / sub-source breakdown from the discovery manifest."""
    docs = read_manifest()
    by_cat: dict[str, Counter] = defaultdict(Counter)
    by_sub: dict[str, Counter] = defaultdict(Counter)
    by_year: dict[str, Counter] = defaultdict(Counter)
    for d in docs:
        by_cat[d.source][d.category or "unspecified"] += 1
        by_sub[d.source][d.subsource or "unspecified"] += 1
        by_year[d.source][d.year] += 1
    return {
        "manifest_total": len(docs),
        "categories": {k: dict(v) for k, v in by_cat.items()},
        "subsources": {k: dict(v.most_common(25)) for k, v in by_sub.items()},
        "manifest_by_year": {k: dict(sorted(v.items())) for k, v in by_year.items()},
    }


def _fmt_bytes(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} GB"


def build(write: bool = True) -> dict:
    fs = scan()
    extra = manifest_breakdown()
    years = sorted({y for src in fs.values() for y in src})
    sources = sorted(fs)

    matrix = {s: {y: fs[s].get(y, {}).get("documents", 0) for y in years} for s in sources}
    totals_by_year = {y: sum(matrix[s][y] for s in sources) for y in years}
    totals_by_source = {s: sum(matrix[s].values()) for s in sources}
    grand_total = sum(totals_by_source.values())

    files_total = Counter()
    for s in sources:
        for y in years:
            cell = fs[s].get(y)
            if cell:
                for k in ("html", "pdf", "other", "attachments", "bytes"):
                    files_total[k] += cell[k]

    reg = config.load_sources()
    result = {
        "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "coverage_start": reg.get("coverage_start"),
        "download_root": str(config.DOWNLOAD_DIR),
        "documents_total": grand_total,
        "documents_by_source": totals_by_source,
        "documents_by_year": totals_by_year,
        "documents_by_source_and_year": matrix,
        "files": dict(files_total),
        "detail": fs,
        **extra,
    }

    if write:
        config.SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
        (config.SUMMARY_DIR / "summary.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        _write_csv(config.SUMMARY_DIR / "summary.csv", fs, sources, years)
        md = render_markdown(result, sources, years, reg)
        (config.SUMMARY_DIR / "summary.md").write_text(md, encoding="utf-8")
        # Keep a copy where a reader will look for it first.
        (config.ROOT / "SUMMARY.md").write_text(md, encoding="utf-8")
    return result


def _write_csv(path: Path, fs: dict, sources: list[str], years: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["source", "year", "documents", "html_files", "pdf_files",
                    "other_files", "attachment_files", "bytes"])
        for s in sources:
            for y in years:
                c = fs[s].get(y)
                if not c:
                    continue
                w.writerow([s, y, c["documents"], c["html"], c["pdf"],
                            c["other"], c["attachments"], c["bytes"]])


def render_markdown(r: dict, sources: list[str], years: list[str], reg: dict) -> str:
    L = []
    A = L.append
    A("# Medical Fraud Case Download - Summary")
    A("")
    A(f"*Generated {r['generated_at']}*")
    A("")
    A(f"- Coverage window: **{r['coverage_start']} to today**")
    A(f"- Documents downloaded: **{r['documents_total']:,}**")
    f = r["files"]
    A(f"- Files on disk: **{f.get('html', 0):,} HTML**, **{f.get('pdf', 0):,} PDF**, "
      f"**{f.get('other', 0):,} other (CSV/XLS/ZIP)**, "
      f"**{f.get('attachments', 0):,} attachments** "
      f"({_fmt_bytes(f.get('bytes', 0))} total)")
    A(f"- Download root: `{r['download_root']}`")
    A("")

    A("## Documents by source and year")
    A("")
    A("| Source | " + " | ".join(years) + " | **Total** |")
    A("|---|" + "---|" * (len(years) + 1))
    m = r["documents_by_source_and_year"]
    for s in sources:
        row = [f"{m[s][y]:,}" if m[s][y] else "-" for y in years]
        A(f"| **{s}** | " + " | ".join(row) + f" | **{r['documents_by_source'][s]:,}** |")
    tot = [f"**{r['documents_by_year'][y]:,}**" for y in years]
    A("| **Total** | " + " | ".join(tot) + f" | **{r['documents_total']:,}** |")
    A("")

    A("## Files by source and year")
    A("")
    A("| Source | Year | Documents | HTML | PDF | Other | Attachments | Size |")
    A("|---|---|---|---|---|---|---|---|")
    for s in sources:
        for y in years:
            c = r["detail"][s].get(y)
            if not c:
                continue
            A(f"| {s} | {y} | {c['documents']:,} | {c['html']:,} | {c['pdf']:,} | "
              f"{c['other']:,} | {c['attachments']:,} | {_fmt_bytes(c['bytes'])} |")
    A("")

    A("## Document categories (from the discovery manifest)")
    A("")
    for s in sources:
        cats = r.get("categories", {}).get(s)
        if not cats:
            continue
        A(f"- **{s}**: " + ", ".join(f"{k} ({v:,})" for k, v in
                                     sorted(cats.items(), key=lambda kv: -kv[1])))
    A("")

    A("## Sources searched")
    A("")
    for s in reg["sources"]:
        mark = "" if s.get("enabled", True) else " *(disabled)*"
        A(f"### {s['key']} - {s['name']}{mark}")
        A("")
        A(s["why"])
        A("")
        for w in s["websites"]:
            A(f"- {w}")
        A("")
    if reg.get("considered_but_not_scraped"):
        A("### Considered but not scraped")
        A("")
        for s in reg["considered_but_not_scraped"]:
            A(f"- **{s['name']}** ({s['url']}) - {s['reason']}")
        A("")
    return "\n".join(L) + "\n"
