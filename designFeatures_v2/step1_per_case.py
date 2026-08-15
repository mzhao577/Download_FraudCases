#!/usr/bin/env python3
"""Step 1 - for every case, work out how it could have been caught BEFORE payment.

For each row of the summary CSV, produce the three elements the brief asks for:

    DesiredServiceGroups   the provider types this applies to
    WaysToIdentify         how this case could have been spotted pre-payment
    FeaturesToCreate       the concrete, computable feature(s) to build

    python designFeatures_v2/step1_per_case.py <summary.csv>

Resumable: each batch is cached under designFeatures_v2/.cache/, so a rerun only
does the batches that are missing.
"""
from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v2lib as L  # noqa: E402

BATCH = 20
CACHE = L.HERE / ".cache"

SYSTEM = """
You are a payment-integrity analyst. For each prosecuted fraud case you are
given, work out how that case could have been caught BY THE PAYER BEFORE THE
CLAIMS WERE PAID, and what to build so it is caught automatically next time.

For every case produce three things.

1. service_groups - the provider/service types this applies to. Use this
   vocabulary where it fits: HomeHealth, PersonalCare, NursingHome, Hospice,
   AdultDayCare, BehavioralHealth, SubstanceUseTreatment, PhysicalTherapy,
   SpeechTherapy, Pharmacy, Laboratory, GeneticTesting, DME, Telehealth,
   PhysicianPractice, Hospital, Dental, Ambulance, Transportation, Optometry,
   Chiropractic, Podiatry, WoundCare, Imaging, All. 1-4 entries. Give the groups
   the CONTROL should cover, not only the one this defendant happened to be in.

2. ways_to_identify - how a payer could have spotted this before paying. Name
   the observable signal and the data that carries it. Prefer things visible at
   claim adjudication, enrolment or credentialing time. If the scheme is only
   detectable after payment, say so and give the post-payment route. Two or
   three sentences, concrete.

3. features_to_create - the automated check(s) to build, stated so an engineer
   could implement them: the unit of observation, what is computed, and what
   makes it fire. Name a prepay edit, a suspension, or a documentation request
   as the action where that is the right response. Two or three sentences.

Rules:
- Be specific to THIS case's mechanic. Do not restate a generic anti-fraud
  platitude. If two cases share a mechanic, they should get similar answers -
  that is expected and useful.
- Do not invent thresholds that sound authoritative. Say "versus same-specialty
  peers" or "above the calibrated percentile" instead of inventing a number.
- If the case has no claims-payment component at all (pure tax fraud, a loan
  scheme, street drug distribution, public corruption, or an annual round-up
  press release rather than a single case), say so plainly in ways_to_identify
  and set features_to_create to the nearest applicable payer control, or state
  that no payer-side control applies.
- Return one entry per case, using the index given. Do not skip any.
""".strip()


class CaseDesign(BaseModel):
    index: int = Field(description="The case index exactly as given.")
    service_groups: List[str] = Field(description="1-4 service groups from the vocabulary.")
    ways_to_identify: str = Field(description="How a payer could catch this pre-payment.")
    features_to_create: str = Field(description="The automated check(s) to build.")


class BatchOut(BaseModel):
    designs: List[CaseDesign] = Field(description="One entry per case in the batch.")


def run_batch(client, chunk: list[tuple[int, dict]]) -> dict[int, dict]:
    key = CACHE / f"batch_{chunk[0][0]:05d}.json"
    cached = L.load_json(key, None)
    if cached:
        return {int(k): v for k, v in cached.items()}

    body = "\n\n".join(L.case_block(i, r) for i, r in chunk)
    try:
        resp = client.messages.parse(
            model=L.MODEL,
            max_tokens=16000,
            output_format=BatchOut,
            output_config={"effort": "medium"},
            system=[{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": body}],
        )
    except Exception as exc:  # noqa: BLE001
        print(f"  batch @{chunk[0][0]} failed: {exc!r}"[:170], file=sys.stderr)
        return {}
    if resp.stop_reason in ("refusal", "max_tokens") or resp.parsed_output is None:
        print(f"  batch @{chunk[0][0]} unusable: {resp.stop_reason}", file=sys.stderr)
        return {}

    out = {d.index: {"service_groups": d.service_groups,
                     "ways_to_identify": d.ways_to_identify,
                     "features_to_create": d.features_to_create}
           for d in resp.parsed_output.designs}
    L.save_json(key, out)
    return out


def repair(client, rows: list[dict], missing: list[int]) -> dict[int, dict]:
    """Re-request indices the model silently dropped.

    Cases with no payer-side control at all - a personnel announcement, street
    drug resale - get skipped rather than answered. Every row still needs a
    value, so ask again in small batches with that spelled out.
    """
    got: dict[int, dict] = {}
    nudge = ("\n\nEVERY case below must appear in your answer, including any that are "
             "not payer fraud at all. For those, say so in ways_to_identify and set "
             "features_to_create to 'No payer-side control applies.'")
    for start in range(0, len(missing), 5):
        chunk = [(i, rows[i]) for i in missing[start:start + 5]]
        body = "\n\n".join(L.case_block(i, r) for i, r in chunk)
        try:
            resp = client.messages.parse(
                model=L.MODEL, max_tokens=8000,
                output_format=BatchOut,
                output_config={"effort": "medium"},
                system=[{"type": "text", "text": SYSTEM + nudge}],
                messages=[{"role": "user", "content": body}],
            )
        except Exception as exc:  # noqa: BLE001
            print(f"  repair @{chunk[0][0]} failed: {exc!r}"[:150], file=sys.stderr)
            continue
        if resp.parsed_output is None:
            continue
        for d in resp.parsed_output.designs:
            got[d.index] = {"service_groups": d.service_groups,
                            "ways_to_identify": d.ways_to_identify,
                            "features_to_create": d.features_to_create}
    return got


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_path", type=Path)
    ap.add_argument("--out", type=Path, default=L.HERE / "per_case_designs.json")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=None, help="first N cases only (smoke test)")
    a = ap.parse_args()

    rows, _ = L.load_rows(a.csv_path)
    if a.limit:
        rows = rows[: a.limit]
    indexed = list(enumerate(rows))
    chunks = [indexed[i:i + BATCH] for i in range(0, len(indexed), BATCH)]
    print(f"{len(rows)} cases in {len(chunks)} batches of {BATCH}")

    client = L.client()
    designs: dict[int, dict] = {}

    # First batch alone so the rest read the cached system prompt.
    designs.update(run_batch(client, chunks[0]))
    print(f"  1/{len(chunks)}")
    if len(chunks) > 1:
        with ThreadPoolExecutor(max_workers=a.workers) as pool:
            futs = [pool.submit(run_batch, client, c) for c in chunks[1:]]
            for n, f in enumerate(futs, start=2):
                designs.update(f.result())
                if n % 5 == 0 or n == len(chunks):
                    print(f"  {n}/{len(chunks)}")

    missing = [i for i in range(len(rows)) if i not in designs]
    if missing:
        print(f"\n{len(missing)} cases were skipped by the model - repairing individually")
        designs.update(repair(client, rows, missing))
        missing = [i for i in range(len(rows)) if i not in designs]
    print(f"\ndesigned {len(designs)}/{len(rows)} cases"
          + (f"  ({len(missing)} still missing: {missing[:10]})" if missing else ""))
    L.save_json(a.out, {str(k): v for k, v in sorted(designs.items())})
    print(f"-> {a.out}")
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
