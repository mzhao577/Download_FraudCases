"""The Doc record and manifest read/write helpers."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import unicodedata
from dataclasses import asdict, dataclass, field
from pathlib import Path

from . import config


@dataclass
class Doc:
    """One document we intend to (or did) download."""

    source: str                 # DOJ, HHS-OIG, FBI, CMS, GAO -> folder under downloaded/
    url: str                    # canonical URL of the document
    title: str = ""
    date: str = ""              # ISO yyyy-mm-dd, "" when unknown
    doc_type: str = "html"      # html | pdf | csv | zip ...
    category: str = ""          # press release, enforcement action, report, ...
    subsource: str = ""         # e.g. USAO-SDTX, FBI Detroit, MFCU
    summary: str = ""
    extra: dict = field(default_factory=dict)

    # ---- derived ---------------------------------------------------------
    @property
    def year(self) -> str:
        return self.date[:4] if self.date[:4].isdigit() else "undated"

    @property
    def doc_id(self) -> str:
        return hashlib.sha1(self.url.encode("utf-8")).hexdigest()[:12]

    @property
    def slug(self) -> str:
        base = slugify(self.title) or slugify(self.url.rstrip("/").rsplit("/", 1)[-1])
        return f"{base[:110]}_{self.doc_id}" if base else self.doc_id

    def dest_dir(self) -> Path:
        # year first, then source: downloaded/2026/FBI/
        return config.DOWNLOAD_DIR / self.year / self.source

    def dest_base(self) -> Path:
        return self.dest_dir() / self.slug

    def to_json(self) -> dict:
        return asdict(self)

    @classmethod
    def from_json(cls, d: dict) -> "Doc":
        known = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in d.items() if k in known})


_slug_bad = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return _slug_bad.sub("-", text.lower()).strip("-")


# --------------------------------------------------------------------------
# date parsing
# --------------------------------------------------------------------------
_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}
_PATTERNS = [
    re.compile(r"(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})"),
    re.compile(r"(?P<m>\d{1,2})/(?P<d>\d{1,2})/(?P<y>\d{4})"),
    re.compile(
        r"(?P<mon>[A-Za-z]{3,9})\.?\s+(?P<d>\d{1,2}),?\s+(?P<y>\d{4})"
    ),
    re.compile(r"(?P<d>\d{1,2})\s+(?P<mon>[A-Za-z]{3,9})\.?\s+(?P<y>\d{4})"),
]


def parse_date(text: str | None) -> str:
    """Best-effort date parse -> 'yyyy-mm-dd' or ''."""
    if not text:
        return ""
    text = text.strip()
    for pat in _PATTERNS:
        m = pat.search(text)
        if not m:
            continue
        g = m.groupdict()
        try:
            if g.get("mon"):
                mon = _MONTHS.get(g["mon"][:4].lower().rstrip(".")) or _MONTHS.get(
                    g["mon"][:3].lower()
                )
                if not mon:
                    continue
                return dt.date(int(g["y"]), mon, int(g["d"])).isoformat()
            return dt.date(int(g["y"]), int(g["m"]), int(g["d"])).isoformat()
        except ValueError:
            continue
    return ""


# --------------------------------------------------------------------------
# manifest
# --------------------------------------------------------------------------

def write_manifest(docs: list[Doc], path: Path | None = None) -> Path:
    path = path or config.MANIFEST_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for d in docs:
            fh.write(json.dumps(d.to_json(), ensure_ascii=False) + "\n")
    return path


def read_manifest(path: Path | None = None) -> list[Doc]:
    path = path or config.MANIFEST_FILE
    if not path.exists():
        return []
    out = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(Doc.from_json(json.loads(line)))
    return out


def _score(d: Doc) -> tuple:
    # prefer the copy with a date, a title, more summary text, and - for DOJ -
    # the Office of Public Affairs URL over a district mirror of the same release
    return (bool(d.date), bool(d.title), "/opa/pr/" in d.url, len(d.summary))


def dedupe(docs: list[Doc]) -> list[Doc]:
    """Collapse duplicates, keeping the record with the most metadata.

    Two passes, because agencies republish the same release twice: DOJ posts many
    press releases under both `/opa/pr/...` and the district office's own
    `/usao-xx/pr/...` URL, so a URL-only key would save the same document twice.
    """
    by_url: dict[str, Doc] = {}
    for d in docs:
        key = d.url.split("#")[0].rstrip("/")
        cur = by_url.get(key)
        if cur is None or _score(d) > _score(cur):
            by_url[key] = d

    by_title: dict[tuple, Doc] = {}
    out: list[Doc] = []
    for d in by_url.values():
        if not (d.title and d.date):
            out.append(d)
            continue
        key = (d.source, d.date, slugify(d.title)[:90])
        cur = by_title.get(key)
        if cur is None or _score(d) > _score(cur):
            by_title[key] = d
    return out + list(by_title.values())
