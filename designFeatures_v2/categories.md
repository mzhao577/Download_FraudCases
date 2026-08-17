# Feature Categories

25 categories covering 679 cases from `extractedSummary_2025_DOJ.csv`.

| Category | Control point | Cases | Definition |
|---|---|---:|---|
| **Order Without Treating Encounter** | `prepay_edit` | 63 | Edits computing the gap between an ordered or prescribed item and the nearest qualifying E/M or telehealth encounter between the ordering provider and the beneficiary. |
| **No Claims System Nexus** | `no_payer_control` | 53 | Cases whose conduct has no claims-adjudication footprint at all, handled through law-enforcement intake, watchlist routing, restitution tracking or other non-payer channels. |
| **Impossible Day and Capacity Limits** | `prepay_analytics` | 52 | Analytics summing billed time-based minutes, overlapping service intervals, travel time between locations, licensed beds, instrument throughput or staffing ratios against physically or contractually possible limits. |
| **Product Provenance and Inventory Reconciliation** | `postpay_audit` | 51 | Reconciliation of billed drug, device, graft or reagent units against wholesaler pedigree, ARCOS, purchase invoices and dispensing or administration records, plus registry matching of UDI, serial, clearance, recall and NDC validity. |
| **Referral Concentration and Remuneration** | `referral_network` | 46 | Graph analysis of referral concentration, self-referral and ownership overlap between orderers and performing entities, joined to Open Payments, marketing-vendor, lease or per-claim payment flows. |
| **Coverage, Indication and Prior Auth Edits** | `prepay_edit` | 38 | Edits testing whether the billed service has a covered diagnosis, supporting clinical history, required frequency interval or a truthfully substantiated prior-authorisation assertion. |
| **Licence and Scope Verification** | `credentialing` | 32 | Primary-source verification that the rendering, prescribing or certifying identity holds an active licence, DEA registration, CLIA certificate, taxonomy, reassignment or credential covering the billed service on the date of service. |
| **Code Intensity and Upcoding Outliers** | `prepay_analytics` | 30 | Peer and self-baseline comparison of code-mix distributions such as high-level E/M shares, long-session psychotherapy, add-on attach rates, therapy tiers and highest-analyte panels. |
| **Enrolment Identity and Ownership Screening** | `enrolment` | 27 | Screening of enrolment applications for nominee or straw owners, undisclosed common control, synthetic identities and shared bank accounts, addresses or phones linking multiple billing NPIs or TINs. |
| **Fiduciary and Bank Account Monitoring** | `no_payer_control` | 25 | Cases with no payer-side control where funds are diverted from trusts, benefit plans, resident or vendor accounts, elderly customers or investors and only bank, treasury or fiduciary monitoring applies. |
| **Controlled Substance Prescriber Analytics** | `prepay_analytics` | 24 | Peer and trailing-baseline analytics on prescriber controlled-substance volume, MME per patient, schedule mix, patient travel radius, pharmacy channelling and prescribing-without-encounter rates. |
| **Relief Loan and Affiliation Screening** | `no_payer_control` | 24 | Cases with no payer-side control where the nearest check verifies loan or forgiveness payroll attestations against tax and wage filings and aggregates affiliated entities against programme size standards. |
| **Applicant Eligibility Verification** | `enrolment` | 23 | Identity, income, dependency and household verification of benefit applicants against SSA, vital records, wage files and shared-contact clustering before eligibility or benefit issuance. |
| **EVV, Attendance and Payroll Reconciliation** | `prepay_edit` | 23 | Reconciliation of billed visit units against electronic visit verification records, sign-in sheets, timesheets, payroll hours and prior-authorised units for in-home and facility-based services. |
| **Grant and Contract Award Integrity** | `no_payer_control` | 23 | Cases with no payer-side control where the nearest check sits in grant or procurement administration, covering disclosure and misconduct screens, deliverable and specification verification, conflicts and subrecipient payee checks. |
| **Bundling and Unit Limit Edits** | `prepay_edit` | 22 | Claim-line edits detecting unbundled panels or components, NCCI code-pair and modifier violations, medically unlikely unit ceilings, duplicate or split billing and group-service billed as individual. |
| **Employment Tax Withholding Gap** | `no_payer_control` | 21 | Cases with no payer-side control where the nearest check reconciles W-2 or payroll withholding against Form 941 filings and federal deposits for an employer or successor entity. |
| **Decedent and Ineligible Date Edits** | `prepay_edit` | 20 | Claim-level edits comparing the date of service against Death Master File dates, incarceration spans, inpatient or hospice periods, coverage termination and anatomical or sex contradictions. |
| **Controlled Substance Dispensing Edits** | `prepay_edit` | 18 | Pharmacy-claim edits on early refills, overlapping days supply, dangerous combination therapy, daily MME ceilings, prescriber-identity validation and multi-pharmacy or multi-prescriber shopping. |
| **Exclusion and Sanction Screening** | `credentialing` | 17 | Matching providers, owners, managing employees and submitters against OIG LEIE, state exclusion, preclusion, prior-revocation and indictment feeds at enrolment, revalidation and adjudication. |
| **Beneficiary Recruitment and Steering** | `referral_network` | 14 | Detection of patient brokering and enrolment steering through shared beneficiary addresses or phones, congregate-site clustering, out-of-area new-patient surges, recruiter graphs and broker or agent enrolment patterns. |
| **Cost Report and Risk Adjustment Audit** | `postpay_audit` | 13 | Post-payment review of cost reports, related-party and chain transfers, staffing and care-spend ratios, medical loss ratio reconciliation and risk-adjusting diagnoses unsupported by encounters. |
| **Orderer Dispersion and Signing Throughput** | `referral_network` | 11 | Network and velocity measures on ordering NPIs, counting distinct beneficiary states, supplier or lab NPIs, payers and signed orders per day relative to physically feasible review time. |
| **New Enrollee Billing Ramp** | `prepay_analytics` | 7 | Analytics on paid dollars or volume relative to a provider's own trailing baseline since enrolment or ownership change, including rapid ramps, post-acquisition spikes and same-week sweep-out of remittances. |
| **Record Authenticity and Cloning Review** | `documentation_request` | 2 | Requested-record review detecting duplicated or templated note text, reused signature and delivery-proof image hashes, backdated entries and documentation absent for billed time or units. |

## By control point

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

