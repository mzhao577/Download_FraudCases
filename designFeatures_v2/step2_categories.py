#!/usr/bin/env python3
"""Step 2 - group the per-case features into about 20 categories, then assign one to each case.

    python designFeatures_v2/step2_categories.py

Two passes:
  a) read every case's features_to_create and derive ~20 categories that cover
     them, each with a name, definition and the control point it acts at;
  b) assign every case to exactly one category, constrained to that closed set.
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

BATCH = 40
TARGET_CATEGORIES = 20

DERIVE_SYSTEM = f"""
You are organising payment-integrity controls. You will be shown the
"features to create" written for several hundred prosecuted fraud cases. Group
them into about {TARGET_CATEGORIES} categories.

A good category set here:
- covers every case, including ones with no payer-side control (give those a
  category of their own rather than forcing them somewhere);
- splits by the CONTROL MECHANISM and the point in the payment lifecycle it acts
  at - enrolment screening, credential checking, prepay claim edits, volume and
  capacity analytics, referral-network analysis, documentation requests,
  post-payment audit - not by service line, and not by legal theory;
- has categories of comparable weight; avoid one bucket that swallows half the
  corpus and several that hold three cases;
- uses names an analyst would recognise, 2-5 words, no numbering.

For each category give: a snake_case id, a short name, a one-sentence
definition, and the control point (one of: enrolment, credentialing, prepay_edit,
prepay_analytics, documentation_request, postpay_audit, referral_network,
no_payer_control).
""".strip()

ASSIGN_SYSTEM = """
Assign each case to exactly one category from the list. Judge by the control
mechanism its feature describes and the point in the payment lifecycle it acts
at - not by the service line, and not by the legal theory charged.

Use the no-payer-control category only for cases with genuinely no claims-payment
component. Return one entry per case, using the index given. Do not skip any.
""".strip()


class Category(BaseModel):
    id: str = Field(description="snake_case identifier.")
    name: str = Field(description="Short analyst-readable name, 2-5 words.")
    definition: str = Field(description="One sentence: what belongs in this category.")
    control_point: str = Field(
        description="One of: enrolment, credentialing, prepay_edit, prepay_analytics, "
                    "documentation_request, postpay_audit, referral_network, no_payer_control.")


class CategorySet(BaseModel):
    categories: List[Category] = Field(description=f"About {TARGET_CATEGORIES} categories.")


def derive(client, designs: dict[str, dict]) -> list[dict]:
    # Feed every feature text; the point is coverage of the whole corpus.
    body = "\n".join(f"[{k}] ({', '.join(v['service_groups'])}) {v['features_to_create']}"
                     for k, v in designs.items())
    resp = client.messages.parse(
        model=L.MODEL, max_tokens=16000,
        output_format=CategorySet,
        output_config={"effort": "high"},
        system=[{"type": "text", "text": DERIVE_SYSTEM}],
        messages=[{"role": "user", "content": body}],
    )
    if resp.parsed_output is None:
        raise SystemExit("category derivation returned nothing")
    return [c.model_dump() for c in resp.parsed_output.categories]


def build_assign_types(ids: list[str]):
    from typing import Literal
    Label = Literal[tuple(ids)]  # type: ignore[valid-type]

    class One(BaseModel):
        index: int = Field(description="The case index exactly as given.")
        category_id: Label = Field(description="The category this case's feature belongs to.")

    class Out(BaseModel):
        assignments: List[One] = Field(description="One entry per case in the batch.")

    return Out


def assign_batch(client, Out, cat_text: str, chunk: list[tuple[str, dict]]) -> dict[str, str]:
    body = "\n\n".join(
        f"[{k}] services={', '.join(v['service_groups'])}\nfeature: {v['features_to_create']}"
        for k, v in chunk)
    try:
        resp = client.messages.parse(
            model=L.MODEL, max_tokens=8000,
            output_format=Out,
            output_config={"effort": "low"},
            system=[{"type": "text", "text": ASSIGN_SYSTEM + "\n\nCATEGORIES:\n" + cat_text,
                     "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": body}],
        )
    except Exception as exc:  # noqa: BLE001
        print(f"  assign batch @{chunk[0][0]} failed: {exc!r}"[:160], file=sys.stderr)
        return {}
    if resp.parsed_output is None:
        return {}
    return {str(x.index): x.category_id for x in resp.parsed_output.assignments}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--designs", type=Path, default=L.HERE / "per_case_designs.json")
    ap.add_argument("--categories", type=Path, default=L.HERE / "categories.json")
    ap.add_argument("--out", type=Path, default=L.HERE / "case_categories.json")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--rederive", action="store_true", help="re-derive the category set")
    a = ap.parse_args()

    designs = L.load_json(a.designs, {})
    if not designs:
        print(f"no designs at {a.designs} - run step1 first", file=sys.stderr)
        return 2
    client = L.client()

    cats = L.load_json(a.categories, None)
    if cats is None or a.rederive:
        print(f"deriving ~{TARGET_CATEGORIES} categories from {len(designs)} case features...")
        cats = derive(client, designs)
        L.save_json(a.categories, cats)
    print(f"{len(cats)} categories")

    ids = [c["id"] for c in cats]
    Out = build_assign_types(ids)
    cat_text = "\n".join(f"{c['id']}  [{c['control_point']}]  {c['name']}: {c['definition']}"
                         for c in cats)

    items = sorted(designs.items(), key=lambda kv: int(kv[0]))
    chunks = [items[i:i + BATCH] for i in range(0, len(items), BATCH)]
    print(f"assigning {len(items)} cases in {len(chunks)} batches")

    out: dict[str, str] = {}
    out.update(assign_batch(client, Out, cat_text, chunks[0]))
    if len(chunks) > 1:
        with ThreadPoolExecutor(max_workers=a.workers) as pool:
            futs = [pool.submit(assign_batch, client, Out, cat_text, c) for c in chunks[1:]]
            for n, f in enumerate(futs, start=2):
                out.update(f.result())
                if n % 5 == 0 or n == len(chunks):
                    print(f"  {n}/{len(chunks)}")

    missing = [k for k, _ in items if k not in out]
    print(f"\nassigned {len(out)}/{len(items)}"
          + (f"  ({len(missing)} missing)" if missing else ""))
    L.save_json(a.out, out)
    print(f"-> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
