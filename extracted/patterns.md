# Medical Fraud Cases - Extracted Features and Patterns

*Generated 2026-08-13T17:48:44-04:00 with `claude-opus-5`*

- Documents processed: **13** (extracted 13, failed 0)
- Distinct cases: **12** - 1 case(s) are covered by more than one document (charge, plea and sentencing are announced separately), so per-document counts overstate case counts
- Fraud amounts stated in **9** cases, totalling **$78,987,938** (median $1,600,000, range $174,496 - $68,000,000)
- Settlements/judgments stated in **9** cases, totalling **$40,112,300**
- Custodial sentences imposed in **4** cases (median 24 months, range 15-60)

## Cases

| Document | Date | Entity | Payer | Fraud $ | Settlement $ | Jail (mo) | Type |
|---|---|---|---|---|---|---|---|
| two-individuals-plead-guilty-to-68-million-f | 2026-01-15 | Elaine Antao (marketer/recruiter); Manal Wasef (mark | Medicaid (New York) | $68,000,000 | $1,000,000 | - | kickback_Bribery For Referral |
| traditions-health-agrees-to-pay-34m-to-resol | 2026-01-22 | Traditions Health LLC (home health provider) | Medicare | - | $34,000,000 | - | FakeEncounter |
| two-home-health-providers-agree-to-pay-702-5 | 2026-01-26 | Medical Services of America, Inc.; Traditional Home  | Medicare | - | $702,541 | - | kickback_Bribery For Referral |
| local-home-healthcare-company-owner-admits-o | 2026-02-17 | Natavia Boyd-Wells (owner of Touch of the Heart Home | Missouri Medicaid Program; U | $209,000 | - | - | Phantom Claims |
| st-louis-county-home-healthcare-company-owne | 2026-02-17 | Daniell Green (owner and operator of A&L Angels Home | Medicaid (Missouri Medicaid  | $1,460,000 | - | - | Phantom Claims |
| home-health-care-operator-admits-defrauding- | 2026-03-20 | Camille S. Childress (operator/owner of Inspiring An | Missouri Medicaid | $174,496 | $174,496 | 15 | Phantom Claims |
| former-sober-home-owner-and-operator-sentenc | 2026-04-24 | Delores Jordan (owner of Serenity Keeper's, LLC); Er | Medicaid (Kentucky); Medicar | $2,569,946 | - | 60 | kickback_Bribery For Referral |
| michigan-home-health-care-agency-owner-convi | 2026-05-15 | Ruby Scott (nurse, owner of Delta Home Health Care L | Medicare | $1,600,000 | - | - | Falsify certificate |
| queens-home-care-agency-and-home-health-aide | 2026-05-19 | Kris Agency & Home Care, Inc. (Queens home care agen | - | $1,800,000 | $2,347,133 | - | Falsify certificate |
| u-s-attorney-moore-capito-announces-fraud-co | 2026-06-23 | Raymond C. "Rocky" Meadows II (founder and director, | Medicaid (West Virginia); Ve | - | $120,000 | - | Falsify certificate |
| home-health-care-operator-sentenced-for-defr | 2026-07-21 | Camille S. Childress (operator/owner of Inspiring An | Medicaid (Missouri Medicaid) | $174,496 | $174,496 | 15 | Phantom Claims |
| ceo-of-bay-area-home-health-agency-convicted | 2026-07-23 | Simon Katz; Veronica Katz (former CEO of HealthNow H | Medicare | $3,000,000 | $593,634 | 24 | FakeEncounter |
| philadelphia-in-home-care-services-provider- | 2026-08-04 | Blessings 4 Ever Home Care Agency LLC (in-home care  | Medicaid (Pennsylvania Medic | - | $1,000,000 | - | Falsify certificate |

## Fraud types (cases may carry several)

| Type | Cases |
|---|---|
| Phantom Claims | 10 |
| Falsify certificate | 10 |
| FakeEncounter | 5 |
| kickback_Bribery For Referral | 5 |
| other | 2 |
| Ineligible provider enrollment | 2 |
| Money laundering of proceeds | 1 |

## Scheme combinations

| Combination | Cases |
|---|---|
| Falsify certificate + Ineligible provider enrollment + Phantom Claims | 2 |
| Falsify certificate + Phantom Claims | 2 |
| FakeEncounter + Falsify certificate + Phantom Claims | 2 |
| FakeEncounter + Falsify certificate + Phantom Claims + other | 1 |
| FakeEncounter + Falsify certificate + Phantom Claims + kickback_Bribery For Referral | 1 |
| Falsify certificate + Phantom Claims + kickback_Bribery For Referral | 1 |
| Falsify certificate + other | 1 |
| FakeEncounter + kickback_Bribery For Referral | 1 |
| Money laundering of proceeds + Phantom Claims + kickback_Bribery For Referral | 1 |

## Payers defrauded

| Payer | Cases |
|---|---|
| Medicaid | 8 |
| Medicare | 5 |
| U.S. Department of Veterans Affairs Community Care Network | 1 |
| Veterans Administration Community Health program | 1 |

## States

| State | Cases |
|---|---|
| Missouri | 4 |
| New York | 2 |
| California | 1 |
| Kentucky | 1 |
| Michigan | 1 |
| Pennsylvania | 1 |
| Oklahoma | 1 |
| Florida | 1 |
| West Virginia | 1 |

## Case status

| Status | Cases |
|---|---|
| civil settlement | 4 |
| pleaded guilty | 3 |
| convicted at trial | 2 |
| sentenced | 2 |
| charged | 2 |

## Documents covering the same case

| Entity | Documents | Stages |
|---|---|---|
| Camille S. Childress (operator/owner of Inspiring Angels LLC | home-health-care-operator-admits-defrauding-missou<br>home-health-care-operator-sentenced-for-defrauding | pleaded guilty, sentenced |

# Pattern analysis

## Recurring scheme patterns

**1. Billing for visits that never happened, proved by the patient's location.** This is the single most common mechanic and the one with the cleanest data footprint. *Blessings 4 Ever Home Care Agency* billed 1,141 personal-care claims for 209 Pennsylvania Medicaid beneficiaries on days those beneficiaries were hospital inpatients "all day" (June 2020–Dec 2023). *Camille Childress / Inspiring Angels LLC* billed Missouri Medicaid for in-home services including "clients who were hospitalized" and visits with no timesheets at all. *Natavia Boyd-Wells / Touch of the Heart* billed both Missouri Medicaid and the VA Community Care Network for dates when veteran patients were hospitalized. *Daniell Green / A&L Angels* is charged with false timesheets for services never provided, again including dates patients were hospitalized. Four separate cases, three states, two payer families — the inpatient-overlap tell recurs more than any other fact in this sample.

**2. Fabricated or backdated paper to manufacture eligibility and compliance.** The documentation, not the service, is the product. *Blessings 4 Ever* allegedly fabricated or backdated 181 training certificates and personnel files so personal care attendants appeared to meet state training requirements. *HealthNow Home Healthcare* (Simon and Veronica Katz) altered medical records, forged physician signatures, and submitted falsified documents to California Department of Public Health inspectors to preserve Medicare billing privileges. *Ruby Scott / Delta Home Health Care* falsely represented that physicians had certified patients as homebound and eligible when no physician had evaluated them. *Green* allegedly filed a false Medicaid participation agreement asserting workers were in the Family Care Safety Registry and background-checked. *Boyd-Wells* fabricated documentation specifically **in response to a Medicaid audit request** — i.e., the fraud extended into the payer's own verification loop. *Raymond and Helen Meadows / Lifehouse Inc.* allegedly submitted timesheets to a drug-testing lab for work never performed, including 32 hours of weekly overtime for months and hours billed while on out-of-state vacations.

**3. Kickbacks and referral steering, in both criminal and civil form.** Five cases turn on remuneration for referrals, and the payment mechanics vary widely:
- *Delores Jordan / Serenity Keeper's* took checks, cash, ACH and $5,000 "consulting" payments (routed to co-defendant Davis's company, *X-Tremly for Christ LLC*) for steering sober-home residents' urine drug tests to three labs — $2.57M paid by Kentucky Medicaid and Medicare for tests not ordered or reviewed by any provider.
- *Ruby Scott* paid a Detroit hospital discharge nurse over $130,000, roughly $100–$300 per patient, via CashApp, PayPal, check and cash, to fax confidential Medicare patient records to her agency — a kickback that doubles as a patient-data theft scheme feeding phantom certifications.
- *Antao and Wasef* (Brooklyn) were paid as marketers to funnel Medicaid recipients to two social adult day care centers and a home health fiscal intermediary, and paid cash bribes *to beneficiaries* — $68M billed, the largest figure in the set.
- On the civil side, *Traditions Health LLC* self-disclosed paying remuneration to physician-medical directors in Oklahoma and Texas who referred Medicare home health patients (AKS/Stark), and *Traditional Home Care d/b/a Community Home Health Services* paid an employee bonuses keyed to the referral volume of the employee's **physician spouse** (Stark).

**4. Services rendered by people not licensed or trained to render them, billed at professional rates.** *HealthNow* used unqualified personnel to perform home health assessments outside their scope of practice. *Serenity Keeper's* billed Medicaid for six hours per day of peer support that was not provided and not delivered by licensed peer support specialists. *West Virginia Sleep Centers LLC* paid $120,000 to settle allegations that sleep studies and polysomnogram reports were prepared and signed by unqualified non-physician staff (Jan 2016–Jan 2020). *Blessings 4 Ever*'s certificate fabrication is the same defect one step upstream.

**5. Concealed ownership and enrollment by excluded or disqualified people.** *Childress* enrolled Inspiring Angels in Missouri Medicaid using paperwork falsely naming another person as owner, to hide a 2012 conviction that would have disqualified her. *Green* allegedly concealed co-defendant Bingham's felony conviction on the participation agreement. This is the smallest recurring pattern (two cases) but it is the one that defeats screening at the front door rather than at the claim.

**6. Compensation structures that pay a percentage of billings.** *Ernest Williams* received $365,374.72 as a percentage of amounts Serenity Keeper's billed; *Community Home Health Services* tied bonuses to referral volume. Volume-linked pay to non-clinical actors is a structural precursor to the phantom-billing patterns above.

**7. Proceeds handling and obstruction as trailing behaviour.** The Brooklyn defendants laundered proceeds through multiple business entities to generate bribe cash; *Green*'s proceeds allegedly funded vacations, furniture and luxury goods; *Simon Katz* took $300,000 out of HealthNow and instructed an employee to lie to the FBI. One case in the set (*Kris Agency & Home Care* with *Career Development Center of Queens*) is not claims fraud at all — it is a $1.8M second-draw PPP scheme resting on false employee-count and affiliation certifications, settled for $2,347,133.10. It belongs to the same population of provider-side certification fraud, but it should not be counted as a billing pattern.

## What the schemes have in common

- **The setting is almost always the home or a residential program.** Home health agencies, in-home personal care, sober living homes, and social adult day care dominate. These are services with no institutional witness: the only evidence a visit occurred is a timesheet or a note produced by the entity being paid. Every phantom-claim case here exploits exactly that.
- **Small owner-operator entities, with the owner as the fraud actor.** Childress, Boyd-Wells, Green, Jordan, Scott, the Meadowses, the Katzes — the person who signs the enrollment paperwork is the person falsifying the records. The two exceptions are the corporate civil settlements (*Traditions Health*, *Medical Services of America / Community Home Health Services*), where the defect is a referral-compensation arrangement rather than a fabricated visit.
- **Layered, not single-mode.** Ten of the extracted records carry both a phantom-claims and a falsified-certificate tag, and five add kickbacks. The pattern is consistent: acquire patients improperly (kickback, recruitment, stolen discharge records), paper over eligibility or credentials, then bill. Detection logic that scores one mode in isolation will underweight these entities.
- **Long, uninterrupted runs.** *Blessings 4 Ever* spans Jan 2015–Dec 2023; *Green* July 2020–Feb 2026; *Scott* 2018–2024; *Antao/Wasef* Oct 2017–July 2024. Multi-year persistence means the anomalies were present in claims data for years before enforcement — these are not one-quarter outliers.
- **Ancillary lab and diagnostic services bolted onto a residential population.** *Serenity Keeper's* (urine drug testing), *Lifehouse* (drug testing lab timesheets), and *West Virginia Sleep Centers* (polysomnography) all convert a captive resident population into a recurring testing revenue stream, with no ordering or reviewing clinician in the Serenity Keeper's facts.
- **Public programs bear it, and Medicaid more than Medicare.** Medicaid appears in eight records against Medicare in five, and two cases reach VA community-care programs (*Boyd-Wells*, *Meadows / WV Sleep Centers*). *Boyd-Wells* and *Jordan* each hit two payers simultaneously — cross-payer blindness is part of the opportunity.
- **Relators and self-disclosure drive the civil side.** *Blessings 4 Ever* (relator took 21%), *Community Home Health Services*, and *Kris Agency* were qui tam actions; *Traditions Health* self-disclosed. In this sample, insiders — not analytics — surfaced the large-dollar civil matters.

## Detection signals for a predictive model

Signals below are named only where a case in this set demonstrates them.

**High-confidence, deterministic edits (available in claims alone):**
- **Home/community service dates overlapping institutional stays.** Cross-reference home health, personal care and adult day care claim service dates against inpatient claims for the same beneficiary. Four cases (*Blessings 4 Ever*, *Childress*, *Boyd-Wells*, *Green*) would fire. Note *Blessings 4 Ever*'s volume — 1,141 claims across 209 beneficiaries — meaning this is a rate/ratio feature per provider, not a one-off exception.
- **Cross-payer date overlap.** *Boyd-Wells* billed Missouri Medicaid and the VA Community Care Network; *Jordan* hit Medicaid and Medicare. Overlap checks confined to one payer would have missed part of both.
- **Impossible-hours and concurrency.** Billed units per attendant per day (*Serenity Keeper's*: six hours/day of peer support per resident), aggregate hours per worker across beneficiaries and across employers (*Green*: listed workers employed elsewhere on billed dates), and implausible overtime patterns (*Lifehouse*: 32 hours weekly overtime for months, hours during out-of-state travel).

**Certification and credential integrity:**
- **Certifying physician has no encounter history with the beneficiary.** *Scott* billed Medicare home health on physician certifications where no doctor had evaluated the patient. A feature comparing the certifying NPI against that beneficiary's prior/concurrent E/M claims is directly on-target, as is concentration of one certifying NPI across a single agency's census.
- **Rendering provider licensure/scope mismatch.** *HealthNow* (assessments outside scope), *Serenity Keeper's* (unlicensed peer support), *WV Sleep Centers* (non-physician-signed polysomnogram reports). This requires joining claims to state licensure and training-registry files; where the certificates themselves are forged (*Blessings 4 Ever*, 181 documents), claims data alone will not catch it — only registry-of-record verification will.
- **Diagnostics with no ordering or reviewing clinician.** *Serenity Keeper's*: $2.57M of urine drug tests "not ordered or reviewed by a medical provider." Lab claims whose ordering NPI has no contemporaneous E/M or treatment relationship with the beneficiary are a strong feature.

**Referral-network and entity-graph signals:**
- **Referral concentration between a residential program and a small set of labs** (*Serenity Keeper's* → three labs), and per-resident testing frequency.
- **Referral concentration from physician-medical directors who are also paid by the agency** (*Traditions Health*) and from physicians with a household or employment tie to agency staff (*Community Home Health Services* — physician spouse). Payment-to-referral joins (Open Payments, payroll, W-9/1099 data) plus referral-share concentration are the operative features.
- **Undisclosed affiliation between entities sharing addresses, officers or management companies.** *Blessings 4 Ever* operated alongside *V&V Management Solutions*; *Kris Agency* and *Career Development Center of Queens* concealed their affiliation. Entity-resolution on enrollment records is the control.
- **Beneficiary overlap across service types owned by the same network** — the Brooklyn scheme billed both social adult day care and a home health fiscal intermediary for the same referred Medicaid population.
- **Patient-acquisition anomalies:** clusters of new patients arriving from a single hospital discharge unit (*Scott*'s bribed discharge nurse), or new admissions sharing a recruiter/marketer pathway (*Green*'s recruited Medicaid patients; *Antao/Wasef*'s beneficiary cash bribes). Sudden census growth sourced from one referral node is observable.

**Enrollment and screening signals:**
- **Ownership attestation inconsistencies** — named owner who does not appear in payroll, tax or bank records; ownership churn at enrollment (*Childress*). Both concealed-ownership cases were designed to survive an exclusion/background screen, so the feature is the *discrepancy* across data sources, not the attestation itself.
- **Attestations about background-check registries that can be verified directly** (*Green*: Family Care Safety Registry claim). Automated registry lookups at enrollment and re-validation would fire.

**Behavioural / audit-response signals:**
- **Documentation absent or produced late.** *Scott*: files missing for over a third of billed patients. *Childress*: visits with no timesheets. A provider's documentation-production failure rate on audit sample requests is itself a predictive feature.
- **Documents created or dated after the audit request** (*Boyd-Wells* fabricated records in response to a Medicaid audit; *HealthNow* falsified documents for state inspectors). File metadata, submission timing and backdating checks belong in the post-audit workflow, and a prior falsified-audit-response should be a heavy prior on the provider.

## Caveats and sample limits

- **Thirteen documents, twelve distinct cases.** *Childress / Inspiring Angels* appears twice (plea and sentencing), so any per-case statistic computed on documents double-counts it. Twelve cases cannot support prevalence or base-rate claims about anything.
- **This is not a sample of health care fraud; it is a sample of home-based care fraud.** Almost every record involves home health, in-home personal care, sober living/recovery housing, or adult day care. There is exactly one lab-adjacent settlement (*WV Sleep Centers*), one drug-testing lab context (*Serenity Keeper's*, *Lifehouse*), and no hospital, physician-practice, DME, pharmacy, telehealth or behavioural-outpatient cases. Nothing here supports generalising these mechanics to other provider types.
- **Enforcement geography is not fraud geography.** Four records from Missouri (three distinct cases, all Eastern District of Missouri) reflect one office's activity, not Missouri's fraud density. The same caution applies to the two New York cases.
- **Two cases are allegations only.** *Green / A&L Angels* and the *Meadows / Lifehouse* complaint are at the "charged" stage; the *Blessings 4 Ever*, *Traditions Health*, *Community Home Health Services* and *Kris Agency* matters are civil settlements with no admission of liability. Patterns drawn from them describe what the government alleged.
- **Amount fields are not comparable.** Nine records carry a fraud amount and nine a settlement amount, and they mean different things (billed loss, restitution, FCA settlement including multipliers and a relator share, forfeiture). The $68M Brooklyn figure is billed amount and dominates any total; the $34M *Traditions Health* figure is a settlement with no loss figure recorded. Do not sum or average across these.
- **Sentence data is thin.** Only four records reflect imposed custody, and figures inside a single case span co-defendants (HealthNow's 24 months attaches to Veronica Katz, with Simon Katz not yet sentenced; Serenity Keeper's spans 60 months for Jordan, probation for Williams, 12 months and a day for Davis). No sentencing inference is supportable.
- **Missing fields.** *Kris Agency* has no payer or date range; *Traditions Health*, *Blessings 4 Ever*, *Community Home Health Services* and the *Meadows* case have no loss amount. The Kris Agency matter is PPP fraud, not claims fraud, and should be excluded from any claims-based modelling set.
- **No negative class and no denominators.** These records describe only detected, charged or settled conduct. Every "signal" above is a post-hoc description of caught schemes; none has been tested against compliant providers, so precision, recall and false-positive burden are unknown. Several signals (forged training certificates, forged physician signatures, concealed true ownership, fabricated audit responses) are by construction invisible in claims data and require external registries, licensure files or document forensics.

