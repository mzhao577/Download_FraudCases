"""Shared configuration: paths, coverage window, keyword matching, source registry."""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SOURCES_FILE = ROOT / "sources.json"
DOWNLOAD_DIR = ROOT / "downloaded"
STATE_DIR = ROOT / "state"
CACHE_DIR = STATE_DIR / "cache"
MANIFEST_FILE = STATE_DIR / "manifest.jsonl"
DOWNLOAD_LOG = STATE_DIR / "download_log.jsonl"
SUMMARY_DIR = ROOT / "summary"

# Only documents dated on or after this day are kept (instruction: "last 5 years,
# in other words any reports or documents that are dated from Jan. 2021").
DEFAULT_SINCE = dt.date(2021, 1, 1)

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

# Politeness: minimum seconds between two requests to the same host, per process.
HOST_DELAY = {
    "www.justice.gov": 0.4,
    "oig.hhs.gov": 0.4,
    "www.fbi.gov": 0.5,
    "www.cms.gov": 0.6,
    "www.gao.gov": 0.6,
}
DEFAULT_HOST_DELAY = 0.5

# --------------------------------------------------------------------------
# Keyword matching
# --------------------------------------------------------------------------
# A document is treated as a medical / health care fraud item when it mentions a
# health care context AND a fraud context. Keeping the two axes separate avoids
# both the "every fraud case" and the "every Medicare press release" failure modes.

# Tier 1 - phrases that settle the question on their own.
STRONG_TERMS = r"""
    health \s* -? \s* care \s+ fraud | healthcare \s+ fraud |
    medicare \s+ fraud | medicaid \s+ fraud | medical \s+ fraud | tricare \s+ fraud |
    health \s+ care \s+ benefit \s+ program |
    medicaid \s+ fraud \s+ control \s+ unit | health \s+ care \s+ fraud \s+ unit |
    health \s+ care \s+ fraud \s+ (?: takedown | strike \s+ force | enforcement ) |
    medicare \s+ strike \s+ force | health \s+ care \s+ (?: kickback | false \s+ claims )
"""

# Tier 2 - the payer or program being billed. Narrow on purpose: these words are
# what separate a health care fraud case from every other kind of fraud case.
PAYER_TERMS = r"""
    medicare | medicaid | medi-cal | tricare | champva | chip \s+ program |
    health \s+ (?: insurance | insurer | benefit | benefits | plan | plans ) |
    health \s+ care \s+ (?: program | benefit | claims | provider | providers | payer ) |
    indian \s+ health \s+ service | veterans \s+ health |
    federal \s+ employees \s+ health \s+ benefits | fehb |
    blue \s+ cross | blue \s+ shield | unitedhealth | aetna | cigna | humana |
    private \s+ (?: insurer | insurers | health \s+ insurer ) | commercial \s+ (?: payer | insurer )
"""

# Tier 3 - clinical / provider context. Only counts when paired with a billing
# style of fraud, otherwise every drug or violent-crime release matches.
PROVIDER_TERMS = r"""
    hospice | home \s+ health | nursing \s+ home | skilled \s+ nursing |
    assisted \s+ living | adult \s+ day \s+ care | behavioral \s+ health |
    substance \s+ (?: use | abuse ) \s+ treatment | sober \s+ home | addiction \s+ treatment |
    pharmac (?: y | ies | ist | eutical ) | compound (?: ed | ing ) \s+ (?: drug | medication | cream ) |
    physician | doctor | dentist | dental | chiropract | podiatr | optometr | ophthalmol |
    psychiatr | psycholog | physical \s+ therap | occupational \s+ therap | nurse \s+ practitioner |
    hospital | clinic | medical \s+ (?: center | practice | group | clinic | billing | equipment |
        supply | supplies | device | services | provider ) |
    lab (?: oratory | oratories ) | genetic \s+ test | urine \s+ drug \s+ test | toxicology \s+ test |
    telemedicine | telehealth | durable \s+ medical \s+ equipment | \b dme \b |
    orthotic | prosthet | catheter | wound \s+ care | ambulance |
    covid-? 19 \s+ (?: test | testing ) | diagnostic \s+ test
"""

# Tier 4 - the wrongdoing. Deliberately excludes generic prosecution verbs
# (indicted, convicted, sentenced, guilty, conspiracy) which appear everywhere.
FRAUD_TERMS = r"""
    fraud | defraud | fraudulent | kickback | anti-? kickback | stark \s+ law |
    false \s+ claims \s+ act | false \s+ claims | false \s+ (?: billing | statements? \s+ relating ) |
    illegal \s+ remuneration | bribe (?: ry | s )? |
    upcod | overbill | over-? billing | overpayment | improper \s+ payment | double \s+ bill |
    phantom \s+ billing | billing \s+ scheme | bill (?: ed | ing ) \s+ (?: medicare | medicaid |
        for \s+ (?: services | items | procedures | tests ) ) |
    medically \s+ unnecessary | unnecessary \s+ (?: services | procedures | tests | items |
        prescriptions | surgeries ) |
    qui \s+ tam | whistleblower | civil \s+ monetary \s+ penalt | self-? disclosure |
    program \s+ integrity | exclusion \s+ (?: list | authority ) | excluded \s+ (?: individual | provider ) |
    money \s+ launder | embezzl | theft \s+ of \s+ (?: government | health )
"""

# Tier 4b - billing-flavoured wrongdoing, required when only Tier 3 context is present.
BILLING_FRAUD_TERMS = r"""
    kickback | false \s+ claims | illegal \s+ remuneration | health \s+ care \s+ fraud |
    billing \s+ fraud | fraudulent \s+ (?: billing | claims | bills | prescriptions ) |
    defraud (?: ed | ing )? \s+ (?: medicare | medicaid | tricare | health ) |
    upcod | overbill | over-? billing | improper \s+ payment | phantom \s+ billing |
    billing \s+ scheme | medically \s+ unnecessary | unnecessary \s+ (?: services | procedures |
        tests | items | prescriptions | surgeries ) | qui \s+ tam | overpayment |
    civil \s+ monetary \s+ penalt | bill (?: ed | ing ) \s+ for
"""

_FLAGS = re.IGNORECASE | re.VERBOSE
STRONG_RE = re.compile(STRONG_TERMS, _FLAGS)
PAYER_RE = re.compile(PAYER_TERMS, _FLAGS)
PROVIDER_RE = re.compile(PROVIDER_TERMS, _FLAGS)
FRAUD_RE = re.compile(FRAUD_TERMS, _FLAGS)
BILLING_FRAUD_RE = re.compile(BILLING_FRAUD_TERMS, _FLAGS)


def _slugify_pattern(pattern: str) -> str:
    """Let a pattern match hyphenated URL slugs as well as prose."""
    return pattern.replace(r"\s+", r"[\s\-]+").replace(r"\s*", r"[\s\-]*")


SLUG_STRONG_RE = re.compile(_slugify_pattern(STRONG_TERMS), _FLAGS)
SLUG_PAYER_RE = re.compile(_slugify_pattern(PAYER_TERMS), _FLAGS)
SLUG_PROVIDER_RE = re.compile(_slugify_pattern(PROVIDER_TERMS), _FLAGS)
SLUG_FRAUD_RE = re.compile(_slugify_pattern(FRAUD_TERMS), _FLAGS)
SLUG_BILLING_FRAUD_RE = re.compile(_slugify_pattern(BILLING_FRAUD_TERMS), _FLAGS)


def is_healthcare_fraud(text: str, slug_mode: bool = False, relaxed: bool = False) -> bool:
    """True when `text` looks like a medical / health care fraud document.

    strong phrase
      OR (payer/program mentioned AND some kind of fraud)
      OR (clinical provider context AND billing-style fraud)

    `relaxed=True` accepts any fraud term on the provider path. Use it when the
    text being matched is a title or URL slug rather than a full page body: a
    slug is short and title-like, so "pharmacy ... fraud" there is a real signal,
    whereas in 4,000 characters of body text the two words co-occur by accident.
    """
    if not text:
        return False
    strong, payer, provider, fraud, billing = (
        (SLUG_STRONG_RE, SLUG_PAYER_RE, SLUG_PROVIDER_RE, SLUG_FRAUD_RE, SLUG_BILLING_FRAUD_RE)
        if slug_mode
        else (STRONG_RE, PAYER_RE, PROVIDER_RE, FRAUD_RE, BILLING_FRAUD_RE)
    )
    if strong.search(text):
        return True
    if payer.search(text) and fraud.search(text):
        return True
    provider_fraud = fraud if relaxed else billing
    return bool(provider.search(text) and provider_fraud.search(text))


# --------------------------------------------------------------------------
# Source registry
# --------------------------------------------------------------------------

def load_sources() -> dict:
    with SOURCES_FILE.open(encoding="utf-8") as fh:
        return json.load(fh)


def source_keys(only_enabled: bool = True) -> list[str]:
    reg = load_sources()
    return [
        s["key"]
        for s in reg["sources"]
        if s.get("enabled", True) or not only_enabled
    ]


def ensure_dirs() -> None:
    for d in (DOWNLOAD_DIR, STATE_DIR, CACHE_DIR, SUMMARY_DIR):
        d.mkdir(parents=True, exist_ok=True)
