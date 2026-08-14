"""Find and load the case datasets that back the web tool.

Input convention (instruction_APIAnalisys.md):

    <input dir>/
        DOJ_2025/                             raw PDFs, one per case
        extractedSummary_2025_DOJ.csv         one row per PDF

The folder name and the CSV name have to refer to the same dataset. The brief
calls the shared part "DOJ_2025" while the example CSV spells it "2025_DOJ", so
matching is done on the set of tokens rather than on the literal string - a
folder matches a CSV when every token of the folder name appears in the CSV
name, in any order.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

# The column carrying the PDF filename, and the column shown at the top of the
# right-hand panel. Matched case-insensitively: the brief writes "schemeSummary"
# and the extractor emits "SchemeSummary".
DOC_COLUMN = "DocumentName"
SUMMARY_COLUMN = "SchemeSummary"
TITLE_COLUMNS = ("DocumentName", "FraudType")


def tokens(name: str) -> set[str]:
    return {t.lower() for t in re.split(r"[^A-Za-z0-9]+", name) if t}


@dataclass
class Dataset:
    key: str                      # e.g. "DOJ_2025"
    pdf_dir: Path
    csv_path: Path
    rows: list[dict] = field(default_factory=list)
    columns: list[str] = field(default_factory=list)
    missing_pdf: list[str] = field(default_factory=list)
    orphan_pdfs: list[str] = field(default_factory=list)

    @property
    def doc_column(self) -> str:
        return _resolve(self.columns, DOC_COLUMN) or DOC_COLUMN

    @property
    def summary_column(self) -> str | None:
        return _resolve(self.columns, SUMMARY_COLUMN)

    def title_columns(self) -> list[str]:
        return [c for c in (_resolve(self.columns, t) for t in TITLE_COLUMNS) if c]

    def pdf_for(self, filename: str) -> Path | None:
        """Resolve a PDF, refusing anything outside the dataset's folder."""
        if filename not in self._pdf_names:
            return None
        candidate = (self.pdf_dir / filename).resolve()
        # Defence in depth: the name came from the CSV, but never let a crafted
        # value escape the dataset directory.
        if not str(candidate).startswith(str(self.pdf_dir.resolve())):
            return None
        return candidate if candidate.is_file() else None

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
        }


def _resolve(columns: list[str], wanted: str) -> str | None:
    """Case-insensitive column lookup."""
    lowered = {c.lower(): c for c in columns}
    return lowered.get(wanted.lower())


def discover(input_dir: Path) -> list[Dataset]:
    """Pair every PDF subfolder in `input_dir` with its summary CSV."""
    input_dir = input_dir.expanduser().resolve()
    if not input_dir.is_dir():
        raise FileNotFoundError(f"input folder not found: {input_dir}")

    csvs = sorted(input_dir.glob("*.csv"))
    subdirs = sorted(p for p in input_dir.iterdir() if p.is_dir())

    found: list[Dataset] = []
    for sub in subdirs:
        if not any(sub.glob("*.pdf")):
            continue
        want = tokens(sub.name)
        matches = [c for c in csvs if want <= tokens(c.stem)]
        if not matches:
            continue
        # Prefer the closest name when several CSVs match.
        matches.sort(key=lambda c: len(tokens(c.stem) - want))
        found.append(Dataset(key=sub.name, pdf_dir=sub, csv_path=matches[0]).load())
    return found


def describe_problem(input_dir: Path) -> str:
    """A specific message for why discovery found nothing."""
    input_dir = input_dir.expanduser().resolve()
    if not input_dir.is_dir():
        return f"input folder does not exist: {input_dir}"
    subdirs = [p.name for p in input_dir.iterdir() if p.is_dir()]
    csvs = [p.name for p in input_dir.glob("*.csv")]
    with_pdfs = [d for d in subdirs if any((input_dir / d).glob("*.pdf"))]
    lines = [f"no dataset found in {input_dir}", ""]
    lines.append(f"  subfolders          : {', '.join(subdirs) or '(none)'}")
    lines.append(f"  ...containing PDFs  : {', '.join(with_pdfs) or '(none)'}")
    lines.append(f"  CSV files           : {', '.join(csvs) or '(none)'}")
    lines.append("")
    if not with_pdfs:
        lines.append("  Add a subfolder of PDFs, e.g. DOJ_2025/")
    elif not csvs:
        lines.append("  Add the summary CSV, e.g. extractedSummary_2025_DOJ.csv")
    else:
        lines.append("  The names do not match. Every token of the folder name must")
        lines.append("  appear in the CSV name, e.g. DOJ_2025/ + extractedSummary_2025_DOJ.csv")
    return "\n".join(lines)
