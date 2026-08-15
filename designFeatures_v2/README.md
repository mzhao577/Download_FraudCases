# designFeatures_v2 — Per-Case Prevention Design

Implements [`instruction_designFeatures_v2.txt`](../instruction_designFeatures_v2.txt): for
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

Step 1 is **resumable** — each batch is cached under `.cache/`, so a rerun only
redoes what is missing.

## Output

**`extractedSummary_2025_DOJ_withFeatures.csv`** — every input column, unchanged,
plus four:

| Column | Contents |
|---|---|
| `DesiredServiceGroups` | The provider types the control should cover — not only the one this defendant happened to be in |
| `WaysToIdentify` | How a payer could have spotted this case before paying: the observable signal and the data carrying it |
| `FeaturesToCreate` | The automated check to build — unit of observation, what is computed, what makes it fire, and the action (prepay edit, suspension, records request) |
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
| `prepay_edit` | 8 | 250 |
| `no_payer_control` | 2 | 89 |
| `postpay_audit` | 4 | 76 |
| `enrolment` | 3 | 75 |
| `prepay_analytics` | 3 | 74 |
| `referral_network` | 2 | 58 |
| `credentialing` | 2 | 52 |
| `documentation_request` | 1 | 5 |

The distribution is even — largest category 53 cases, smallest 5 — so no bucket
swallows the corpus.

**89 cases (13%) have no meaningful payer-side control**: COVID/PPP loan fraud,
tax and payroll fraud, street drug distribution, public corruption, and annual
round-up press releases that are not single cases. Those are labelled honestly
rather than forced into a category.

## Design notes

- **Prevention-first.** The prompt asks specifically how each case could have
  been caught *before payment*, and only falls back to a post-payment route when
  the scheme genuinely leaves no pre-payment trace.
- **No invented thresholds.** Controls say "versus same-specialty peers" or
  "above the calibrated percentile" rather than inventing a cut-point the corpus
  cannot support.
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
