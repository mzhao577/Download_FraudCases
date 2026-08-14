# Medical Fraud Cases - Extracted Features and Patterns

*Generated 2026-08-13T20:17:59-04:00 with `claude-opus-5`*

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
| local-home-healthcare-company-owner-admits-o | 2026-02-17 | Natavia Boyd-Wells (owner, Touch of the Heart Home H | Medicaid (Missouri Medicaid  | $209,000 | - | - | Phantom Claims |
| st-louis-county-home-healthcare-company-owne | 2026-02-17 | Daniell Green (owner and operator of A&L Angels Home | Medicaid (Missouri Medicaid  | $1,460,000 | - | - | Phantom Claims |
| home-health-care-operator-admits-defrauding- | 2026-03-20 | Camille S. Childress (operator/owner of Inspiring An | Medicaid (Missouri Medicaid) | $174,496 | $174,496 | 15 | Phantom Claims |
| former-sober-home-owner-and-operator-sentenc | 2026-04-24 | Delores Jordan (owner, Serenity Keeper's, LLC); Erne | Medicaid (Kentucky); Medicar | $2,569,946 | - | 60 | kickback_Bribery For Referral |
| michigan-home-health-care-agency-owner-convi | 2026-05-15 | Ruby Scott (nurse; owner of Delta Home Health Care L | Medicare | $1,600,000 | - | - | kickback_Bribery For Referral |
| queens-home-care-agency-and-home-health-aide | 2026-05-19 | Kris Agency & Home Care, Inc. (home care agency); Ca | Small Business Administratio | $1,800,000 | $2,347,133 | - | Covid or General Loan Fraud |
| u-s-attorney-moore-capito-announces-fraud-co | 2026-06-23 | Raymond C. "Rocky" Meadows II (founder and director, | Medicaid (West Virginia); Ve | - | $120,000 | - | Falsify certificate |
| home-health-care-operator-sentenced-for-defr | 2026-07-21 | Camille S. Childress (operator/owner); Inspiring Ang | Medicaid (Missouri Medicaid) | $174,496 | $174,496 | 15 | Phantom Claims |
| ceo-of-bay-area-home-health-agency-convicted | 2026-07-23 | Simon Katz; Veronica Katz (former CEO of HealthNow H | Medicare | $3,000,000 | $593,634 | 24 | Falsify certificate |
| philadelphia-in-home-care-services-provider- | 2026-08-04 | Blessings 4 Ever Home Care Agency LLC; V&V Managemen | Medicaid (Pennsylvania Medic | - | $1,000,000 | - | Falsify certificate |

## Fraud types (cases may carry several)

| Type | Cases |
|---|---|
| Phantom Claims | 10 |
| Falsify certificate | 8 |
| kickback_Bribery For Referral | 5 |
| FakeEncounter | 4 |
| Benefit & Eligibility Fraud | 4 |
| Wire Fraud | 3 |
| IdentityFraud | 2 |
| Covid or General Loan Fraud | 1 |

## Scheme combinations

| Combination | Cases |
|---|---|
| Benefit & Eligibility Fraud + Falsify certificate + Phantom Claims | 3 |
| Benefit & Eligibility Fraud + FakeEncounter + Falsify certificate + Phantom Claims | 1 |
| FakeEncounter + IdentityFraud + Phantom Claims + kickback_Bribery For Referral | 1 |
| Falsify certificate + Phantom Claims + Wire Fraud | 1 |
| Falsify certificate + IdentityFraud + Phantom Claims + kickback_Bribery For Referral | 1 |
| Falsify certificate + Phantom Claims | 1 |
| FakeEncounter + kickback_Bribery For Referral | 1 |
| Phantom Claims + Wire Fraud + kickback_Bribery For Referral | 1 |
| FakeEncounter + Falsify certificate + Phantom Claims + Wire Fraud | 1 |

## Payers defrauded

| Payer | Cases |
|---|---|
| Medicaid | 8 |
| Medicare | 5 |
| U.S. Department of Veterans Affairs Community Care Network | 1 |
| Small Business Administration (Paycheck Protection Program) | 1 |
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

**1. Phantom visits billed by owner-operated home care agencies.** This is the backbone pattern: the agency bills for visits, hours or aide shifts that never happened, and the supporting paper is created afterwards. *Camille Childress / Inspiring Angels LLC* (Missouri Medicaid, $174,496) billed for home health with no timesheets and no documentation at all. *Natavia Boyd-Wells / Touch of the Heart Home Health Care LLC* submitted "hundreds" of claims to Missouri Medicaid and the VA Community Care Network ($109,751 + $100,563). *Daniell Green / A&L Angels Home Healthcare Services LLC* is charged with manufacturing false timesheets covering $1.46M. *Ruby Scott / Delta Home Health Care LLC* billed Medicare $1.6M with files missing for more than a third of billed patients. *HealthNow Home Healthcare* (Katz) billed Medicare for services never provided as part of a $3M scheme. In the largest case, *Happy Family / Family Social Adult Day Care and Responsible Care Staffing* (Brooklyn), over $68M in New York Medicaid billing was either never provided or kickback-induced.

**2. The hospitalised-beneficiary overlap.** A distinct and highly repeatable sub-mechanic: billing in-home services on dates the patient was a hospital inpatient. It appears in four separate cases — Childress (clients hospitalized at the time), Boyd-Wells (veterans hospitalized on the service dates), Green (patients hospitalized), and *Blessings 4 Ever Home Care Agency* in Philadelphia, quantified precisely at 1,141 claims for 209 beneficiaries on days they were inpatients all day. That this crops up across four unrelated defendants in four states suggests the fabricators were working from patient rosters, not from actual schedules.

**3. Credential and certification fabrication.** Providers billed for services performed by people who were not qualified to perform them, and then forged the paperwork saying otherwise. *Blessings 4 Ever* allegedly fabricated or backdated 181 training certificates so personal care attendants would appear to meet Pennsylvania Medicaid training rules. *HealthNow* used unqualified staff to conduct home health assessments outside their scope of practice, forged physician signatures, and altered records shown to California Department of Public Health inspectors. *West Virginia Sleep Centers LLC* ($120,000 settlement) billed Medicaid and the VA for sleep studies and polysomnogram reports prepared and signed by unqualified non-physician staff. *Serenity Keeper's* billed Kentucky Medicaid for peer support not delivered by licensed peer support specialists.

**4. Kickbacks and referral-volume compensation.** Five cases, spanning the full spectrum from cash-in-envelopes to structured corporate arrangements:
- *Ruby Scott / Delta* paid a Detroit hospital discharge nurse over $130,000 — roughly $300 per billed patient, via CashApp, PayPal, check and cash — for faxed confidential Medicare patient records.
- *Delores Jordan / Serenity Keeper's* took checks, cash and ACH "consulting" payments up to $5,000, some routed through co-defendant Jerome Davis's company *X-Tremly for Christ, LLC*, for steering sober-home residents' urine drug tests to three labs.
- *Antao and Wasef* were paid as marketers to funnel Medicaid recipients into the Brooklyn adult day cares and home health intermediary, and paid cash bribes to the beneficiaries themselves.
- *Traditions Health LLC* paid remuneration to physician-medical directors in Oklahoma and Texas who referred Medicare home health patients ($34M settlement, self-disclosed).
- *Medical Services of America / Traditional Home Care* paid an employee bonuses keyed to the referral volume generated by the employee's physician spouse — a Stark violation resolved for $702,541.

**5. Identity misuse — of patients and of clinicians.** Scott used stolen hospital patient profiles and "used real doctors' identities to fabricate evaluations," falsely representing physician homebound certifications. *Lily Bell* in the Kentucky case pled guilty to aggravated identity theft involving a nurse practitioner's stolen identifiers. Green allegedly recruited Medicaid patients to "lend their names" for claims. In all three, the beneficiary or ordering clinician on the claim is real; the encounter is not.

**6. Enrollment and eligibility fraud to get and keep billing privileges.** Childress enrolled with Missouri Medicaid using paperwork naming a nominee owner, specifically to hide a disqualifying 2012 conviction. Green allegedly filed a false Medicaid participation agreement claiming registry enrollment and background checks, and concealed a co-defendant's felony drug conviction. HealthNow submitted falsified documents to state inspectors expressly "to preserve Medicare billing privileges." The fraud starts before the first claim.

**7. Medically unnecessary or unordered services.** Traditions Health's McAlester location billed Medicare for home health that was not medically necessary. The Kentucky labs billed roughly $2.57M for urine drug tests "not ordered or reviewed by a medical provider" — the service may have physically occurred, but nobody clinically wanted it.

**8. Upstream timesheet fraud feeding a downstream biller.** *Raymond and Helen Meadows / Lifehouse Inc.* allegedly submitted false timesheets to a drug testing lab — including 32 hours of weekly overtime and hours claimed during out-of-state vacations — and the lab paid on them and then sought reimbursement from West Virginia Medicaid and the VA. The entity that touched the payer was not the entity that lied.

**9. Non-claims program fraud (one case).** *Kris Agency & Home Care* and *Career Development Center of Queens* obtained over $1.8M in second-draw PPP loans by falsely certifying fewer than 300 employees and concealing their affiliation with each other; settled for $2,347,133. This is the only case in the set with no claims component, but it uses the same corporate-affiliation opacity seen elsewhere.

## What the schemes have in common

**The provider type is nearly monolithic.** Home health, personal care and home-based aide services appear in almost every case; the exceptions are the sober-home/lab combinations (Jordan, Meadows) and the Brooklyn adult day cares, which were paired with a home health fiscal intermediary anyway. These are low-capital, licence-light, small-LLC businesses where a single owner controls enrollment, scheduling, documentation and billing with no internal separation of duties. In eight of the twelve cases the named defendant is the owner or CEO.

**Documentation is the only control, and documentation is what gets faked.** Because home-based services are unobservable — no facility, no chart audit trail, no independent witness — the payer's sole verification is the agency's own paper. Every scheme here attacks that paper: timesheets (Green, Meadows), training certificates (Blessings 4 Ever), physician signatures and homebound certifications (Scott, HealthNow), ownership disclosures (Childress), participation agreements (Green). Two cases show fabrication specifically triggered by oversight — Boyd-Wells submitted fabricated documentation *during a 2022 Medicaid audit*, and HealthNow falsified documents *for state inspectors*. Audit response is itself a fraud surface.

**Related-entity layering.** Kickbacks and proceeds move through affiliated LLCs: V&V Management Solutions alongside Blessings 4 Ever; X-Tremly for Christ routing Jordan's payments; Responsible Care Staffing alongside the two Brooklyn day cares; the Kris Agency / Career Development Center affiliation concealed from SBA. The Brooklyn defendants explicitly "used multiple business entities to launder proceeds and generate the cash for bribes."

**Long undetected runs.** Where dates exist, schemes ran for years: Blessings 4 Ever 2015–2023, the Florida self-referral 2017–2025, Brooklyn 2017–2024, Delta 2018–2024, Traditions 2019–2024, Boyd-Wells 2020–2024. The short cases are the small ones (Childress, 2021–2022, $174K). Detection lag correlates with restraint in billing volume more than with scheme sophistication.

**Vulnerable, low-complaint populations.** Homebound Medicare beneficiaries, Medicaid recipients, sober-home residents in early recovery, veterans. These patients rarely review EOBs, and in the Brooklyn and Green cases were actively paid or recruited to participate.

**Detection routes were mostly not analytics.** Three civil cases came from qui tam relators (Blessings 4 Ever — relator took 21% of federal recovery; Medical Services of America; Kris Agency, "whistleblowers"), and Traditions Health *self-disclosed*. Only the hospitalisation-overlap findings look like data-driven detection.

**Loss magnitudes are extremely skewed.** The set spans $174,496 (Childress) to $68,000,000 (Brooklyn). Kickback-driven, multi-entity, recruiter-fed schemes are one to two orders of magnitude larger than solo-owner phantom-billing schemes. Any aggregate total or median across nine amounts is dominated by one case and should not be quoted as typical.

## Detection signals for a predictive model

These are hypotheses derived from the mechanics described in the records, not validated features — see caveats.

**Cross-claim concurrency checks (strongest signal in the set):**
- Home health / personal care / adult day care service dates that fall inside an inpatient stay for the same beneficiary. Four independent cases turn on this, and the Blessings 4 Ever record shows it is countable at scale (1,141 claims, 209 beneficiaries). This requires only joining the agency's claims to institutional claims for the same member — no chart review.
- Same rendering aide or clinician billed on two providers' claims for overlapping hours (Green: "listed workers were working elsewhere").
- Cumulative hours per attendant per day exceeding a feasible ceiling; Meadows' 32 hours of weekly overtime and hours logged during out-of-state travel are the same arithmetic impossibility one tier upstream.

**Fixed-quantity, non-varying billing:** Serenity Keeper's billed six hours per day of peer support. Flat, invariant per-member-per-day units with no clinical variance across a panel is a low-cost anomaly to compute.

**Credential and licensure joins:**
- Rendering-provider licence status at date of service against the state registry — would have caught the unlicensed peer support specialists (Serenity Keeper's), the non-physician polysomnogram signers (West Virginia Sleep Centers), and the out-of-scope assessors (HealthNow).
- Training-certificate issue dates that post-date the claims they purport to support, or that cluster suspiciously (181 documents at Blessings 4 Ever).

**Ordering/certifying physician anomalies:**
- Homebound certifications or plans of care attributed to a physician who has no evaluation/management claim for that beneficiary in a surrounding window — the exact gap Scott exploited by fabricating evaluations under real doctors' identities.
- A single NPI certifying an implausible share of one agency's admissions.
- Lab claims with a missing, invalid, or contested ordering NPI (Bell's use of a nurse practitioner's stolen identifiers; Kentucky tests "not ordered or reviewed by a medical provider").

**Referral concentration and source clustering:**
- Share of an agency's new admissions originating from a single discharge source or hospital unit. Scott's agency was fed by one discharge nurse at ~$300 per patient; the admissions graph would show an unnatural single-node dependency.
- Beneficiaries sharing a residential address, especially a sober-home address, funnelling drug tests to a small set of labs (Jordan) — address-clustering on the member file, not the claim.
- For Stark/AKS exposure: medical-director or employee compensation records cross-referenced against referral volume (Traditions Health; Medical Services of America's spouse-referral bonus). This is not visible in claims alone and requires payment-transparency or payroll data.

**Enrollment-file signals available before any claim:**
- Nominee/straw ownership: an owner of record with no operational footprint, or an ownership change immediately preceding enrollment (Childress).
- Shared address, phone, bank account or officer between an enrolling agency and an affiliated management company or training school (V&V Management; Kris Agency / Career Development Center — the affiliation the SBA case turned on).
- Exclusion- and criminal-history matching extended to family members, associates and prior entities of the applicant, since both Childress and Green allegedly enrolled specifically to route around disqualifications.

**Documentation-response behaviour:** inability to produce files on request — Delta had no files for over a third of billed patients, Childress had no timesheets at all. A "records produced / claims billed" ratio from prior audits is a strong provider-level prior, and a sharp change in documentation quality immediately after an audit notice (Boyd-Wells, HealthNow) is itself suspicious.

**Beneficiary-side patterns:** simultaneous enrollment in social adult day care and home health under a shared corporate family (Brooklyn), implausible travel distance between residence and day-care site, and beneficiaries whose utilisation begins abruptly with no prior claims history — consistent with recruited members "lending their names" (Green).

**Payer-crossing:** Boyd-Wells billed Missouri Medicaid *and* the VA Community Care Network; Meadows' lab billed West Virginia Medicaid *and* the VA. Neither payer alone sees the full picture. Cross-payer data sharing is a structural detection gap in at least two of twelve cases.

## Caveats and sample limits

- **Twelve distinct cases in thirteen documents is not a sample from which rates can be estimated.** The Childress matter appears twice (plea and sentencing) — a reminder that document counts overstate case counts and that any per-document statistic double-counts entities with long procedural histories.
- **Severe selection bias toward home health.** Almost every case involves home-based care. This tells us what these thirteen DOJ press releases were about; it does not establish that home health is the highest-risk sector overall. There are no hospital, physician-practice, DME, telehealth, hospice or pharmacy cases here at all, so nothing in this analysis speaks to those settings.
- **These are all detected, prosecuted cases.** Every pattern above is a pattern of *fraud that failed*. Schemes that avoid hospitalisation overlaps, keep documentation tidy, and stay below audit thresholds are absent by construction. A model trained on this population learns the signature of caught fraud.
- **No denominators.** There is no information about the population of non-fraudulent agencies, so none of the proposed features can be assessed for precision or false-positive rate. Legitimate agencies also bill on days a patient is briefly admitted, also have single dominant referral sources, and also have credential-file gaps.
- **Two cases are allegations only.** Green / A&L Angels and the Meadows / Lifehouse matter are at the *charged* stage; the Blessings 4 Ever, Traditions, Medical Services of America, Kris Agency and West Virginia Sleep Centers matters are civil settlements with no admission of liability. Descriptions above follow the records' own "allegedly" framing.
- **Amounts are not comparable across cases.** Some figures are amounts billed, some amounts paid (Delta: $1.6M loss, $1.2M paid), some settlement values that include multipliers and restitution (Kris Agency settled for more than the $1.8M obtained). Four cases have no FraudAmt and four have no SettlementAmt. Summing or taking medians across these mixes incompatible quantities.
- **Sentencing data is too thin to interpret.** Only four cases carry a jail term, and several defendants (Simon Katz, Scott, Boyd-Wells) were awaiting sentencing. No relationship between loss amount and sentence length can be inferred from four points — note that the $174K Childress case drew 15 months while the $2.57M Jordan case drew 60.
- **Geographic counts reflect prosecutorial activity, not fraud density.** Four Missouri cases is a fact about the Eastern District of Missouri's home health enforcement focus (three of them St. Louis-area home health agencies), not evidence that Missouri has more fraud than states with zero cases here.
- **FraudType labels are analyst-assigned, not charged offences.** The co-occurrence patterns (phantom claims almost always paired with falsified certification) are partly an artefact of how one summary gets tagged with multiple labels.
- **One case has no date range** (Kris Agency), and the PPP case is not claims fraud at all — it should be excluded from any claims-based modelling and treated as a separate program-integrity problem.

