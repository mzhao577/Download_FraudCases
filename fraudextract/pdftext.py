"""PDF -> plain text."""

from __future__ import annotations

import logging
import re
from pathlib import Path

import pypdfium2

from . import config

log = logging.getLogger(__name__)

# The saved pages carry site chrome (nav, cookie banner, "An official website of
# the United States government", share widgets). Dropping it keeps the model on
# the press release itself and cuts input tokens by roughly a third.
_BOILERPLATE = re.compile(
    r"""^(?:
        skip\s+to\s+main\s+content | an\s+official\s+website\s+of\s+the\s+united\s+states\s+government |
        here'?s\s+how\s+you\s+know | official\s+websites\s+use\s+\.gov |
        secure\s+\.gov\s+websites\s+use\s+https | share | print | menu | search |
        breadcrumb | related\s+content | updated\s+\w+\s+\d{1,2},\s+\d{4} |
        \s*\d+\s* )$""",
    re.IGNORECASE | re.VERBOSE,
)


def clean(text: str) -> str:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or _BOILERPLATE.match(line):
            continue
        lines.append(line)
    out = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", out).strip()


def read_pdf(path: Path, max_chars: int = config.MAX_DOC_CHARS) -> str:
    """Extract the text of a PDF. Returns '' when nothing is extractable."""
    try:
        doc = pypdfium2.PdfDocument(str(path))
    except Exception as exc:  # noqa: BLE001
        log.warning("cannot open %s: %r", path.name, exc)
        return ""
    try:
        pages = []
        for i in range(len(doc)):
            try:
                pages.append(doc[i].get_textpage().get_text_range())
            except Exception as exc:  # noqa: BLE001
                log.debug("page %s of %s failed: %r", i, path.name, exc)
        text = clean("\n".join(pages))
    finally:
        doc.close()

    if len(text) > max_chars:
        log.info("%s truncated %s -> %s chars", path.name, len(text), max_chars)
        text = text[:max_chars]
    return text


def find_pdfs(directory: Path) -> list[Path]:
    return sorted(p for p in directory.rglob("*.pdf") if p.is_file())
