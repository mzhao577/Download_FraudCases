# Fraud Monitoring Features

| | |
|---|---|
| **Source** | `downloaded/webtool/extractedSummary_2025_DOJ.csv` — 679 prosecuted cases (DOJ, 2025) |
| **Features** | 10 |
| **Generated** | 2026-08-14 |
| **Specification** | [`instruction_designFeatures.md`](../instruction_designFeatures.md) |
| **Reproduce** | `designFeatures/analyze.py` → `design_features.py` → `render_features.py` |

Each feature is a signal a payer could compute against claims, enrolment or credentialing data, derived from mechanics that recur across the case corpus.

## Index

| # | Feature | Service groups | Cases | Priority |
|---:|---|---|---:|---|
| 1 | [Order sign-off velocity per ordering NPI (DME, lab, genetic)](#1-signoff-velocity-orders-per-signing-npi) | Telehealth, DME, GeneticTesting, Laboratory… | 55 | high |
| 2 | [Impossible provider service-day: billed time exceeds available hours](#2-impossible-service-day-hours) | BehavioralHealth, SubstanceUseTreatment, PhysicianPractice, HomeHealth… | 110 | high |
| 3 | [Service dates conflicting with beneficiary death, inpatient stay or incarceration](#3-service-date-vs-beneficiary-status) | All | 110 | high |
| 4 | [New enrolee billing ramp with concentrated ordering source (no claims history needed)](#4-new-supplier-ramp-no-history) | DME, Laboratory, GeneticTesting, Hospice… | 40 | high |
| 5 | [Enrolment screen: excluded/convicted persons and nominee-owner indicators](#5-enrolment-exclusion-and-hidden-ownership) | DME, Hospice, Laboratory, BehavioralHealth… | 40 | high |
| 6 | [Dispensed quantity exceeds verifiable wholesale acquisition](#6-pharmacy-dispense-vs-wholesale-purchase) | Pharmacy | 19 | high |
| 7 | [Panel stacking and same-day presumptive+definitive testing without review](#7-lab-panel-stacking-and-reflex-without-review) | Laboratory, SubstanceUseTreatment, PhysicianPractice | 37 | high |
| 8 | [Hospice election without terminal-illness trajectory: live discharge and certifier concentration](#8-hospice-nonterminal-and-live-discharge) | Hospice, NursingHome, HomeHealth | 20 | medium |
| 9 | [EVV geolocation mismatch and attendant double-booking in home/personal care](#9-evv-geolocation-and-attendant-overlap) | PersonalCare, HomeHealth, BehavioralHealth, AdultDayCare | 30 | medium |
| 10 | [Procedure-substitution upcoding: high-paying code without required setting or supply](#10-procedure-substitution-upcode-pairs) | PhysicianPractice, DME, Chiropractic, Optometry… | 127 | medium |

---

## 1. Order sign-off velocity per ordering NPI (DME, lab, genetic)

**Service groups** — `Telehealth`, `DME`, `GeneticTesting`, `Laboratory`, `Pharmacy`

**Mechanic.** Telemedicine outfits pay physicians and NPs a per-order fee to sign pre-populated DME/genetic-test orders for beneficiaries they never examined, often at rates of thousands of orders per clinician.

### Feature to be created

Unit of observation: ordering/referring NPI x calendar month. Compute (a) count of distinct beneficiaries appearing as the ordering/referring provider on DME (HCPCS L-codes, K-codes), CGx/PGx molecular pathology, or topical compound claims; (b) share of those beneficiaries for whom the same NPI has NO evaluation & management, telehealth, or any other professional claim within the prior 12 months or following 90 days; (c) count of distinct billing suppliers/labs downstream of that NPI; (d) count of distinct states of beneficiary residence. Also compute beneficiary-per-day maximum for order dates.

### Alert logic

Fire when the no-prior-encounter share exceeds a high percentile of same-specialty peers AND downstream distinct supplier count is above peer percentile AND monthly ordered-beneficiary count exceeds a plausible panel ceiling. Action: prepay edit placing the NPI's downstream DME/genetic claims into documentation review (request the signed order plus encounter note). Thresholds must be calibrated on a control population of the same specialty, telehealth-heavy vs office-based, because the corpus gives mechanics not cut-points.

### Data required

- claim line ordering/referring NPI
- claim line rendering/billing NPI (supplier or lab)
- HCPCS/CPT code
- beneficiary ID and state of residence
- professional E&M and telehealth claim history by beneficiary-provider pair
- order/prescription date

### Evidence

**55** of 679 cases support this feature. Keyword probe `telehealth_signoff` independently finds 55.

Example cases:

- `alabama-doctor-pleads-guilty-to-6-million-telemedicine-health-care-fraud-scheme_8435d6b83c17.pdf`
- `doctor-sentenced-for-70m-medicare-fraud-scheme_8ffdd9c280f1.pdf`
- `coeur-dalene-physician-found-guilty-in-telemarketing-medicare-fraud-conspiracy_ed1e677a36a7.pdf`
- `ceo-of-health-care-software-company-sentenced-for-1b-fraud-conspiracy_b3c1f5c03254.pdf`

### False positives

Legitimate high-volume telehealth and locum tenens clinicians, and hospitalists/SNF-ists who order for patients seen under another billing entity, will show low prior-encounter rates. Damp by excluding orders where any affiliated group TIN has an encounter for that beneficiary, by requiring the multi-state and multi-supplier conditions jointly, and by carving out clinicians enrolled in recognised telehealth groups with documented visit claims.

---

## 2. Impossible provider service-day: billed time exceeds available hours

**Service groups** — `BehavioralHealth`, `SubstanceUseTreatment`, `PhysicianPractice`, `HomeHealth`, `PersonalCare`, `Chiropractic`

**Mechanic.** Providers bill time-based psychotherapy, counselling, home-care or in-home visit codes summing to far more than a working day, or duplicate the same hour across employers or across clients.

### Feature to be created

Unit of observation: rendering NPI x date of service. Convert every time-based or timed-unit code (psychotherapy 908xx, CSW/community support, personal care 15-minute units, home health aide G-codes, in-home E&M) into implied minutes using the code's defining time, sum across all claim lines and all billing TINs for that NPI on that date, and produce implied_hours. Separately compute count of dates in a rolling 90 days where implied_hours > 16 and > 24, and count of overlapping intervals where start/end times are recorded.

### Alert logic

Any single date with implied_hours > 24 is a hard flag; > 16 hours on 3+ dates in 90 days is a soft flag. Hard flag triggers prepay suspension of that NPI's timed-code claims and a records request; soft flag triggers retrospective audit sampling. The 16-hour soft threshold is illustrative and must be calibrated against a control distribution of high-volume behavioural-health clinicians before use.

### Data required

- rendering NPI on each claim line
- date of service and, where captured, start/stop times
- CPT/HCPCS code with defined time increment
- units billed
- billing TIN so cross-employer aggregation is possible

### Evidence

**110** of 679 cases support this feature. Keyword probe `not_delivered` independently finds 110.

Example cases:

- `north-haven-counselor-sentenced-to-more-than-3-years-in-federal-prison-for-defrauding-medicaid-of-more-than-1-_d49441a1bede.pdf`
- `charlotte-clinic-owner-agrees-to-settle-allegations-of-medicaid-fraud_378d0564dbdc.pdf`
- `healthcare-worker-pleads-guilty-to-double-billing-district-of-columbia-medicaid-programs_39fe5d2bda70.pdf`
- `little-rock-psychologist-indicted-by-federal-grand-jury-for-defrauding-medicare-and-arkansas-blue-cross-blue-s_4aef40e13175.pdf`

### False positives

Group practices that bill all encounters under a supervising physician's NPI, and incident-to or locum arrangements, inflate a single NPI's implied hours legitimately. Damp by resolving supervising vs performing provider fields where available, excluding facility-based global codes, and treating group-billed NPIs as a separate peer stratum rather than flagging them outright.

---

## 3. Service dates conflicting with beneficiary death, inpatient stay or incarceration

**Service groups** — `All`

**Mechanic.** Claims are submitted for beneficiaries who were deceased, hospitalised, incarcerated or otherwise unable to receive the billed outpatient service on that date.

### Feature to be created

Unit of observation: claim line. Build a per-beneficiary status calendar from (a) date of death from enrolment/EDB feeds, (b) inpatient facility admission/discharge spans, (c) SNF/hospice election spans, (d) incarceration or out-of-country indicators where the payer holds them. Flag any professional, DME, lab, home-health, personal-care or transport line whose date of service falls after date of death, or falls inside an inpatient span for a service type that is not payable during inpatient status.

### Alert logic

Post-death lines: hard prepay edit rejecting the line and counting toward a provider-level post-death claim rate. Inpatient-conflict lines: flag for review, and compute per-provider conflict_rate = conflicting lines / total lines per quarter; providers above a peer percentile get a records request. Conflict rates in a clean population are non-zero because of date-of-death lag, so the percentile cut must be calibrated locally.

### Data required

- beneficiary date of death with source and update timestamp
- Part A / facility inpatient admission and discharge dates
- hospice and SNF election spans
- claim line date of service and place of service
- provider identifiers

### Evidence

**110** of 679 cases support this feature. The nearest keyword probe (`deceased_or_inpatient`) finds **25**; the higher figure comes from reading the summaries in full, and is an estimate rather than a verified count.

Example cases:

- `clinic-owner-arrested-in-multimillion-dollar-fraud-scheme-involving-non-existent-psychotherapy-services_69dcc3c33bda.pdf`
- `hendersonville-doctor-and-her-office-manager-husband-indicted-as-part-of-the-department-of-justice-039-s-2025-_46f32fb85e72.pdf`
- `indian-national-sentenced-to-prison-for-medicare-fraud-scheme-that-stole-more-than-1-million-in-taxpayer-funds_382b9ef58021.pdf`
- `illinois-doctor-sentenced-to-34-months-in-prison-for-evading-1-6m-in-taxes-and-committing-health-care-fraud_729d34a9966f.pdf`

### False positives

Date-of-death records lag and are sometimes wrong, and legitimate services (final-day care, DME delivered before death, professional consults during an inpatient stay billed with the correct modifier) will trip the rule. Damp with a grace window around death, by honouring valid inpatient-professional modifiers, and by requiring a provider-level elevated rate rather than acting on isolated lines.

---

## 4. New enrolee billing ramp with concentrated ordering source (no claims history needed)

**Service groups** — `DME`, `Laboratory`, `GeneticTesting`, `Hospice`, `HomeHealth`, `BehavioralHealth`

**Mechanic.** Newly enrolled or newly acquired supplier shells bill enormous volumes within weeks of enrolment, all resting on orders from one or a handful of ordering NPIs, then close before recoupment.

### Feature to be created

Unit of observation: billing provider (NPI/TIN) x week, restricted to providers whose Medicare/Medicaid enrolment effective date or ownership-change date is within the prior 12 months. Compute (a) cumulative billed charges by week since first claim; (b) Herfindahl concentration of ordering NPIs across all claims to date; (c) count of distinct beneficiary states versus supplier's service area; (d) share of claims for the single highest-paying HCPCS in the provider's mix. Requires no prior claims history for the provider itself — the baseline is the peer distribution of same-specialty new enrolees.

### Alert logic

Flag when weekly billed charges cross the peer new-enrolee distribution's upper tail AND ordering-NPI concentration is extreme (e.g. top 1-2 orderers account for most claims) AND beneficiary geography is dispersed beyond the supplier's declared service area. Action: prepay payment suspension pending site verification and beneficiary contact for a sample. All cut-points must be calibrated against a control cohort of legitimate new enrolees, which also ramp quickly.

### Data required

- provider enrolment effective date and ownership-change date
- weekly billed and allowed amounts
- ordering/referring NPI per claim
- beneficiary residence ZIP
- supplier declared service area / practice location
- HCPCS mix

### Evidence

**40** of 679 cases support this feature. Keyword probe `telehealth_signoff` independently finds 55.

Example cases:

- `11-defendants-indicted-in-multi-billion-health-care-fraud-scheme-the-largest-case-by-loss-amount-ever-charged-_ec7a233deffb.pdf`
- `new-jersey-business-owner-sentenced-to-87-months-for-172-million-fraud-and-money-laundering-scheme_3f44109d893c.pdf`
- `justice-department-files-two-civil-forfeiture-actions-to-recover-nearly-11-million-in-health-care-fraud-procee_5fb3ae64700e.pdf`
- `middletown-resident-charged-in-health-care-fraud-scheme-involving-durable-medical-equipment_333412e93142.pdf`

### False positives

Legitimate start-ups, practices acquired by a larger group, and single-specialty suppliers serving one large referring clinic all show concentrated orderers and steep ramps. Damp by requiring the geographic-dispersion condition, checking whether the concentrated orderer is co-located or commonly owned, and by escalating to prepay review rather than denial on first trip.

---

## 5. Enrolment screen: excluded/convicted persons and nominee-owner indicators

**Service groups** — `DME`, `Hospice`, `Laboratory`, `BehavioralHealth`, `HomeHealth`, `Pharmacy`, `SubstanceUseTreatment`

**Mechanic.** Individuals excluded, revoked or previously convicted enrol through paid nominee or straw owners and fabricated ownership records so they can keep billing.

### Feature to be created

Unit of observation: enrolment application / revalidation record. Compute a composite flag set at enrolment and at every ownership change: (1) any listed owner, officer, managing employee or authorised official matches HHS-OIG LEIE, SAM debarment, state Medicaid exclusion, or the payer's own prior-revocation list on name+DOB+SSN; (2) the practice address, phone, bank routing/account, or authorised-official email matches any currently or previously revoked provider; (3) owner has an owner-role in 3+ enrolled entities of the same specialty within 24 months; (4) owner's residence is out of state or out of country relative to the service location; (5) ownership transferred within 90 days of a payment suspension on the predecessor entity.

### Alert logic

Any single hard match (criterion 1) blocks enrolment pending adjudication. Two or more of criteria 2-5 route the application to enhanced screening: site visit, fingerprint-based background check, and a payment cap or prepay review for the first 6 months of billing. Weighting across the soft criteria needs calibration against a control set of clean enrolments, since shared addresses and multi-entity ownership are common and benign.

### Data required

- enrolment application owner/officer/managing-employee identities with SSN/DOB
- LEIE, SAM, state exclusion and prior-revocation lists with effective dates
- practice address, phone, bank account and email on file
- ownership-change and CHOW records with dates
- payment suspension history by entity

### Evidence

**40** of 679 cases support this feature. Keyword probe `nominee_shell` independently finds 40.

Example cases:

- `durable-medical-equipment-owner-sentenced-to-12-years-for-61-million-medicare-fraud-scheme_57f2cb90140a.pdf`
- `glendale-woman-sentenced-to-9-years-in-federal-prison-for-10-6-million-hospice-fraud-scheme-involving-kickback_ea9a28b73115.pdf`
- `blood-test-lab-owner-pleads-guilty-to-evading-over-11-2-million-in-federal-taxes-by-using-shill-to-illegally-c_8241e8a619ac.pdf`
- `owner-of-halo-home-healthcare-sentenced-to-4-years-in-prison-for-health-care-fraud-tax-crimes_c5fd2a1b28b5.pdf`

### False positives

Common names produce false exclusion matches, and legitimate multi-site operators and billing-service addresses shared across many clean providers will trip the address/phone criteria. Damp by requiring at least two identifiers to match for exclusion hits, by maintaining an allow-list of known billing-agent and registered-agent addresses, and by treating chain ownership as a distinct stratum.

---

## 6. Dispensed quantity exceeds verifiable wholesale acquisition

**Service groups** — `Pharmacy`

**Mechanic.** Pharmacies bill Part D, Medicaid and commercial plans for high-cost drugs they never purchased and never dispensed, with inventory records manipulated to hide the gap.

### Feature to be created

Unit of observation: pharmacy NPI x NDC (or therapeutic-equivalent group) x quarter. Compute billed_units = sum of metric quantity on paid pharmacy claims; acquired_units = sum of units from wholesaler 867/ARCOS-style purchase feeds or, where unavailable, from the pharmacy's attested inventory purchase reporting. Ratio = billed_units / acquired_units, plus an absolute gap in dollars at plan-paid price. Restrict initially to the top-cost NDC deciles (specialty, HIV, oncology, antipsychotic, inhaler, brand injectables) as those recur in the corpus.

### Alert logic

Flag when billed_units exceeds acquired_units by more than a tolerance band for two consecutive quarters, or when the dollar gap exceeds a materiality floor in one quarter. Action: retrospective audit and invoice request; for repeat offenders, prepay review on the affected NDCs. This works retrospectively only, since purchase data lags claims. Tolerance band must be calibrated to account for legitimate inventory carry-over, returns and transfers.

### Data required

- pharmacy claim NDC, metric quantity, days supply, plan-paid amount
- wholesaler purchase/invoice data or 867 chargeback feed by pharmacy DEA/NPI
- inventory transfer and return records where available
- pharmacy NPI-to-DEA crosswalk

### Evidence

**19** of 679 cases support this feature. Keyword probe `not_delivered` independently finds 110.

Example cases:

- `five-new-jersey-pharmacies-agree-to-pay-1-935-million-to-resolve-false-claims-act-allegations-of-billing-for-d_06b491c8d9f9.pdf`
- `michigan-pharmacist-sentenced-to-46-months-in-prison-for-4m-health-care-fraud-scheme_4b48bd8ea077.pdf`
- `pharmacist-and-brother-sentenced-to-prison-for-15m-health-care-and-wire-fraud-scheme_1dd3ccb84346.pdf`
- `pharmacy-owner-sentenced-to-87-months-in-prison-and-administrator-sentenced-to-72-months-for-their-respective-_6c9544157e42.pdf`

### False positives

Purchases through a secondary wholesaler, chain warehouse transfers, 340B replenishment and split-billing all break the one-to-one link between purchase feeds and dispensing. Damp by aggregating purchases at the chain/warehouse level, excluding 340B contract pharmacies unless separate data exists, and using a multi-quarter persistence requirement.

---

## 7. Panel stacking and same-day presumptive+definitive testing without review

**Service groups** — `Laboratory`, `SubstanceUseTreatment`, `PhysicianPractice`

**Mechanic.** Labs add high-paying respiratory pathogen panels or definitive drug confirmations onto every specimen, or unbundle a panel into component codes, without any clinician reviewing the screening result.

### Feature to be created

Unit of observation: performing lab NPI x month, with a companion ordering-provider view. Compute (a) reflex_rate = share of beneficiaries with a presumptive drug screen who also have a definitive/confirmatory test (G0480-G0483 family) on the same date of service; (b) panel_add_rate = share of specimens with a COVID or single-pathogen order that also carry a multiplex respiratory or GI panel on the same accession date; (c) unbundling_index = ratio of summed component-code payments to the payment for the equivalent bundled panel code, per beneficiary-day; (d) per-beneficiary testing frequency (tests per beneficiary per 30 days).

### Alert logic

Flag labs whose reflex_rate, panel_add_rate or unbundling_index sit in the extreme upper tail of the peer distribution for their lab type, or whose per-beneficiary testing frequency exceeds a clinical plausibility ceiling. Action: prepay edit requiring documentation of individualised medical necessity for the add-on code, plus review of the ordering arrangement for standing/blanket orders. Peer tails must be set from a control population; pain-management and SUD labs legitimately reflex more than general labs.

### Data required

- performing lab NPI and accession/date of service
- CPT/HCPCS for presumptive, definitive, and multiplex panel codes
- ordering provider NPI and specialty
- beneficiary ID for longitudinal frequency
- payment amounts by code for the unbundling comparison

### Evidence

**37** of 679 cases support this feature. The nearest keyword probe (`urine_drug_testing`) finds **16**; the higher figure comes from reading the summaries in full, and is an estimate rather than a verified count.

Example cases:

- `connecticut-lab-its-owners-and-officers-to-pay-more-than-1-2-million-to-settle-false-claims-act-allegations_263df8f50cc2.pdf`
- `diagnostic-laboratory-agrees-to-pay-more-than-9-million-to-settle-alleged-false-claims-act-violations_bfab071a06c4.pdf`
- `tri-cities-urgent-care-clinic-agrees-to-pay-2-8-million-to-resolve-claims-of-overbilling-for-diagnostic-tests_254a12f2fd51.pdf`
- `austin-pain-management-doctor-and-pain-medicine-practice-to-pay-13-625-000-to-settle-civil-false-claims-act-al_b38853c294d5.pdf`

### False positives

Genuine high-acuity SUD treatment programmes and immunocompromised populations warrant frequent definitive testing and multiplex panels; outbreak periods legitimately spike panel use. Damp by stratifying peers on ordering-provider specialty and patient mix, by seasonally adjusting panel rates, and by exempting labs that can show documented reflex protocols with clinician sign-off.

---

## 8. Hospice election without terminal-illness trajectory: live discharge and certifier concentration

**Service groups** — `Hospice`, `NursingHome`, `HomeHealth`

**Mechanic.** Hospices enrol beneficiaries who are not terminally ill, using marketer kickbacks and a small number of physicians who certify and recertify terminal illness sight-unseen.

### Feature to be created

Unit of observation: hospice provider x rolling 12 months. Compute (a) live_discharge_rate = beneficiaries discharged alive / total elections; (b) median and 90th-percentile length of stay, plus share of stays ending between 150 and 210 days; (c) certifier concentration: share of elections certified by the top 1-3 attending/certifying physicians; (d) share of elected beneficiaries with no inpatient admission, no oncology/serious-illness diagnosis cluster, and no hospice-consistent drug utilisation in the 12 months before election; (e) share of certifying physicians with no other claim for that beneficiary in the prior 12 months.

### Alert logic

Flag hospices in the upper tail on live_discharge_rate combined with high certifier concentration and a high share of beneficiaries lacking a serious-illness clinical footprint. Action: targeted medical review of election certifications and face-to-face encounter documentation; escalate to payment suspension if the certifier also appears in kickback-arrangement data. Retrospective by construction for live-discharge; the pre-election clinical-footprint component can run at the time of the election notice, making it partly prepay. Thresholds require calibration by hospice size and case mix.

### Data required

- hospice election and revocation/discharge dates with discharge reason
- certifying and attending physician NPI on the election
- beneficiary diagnosis and utilisation history 12 months pre-election
- Part A inpatient and SNF history
- hospice claim revenue codes and levels of care

### Evidence

**20** of 679 cases support this feature. Keyword probe `medically_unnecessary` independently finds 127.

Example cases:

- `four-more-charged-in-110-million-hospice-fraud-scheme_8e8e7071cac3.pdf`
- `two-west-covina-women-arrested-on-indictment-alleging-4-8-million-hospice-services-scheme-to-defraud-medicare_f7df5b60eddf.pdf`
- `glendale-woman-sentenced-to-9-years-in-federal-prison-for-10-6-million-hospice-fraud-scheme-involving-kickback_ea9a28b73115.pdf`
- `saad-healthcare-agrees-to-pay-3m-to-settle-false-claims-act-allegations-that-it-billed-medicare-for-ineligible_92d0d3c6dda8.pdf`

### False positives

Small hospices, and those serving dementia or debility populations, legitimately show long stays and some live discharges when patients stabilise; a single medical director properly certifies most patients at a small agency. Damp by size-stratified peer groups, by requiring at least two of the three components to fire, and by weighting the pre-election clinical-footprint signal most heavily since it is the least confounded.

---

## 9. EVV geolocation mismatch and attendant double-booking in home/personal care

**Service groups** — `PersonalCare`, `HomeHealth`, `BehavioralHealth`, `AdultDayCare`

**Mechanic.** Attendants, agency owners and consumer-directed enrolees submit electronic visit verification or timesheets for visits that never happened, sometimes for attendants living hundreds of miles away or working two clients at once.

### Feature to be created

Unit of observation: attendant/caregiver identifier x visit. Compute (a) distance between the EVV check-in geolocation (or originating phone number's registered location) and the client's service address; (b) overlap minutes between this visit and any other visit claimed by the same attendant across all agencies; (c) attendant's home address distance from client address; (d) per-attendant weekly billed hours; (e) share of an agency's visits where check-in and check-out originate from the same device as the agency office or the owner's phone. Aggregate to agency level as rates.

### Alert logic

Hard flag any visit with attendant-level overlap greater than a small tolerance, or check-in geolocation more than a set radius from the service address. Agency-level flag when the rate of such visits exceeds the peer upper tail. Action: prepay hold on the attendant's claims and a records/timesheet request to the agency; refer consumer-directed cases where enrolee and attendant addresses are hundreds of miles apart. Radius and overlap tolerances need calibration against a control set, since GPS drift and rural addressing are noisy.

### Data required

- EVV check-in/check-out timestamps and geolocation or caller ID
- client service address
- attendant identifier and home address of record
- claim line units and dates across all employing agencies
- agency office address and registered devices

### Evidence

**30** of 679 cases support this feature. The nearest keyword probe (`impossible_volume`) finds **10**; the higher figure comes from reading the summaries in full, and is an estimate rather than a verified count.

Example cases:

- `bucks-county-home-care-company-and-its-owners-and-managers-charged-in-alleged-health-care-fraud-scheme_d0fe1cc53635.pdf`
- `personal-health-care-aide-charged-with-health-care-fraud_59f9a5fbe980.pdf`
- `danville-woman-sentenced-for-health-care-fraud_6da9d3ffc819.pdf`
- `hampton-man-sentenced-to-over-nine-years-in-prison-for-defrauding-virginia-medicaid-and-virginia-unemployment_750836723568.pdf`

### False positives

Clients seen in the community (medical appointments, day programmes), poor GPS in rural or high-rise settings, and back-to-back visits in the same building all generate mismatches and apparent overlaps. Damp by allowing community-visit modifiers, using a generous urban/rural-specific radius, ignoring overlaps under a few minutes, and requiring an agency-level elevated rate before any payment action.

---

## 10. Procedure-substitution upcoding: high-paying code without required setting or supply

**Service groups** — `PhysicianPractice`, `DME`, `Chiropractic`, `Optometry`, `WoundCare`, `NursingHome`

**Mechanic.** Providers bill a high-reimbursement surgical or complex code while actually delivering a cheap, often non-covered item or a simpler service — taped electro-acupuncture devices billed as implanted neurostimulators, non-surgical debridement billed as surgical, group therapy billed as individual, mid-level services billed as physician services.

### Feature to be created

Unit of observation: rendering NPI x quarter, for a curated list of substitution-prone code pairs (implanted neurostimulator vs electro-acupuncture device supply; surgical excisional debridement vs selective/non-surgical debridement; individual vs group therapy; physician-rate E&M vs incident-to/mid-level; flap repair vs linear repair). For each pair compute the high-code share = high-paying code volume / (high + low) volume, and a corroboration flag: presence or absence of the required facility place-of-service, anaesthesia claim, operating-room facility claim, implantable device HCPCS, or supervising-physician presence on the same date.

### Alert logic

Flag providers whose high-code share exceeds the specialty peer upper tail AND whose corroboration flag is absent on more than a small share of those claims (e.g. surgical debridement billed with no facility or device line). Action: prepay edit requiring the corroborating line or documentation; retrospective extrapolated audit for established outliers. Peer tails and the corroboration-absence tolerance must be calibrated per specialty, since office-based procedures legitimately lack facility claims.

### Data required

- rendering NPI and specialty
- CPT/HCPCS and modifier on every line
- place of service
- paired facility, anaesthesia and device/implant claim lines for the same beneficiary-date
- supervising provider field where captured

### Evidence

**127** of 679 cases support this feature. The nearest keyword probe (`upcode_level`) finds **7**; the higher figure comes from reading the summaries in full, and is an estimate rather than a verified count.

Example cases:

- `united-states-obtains-more-than-1-4-million-judgment-against-family-medical-practitioner-for-fraudulent-billin_9fb9e6d54882.pdf`
- `vohra-wound-physicians-and-its-owner-agree-to-pay-45m-to-settle-fraud-allegations-of-overbilling-for-wound-car_08fa6f6e252a.pdf`
- `eureka-chiropractor-sentenced-to-20-months-in-prison-and-ordered-to-repay-more-than-2-3-million-for-defrauding_9a1ea9ebb6d0.pdf`
- `dermatology-providers-agree-to-pay-nearly-850-000-to-resolve-allegations-of-false-wound-repair-claims_81868526afd5.pdf`

### False positives

Genuine subspecialists (interventional pain, wound-care surgeons, Mohs surgeons) legitimately sit at the top of the high-code share distribution, and office-based procedures correctly have no facility claim. Damp by narrow specialty peer groups, by weighting the corroboration-absence component more than raw share, and by excluding providers whose device/implant purchase records support the billed code.

---

## Appendix A — Mechanics found in the corpus

Deterministic keyword probes over all 679 `SchemeSummary` values. These are **lower bounds**: the summaries are compressed prose, so a mechanic present in a case is not always phrased in a way a regex catches.

| Mechanic | Cases | % | Top service groups |
|---|---:|---:|---|
| `medically_unnecessary` | 127 | 18.7 | DME (41), PhysicianPractice (38), Laboratory (37), Pharmacy (24) |
| `not_delivered` | 110 | 16.2 | BehavioralHealth (28), Pharmacy (19), Laboratory (16), PhysicianPractice (16) |
| `telemarketing_leads` | 55 | 8.1 | DME (32), Telehealth (28), GeneticTesting (17), Laboratory (15) |
| `telehealth_signoff` | 55 | 8.1 | Telehealth (49), DME (26), Laboratory (21), GeneticTesting (21) |
| `covid_addon` | 50 | 7.4 | Laboratory (33), PhysicianPractice (9), DME (8), GeneticTesting (7) |
| `nominee_shell` | 40 | 5.9 | DME (15), Laboratory (10), Hospice (8), Telehealth (7) |
| `genetic_cancer_screen` | 32 | 4.7 | GeneticTesting (32), Telehealth (21), Laboratory (20), DME (14) |
| `deceased_or_inpatient` | 25 | 3.7 | Laboratory (9), BehavioralHealth (7), DME (4), PhysicianPractice (4) |
| `sham_consulting` | 24 | 3.5 | Laboratory (15), GeneticTesting (7), Telehealth (6), BehavioralHealth (4) |
| `excluded_or_unlicensed` | 22 | 3.2 | BehavioralHealth (11), Pharmacy (4), Telehealth (4), DME (3) |
| `no_records` | 17 | 2.5 | DME (8), PhysicianPractice (8), Telehealth (5), BehavioralHealth (4) |
| `urine_drug_testing` | 16 | 2.4 | Laboratory (16), PhysicianPractice (7), SubstanceUseTreatment (4), BehavioralHealth (3) |
| `identity_misuse` | 11 | 1.6 | Pharmacy (4), Hospice (3), DME (2), HomeHealth (2) |
| `compound_or_expensive_rx` | 11 | 1.6 | Pharmacy (10), PhysicianPractice (2), Telehealth (1), DME (1) |
| `impossible_volume` | 10 | 1.5 | BehavioralHealth (5), Laboratory (2), HomeHealth (2), SubstanceUseTreatment (1) |
| `unqualified_staff` | 9 | 1.3 | BehavioralHealth (3), HomeHealth (2), DME (1), Telehealth (1) |
| `upcode_level` | 7 | 1.0 | PhysicianPractice (4), BehavioralHealth (2), Laboratory (2), Telehealth (2) |
| `beneficiary_bribes` | 5 | 0.7 | Laboratory (3), SubstanceUseTreatment (2), GeneticTesting (1), BehavioralHealth (1) |
| `rapid_enrollment_spike` | 1 | 0.1 | DME (1), Pharmacy (1), SubstanceUseTreatment (1), Laboratory (1) |
| `proof_of_delivery` | 1 | 0.1 | Pharmacy (1) |

## Appendix B — Corpus composition

| Service group | Cases |
|---|---:|
| PhysicianPractice | 118 |
| Pharmacy | 108 |
| DME | 95 |
| Laboratory | 93 |
| BehavioralHealth | 65 |
| Telehealth | 58 |
| Other | 54 |
| GeneticTesting | 39 |
| Hospital | 33 |
| HomeHealth | 30 |
| NursingHome | 27 |
| SubstanceUseTreatment | 26 |
| Hospice | 20 |
| Device, DME | 14 |
| PersonalCare | 14 |

| Fraud type | Cases |
|---|---:|
| Falsify certificate | 263 |
| Phantom Claims | 226 |
| kickback_Bribery For Referral | 209 |
| FakeEncounter | 200 |
| Wire Fraud | 182 |
| Drug_Prescriptions | 157 |
| IdentityFraud | 123 |
| Benefit & Eligibility Fraud | 112 |
| Device, DME | 108 |
| Upcoding | 79 |
| Covid or General Loan Fraud | 75 |
| Tax, Payroll or Coupon Fraud | 56 |
| Other - Unknown | 51 |
| Unbundling | 21 |
| Retention of Overpayment | 12 |
| Other - FDA Submission Fraud | 10 |
| Other - Embezzlement of federal grant funds | 8 |

## Appendix C — Limitations

These are prosecution press releases: they describe scheme mechanics vividly (who signed what, what was never delivered, how ownership was hidden) but contain almost no claims-level detail — no code frequencies, no baseline rates, no denominators. Nothing here supports a specific numeric threshold, so every feature above states a comparison against a calibrated peer or control distribution rather than an invented cut-point. The corpus over-represents Medicare fee-for-service and large-dollar criminal matters and under-represents Medicare Advantage risk-adjustment, commercial network and pricing abuse, prior-authorisation gaming, and small-dollar attrition fraud; it also gives little insight into detection lag, so features relying on death files, wholesaler purchase feeds or live-discharge outcomes can only run retrospectively. Enrolment, ownership and exclusion facts appear repeatedly in the prose but the corpus never shows what the corresponding enrolment records looked like, so the credentialing feature is designed from described conduct rather than observed data.

Additionally:

- **No thresholds are supplied.** The corpus describes what schemes look like, not how often benign providers look similar. Every threshold above is a starting point to calibrate against a control population.
- **Selection bias runs one way.** Every case here was detected and prosecuted, so these are features for schemes that *got caught* — they may over-represent clumsy mechanics and under-represent successful fraud.
- **Case counts are evidence of a mechanic recurring, not of its prevalence** in the provider population.
