"""Download one Doc: save the HTML, render a PDF of it, grab its attachments."""

from __future__ import annotations

import datetime as dt
import html as html_mod
import json
import logging
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from . import browser, config, net, pagefetch
from .models import Doc, slugify

log = logging.getLogger(__name__)

BINARY_TYPES = {"pdf", "csv", "zip", "xlsx", "xls", "doc", "docx", "txt"}
ATTACHMENT_EXT = re.compile(r"\.(pdf|xlsx?|docx?|csv|zip)(\?|$)", re.IGNORECASE)
MAX_ATTACHMENTS = 12


# --------------------------------------------------------------------------
# HTML post-processing
# --------------------------------------------------------------------------

_CANONICAL = re.compile(
    r"""<link[^>]+rel=["']canonical["'][^>]+href=["'](https?://[^"']+)""", re.IGNORECASE
)


def _effective_url(raw: str, doc: Doc) -> str:
    """The URL the saved page really came from.

    Matters when a source syndicates another agency's release: several FBI
    press-release URLs, for instance, redirect to justice.gov, and the saved copy
    needs the destination as its <base> or its stylesheets and images break.
    """
    m = _CANONICAL.search(raw[:20000])
    return m.group(1) if m else doc.url


def _prepare_html(raw: str, doc: Doc) -> str:
    """Add a provenance comment and a <base> tag so the saved copy renders."""
    stamp = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    effective = _effective_url(raw, doc)
    banner = (
        "<!-- Downloaded by fraudscrape (Download_FraudCases)\n"
        f"     source        : {doc.source}\n"
        f"     url           : {doc.url}\n"
        + (f"     resolved_url  : {effective}\n" if effective != doc.url else "")
        + f"     title         : {html_mod.escape(doc.title)}\n"
        f"     published     : {doc.date or 'unknown'}\n"
        f"     category      : {doc.category}\n"
        f"     retrieved_at  : {stamp}\n"
        "-->\n"
    )
    base_tag = f'<base href="{html_mod.escape(effective, quote=True)}">'
    if re.search(r"<base\s", raw, re.IGNORECASE):
        base_tag = ""
    if re.search(r"<head[^>]*>", raw, re.IGNORECASE):
        raw = re.sub(r"(<head[^>]*>)", r"\1" + base_tag, raw, count=1, flags=re.IGNORECASE)
    else:
        raw = base_tag + raw
    return banner + raw


DOJ_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<base href="{url}">
<title>{title}</title>
<style>
 body{{font-family:Georgia,'Times New Roman',serif;max-width:46em;margin:2.5em auto;
      padding:0 1.5em;line-height:1.55;color:#1b1b1b}}
 h1{{font-size:1.6em;line-height:1.25}}
 .meta{{font-size:.85em;color:#555;border-bottom:1px solid #ccc;padding-bottom:1em;margin-bottom:1.5em}}
 .meta div{{margin:.15em 0}}
 .src{{margin-top:2.5em;font-size:.8em;color:#666;border-top:1px solid #ccc;padding-top:1em}}
</style></head><body>
<h1>{title}</h1>
<div class="meta">
 <div><strong>Source:</strong> U.S. Department of Justice{component}</div>
 <div><strong>Date:</strong> {date}</div>
 {number}
 {topics}
</div>
{body}
<div class="src">Retrieved from <a href="{url}">{url}</a> via the justice.gov press-release API on {stamp}.</div>
</body></html>
"""


def _doj_fallback_html(doc: Doc) -> str | None:
    body = (doc.extra or {}).get("api_body")
    if not body:
        return None
    comp = f" &mdash; {html_mod.escape(doc.subsource)}" if doc.subsource else ""
    num = (doc.extra or {}).get("release_number")
    topics = (doc.extra or {}).get("topics") or []
    return DOJ_TEMPLATE.format(
        url=html_mod.escape(doc.url, quote=True),
        title=html_mod.escape(doc.title or doc.url),
        component=comp,
        date=doc.date or "unknown",
        number=f"<div><strong>Release number:</strong> {html_mod.escape(num)}</div>" if num else "",
        topics=f"<div><strong>Topics:</strong> {html_mod.escape(', '.join(topics))}</div>" if topics else "",
        body=body,
        stamp=dt.datetime.now().astimezone().isoformat(timespec="seconds"),
    )


# --------------------------------------------------------------------------
# attachments
# --------------------------------------------------------------------------

def _attachment_urls(html: str, page_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    host = urlparse(page_url).netloc
    out, seen = [], set()
    for a in soup.find_all("a", href=True):
        href = urljoin(page_url, a["href"])
        if not ATTACHMENT_EXT.search(href):
            continue
        netloc = urlparse(href).netloc
        # keep only files published by the same agency (avoid crawling outward)
        if netloc and netloc != host and not netloc.endswith(".gov"):
            continue
        if href in seen:
            continue
        seen.add(href)
        out.append(href)
        if len(out) >= MAX_ATTACHMENTS:
            break
    return out


def _binary(url: str, referer: str | None = None) -> bytes | None:
    """Plain HTTP first; fall back to the browser for bot-walled hosts."""
    host = url.split("/")[2].lower() if "://" in url else ""
    if host not in pagefetch.BROWSER_ONLY_HOSTS:
        data = net.get_bytes(url, timeout=300)
        if data:
            return data
    return browser.fetch_binary(url, referer=referer)


def _save_attachments(doc: Doc, html: str, base: Path) -> list[str]:
    saved = []
    urls = _attachment_urls(html, doc.url)
    if not urls:
        return saved
    outdir = base.parent / f"{base.name}_attachments"
    for url in urls:
        name = slugify(Path(urlparse(url).path).stem)[:90] or "attachment"
        ext = Path(urlparse(url).path).suffix.lower() or ".pdf"
        target = outdir / f"{name}{ext}"
        if target.exists() and target.stat().st_size > 0:
            saved.append(str(target.relative_to(config.DOWNLOAD_DIR)))
            continue
        data = _binary(url, referer=doc.url)
        if not data or len(data) < 512:
            continue
        outdir.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        saved.append(str(target.relative_to(config.DOWNLOAD_DIR)))
    return saved


# --------------------------------------------------------------------------
# main entry point
# --------------------------------------------------------------------------

def download(doc: Doc, *, force: bool = False, make_pdf: bool = True,
             with_attachments: bool = True) -> dict:
    """Fetch and save one document. Returns a status record for the log."""
    rec = {
        "source": doc.source,
        "url": doc.url,
        "title": doc.title,
        "date": doc.date,
        "year": doc.year,
        "category": doc.category,
        "subsource": doc.subsource,
        "status": "error",
        "files": [],
        "attachments": [],
        "error": "",
        "fetched_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    base = doc.dest_base()
    base.parent.mkdir(parents=True, exist_ok=True)

    try:
        if doc.doc_type.lower() in BINARY_TYPES:
            return _download_binary(doc, base, rec, force=force)
        return _download_html(doc, base, rec, force=force, make_pdf=make_pdf,
                              with_attachments=with_attachments)
    except Exception as exc:  # noqa: BLE001
        rec["error"] = repr(exc)[:300]
        log.warning("download failed %s: %r", doc.url, exc)
        return rec


def _download_binary(doc: Doc, base: Path, rec: dict, *, force: bool) -> dict:
    ext = doc.doc_type.lower()
    target = base.with_suffix(f".{ext}")
    if target.exists() and target.stat().st_size > 0 and not force:
        rec["status"] = "skipped"
        rec["files"] = [str(target.relative_to(config.DOWNLOAD_DIR))]
        return rec
    data = _binary(doc.url)
    if not data:
        rec["error"] = "binary download failed"
        return rec
    target.write_bytes(data)
    rec["status"] = "ok"
    rec["files"] = [str(target.relative_to(config.DOWNLOAD_DIR))]
    rec["bytes"] = len(data)
    return rec


def _download_html(doc: Doc, base: Path, rec: dict, *, force: bool, make_pdf: bool,
                   with_attachments: bool) -> dict:
    html_path = base.with_suffix(".html")
    pdf_path = base.with_suffix(".pdf")

    have_html = html_path.exists() and html_path.stat().st_size > 0
    have_pdf = pdf_path.exists() and pdf_path.stat().st_size > 0
    if have_html and (have_pdf or not make_pdf) and not force:
        rec["status"] = "skipped"
        rec["files"] = [str(p.relative_to(config.DOWNLOAD_DIR))
                        for p in (html_path, pdf_path) if p.exists()]
        return rec

    raw = None
    if have_html and not force:
        raw = html_path.read_text(encoding="utf-8", errors="replace")
        prepared = raw
    else:
        raw = pagefetch.fetch(doc.url, force=force)
        if raw is None and doc.source == "DOJ":
            fallback = _doj_fallback_html(doc)
            if fallback:
                raw = fallback
                rec["note"] = "rebuilt from justice.gov API body (page fetch blocked)"
        if raw is None:
            rec["error"] = "html fetch failed"
            return rec
        prepared = raw if rec.get("note") else _prepare_html(raw, doc)
        html_path.write_text(prepared, encoding="utf-8", errors="replace")

    rec["files"].append(str(html_path.relative_to(config.DOWNLOAD_DIR)))

    if make_pdf and (force or not have_pdf):
        pdf = browser.pdf_from_file(html_path.resolve())
        if pdf and len(pdf) > 800:
            pdf_path.write_bytes(pdf)
            rec["files"].append(str(pdf_path.relative_to(config.DOWNLOAD_DIR)))
        else:
            rec["error"] = "pdf render failed"
    elif have_pdf:
        rec["files"].append(str(pdf_path.relative_to(config.DOWNLOAD_DIR)))

    if with_attachments:
        rec["attachments"] = _save_attachments(doc, prepared, base)

    rec["status"] = "ok" if not rec["error"] else "partial"
    return rec


def append_log(records: list[dict], path: Path | None = None) -> None:
    path = path or config.DOWNLOAD_LOG
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
