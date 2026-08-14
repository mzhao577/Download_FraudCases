"""Per-document field extraction with Claude."""

from __future__ import annotations

import hashlib
import json
import logging
import time
from pathlib import Path

import anthropic
from pydantic import ValidationError

from . import config, pdftext
from .schema import FRAUD_TYPE_GUIDE, FRAUD_TYPES, CaseRecord

log = logging.getLogger(__name__)

SYSTEM_PROMPT = f"""
You extract structured case data from U.S. medical / health care fraud documents
(DOJ and HHS-OIG press releases, indictments, settlement announcements). The
output feeds a model that predicts fraud against Medicare, Medicaid and
commercial payers, so precision matters more than completeness: a wrong value is
worse than a null.

Rules:
- Use only what the document states. Never infer, estimate, or fill from general
  knowledge. If the document does not say, the value is null.
- Dates are yyyy-mm-dd. A conduct period is "yyyy-mm to yyyy-mm".
- Money is a plain number of whole US dollars: $1.6 million -> 1600000.
- Keep the distinction between the amount defrauded and the amount paid back.
- Sentences are in months, and only when actually imposed. "Faces up to 10
  years" is not a sentence - that is null.
- One document describes one case. If it covers several defendants in the same
  scheme, that is still one case: list them all in FraudEntity, and roll their
  numbers up consistently - SettlementAmt is the total owed across defendants,
  JailTime is the longest custodial sentence imposed on any of them. Say in
  SchemeSummary when the figures span more than one defendant.

Fraud type taxonomy - this is a CLOSED set of {len(FRAUD_TYPES)} values:
{FRAUD_TYPE_GUIDE}

Never invent a label outside this list. Choose the type by the mechanism that
made the money, not by the statute charged: a case charged as wire fraud but
built on billing for visits that never happened is Phantom Claims. Use
"Other - Unknown" only when nothing in the list fits.
""".strip()


def _repair(data: dict) -> dict:
    """Coerce a nearly-valid record into a valid one.

    The model occasionally puts a Service value ('GeneticTesting') or an invented
    label into FraudType/FraudTypeAll despite the enum. Dropping the stray label
    keeps a document that is otherwise correct, instead of losing the whole
    record - and, before the fix, the whole run.
    """
    valid = set(FRAUD_TYPES)

    kept = [t for t in (data.get("FraudTypeAll") or []) if t in valid]
    dropped = [t for t in (data.get("FraudTypeAll") or []) if t not in valid]

    if data.get("FraudType") not in valid:
        dropped.append(data.get("FraudType"))
        data["FraudType"] = kept[0] if kept else "Other - Unknown"
    if data["FraudType"] not in kept:
        kept.insert(0, data["FraudType"])
    data["FraudTypeAll"] = kept or [data["FraudType"]]

    if dropped:
        data["_repaired"] = f"dropped out-of-taxonomy label(s): {dropped}"
    return data


def _client() -> anthropic.Anthropic:
    # Resolves ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN, or an `ant auth login`
    # profile, in that order.
    return anthropic.Anthropic(max_retries=4)


def _cache_path(path: Path, text: str) -> Path:
    key = hashlib.sha1(f"{path.name}:{len(text)}:{config.MODEL}".encode()).hexdigest()[:16]
    return config.CACHE_DIR / f"{path.stem[:80]}_{key}.json"


def extract_one(
    client: anthropic.Anthropic,
    path: Path,
    text: str | None = None,
    *,
    effort: str = config.EFFORT,
    force: bool = False,
) -> dict:
    """Extract one document. Returns a row dict, or a dict with an 'error' key.

    `text` must be supplied when calling this from a worker thread: PDFium is not
    thread-safe, so all PDF reading happens on one thread (see extract_all).
    """
    if text is None:
        text = pdftext.read_pdf(path)
    if not text:
        return {"DocumentName": path.name, "error": "no extractable text in PDF"}

    cache = _cache_path(path, text)
    if cache.exists() and not force:
        try:
            return json.loads(cache.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    user_content = (
        f"Source file: {path.name}\n\n"
        f"--- BEGIN DOCUMENT ---\n{text}\n--- END DOCUMENT ---"
    )
    # The system prompt is byte-identical across documents, so cache it: it is
    # the whole taxonomy and rule set, and it is re-sent on every request.
    system = [{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}]

    repaired_note = None
    for model in (config.MODEL, config.FALLBACK_MODEL):
        try:
            response = client.messages.parse(
                model=model,
                max_tokens=config.MAX_TOKENS,
                output_format=CaseRecord,
                output_config={"effort": effort},
                system=system,
                messages=[{"role": "user", "content": user_content}],
            )
        except ValidationError as exc:
            # The enum is in the schema, but the model can still return a label
            # outside it (typically a Service value leaking into FraudTypeAll).
            # Repair it rather than losing the document - and never let this
            # propagate: one bad record used to abort the entire run.
            log.warning("%s: schema violation on %s, repairing", path.name, model)
            record, repaired_note = _retry_repaired(
                client, model, system, user_content, effort, path
            )
            if record is None:
                if model == config.FALLBACK_MODEL:
                    return {"DocumentName": path.name,
                            "error": f"schema violation: {exc.errors()[:1]}"[:300]}
                continue
            row = {"DocumentName": path.name, **record.model_dump(),
                   "_repaired": repaired_note}
            _write_cache(cache, row)
            return row
        except anthropic.APIStatusError as exc:
            log.warning("%s: %s on %s", path.name, type(exc).__name__, model)
            if model == config.FALLBACK_MODEL:
                return {"DocumentName": path.name, "error": f"{type(exc).__name__}: {exc}"[:300]}
            continue
        except anthropic.APIConnectionError as exc:
            return {"DocumentName": path.name, "error": f"connection error: {exc!r}"[:300]}

        # Check the stop reason before touching content: a declined request
        # returns HTTP 200 with empty or partial content.
        if response.stop_reason == "refusal":
            detail = getattr(response.stop_details, "category", None)
            log.warning("%s: refused by %s (%s)", path.name, model, detail)
            if model == config.FALLBACK_MODEL:
                return {"DocumentName": path.name, "error": f"refused ({detail})"}
            continue

        record = response.parsed_output
        if record is None:
            if model == config.FALLBACK_MODEL:
                return {"DocumentName": path.name, "error": "no parsed output"}
            continue

        row = {"DocumentName": path.name, **record.model_dump()}
        row["_meta"] = {
            "model": response.model,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "cache_read_input_tokens": response.usage.cache_read_input_tokens,
            "source_chars": len(text),
        }
        _write_cache(cache, row)
        return row

    return {"DocumentName": path.name, "error": "all models failed"}


def _write_cache(cache: Path, row: dict) -> None:
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(row, indent=2, ensure_ascii=False), encoding="utf-8")


def _retry_repaired(client, model, system, user_content, effort, path):
    """Re-request the record as raw JSON, then coerce it into the taxonomy."""
    schema = CaseRecord.model_json_schema()
    schema["additionalProperties"] = False
    try:
        response = client.messages.create(
            model=model,
            max_tokens=config.MAX_TOKENS,
            output_config={"effort": effort,
                           "format": {"type": "json_schema", "schema": schema}},
            system=system,
            messages=[
                {"role": "user", "content": user_content},
                {"role": "system", "content":
                 "FraudType and FraudTypeAll accept ONLY the 18 taxonomy values. "
                 "A service type such as GeneticTesting or Laboratory belongs in "
                 "Service, never in FraudType or FraudTypeAll."},
            ],
        )
    except (anthropic.APIStatusError, anthropic.APIConnectionError) as exc:
        log.warning("%s: repair call failed: %r", path.name, exc)
        return None, None
    if response.stop_reason == "refusal":
        return None, None

    text = "".join(b.text for b in response.content if b.type == "text")
    try:
        data = _repair(json.loads(text))
        return CaseRecord.model_validate(data), data.get("_repaired")
    except (json.JSONDecodeError, ValidationError) as exc:
        log.warning("%s: repair failed: %r", path.name, str(exc)[:160])
        return None, None


def extract_all(
    paths: list[Path],
    *,
    effort: str = config.EFFORT,
    workers: int = 4,
    force: bool = False,
) -> list[dict]:
    """Extract every document. The first runs alone so the rest hit its cache."""
    from concurrent.futures import ThreadPoolExecutor

    client = _client()
    rows: list[dict] = []
    if not paths:
        return rows

    started = time.time()
    # PDFium is not thread-safe - concurrent reads raise "Failed to load page"
    # or kill the interpreter outright. Read every document up front on this
    # thread; only the API calls are parallelised below.
    texts = {p: pdftext.read_pdf(p) for p in paths}

    # A cache entry is only readable once the first response has been written,
    # so run one document alone before fanning out; otherwise all N requests
    # miss the cached system prompt.
    rows.append(extract_one(client, paths[0], texts[paths[0]], effort=effort, force=force))
    log.info("1/%s %s", len(paths), paths[0].name)

    rest = paths[1:]
    if rest:
        with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            futures = [
                pool.submit(extract_one, client, p, texts[p], effort=effort, force=force)
                for p in rest
            ]
            for i, fut in enumerate(futures, start=2):
                try:
                    row = fut.result()
                except Exception as exc:  # noqa: BLE001
                    # Last line of defence. Whatever goes wrong on one document,
                    # the other 678 must still be written out.
                    log.exception("unhandled error on %s", rest[i - 2].name)
                    row = {"DocumentName": rest[i - 2].name,
                           "error": f"{type(exc).__name__}: {exc}"[:300]}
                rows.append(row)
                log.info("%s/%s %s%s", i, len(paths), rest[i - 2].name,
                         "  [ERROR]" if "error" in row else "")

    log.info("extracted %s documents in %.1f min", len(rows), (time.time() - started) / 60)
    return rows
