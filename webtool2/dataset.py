"""Find and load the case datasets that back webtool2.

Input convention (instruction_APIAnalisys.md):

    <input dir>/
        DOJ_2025/                                     raw PDFs, one per case
        extractedSummary_2025_DOJ_withFeatures.csv    one row per PDF

The folder name and the CSV name must refer to the same dataset. Matching is on
the SET OF TOKENS rather than the literal string - every token of the folder name
has to appear in the CSV name, in any order - so `DOJ_2025/` pairs with
`extractedSummary_2025_DOJ.csv` and equally with the `_withFeatures` variant.

Difference from webtool v1: any columns that come AFTER the summary column in the
CSV are treated as *highlight* columns and rendered immediately below the summary
rather than in the general field table. For the v2 file that is
DesiredServiceGroups, WaysToIdentify, FeaturesToCreate and FeatureCategory - the
prevention design, which is the thing being reviewed.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

DOC_COLUMN = "DocumentName"
SUMMARY_COLUMN = "SchemeSummary"
TITLE_COLUMNS = ("DocumentName", "FraudType")
# Columns offered as the tab dimension, in order of preference.
TAB_COLUMNS = ("FeatureCategory", "FraudType", "Service", "CaseStatus")


def tokens(name: str) -> set[str]:
    return {t.lower() for t in re.split(r"[^A-Za-z0-9]+", name) if t}


def _resolve(columns: list[str], wanted: str) -> str | None:
    """Case-insensitive column lookup."""
    return {c.lower(): c for c in columns}.get(wanted.lower())


@dataclass
class Dataset:
    key: str
    pdf_dir: Path
    csv_path: Path
    rows: list[dict] = field(default_factory=list)
    columns: list[str] = field(default_factory=list)
    missing_pdf: list[str] = field(default_factory=list)
    orphan_pdfs: list[str] = field(default_factory=list)

    # ---------------------------------------------------------------- columns
    @property
    def doc_column(self) -> str:
        return _resolve(self.columns, DOC_COLUMN) or DOC_COLUMN

    @property
    def summary_column(self) -> str | None:
        return _resolve(self.columns, SUMMARY_COLUMN)

    def title_columns(self) -> list[str]:
        return [c for c in (_resolve(self.columns, t) for t in TITLE_COLUMNS) if c]

    def highlight_columns(self) -> list[str]:
        """Columns after the summary column - shown directly below it."""
        s = self.summary_column
        if not s or s not in self.columns:
            return []
        return self.columns[self.columns.index(s) + 1:]

    def tab_columns(self) -> list[str]:
        """Columns worth driving the tab strip, those actually present."""
        return [c for c in (_resolve(self.columns, t) for t in TAB_COLUMNS) if c]

    # ------------------------------------------------------------------ files
    def pdf_for(self, filename: str) -> Path | None:
        if filename not in self._pdf_names:
            return None
        candidate = (self.pdf_dir / filename).resolve()
        # Defence in depth: the name came from the CSV, but never let a crafted
        # value escape the dataset directory.
        if not str(candidate).startswith(str(self.pdf_dir.resolve())):
            return None
        return candidate if candidate.is_file() else None

    # ------------------------------------------------------------------- load
    def load(self) -> "Dataset":
        with self.csv_path.open(newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            self.columns = list(reader.fieldnames or [])
            self.rows = [dict(r) for r in reader]

        self._pdf_names = {p.name for p in self.pdf_dir.glob("*.pdf")}
        doc_col = self.doc_column
        referenced = set()
        for i, row in enumerate(self.rows):
            name = (row.get(doc_col) or "").strip()
            row["_index"] = i
            row["_has_pdf"] = name in self._pdf_names
            referenced.add(name)
            if not row["_has_pdf"]:
                self.missing_pdf.append(name or f"<row {i} has no {doc_col}>")
        self.orphan_pdfs = sorted(self._pdf_names - referenced)
        return self

    def summary(self) -> dict:
        return {
            "key": self.key,
            "cases": len(self.rows),
            "pdfs": len(self._pdf_names),
            "missing_pdf": len(self.missing_pdf),
            "orphan_pdfs": len(self.orphan_pdfs),
            "columns": self.columns,
            "doc_column": self.doc_column,
            "summary_column": self.summary_column,
            "title_columns": self.title_columns(),
            "highlight_columns": self.highlight_columns(),
            "tab_columns": self.tab_columns(),
        }


def discover(input_dir: Path) -> list[Dataset]:
    input_dir = input_dir.expanduser().resolve()
    if not input_dir.is_dir():
        raise FileNotFoundError(f"input folder not found: {input_dir}")

    csvs = sorted(input_dir.glob("*.csv"))
    found: list[Dataset] = []
    for sub in sorted(p for p in input_dir.iterdir() if p.is_dir()):
        if not any(sub.glob("*.pdf")):
            continue
        want = tokens(sub.name)
        matches = [c for c in csvs if want <= tokens(c.stem)]
        if not matches:
            continue
        # Prefer the richest matching CSV: with both extractedSummary_2025_DOJ
        # and ..._withFeatures present, the longer name is the fuller file.
        matches.sort(key=lambda c: -len(tokens(c.stem)))
        found.append(Dataset(key=sub.name, pdf_dir=sub, csv_path=matches[0]).load())
    return found


def describe_problem(input_dir: Path) -> str:
    input_dir = input_dir.expanduser().resolve()
    if not input_dir.is_dir():
        return f"input folder does not exist: {input_dir}"
    subdirs = [p.name for p in input_dir.iterdir() if p.is_dir()]
    csvs = [p.name for p in input_dir.glob("*.csv")]
    with_pdfs = [d for d in subdirs if any((input_dir / d).glob("*.pdf"))]
    lines = [f"no dataset found in {input_dir}", "",
             f"  subfolders          : {', '.join(subdirs) or '(none)'}",
             f"  ...containing PDFs  : {', '.join(with_pdfs) or '(none)'}",
             f"  CSV files           : {', '.join(csvs) or '(none)'}", ""]
    if not with_pdfs:
        lines.append("  Add a subfolder of PDFs, e.g. DOJ_2025/")
    elif not csvs:
        lines.append("  Add the summary CSV, e.g. extractedSummary_2025_DOJ_withFeatures.csv")
    else:
        lines.append("  The names do not match. Every token of the folder name must")
        lines.append("  appear in the CSV name, e.g. DOJ_2025/ + ..._2025_DOJ_withFeatures.csv")
    return "\n".join(lines)
