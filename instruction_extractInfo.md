# Case Information Extraction — Specification

| | |
|---|---|
| **Project** | Download_FraudCases (part 2 of 4) |
| **Status** | Final — consolidates the original brief, the 18-type taxonomy added in revision 2, and everything learned building the code |
| **Last updated** | 2026-08-14 |
| **Implementation** | [`fraudextract/`](fraudextract/), [`extract_patterns.py`](extract_patterns.py), [`ExtractedAll_in1InputFolder.sh`](ExtractedAll_in1InputFolder.sh) |
| **Earlier drafts** | `instruction_findpattern_v0.txt`, `instruction_findpattern.original.txt` |
| **Related** | [`instruction_download.md`](instruction_download.md) (part 1) · [`instruction_APIAnalisys.md`](instruction_APIAnalisys.md) (part 3) · [`instruction_designFeatures.md`](instruction_designFeatures.md) (part 4) |

---

## 1. Goal

Build models to predict medical fraud against Medicare, Medicaid or any
commercial payer. Many fraud cases have already been downloaded from DOJ and
HHS-OIG (part 1).

Summarise those reported cases: extract a structured record from each, and
identify the patterns — the common ways these fraudsters carried out their
illegal behaviour.

---

## 2. Input

- A folder of PDF files. **Each PDF is one fraud case.**
- The reference folder is `./downloaded/testdata_DOJ_2026`. Any folder of case
  PDFs works — the folder is a command-line argument, not a constant.
- Documents that yield no extractable text are **reported as errors, not silently
  dropped**.

---

## 3. Output fields

One row per input PDF.

| Field | Meaning |
|---|---|
| `DocumentName` | The PDF filename. Taken from the file, not asked of the model. |
| `ReportDT` | Publication date of the document, `yyyy-mm-dd`. |
| `JurisdictionName` | The prosecuting office and/or court named in the document. |
| `OccurDt` | When the fraud occurred: `yyyy-mm to yyyy-mm`, or a single value if only one date is given. This is the **conduct** period, not the charge/plea/sentencing date. |
| `FraudEntity` | The individual(s) and/or company(ies) that committed the fraud; semicolon-separated, roles in parentheses. |
| `Service` | Type of service involved (see below); semicolon-separated if several. |
| `State_County` | State and county/city, combined into one string if several. |
| `PayerName` | Medicare, Medicaid (naming the state programme), TRICARE, or a named commercial payer; semicolon-separated if several. |
| `FraudAmt` | Amount of money involved, whole US dollars. |
| `SettlementAmt` | Amount of the settlement, whole US dollars. |
| `JailTime` | Months in jail, if sentenced to jail. |
| `FraudType` | One value from the taxonomy in §4. |

**`Service` vocabulary** — `HomeHealth`, `PersonalCare`, `NursingHome`,
`Hospice`, `AdultDayCare`, `BehavioralHealth`, `SubstanceUseTreatment`,
`Pharmacy`, `Laboratory`, `GeneticTesting`, `DME`, `Telehealth`,
`PhysicianPractice`, `Hospital`, `Dental`, `Ambulance`, `Transportation`,
`Optometry`, `Chiropractic`, `Podiatry`, `Other`.

### 3.1 Fields added beyond the brief

| Field | Why it exists |
|---|---|
| `FraudTypeAll` | Every scheme type present, most central first. A single case routinely runs two schemes at once (kickbacks **and** phantom claims); one label per case throws most of that signal away, and the signal is the point of the exercise. |
| `CaseStatus` | `charged` / `pleaded guilty` / `convicted at trial` / `sentenced` / `civil settlement` / `other`. |
| `SchemeSummary` | One or two sentences on the actual mechanics: what was billed, to whom, and how the money was obtained. |

### 3.2 Field-name corrections

`urisdictionName` is read as **`JurisdictionName`** (dropped J), and `jailTime`
is normalised to **`JailTime`**, so every column is PascalCase.

---

## 4. FraudType taxonomy — closed set of 18

`FraudType` **must** be one of these. If nothing matches, use `Other - Unknown`.
Do **not** invent a label outside the list.

> Choose by the **mechanism that made the money**, not by the statute charged: a
> case charged as wire fraud but built on billing for visits that never happened
> is `Phantom Claims`, not `Wire Fraud`.

| # | Label | Definition |
|---:|---|---|
| 1 | `Phantom Claims` | Billing for encounters, visits or items that never happened at all — including billing for dead, incarcerated, hospitalised or absent patients. |
| 2 | `FakeEncounter` | An encounter occurred but was fabricated or staged to create a billable event: sham visits, recruited or paid patients, services by unlicensed or unqualified staff, services not medically necessary. |
| 3 | `Upcoding` | A real service billed under a higher-paying code, level of care, acuity or risk-adjustment diagnosis than what was delivered. |
| 4 | `Unbundling` | One bundled/global service split into component codes to collect more than the bundled rate. |
| 5 | `Falsify certificate` | Falsified certifications, plans of care, physician orders, timesheets, licences, training certificates or medical records used to make an otherwise unpayable claim payable. |
| 6 | `kickback_Bribery For Referral` | Payments, bribes or anything of value for patient referrals or to induce ordering of services; includes Anti-Kickback Statute and Stark Law self-referral. |
| 7 | `Drug_Prescriptions` | Anything centred on drugs or prescriptions: pill mills, diversion, medically unnecessary prescribing, compounding schemes, prescription forgery, adulteration or misbranding. |
| 8 | `Benefit & Eligibility Fraud` | Fraud about who is entitled to participate or be covered: concealed ownership, nominee owners, enrolment by an excluded or disqualified person, false enrolment or participation certifications, false beneficiary eligibility. |
| 9 | `Wire Fraud` | Laundering or moving the proceeds: shell companies, structured transfers, wire/mail fraud counts centred on moving money. |
| 10 | `Covid or General Loan Fraud` | PPP, EIDL, Provider Relief Fund, COVID testing or vaccine funds, other government loan/grant fraud. |
| 11 | `Tax, Payroll or Coupon Fraud` | Tax evasion, employment-tax and payroll fraud, ghost employees, coupon or rebate fraud. |
| 12 | `IdentityFraud` | Theft or misuse of patient, provider or beneficiary identities, including aggravated identity theft and stolen Medicare numbers. |
| 13 | `Device, DME` | Durable medical equipment, orthotics, prosthetics, braces, medical device schemes. |
| 14 | `Other - Embezzlement of federal grant funds` | Diversion of federal grant money. |
| 15 | `Other - FDA Submission Fraud` | False or misleading submissions to the FDA. |
| 16 | `Other - Arson insurance fraud` | Arson or property-insurance fraud. |
| 17 | `Retention of Overpayment` | Knowingly keeping a payment known to be unearned, including failure to report and return an identified overpayment. |
| 18 | `Other - Unknown` | Use **only** when nothing above fits. |

### 4.1 Spelling corrections

These strings become categorical values in a model, so they must not carry
typos:

| Earlier draft | Canonical |
|---|---|
| `Upcodiong` | `Upcoding` |
| `Device, DE` | `Device, DME` |
| `Other - Unknow` | `Other - Unknown` |
| `Wire Fraud: Fraud in laundering or money transferring` | `Wire Fraud` |

Long descriptive entries are shortened to a stable key; the full description
stays in the table above as the definition.

### 4.2 Enforcement

The taxonomy is **enforced, not merely requested** — it is declared as a closed
enum in the output schema, so a label outside the list cannot be returned.

### 4.3 Source of truth

**This file is the source of truth for the taxonomy.** When it changes here,
update `FRAUD_TYPES` and `FRAUD_TYPE_GUIDE` in
[`fraudextract/schema.py`](fraudextract/schema.py) to match.

---

## 5. Extraction rules

1. **Use only what the document states.** Never infer, estimate, or fill from
   general knowledge. If the document does not say, the value is null — *a wrong
   value is worse than a null.*
2. Dates are `yyyy-mm-dd`; a conduct period is `yyyy-mm to yyyy-mm`.
3. **Money** is a plain number of whole US dollars: `$1.6 million` → `1600000`.
   Keep `FraudAmt` (money taken) and `SettlementAmt` (money paid back) distinct.
   Where both a billed and a paid/loss figure are given for `FraudAmt`, use the
   larger (billed).
4. **`JailTime`** is in months, and only for custody *actually imposed*. "Faces
   up to 10 years" is a maximum penalty, not a sentence — that is null. Probation
   and supervised release are not custody.
5. **Multi-defendant cases roll up consistently.** One document is one case; all
   defendants go in `FraudEntity`; `SettlementAmt` is the **total** owed across
   them; `JailTime` is the **longest** custodial sentence imposed on any of them.
   `SchemeSummary` says when the figures span more than one defendant.
6. **Repeat coverage is expected and must be visible.** A case is announced more
   than once — charge, then plea, then sentencing — so "one PDF = one case"
   overcounts. Documents sharing a lead defendant are grouped and a distinct-case
   count is reported next to the document count. **Rows are not merged.**

---

## 6. How to run

### One folder in, one folder out

```bash
./ExtractedAll_in1InputFolder.sh testdata_DOJ_2026
./ExtractedAll_in1InputFolder.sh testdata_DOJ_2026 --effort high
```

The input folder resolves as a full path, a path relative to the project, or a
bare name under `./downloaded/`. Results go to `./extracted/<folder name>/`.
Extra arguments pass through to the Python CLI.

### Or the Python CLI directly

```bash
python extract_patterns.py --input-dir DIR --output-dir DIR
python extract_patterns.py --limit 3          # smoke test
python extract_patterns.py --effort high      # deeper reading
python extract_patterns.py --no-analysis      # fields only
python extract_patterns.py --force            # ignore the cache
```

### Outputs

| File | Contents |
|---|---|
| `cases.csv` | One row per case, the fields in §3 |
| `cases.json` | The same rows plus the computed counts |
| `patterns.md` | Counts, a case table, and the pattern analysis |
| `errors.json` | Written only if a document failed |
| `run.log` | Console output of the run |

`patterns.md` must contain: recurring scheme patterns, what the schemes have in
common, detection signals visible in claims data, and caveats/sample limits —
with every claim citing the specific cases that support it.

---

## 7. Technical requirements

| # | Requirement |
|---|---|
| 7.1 | Extraction uses the Claude API (`claude-opus-5`) with **structured outputs** — `messages.parse` against a Pydantic schema — so every record validates. No JSON repair, no regex fallback, no invalid taxonomy labels. |
| 7.2 | **Counting is done in code, not by the model.** Totals, medians, ranges, type and payer frequencies, and duplicate detection are all deterministic. The model supplies only the judgement layer: reading each document, and interpreting what the schemes have in common. |
| 7.3 | The system prompt (taxonomy + rules) is identical across documents and is **prompt-cached**. The first document runs alone so the rest read its cache; firing all of them at once would make every request a cache miss. |
| 7.4 | **PDF text is read on one thread.** PDFium is not thread-safe — reading inside the worker pool raises `Failed to load page` or kills the interpreter outright. Only the API calls are parallel. |
| 7.5 | **Resumable.** Each document's result is cached under `<output>/.cache/`; rerunning skips what is done, `--force` re-extracts. The cache lives with the outputs, so each input folder keeps its own state. |
| 7.6 | **Per-document error isolation** — see below. |
| 7.7 | Dependencies: `anthropic`, `pydantic`, `pypdfium2`. Requires `ANTHROPIC_API_KEY` or an `ant auth login` profile. |

### 7.6 Per-document error isolation

No single document may abort the run:

- `stop_reason` is checked before any content is read;
- refusals fall back to a second model;
- a schema violation is **repaired** (an out-of-taxonomy label is dropped and the
  record kept) rather than discarded;
- any unhandled exception in a worker becomes an error row.

Failures land in `errors.json`.

> **Why this is a requirement, not a nicety.** A run over 679 documents once died
> at document 676 because the model put a `Service` value (`GeneticTesting`) into
> `FraudTypeAll` and the resulting `ValidationError` was not caught. The cache
> meant no completed work was lost, but the run produced no output at all.

### Layout

```
ExtractedAll_in1InputFolder.sh   one folder in, one folder out
extract_patterns.py              the Python CLI
fraudextract/
  config.py      paths, model, effort, fallback model
  schema.py      the record + the 18-type taxonomy (keep in sync with §4)
  pdftext.py     PDF -> text, strips site chrome
  extract.py     one Claude call per document
  patterns.py    counts -> narrative analysis -> output files
```

---

## 8. Results

### 8.1 Reference folder — `testdata_DOJ_2026`

**13 documents, 13 extracted, 0 failures, 12 distinct cases** (one case appears
twice: plea and sentencing).

| FraudType (a case may carry several) | Cases |
|---|---:|
| Phantom Claims | 10 |
| Falsify certificate | 8 |
| kickback_Bribery For Referral | 5 |
| FakeEncounter | 4 |
| Benefit & Eligibility Fraud | 4 |
| Wire Fraud | 3 |
| IdentityFraud | 2 |
| Covid or General Loan Fraud | 1 |

**Service** — HomeHealth 11, SubstanceUseTreatment 2, Laboratory 2,
BehavioralHealth 1, PersonalCare 1, AdultDayCare 1.

Fraud amounts stated in 9 cases totalling **$78,987,938** (median $1.6M);
settlements in 9 cases totalling **$40,112,300**; custodial sentences in 4 cases
(median 24 months, range 15–60).

Values were spot-checked against source text: the 60-month sentence, the
$2,569,946 fraud amount and the Oct 2018 – Nov 2020 conduct period all match
their documents exactly.

**Headline patterns.** `Phantom Claims` and `Falsify certificate` co-occur almost
perfectly — falsification is not a separate offence, it is the operational
requirement that makes phantom billing survivable. Nearly every case sits in home-
and community-based care, where the service is unobservable and the only evidence
of it is documentation the defendant controls. Compliance touchpoints (inspection,
audit request, enrolment application) generated more fraud rather than stopping
it. Several schemes ran five to nine years before detection.

### 8.2 Full year — `DOJ_2025`

**679 documents, 679 extracted, 0 failures, 0 repairs.**

| FraudType | Cases |
|---|---:|
| Falsify certificate | 263 |
| Phantom Claims | 226 |
| kickback_Bribery For Referral | 209 |
| FakeEncounter | 200 |
| Wire Fraud | 182 |
| Drug_Prescriptions | 157 |
| IdentityFraud | 123 |
| Benefit & Eligibility Fraud | 112 |

---

## 9. Cost

Measured at **~$0.037 per document** at `--effort high`, **~$0.026** at the
default `medium`. Roughly two-thirds of the cost is output tokens, so effort is
the main cost lever; prompt-caching the taxonomy saves about 25% on a large
folder.

| Folder | high | medium |
|---|---:|---:|
| 13 documents (reference) | ~$0.30 | ~$0.20 |
| 463 documents (a year of DOJ) | ~$18 | ~$13 |

Start at `medium` and escalate only where the extractions show errors.

---

## 10. Known limitations

- **These are press releases, not claims data.** The detection signals in
  `patterns.md` are reconstructions of what *would* have been visible in claims;
  none has been tested against actual claim lines.
- **Selection bias runs one way.** Every case here was detected and prosecuted,
  so signals derived from them are signals of schemes that *got caught*.
- **Small samples cannot support prevalence or ranking claims.** The reference
  folder is 12 distinct cases, all home- and community-based care; it says
  nothing about DME, telehealth, pharmacy, hospital or genetic-testing risk.
- **Charged cases are allegations, not findings.** `CaseStatus` carries this —
  filter on it before treating a row as established fact.
