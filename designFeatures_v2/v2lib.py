"""Shared helpers for the designFeatures_v2 pipeline."""
from __future__ import annotations

import csv
import json
from pathlib import Path

import anthropic

MODEL = "claude-opus-5"
HERE = Path(__file__).resolve().parent

# Column names added to the input CSV. The first three are the elements the
# brief asks for; FeatureCategory carries the ~20-category grouping, which the
# brief also asks for but does not give a column of its own.
COL_SERVICE = "DesiredServiceGroups"
COL_WAYS = "WaysToIdentify"
COL_FEATURES = "FeaturesToCreate"
COL_CATEGORY = "FeatureCategory"


def load_rows(csv_path: Path) -> tuple[list[dict], list[str]]:
    with csv_path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        cols = list(reader.fieldnames or [])
        return [dict(r) for r in reader], cols


def write_rows(path: Path, rows: list[dict], cols: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def client() -> anthropic.Anthropic:
    return anthropic.Anthropic(max_retries=4, timeout=900)


def case_block(i: int, r: dict) -> str:
    return (f"[{i}] service={r.get('Service') or '-'} | types={r.get('FraudTypeAll') or '-'} | "
            f"payer={r.get('PayerName') or '-'}\n{(r.get('SchemeSummary') or '').strip()}")


def load_json(p: Path, default):
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return default


def save_json(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
