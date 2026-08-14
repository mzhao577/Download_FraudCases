#!/usr/bin/env python3
"""Step 0 - render sources.json (the list of websites used for the search) into
a readable SOURCES.md and a plain-text listofWebsites.txt, and print it.
"""

from __future__ import annotations

import datetime as dt
import sys

from fraudscrape import config


def render(reg: dict) -> str:
    L = []
    A = L.append
    A("# Sources searched for medical / health care fraud cases")
    A("")
    A(f"Coverage: documents dated **{reg['coverage_start']}** or later.")
    A("")
    A("This file is generated from [`sources.json`](sources.json), which is what the")
    A("scrapers actually read. Edit the JSON, not this file.")
    A("")
    for s in reg["sources"]:
        mark = "" if s.get("enabled", True) else "  *(disabled)*"
        A(f"## {s['key']} - {s['name']}{mark}")
        A("")
        A(f"**Why this source.** {s['why']}")
        A("")
        A("**Websites searched**")
        A("")
        for w in s["websites"]:
            A(f"- <{w}>")
        A("")
        h = s.get("harvest", {})
        if h:
            A(f"**How.** {h.get('method', '')}")
            A("")
            eps = h.get("endpoints") or ([h["endpoint"]] if h.get("endpoint") else [])
            for e in eps:
                A(f"- `{e}`")
            if h.get("notes"):
                A("")
                A(f"*Note:* {h['notes']}")
            A("")
        if s.get("document_types"):
            A(f"**Document types:** {', '.join(s['document_types'])}")
            A("")
    if reg.get("considered_but_not_scraped"):
        A("## Considered but not scraped")
        A("")
        for s in reg["considered_but_not_scraped"]:
            A(f"- **{s['name']}** (<{s['url']}>) - {s['reason']}")
        A("")
    return "\n".join(L) + "\n"


def render_plain(reg: dict) -> str:
    """Flat text list of every website used for the search."""
    L = []
    A = L.append
    rule = "=" * 78
    A(rule)
    A("LIST OF WEBSITES USED TO SEARCH FOR MAJOR MEDICAL / HEALTH CARE FRAUD CASES")
    A("Medicare, Medicaid, TRICARE and commercial-payer cases")
    A(rule)
    A(f"Coverage      : documents dated {reg['coverage_start']} or later")
    A(f"Generated     : {dt.datetime.now().astimezone().isoformat(timespec='seconds')}")
    A("Generated from: sources.json (edit that file, not this one)")
    A("")

    A("-" * 78)
    A("QUICK LIST - every site searched")
    A("-" * 78)
    seen = []
    for s in reg["sources"]:
        for w in s["websites"]:
            if w not in seen:
                seen.append(w)
    for i, w in enumerate(seen, 1):
        A(f"{i:3}. {w}")
    A("")

    A("-" * 78)
    A("DETAIL BY SOURCE")
    A("-" * 78)
    for s in reg["sources"]:
        A("")
        state = "" if s.get("enabled", True) else "   [DISABLED]"
        A(f"[{s['key']}] {s['name']}{state}")
        A("")
        A("  Why this source:")
        for line in _wrap(s["why"]):
            A(f"    {line}")
        A("")
        A("  Websites searched:")
        for w in s["websites"]:
            A(f"    - {w}")
        h = s.get("harvest", {})
        if h.get("method"):
            A("")
            A("  How it is harvested:")
            for line in _wrap(h["method"]):
                A(f"    {line}")
        eps = h.get("endpoints") or ([h["endpoint"]] if h.get("endpoint") else [])
        if eps:
            A("")
            A("  Endpoints actually requested:")
            for e in eps:
                A(f"    - {e}")
        if h.get("notes"):
            A("")
            A("  Notes:")
            for line in _wrap(h["notes"]):
                A(f"    {line}")
        if s.get("document_types"):
            A("")
            A(f"  Document types: {', '.join(s['document_types'])}")
    A("")

    if reg.get("considered_but_not_scraped"):
        A("-" * 78)
        A("CONSIDERED BUT NOT SCRAPED")
        A("-" * 78)
        for s in reg["considered_but_not_scraped"]:
            A("")
            A(f"  {s['name']}")
            A(f"    {s['url']}")
            for line in _wrap(s["reason"]):
                A(f"    Reason: {line}" if line == _wrap(s["reason"])[0] else f"            {line}")
    A("")
    return "\n".join(L) + "\n"


def _wrap(text: str, width: int = 72) -> list[str]:
    import textwrap
    return textwrap.wrap(text, width=width) or [""]


def main() -> int:
    reg = config.load_sources()
    md = render(reg)
    out_md = config.ROOT / "SOURCES.md"
    out_md.write_text(md, encoding="utf-8")

    txt = render_plain(reg)
    out_txt = config.ROOT / "listofWebsites.txt"
    out_txt.write_text(txt, encoding="utf-8")

    print(txt)
    print(f"-> {out_md}", file=sys.stderr)
    print(f"-> {out_txt}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
