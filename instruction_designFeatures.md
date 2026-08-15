# Monitoring Feature Design — Specification

| | |
|---|---|
| **Project** | Download_FraudCases (part 4 of 4) |
| **Status** | Final — consolidates the original brief and the work as delivered |
| **Last updated** | 2026-08-14 |
| **Deliverable** | [`designFeatures/monitoring_features.md`](designFeatures/monitoring_features.md) |
| **Implementation** | [`designFeatures/`](designFeatures/) |
| **Earlier draft** | `instruction_designFeatures_v0.txt` |
| **Related** | [`instruction_download.txt`](instruction_download.txt) (1) · [`instruction_extractInfo.md`](instruction_extractInfo.md) (2) · [`instruction_APIAnalisys.md`](instruction_APIAnalisys.md) (3) |

---

## 1. Goal

Analyse the extracted case summaries — `SchemeSummary` and the other columns —
and, based on what the fraudsters actually did, **design features to monitor
relevant providers**.

Target: **about 10 features**.

---

## 2. Input

```
downloaded/webtool/extractedSummary_2025_DOJ.csv
```

679 prosecuted medical fraud cases (DOJ, 2025), produced by part 2. The columns
used are `SchemeSummary`, `Service`, `FraudTypeAll`, `PayerName` and `FraudAmt`.

---

## 3. What each feature must specify

The brief asks for two elements and leaves a third bullet blank. The blank one is
filled with what makes a feature actionable rather than aspirational:

| Element | From the brief | Purpose |
|---|---|---|
| **Service groups** | ✅ stated | Which provider types this applies to — Home Health, Telehealth, DME, Laboratory, … |
| **Feature to be created** | ✅ stated | What is computed |
| **Alert logic** | *added* | The rule that fires, and what happens when it does |
| **Data required** | *added* | The fields needed, so feasibility is visible up front |
| **Evidence** | *added* | How many of the 679 cases support it, with example filenames |
| **False positives** | *added* | The benign explanation that will trip it, and how to damp it |

A feature must be **computable**. "Monitor for suspicious billing" is not a
feature; "share of a rendering NPI's ordered beneficiaries with no encounter in
the prior 12 months, versus same-specialty peers" is.

---

## 4. Worked examples from the brief

Three examples were given. All three are covered:

| Brief | Delivered as |
|---|---|
| Over-capacity: providers billing more service hours than they could deliver (Home Health, PT, speech therapy, telehealth) | **#2 Impossible provider service-day** — converts timed codes to minutes per rendering NPI per day; **#9 EVV geolocation mismatch and attendant double-booking** |
| Records and proof of delivery: knowing which services need records requested (DME, prescriptions) | **#6 Dispensed quantity exceeds verifiable wholesale acquisition**; **#1 Order sign-off velocity** (documentation review as the action); **#3 Service-date conflicts** |
| "Check License" before paying claims | **#5 Enrolment screen: excluded/convicted persons and nominee-owner indicators** — LEIE/SAM and licence status checked at enrolment, revalidation and ownership change |

---

## 5. Method

Three stages, deterministic where it can be:

```bash
python designFeatures/analyze.py downloaded/webtool/extractedSummary_2025_DOJ.csv
python designFeatures/design_features.py downloaded/webtool/extractedSummary_2025_DOJ.csv
python designFeatures/render_features.py
```

| Stage | Script | Does |
|---|---|---|
| 1 | `analyze.py` | 20 regex probes for recurring **detectable mechanics** across all 679 summaries, cross-tabbed by service group → `evidence.json` |
| 2 | `design_features.py` | Claude (`claude-opus-5`, high effort) reads all 679 summaries plus the probe counts and designs the features, via structured outputs so every field is present |
| 3 | `render_features.py` | Renders the deliverable, cross-checking each claimed case count against the probes |

### 5.1 Guardrails

- **Citations are verified.** Every `example_documents` value is checked against
  the real filenames in the CSV; a fabricated citation fails the run loudly.
- **Claimed counts are cross-checked** against the deterministic probes. Where a
  feature claims more cases than its nearest probe, the document says so and
  marks the figure an estimate rather than a verified count.
- **No invented thresholds.** The corpus shows what schemes look like, not how
  often benign providers look similar, so every rule states a comparison against
  a calibrated peer or control distribution.

---

## 6. Output

`designFeatures/monitoring_features.md` — 10 features, each with the six elements
in §3, plus three appendices:

| Appendix | Contents |
|---|---|
| A | Mechanics found in the corpus — 20 probes with case counts, percentages and top service groups |
| B | Corpus composition — service groups and fraud types |
| C | Limitations |

`monitoring_features.json` carries the same content machine-readably.

### 6.1 The features

| # | Feature | Primary service groups | Cases |
|---:|---|---|---:|
| 1 | Order sign-off velocity per ordering NPI | Telehealth, DME, GeneticTesting, Laboratory | 55 |
| 2 | Impossible provider service-day | BehavioralHealth, PhysicianPractice, HomeHealth | 110 |
| 3 | Service dates conflicting with death, inpatient stay or incarceration | All | 110 |
| 4 | New-enrolee billing ramp with concentrated ordering source | DME, Laboratory, Hospice, HomeHealth | 40 |
| 5 | Enrolment screen: excluded persons and nominee-owner indicators | DME, Hospice, Laboratory, Pharmacy | 40 |
| 6 | Dispensed quantity exceeds verifiable wholesale acquisition | Pharmacy | 19 |
| 7 | Panel stacking and same-day presumptive + definitive testing | Laboratory, SubstanceUseTreatment | 37 |
| 8 | Hospice election without terminal-illness trajectory | Hospice, NursingHome | 20 |
| 9 | EVV geolocation mismatch and attendant double-booking | PersonalCare, HomeHealth, AdultDayCare | 30 |
| 10 | Procedure-substitution upcoding | PhysicianPractice, DME, Chiropractic | 127 |

Features 4 and 5 need **no claims history**, so they work on a brand-new
provider — which matters, because rapid enrolment followed by immediate high-volume
billing is one of the corpus's most common shapes.

---

## 7. Limitations

- **These are press releases, not claims data.** The features are reconstructions
  of what *would* have been visible; none has been tested against claim lines.
- **No thresholds are supplied**, for the reason in §5.1.
- **Selection bias runs one way.** Every case was detected and prosecuted, so
  these are features for schemes that *got caught*.
- **Case counts evidence a mechanic recurring**, not its prevalence in the
  provider population.
- The corpus is DOJ 2025 only. Re-running the three scripts against another
  year's CSV regenerates the features against that evidence.
