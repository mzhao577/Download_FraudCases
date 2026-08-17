# designFeatures_v2 — Per-Case Prevention Design

Implements [`instruction_designFeatures_v2.md`](../instruction_designFeatures_v2.md): for
**every** case in the summary file, work out how it could have been caught
*before the claims were paid*, and what to build so it is caught automatically
next time. Then group those controls into categories.

Where [`designFeatures/`](../designFeatures) (v1) produced **10 features for the
corpus as a whole**, v2 produces **one design per case** — 679 of them — and
then organises them.

## Run it

```bash
python designFeatures_v2/step1_per_case.py downloaded/webtool/extractedSummary_2025_DOJ.csv
python designFeatures_v2/step2_categories.py
python designFeatures_v2/step3_build_csv.py downloaded/webtool/extractedSummary_2025_DOJ.csv
```

Requires `ANTHROPIC_API_KEY` (or an `ant auth login` profile). Step 1 costs
roughly **$8–10** for 679 cases and is the slow one; steps 2 and 3 are cents.

Step 1 is **resumable** — each batch is cached under `.cache/<prompt-id>/`, so a
rerun only redoes what is missing. The prompt id is a hash of step 1's system
prompt, so editing the prompt starts a fresh cache instead of serving answers
written to the old spec.

## Output

**`extractedSummary_2025_DOJ_withFeatures.csv`** — every input column, unchanged,
plus four:

| Column | Contents |
|---|---|
| `DesiredServiceGroups` | The provider types the control should cover — not only the one this defendant happened to be in |
| `WaysToIdentify` | How a payer could have spotted this case before paying — **4–5 sentences, one signal each, ≤25 words**, every one naming the data that carries it (claim field, CMS-855 record, PECOS, LEIE, EVV, ARCOS, prior auth) and where in the lifecycle it is visible |
| `FeaturesToCreate` | **2–3 numbered checks**, each `<name>: on <unit of observation>, compute <quantity over named fields>; fires when <comparison>; action <prepay edit / suspension / ADR / prior auth / site visit / postpay audit>` |
| `FeatureCategory` | Which of the 25 categories that check belongs to |

> The brief asks for **three** new columns and, separately, for the features to be
> grouped into categories. `FeatureCategory` is the fourth column that grouping
> needs in order to be usable from the CSV.

**`categories.md`** — the category catalogue: each category's definition, control
point and case count, plus a roll-up by control point.

Intermediates: `per_case_designs.json` (step 1), `categories.json` +
`case_categories.json` (step 2).

## Categories

25 categories, split by **control mechanism and where it acts in the payment
lifecycle** rather than by service line:

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

The distribution is reasonably even — largest category 63 cases, smallest 2 — so
no bucket swallows the corpus.

**165 cases (24%) have no payer-side control**: COVID/PPP loan fraud, tax and
payroll fraud, street drug distribution, public corruption, grant and trust
embezzlement, and annual round-up press releases that are not single cases.
Their `FeaturesToCreate` starts with the literal phrase `No payer-side control
applies.`, so they are filterable, and most still carry the nearest non-claims
control after it. (This ran at 89 under the earlier prompt, which let a case be
answered with a loosely related payer control instead of being labelled.)

## Design notes

- **Prevention-first.** The prompt asks specifically how each case could have
  been caught *before payment*, and only falls back to a post-payment route when
  the scheme genuinely leaves no pre-payment trace.
- **One signal per sentence.** `WaysToIdentify` is capped at 4–5 sentences of
  ≤25 words, so each line is a single testable signal with its data source named
  rather than a paragraph-long run-on.
- **Features are written to a template.** Unit of observation → computed
  quantity → trigger → action. The computation must be arithmetic over named
  fields — a count, ratio, day gap, overlap or graph degree — never "review" or
  "monitor". Step 1 checks every answer against that shape and re-asks (twice)
  for any that miss it, keeping the better of the two; `--no-shape-pass` skips
  it. The run prints how many answers still miss the shape.
- **No invented thresholds.** Controls say "versus same-specialty peers" or
  "above the calibrated percentile" rather than inventing a cut-point the corpus
  cannot support. Numbers from physics or the rule book — 24 hours in a day,
  overlapping visit minutes, a licence expiry — are allowed.
- **Every row gets a value.** Cases the model initially skipped — a personnel
  announcement, a street opioid resale — are re-requested individually with an
  explicit instruction to answer even when no payer control applies. 679/679.
- **Categories are a closed enum at assignment time**, so no invented category
  can appear in the CSV.

## Limitations

These are press releases, not claims data. Every control is a reconstruction of
what *would* have been visible; none has been tested against claim lines, and
every threshold needs calibration against a control population before use. And
because each case was detected and prosecuted, these are controls for schemes
that *got caught*.
