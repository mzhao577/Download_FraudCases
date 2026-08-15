# Feature Categories

25 categories covering 679 cases from `extractedSummary_2025_DOJ.csv`.

| Category | Control point | Cases | Definition |
|---|---|---:|---|
| **Necessity And Frequency Edits** | `prepay_edit` | 53 | Prepay clinical-criteria, prior-authorization, frequency-cap, laterality and repeat-interval edits requiring qualifying diagnosis, prior conservative care or documented indication for specific procedures, tests and products. |
| **Referral Concentration And Kickback Analytics** | `referral_network` | 46 | Analytics on referrer-to-entity concentration, dyad revenue share, marketer and recruiter linkage, Open Payments correlation and disclosed financial arrangements, holding claims for Stark/AKS review. |
| **No Payer Control Applicable** | `no_payer_control` | 46 | Cases where no payer-side claim or enrolment control applies, including tax, obstruction, embezzlement and non-case press items to be excluded from rule mining. |
| **Treating Relationship Order Edits** | `prepay_edit` | 44 | Prepay edits requiring a qualifying encounter by the ordering provider within a lookback window, plus a supporting diagnosis, before paying order-driven items such as braces, genetic panels, DME and compounds. |
| **Grant And Loan Disbursement Screening** | `no_payer_control` | 43 | Pre-disbursement verification of payroll, affiliation size, ownership graphs, deliverables and conflicts for loan, grant, procurement and contract payments outside the health claim stream. |
| **Provider Day Capacity Edits** | `prepay_edit` | 40 | Accumulators that sum time-based units or implied minutes per rendering clinician per date across all sites and payers and deny, pend or downcode when totals exceed a feasible workday, overlap, or defy travel feasibility. |
| **Coding, Bundling And Upcoding Edits** | `prepay_edit` | 38 | Claim-level rebundling, NCCI pair, modifier-25, panel-versus-component, unit/charge sanity, site-of-service and level-distribution edits that deny, reprice or downcode inflated or unbundled coding. |
| **Inventory Acquisition Reconciliation** | `postpay_audit` | 35 | Comparison of billed drug, device or single-use-supply units against wholesaler, ARCOS, distributor or invoice acquisition records at provider-product-period level, suspending payment on unexplained excess. |
| **Prescriber Diversion Profiling** | `prepay_analytics` | 33 | Prescriber- and pharmacy-level controlled-substance profiling on volume, MME, patient distance, cash share, baseline step-changes and prescriber authentication, driving prepay holds and DEA or board referral. |
| **Benefit Eligibility Data Matching** | `enrolment` | 31 | Application-time and recertification identity, income, wage, death and duplicate-identity matching for member, benefit, subsidy, broker-driven and representative-payee enrolment decisions. |
| **Primary Source Credential Verification** | `credentialing` | 29 | Automated primary-source verification of licences, degrees, certifications, DEA registration, taxonomy and roster affiliation, with claim rejection when the rendering or supervising clinician is unverified, unlicensed or out of scope. |
| **Ordering Prescriber Fan-Out Analytics** | `prepay_analytics` | 29 | Surveillance of ordering or signing NPIs on orders per day, distinct downstream suppliers and labs, beneficiary state dispersion and share of orders lacking any encounter, with suspension of downstream claims from outlier prescribers. |
| **Enrolment Ownership Identity Graph** | `enrolment` | 28 | Entity-resolution and link-analysis screening at enrolment or revalidation that clusters applicants by owners, officers, addresses, phones, bank/EFT accounts, IPs, notaries and billing agents to detect shells, nominees and undisclosed common control. |
| **Device And Product Registry Validation** | `prepay_edit` | 24 | Validation of UDI, NDC, serial, lot, NIOSH or FDA registration identifiers on claims against authoritative registries, recall feeds and authorized-distributor lists, with denial of unapproved, counterfeit or unlisted products. |
| **Exclusion And Adverse Action Screening** | `credentialing` | 23 | Continuous or periodic matching of providers, owners, managing employees and staff against exclusion lists, criminal-conviction, licence-board and indictment feeds to deny enrolment or trigger credible-allegation payment suspension. |
| **Eligibility And Impossible Day Edits** | `prepay_edit` | 21 | Hard prepay edits denying claims whose service dates postdate death, fall in incarceration, inpatient or institutional spans, precede enrolment, or otherwise conflict with eligibility and facility status files. |
| **EVV And Attendance Verification** | `prepay_edit` | 16 | Reconciliation of home-, community- and centre-based service claims to electronic visit verification, GPS geofence, biometric sign-in or attendance records, denying units with no matching verified visit. |
| **Payee And Disbursement Controls** | `enrolment` | 16 | Controls on payment routing and internal disbursement: EFT change callback verification, payee-account dedup and employee matching, dual approval, adjudicator override monitoring and vendor-master change holds. |
| **Controlled Substance Point Of Sale Edits** | `prepay_edit` | 14 | Member-level pharmacy edits and lock-in using MME, early refill, days-supply overlap, dangerous-combination, multi-prescriber and multi-pharmacy counts to reject or force prior authorization at the point of sale. |
| **Facility Certification And Quality Review** | `postpay_audit` | 14 | Prepay medical review or payment suspension driven by facility-level certification, licensure scope, survey deficiency, hospice or SNF length-of-stay, live-discharge, level-of-care and admission-provenance indicators. |
| **Cost Report And Related Party Audit** | `postpay_audit` | 14 | Post-payment audit of cost reports, related-party vendor disclosures, chain financial viability, trust-account reconciliations and unreturned identified overpayments, holding settlement or escrowing payment. |
| **Staffing And Payroll Reconciliation** | `postpay_audit` | 13 | Comparison of billed service hours, units or census against payroll, roster, FTE, licensed-capacity or payroll-based-journal data to detect hours or attendance that no staffed workforce could deliver. |
| **New Provider Velocity Throttle** | `prepay_analytics` | 12 | Payment caps, prepay holds, site visits and ramp-rate monitoring applied to newly enrolled or newly transferred providers whose early billing volume, dollars or beneficiary counts exceed peer-calibrated norms. |
| **Beneficiary Cohort And Recruitment Graph** | `referral_network` | 12 | Detection of shared or compromised beneficiary cohorts across unrelated providers, address clustering, burst arrivals and identity misuse, triggering beneficiary verification outreach and coordinated suspension. |
| **Documentation Authenticity Review** | `documentation_request` | 5 | Records requests paired with authenticity testing of submitted documentation, including note near-duplicate hashing, signature-image reuse, metadata and physician attestation of forged orders. |

## By control point

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

