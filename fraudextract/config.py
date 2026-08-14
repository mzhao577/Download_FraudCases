"""Paths and model settings for the pattern-extraction pipeline."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Input: one PDF per fraud case (instruction_findpattern.txt).
DEFAULT_INPUT_DIR = ROOT / "downloaded" / "testdata_DOJ_2026"

EXTRACTED_ROOT = ROOT / "extracted"

OUTPUT_DIR = EXTRACTED_ROOT
CACHE_DIR = OUTPUT_DIR / ".cache"          # one JSON per document, for resuming

CASES_CSV = OUTPUT_DIR / "cases.csv"
CASES_JSON = OUTPUT_DIR / "cases.json"
PATTERNS_MD = OUTPUT_DIR / "patterns.md"
ERRORS_JSON = OUTPUT_DIR / "errors.json"


def set_output_dir(path) -> Path:
    """Point every output at `path`.

    The other modules read these as `config.NAME` at call time, so rebinding the
    module globals here redirects the whole run. The per-document cache moves
    with the outputs, so each input folder keeps its own resumable state.
    """
    global OUTPUT_DIR, CACHE_DIR, CASES_CSV, CASES_JSON, PATTERNS_MD, ERRORS_JSON
    OUTPUT_DIR = Path(path).expanduser().resolve()
    CACHE_DIR = OUTPUT_DIR / ".cache"
    CASES_CSV = OUTPUT_DIR / "cases.csv"
    CASES_JSON = OUTPUT_DIR / "cases.json"
    PATTERNS_MD = OUTPUT_DIR / "patterns.md"
    ERRORS_JSON = OUTPUT_DIR / "errors.json"
    return OUTPUT_DIR

MODEL = "claude-opus-5"
# Extraction is a bounded reading task, not open-ended reasoning: medium effort
# matches it and keeps the per-document cost down. Raise with --effort for
# longer or messier source documents.
EFFORT = "medium"
MAX_TOKENS = 16000                          # caps thinking + output on Opus 5

# If the safety classifiers decline a document, retry it once here. Handled
# client-side: this SDK build has no server-side `fallbacks` parameter.
FALLBACK_MODEL = "claude-opus-4-8"

# Characters of document text sent per request. These press releases run 3-8k
# characters; the cap is a guard against an unexpectedly long attachment.
MAX_DOC_CHARS = 120_000
