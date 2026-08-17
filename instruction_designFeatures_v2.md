# Per-Case Prevention Design (v2) — Specification

| | |
|---|---|
| **Project** | Download_FraudCases (part 4 of 4, second generation) |
| **Status** | Final — consolidates the original brief and the instructions given while refining it |
| **Last updated** | 2026-08-17 |
| **Deliverable** | [`designFeatures_v2/extractedSummary_2025_DOJ_withFeatures.csv`](designFeatures_v2/extractedSummary_2025_DOJ_withFeatures.csv) · [`categories.md`](designFeatures_v2/categories.md) |
| **Implementation** | [`designFeatures_v2/`](designFeatures_v2/) |
| **Original brief** | `instruction_designFeatures_v2.txt` |
| **Related** | [`instruction_designFeatures.md`](instruction_designFeatures.md) (v1, 10 corpus-wide features) · [`instruction_APIAnalisys.md`](instruction_APIAnalisys.md) (the tool that reads this) · [`instruction_deploy.md`](instruction_deploy.md) (hosting it) |

> **Scope note.** The refinement instructions in §3 are the ones given in the
> session that tightened the column contract and regenerated the corpus. The
> original v2 build happened earlier; what survives of that conversation is the
> brief in §2 and the code itself, so §4 onward describes the pipeline **as
> built** rather than as originally specified.

---

## 1. What this is, versus v1

Both generations read the same 679-case summary and ask the same question. They
differ in the unit of output.

| | v1 — [`designFeatures/`](designFeatures/) | v2 — [`designFeatures_v2/`](designFeatures_v2/) |
|---|---|---|
| **Unit** | The corpus as a whole | **One design per case** |
| **Output** | 10 monitoring features | 679 designs, grouped into 25 categories |
| **Form** | A standalone report | **Four new columns on the summary CSV** |
| **Use** | Read it, pick what to build | Read a case beside its own control, in `webtool2` |

v2 exists because a feature written for the corpus loses the case that motivated
it. Attaching the design to the row keeps the evidence and the control together.

---

## 2. The original brief

Verbatim from `instruction_designFeatures_v2.txt`, typos included:

```
Goal:
I would like to analyze the summary file by looking at the SchemeSummary and other info.
Based on what the fraudsters do and design some features to monitor For relevant providers.

Here are threet cases you may use as examples:
 - When I see some cases of providers in the domain of Home Health, Physical THerapy, speech
   therapy, TeleHealth, who charged insurance companies way more hours of service much more
   than it could, I want to track the weekly hours of service for all clinic with one billing
   NPI. This way, I may be able to identify clinics that has abrupt increase in service hours.
   This is to track the over-capacity issue.
 - When I see many cases of certain providers cheated on Medicare/ Medicaid by not having the
   treat=ment records. I want to ask for medical records.patient receipts for these kind of
   services such as DME or prescription, proof of delivery. For this, I will need to know what
   kind of services may have this kind of issue.
 - When I se a few cases where payer paid the fraudsters got paid even at times when their
   licenses expired or suspended, I would like to have a feature called "Check License"
   before paying the claims.

Input file: downloaded/webtool/extractedSummary_2025_DOJ.csv

These are just a few examples. Could you look at each of the examples and figure out ways to
identify these cases before they got paid? And also design ways to check these cases so that
they will be automatically identified, thus prevent them to be paid?

You may create the following for each of the fraud cases. Each feature should have these
elements:
 - Desired service groups such as Home Health, Telehealth, Physicial therapy, DEM etc.
 - Ways to identify these fraud cases
 - Features to be created to identify these cases

After each features are obtained, please put similar ideas, ways and features into category.
I would like you to create about 20 categories.

Output:
Please output a csv file that contains all input file columns, plus the 3 new coluimns
specified above.

Please create a new folder to hold all the codes and output. Let's name the folder as
designFeatures_v2".
```

Three things in that brief govern everything below:

1. **"before they got paid"** — the design target is *prevention*, not detection.
   A post-payment audit route is the fallback, not the answer.
2. **The three examples are shapes, not a shortlist** — over-capacity hours,
   missing treatment records, and expired licences are illustrations of the kind
   of reasoning wanted, applied to *every* case.
3. **"automatically identified"** — the output must be buildable by an engineer,
   not a description of a concern.

---

## 3. Refinement instructions, as given

| # | Instruction | Effect |
|---|---|---|
| 1 | "Could you work harder … so that you design the **WaysToIdentify** to be more specific and **shorter, maybe in 4 to 5 sentences**?" | Replaced "two or three sentences" with a hard shape: 4–5 sentences, one signal each, ≤25 words. The old spec was being met with 50-word run-ons stacking five signals behind semicolons. |
| 2 | "Could you also make the **Features2Create** to be **very specific**?" | Replaced prose with a fixed template — unit of observation → computed quantity → trigger → action — and banned "review", "monitor", "assess", "analyse" as the computation. |
| 3 | *Regenerate the corpus now?* → **"Nothing yet"** | The prompt change shipped first, validated on 40 cases, with the corpus left on the old output for review. |
| 4 | "Please run **Step 1 through step 3** for all 679 cases." | Full regeneration, including re-deriving the categories from the new feature text. |

---

## 4. The column contract

Four columns are appended to every input column. The brief asks for three; the
fourth is what makes the category grouping usable from the CSV.

### 4.1 `DesiredServiceGroups`

1–4 entries from a closed vocabulary: `HomeHealth`, `PersonalCare`,
`NursingHome`, `Hospice`, `AdultDayCare`, `BehavioralHealth`,
`SubstanceUseTreatment`, `PhysicalTherapy`, `SpeechTherapy`, `Pharmacy`,
`Laboratory`, `GeneticTesting`, `DME`, `Telehealth`, `PhysicianPractice`,
`Hospital`, `Dental`, `Ambulance`, `Transportation`, `Optometry`,
`Chiropractic`, `Podiatry`, `WoundCare`, `Imaging`, `All`.

The groups the **control** should cover — not only the one this defendant
happened to be in.

### 4.2 `WaysToIdentify`

**Exactly 4 or 5 sentences**, most decisive first.

| Rule | Detail |
|---|---|
| One signal per sentence | No semicolon lists, no `and`/`or` stacking to smuggle in a second signal |
| ≤25 words per sentence | Checked; 30 is the tolerance before a rewrite is requested |
| Name the data | The claim field, form, registry or file that carries the signal |
| Name the control point | Enrolment, credentialing, prior authorisation, or claim adjudication |
| No narrative | Do not restate the case or name the defendant |

The vocabulary the prompt supplies as examples of "name the data": billed
HCPCS/CPT/NDC, units and place of service, ordering/referring/rendering NPI,
dates of service, CMS-855 enrolment and ownership fields, PECOS, NPPES, state
licence board file, OIG LEIE, prior-auth records, EVV visit records, timesheets,
OASIS/MDS assessments, ARCOS or wholesaler pedigree, the beneficiary's other
claims, the Death Master File, the payer's own remittance history.

### 4.3 `FeaturesToCreate`

**2 or 3 numbered checks**, each one sentence in exactly this shape:

```
N) <feature name>: on <unit of observation>, compute <the exact quantity, over
named fields>; fires when <the comparison that trips it>; action <prepay edit |
claim suspension | payment suspension | documentation request (ADR) |
prior-authorisation requirement | site visit | postpay audit>.
```

| Element | Requirement |
|---|---|
| **Unit of observation** | A real group-by key: provider NPI, provider NPI × week, beneficiary × supplier NPI, ordering NPI × HCPCS, claim line, rendering NPI × date of service, TIN, bank account |
| **Computed quantity** | Arithmetic over named data — a count, sum, rate, ratio, day gap, overlapping minutes, distinct-value count, graph degree. **Never** "review", "monitor", "assess", "analyse" or "flag" |
| **Trigger** | A stated comparison: calibrated percentile versus same-specialty peers, the provider's own trailing baseline, a physical impossibility, or an exact registry mismatch |
| **Action** | One of the listed payer responses |

**No invented thresholds.** "Above the calibrated percentile versus
same-specialty peers", never a number the corpus cannot support. Numbers from
physics or the rule book are fine: 24 hours in a day, overlapping visit minutes,
a licence expiry date, one device per lifetime.

### 4.4 `FeatureCategory`

One of ~20 categories (25 as derived), split by **control mechanism and where it
acts in the payment lifecycle** — enrolment, credentialing, prepay edit, prepay
analytics, documentation request, postpay audit, referral network, no payer
control — not by service line and not by legal theory.

### 4.5 Cases with no payer-side control

Some cases have no claims-payment component at all: PPP/EIDL loan fraud, tax and
payroll fraud, street drug distribution, public corruption, grant and trust
embezzlement, and annual round-up press releases that are not single cases.

These are **labelled, not forced into a category**. `FeaturesToCreate` starts
with the literal string `No payer-side control applies.`, optionally followed by
the nearest control outside the claims system. `WaysToIdentify` may be shorter
than four sentences for these, since there is less to say.

---

## 5. Pipeline

```bash
python designFeatures_v2/step1_per_case.py downloaded/webtool/extractedSummary_2025_DOJ.csv
python designFeatures_v2/step2_categories.py --rederive
python designFeatures_v2/step3_build_csv.py downloaded/webtool/extractedSummary_2025_DOJ.csv
```

Requires `ANTHROPIC_API_KEY`. Step 1 costs roughly **$8–10** for 679 cases and is
the slow one; steps 2 and 3 are cents.

| Step | Does |
|---|---|
| **1** `step1_per_case.py` | One design per case, in batches of 20, then shape-checked and repaired |
| **2** `step2_categories.py` | Derives ~20 categories from every case's feature text, then assigns each case to exactly one — as a **closed enum**, so no invented category can reach the CSV |
| **3** `step3_build_csv.py` | Writes the output CSV and `categories.md` |

### 5.1 How step 1 defends its own output

| Mechanism | Why |
|---|---|
| **Cache keyed on a hash of the system prompt** (`.cache/<prompt-id>/`) | Editing the prompt starts a fresh cache instead of serving answers written to the old spec |
| **Shape check on every answer** | Sentence count, sentence length, numbering, presence of a trigger and an action, and stub detection (the model occasionally answers `"x"`) |
| **Two rewrite rounds** | Off-shape answers are re-asked, and a rewrite is taken **only if strictly closer to spec**, so a re-ask can never lose ground |
| **Missing-index repair** | Indices the model silently drops are re-requested in small batches with an explicit instruction to answer even when no payer control applies |
| **Per-case fallback** | A chunk that returns nothing at all is retried case by case |
| **Compliance report** | The run prints average sentences, words and checks, the no-control count, and anything still off-shape |

`--no-shape-pass` skips the rewrite rounds; `--limit N` runs the first N cases
(see the caching warning in §7).

---

## 6. Result as delivered

| Measure | Value |
|---|---|
| Cases designed | **679 / 679**, 0 off-shape |
| `WaysToIdentify` (payer cases) | **5.0 sentences**, 88 words average, 106 maximum |
| `FeaturesToCreate` (payer cases) | **3.0 numbered checks** average |
| Cases with no payer-side control | **165 (24%)** |
| Categories | **25**, largest 63 cases, smallest 2 |

By control point:

| Control point | Categories | Cases |
|---|---:|---:|
| `prepay_edit` | 6 | 184 |
| `no_payer_control` | 5 | 146 |
| `prepay_analytics` | 4 | 113 |
| `referral_network` | 3 | 71 |
| `postpay_audit` | 2 | 64 |
| `enrolment` | 2 | 50 |
| `credentialing` | 2 | 49 |
| `documentation_request` | 1 | 2 |

The five largest categories: Order Without Treating Encounter (63), No Claims
System Nexus (53), Impossible Day and Capacity Limits (52), Product Provenance
and Inventory Reconciliation (51), Referral Concentration and Remuneration (46).

> **Filter on the marker, not the category.** 165 rows carry
> `No payer-side control applies.` but only 146 sit in a `no_payer_control`
> category: step 2 assigns by control mechanism, so 23 marker rows are filed
> under the nearest non-claims category (Product Provenance 7, Exclusion and
> Sanction Screening 4, Applicant Eligibility Verification 4, …) and 4 rows in
> `no_payer_control` categories do carry a payer-side check.

The no-control count was **89 under the earlier prompt and 165 under this one** —
the same cases, relabelled. The old spec allowed a case to be answered with a
loosely related payer control instead of being marked.

---

## 7. Rework notes

- **Do not smoke-test into the shared cache.** `--limit 8` writes
  `batch_00000.json` holding only 8 answers, and a later full run treats cases
  8–19 as dropped and sends them down the repair path. Delete the partial batch,
  or point `--out` and the cache elsewhere. Symptom: partial batch files.
- **Watch for truncation.** Reasoning tokens count against `max_tokens`; at 16k a
  batch of 20 came back with 2 usable answers, and a 5-case repair chunk died on
  invalid JSON mid-string. Now 32k for the main pass, 16k for re-asks, with a
  per-case fallback. Symptom: `still missing` indices, or a batch file with far
  fewer than 20 entries.
- **Re-derive the categories after changing the feature text** (`--rederive`).
  They are derived *from* that text; keeping an old set silently mislabels.
- **Refresh the review tool's input.** `python webtool2/setup_input.py --key
  DOJ_2025` **copies** the CSV — without it, `webtool2` and the hosted Space show
  the previous categories.
- **The deck is downstream.** `FraudAnalysis_ReportedCases.pptx` quotes this
  output and does not regenerate itself.

---

## 8. Limitations

- **Press releases are not claims data.** Every control is a reconstruction of
  what *would* have been visible. None has been tested against claim lines, and
  every threshold needs calibration against a control population before use.
- **Selection bias runs one way.** Every case here was detected and prosecuted,
  so these are controls for schemes that *got caught*.
- **Similar cases get similar answers**, by design — a shared mechanic should
  produce a shared control. The corpus is not 679 distinct ideas.
- **One category per case**, though several controls often apply. The category
  reflects the mechanism of the *primary* check.
- **DOJ 2025 only.** Rerunning the three steps against another year's CSV
  regenerates everything against that evidence.
