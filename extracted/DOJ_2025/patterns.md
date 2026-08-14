# Medical Fraud Cases - Extracted Features and Patterns

*Generated 2026-08-13T21:42:59-04:00 with `claude-opus-5`*

- Documents processed: **679** (extracted 679, failed 0)
- Distinct cases: **590** - 83 case(s) are covered by more than one document (charge, plea and sentencing are announced separately), so per-document counts overstate case counts
- Fraud amounts stated in **379** cases, totalling **$47,401,013,741** (median $4,592,650, range $4,750 - $14,600,000,000)
- Settlements/judgments stated in **373** cases, totalling **$12,617,735,942**
- Custodial sentences imposed in **196** cases (median 42 months, range 1-708)

## Cases

| Document | Date | Entity | Payer | Fraud $ | Settlement $ | Jail (mo) | Type |
|---|---|---|---|---|---|---|---|
| labcorp-and-university-health-system-agree-t | 2025-01-02 | Laboratory Corporation of America Holdings; Laborato | Medicare | - | $388,667 | - | Other - Unknown |
| new-haven-psychiatrist-to-pay-more-than-450k | 2025-01-02 | Naimetulla Ahmed Syed, M.D. (psychiatrist, sole prac | Medicare; Medicaid (Connecti | - | $575,439 | - | Drug_Prescriptions |
| u-s-attorney-ryan-k-buchanan-announces-upcom | 2025-01-02 | Charles Adams, M.D. (physician); Adams' medical prac | Medicare | $1,100,000 | $27,000,000 | - | FakeEncounter |
| u-s-attorneys-offices-collection-and-enforce | 2025-01-02 | - | - | - | $20,078,264 | - | Other - Unknown |
| usao-collects-nearly-28m-in-civil-and-crimin | 2025-01-02 | Matthew Maluchnik | - | - | $941,069 | - | Other - Unknown |
| virginia-beach-doctor-agrees-to-625-000-fals | 2025-01-02 | Dr. Scott Saffold (physician); Chesapeake Bay, ENT,  | Medicare; Virginia Medicaid; | - | $625,000 | - | FakeEncounter |
| defense-contractor-agrees-to-pay-628-000-to- | 2025-01-03 | Live Wire, LLC (Vermont-based defense contractor) | U.S. Army | - | $628,328 | - | Other - Unknown |
| operations-manager-pleads-guilty-to-kickback | 2025-01-03 | Timothy Doyle (operations manager) | Medicare | $70,600,000 | - | - | kickback_Bribery For Referral |
| physicians-toxicology-laboratory-and-its-own | 2025-01-03 | Physicians Toxicology Laboratory, LLC (laboratory);  | Medicare | - | $4,613,633 | - | FakeEncounter |
| rebecca-c-lutzko-announces-resignation-from- | 2025-01-03 | Ankita Singh, M.D. (physician who signed brace order | Medicare; Medicaid (Ohio); N | $8,000,000 | - | 42 | Falsify certificate |
| telehealth-company-pays-386-000-to-resolve-a | 2025-01-03 | CompreCare Health LLC and its affiliates, d/b/a Medi | Medicare | - | $358,514 | - | Upcoding |
| athira-pharma-inc-agrees-to-pay-4m-to-settle | 2025-01-06 | Athira Pharma Inc.; Leen Kawas (former CEO) | National Institutes of Healt | - | $4,068,698 | - | Other - Embezzlement of federa |
| bothell-biopharmaceutical-company-pays-4-mil | 2025-01-06 | Athira Pharma, Inc. (Bothell, WA biopharmaceutical c | National Institutes of Healt | - | $4,068,698 | - | Falsify certificate |
| u-s-attorney-vanessa-roberts-avery-announces | 2025-01-06 | - | - | - | - | - | Other - Unknown |
| united-states-attorney-nikolas-kerest-submit | 2025-01-06 | - | - | - | - | - | Other - Unknown |
| connecticut-dentist-pays-more-than-600k-to-s | 2025-01-07 | Lakshmi Bethi, DMD (dentist/owner); New Haven Dental | Medicaid (Connecticut Medica | $2,200,000 | $1,108,296 | - | kickback_Bribery For Referral |
| marketers-and-healthcare-providers-in-texas- | 2025-01-07 | Shahram Naghshbandi (laboratory marketer); John Bell | Medicare | - | $1,137,914 | - | kickback_Bribery For Referral |
| owner-of-addiction-treatment-chain-that-bill | 2025-01-07 | Michael Brier (owner); Recovery Connections Centers  | Medicare; Medicaid; other pr | - | $4,515,100 | 98 | Upcoding |
| pharmacy-owner-sentenced-to-imprisonment-for | 2025-01-07 | Randy Yost (owner of Randy's Gateway Drug) | Medicare; Medicaid (Virginia | $1,309,515 | $1,309,515 | 18 | Drug_Prescriptions |
| boerne-ceo-sentenced-to-three-years-in-feder | 2025-01-08 | Belinda Jo Juarez (majority owner and CEO of Superio | - | - | $4,304,837 | 36 | Tax, Payroll or Coupon Fraud |
| california-man-admits-role-in-10-million-hea | 2025-01-08 | Adam Wayne Owens (owner of marketing companies) | Medicare | $10,000,000 | - | - | kickback_Bribery For Referral |
| chesapeake-hospital-indicted-for-healthcare- | 2025-01-08 | Chesapeake Regional Medical Center (hospital, former | Medicare; Medicaid (Virginia | $18,500,000 | - | 708 | FakeEncounter |
| former-virginia-business-owner-pleads-guilty | 2025-01-08 | Richard E. Moore (executive vice president and part  | IRS | $3,100,000 | - | - | Tax, Payroll or Coupon Fraud |
| united-states-attorney-brandon-b-brown-annou | 2025-01-08 | Lafayette Physical Rehabilitation Hospital; Acadiana | Medicare | - | $1,775,000 | - | FakeEncounter |
| former-senior-partner-at-mckinsey-amp-compan | 2025-01-10 | Martin Elling (former senior partner, McKinsey & Com | - | - | $650,000,000 | - | Other - Unknown |
| u-s-attorney-damien-m-diggs-announces-depart | 2025-01-10 | Walgreens (retail pharmacy chain) | Medicare; Medicaid | - | $97,000,000 | - | Phantom Claims |
| army-veteran-sentenced-to-federal-prison-for | 2025-01-13 | Kevin Paul McMains (Army veteran, benefits claimant) | Medicare; Department of Vete | $779,000 | $779,680 | 33 | Benefit & Eligibility Fraud |
| edinburg-doctor-and-son-guilty-in-kickback-c | 2025-01-13 | Dr. Tajul Shams Chowdhury (physician, owner of Cente | - | $6,600,000 | - | - | kickback_Bribery For Referral |
| radiopharmaceutical-company-set-to-pay-350-0 | 2025-01-13 | PharmaLogic Holdings Corporation (radiopharmaceutica | - | - | $350,000 | - | Benefit & Eligibility Fraud |
| slidell-chiropractor-convicted-of-health-car | 2025-01-13 | Dennis Michael Peyroux (chiropractor, clinic owner) | Medicare | $3,300,000 | $4,200,000 | - | Phantom Claims |
| the-united-states-and-state-of-north-carolin | 2025-01-13 | Benson I. Ejindu (operator of durable medical equipm | Medicaid (North Carolina Med | - | - | - | Upcoding |
| new-jersey-pharmacy-agrees-to-resolve-false- | 2025-01-14 | Medsinbox Pharmacy LTC LLC, d/b/a Farmacia San Anton | Medicare Part D; New Jersey  | - | $625,000 | - | Phantom Claims |
| pharmacy-agrees-to-resolve-false-claims-act- | 2025-01-14 | Medsinbox Pharmacy LTC LLC d/b/a Farmacia San Antoni | Medicare Part D; Medicaid (N | - | $625,000 | - | Phantom Claims |
| u-s-attorneys-office-and-former-los-alamos-n | 2025-01-14 | William Monford Wood (former Los Alamos National Lab | - | - | $67,500 | - | Tax, Payroll or Coupon Fraud |
| doctor-sentenced-for-70m-medicare-fraud-sche | 2025-01-15 | David M. Young M.D. (physician) | Medicare | $70,000,000 | $26,622,522 | 120 | Falsify certificate |
| false-claims-act-settlements-and-judgments-e | 2025-01-15 | Teva Pharmaceuticals USA Inc.; Raytheon Company; End | Medicare; Medicaid; TRICARE | - | $2,900,000,000 | 42 | kickback_Bribery For Referral |
| texas-hospital-ceo-sentenced-to-federal-pris | 2025-01-15 | Jeffrey Paul Madison (hospital CEO, Little River Hea | Medicare; Medicaid; other fe | - | $5,443,630 | 36 | kickback_Bribery For Referral |
| doctor-jailed-for-hipaa-violations_0a6158a18 | 2025-01-16 | Gabriel Alejandro Hernandez-Roman (emergency room re | - | - | $1,000 | 1 | IdentityFraud |
| owner-of-three-north-shore-restaurants-sente | 2025-01-16 | John Drivas (owner and operator of Red's Sandwich Sh | - | $2,036,116 | $2,056,116 | 12 | Tax, Payroll or Coupon Fraud |
| two-iowa-healthcare-practitioners-settle-all | 2025-01-16 | Cori Lempiainen (nurse practitioner); Paul Baumert,  | Medicare | - | $164,325 | - | Phantom Claims |
| vicksburg-man-sentenced-to-32-years-in-feder | 2025-01-16 | Laron Evans (organizer, purported owner/manager of f | Third-party Health Savings A | - | $2,219,330 | 384 | IdentityFraud |
| bioreference-health-and-opko-health-agree-to | 2025-01-17 | BioReference Health LLC, formerly BioReference Labor | Federal health care programs | - | $704,349 | - | Upcoding |
| former-nurse-practitioner-in-butte-sentenced | 2025-01-17 | Tristan Ashley Svejkovsky (nurse practitioner) | Blue Cross Blue Shield of Mo | $62,310,000 | $613,108 | 60 | Phantom Claims |
| health-care-plan-agrees-to-pay-over-500-000- | 2025-01-17 | Commonwealth Care Alliance, Inc. (acquirer/successor | Medicare | - | $520,355 | - | kickback_Bribery For Referral |
| justice-department-files-nationwide-lawsuit- | 2025-01-17 | Walgreens Boots Alliance Inc.; Walgreen Co. and vari | Medicare; Medicaid; other fe | - | - | - | Drug_Prescriptions |
| pharmacist-guilty-in-110-million-dollar-kick | 2025-01-17 | John Ageudo Rodriguez (licensed pharmacist, owner of | Federal health care benefit  | $110,000,000 | - | - | kickback_Bribery For Referral |
| south-bay-based-nursing-facilities-chain-and | 2025-01-17 | Unified Care Services LLC (skilled nursing facilitie | Small Business Administratio | - | $18,000,000 | - | Covid or General Loan Fraud |
| two-charged-with-defrauding-connecticuts-med | 2025-01-17 | Ramon Apellaniz (a/k/a "Kristopher Rockefeller," de  | Medicaid (Connecticut Medica | $1,800,000 | - | - | Phantom Claims |
| unified-care-services-llc-agrees-to-pay-18m- | 2025-01-17 | Unified Care Services LLC (skilled nursing facility  | Small Business Administratio | - | $18,000,000 | - | Covid or General Loan Fraud |
| middlesex-county-man-admits-defrauding-south | 2025-01-21 | Mohammed Rahman (controlled Caltech Trading Corporat | - | $1,000,000 | - | - | Wire Fraud |
| military-contractor-to-pay-1-2-million-to-un | 2025-01-21 | Neuro Stat Analytical Solutions, LLC (Neurostat) (Te | United States Air Force / De | - | $1,200,000 | - | kickback_Bribery For Referral |
| united-states-attorney-039-s-office-collecte | 2025-01-21 | - | Medicare; Medicaid (TennCare | - | $137,054,515 | - | Other - Unknown |
| amtrak-employee-admits-participating-in-11-m | 2025-01-23 | Rodolfo Rivera (Amtrak employee); Kevin Frink (Amtra | Amtrak employee health care  | $11,000,000 | - | 34 | kickback_Bribery For Referral |
| anesthesiology-service-provider-pays-almost- | 2025-01-23 | Northwest Anesthesiology and Pain Services (NWAP) (a | Medicare | $1,800,000 | $999,999 | - | kickback_Bribery For Referral |
| broward-county-man-sentenced-to-prison-for-f | 2025-01-23 | Willie F. Murray, Jr. (registered agent and manager  | Health Resources and Service | $5,671,611 | $7,250,537 | 61 | Phantom Claims |
| c-r-bard-inc-and-affiliates-pay-17-million-t | 2025-01-23 | C.R. Bard, Inc.; Liberator Medical Supply, Inc.; Lib | Medicare; Medicaid; TRICARE | - | $17,000,000 | - | kickback_Bribery For Referral |
| former-mercer-county-pharmacist-found-guilty | 2025-01-23 | Florence Ndubizu (co-owner and pharmacist-in-charge, | - | - | - | - | Drug_Prescriptions |
| operator-of-home-health-care-company-sentenc | 2025-01-23 | Faith Newton (operator of Arbor Homecare Services LL | Medicaid (MassHealth) | $100,000,000 | $99,984,517 | 144 | Phantom Claims |
| pain-management-doctor-and-medical-practice- | 2025-01-23 | Dr. Kamal Kabakibou (pain-management physician); Kam | Medicare; TRICARE; U.S. Depa | - | $3,500,000 | - | FakeEncounter |
| corporation-and-former-chief-executive-offic | 2025-01-24 | KBWB Operations LLC, d/b/a Atrium Health and Senior  | Medicare; Medicaid (Wisconsi | - | - | - | Other - Unknown |
| former-ceo-of-startup-software-company-sente | 2025-01-24 | Andrew Park (co-founder and CEO of a startup technol | IRS | $14,000,000 | $654,821 | 30 | Tax, Payroll or Coupon Fraud |
| former-ceo-of-startup-software-company-sente | 2025-01-24 | Andrew Park (co-founder and CEO of a startup technol | - | $14,700,000 | $654,821 | 30 | Tax, Payroll or Coupon Fraud |
| madison-man-sentenced-to-37-months-in-prison | 2025-01-24 | Reginald Fullwood, Jr. (owner of Jackson Medical Sup | Medicare; Medicare Advantage | $12,441,625 | - | 37 | kickback_Bribery For Referral |
| pfizer-agrees-to-pay-nearly-60-million-to-re | 2025-01-24 | Pfizer Inc. (parent/acquirer); Biohaven Pharmaceutic | Medicare; Medicaid (state Me | - | $59,746,277 | - | kickback_Bribery For Referral |
| pfizer-agrees-to-pay-nearly-60m-to-resolve-f | 2025-01-24 | Pfizer Inc. (parent/acquirer); Biohaven Pharmaceutic | Medicare; Medicaid (state Me | - | $59,746,277 | - | kickback_Bribery For Referral |
| greenfield-man-sentenced-to-15-months-impris | 2025-01-27 | Mohammed Kazim Ali (co-owner, Noah Associates); Just | Medicare; Medicaid | $2,200,000 | $2,275,000 | 15 | kickback_Bribery For Referral |
| philadelphia-mental-health-clinic-and-its-ps | 2025-01-27 | Ghodrat Pirooz Sholevar, M.D. (psychiatrist owner);  | Medicaid (Community Behavior | - | $900,000 | - | Falsify certificate |
| greensboro-laboratory-and-owner-agree-to-pay | 2025-01-28 | Substance Abuse Treatment Labs; Paul Fribush (owner) | Medicaid (North Carolina Med | - | $850,000 | - | FakeEncounter |
| u-s-attorneys-office-recovers-more-than-55-m | 2025-01-28 | Medisca, Inc.; Booz Allen Hamilton; Elara Caring and | Department of Veterans Affai | - | $55,969,678 | - | Drug_Prescriptions |
| woman-sentenced-for-fraud-scheme-involving-c | 2025-01-28 | Lourdes Navarro (co-owner of Matias Clinical Laborat | Medicare; HRSA COVID-19 Unin | $369,000,000 | $61,253,885 | 120 | FakeEncounter |
| waterford-woman-sentenced-to-2-years-in-pris | 2025-01-29 | Michele Devine (executive director of Southeastern R | - | $397,064 | $399,064 | 24 | Other - Embezzlement of federa |
| u-s-attorneys-office-collects-17-444-425-in- | 2025-01-30 | Penn State Health (multi-hospital health system) | Medicare | - | $11,712,336 | - | Phantom Claims |
| arizona-couple-pleads-guilty-to-1-2b-health- | 2025-01-31 | Alexandra Gehrke (owner of Apex Medical LLC and Viki | Medicare; TRICARE; CHAMPVA;  | $1,212,005,778 | $1,220,680,530 | - | kickback_Bribery For Referral |
| livecare-inc-agrees-to-pay-up-to-4-9-million | 2025-01-31 | LiveCare Inc. (remote patient monitoring provider) | Medicare | - | $4,900,000 | - | kickback_Bribery For Referral |
| u-s-attorneys-office-collects-more-than-4m-i | 2025-01-31 | Keven Ellis Partin | TRICARE; Medicare; Departmen | - | $338,805 | - | kickback_Bribery For Referral |
| u-s-attorneys-office-collects-over-39-millio | 2025-01-31 | Guidehouse, Inc. (federal contractor); Nan McKay and | - | - | $39,262,324 | 72 | Other - Unknown |
| hartford-substance-abuse-counselor-sentenced | 2025-02-03 | Thelma "Wendy" Epps (Licensed Alcohol and Drug Abuse | Medicaid (Connecticut Medica | $1,001,508 | $1,001,058 | 27 | Benefit & Eligibility Fraud |
| man-pleads-guilty-in-connection-with-17m-med | 2025-02-03 | Petros Fichidzhyan (operator of sham hospice compani | Medicare | $17,000,000 | - | - | Phantom Claims |
| new-york-man-arrested-in-dallas-airport-on-h | 2025-02-03 | Robert Lake (licensed prosthetist and orthotist, own | Medicare | $17,000,000 | - | - | Device, DME |
| serial-fraudster-sentenced-to-ten-years-in-f | 2025-02-03 | James Henley (organizer; claimed CEO of five fake bu | - | $2,927,758 | $1,887,426 | 120 | IdentityFraud |
| tampa-man-agrees-to-pay-u-s-government-2-mil | 2025-02-03 | Mihir Taneja; Larry Smith (owner of Z Stat Medical,  | TRICARE | - | $21,600,000 | - | kickback_Bribery For Referral |
| man-pleads-guilty-to-conspiracy-to-launder-m | 2025-02-04 | Chaudhry Shabbir Ahmed (nominee owner of Dune Medica | Medicare | $100,000,000 | $17,600,000 | - | Device, DME |
| pharmacy-llc-agrees-to-resolve-false-claims- | 2025-02-04 | A Plus Pharmacy LLC (former owner of A Plus Pharmacy | Medicare (Part D) | - | $350,000 | - | Phantom Claims |
| u-s-attorneys-office-collects-more-than-26-m | 2025-02-05 | Unnamed network of healthcare companies (telehealth  | Medicare; Connecticut Medica | - | $5,500,000 | - | kickback_Bribery For Referral |
| former-government-employee-and-wife-plead-gu | 2025-02-06 | Rafael Castro (VA benefits recipient, former Veteran | Department of Veterans Affai | $130,000 | - | - | Benefit & Eligibility Fraud |
| four-pharmacists-sentenced-for-roles-in-13m- | 2025-02-06 | Raef Hamaed (pharmacist/pharmacy owner); Tarek Fakhu | Medicare; Medicaid; Blue Cro | $13,000,000 | - | 120 | Phantom Claims |
| louisiana-doctor-sentenced-for-illegally-dis | 2025-02-06 | Adrian Dexter Talbot M.D. (owner/operator of Medex C | Medicare; Medicaid (Louisian | $5,400,000 | - | 87 | Drug_Prescriptions |
| u-s-attorneys-office-collects-more-than-17-m | 2025-02-07 | Edward William Salko, D.O. (physician); Jackson & Co | Medicare | - | $924,620 | - | kickback_Bribery For Referral |
| humboldt-county-woman-charged-with-embezzlin | 2025-02-10 | Christina Ann Mobley, also known as Kris Mobley (bus | - | $500,000 | - | - | Wire Fraud |
| amtrak-employee-admits-participating-in-11-m | 2025-02-11 | Anthony Saloka (Amtrak employee/insurance beneficiar | Amtrak health care plan | $11,000,000 | - | 34 | kickback_Bribery For Referral |
| california-company-pleads-guilty-to-conspiri | 2025-02-11 | Advoque Safeguard LLC (mask manufacturer); Jason Aze | - | - | - | - | Device, DME |
| doctor-convicted-of-24m-medicare-fraud-schem | 2025-02-11 | Alexander Baldonado, M.D. (physician) | Medicare; Medicaid | $24,000,000 | - | - | kickback_Bribery For Referral |
| farmington-woman-pleads-guilty-to-health-car | 2025-02-11 | Helen Zervas (optometrist, owner of Family Eye Care) | Medicare; Connecticut Medica | - | - | - | Phantom Claims |
| missouri-man-sentenced-to-108-months-in-pris | 2025-02-11 | Christopher Lee Carroll (co-owner, Square One Group  | - | $3,000,000 | $3,000,000 | 108 | Covid or General Loan Fraud |
| phobos-ransomware-affiliates-arrested-in-coo | 2025-02-11 | Roman Berezhnoy (operator of ransomware affiliate gr | - | $16,000,000 | - | - | Wire Fraud |
| two-arizona-department-of-economic-security- | 2025-02-11 | Jacqueline Espino (Arizona Department of Economic Se | Arizona Department of Econom | $3,735,454 | $2,994,484 | 30 | Benefit & Eligibility Fraud |
| aiken-man-pleads-guilty-to-conspiracy-to-com | 2025-02-12 | Cody Lee Anderson (designated personal representativ | - | $20,000,000 | - | - | Wire Fraud |
| two-pharmacists-convicted-for-illegal-distri | 2025-02-12 | Yousef Ennab (licensed pharmacist, supervising pharm | Private insurance companies  | $36,000,000 | - | 216 | Drug_Prescriptions |
| u-s-attorneys-office-collects-more-than-1-5- | 2025-02-12 | Dr. Frank Li (physician, medical office owner) | - | - | $2,850,000 | - | Other - Unknown |
| united-states-attorney-dena-j-king-announces | 2025-02-12 | - | Medicare; Medicaid | - | - | - | Other - Unknown |
| philadelphia-man-sentenced-to-39-months-impr | 2025-02-13 | Aboudramane Karamoko; Sekou Fofanah; Shamaire Brown; | - | $1,600,157 | $1,600,157 | 39 | Other - Unknown |
| u-s-attorney-039-s-office-collects-more-than | 2025-02-13 | Raytheon Company; Teva Pharmaceuticals; Kabbage, Inc | - | - | $60,170,000 | - | kickback_Bribery For Referral |
| u-s-attorneys-office-collects-23-5-million-i | 2025-02-13 | Total Access Urgent Care (TAUC); Dr. Nehal Modh (Fes | - | - | $10,300,000 | - | Phantom Claims |
| saint-vincents-catholic-medical-centers-of-n | 2025-02-14 | SVCMC Inc., formerly known as Saint Vincents Catholi | TRICARE (Defense Health Agen | - | $29,000,000 | - | Retention of Overpayment |
| suburban-chicago-medical-device-company-to-p | 2025-02-14 | Advanced Inventory Management, Inc. (medical device  | - | $500,000 | $1,000,000 | - | Device, DME |
| former-western-new-york-man-pleads-guilty-to | 2025-02-18 | Michael W. Luehrsen | - | - | $4,000,000 | - | Drug_Prescriptions |
| health-net-federal-services-llc-and-centene- | 2025-02-18 | Health Net Federal Services, LLC (TRICARE managed ca | TRICARE (Defense Health Agen | - | $11,253,400 | - | Falsify certificate |
| u-s-attorney-039-s-office-collects-nearly-3- | 2025-02-18 | Dunes Surgical Hospital; two unnamed physician group | - | - | $12,700,000 | - | kickback_Bribery For Referral |
| u-s-attorney-039-s-office-for-the-western-di | 2025-02-18 | - | - | - | $104,800,000 | - | Other - Unknown |
| president-of-insurance-brokerage-firm-and-ce | 2025-02-19 | Cory Lloyd (president of insurance brokerage firm);  | Federal government (Affordab | $161,900,000 | - | - | Benefit & Eligibility Fraud |
| sacramento-county-man-sentenced-to-33-months | 2025-02-19 | Michael Andrew Scott (owner/operator of Trusted Medi | - | $470,000 | $376,044 | 33 | Wire Fraud |
| st-louis-area-doctor-sentenced-ordered-to-re | 2025-02-19 | Dr. Sonny Saggar (doctor, operator of St. Louis Gene | Medicare; Medicaid (Missouri | $742,528 | $742,528 | 35 | Falsify certificate |
| wny-medical-agrees-to-pay-250-000-to-resolve | 2025-02-19 | Western New York Medical P.C. (WNY Medical) (health  | Medicare | - | $251,477 | - | Phantom Claims |
| columbia-physician-pleads-guilty-to-false-st | 2025-02-20 | Jerry Joseph Bruggeman, M.D. (physician) | Medicare | $1,606,408 | - | - | Falsify certificate |
| lackawanna-man-pleads-guilty-to-defrauding-m | 2025-02-20 | Munef Fadhel (owner, Great Lake Transportation, Inc. | Medicaid (New York) | $95,000 | - | - | Upcoding |
| law-enforcement-seizes-range-rover-and-over- | 2025-02-20 | Magaly Travieso (advanced practitioner registered nu | Medicare; Medicare Advantage | $20,000,000 | - | - | Phantom Claims |
| owner-of-durable-medical-equipment-companies | 2025-02-20 | Raju Sharma (owner of Pharmagears, LLC and RR Medco, | Medicare | $29,600,000 | - | - | Device, DME |
| vice-president-of-health-care-software-and-s | 2025-02-20 | Gregory Schreck (vice president of the company that  | Medicare; other federal heal | $1,000,000,000 | - | - | kickback_Bribery For Referral |
| howey-in-the-hills-resident-pleads-guilty-to | 2025-02-21 | Dorian Farmer (owner of several businesses, includin | - | $806,653 | - | - | Tax, Payroll or Coupon Fraud |
| man-pleads-guilty-to-illegally-importing-sui | 2025-02-21 | Daniel Gonzalez-Munguia, aka "Alejandro Vasquez" (op | - | - | - | - | Drug_Prescriptions |
| ohio-doctor-agrees-to-pay-600-000-to-settle- | 2025-02-21 | Ronald F. Ambrosia (physician) | Medicare | - | $600,000 | - | Upcoding |
| saad-healthcare-agrees-to-pay-3m-to-settle-f | 2025-02-21 | Saad Enterprises Inc., d/b/a Saad Healthcare (hospic | Medicare | - | $3,000,000 | - | Benefit & Eligibility Fraud |
| eureka-chiropractor-convicted-of-defrauding- | 2025-02-24 | Carrie Musselman (chiropractor) | Medicare; other insurance co | $1,500,000 | $2,300,000 | 20 | Upcoding |
| north-haven-counselor-sentenced-to-more-than | 2025-02-24 | Rachel Collins (licensed professional counselor and  | Medicaid (Connecticut Medica | $1,647,032 | $1,761,117 | 37 | Phantom Claims |
| webster-woman-charged-with-defrauding-medica | 2025-02-24 | Ashley Jackson (sole owner of Roc City Transport); R | Medicaid | $40,123 | - | - | Phantom Claims |
| chester-business-owner-sentenced-to-two-year | 2025-02-25 | David Neel (sole owner and operator of Siesta Health | - | $460,543 | - | 24 | Tax, Payroll or Coupon Fraud |
| danville-woman-pleads-guilty-to-health-care- | 2025-02-25 | Jacquelyn Farrish (Medicaid Consumer Directed Care P | Medicaid (Virginia Medicaid) | $116,536 | - | - | Phantom Claims |
| lab-operator-convicted-of-4m-medicare-fraud- | 2025-02-25 | Sherif Khalil (owner/operator of Spectra Clinical La | Medicare | $4,000,000 | - | - | kickback_Bribery For Referral |
| national-sales-director-for-new-york-based-m | 2025-02-25 | David Fuhrmann (national sales director of mobile me | Medicare | $70,600,000 | - | - | kickback_Bribery For Referral |
| united-states-sues-skilled-nursing-company-e | 2025-02-25 | RegalCare Management Group, LLC; RegalCare Managemen | Medicare; Medicaid (MassHeal | - | - | - | Upcoding |
| 8-charged-in-north-charleston-public-corrupt | 2025-02-26 | Jerome Sydney Heyward (North Charleston City Council | - | - | - | - | kickback_Bribery For Referral |
| former-executive-director-is-sentenced-for-s | 2025-02-26 | Stephanie L. Roberts (executive director of Cancer S | - | $136,000 | $220,334 | 18 | Tax, Payroll or Coupon Fraud |
| morgantown-physician-sentenced-for-tax-fraud | 2025-02-26 | David M. Anderson (physician) | - | $143,599 | - | 6 | Tax, Payroll or Coupon Fraud |
| shelbyville-woman-pleads-guilty-to-employmen | 2025-02-26 | Rebekah Proctor (operator of Franklin Springs Academ | - | - | $1,117,032 | - | Tax, Payroll or Coupon Fraud |
| u-s-attorneys-office-collects-over-20-millio | 2025-02-26 | Shephard Spruill | Medicaid | - | $800,000 | - | IdentityFraud |
| woman-previously-convicted-of-fraud-and-iden | 2025-02-26 | Jessica Stuart (unlicensed provider impersonating a  | Medicaid (Connecticut) | $369,439 | - | 27 | IdentityFraud |
| community-health-care-solutions-llc-and-the- | 2025-02-27 | Community Health Care Solutions, LLC (Shreveport cou | Medicaid (Louisiana Medicaid | - | $4,600,000 | - | Phantom Claims |
| gastonia-pharmacy-to-pay-204-000-to-resolve- | 2025-02-27 | Prescriptions Plus (pharmacy, Gastonia, N.C.) | - | - | $204,000 | - | Drug_Prescriptions |
| acting-united-states-attorney-fondren-announ | 2025-02-28 | Sanjeev Kumar (gynecologist) | Medicare; Medicaid | - | - | - | FakeEncounter |
| former-state-official-and-state-representati | 2025-02-28 | Konstantinos "Kosta" Diamantis (Deputy Secretary, Co | Medicaid (Connecticut Depart | - | $599,810 | - | kickback_Bribery For Referral |
| owner-of-oahu-physical-therapy-clinic-senten | 2025-02-28 | Stephen Timothy Wells (owner of Oahu Spine and Rehab | TRICARE; Medicare | - | $392,157 | 9 | FakeEncounter |
| skilled-nursing-facility-and-acute-care-hosp | 2025-02-28 | Providence Park, Inc., d/b/a Ascension Living Provid | Medicare; Medicaid (Texas) | - | $6,526,851 | - | Upcoding |
| two-brothers-from-india-arraigned-on-indictm | 2025-02-28 | Avanish Kumar Jha; Rajnish Kumar Jha; Dhrishti Pharm | - | - | - | - | Drug_Prescriptions |
| attorney-general-pamela-bondi-appoints-micha | 2025-03-03 | - | - | - | - | - | Other - Unknown |
| former-d-c-public-official-sentenced-to-15-m | 2025-03-03 | Wendy Nicole Villatoro (former D.C. Homeland Securit | Small Business Administratio | $5,500,000 | $844,415 | 15 | Covid or General Loan Fraud |
| harrisburg-woman-sentenced-to-41-months-in-p | 2025-03-03 | Ester N. Mbaya (president of Cool Waters, LLC, home  | Medicaid (Pennsylvania) | $3,000,000 | $3,349,550 | 41 | Phantom Claims |
| lisa-g-johnston-named-acting-united-states-a | 2025-03-03 | - | - | - | - | - | Other - Unknown |
| orlando-woman-ordered-to-pay-over-3-million- | 2025-03-03 | Marielys Feliciano Rodriguez (owner of shell constru | - | $3,338,558 | $3,686,318 | - | Tax, Payroll or Coupon Fraud |
| middle-district-of-florida-u-s-attorneys-off | 2025-03-04 | Walgreens Boots Alliance (pharmacy chain); Dr. Edwar | Medicare; Medicaid; other fe | - | $174,896,693 | - | Phantom Claims |
| addiction-treatment-center-supervisor-senten | 2025-03-05 | Mi Ok Song Bruining (clinical social worker and supe | Medicare; Medicaid; other pr | $3,500,000 | $100,000 | - | Upcoding |
| buffalo-business-owner-sentenced-for-medicai | 2025-03-05 | Arkan Fadhel (owner, Queen City Transportation, Inc. | Medicaid (New York) | $250,000 | $1,031,187 | - | Phantom Claims |
| thibodaux-social-worker-sentenced-to-30-mont | 2025-03-05 | John Christopher Barrilleaux (social worker) | Private insurance companies  | - | $4,592,650 | 30 | Phantom Claims |
| health-care-providers-and-laboratory-markete | 2025-03-06 | Gerald Congdon, M.D.; Coastal Urgent Care LLC; Coast | Medicare; TRICARE | - | $1,913,808 | - | kickback_Bribery For Referral |
| healthcare-providers-and-laboratory-marketer | 2025-03-06 | Gerald Congdon, M.D.; Coastal Urgent Care, LLC; Coas | Medicare; TRICARE | - | $1,913,808 | - | kickback_Bribery For Referral |
| lake-charles-physician-wife-and-clinic-agree | 2025-03-06 | Dr. Henry Goolsby (physician); Patricia Lenae Goolsb | Medicare | - | $450,000 | - | Upcoding |
| medical-billing-company-owner-sentenced-for- | 2025-03-06 | Scott Newcombe (owner of SJ Healthcare Management Se | public and private insurers  | - | $34,583 | - | Phantom Claims |
| owner-of-marketing-companies-and-dme-company | 2025-03-06 | Raheel Naviwala (owner of marketing companies and a  | Medicare; TRICARE | $100,000,000 | - | - | kickback_Bribery For Referral |
| eastern-nc-man-sentenced-to-over-four-years- | 2025-03-07 | Tyreek Rasheed Exum; Anthony Wandland, Jr. (co-defen | - | $1,000,000 | $620,000 | 50 | Covid or General Loan Fraud |
| san-bernardino-church-pastor-and-ex-politica | 2025-03-07 | Terrance Owens Elliott, a.k.a. 'Tony Elliott' (churc | - | $238,563 | - | - | Wire Fraud |
| va-firefighter-admits-scheme-to-commit-worke | 2025-03-07 | Richard Hyland (Department of Veterans Affairs firef | U.S. Department of Labor (fe | $479,341 | - | - | Benefit & Eligibility Fraud |
| baton-rouge-man-falsely-holding-himself-as-a | 2025-03-10 | Samrat Mukherjee (licensed paramedic falsely posing  | Medicaid (Louisiana); Blue C | - | - | - | Drug_Prescriptions |
| doctor-agrees-to-pay-468-000-to-settle-civil | 2025-03-10 | John Patterson, M.D. (physician); Nursemind Home Car | Medicare | - | $468,626 | - | kickback_Bribery For Referral |
| texas-pharmacist-sentenced-to-over-17-years- | 2025-03-10 | Dehshid "David" Nourian (pharmacist, owner/operator  | U.S. Department of Labor Off | $145,000,000 | $520,000,000 | 210 | Drug_Prescriptions |
| thibodaux-social-worker-sentenced-to-30-mont | 2025-03-10 | John Christopher Barrilleaux (social worker) | Private insurance companies | $4,592,650 | $4,592,750 | 30 | Phantom Claims |
| slidell-doctor-charged-with-health-care-frau | 2025-03-11 | Robert Tassin, M.D. (physician, independent contract | Medicare | $6,600,000 | - | - | Falsify certificate |
| three-former-executives-for-magellan-diagnos | 2025-03-11 | Amy Winslow (former CEO, Magellan Diagnostics, Inc.) | - | - | - | - | Other - FDA Submission Fraud |
| eastern-district-of-louisiana-u-s-attorneys- | 2025-03-12 | Shiva Akula (hospice owner); Michelle Andre | Medicare | - | $3,734,570 | - | Other - Unknown |
| hampton-man-sentenced-to-over-nine-years-in- | 2025-03-12 | Jamahl Rennelle Burch, aka Jarod or Jerrod Burch | Virginia Medicaid; Virginia  | $952,670 | $1,758,679 | 111 | Phantom Claims |
| doctor-sentenced-for-health-care-fraud-and-m | 2025-03-14 | Wendell Lewis Randall (physician, sole owner of Nati | Medicare; Medicaid (North Ca | $2,049,747 | $2,049,747 | 30 | FakeEncounter |
| illinois-doctor-pleads-guilty-to-evading-app | 2025-03-14 | Krishnaswami Sriram (medical doctor) | Medicare; IRS (tax loss) | $1,600,000 | - | - | Tax, Payroll or Coupon Fraud |
| marshalltown-woman-pleads-guilty-to-charges- | 2025-03-14 | Amanda Nicole Manatt (registered nurse) | - | - | - | - | Drug_Prescriptions |
| medical-equipment-business-owner-sentenced-t | 2025-03-14 | Shafi Abbas (owner of Aidmen Medical Equipment LLC a | Medicare | - | $1,333,722 | 12 | Device, DME |
| miami-inspector-pleads-guilty-in-a-scheme-to | 2025-03-14 | Manuel Delgado (contractor/inspector for Board of Ce | Medicare | $1,400,000 | - | - | kickback_Bribery For Referral |
| robert-burkich-m-d-settles-case-alleging-tha | 2025-03-14 | Robert Burkich, M.D. (physician); Preventive Medicin | Medicare | - | $700,000 | - | FakeEncounter |
| two-executives-of-louisiana-compounding-phar | 2025-03-14 | Christopher Kyle Johnston (general counsel, Central  | TRICARE; New Jersey State He | $100,000,000 | - | - | Drug_Prescriptions |
| former-long-island-business-owner-charged-wi | 2025-03-18 | Oleg Beretsky (owner of Obest, Inc.); Obest, Inc. | Medicare | $22,000,000 | - | - | kickback_Bribery For Referral |
| buffalo-woman-going-to-prison-for-filing-fal | 2025-03-19 | Maureen Holleran (workers' compensation claims handl | Insurance Company 1 (unnamed | $2,370,848 | - | 18 | Phantom Claims |
| putnam-county-nurse-practitioner-pleads-guil | 2025-03-19 | Shawn R. Blankenship (licensed nurse practitioner, o | Medicaid (West Virginia Medi | $600,000 | - | - | Phantom Claims |
| new-jersey-pain-clinic-admits-health-care-fr | 2025-03-20 | Pain Specialists, P.A. (pain clinic with locations i | Medicare; New Jersey Medicai | $58,365 | $380,077 | - | Upcoding |
| two-california-doctors-agree-to-settlements- | 2025-03-20 | Zachary J. Lipman MD (physician); Michael Woo-Ming M | Medicare | - | $375,000 | - | Device, DME |
| hollywood-hills-man-sentenced-to-nearly-312- | 2025-03-21 | Casey Mahoney (owner/operator of Healing Path Detox  | Private insurers | $2,900,000 | $240,000 | 41 | kickback_Bribery For Referral |
| jury-finds-physician-guilty-of-operating-a-p | 2025-03-21 | Ndubuisi Joseph Okafor, M.D. (sole practitioner and  | - | - | - | - | Drug_Prescriptions |
| three-convicted-for-fraudulently-billing-ove | 2025-03-21 | Dr. José Alzadon (medical director, Kentucky Addicti | Medicare; Kentucky Medicaid | $8,000,000 | - | - | Phantom Claims |
| carson-tahoe-health-system-agrees-to-pay-ove | 2025-03-24 | Carson Tahoe Health System (owner of Carson Tahoe Ph | - | $7,267,009 | $8,876,475 | - | Covid or General Loan Fraud |
| cuban-national-sentenced-to-over-five-years- | 2025-03-24 | Fernando Espinosa Leon (owner, Global Medical Supply | Medicare | $7,600,000 | $4,013,148 | 70 | Device, DME |
| river-hills-man-sentenced-to-21-months-impri | 2025-03-24 | Justin Drew Hanson (co-owner, Noah Associates); Moha | Medicare; Medicaid | $2,200,000 | $2,275,000 | 21 | kickback_Bribery For Referral |
| roofing-business-owner-and-payroll-administr | 2025-03-24 | William Skaggs Jr. (owner of Nastar Roofing); Billie | IRS | $2,500,000 | - | 36 | Tax, Payroll or Coupon Fraud |
| camden-county-company-settles-matter-allegin | 2025-03-25 | American Furniture Rentals, Inc. (furniture rental c | Small Business Administratio | $2,000,000 | $2,907,703 | - | Covid or General Loan Fraud |
| principals-of-fire-alarm-repair-company-plea | 2025-03-25 | Walter Stanzione (principal/leader of Fire Alarm Ele | City of New York agencies (D | - | - | - | Wire Fraud |
| romanian-men-indicted-for-card-skimming_93d9 | 2025-03-25 | Daniel Iulian Teutoc (a/k/a "Simon Mikula"); Constan | - | - | - | - | IdentityFraud |
| acting-u-s-attorney-announces-5-million-fals | 2025-03-26 | Community Options, Inc. (New Jersey not-for-profit p | Medicaid (New York Medicaid  | - | $5,016,626 | - | Retention of Overpayment |
| behavioral-healthcare-company-executive-sent | 2025-03-26 | Miguel Saravia (CEO of Dana Group Associates; former | - | - | $561,141 | 3 | Phantom Claims |
| convicted-nurse-practitioner-to-forfeit-over | 2025-03-26 | Trivikram Reddy (licensed nurse practitioner, owner  | Medicare; Blue Cross Blue Sh | $50,000,000 | $41,237,703 | 240 | Phantom Claims |
| koreatown-based-medicare-advantage-provider- | 2025-03-26 | Seoul Medical Group Inc. (Medicare Advantage provide | Medicare (Medicare Advantage | - | $62,850,000 | - | Upcoding |
| medical-device-manufacturer-and-its-owner-ag | 2025-03-26 | The Prometheus Group (medical device manufacturer);  | Medicare | - | $550,000 | - | Device, DME |
| medicare-advantage-provider-seoul-medical-gr | 2025-03-26 | Seoul Medical Group Inc. (Medicare Advantage provide | Medicare (Medicare Advantage | - | $62,850,000 | - | Upcoding |
| diopsys-inc-agrees-to-pay-up-to-14-25-millio | 2025-03-27 | Diopsys, Inc. (medical device company) | Medicare; Medicaid | - | $14,250,000 | - | FakeEncounter |
| leader-of-23-million-health-care-fraud-schem | 2025-03-27 | Junyi Liu a/k/a 'Jenny' (licensed acupuncturist, lea | Medicare; other insurance pr | $23,855,425 | $39,263,671 | - | Phantom Claims |
| walgreen-co-agrees-to-pay-over-2-8-million-t | 2025-03-27 | Walgreen Co. (national pharmacy chain) | Medicaid (MassHealth); Medic | - | $2,800,000 | - | Upcoding |
| diopsys-inc-agrees-to-pay-up-to-14-25-millio | 2025-03-28 | Diopsys Inc. (medical device company) | Medicare; Medicaid | - | $14,250,000 | - | FakeEncounter |
| texas-insurance-broker-sentenced-in-scheme-t | 2025-03-28 | Shelby Lynn Hill (health insurance broker) | - | $263,345 | $264,645 | 12 | Covid or General Loan Fraud |
| south-carolina-construction-company-to-pay-1 | 2025-03-31 | Thompson Construction Group Inc. (contractor, Sumter | U.S. Department of Housing a | $95,535 | $191,070 | - | Falsify certificate |
| florida-woman-convicted-of-embezzling-from-c | 2025-04-01 | Sehrelina Tardo (senior accountant at a car dealersh | - | - | $535,750 | - | Wire Fraud |
| beckley-medical-clinic-and-physician-agree-t | 2025-04-02 | Med-Surg Physician Group Inc. (medical practice); Ol | Medicare; Medicaid (West Vir | $76,191 | $152,382 | - | Phantom Claims |
| florida-man-pleads-guilty-to-multi-million-d | 2025-04-02 | Corey Alston; Latresia A. Wilson (co-defendant); com | Medicare | $8,400,000 | - | - | IdentityFraud |
| hospital-medical-imaging-services-company-an | 2025-04-02 | Desert Imaging Services, L.P.; In Tandem Solutions G | Medicare;Medicaid (Texas) | - | $3,100,652 | - | kickback_Bribery For Referral |
| lancaster-county-trio-pleads-guilty-to-consp | 2025-04-02 | Charles McKinley Griffin (owner/operator, Transforma | Medicaid (South Carolina Med | $246,335 | - | - | Phantom Claims |
| louisiana-chiropractor-convicted-of-health-c | 2025-04-02 | Dr. Benjamin Tekippe (chiropractor, owner of Metairi | Blue Cross Blue Shield of Lo | $2,300,000 | - | - | Phantom Claims |
| medical-group-agrees-to-pay-2-8m-to-settle-f | 2025-04-02 | Fairfax Radiological Consultants, PLLC, formerly kno | Small Business Administratio | $6,800,000 | $2,881,260 | - | Covid or General Loan Fraud |
| national-sales-director-for-new-york-based-m | 2025-04-02 | David Fuhrmann (national sales director for mobile m | Medicare | $70,600,000 | - | - | kickback_Bribery For Referral |
| st-johns-county-man-pleads-guilty-to-tax-fra | 2025-04-02 | Daniel Tharp (managing director, Hangar X Holdings,  | - | $1,200,000 | - | - | Tax, Payroll or Coupon Fraud |
| nurse-anesthetist-sentenced-to-federal-priso | 2025-04-03 | Ian Lindsey (nurse anesthetist) | - | - | $5,000 | 3 | Drug_Prescriptions |
| owner-of-halo-home-healthcare-sentenced-to-4 | 2025-04-03 | Sharon Romaine Ward (owner of Halo Home Healthcare); | Medicare; Medicaid (Ohio Dep | $8,556,777 | $8,484,916 | 48 | Phantom Claims |
| kansas-doctor-admits-accepting-kickbacks-to- | 2025-04-04 | Dr. Scott Taggart Roethle (telemedicine physician, a | Medicare | $9,500,000 | - | - | kickback_Bribery For Referral |
| united-states-files-false-claims-act-complai | 2025-04-04 | Vohra Wound Physicians Management LLC; Dr. Ameet Voh | Medicare | - | - | - | Upcoding |
| ceo-of-local-it-staffing-company-charged-wit | 2025-04-07 | Thomas Stafford (Chief Executive Officer and Preside | - | $2,008,046 | - | - | Tax, Payroll or Coupon Fraud |
| pain-management-clinic-owners-and-operators- | 2025-04-07 | Brandon Nowak (officer/operator, Alternative Integra | Medicare; Medicare Advantage | - | - | - | Phantom Claims |
| home-health-care-companies-owner-sentenced-t | 2025-04-08 | Sally Njume-Tatsing (owner/operator of three Labelle | Medicaid (Ohio) | $5,700,000 | $5,700,000 | 42 | Upcoding |
| new-jersey-man-sentenced-for-prescription-op | 2025-04-08 | Chris Ruediger | - | - | - | 16 | Drug_Prescriptions |
| greensboro-woman-pleads-guilty-to-health-car | 2025-04-09 | Jasmine Hoyle (owner of Harvest Focused & Consulting | Medicaid (North Carolina Med | $6,000,000 | - | - | Phantom Claims |
| florida-pharmacy-pleads-guilty-to-health-car | 2025-04-10 | OHM Pharmacy Services, aka "Benzer," aka "Auburndale | Medicare (Part D plans) | - | $1,100,000 | - | Falsify certificate |
| founder-and-top-executive-for-fresno-based-b | 2025-04-10 | Marcus Asay (founder and chairman); Antonio Gastelum | - | $2,250,000 | $2,638,500 | 60 | Other - Unknown |
| fresno-county-podiatrist-and-sales-represent | 2025-04-10 | Felipe Ruiz (podiatrist at West Coast Podiatry Inc.) | Medicare; Medicaid (Medi-Cal | $3,200,000 | - | 63 | FakeEncounter |
| minnesota-couple-indicted-in-15-million-medi | 2025-04-10 | Gabriel Adam Alexander Luthor, a.k.a. Gabriel Adam A | Medicare; Medicaid; other in | $15,000,000 | - | - | Upcoding |
| fort-myers-couple-sentenced-to-federal-priso | 2025-04-11 | Timothy Craig Jolloff; Lisa Ann Jolloff | Small Business Administratio | $3,403,265 | $3,400,000 | 97 | Covid or General Loan Fraud |
| justice-department-surpasses-12-billion-in-c | 2025-04-11 | Bernard L. Madoff (chairman, Bernard L. Madoff Inves | - | - | - | 180 | Other - Unknown |
| north-ridgeville-doctor-pleads-guilty-to-hea | 2025-04-11 | Timothy Sutton (doctor); Real Time Physicians, LLC ( | Medicare | $14,500,000 | - | - | Falsify certificate |
| two-men-sentenced-for-misbranding-and-conspi | 2025-04-11 | Daniel Motha (co-owner and CEO of JDM Supply LLC); J | - | $2,600,000 | $19,000 | - | Device, DME |
| union-city-pharmacy-agrees-to-resolve-false- | 2025-04-11 | People's Rx, Inc., d/b/a The People's Pharmacy Shopp | Medicare Part D; New Jersey  | - | $995,420 | - | Phantom Claims |
| ashland-city-doctor-sentenced-to-3-years-for | 2025-04-14 | John R. Manning (licensed medical doctor) | Medicare | $41,083,490 | $20,592,868 | 36 | kickback_Bribery For Referral |
| colombian-national-indicted-for-assaulting-i | 2025-04-15 | Hector Villegas-Alvarez | - | - | - | - | Other - Unknown |
| florida-woman-pleads-guilty-to-conspiring-to | 2025-04-15 | Yolanda Dupont (nominee owner of Allstar Medical Sup | Medicare | $3,300,000 | - | - | Device, DME |
| owner-of-new-jersey-businesses-admits-to-fra | 2025-04-15 | Daniel Dadoun (owner of several New Jersey businesse | - | $3,200,000 | - | - | Covid or General Loan Fraud |
| panamanian-doctor-pleads-guilty-in-criminal- | 2025-04-15 | Dr. Rolando Chin (surgeon residing in Panama); nearl | U.S. Department of Veterans  | - | - | - | Phantom Claims |
| delaware-woman-admits-role-in-covid-19-relie | 2025-04-16 | Adrienne Ponzo (loan application preparer); unnamed  | - | $1,500,000 | - | - | Covid or General Loan Fraud |
| former-nurse-practitioner-agrees-to-50-000-s | 2025-04-16 | Jordona Ndon (former nurse practitioner) | Medicare | - | $50,000 | - | Device, DME |
| physician-convicted-at-trial-for-illegal-dis | 2025-04-16 | Neil K. Anand M.D. (physician, owner of in-house pha | Medicare; U.S. Office of Per | $2,300,000 | - | - | Drug_Prescriptions |
| former-owner-of-collapsed-nursing-home-empir | 2025-04-17 | Joseph Schwartz (owner/operator of Skyline Managemen | Internal Revenue Service (U. | $38,000,000 | - | 36 | Tax, Payroll or Coupon Fraud |
| new-england-doctor-sentenced-for-drug-conspi | 2025-04-17 | Adnan S. Khan, M.D. (owner/physician, New England Me | - | - | $95,000 | 8 | Drug_Prescriptions |
| pharmacist-indicted-in-2-million-health-care | 2025-04-17 | Cynthia Ann Herrera (pharmacist) | Medicaid (Texas Medicaid Pro | $2,000,000 | - | - | Phantom Claims |
| executive-vice-president-of-insurance-broker | 2025-04-18 | Dafud Iza (executive vice president of an insurance  | Affordable Care Act federal  | $133,900,000 | - | - | Benefit & Eligibility Fraud |
| the-arthritis-knee-pain-centers-and-dr-john- | 2025-04-18 | The Arthritis Knee Pain Centers (AKPC); Dr. John Rus | Medicare | - | - | - | FakeEncounter |
| united-states-files-complaint-against-barco- | 2025-04-18 | Barco Uniforms Inc. (apparel seller/importer); Kenny | - | - | - | - | Tax, Payroll or Coupon Fraud |
| operators-of-new-jersey-company-sentenced-to | 2025-04-21 | Eric Karlewicz a/k/a 'Anthony Mazza' (operator of ma | Medicare; TRICARE | $127,000,000 | $259,900,000 | 80 | kickback_Bribery For Referral |
| walgreens-agrees-to-pay-up-to-350-million-fo | 2025-04-21 | Walgreens Boots Alliance; Walgreen Co. and subsidiar | Medicare; other federal heal | - | $300,000,000 | - | Drug_Prescriptions |
| walgreens-agrees-to-pay-up-to-350m-for-illeg | 2025-04-21 | Walgreens Boots Alliance; Walgreen Co. and various s | Medicare; other federal heal | - | $350,000,000 | - | Drug_Prescriptions |
| a-leader-of-notorious-philadelphia-10th-and- | 2025-04-22 | Michael Procopio (leader of South Philadelphia's '10 | - | - | - | 72 | Drug_Prescriptions |
| lawton-area-trio-sentenced-to-serve-more-tha | 2025-04-22 | Nathan Mathews (owner, Emerald Lane Therapy Services | TRICARE (Defense Health Agen | $7,000,000 | $2,695,551 | 87 | Phantom Claims |
| genetic-testing-marketing-companies-genexe-l | 2025-04-23 | Genexe, LLC (d/b/a Genexe Health, marketing company) | Medicare | - | $6,000,000 | - | kickback_Bribery For Referral |
| memphis-woman-sentenced-in-healthcare-fraud- | 2025-04-23 | Nakita Cannady (owner and operator of What About Us  | Cigna Insurance | $193,508 | $540,390 | 14 | Upcoding |
| philadelphia-businesswoman-sentenced-to-20-m | 2025-04-23 | Nyesha D. Paris, aka Nyesha D. Henderson and Nyesha  | Medicaid; Paycheck Protectio | $600,000 | $630,001 | 20 | Phantom Claims |
| vault-agrees-to-pay-8-million-to-settle-alle | 2025-04-23 | Vault Medical Services, P.A.; Vault Medical Services | HRSA COVID-19 Uninsured Prog | - | $8,000,000 | - | Covid or General Loan Fraud |
| ex-orange-county-resident-sentenced-to-7-yea | 2025-04-24 | Darius Moore (patient recruiter / "body broker") | Private health insurance pla | $500,000 | - | 84 | kickback_Bribery For Referral |
| former-owner-of-york-pain-management-practic | 2025-04-24 | Rodney L. Yentzer (former owner of Pain Medicine of  | Medicare; Pennsylvania Medic | $10,000,000 | $7,851,664 | 97 | FakeEncounter |
| payroll-services-company-owner-sentenced-to- | 2025-04-24 | Matthew Brown (owner/operator of Elite Payroll and o | - | $20,000,000 | $22,601,585 | 50 | Tax, Payroll or Coupon Fraud |
| massachusetts-doctor-agrees-to-plead-guilty- | 2025-04-25 | Le Thu (doctor) | Medicare | $35,300,000 | - | - | Falsify certificate |
| two-former-laboratory-sales-executives-sente | 2025-04-25 | Stephen Kash (laboratory sales executive, True Healt | Medicare; Medicaid | - | $997,042 | 18 | kickback_Bribery For Referral |
| complaint-filed-against-houston-pharmacy-and | 2025-04-28 | Nnwood Pharmacy; Cheryl Brew Greenleaf (owner); Wend | - | - | - | - | Drug_Prescriptions |
| wake-forest-woman-sentenced-to-prison-for-85 | 2025-04-28 | Sonya Lenise Davis (owner of Sonya's Braiding) | - | $85,000 | - | 6 | Covid or General Loan Fraud |
| former-monmouth-county-resident-sentenced-to | 2025-04-29 | Kevin Aguilar | - | $3,772,567 | $7,545,134 | 192 | Covid or General Loan Fraud |
| harlingen-couple-guilty-in-multimillion-doll | 2025-04-29 | Jeremiah Yzaguirre (operator, Southwest Medical Home | Medicare | $14,000,000 | - | - | Phantom Claims |
| jury-convicts-florida-man-for-stealing-10-9- | 2025-04-29 | Lino Mallari Gutierrez a/k/a 'Joe Gutierrez' (owner/ | Medicare | $10,900,000 | - | - | Device, DME |
| philadelphia-man-pleads-guilty-to-defrauding | 2025-04-29 | James Sessoms | Medicaid (Pennsylvania Depar | $1,063,633 | - | - | Benefit & Eligibility Fraud |
| statement-of-u-s-attorney-jay-clayton-on-the | 2025-04-29 | Omnicare (long-term care pharmacy); CVS Health Corpo | Medicare; Medicaid; TRICARE | $135,592,814 | $406,778,442 | - | Drug_Prescriptions |
| u-s-attorney-announces-202-million-settlemen | 2025-04-29 | Gilead Sciences, Inc. (pharmaceutical manufacturer) | Medicare; Medicaid (New York | - | $202,000,000 | - | kickback_Bribery For Referral |
| cumberland-county-drug-and-alcohol-rehabilit | 2025-04-30 | Summit BHC New Jersey, LLC, d/b/a Seabrook (drug and | Veterans Health Administrati | - | $19,750,000 | - | Falsify certificate |
| kingsville-business-owner-pleads-guilty-to-t | 2025-04-30 | Timothy Gaines Pollard (owner, Tim Pollard Construct | - | $400,000 | - | - | Tax, Payroll or Coupon Fraud |
| owner-of-chicago-area-convenience-stores-con | 2025-04-30 | Hassan Abdellatif, aka 'Eric' (owner/operator of El  | USDA Women, Infants, and Chi | $19,000,000 | - | - | Tax, Payroll or Coupon Fraud |
| wethersfield-woman-admits-role-in-scheme-tha | 2025-04-30 | Suhail Aponte (sole principal and registered agent o | Medicaid (Connecticut Medica | $1,876,617 | $459,000 | - | Phantom Claims |
| the-united-states-files-false-claims-act-com | 2025-05-01 | Aetna Inc. and affiliates (Medicare Advantage insure | Medicare (Medicare Advantage | - | - | - | kickback_Bribery For Referral |
| united-states-files-complaint-against-severa | 2025-05-01 | Aetna, Inc. and affiliates (Medicare Advantage insur | Medicare (Medicare Advantage | - | - | - | kickback_Bribery For Referral |
| louisiana-nurse-practitioner-convicted-of-2m | 2025-05-02 | Shanone Chatman-Ashley (nurse practitioner, independ | Medicare | $2,000,000 | - | - | Device, DME |
| nurse-practitioner-from-opelousas-convicted- | 2025-05-02 | Shanone Chatman-Ashley (nurse practitioner, independ | Medicare | $2,000,000 | - | - | Device, DME |
| charlotte-clinic-owner-agrees-to-settle-alle | 2025-05-05 | Steven Osbey (co-owner, Reign & Inspirations, LLC);  | Medicaid (NC Medicaid) | - | $4,711,159 | 52 | Phantom Claims |
| franklin-kentucky-pharmacist-and-spouse-sent | 2025-05-05 | Joseph Huff (pharmacist); Jenifer Huff (spouse) | Kentucky Medicaid; unnamed c | - | $23,248 | 36 | Drug_Prescriptions |
| california-man-sentenced-to-12-years-impriso | 2025-05-06 | Petros Fichidzhyan (controlled sham hospice entities | Medicare | $17,000,000 | $17,129,060 | 144 | Phantom Claims |
| leader-of-48-million-healthcare-fraud-scheme | 2025-05-06 | Manishkumar Patel (leader of scheme, script seller) | Medicare | $48,000,000 | $54,990,592 | 14 | kickback_Bribery For Referral |
| four-sentenced-in-110-million-dollar-kickbac | 2025-05-08 | John Ageudo Rodriguez (pharmacist, owner of Pharr Fa | Medicare; TRICARE; U.S. Depa | $110,000,000 | - | 60 | kickback_Bribery For Referral |
| providence-man-indicted-for-making-false-sta | 2025-05-08 | Nicholas M. Ash | U.S. Department of Veterans  | - | - | - | Benefit & Eligibility Fraud |
| indian-citizen-charged-in-multi-million-doll | 2025-05-09 | Mohammed Asif (owner and director of American Labwor | Medicare | $8,700,000 | - | - | Phantom Claims |
| norwalk-dentists-pay-more-than-600k-to-settl | 2025-05-09 | Advanced Dental Center PC (dental practice); Tal Yos | Medicaid (Connecticut Medica | - | $645,721 | - | kickback_Bribery For Referral |
| pharmaceutical-manufacturer-assertio-therape | 2025-05-09 | Assertio Therapeutics Inc., f/k/a Depomed Inc. (phar | Medicare (including Medicare | - | $3,600,000 | - | Drug_Prescriptions |
| pharmaceutical-manufacturer-assertio-therape | 2025-05-09 | Assertio Therapeutics, Inc., formerly known as Depom | Medicare; TRICARE | - | $3,600,000 | - | Drug_Prescriptions |
| second-leader-of-notorious-philadelphia-10th | 2025-05-09 | Frank Procopio (leader of '10th and O Crew'); Michae | - | - | - | 72 | Drug_Prescriptions |
| three-baton-rouge-individuals-plead-guilty-i | 2025-05-09 | Kevan Andre Hills; Devin Tyrone Stampley, Jr.; Asia  | Medicaid; Paycheck Protectio | $419,476 | - | - | Drug_Prescriptions |
| new-hampshire-doctor-pleads-guilty-to-illega | 2025-05-13 | Robert G. Soucy Jr., D.O. (doctor) | - | - | - | - | Drug_Prescriptions |
| four-businessmen-and-two-companies-charged-i | 2025-05-14 | Alan Redmond (principal architect/controller of the  | - | - | - | - | Wire Fraud |
| fresno-based-community-health-system-agree-t | 2025-05-14 | Community Health System (hospital system operating C | Medicare; other governmental | - | $31,500,000 | - | kickback_Bribery For Referral |
| texas-company-charged-with-aiding-and-abetti | 2025-05-14 | Murex Management, Inc. (MMI) (management company of  | First NBC Bank; a North Caro | $1,200,000,000 | - | - | Wire Fraud |
| catholic-health-agrees-to-pay-nearly-3-3-mil | 2025-05-16 | Catholic Health System, Inc. (CHS) and its affiliate | Medicare | - | $3,293,122 | - | kickback_Bribery For Referral |
| connecticut-physiatrist-and-practice-pay-427 | 2025-05-16 | Pain Management, LLC; Halina Snowball, M.D. (owner,  | Medicare | - | $427,129 | - | Unbundling |
| florida-ophthalmology-practice-agrees-to-pay | 2025-05-16 | Pinellas Eye Care, P.A. d/b/a Gulfcoast Eye Care (op | Medicare; Medicaid (Florida) | - | $615,000 | - | kickback_Bribery For Referral |
| florida-pharmacy-pleads-guilty-to-health-car | 2025-05-16 | OHM Pharmacy Services, aka "Benzer," aka "Auburndale | Medicare Part D | - | $1,100,000 | - | Falsify certificate |
| middletown-man-admits-role-in-scheme-that-de | 2025-05-16 | Ramon Apellaniz (a/k/a 'Kristopher Rockefeller', de  | Medicaid (Connecticut Medica | $1,876,617 | $469,000 | - | Phantom Claims |
| ceo-of-spine-device-company-pleads-guilty-to | 2025-05-19 | Dr. Kingsley R. Chin (Founder, President and CEO of  | Medicare | $4,750 | - | - | kickback_Bribery For Referral |
| correction-officers-charged-with-years-long- | 2025-05-19 | Todd Faustin (current NYC Department of Correction o | New York State Workers' Comp | $996,171 | - | 15 | Benefit & Eligibility Fraud |
| former-tulare-county-medical-doctor-pleads-g | 2025-05-19 | Stephen D. Meis, M.D. (Medical Director, Golden Sunr | - | - | - | 18 | Drug_Prescriptions |
| business-owner-pleads-guilty-to-fraud-and-mo | 2025-05-20 | Zaven Yeghiazaryan (business owner) | Medicaid | - | $334,905 | - | Covid or General Loan Fraud |
| director-of-mobile-medical-diagnostics-compa | 2025-05-20 | James Rausch (director of operations and sales, Nort | Medicare | $70,600,000 | - | - | kickback_Bribery For Referral |
| florida-ophthalmology-practice-agrees-to-pay | 2025-05-20 | Pinellas Eye Care, P.A. d/b/a Gulfcoast Eye Care (op | Medicare; Medicaid (Florida) | - | $615,000 | - | kickback_Bribery For Referral |
| foreign-national-sentenced-for-3-2-million-m | 2025-05-20 | Julian Lopez (seller of Medicare beneficiary informa | Medicare | $3,200,000 | $1,496,412 | 30 | Device, DME |
| pittsburgh-area-nursing-home-companies-order | 2025-05-20 | Comprehensive Healthcare Management Services, LLC, d | Medicare; Medicaid | - | $15,350,569 | - | Falsify certificate |
| agendia-inc-knoxville-comprehensive-breast-c | 2025-05-21 | Agendia, Inc. (molecular diagnostics company); Knoxv | Medicare; Medicaid; Federal  | - | $3,780,000 | - | kickback_Bribery For Referral |
| houston-pharmacy-owner-sentenced-to-19-years | 2025-05-21 | Christopher Obaze (owner and pharmacist-in-charge, C | - | - | - | 228 | Drug_Prescriptions |
| jackson-health-foundation-executive-charged- | 2025-05-21 | Charmaine Gatlin (former Chief Operating Officer of  | - | $3,600,000 | - | - | Wire Fraud |
| jury-convicts-home-health-agency-owner-in-me | 2025-05-21 | Paul Njoku (owner and CEO of Opnet Health Care Servi | Medicare | $400,000 | - | - | Falsify certificate |
| ohio-man-sentenced-to-prison-for-paycheck-pr | 2025-05-21 | Daniel R. Hitlan (owner of small businesses) | - | $2,000,000 | $2,744,013 | 27 | Covid or General Loan Fraud |
| oklahoma-city-doctor-surrenders-dispensing-a | 2025-05-21 | Richard Swenson, M.D. (physician at Accident Care an | - | - | $130,000 | - | Drug_Prescriptions |
| taunton-man-sentenced-to-more-than-two-years | 2025-05-21 | Henry Ezeonyido (organizer); Brendon Ashe; Aqiyla At | Five unnamed private health  | $1,000,000 | $1,052,311 | 27 | Phantom Claims |
| texas-doctor-who-falsely-diagnosed-patients- | 2025-05-21 | Jorge Zamora-Quezada, M.D. (rheumatologist) | Medicare; Medicaid; TRICARE; | $118,000,000 | $28,245,454 | 120 | FakeEncounter |
| illegal-alien-sentenced-in-multi-million-dol | 2025-05-22 | Ana Juanita Andrade-Reyes (owner of shell constructi | Internal Revenue Service (IR | $8,000,000 | $2,748,770 | 37 | Tax, Payroll or Coupon Fraud |
| irondequoit-man-claiming-to-be-a-physician-c | 2025-05-22 | Kevin M. Whitman (individual falsely claiming to be  | - | - | - | - | Drug_Prescriptions |
| two-charged-in-227m-medicare-fraud-scheme_06 | 2025-05-22 | Syed Murtuza Kablazada (owner/operator of purported  | Medicare | $227,000,000 | - | - | Phantom Claims |
| two-st-louis-area-doctors-admit-health-crime | 2025-05-22 | Dr. Asim Muhammad Ali (physician, owner of Central D | Medicare; Missouri Medicaid; | $23,344 | - | - | Phantom Claims |
| former-senior-partner-at-mckinsey-amp-compan | 2025-05-23 | Martin Elling (former senior partner, McKinsey & Com | - | - | $40,000 | 6 | Other - Unknown |
| illegal-alien-arrested-for-impersonating-u-s | 2025-05-23 | Javier Alfonso Nunez Suarez (beneficiary) | Medicaid; Social Security Ad | $588,000 | - | - | Benefit & Eligibility Fraud |
| owner-of-durable-medical-equipment-companies | 2025-05-23 | Raju Sharma (owner of Pharmagears, LLC and RR Medco, | Medicare | $29,600,000 | $16,050,000 | - | Device, DME |
| three-people-sentenced-to-prison-for-scheme- | 2025-05-23 | Jeremie Vargas Ramirez (de facto owner of NOVA DME); | Medicare | $13,526,920 | $2,256,787 | 24 | Device, DME |
| bloomfield-resident-admits-role-in-opioid-di | 2025-05-27 | Danielle Molinari | - | - | - | - | Drug_Prescriptions |
| chula-vista-man-pleads-guilty-in-51-million- | 2025-05-27 | Fernando Valenzuela Ayub (owner/operator of DME comp | Medicare | $51,000,000 | $7,101,320 | - | Device, DME |
| craig-h-missakian-sworn-in-as-united-states- | 2025-05-27 | - | - | - | - | - | Other - Unknown |
| medical-equipment-business-owner-sentenced-t | 2025-05-27 | Pedro Reyes (owner of durable medical equipment busi | Medicare | - | $6,004,916 | 33 | Device, DME |
| ohio-man-pleads-guilty-to-filing-false-tax-r | 2025-05-27 | Sidney L. Glover, Jr. (sole owner of Teaching Excell | Medicaid (Ohio Medicaid, via | $155,000 | - | - | Tax, Payroll or Coupon Fraud |
| slidell-doctor-convicted-of-health-care-frau | 2025-05-27 | Robert Tassin, M.D. (physician working for purported | Medicare | $6,600,000 | $2,106,757 | - | Falsify certificate |
| amtrak-employees-admit-participating-in-11-m | 2025-05-28 | Kevin Frink (Amtrak employee); Michael Toal (Amtrak  | Amtrak health care plan | $11,000,000 | - | 34 | kickback_Bribery For Referral |
| five-new-jersey-pharmacies-agree-to-pay-1-93 | 2025-05-28 | 2818 JFK Pharmacy LLC; 518 Summit Care Pharmacy LLC; | Medicare Part D; New Jersey  | - | $1,935,000 | - | Phantom Claims |
| illinois-woman-sentenced-for-prescription-dr | 2025-05-28 | Cassandra Marie Strube (administrator at nursing and | - | - | $7,175 | - | Drug_Prescriptions |
| pharmacist-sentenced-to-prison-for-false-med | 2025-05-28 | Justin Bell (pharmacist, owner and operator of Georg | Kentucky Medicaid | $118,621 | $138,621 | 4 | Drug_Prescriptions |
| south-carolina-man-charged-for-multimillion- | 2025-05-28 | Patrick Britton-Harr (owner of Provista Health and A | Medicare | $15,000,000 | - | - | Phantom Claims |
| south-carolina-man-charged-in-maryland-for-m | 2025-05-28 | Patrick Britton-Harr (owner of Provista Health and A | Medicare | $15,000,000 | - | - | Phantom Claims |
| missouri-man-pleads-guilty-to-multimillion-d | 2025-05-29 | Jamie P. McNamara (operator/owner of laboratories in | Medicare | $174,000,000 | $7,000,000 | - | kickback_Bribery For Referral |
| sovereign-health-group-founder-and-ex-ceo-ar | 2025-05-29 | Tonmoy Sharma (founder and former CEO, Sovereign Hea | Private health insurers (out | $149,000,000 | - | - | Wire Fraud |
| collin-county-physician-agrees-to-pay-3-5-mi | 2025-05-30 | Samad Khan, M.D. (physician, owner of SK Primary Car | HRSA COVID-19 Claims Reimbur | - | $3,500,000 | - | Upcoding |
| florida-man-sentenced-to-42-months-for-multi | 2025-05-30 | Alan Swiss (operator of Tropical Medical Marketing,  | Medicare; Medicare Advantage | $18,000,000 | $13,301,859 | 42 | Device, DME |
| spokane-dermatologist-agrees-to-pay-1-4-mill | 2025-05-30 | William Philip Werschler (dermatologist, owner); Spo | - | - | $1,400,000 | - | Covid or General Loan Fraud |
| ellison-c-travis-appointed-acting-united-sta | 2025-06-02 | - | - | - | - | - | Other - Unknown |
| john-p-heekin-sworn-in-as-u-s-attorney-for-t | 2025-06-02 | - | - | - | - | - | Other - Unknown |
| residential-treatment-provider-agrees-to-pay | 2025-06-02 | The Opportunity Alliance (residential treatment prov | Medicare; Medicaid (MaineCar | - | $346,369 | - | FakeEncounter |
| ceo-of-health-care-software-company-convicte | 2025-06-03 | Gary Cox (CEO of Power Mobility Doctor Rx, LLC (DMER | Medicare; other federal heal | $1,000,000,000 | - | - | Falsify certificate |
| florida-man-sentenced-to-22-months-imprisonm | 2025-06-03 | Michael G.V. Comino (fifty percent owner of Kestrel  | Medicare | $2,000,000 | $2,000,000 | 22 | kickback_Bribery For Referral |
| houston-doctor-pays-six-figures-to-settle-fa | 2025-06-03 | Dr. Benjamin Tiongson (pain management physician); P | Medicare | - | $390,082 | - | Upcoding |
| ohio-based-nonprofit-and-affiliated-nursing- | 2025-06-03 | American Health Foundation Inc. (nonprofit owner); A | Medicare; Medicaid | - | $3,610,000 | - | FakeEncounter |
| two-west-covina-women-arrested-on-indictment | 2025-06-03 | Normita Sierra (owner/operator of Golden Meadows Hos | Medicare | $4,800,000 | - | - | FakeEncounter |
| united-states-files-false-claims-act-complai | 2025-06-03 | AIMA Business and Medical Support, LLC (medical bill | Medicare | $15,178,946 | - | - | FakeEncounter |
| middlesex-county-man-sentenced-to-27-months- | 2025-06-04 | Mohammed Rahman (controller of Caltech Trading Corpo | - | $1,000,000 | $2,393,200 | 27 | Wire Fraud |
| sacramento-doctor-agrees-to-pay-125-000-for- | 2025-06-04 | Philip Yen, M.D. (radiologist; DEA registrant at Sut | - | - | $125,000 | - | Drug_Prescriptions |
| former-spouse-of-deceased-u-s-army-veteran-s | 2025-06-05 | Miranda Rachel Briggs, a/k/a Miranda Rachel Fisher ( | U.S. Department of Veterans  | $129,000 | $129,000 | 2 | Benefit & Eligibility Fraud |
| louisiana-man-pleads-guilty-to-3-8-million-d | 2025-06-05 | Michael L. Riggins (owner of Bluewater Healthcare);  | Medicare | $3,800,000 | - | - | Device, DME |
| small-business-investment-company-agrees-to- | 2025-06-05 | Argosy Investment Partners V, L.P. (Small Business I | U.S. Small Business Administ | $1,205,352 | $1,500,000 | - | Covid or General Loan Fraud |
| ceo-of-health-care-software-company-convicte | 2025-06-06 | Gary Cox (CEO of Power Mobility Doctor Rx, LLC (DMER | Medicare; other federal heal | $1,000,000,000 | - | - | Falsify certificate |
| former-chief-financial-officer-pleads-guilty | 2025-06-06 | Pamela J. Kahut (former Chief Financial Officer, Pac | Pacific States Marine Fisher | $211,083 | - | - | Other - Unknown |
| fraudulent-billing-scheme-targeted-in-false- | 2025-06-06 | Absolute Physical & Aquatic Therapy, LLC (physical t | - | - | $754,723 | - | Phantom Claims |
| man-sentenced-for-obtaining-a-controlled-sub | 2025-06-06 | Paul M. Hughes; The Hughes and Company Foundation US | - | - | - | 54 | Drug_Prescriptions |
| southern-california-nurse-indicted-for-multi | 2025-06-06 | Jessa Zayas (CEO and owner of Healing Hands Hospice  | Medicare | $2,500,000 | - | - | Falsify certificate |
| suburban-chicago-physician-sentenced-to-ten- | 2025-06-10 | Mona Ghosh (physician, owner of Progressive Women's  | Medicaid (Illinois);TRICARE; | - | $1,500,000 | 120 | FakeEncounter |
| doctor-at-l5-pain-clinic-sentenced-to-40-mon | 2025-06-11 | Duane Dixon (doctor); Wendell Lewis Randall (former  | Medicaid (Virginia) | - | $235,000 | 40 | Drug_Prescriptions |
| mahlega-abdsharafat-and-creative-hospice-set | 2025-06-11 | Mahlega Abdsharafat, aka "Mallie Sharafat"; Creative | Medicare; Medicaid (Georgia) | - | $9,200,000 | - | kickback_Bribery For Referral |
| new-york-man-pleads-guilty-to-70-million-kic | 2025-06-11 | James Rausch (director of operations and sales, Nort | Medicare | $70,600,000 | - | - | kickback_Bribery For Referral |
| owner-of-long-island-ambulette-services-plea | 2025-06-11 | Adnan Arshad, aka 'Eddie' (owner of MTK Taxi LLC and | Medicaid (New York) | $20,000,000 | - | 97 | Phantom Claims |
| veterans-affairs-contractor-agrees-to-pay-4- | 2025-06-11 | Omnicell (Delaware-based VA contractor selling/leasi | U.S. Department of Veterans  | - | $4,366,660 | - | Retention of Overpayment |
| four-charged-with-health-care-fraud-and-rela | 2025-06-12 | Edward Cannatelli; Robbyn Cannatelli; Thomas Farese; | Medicare | - | - | - | Device, DME |
| fugitive-physician-sentenced-to-prison-in-me | 2025-06-12 | Lilit Gagikovna Baltaian (physician) | Medicare | $1,497,159 | $1,497,159 | 54 | Falsify certificate |
| waterbury-woman-pleads-guilty-admits-multipl | 2025-06-13 | Marlenin Vito (Medicaid Coordinator at assisted livi | - | $361,557 | - | - | Wire Fraud |
| wmata-train-operators-arrested-in-health-car | 2025-06-13 | Michelle Shropshire (WMATA train operator, scheme or | American Family Life Assuran | $362,035 | - | 24 | Phantom Claims |
| baltimore-man-pleads-guilty-in-connection-wi | 2025-06-16 | Matthew Hightower; Davon Carter (shooter); Clifton M | - | - | - | - | Other - Unknown |
| chicago-lab-owner-sentenced-to-seven-years-i | 2025-06-18 | Zishan Alvi (owner/operator of Chicago Covid-19 test | U.S. Department of Health an | $14,000,000 | $22,100,000 | 84 | Phantom Claims |
| chicago-lab-owner-sentenced-to-seven-years-i | 2025-06-18 | Zishan Alvi (owner and operator of Chicago laborator | U.S. Department of Health an | $14,000,000 | $21,629,217 | 84 | Phantom Claims |
| ocala-mental-health-counselor-arrested-for-a | 2025-06-18 | Michelle Forsythe (licensed mental health counselor) | Two unnamed commercial healt | $483,511 | $483,511 | - | Phantom Claims |
| chesterfield-doctor-sentenced-to-5-years-in- | 2025-06-20 | Dr. Stanley L. Librach (physician); Dr. Asim Muhamma | Medicare; Missouri Medicaid | - | $3,051,265 | 108 | kickback_Bribery For Referral |
| south-florida-medical-providers-agree-to-pay | 2025-06-20 | Vascular and Interventional Specialists, LLC (VIS) ( | Medicare | - | $810,301 | - | FakeEncounter |
| california-man-pleads-guilty-in-connection-w | 2025-06-23 | Mihran Panosyan (money launderer); Petros Fichidzhya | Medicare | $16,000,000 | - | 144 | Phantom Claims |
| florida-nonprofit-founder-and-accountant-cha | 2025-06-23 | Leo Joseph Govoni (co-founder of Center for Special  | - | $100,000,000 | - | - | Wire Fraud |
| florida-man-convicted-in-multimillion-dollar | 2025-06-24 | Ted Albin (operator of Grapevine Professional Servic | Medicare | $38,000,000 | - | - | Device, DME |
| companies-pay-13-million-to-resolve-false-cl | 2025-06-25 | C&J Welding & Construction (subsidiary of Rema Tip T | Small Business Administratio | $8,854,787 | $13,000,000 | - | Covid or General Loan Fraud |
| eureka-chiropractor-sentenced-to-20-months-i | 2025-06-25 | Carrie Musselman (chiropractor) | Medicare; twelve other insur | $2,500,000 | $2,300,000 | 20 | Upcoding |
| michigan-doctor-sentenced-to-four-years-for- | 2025-06-26 | Sophie Toya, M.D. (physician who signed orthotic bra | Medicare | $6,300,000 | $3,727,410 | 48 | Device, DME |
| nuway-alliance-agrees-to-pay-18-500-000-sett | 2025-06-26 | NUWAY Alliance, Inc. (substance use disorder treatme | Medicaid (Minnesota Medical  | - | $18,500,000 | - | kickback_Bribery For Referral |
| physician-sentenced-to-18-years-in-prison-fo | 2025-06-26 | Ndubuisi Joseph Okafor, M.D. (sole practitioner and  | - | - | $213,174 | 216 | Drug_Prescriptions |
| remote-patient-monitoring-company-settles-fa | 2025-06-26 | Health Wealth Safe, Inc.; Dr. Subodh Agrawal (owner) | Medicare | - | $1,290,000 | - | Other - Unknown |
| lab-owner-marketing-company-owner-and-doctor | 2025-06-27 | Fadel Alshalabi (owner/CEO, Crestar Labs, LLC); Samu | Medicare;Medicaid | $129,000,000 | $495,000 | 60 | kickback_Bribery For Referral |
| 11-defendants-indicted-in-multi-billion-heal | 2025-06-30 | Imam Nakhmatullaev; Svjatoslav Jakovlev; Eric Juerge | Medicare; Medicare Supplemen | $10,600,000,000 | $27,700,000 | - | Phantom Claims |
| bensalem-woman-charged-in-home-care-fraud-ki | 2025-06-30 | Hemal Patel | Medicaid | $1,069,384 | - | - | Phantom Claims |
| canton-man-charged-in-national-health-care-f | 2025-06-30 | Krishna Gidwani (co-owner/operator of DME company);  | Medicare | $4,000,000 | - | - | Device, DME |
| district-of-arizona-charges-7-defendants-as- | 2025-06-30 | Farrukh Jarar Ali (owner of ProMD Solutions); Cle'Es | Medicare; Medicaid (Arizona  | $1,650,000,000 | $7,200,000 | - | FakeEncounter |
| federal-and-state-officials-announce-efforts | 2025-06-30 | Donald Calvin Saunders (organizer/leader); Vanessa R | South Carolina Medicaid; Nor | $21,000,000 | $5,135,000 | - | Phantom Claims |
| five-defendants-charged-for-their-roles-in-h | 2025-06-30 | Vincent Thayer (owner, Patient Payment Agent d/b/a M | Medicare; Medicaid (Medi-Cal | $242,005,233 | - | - | Phantom Claims |
| four-pensacola-women-charged-with-illegal-dr | 2025-06-30 | Lindsay N. McCray (also known as Lindsay Rogers) (em | - | - | - | - | Drug_Prescriptions |
| hendersonville-doctor-and-her-office-manager | 2025-06-30 | Xuhan Zhang a/k/a "Shelia Zhang" a/k/a "Xuhan Mei" ( | Medicare; Blue Cross Blue Sh | $20,000,000 | $6,000,000 | - | Phantom Claims |
| largest-ever-nationwide-healthcare-fraud-tak | 2025-06-30 | Andrew Voegel-Podadera (anesthesiology resident); Pi | Medicare; TRICARE | $500,000 | $1,115,976 | - | Drug_Prescriptions |
| lewiston-man-charged-with-identity-theft-and | 2025-06-30 | Joseph Dobie | Medicaid | - | - | - | IdentityFraud |
| multiple-eastern-north-carolina-healthcare-p | 2025-06-30 | Life Touch, LLC (North Carolina substance abuse trea | Medicaid (North Carolina Med | $64,000,000 | $6,000,000 | - | kickback_Bribery For Referral |
| national-health-care-fraud-enforcement-actio | 2025-06-30 | Usman Ahmad, R.Ph. (owner/operator, Detroit Hoover P | Medicare; Medicaid (Michigan | $6,000,000 | $6,000,000 | - | Drug_Prescriptions |
| national-health-care-fraud-takedown-results- | 2025-06-30 | 324 charged defendants nationwide, including 96 doct | Medicare;Medicare Advantage; | $14,600,000,000 | $34,300,000 | - | Phantom Claims |
| nearly-50-charged-in-southern-district-of-te | 2025-06-30 | Dera Ogudo (owner/operator, United Palliative & Hosp | Medicare; Medicaid (Texas);  | $360,000,000 | - | - | Drug_Prescriptions |
| nurse-practitioner-pleads-guilty-to-health-c | 2025-06-30 | Anja Salamack (psychiatric nurse practitioner) | Medicare | $163,640 | $352,510 | - | Phantom Claims |
| oklahoma-city-man-charged-with-medicare-frau | 2025-06-30 | Alexander Frank | Medicare | $3,200,000 | - | - | Phantom Claims |
| orange-county-man-charged-in-federal-complai | 2025-06-30 | Paul Richard Randall; Kyrollos Mekail; Patricia Ande | Medicaid (Medi-Cal) | $269,000,000 | - | - | Drug_Prescriptions |
| personal-health-care-aide-charged-with-healt | 2025-06-30 | Amstrong Chapajong (personal care aide and community | Medicaid (District of Columb | $461,369 | - | - | Phantom Claims |
| s-c-cases-among-hundreds-announced-in-nation | 2025-06-30 | Tina Marie Armstrong (owner, Safe at Home Medical Eq | Medicare; Medicaid; Veterans | $2,572,128 | - | - | Phantom Claims |
| three-west-tennessee-residents-charged-in-co | 2025-06-30 | Kossie Lamon Simmons (beneficial owner); Katina Marz | Federal Employees' Compensat | $28,738,532 | - | - | Phantom Claims |
| tulsa-doctor-charged-in-national-healthcare- | 2025-06-30 | Ladd Clayton Atkins (Doctor of Osteopathic Medicine) | Medicare; Medicaid | - | - | - | Drug_Prescriptions |
| two-men-charged-in-hiv-medication-fraud-and- | 2025-06-30 | Josue Torres; Anthony Guerra | Private health insurance (un | $2,638,581 | - | - | Drug_Prescriptions |
| u-s-attorney-039-s-office-participates-in-re | 2025-06-30 | Paulino Gonzalez (registered nurse); Mary Huntly (nu | Medicare | $108,333,550 | - | - | kickback_Bribery For Referral |
| u-s-attorney-erik-s-siebert-announces-charge | 2025-06-30 | Jawad Bhatti (pain management physician); Keri Ayres | Medicare; Virginia Medicaid; | $5,202,374 | - | - | Phantom Claims |
| u-s-attorneys-office-announces-charges-filed | 2025-06-30 | Terry Hill, Jr. (owner/operator of Recovery Street C | Medicaid (Ohio); Medicare | $4,000,000 | - | - | Benefit & Eligibility Fraud |
| u-s-attorneys-office-participates-in-record- | 2025-06-30 | Amstrong Chapajong (personal care aide and community | Medicaid (District of Columb | $882,154 | - | 24 | Phantom Claims |
| ambulance-company-and-its-owners-agree-to-pa | 2025-07-01 | Courtesy Transport Services, LLC; Melanie Burger (ow | Medicare; Medicaid (Florida) | - | $900,000 | - | FakeEncounter |
| centers-healthcare-pays-over-6-million-for-f | 2025-07-01 | Centers Healthcare (operator of 44 related skilled n | Medicare | - | $6,063,500 | - | Other - Unknown |
| doctor-arrested-for-multimillion-dollar-covi | 2025-07-01 | Ali Rashan (medical doctor, CEO and founder of Clear | Private insurance companies | $24,000,000 | - | - | Phantom Claims |
| durable-medical-equipment-owner-sentenced-to | 2025-07-01 | Peter Roussonicolos (silent-partner owner of five DM | Medicare | $61,500,000 | $23,709,580 | 144 | Device, DME |
| four-individuals-charged-in-northern-distric | 2025-07-01 | Demitrious Gilmore (owner of WM Wellness, LLC and Gi | Medicare; TRICARE; Departmen | $210,000,000 | - | - | Phantom Claims |
| national-health-care-fraud-takedown-results- | 2025-07-01 | Leland Roberts (co-owner, CEO and later consultant t | Medicare | $42,100,000 | - | - | kickback_Bribery For Referral |
| national-health-care-fraud-takedown-results- | 2025-07-01 | Ruknuddin "Rick" Charolia (call center operator, Hel | Medicare; Medicare Advantage | $1,830,000,000 | - | - | Phantom Claims |
| the-new-england-strike-force-joins-nationwid | 2025-07-01 | Erik Alonso (excluded social worker/psychotherapy pr | Medicaid (New Hampshire Medi | $14,000,000 | - | - | Device, DME |
| u-s-attorneys-office-announces-5-individuals | 2025-07-01 | Ashley Barnett (doctor of veterinary medicine); Laur | Medicaid | - | - | - | Drug_Prescriptions |
| u-s-attorneys-office-participates-in-nationa | 2025-07-01 | Riverpark Operations, LLC (operator of Avamere River | Medicare; Oregon Medicaid (O | - | $2,000,000 | - | FakeEncounter |
| bonita-man-pleads-guilty-in-5-8-million-medi | 2025-07-02 | Jacobo Melcer (owner/operator of two durable medical | Medicare | $5,885,382 | $3,479,303 | - | kickback_Bribery For Referral |
| doj-hhs-false-claims-act-working-group_d521f | 2025-07-02 | - | Medicare | - | - | - | Other - Unknown |
| pharmacy-owner-sentenced-to-87-months-in-pri | 2025-07-02 | Samuel "Sam" Khaimov (co-owner of Prime Aid Union Ci | Medicare; Medicaid; private  | $65,000,000 | - | 87 | Phantom Claims |
| tonawanda-doctor-pleads-guilty-for-his-role- | 2025-07-02 | William Stephan (medical doctor, family practice); E | Express Scripts, Inc.; unspe | $8,750,315 | - | - | Drug_Prescriptions |
| consulting-company-pays-more-than-450k-to-se | 2025-07-07 | Mercer (US), LLC (consulting company/government cont | TRICARE (Defense Health Agen | - | $456,796 | - | Upcoding |
| former-delaware-nurse-practitioner-resolves- | 2025-07-07 | Sandra Jackson (former Delaware nurse practitioner) | Medicare | $520,000 | - | - | Falsify certificate |
| kentucky-nurse-sentenced-to-prison-for-opioi | 2025-07-07 | Jacqueline Brewster (travel nurse at Raleigh General | - | - | - | 60 | Drug_Prescriptions |
| united-states-files-false-claim-act-complain | 2025-07-07 | Dr. Shayasta S. Mufti (physician) | Medicare | - | - | - | FakeEncounter |
| former-chief-operating-officer-of-pain-care- | 2025-07-08 | Jennifer Adams (Chief Operating Officer and practice | Medicaid (Virginia); commerc | - | - | 36 | Drug_Prescriptions |
| new-york-man-charged-with-wire-fraud-and-agg | 2025-07-08 | Humza Khan (financial interest holder in a Florida-b | - | $150,000 | - | - | IdentityFraud |
| two-california-residents-plead-guilty-in-con | 2025-07-08 | Karpis Srapyan; Susanna Harutyunyan; Petros Fichidzh | Medicare | $16,000,000 | - | 144 | Phantom Claims |
| department-of-justice-subpoenas-doctors-and- | 2025-07-09 | More than 20 unnamed doctors and clinics that perfor | - | - | - | - | Other - Unknown |
| brothers-from-india-sentenced-to-prison-for- | 2025-07-10 | Avanish Kumar Jha (co-owner, Dhrishti Pharma Interna | - | - | $100,000 | 30 | Drug_Prescriptions |
| ohio-doctor-pleads-guilty-to-role-in-telemed | 2025-07-10 | Mohammed Ahmad (licensed physician/telemedicine cont | Medicare | $267,402 | - | - | Falsify certificate |
| home-health-care-provider-to-pay-334-807-to- | 2025-07-11 | M&Y Care, LLC (home health care provider) | Medicare; Medicaid (Michigan | - | $334,807 | - | Upcoding |
| california-man-pleads-guilty-in-connection-w | 2025-07-14 | Juan Carlos Esparza (owner of House of Angels Hospic | Medicare | $16,000,000 | - | 144 | Phantom Claims |
| cape-coral-man-indicted-for-running-fraudule | 2025-07-15 | Eric Strom Holland (operator of unlicensed virtual p | - | $4,000,000 | - | - | Drug_Prescriptions |
| healthcare-worker-pleads-guilty-to-double-bi | 2025-07-15 | Amstrong Chapajong (personal care aide and community | Medicaid (District of Columb | $113,243 | $113,243 | - | Phantom Claims |
| law-enforcement-recovers-over-6-million-in-f | 2025-07-15 | Magaly Travieso (advanced practitioner registered nu | Medicare; Medicare Advantage | $20,000,000 | $6,000,000 | 108 | Falsify certificate |
| new-york-man-admits-health-care-fraud-scheme | 2025-07-15 | Thomas Conzo (owner and operator of Elite Pharmacy); | Medicare; Medicaid | - | - | - | Falsify certificate |
| urgent-care-operator-pays-3-million-dollars- | 2025-07-15 | Bloom Care LLC (urgent care operator); its owners | Medicare; Medicaid; Departme | - | $3,000,000 | - | Upcoding |
| florida-man-admits-role-in-4-8-million-healt | 2025-07-16 | Charles P. Kasbee, Jr. (marketer) | Medicare | $4,800,000 | - | - | kickback_Bribery For Referral |
| nevada-nurse-practitioner-pleads-guilty-to-f | 2025-07-16 | Mary Huntly (nurse practitioner, owner of wound care | Medicare | $14,333,550 | - | - | FakeEncounter |
| physician-assistant-who-pretended-to-be-a-li | 2025-07-17 | Raúl D. Villalobos-Meléndez (physician assistant pos | Medicare | - | - | - | Falsify certificate |
| rossi-sentenced-to-an-additional-three-years | 2025-07-17 | Aaron Rossi (owner/operator of Reditus Labs); Reditu | Medicare; State of Illinois; | $525,520 | $1,000,000 | 37 | Phantom Claims |
| united-states-and-the-states-of-georgia-colo | 2025-07-17 | Premier Medical, Inc. (clinical laboratory); Kevin S | Medicaid (Georgia Medicaid;  | $13,772,230 | $114,559,460 | - | kickback_Bribery For Referral |
| new-jersey-doctor-charged-with-distributing- | 2025-07-18 | Ritesh Kalra (internist/physician, owner of medical  | Medicaid (New Jersey Medicai | - | - | - | Drug_Prescriptions |
| eye-consultants-of-pennsylvania-pc-agrees-to | 2025-07-21 | Eye Consultants of Pennsylvania, PC (ECOP) (ophthalm | Medicare | - | $790,000 | - | Unbundling |
| united-states-reaches-501-556-civil-settleme | 2025-07-22 | Dr. Mohd Azfar Malik (psychiatrist, part-owner of Be | Medicare; Missouri Medicaid; | $250,778 | $501,556 | - | Phantom Claims |
| two-jonesborough-women-and-a-bristol-virgini | 2025-07-23 | Monika D. Schorer (VA Medical Center employee); Tere | U.S. Department of Veterans  | - | $852,598 | 12 | kickback_Bribery For Referral |
| alexandria-man-pleads-guilty-to-defrauding-p | 2025-07-24 | Muhammad Adil Quraish (former Air Force dentist); at | Small Business Administratio | $1,471,599 | - | - | Covid or General Loan Fraud |
| high-point-woman-sentenced-for-wire-fraud_ca | 2025-07-24 | Wendy Gibson-Fitzgerald | - | $466,777 | - | 87 | IdentityFraud |
| louisiana-nurse-practitioner-convicted-of-12 | 2025-07-24 | Scharmaine Lawson Baker (nurse practitioner, indepen | Medicare | $12,100,000 | - | - | FakeEncounter |
| florida-man-sentenced-to-more-than-17-years- | 2025-07-25 | Lino Mallari Gutierrez, a/k/a 'Joe Gutierrez' (licen | Medicare | $10,800,000 | $5,600,000 | 210 | Device, DME |
| fresno-man-sentenced-to-7-5-years-in-prison- | 2025-07-28 | Kelo White; Donald Ray Pierre; Ifeanyi Vincent Ntuko | - | - | - | 112 | Drug_Prescriptions |
| dermatology-providers-agree-to-pay-nearly-85 | 2025-07-30 | Forefront Dermatology S.C. (owner/operator of Hengho | Medicare | - | $847,394 | - | Upcoding |
| ceo-and-medical-director-charged-in-500m-cov | 2025-07-31 | Cemhan "Jimmy" Biricik (sole member and CEO of Fast  | Medicare; Medicaid; TRICARE; | $500,000,000 | - | - | Phantom Claims |
| florida-woman-to-pay-400-000-to-settle-alleg | 2025-07-31 | Georgina Exposito (owner of 3rd Party Services of Fl | Medicare; TRICARE | - | $400,000 | - | Falsify certificate |
| greensboro-woman-sentenced-in-conviction-wit | 2025-07-31 | Jasmine Hoyle (owner/operator of Harvest Focused & C | Medicaid (North Carolina) | $6,299,738 | $6,299,738 | 44 | Phantom Claims |
| canton-man-pleads-guilty-to-multi-million-do | 2025-08-05 | Krishna Gidwani (DME company owner/operator); Raju S | Medicare | $4,000,000 | - | - | Device, DME |
| glendale-woman-sentenced-to-9-years-in-feder | 2025-08-05 | Nita Almuete Paddit Palma (concealed owner of Magnol | Medicare | $10,600,000 | $8,270,032 | 108 | kickback_Bribery For Referral |
| putnam-county-veterinarian-ordered-to-pay-95 | 2025-08-05 | Clara Ann Mason (veterinarian, DEA-registered practi | - | - | $956,709 | - | Drug_Prescriptions |
| aprn-and-medical-practice-to-pay-over-600k-a | 2025-08-06 | Armand Ntchana (APRN, owner); Integrated Procare Ser | Medicare; Connecticut Medica | - | $614,427 | - | Phantom Claims |
| brooklyn-woman-pleads-guilty-to-leading-a-68 | 2025-08-06 | Zakia Khan (owner of Happy Family Social Adult Day C | Medicaid | $68,000,000 | $5,000,000 | - | kickback_Bribery For Referral |
| justice-department-files-two-civil-forfeitur | 2025-08-06 | Vida Med Center LLC (purported DME company); Med-Uni | Medicare | $33,155,336 | $10,982,085 | - | Device, DME |
| leader-of-68m-adult-day-care-fraud-scheme-pl | 2025-08-06 | Zakia Khan (owner of Happy Family Social Adult Day C | Medicaid | $68,000,000 | $5,000,000 | - | kickback_Bribery For Referral |
| ceo-of-spine-device-company-sentenced-for-fa | 2025-08-07 | Dr. Kingsley R. Chin (Founder, President and CEO of  | Medicare | $4,750 | $904,500 | - | kickback_Bribery For Referral |
| illinois-man-charged-in-durable-medical-equi | 2025-08-07 | Kartik Bhatia (DME company owner/operator); Raju Sha | Medicare | $2,000,000 | - | - | Device, DME |
| allentown-area-pharmacy-and-its-owner-agree- | 2025-08-08 | West End Services, Inc. (pharmacy); Christopher Leon | Medicare | - | $825,000 | - | Phantom Claims |
| houston-doctor-agrees-to-pay-over-2-million- | 2025-08-11 | Dr. Ajay Aggarwal (anesthesiologist and pain medicin | Medicare; U.S. Department of | - | $2,053,515 | - | Upcoding |
| richmond-psychotherapist-convicted-of-health | 2025-08-11 | Daniel Jacobsen (Licensed Clinical Social Worker/psy | Medicaid (Virginia Medicaid) | $335,824 | $1,201,174 | 3 | Phantom Claims |
| united-states-obtains-more-than-1-4-million- | 2025-08-11 | Dr. Richard Akoto, M.D. (family medical doctor); Ric | Medicare | - | $1,407,493 | - | Upcoding |
| superseding-indictment-against-pittsburgh-he | 2025-08-12 | Kelley Oliver-Hollis (owner of SerenityCare LLC); Se | Medicaid (Pennsylvania Medic | - | - | - | Upcoding |
| connecticut-lab-its-owners-and-officers-to-p | 2025-08-13 | Genco Lab, LLC (reference laboratory); Paul Conroy ( | Medicare; Medicaid (Connecti | - | $1,255,825 | - | FakeEncounter |
| baltimore-county-woman-admits-to-impersonati | 2025-08-14 | Thomasina E. Amponsah (unlicensed individual posing  | Medicare; Medicaid | $100,000 | - | 38 | IdentityFraud |
| four-men-including-two-doctors-charged-in-a- | 2025-08-14 | Dr. Shakeeb Chinoy (physician); Dr. Sunil Manjila-Va | Medicare; Medicaid | $7,000,000 | - | - | Drug_Prescriptions |
| marshalltown-woman-sentenced-to-six-months-i | 2025-08-14 | Amanda Nicole Manatt (registered nurse) | - | - | $11,058 | 6 | Drug_Prescriptions |
| arizona-ceo-indicted-for-embezzling-over-2-4 | 2025-08-15 | James Vincent Campbell (CEO and founder of Axim Frin | - | $2,486,905 | - | - | Other - Unknown |
| oklahoma-city-woman-pleads-guilty-to-health- | 2025-08-15 | Natasha Allmon (behavioral health counselor) | Blue Cross Blue Shield | $1,400,000 | - | - | Phantom Claims |
| three-indicted-in-multi-state-prescription-f | 2025-08-15 | Ciera Washington; Raven White; Bryan Otero | Medicaid (New York) | - | - | - | Drug_Prescriptions |
| alabama-doctor-charged-with-6-million-teleme | 2025-08-18 | Tommie Robinson (physician) | Medicare | $6,000,000 | - | - | Falsify certificate |
| florida-man-pleads-guilty-for-role-in-an-off | 2025-08-18 | Alexis Garcia (manager/director of Tape Drywall Serv | IRS (United States); workers | $4,200,000 | - | - | Tax, Payroll or Coupon Fraud |
| california-behavioral-medicine-provider-agre | 2025-08-19 | American Psychiatric Centers, Inc., d/b/a Comprehens | Medicare; Medicaid (Medi-Cal | - | $2,750,000 | - | Phantom Claims |
| lackawanna-man-sentenced-for-defrauding-medi | 2025-08-19 | Munef Fadhel (owner, Great Lake Transportation, Inc. | Medicaid | $95,000 | - | - | Upcoding |
| illinois-doctor-sentenced-to-34-months-in-pr | 2025-08-20 | Krishnaswami Sriram (doctor) | Medicare | $1,600,000 | $1,700,000 | 34 | Phantom Claims |
| philadelphia-man-sentenced-to-over-two-years | 2025-08-20 | James Sessoms | Medicaid (Pennsylvania Depar | $1,063,633 | $398,708 | 28 | Benefit & Eligibility Fraud |
| troy-health-inc-enters-non-prosecution-agree | 2025-08-20 | Troy Health, Inc. (Medicare Advantage, Part D, and D | Medicare | - | $1,430,008 | - | Benefit & Eligibility Fraud |
| brooklyn-cardiologist-sentenced-to-37-months | 2025-08-21 | Niranjan Mittal (cardiologist, operator of Brooklyn  | Medicare; Medicaid | $40,000,000 | - | 37 | kickback_Bribery For Referral |
| roofing-contractor-admits-tax-evasion-scheme | 2025-08-21 | Anthony Delmaro (owner of Kings Roofing commercial r | Medicaid (Connecticut Husky  | $500,000 | $1,707,928 | - | Tax, Payroll or Coupon Fraud |
| three-baton-rouge-individuals-sentenced-to-f | 2025-08-21 | Kevan Andre Hills; Devin Tyrone Stampley, Jr.; Asia  | Medicaid; Paycheck Protectio | $419,476 | - | 104 | Drug_Prescriptions |
| mississippi-medicaid-recipients-agree-to-pay | 2025-08-22 | Rajwinder Kaur; Kawaldeep Singh; Narinder Kaur; Prab | Medicaid (Mississippi Divisi | - | $173,627 | - | Benefit & Eligibility Fraud |
| united-states-attorneys-office-in-chicago-cr | 2025-08-22 | - | - | - | - | - | Other - Unknown |
| compliance-director-and-office-manager-of-su | 2025-08-25 | Keke Komeko Johnson (Compliance Director, Life Touch | Medicaid | $1,000,000 | - | - | kickback_Bribery For Referral |
| three-defendants-plead-guilty-in-multi-milli | 2025-08-26 | Rita Shaba; Samer Kammo; Christina Anasi | - | $3,000,000 | $2,100,000 | - | Covid or General Loan Fraud |
| danville-woman-sentenced-for-health-care-fra | 2025-08-27 | Jacquelyn Farrish (Medicaid Consumer Directed Care r | Medicaid (Virginia Medicaid) | $116,536 | $116,536 | - | Phantom Claims |
| louisville-physician-agrees-to-pay-250-000-t | 2025-08-27 | Dr. James Charasika (physician); Louisville Patient  | Medicare; Medicaid (Kentucky | - | $250,000 | - | Upcoding |
| maryland-woman-pleads-guilty-to-conspiracy-t | 2025-08-27 | Carolyn Bryant-Taylor (former director and corporate | Medicaid (Virginia Medicaid) | - | - | - | Phantom Claims |
| former-battle-creek-doctor-to-pay-over-700-0 | 2025-08-28 | Shekhar Thakur (physician, owner of Parkside Medical | - | - | $705,075 | - | Drug_Prescriptions |
| home-health-agency-owner-sentenced-to-more-t | 2025-08-28 | Paul Njoku (owner and CEO of Opnet Health Care Servi | Medicare | $400,000 | - | 75 | Falsify certificate |
| blood-test-lab-owner-pleads-guilty-to-evadin | 2025-08-29 | Armen Muradyan (owner/operator of Genex Laboratories | Medicare | $11,236,357 | - | - | Benefit & Eligibility Fraud |
| departments-of-justice-and-homeland-security | 2025-08-29 | - | - | - | - | - | Other - Unknown |
| middletown-resident-charged-in-health-care-f | 2025-08-29 | Habroon Habib (owner/formed company); Around the Wor | Medicare (Medicare Advantage | $680,000 | - | - | Phantom Claims |
| owner-of-california-blood-testing-laboratory | 2025-08-29 | Armen Muradyan (owner/operator of Genex Laboratories | Medicare | $23,000,000 | - | - | Benefit & Eligibility Fraud |
| martinsville-doctor-sentenced-to-40-years-fo | 2025-09-02 | Joel Smithers (physician) | - | - | - | 480 | Drug_Prescriptions |
| united-states-intervenes-and-sues-promedica- | 2025-09-02 | ProMedica Health System, Inc. (owner/operator); HCR  | Medicare; Medicaid | - | - | - | FakeEncounter |
| couple-charged-in-cross-border-identity-thef | 2025-09-03 | Luis Enrique Villegas Brownell; Kassandra Sanchez | Medicaid (California Medi-Ca | - | - | - | IdentityFraud |
| former-chief-financial-officer-sentenced-to- | 2025-09-03 | Pamela J. Kahut (Chief Financial Officer, Pacific St | Pacific States Marine Fisher | $211,083 | $221,083 | 8 | Other - Embezzlement of federa |
| caregiver-who-abused-vulnerable-adult-in-his | 2025-09-04 | Fouodzing Mbord (home health aide/caregiver) | - | - | - | - | Other - Unknown |
| maryland-man-pleads-guilty-to-leading-sophis | 2025-09-05 | Benjamin Jamal Washington (scheme leader) | - | - | - | - | Drug_Prescriptions |
| laboratory-ceo-marketers-and-physicians-to-p | 2025-09-08 | Christopher Grottenthaler (former CEO, True Health D | Medicare; Medicaid; TRICARE | - | $6,068,462 | - | kickback_Bribery For Referral |
| owner-of-facility-for-intellectually-disable | 2025-09-08 | Kelley Oliver-Hollis (owner, Serenitycare LLC) | Medicaid (Pennsylvania Home  | - | - | - | Falsify certificate |
| owners-of-1st-adult-n-pediatric-healthcare-p | 2025-09-08 | Kafomdi "Josephine" Okocha (co-owner, 1st Adult N Pe | Medicaid (Virginia Medicaid) | $10,000,000 | - | - | Phantom Claims |
| st-louis-area-doctor-sentenced-to-70-months- | 2025-09-08 | Dr. Asim Muhammad Ali (physician, owner of Central D | Medicare; Missouri Medicaid; | - | $1,889,260 | 70 | kickback_Bribery For Referral |
| florida-man-sentenced-to-24-months-for-laund | 2025-09-10 | Thomas Farese (investor in DME supply company); Aaro | Medicare; other insurance pr | - | $1,809,000 | 24 | Wire Fraud |
| fraudster-who-submitted-over-340-000-in-fake | 2025-09-10 | Shontavia Riddick | North Carolina Department of | $340,000 | - | - | Covid or General Loan Fraud |
| maryland-woman-arraigned-for-defrauding-the- | 2025-09-10 | Jariatu Jalloh (community support worker employed by | Medicaid (District of Columb | $234,500 | - | - | Phantom Claims |
| clay-county-pharmacy-investigation-and-prose | 2025-09-11 | Thomas K. Weir (majority owner, Oakley Pharmacy d/b/ | Medicare Part D; Medicaid (T | - | $1,419,974 | - | Drug_Prescriptions |
| media-advisory-chesapeake-regional-medical-c | 2025-09-11 | Chesapeake Regional Medical Center (aka Chesapeake G | Medicaid; health care benefi | $18,500,000 | - | - | FakeEncounter |
| texas-resident-sentenced-for-conspiring-to-d | 2025-09-11 | Nnamdi Felix Udeagha | Chickasaw Nation Department  | $214,908 | $214,908 | 27 | Wire Fraud |
| cheyenne-couple-sentenced-in-fraud-case_b740 | 2025-09-12 | Sean P. Madigan (coffee shop operator); Victoria Mad | - | $300,000 | $174,039 | - | Covid or General Loan Fraud |
| former-home-health-care-operator-settles-fra | 2025-09-12 | Irene Oluwatoyin Oshiyoye (operator); Dr. Adekunle O | Medicare; Medicaid (Michigan | - | $250,000 | - | FakeEncounter |
| louisiana-chiropractor-sentenced-to-seven-ye | 2025-09-12 | Dr. Benjamin Tekippe (chiropractor and owner of Meta | Blue Cross Blue Shield of Lo | $2,300,000 | $753,794 | 84 | Phantom Claims |
| seven-arrested-for-conspiring-with-annandale | 2025-09-12 | Rotimi Iluyomade (Annandale-based doctor); Obioma Al | - | - | - | - | Drug_Prescriptions |
| federal-jury-finds-former-prenatal-care-coor | 2025-09-15 | Precious Cruse (owner and operator of Caring Through | Medicaid | - | - | - | Phantom Claims |
| fraud-charges-filed-against-12-defendants-in | 2025-09-15 | Herline Lochard (registered agent/manager, Center fo | - | - | - | 13 | Falsify certificate |
| aiken-men-sentenced-to-federal-prison-for-de | 2025-09-16 | Cody Lee Anderson (designated personal representativ | - | $20,000,000 | - | 24 | Other - Unknown |
| exactech-agrees-to-pay-8-million-to-resolve- | 2025-09-16 | Exactech Inc. (medical device manufacturer, Gainesvi | Medicare; Medicaid; U.S. Dep | - | $8,000,000 | - | Device, DME |
| georgia-man-sentenced-to-over-4-years-in-pri | 2025-09-16 | Kenneth Terrell Harrison (owner); Aurtism, LLC (outp | Medicaid (Arizona Health Car | $6,538,485 | $6,538,485 | 52 | Phantom Claims |
| henderson-man-indicted-for-illegal-smuggling | 2025-09-16 | David Ralph Webber (owner/operator of Passion Plus E | - | $2,500,000 | - | - | Drug_Prescriptions |
| medical-device-company-exactech-inc-agrees-t | 2025-09-16 | Exactech, Inc. (medical device manufacturer, Gainesv | Medicare; Medicaid; U.S. Dep | - | $8,000,000 | - | Device, DME |
| roanoke-home-health-care-attendant-pleads-gu | 2025-09-16 | Vicki Lynn Dowdy (home health attendant) | Medicaid (Virginia Medicaid) | $24,760 | $24,760 | - | Phantom Claims |
| suburban-chicago-man-indicted-on-federal-hea | 2025-09-16 | Shawn Bashir (creator of Success for Kids and Growin | Private insurer (unnamed) | $17,300,000 | - | - | Phantom Claims |
| three-more-plead-guilty-in-1st-adult-n-pedia | 2025-09-16 | 1st Adult N Pediatric Healthcare Service (Medicaid-e | Medicaid (Virginia Medicaid) | - | - | - | Phantom Claims |
| u-s-attorney-039-s-office-collects-48-millio | 2025-09-16 | Insys Therapeutics, Inc.; John N. Kapoor (founder an | Medicare; private insurance  | - | $48,344,036 | - | kickback_Bribery For Referral |
| former-waterbury-resident-sentenced-to-41-mo | 2025-09-17 | Marlenin Vito (Medicaid Coordinator at a Stamford as | - | $361,557 | - | 41 | Wire Fraud |
| minnesota-woman-pleads-guilty-in-2-million-c | 2025-09-17 | Tammy Wadsworth (founder and owner of Pain, Injury a | - | $2,000,000 | - | - | Device, DME |
| owner-of-new-jersey-businesses-sentenced-to- | 2025-09-17 | Daniel Dadoun (owner of several New Jersey businesse | - | $3,200,000 | $3,239,773 | 41 | Covid or General Loan Fraud |
| president-of-queens-based-construction-compa | 2025-09-17 | Liaquat Cheema (President of AFL Construction Co. In | Medicaid (New York); New Yor | $12,000,000 | $3,267,811 | 48 | Wire Fraud |
| two-florida-men-charged-for-34-8m-fraud-sche | 2025-09-17 | Kenneth Charles Kessler III (owner/operator of DME s | Medicare | $34,800,000 | - | - | Device, DME |
| u-s-attorneys-office-seeks-potential-victims | 2025-09-17 | David A. Parks (physician); James M. Bilderback (cli | Medicare; Missouri Medicaid; | - | - | - | Drug_Prescriptions |
| united-states-files-lawsuit-against-san-bern | 2025-09-17 | Local Initiative Health Authority for Inland Empire  | Medicaid (Medi-Cal, Californ | - | - | - | Retention of Overpayment |
| united-states-files-suit-against-california- | 2025-09-17 | Local Initiative Health Authority for Inland Empire  | Medicaid (Medi-Cal, Californ | - | - | - | Retention of Overpayment |
| defendants-charged-in-first-wave-of-housing- | 2025-09-18 | Moktar Hassan Aden (owner, Brilliant Minds Services  | Medicaid (Minnesota Housing  | $8,400,000 | - | - | Phantom Claims |
| government-contractor-to-pay-over-4-million- | 2025-09-18 | Bayonne Drydock and Repair Corporation (government c | U.S. Navy (Department of Def | - | $4,043,810 | - | Other - Unknown |
| marketer-sentenced-for-11-5m-genetic-testing | 2025-09-19 | Robert Desselle (marketer) | Medicare | $11,500,000 | $6,600,000 | 57 | kickback_Bribery For Referral |
| bergen-county-company-settles-matter-allegin | 2025-09-22 | Ulma Form Works, Inc. (manufacturer and supplier of  | Small Business Administratio | $2,000,000 | $2,902,795 | - | Covid or General Loan Fraud |
| fresno-county-podiatrist-and-sales-represent | 2025-09-22 | Felipe Ruiz (podiatrist, West Coast Podiatry Inc.);  | Medicare; Medi-Cal (Californ | $3,200,000 | - | 63 | FakeEncounter |
| owner-of-kansas-city-kansas-pharmacy-agrees- | 2025-09-22 | Daniel Reif, Inc., d/b/a The Medicine Shoppe (retail | - | - | $200,000 | - | Drug_Prescriptions |
| justice-department-expands-health-care-fraud | 2025-09-23 | - | Medicare; Medicaid (Massachu | - | - | - | Other - Unknown |
| morris-county-individual-and-ocean-county-in | 2025-09-23 | Michael Kiszka; Gregory Kubina | - | - | - | - | Drug_Prescriptions |
| physician-sentenced-to-14-years-for-illegal- | 2025-09-23 | Neil K. Anand, M.D. (physician, owner of in-house ph | Medicare; U.S. Office of Per | $2,400,000 | $4,000,000 | 168 | Drug_Prescriptions |
| first-defendant-charged-in-autism-fraud-sche | 2025-09-24 | Asha Farhan Hassan (owner, Smart Therapy LLC); Smart | Minnesota Medicaid (Minnesot | $14,465,000 | - | - | FakeEncounter |
| reno-doctor-arrested-and-indicted-for-health | 2025-09-24 | Dr. Samuel R. Chacon (OB-GYN, owner of Women's Healt | Medicaid; Anthem Blue Cross  | - | - | - | FakeEncounter |
| southfield-doctor-sentenced-to-six-years-in- | 2025-09-24 | Charise Valentine (doctor); Michele Ritter (doctor,  | - | $5,200,000 | - | 72 | Drug_Prescriptions |
| tri-cities-urgent-care-clinic-agrees-to-pay- | 2025-09-24 | Health First Urgent Care (urgent care clinic, Richla | Medicare; Medicaid (Washingt | - | $2,807,729 | - | Unbundling |
| pharmacy-owner-and-pharmacists-sentenced-for | 2025-09-25 | Arthur Billings (owner, operator and pharmacist-in-c | - | - | $2,733,931 | 144 | Drug_Prescriptions |
| st-charles-parish-woman-charged-with-wire-fr | 2025-09-25 | Ashley Hymel (executive assistant at Company 1) | - | $130,664 | - | - | Wire Fraud |
| former-department-of-justice-prosecutor-and- | 2025-09-26 | Carlos A. Lopez (former DOJ Trial Attorney/federal p | - | - | - | - | Other - Unknown |
| owner-of-mail-order-pharmacies-settles-false | 2025-09-26 | Andrew Do (owner and operator of three mail-order ph | Medicare | - | $600,000 | - | kickback_Bribery For Referral |
| semler-scientific-inc-and-bard-peripheral-va | 2025-09-26 | Semler Scientific Inc. (device manufacturer); Bard P | Medicare | - | $36,950,000 | - | Device, DME |
| long-term-international-investigation-into-c | 2025-09-30 | Eric Ndungu Mwangi (Kenyan national, owner of Linear | U.S. Agency for Internationa | $177,000 | $84,000 | - | Other - Embezzlement of federa |
| newburgh-woman-who-made-headlines-for-false- | 2025-09-30 | Sharon Toney-Finch (founder of the Yerik Israel Tone | - | $85,000 | $169,000 | 12 | Wire Fraud |
| clinic-owner-arrested-in-multimillion-dollar | 2025-10-01 | Dempsey Spears (owner of Transitional Life Counselin | Medicare | $4,000,000 | - | - | Phantom Claims |
| charles-neil-floyd-appointed-interim-u-s-att | 2025-10-06 | - | - | - | - | - | Other - Unknown |
| compounding-pharmacy-owner-sent-back-to-pris | 2025-10-14 | Christopher R. Parks (compounding pharmacy owner) | - | - | $6,400,000 | 18 | kickback_Bribery For Referral |
| plasters-union-member-sentenced-for-defraudi | 2025-10-14 | Toby Weatherbee (member of Plasterer's Local Union # | Plaster's Local Union #9 hea | $44,012 | $44,012 | - | Phantom Claims |
| bucks-county-home-care-company-and-its-owner | 2025-10-16 | Favorite Home Care, LLC; Larry Sakson (co-owner); Ol | Medicaid (Pennsylvania); Med | - | - | - | Phantom Claims |
| covid-scammer-sentenced-for-defrauding-inves | 2025-10-16 | Robert Maxwell (promoter/investment solicitor) | - | $12,500,000 | - | 90 | Wire Fraud |
| four-more-charged-in-110-million-hospice-fra | 2025-10-21 | Dera Ogudo (operator of United Palliative & Hospice  | Medicare; Medicaid (Texas) | $110,000,000 | - | - | FakeEncounter |
| repeat-offender-pleads-guilty-to-health-care | 2025-10-23 | Erik X. Alonso (psychotherapist, excluded provider) | Medicaid (New Hampshire Medi | $173,998 | - | - | Benefit & Eligibility Fraud |
| new-united-states-attorney-for-the-middle-di | 2025-10-27 | - | - | - | - | - | Other - Unknown |
| federal-grand-jury-returns-second-supersedin | 2025-11-03 | Sanjeev Kumar (gynecologist) | Medicare; Medicaid | - | - | - | FakeEncounter |
| business-owner-sentenced-to-more-than-five-y | 2025-11-06 | Zaven Yeghiazaryan (business owner) | Medicaid | - | $269,505 | 64 | Covid or General Loan Fraud |
| alabama-doctor-pleads-guilty-to-6-million-te | 2025-11-13 | Tommie Robinson (physician) | Medicare | $6,000,000 | - | - | Falsify certificate |
| baltimore-county-woman-sentenced-for-imperso | 2025-11-13 | Thomasina E. Amponsah (unlicensed individual posing  | Medicare; Medicaid | $145,000 | - | 38 | IdentityFraud |
| diagnostic-laboratory-agrees-to-pay-more-tha | 2025-11-13 | Patients Choice Laboratories (PCL) (diagnostic labor | Medicare | $6,000,000 | $9,620,000 | - | kickback_Bribery For Referral |
| east-granby-woman-who-stole-in-1-1-million-p | 2025-11-13 | Karen Gaston (controlled LNK, Elegant Clinical, Ruby | U.S. Small Business Administ | $1,163,910 | $39,522 | - | Covid or General Loan Fraud |
| former-virginia-business-owner-sentenced-for | 2025-11-13 | Richard Moore (executive vice president and part own | IRS (United States) | $3,100,000 | $3,023,984 | 80 | Tax, Payroll or Coupon Fraud |
| iowa-attorney-pleads-guilty-to-making-a-fals | 2025-11-13 | Timothy Mark Anderson (Iowa licensed attorney provid | Medicaid (Iowa Medicaid) | - | - | - | Benefit & Eligibility Fraud |
| telemarketing-company-operators-sentenced-fo | 2025-11-13 | Paul Wexler (operator of telemarketing company); Pau | Medicare | $20,312,156 | $8,516,106 | 48 | kickback_Bribery For Referral |
| three-leaders-of-primary-health-network-plea | 2025-11-14 | Drew Pierce (former CEO of Primary Health Network);  | - | $1,700,000 | - | - | Wire Fraud |
| vra-enterprises-agrees-to-pay-over-17-millio | 2025-11-14 | VRA Enterprises, LLC dba Precision Rx (pharmacy) | Medicare | - | $17,069,371 | - | Phantom Claims |
| aesculap-implant-systems-agrees-to-pay-38-5- | 2025-11-17 | Aesculap Implant Systems, LLC (medical device compan | Medicare; Medicaid | - | $38,500,000 | - | Device, DME |
| aesculap-implant-systems-agrees-to-pay-38-5m | 2025-11-17 | Aesculap Implant Systems LLC (medical device manufac | Medicare; Medicaid | - | $38,500,000 | - | Device, DME |
| coeur-dalene-physician-found-guilty-in-telem | 2025-11-17 | Dr. David Antonio Becerril (licensed Washington phys | Medicare | $3,200,000 | - | 168 | Falsify certificate |
| cvs-pharmacy-inc-pays-18-2-million-to-resolv | 2025-11-17 | CVS Pharmacy Inc. (pharmacy chain) | Medicaid (California Medi-Ca | - | $18,282,280 | - | Falsify certificate |
| department-of-justice-releases-2025-annual-r | 2025-11-17 | More than 600 unnamed defendants in over 280 enforce | Medicare; Medicaid | $2,000,000,000 | - | - | Other - Unknown |
| four-pensacola-women-plead-guilty-to-illegal | 2025-11-17 | Lindsay N. McCray (also known as Lindsay Rogers) (me | - | - | - | - | Drug_Prescriptions |
| oncologist-sentenced-to-prison-for-illegally | 2025-11-17 | Dr. Naveed Aslam (licensed oncologist); Somerset Hem | - | $17,000,000 | $2,600,000 | 18 | Drug_Prescriptions |
| owners-and-ceo-of-wholesale-pharmaceutical-c | 2025-11-17 | Patrick Boyd (co-owner, Safe Chain Solutions); Charl | - | $92,000,000 | - | - | Drug_Prescriptions |
| president-of-insurance-brokerage-firm-and-ce | 2025-11-17 | Cory Lloyd (president of insurance brokerage firm);  | Affordable Care Act federal  | $233,000,000 | - | - | Benefit & Eligibility Fraud |
| tri-cities-urgent-care-clinic-agrees-to-pay- | 2025-11-17 | Health First Urgent Care (urgent care clinic, Richla | Medicare; Medicaid (Washingt | - | $2,807,729 | - | Unbundling |
| amidst-the-government-shutdown-the-united-st | 2025-11-18 | Dr. David Antonio Becerril (licensed Washington phys | Medicare; Medicaid (Washingt | $3,200,000 | $2,807,729 | - | Phantom Claims |
| anchorage-doctor-and-husband-plead-guilty-to | 2025-11-18 | Dr. Claribel Tan (rheumatologist, clinic owner/opera | More than 10 health insuranc | $12,522,446 | $18,627,099 | 78 | Phantom Claims |
| corporation-and-former-chief-executive-offic | 2025-11-18 | KBWB Operations LLC, d/b/a Atrium Health and Senior  | Medicare; Medicaid (Wisconsi | $146,000,000 | $154,400,000 | 90 | Wire Fraud |
| florida-man-indicted-for-health-care-fraud-w | 2025-11-18 | Mark Weinberger (beneficial owner and/or managing em | Medicare | $6,700,000 | - | - | Device, DME |
| four-california-residents-sentenced-to-priso | 2025-11-18 | Juan Carlos Esparza (owner of House of Angels Hospic | Medicare | $16,000,000 | $29,660,755 | 144 | Phantom Claims |
| memphis-doctor-to-pay-375-296-90-to-settle-f | 2025-11-18 | Dr. Mark Shermer (Memphis nephrologist) | Medicare | - | $375,297 | - | Phantom Claims |
| u-s-attorney-jason-a-reding-quinones-swears- | 2025-11-18 | - | - | - | - | - | Other - Unknown |
| california-company-and-three-employees-sente | 2025-11-19 | Advoque Safeguard LLC (mask manufacturer); Jason Aze | - | - | $1,031,500 | - | Device, DME |
| connecticut-dentists-pay-more-than-714k-to-s | 2025-11-19 | Dent Plus Family Dentistry, PLLC (dissolved dental p | Medicaid (Connecticut Medica | - | $714,446 | - | kickback_Bribery For Referral |
| federal-law-enforcement-highlight-continuity | 2025-11-19 | - | - | - | $9,600,000 | - | kickback_Bribery For Referral |
| founder-ceo-and-clinical-president-of-digita | 2025-11-19 | Ruthia He (founder and CEO of Done); David Brody (cl | Medicare; Medicaid; commerci | $100,000,000 | - | - | Drug_Prescriptions |
| justice-department-secures-denaturalization- | 2025-11-19 | Marieva Briceno (owner of three purported medical cl | Medicare | $5,460,323 | - | 60 | FakeEncounter |
| little-rock-psychologist-indicted-by-federal | 2025-11-19 | Krameelah Banks (psychologist, owner and operator of | Medicare; Arkansas Blue Cros | $500,000 | - | - | Phantom Claims |
| missouri-man-sentenced-to-10-years-in-prison | 2025-11-19 | Jamie P. McNamara (operator/owner of laboratories) | Medicare | $174,000,000 | $62,000,000 | 120 | kickback_Bribery For Referral |
| naples-man-sentenced-to-federal-prison-for-c | 2025-11-19 | Alexis Garcia (manager/director of operations, Tape  | - | $4,200,000 | $4,262,797 | 30 | Tax, Payroll or Coupon Fraud |
| diagnostic-laboratory-agrees-to-pay-more-tha | 2025-11-20 | Genetic Technological Innovations, LLC (GTI) (diagno | Medicare | - | $1,635,000 | - | kickback_Bribery For Referral |
| justice-department-secures-denaturalization- | 2025-11-20 | Marieva Briceno (owner of three purported medical cl | Medicare | $5,460,323 | - | 60 | FakeEncounter |
| mississippi-businessman-pleads-guilty-to-19m | 2025-11-20 | Willie De Gibbs (owner/beneficial owner of seven DME | Medicare | $19,000,000 | - | - | Device, DME |
| physician-convicted-of-conspiracy-to-defraud | 2025-11-20 | Dr. Marion Lee (co-owner and medical advisor, Luminu | Medicare | $24,000,000 | $4,000,000 | - | kickback_Bribery For Referral |
| texas-businessman-admits-1-9-million-covid-t | 2025-11-20 | Rashid Naqvi (owner/operator of Elite Diagnostics In | Medicare | $1,974,479 | - | - | Phantom Claims |
| arizona-ceo-sentenced-to-14-years-in-prison- | 2025-11-21 | Kevin Lamorris McKenzie (Chief Operating Officer the | - | $33,155,701 | $33,210,701 | 168 | Wire Fraud |
| federal-jury-finds-markita-barnes-guilty-of- | 2025-11-21 | Markita Barnes (owner and operator of Here for You,  | Medicaid | - | - | - | Phantom Claims |
| pharmacist-and-brother-sentenced-to-prison-f | 2025-11-21 | Raad Kouza (pharmacist, pharmacy owner); Ramis Kouza | Medicare; Medicaid; Blue Cro | $15,000,000 | $31,000,000 | 96 | Phantom Claims |
| u-k-citizen-indicted-for-2-7m-telehealth-sch | 2025-11-21 | Marek Rex Vernon Harrison (true beneficial owner and | Medicare | $2,700,000 | - | - | FakeEncounter |
| u-s-attorney-zachary-a-keller-highlights-a-d | 2025-11-21 | Michael L. Riggins | Medicare | $3,800,000 | $1,800,000 | 57 | Device, DME |
| vohra-wound-physicians-and-its-owner-agree-t | 2025-11-21 | Dr. Ameet Vohra (owner); Vohra Wound Physicians Mana | Medicare | - | $45,000,000 | - | Upcoding |
| chicago-chiropractor-sentenced-to-nearly-six | 2025-11-24 | Clarence W. Brown III (chiropractor, owner of Dr. CB | Blue Cross Blue Shield of Il | $2,100,000 | $2,088,884 | 70 | Phantom Claims |
| group-of-pennsylvania-based-car-companies-se | 2025-11-24 | Fred Beans Holdings, Inc.; Auto Express Enterprises, | - | $4,866,975 | $1,427,869 | - | Covid or General Loan Fraud |
| indiana-laboratory-company-agrees-to-pay-mor | 2025-11-24 | Patients Choice Laboratories (PCL) (diagnostic labor | Medicare | $6,000,000 | $9,620,000 | - | kickback_Bribery For Referral |
| michigan-pharmacist-sentenced-to-46-months-i | 2025-11-24 | Nabil Fakih (pharmacist, pharmacy owner/operator) | Medicare | $4,000,000 | $4,726,364 | 46 | Phantom Claims |
| missouri-home-health-care-company-agrees-to- | 2025-11-24 | Deer Valley Home Health Services LLC (DVHH) (home he | Medicaid (Missouri) | $534,475 | $534,475 | - | Falsify certificate |
| new-jersey-man-charged-with-using-fraudulent | 2025-11-24 | Mohammad Abuhadba (promoter/co-owner of vaping compa | - | - | - | - | Wire Fraud |
| new-jersey-pharmacy-owner-pleads-guilty-to-h | 2025-11-24 | Nestor E. Jaime (pharmacy owner) | Medicare | $2,500,000 | - | - | Phantom Claims |
| southern-colorado-hospital-and-doctors-agree | 2025-11-24 | Mt. San Rafael Hospital and Rural Health Clinic; Dr. | Medicare; other federal heal | - | $650,000 | - | Drug_Prescriptions |
| three-former-executives-for-magellan-diagnos | 2025-11-24 | Amy Winslow (former CEO, Magellan Diagnostics, Inc.) | - | - | $30,600 | - | Other - FDA Submission Fraud |
| two-time-convicted-felon-ceo-and-his-dietary | 2025-11-24 | Jared Wheat (founder, owner and CEO of Hi-Tech Pharm | - | $4,763,292 | - | - | Falsify certificate |
| adult-residential-group-homes-operator-settl | 2025-11-25 | Sola, Inc. (operator of adult residential group home | Medicaid (Virginia Departmen | $641,396 | $2,000,000 | - | Phantom Claims |
| austin-emergency-center-and-affiliates-to-pa | 2025-11-25 | Austin Emergency Center, LLC; Austin ER, LLC; AEC ER | Federal Employees Health Ben | - | $429,231 | - | Upcoding |
| former-state-representative-pleads-guilty-to | 2025-11-26 | Christopher Ziogas (former Connecticut State Represe | Medicaid (Connecticut Depart | - | $599,810 | - | Phantom Claims |
| new-jersey-doctor-charged-with-unlawfully-di | 2025-11-26 | David Holbrook (licensed psychiatrist) | - | - | - | - | Drug_Prescriptions |
| former-ellensburg-doctor-indicted-on-26-felo | 2025-12-01 | Anna Elperin (osteopathic physician, owner of Awake  | - | - | - | - | Drug_Prescriptions |
| nurse-practitioner-sentenced-to-18-months-an | 2025-12-01 | Anja Salamack (psychiatric nurse practitioner) | Medicare | $163,639 | $362,489 | 18 | Phantom Claims |
| the-breastfeeding-shop-and-its-owner-agree-t | 2025-12-01 | Scottie Girl, LLC d/b/a The Breastfeeding Shop (DME  | TRICARE | - | $1,000,000 | - | Unbundling |
| georgia-man-sentenced-for-24m-kickback-and-m | 2025-12-02 | Patrick C. Moore Jr. (kickback broker/recruiter netw | Medicare | $24,000,000 | $7,200,000 | 46 | kickback_Bribery For Referral |
| indian-national-sentenced-to-prison-for-medi | 2025-12-02 | Mohammed Asif (owner and director of American Labwor | Medicare | $8,700,000 | $1,174,813 | 24 | Phantom Claims |
| largest-north-carolina-behavioral-health-pra | 2025-12-02 | Mindpath Care Centers, North Carolina, PLLC (behavio | Medicare | - | $1,900,000 | - | Falsify certificate |
| u-s-attorney-announces-37-76-million-settlem | 2025-12-02 | CVS Pharmacy, Inc. (national retail pharmacy chain) | Medicare; Medicaid; TRICARE; | - | $37,760,000 | - | Drug_Prescriptions |
| ceo-of-fresno-based-health-care-company-arre | 2025-12-03 | Cashmir Chinedu Luke (CEO, sole owner and billing re | Department of Veterans Affai | $7,000,000 | - | - | Phantom Claims |
| texas-man-charged-with-conspiracy-to-obtain- | 2025-12-03 | Darrion Denard Brooks | - | - | - | - | Drug_Prescriptions |
| trucking-company-operator-sentenced-to-priso | 2025-12-03 | Alice F. Martin (owner/operator of Martin Logistics, | - | $3,600,000 | $1,971,660 | 30 | Tax, Payroll or Coupon Fraud |
| u-s-attorney-039-s-office-hosts-annual-meeti | 2025-12-04 | - | - | - | - | - | Other - Unknown |
| virginia-laboratory-to-pay-758-000-to-settle | 2025-12-04 | NEXT Bio-Research Services LLC, d/b/a NEXT Molecular | Medicare; Medicaid; TRICARE | - | $758,000 | - | kickback_Bribery For Referral |
| illinois-men-face-additional-charges-for-hea | 2025-12-05 | Minhaj Feroz Muhammad (owner/controller of clinical  | Medicare; Medicaid; private  | $293,000,000 | - | - | Phantom Claims |
| st-charles-parish-woman-convicted-of-wire-fr | 2025-12-05 | Ashley Hymel (executive assistant at Company 1) | - | $130,664 | $130,664 | - | Wire Fraud |
| two-miami-men-sentenced-to-nearly-five-years | 2025-12-05 | Boris Arencibia (procured and sold diverted drugs);  | - | $28,000,000 | - | 57 | Drug_Prescriptions |
| executive-director-of-in-home-care-business- | 2025-12-09 | Michael Roberts (executive director and co-owner of  | - | - | $1,015,416 | 24 | Tax, Payroll or Coupon Fraud |
| recovery-centers-of-america-agrees-to-pay-2- | 2025-12-10 | Recovery Centers of America (RCA) / TRC-OC, trading  | Federal Employees Health Ben | - | $2,000,000 | - | Phantom Claims |
| spokane-physician-pays-120-000-to-resolve-al | 2025-12-10 | Dr. Duncan Lahtinen (licensed physician) | - | - | $120,000 | - | Drug_Prescriptions |
| telehealth-company-agrees-to-pay-300-000-to- | 2025-12-10 | LifeWorks Counseling Associates, PLLC; Dr. David Fer | Medicaid | - | $300,000 | - | Benefit & Eligibility Fraud |
| canton-man-sentenced-for-multi-million-dolla | 2025-12-11 | Krishna Gidwani (owner/operator of DME company); Raj | Medicare | $4,000,000 | $3,000,000 | 30 | Device, DME |
| former-community-support-worker-pleads-guilt | 2025-12-11 | Jariatu Jalloh (community support worker) | Medicaid (District of Columb | $234,500 | - | - | Phantom Claims |
| former-st-louis-area-pediatrician-admits-exc | 2025-12-11 | Craig A. Spiegel (pediatrician); April Bingham (co-d | Medicare; Missouri Medicaid; | $114,480 | - | 21 | Drug_Prescriptions |
| owner-of-physical-rehabilitation-company-ple | 2025-12-11 | Nosson Sklar, a/k/a "Nathan Sklar" (owner and CEO of | Three unnamed health benefit | $20,000,000 | - | - | Phantom Claims |
| doctor-sentenced-to-seven-years-in-prison-fo | 2025-12-12 | Alexander Baldonado, M.D. (physician) | Medicare; Medicaid | $24,000,000 | $2,210,384 | 84 | kickback_Bribery For Referral |
| former-new-york-doctor-sentenced-for-receivi | 2025-12-12 | Dr. Kenneth Fishberger (internist) | Medicare; private insurance  | $891,978 | $440,876 | - | kickback_Bribery For Referral |
| med-spa-owner-agrees-to-plead-guilty-to-perf | 2025-12-12 | Rodrigo de Medeiros Siqueira (owner of Rodrigo Beaut | - | - | - | - | Drug_Prescriptions |
| missouri-man-sentenced-to-10-years-in-prison | 2025-12-12 | Jamie P. McNamara (operator/owner of laboratories) | Medicare | $174,000,000 | $7,000,000 | 120 | kickback_Bribery For Referral |
| pharmacist-sentenced-to-over-six-years-in-pr | 2025-12-12 | Isaiah Okoh (pharmacist); unnamed co-conspirator | Medicare; Medicaid; Blue Cro | $6,000,000 | $7,119,907 | 80 | Phantom Claims |
| wound-graft-company-owners-sentenced-for-1-2 | 2025-12-12 | Alexandra Gehrke (owner of wound graft companies, in | Medicare; TRICARE; CHAMPVA;  | $1,212,005,778 | $1,941,275,020 | 186 | kickback_Bribery For Referral |
| essex-county-man-pleaded-guilty-to-online-en | 2025-12-15 | Nabeen Leigh Singha | - | - | - | - | Other - Unknown |
| federal-jury-convicts-north-chesterfield-man | 2025-12-15 | George Nathaniel Boykins (Qualified Mental Health Pr | Medicaid (Virginia) | - | - | - | Phantom Claims |
| medical-biller-charged-with-diverting-opioid | 2025-12-15 | Ty Mauldin (medical biller and credentialer) | Medicaid (Delaware);private  | - | - | - | IdentityFraud |
| medical-software-company-agrees-to-pay-500-0 | 2025-12-15 | PenRad Technologies, Inc. (medical software company  | Medicare; Medicaid (MassHeal | - | $529,069 | - | FakeEncounter |
| morris-county-company-settles-matter-allegin | 2025-12-15 | CIE Tours International Inc. (tour company owned by  | - | $3,410,300 | $4,428,985 | - | Covid or General Loan Fraud |
| rst-sanexas-inc-and-its-owners-agree-to-pay- | 2025-12-16 | RST-Sanexas, Inc. (manufacturer and marketer of elec | Medicare | - | $1,500,000 | - | Device, DME |
| digital-health-company-and-medical-practice- | 2025-12-17 | Done Global Inc. (California digital health company) | Medicare; Medicaid; commerci | $100,000,000 | - | - | Drug_Prescriptions |
| roofing-contractor-sentenced-to-15-months-in | 2025-12-17 | Anthony Delmaro (owner/operator of Kings Roofing) | Medicaid (Connecticut Husky  | $500,000 | $1,707,928 | 15 | Tax, Payroll or Coupon Fraud |
| austin-pain-management-doctor-and-pain-medic | 2025-12-18 | Dr. Mark Malone (pain management doctor, founder of  | Medicare; Texas Medicaid; TR | - | $13,625,000 | - | Unbundling |
| connecticut-man-sentenced-to-30-months-impri | 2025-12-18 | Jesse Foote (controlled marketing company and DME su | Medicare; TRICARE; private i | $7,800,000 | $7,878,991 | 30 | kickback_Bribery For Referral |
| doctor-indicted-for-orchestrating-45m-botox- | 2025-12-18 | Violetta Mailyan (doctor, owner and operator of Heal | Medicare | $45,000,000 | - | - | Phantom Claims |
| florida-man-pleads-guilty-to-health-care-fra | 2025-12-18 | Eric Van Vleet (operator of Hype Med LLC); Hype Med  | Medicare | $1,399,812 | - | - | Drug_Prescriptions |
| local-physician-pleads-guilty-to-adulteratin | 2025-12-18 | Dr. Eric Edward Haeger (physician, sleep clinic owne | Medicaid (Washington State M | - | - | - | Device, DME |
| six-additional-defendants-charged-one-defend | 2025-12-18 | Abdinajib Hassan Yussuf (President and CEO, Star Aut | Medicaid (Minnesota Medical  | $26,750,000 | - | - | Phantom Claims |
| two-pharmacists-sentenced-to-years-in-prison | 2025-12-18 | Mohamed Hassan (pharmacist, owner of approximately 2 | Unspecified insurance compan | $48,000,000 | $549,462 | 216 | Drug_Prescriptions |
| former-new-york-doctor-sentenced-for-receivi | 2025-12-19 | Vishnudat Seodat (internist/physician) | Medicare; private insurance  | $1,000,000 | $444,976 | - | kickback_Bribery For Referral |
| new-jersey-business-owner-sentenced-to-87-mo | 2025-12-19 | Aaron Neil Williamsky (owner of more than twenty dur | Medicare | $172,000,000 | $172,000,000 | 87 | Device, DME |
| u-s-postal-service-employee-indicted-for-all | 2025-12-19 | Graciela Venegas, aka "Graciela Salgado" (U.S. Posta | U.S. Department of Labor (fe | $51,776 | - | - | Benefit & Eligibility Fraud |
| ceo-of-health-care-software-company-sentence | 2025-12-22 | Gary Cox (CEO of Power Mobility Doctor Rx, LLC (DMER | Medicare;TRICARE;Department  | $1,000,000,000 | $452,000,000 | 180 | Falsify certificate |
| u-s-attorney-announces-6-8-million-settlemen | 2025-12-22 | New York-Presbyterian Hudson Valley Hospital (hospit | Medicare; Medicaid (New York | $4,000,000 | $6,836,764 | - | kickback_Bribery For Referral |
| arizona-couple-that-ran-medical-clinic-busin | 2025-12-29 | Mary Blakley (principal of medical clinic business,  | - | - | - | - | FakeEncounter |
| 2025-year-in-review_70abefa5cbdb.pdf | 2025-12-31 | - | Medicare | - | - | - | Other - Unknown |

## Fraud types (cases may carry several)

| Type | Cases |
|---|---|
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

## Scheme combinations

| Combination | Cases |
|---|---|
| FakeEncounter + Falsify certificate + kickback_Bribery For Referral | 21 |
| Drug_Prescriptions + Falsify certificate | 14 |
| Device, DME + FakeEncounter + Falsify certificate + kickback_Bribery For Referral | 13 |
| Falsify certificate + Phantom Claims | 10 |
| Drug_Prescriptions + kickback_Bribery For Referral | 9 |
| Falsify certificate + Phantom Claims + Upcoding | 8 |
| Drug_Prescriptions + Phantom Claims | 7 |
| Benefit & Eligibility Fraud + Covid or General Loan Fraud | 7 |
| Falsify certificate + IdentityFraud + Phantom Claims | 7 |
| Drug_Prescriptions + Falsify certificate + Phantom Claims | 7 |
| Drug_Prescriptions + Falsify certificate + IdentityFraud | 7 |
| Covid or General Loan Fraud + Tax, Payroll or Coupon Fraud + Wire Fraud | 6 |
| FakeEncounter + Phantom Claims | 6 |
| Benefit & Eligibility Fraud + Falsify certificate | 6 |
| Falsify certificate + Upcoding | 6 |
| Drug_Prescriptions + FakeEncounter | 6 |
| FakeEncounter + Phantom Claims + kickback_Bribery For Referral | 5 |
| FakeEncounter + Unbundling | 5 |
| Drug_Prescriptions + FakeEncounter + kickback_Bribery For Referral | 5 |
| Covid or General Loan Fraud + Wire Fraud | 5 |
| Covid or General Loan Fraud + IdentityFraud + Wire Fraud | 5 |
| FakeEncounter + Falsify certificate | 5 |
| Benefit & Eligibility Fraud + FakeEncounter + Falsify certificate + kickback_Bribery For Referral | 5 |
| Drug_Prescriptions + IdentityFraud + Phantom Claims | 5 |
| FakeEncounter + kickback_Bribery For Referral | 4 |
| FakeEncounter + Upcoding | 4 |
| Device, DME + Drug_Prescriptions + FakeEncounter + Falsify certificate + Wire Fraud + kickback_Bribery For Referral | 4 |
| Phantom Claims + Wire Fraud | 4 |
| IdentityFraud + Phantom Claims | 4 |
| Falsify certificate + kickback_Bribery For Referral | 4 |
| Falsify certificate + IdentityFraud + Phantom Claims + Wire Fraud + kickback_Bribery For Referral | 4 |
| Falsify certificate + Retention of Overpayment | 3 |
| Device, DME + FakeEncounter + Phantom Claims | 3 |
| Falsify certificate + Other - Embezzlement of federal grant funds | 3 |
| Benefit & Eligibility Fraud + Drug_Prescriptions + Falsify certificate + IdentityFraud | 3 |
| Phantom Claims + Upcoding | 3 |
| FakeEncounter + Falsify certificate + Upcoding | 3 |
| Covid or General Loan Fraud + Phantom Claims + Wire Fraud | 3 |
| Benefit & Eligibility Fraud + Device, DME + Falsify certificate + Wire Fraud + kickback_Bribery For Referral | 3 |
| Falsify certificate + IdentityFraud + Phantom Claims + Wire Fraud | 3 |
| Other - Unknown + Tax, Payroll or Coupon Fraud | 3 |
| Falsify certificate + Tax, Payroll or Coupon Fraud + Wire Fraud | 3 |
| Benefit & Eligibility Fraud + IdentityFraud | 3 |
| Covid or General Loan Fraud + Falsify certificate + Wire Fraud | 3 |
| Device, DME + FakeEncounter + Other - FDA Submission Fraud | 3 |
| Device, DME + FakeEncounter + Phantom Claims + kickback_Bribery For Referral | 3 |
| Drug_Prescriptions + Other - Unknown | 3 |
| Device, DME + FakeEncounter + Falsify certificate | 3 |
| Drug_Prescriptions + Phantom Claims + Wire Fraud | 3 |
| IdentityFraud + Wire Fraud | 3 |
| Device, DME + Phantom Claims + Upcoding | 3 |
| Drug_Prescriptions + FakeEncounter + Falsify certificate | 3 |
| Device, DME + Other - FDA Submission Fraud | 3 |
| Benefit & Eligibility Fraud + Device, DME + Drug_Prescriptions + FakeEncounter + IdentityFraud + Phantom Claims + Wire Fraud + kickback_Bribery For Referral | 2 |
| Device, DME + Other - FDA Submission Fraud + kickback_Bribery For Referral | 2 |
| Other - Unknown + Wire Fraud | 2 |
| FakeEncounter + Upcoding + Wire Fraud + kickback_Bribery For Referral | 2 |
| Device, DME + Drug_Prescriptions + FakeEncounter + kickback_Bribery For Referral | 2 |
| Covid or General Loan Fraud + Upcoding | 2 |
| Drug_Prescriptions + FakeEncounter + Falsify certificate + IdentityFraud | 2 |
| Benefit & Eligibility Fraud + Covid or General Loan Fraud + Tax, Payroll or Coupon Fraud + Wire Fraud | 2 |
| Phantom Claims + Wire Fraud + kickback_Bribery For Referral | 2 |
| Drug_Prescriptions + Wire Fraud | 2 |
| Falsify certificate + Phantom Claims + Unbundling | 2 |
| Device, DME + kickback_Bribery For Referral | 2 |
| Device, DME + Falsify certificate | 2 |
| Device, DME + Wire Fraud | 2 |
| Benefit & Eligibility Fraud + IdentityFraud + Phantom Claims + Wire Fraud | 2 |
| Drug_Prescriptions + FakeEncounter + Wire Fraud | 2 |
| Device, DME + Falsify certificate + kickback_Bribery For Referral | 2 |
| Device, DME + Falsify certificate + IdentityFraud + Phantom Claims + kickback_Bribery For Referral | 2 |
| Benefit & Eligibility Fraud + Phantom Claims + Wire Fraud | 2 |
| Device, DME + IdentityFraud + Phantom Claims | 2 |
| Benefit & Eligibility Fraud + FakeEncounter + Falsify certificate | 2 |
| Drug_Prescriptions + FakeEncounter + Phantom Claims | 2 |
| FakeEncounter + Falsify certificate + Phantom Claims + Wire Fraud | 2 |
| Benefit & Eligibility Fraud + Device, DME + FakeEncounter + Wire Fraud + kickback_Bribery For Referral | 2 |
| Phantom Claims + Upcoding + Wire Fraud | 2 |
| Device, DME + Falsify certificate + Wire Fraud + kickback_Bribery For Referral | 2 |
| Device, DME + FakeEncounter + Wire Fraud + kickback_Bribery For Referral | 2 |
| Device, DME + Falsify certificate + IdentityFraud + Phantom Claims + Wire Fraud + kickback_Bribery For Referral | 2 |
| Benefit & Eligibility Fraud + Wire Fraud | 2 |
| FakeEncounter + Phantom Claims + Wire Fraud + kickback_Bribery For Referral | 2 |
| Benefit & Eligibility Fraud + Drug_Prescriptions + IdentityFraud + Phantom Claims + Upcoding | 2 |
| Benefit & Eligibility Fraud + Falsify certificate + Wire Fraud | 2 |
| Benefit & Eligibility Fraud + Tax, Payroll or Coupon Fraud + Wire Fraud | 2 |
| Benefit & Eligibility Fraud + FakeEncounter + IdentityFraud + Phantom Claims + Wire Fraud | 2 |
| Drug_Prescriptions + Falsify certificate + kickback_Bribery For Referral | 2 |
| Covid or General Loan Fraud + Falsify certificate + IdentityFraud + Phantom Claims | 2 |
| Falsify certificate + IdentityFraud + kickback_Bribery For Referral | 2 |
| Tax, Payroll or Coupon Fraud + Wire Fraud | 2 |
| Falsify certificate + Phantom Claims + Tax, Payroll or Coupon Fraud | 2 |
| Benefit & Eligibility Fraud + FakeEncounter + kickback_Bribery For Referral | 2 |
| Benefit & Eligibility Fraud + FakeEncounter + Phantom Claims | 2 |
| Benefit & Eligibility Fraud + Device, DME + FakeEncounter + kickback_Bribery For Referral | 2 |
| Falsify certificate + Phantom Claims + Upcoding + kickback_Bribery For Referral | 2 |
| FakeEncounter + Falsify certificate + Phantom Claims | 2 |
| Falsify certificate + Wire Fraud | 2 |
| Benefit & Eligibility Fraud + Phantom Claims | 2 |
| Covid or General Loan Fraud + Drug_Prescriptions + Phantom Claims | 2 |
| IdentityFraud + Phantom Claims + Wire Fraud | 2 |
| Device, DME + Upcoding | 2 |
| Drug_Prescriptions + Phantom Claims + kickback_Bribery For Referral | 2 |
| Drug_Prescriptions + Falsify certificate + Phantom Claims + kickback_Bribery For Referral | 2 |
| Benefit & Eligibility Fraud + Falsify certificate + IdentityFraud | 2 |
| Benefit & Eligibility Fraud + IdentityFraud + Wire Fraud + kickback_Bribery For Referral | 2 |
| Benefit & Eligibility Fraud + IdentityFraud + Tax, Payroll or Coupon Fraud | 2 |
| Device, DME + FakeEncounter + kickback_Bribery For Referral | 2 |
| Drug_Prescriptions + FakeEncounter + Falsify certificate + kickback_Bribery For Referral | 2 |
| Upcoding + Wire Fraud + kickback_Bribery For Referral | 2 |
| FakeEncounter + Phantom Claims + Unbundling | 2 |
| Benefit & Eligibility Fraud + kickback_Bribery For Referral | 2 |
| Drug_Prescriptions + IdentityFraud + Phantom Claims + kickback_Bribery For Referral | 2 |
| FakeEncounter + Unbundling + Upcoding | 2 |
| Other - Embezzlement of federal grant funds + Wire Fraud + kickback_Bribery For Referral | 1 |
| Device, DME + Falsify certificate + Phantom Claims + Unbundling + kickback_Bribery For Referral | 1 |
| FakeEncounter + IdentityFraud + Phantom Claims + kickback_Bribery For Referral | 1 |
| Drug_Prescriptions + Phantom Claims + Tax, Payroll or Coupon Fraud + Upcoding | 1 |
| FakeEncounter + Falsify certificate + Phantom Claims + Unbundling + Upcoding | 1 |
| Drug_Prescriptions + FakeEncounter + Falsify certificate + Wire Fraud | 1 |
| Benefit & Eligibility Fraud + Drug_Prescriptions + FakeEncounter + Falsify certificate + IdentityFraud | 1 |
| Benefit & Eligibility Fraud + Falsify certificate + IdentityFraud + Phantom Claims + Wire Fraud + kickback_Bribery For Referral | 1 |
| Benefit & Eligibility Fraud + Device, DME + Falsify certificate + kickback_Bribery For Referral | 1 |
| Covid or General Loan Fraud + Falsify certificate | 1 |
| Covid or General Loan Fraud + IdentityFraud + Phantom Claims + Wire Fraud | 1 |
| IdentityFraud + Phantom Claims + Tax, Payroll or Coupon Fraud | 1 |
| Covid or General Loan Fraud + IdentityFraud + Other - Unknown + Wire Fraud | 1 |
| Benefit & Eligibility Fraud + Covid or General Loan Fraud + IdentityFraud + Wire Fraud | 1 |
| Wire Fraud + kickback_Bribery For Referral | 1 |
| Benefit & Eligibility Fraud + Falsify certificate + IdentityFraud + Phantom Claims + Wire Fraud | 1 |
| Falsify certificate + Other - Unknown | 1 |
| Phantom Claims + Retention of Overpayment + Wire Fraud | 1 |
| Benefit & Eligibility Fraud + Covid or General Loan Fraud + Wire Fraud | 1 |
| Covid or General Loan Fraud + Phantom Claims + Upcoding | 1 |
| Falsify certificate + Phantom Claims + Upcoding + Wire Fraud + kickback_Bribery For Referral | 1 |
| Falsify certificate + Tax, Payroll or Coupon Fraud + kickback_Bribery For Referral | 1 |
| Phantom Claims + Retention of Overpayment + Unbundling | 1 |
| Falsify certificate + Phantom Claims + Upcoding + Wire Fraud | 1 |
| Benefit & Eligibility Fraud + FakeEncounter + Falsify certificate + Phantom Claims + Wire Fraud + kickback_Bribery For Referral | 1 |
| Falsify certificate + Phantom Claims + Unbundling + Wire Fraud | 1 |
| Drug_Prescriptions + FakeEncounter + Upcoding + Wire Fraud | 1 |
| Device, DME + Phantom Claims + Upcoding + Wire Fraud | 1 |
| Benefit & Eligibility Fraud + Falsify certificate + IdentityFraud + kickback_Bribery For Referral | 1 |
| Covid or General Loan Fraud + Drug_Prescriptions + FakeEncounter + Falsify certificate + Other - Unknown + Phantom Claims + Retention of Overpayment + Upcoding + kickback_Bribery For Referral | 1 |
| FakeEncounter + Falsify certificate + IdentityFraud + Phantom Claims + Upcoding + Wire Fraud + kickback_Bribery For Referral | 1 |
| Benefit & Eligibility Fraud + Covid or General Loan Fraud + FakeEncounter + Falsify certificate + Phantom Claims + Upcoding + Wire Fraud + kickback_Bribery For Referral | 1 |
| Covid or General Loan Fraud + Device, DME + Drug_Prescriptions + Falsify certificate + IdentityFraud + Phantom Claims + Wire Fraud + kickback_Bribery For Referral | 1 |
| Covid or General Loan Fraud + IdentityFraud + Phantom Claims | 1 |
| Benefit & Eligibility Fraud + Device, DME + FakeEncounter | 1 |
| Drug_Prescriptions + FakeEncounter + Falsify certificate + Upcoding | 1 |
| Covid or General Loan Fraud + FakeEncounter + Tax, Payroll or Coupon Fraud + Wire Fraud + kickback_Bribery For Referral | 1 |
| FakeEncounter + Phantom Claims + Tax, Payroll or Coupon Fraud + Wire Fraud + kickback_Bribery For Referral | 1 |
| Phantom Claims + Retention of Overpayment + Wire Fraud + kickback_Bribery For Referral | 1 |
| Covid or General Loan Fraud + Drug_Prescriptions | 1 |
| Falsify certificate + Other - Unknown + Wire Fraud | 1 |
| Drug_Prescriptions + FakeEncounter + Falsify certificate + Phantom Claims + Wire Fraud | 1 |
| Device, DME + Falsify certificate + IdentityFraud + Wire Fraud + kickback_Bribery For Referral | 1 |
| Device, DME + FakeEncounter + Falsify certificate + IdentityFraud + Phantom Claims + kickback_Bribery For Referral | 1 |
| Benefit & Eligibility Fraud + FakeEncounter + Falsify certificate + Wire Fraud + kickback_Bribery For Referral | 1 |
| Drug_Prescriptions + Falsify certificate + IdentityFraud + Phantom Claims + Upcoding | 1 |
| Benefit & Eligibility Fraud + Covid or General Loan Fraud + Falsify certificate | 1 |
| Falsify certificate + Phantom Claims + kickback_Bribery For Referral | 1 |
| Benefit & Eligibility Fraud + IdentityFraud + Phantom Claims | 1 |
| FakeEncounter + Falsify certificate + IdentityFraud + kickback_Bribery For Referral | 1 |
| Device, DME + Phantom Claims | 1 |
| Benefit & Eligibility Fraud + Falsify certificate + Phantom Claims + kickback_Bribery For Referral | 1 |
| Falsify certificate + Upcoding + kickback_Bribery For Referral | 1 |
| Benefit & Eligibility Fraud + Phantom Claims + Upcoding | 1 |
| Benefit & Eligibility Fraud + Upcoding + kickback_Bribery For Referral | 1 |
| Drug_Prescriptions + Tax, Payroll or Coupon Fraud + Wire Fraud | 1 |
| Benefit & Eligibility Fraud + Device, DME + FakeEncounter + Falsify certificate + kickback_Bribery For Referral | 1 |
| Covid or General Loan Fraud + IdentityFraud + Other - Unknown + Tax, Payroll or Coupon Fraud + Wire Fraud | 1 |
| Drug_Prescriptions + IdentityFraud | 1 |
| FakeEncounter + Falsify certificate + Wire Fraud + kickback_Bribery For Referral | 1 |
| Device, DME + FakeEncounter + Falsify certificate + Phantom Claims + Wire Fraud + kickback_Bribery For Referral | 1 |
| Covid or General Loan Fraud + FakeEncounter + Falsify certificate + Phantom Claims + kickback_Bribery For Referral | 1 |
| Device, DME + Drug_Prescriptions + Phantom Claims | 1 |
| Covid or General Loan Fraud + Falsify certificate + Phantom Claims + Wire Fraud | 1 |
| Benefit & Eligibility Fraud + Covid or General Loan Fraud + Falsify certificate + Phantom Claims + Wire Fraud | 1 |
| FakeEncounter + Falsify certificate + IdentityFraud + Phantom Claims + Wire Fraud | 1 |
| Benefit & Eligibility Fraud + Device, DME + Phantom Claims + Wire Fraud | 1 |
| Drug_Prescriptions + IdentityFraud + Wire Fraud | 1 |
| Device, DME + FakeEncounter | 1 |
| Device, DME + FakeEncounter + Wire Fraud | 1 |
| Covid or General Loan Fraud + Tax, Payroll or Coupon Fraud | 1 |
| Benefit & Eligibility Fraud + Device, DME + kickback_Bribery For Referral | 1 |
| Covid or General Loan Fraud + Drug_Prescriptions + FakeEncounter + Phantom Claims + Upcoding + kickback_Bribery For Referral | 1 |
| Benefit & Eligibility Fraud + Falsify certificate + Phantom Claims + Unbundling | 1 |
| Device, DME + Phantom Claims + Wire Fraud | 1 |
| Unbundling + Upcoding + Wire Fraud | 1 |
| Device, DME + FakeEncounter + Falsify certificate + Tax, Payroll or Coupon Fraud + kickback_Bribery For Referral | 1 |
| FakeEncounter + IdentityFraud + Other - Embezzlement of federal grant funds + Phantom Claims + kickback_Bribery For Referral | 1 |
| Covid or General Loan Fraud + Device, DME + Drug_Prescriptions + FakeEncounter + IdentityFraud + Phantom Claims + Wire Fraud + kickback_Bribery For Referral | 1 |
| Covid or General Loan Fraud + Device, DME + Drug_Prescriptions + FakeEncounter + Falsify certificate + Phantom Claims + Wire Fraud + kickback_Bribery For Referral | 1 |
| FakeEncounter + IdentityFraud + Upcoding | 1 |
| Device, DME + FakeEncounter + Falsify certificate + IdentityFraud + Wire Fraud | 1 |
| Phantom Claims + Unbundling + kickback_Bribery For Referral | 1 |
| FakeEncounter + Falsify certificate + Phantom Claims + Wire Fraud + kickback_Bribery For Referral | 1 |
| Drug_Prescriptions + Phantom Claims + Wire Fraud + kickback_Bribery For Referral | 1 |
| Benefit & Eligibility Fraud + Falsify certificate + Phantom Claims + Upcoding | 1 |
| Device, DME + FakeEncounter + Falsify certificate + IdentityFraud + kickback_Bribery For Referral | 1 |
| Device, DME + FakeEncounter + IdentityFraud + kickback_Bribery For Referral | 1 |
| Benefit & Eligibility Fraud + Falsify certificate + Phantom Claims + Wire Fraud | 1 |
| Benefit & Eligibility Fraud + Phantom Claims + Tax, Payroll or Coupon Fraud | 1 |
| Phantom Claims + Upcoding + Wire Fraud + kickback_Bribery For Referral | 1 |
| Benefit & Eligibility Fraud + Device, DME + FakeEncounter + Falsify certificate + Wire Fraud + kickback_Bribery For Referral | 1 |
| Drug_Prescriptions + Falsify certificate + Other - FDA Submission Fraud + Wire Fraud | 1 |
| Benefit & Eligibility Fraud + Drug_Prescriptions + FakeEncounter + IdentityFraud | 1 |
| Drug_Prescriptions + Phantom Claims + Retention of Overpayment + Upcoding | 1 |
| Covid or General Loan Fraud + Phantom Claims + Tax, Payroll or Coupon Fraud + Wire Fraud | 1 |
| Drug_Prescriptions + Falsify certificate + Phantom Claims + Wire Fraud | 1 |
| Benefit & Eligibility Fraud + Falsify certificate + IdentityFraud + Wire Fraud | 1 |
| Covid or General Loan Fraud + Device, DME + Drug_Prescriptions + Falsify certificate + IdentityFraud + Phantom Claims + Retention of Overpayment | 1 |
| Device, DME + IdentityFraud + Phantom Claims + Unbundling + Upcoding | 1 |
| Benefit & Eligibility Fraud + FakeEncounter | 1 |
| Device, DME + Falsify certificate + Wire Fraud | 1 |
| Drug_Prescriptions + FakeEncounter + IdentityFraud | 1 |
| FakeEncounter + Falsify certificate + Phantom Claims + Upcoding + Wire Fraud + kickback_Bribery For Referral | 1 |
| Covid or General Loan Fraud + FakeEncounter + Falsify certificate + Phantom Claims + Wire Fraud | 1 |
| Benefit & Eligibility Fraud + Falsify certificate + IdentityFraud + Phantom Claims | 1 |
| Benefit & Eligibility Fraud + Falsify certificate + IdentityFraud + Phantom Claims + Upcoding + Wire Fraud + kickback_Bribery For Referral | 1 |
| FakeEncounter + Falsify certificate + Phantom Claims + Upcoding | 1 |
| Benefit & Eligibility Fraud + Falsify certificate + Upcoding + Wire Fraud | 1 |
| Benefit & Eligibility Fraud + FakeEncounter + Falsify certificate + IdentityFraud + kickback_Bribery For Referral | 1 |
| Drug_Prescriptions + FakeEncounter + Falsify certificate + Phantom Claims | 1 |
| Drug_Prescriptions + FakeEncounter + Tax, Payroll or Coupon Fraud + Wire Fraud + kickback_Bribery For Referral | 1 |
| Device, DME + Unbundling | 1 |
| Benefit & Eligibility Fraud + Device, DME + Drug_Prescriptions + FakeEncounter + Falsify certificate + IdentityFraud + Wire Fraud | 1 |
| Covid or General Loan Fraud + Drug_Prescriptions + Falsify certificate + IdentityFraud + Wire Fraud | 1 |
| Benefit & Eligibility Fraud + Covid or General Loan Fraud + Drug_Prescriptions + IdentityFraud | 1 |
| Phantom Claims + Tax, Payroll or Coupon Fraud + Wire Fraud + kickback_Bribery For Referral | 1 |
| Benefit & Eligibility Fraud + Device, DME + IdentityFraud + Phantom Claims + Wire Fraud | 1 |
| Benefit & Eligibility Fraud + IdentityFraud + kickback_Bribery For Referral | 1 |
| Benefit & Eligibility Fraud + Covid or General Loan Fraud + Other - Embezzlement of federal grant funds + kickback_Bribery For Referral | 1 |
| Device, DME + Phantom Claims + Upcoding + kickback_Bribery For Referral | 1 |
| Benefit & Eligibility Fraud + IdentityFraud + Phantom Claims + kickback_Bribery For Referral | 1 |
| Benefit & Eligibility Fraud + FakeEncounter + Falsify certificate + Phantom Claims | 1 |
| Drug_Prescriptions + IdentityFraud + Phantom Claims + Wire Fraud + kickback_Bribery For Referral | 1 |
| Device, DME + FakeEncounter + Falsify certificate + Phantom Claims | 1 |
| Device, DME + Falsify certificate + Upcoding + Wire Fraud + kickback_Bribery For Referral | 1 |
| Drug_Prescriptions + IdentityFraud + Phantom Claims + Wire Fraud | 1 |
| Covid or General Loan Fraud + Device, DME + Falsify certificate | 1 |
| Drug_Prescriptions + Falsify certificate + Wire Fraud | 1 |
| Drug_Prescriptions + FakeEncounter + Falsify certificate + IdentityFraud + Phantom Claims | 1 |
| Covid or General Loan Fraud + Other - Unknown + kickback_Bribery For Referral | 1 |
| Phantom Claims + kickback_Bribery For Referral | 1 |
| Device, DME + Drug_Prescriptions + FakeEncounter + IdentityFraud + Other - FDA Submission Fraud + Phantom Claims + Upcoding | 1 |
| Benefit & Eligibility Fraud + Phantom Claims + kickback_Bribery For Referral | 1 |
| Other - Unknown + kickback_Bribery For Referral | 1 |
| Covid or General Loan Fraud + Other - Unknown + Wire Fraud | 1 |
| Benefit & Eligibility Fraud + Covid or General Loan Fraud + Drug_Prescriptions + FakeEncounter + Falsify certificate + Upcoding + kickback_Bribery For Referral | 1 |
| Device, DME + Retention of Overpayment | 1 |
| Device, DME + Drug_Prescriptions + FakeEncounter + Falsify certificate + IdentityFraud + kickback_Bribery For Referral | 1 |
| Benefit & Eligibility Fraud + IdentityFraud + Wire Fraud | 1 |
| FakeEncounter + Falsify certificate + Phantom Claims + Upcoding + kickback_Bribery For Referral | 1 |
| Covid or General Loan Fraud + Phantom Claims + Retention of Overpayment | 1 |
| Other - Embezzlement of federal grant funds + Wire Fraud | 1 |
| Phantom Claims + Upcoding + kickback_Bribery For Referral | 1 |
| Benefit & Eligibility Fraud + FakeEncounter + IdentityFraud | 1 |
| Benefit & Eligibility Fraud + Covid or General Loan Fraud + FakeEncounter + Wire Fraud | 1 |

## Payers defrauded

| Payer | Cases |
|---|---|
| Medicare | 339 |
| Medicaid | 228 |
| Commercial payer | 78 |
| TRICARE/CHAMPVA | 51 |
| Department of Veterans Affairs | 6 |
| Federal Employees Health Benefits Program | 5 |
| other insurers | 5 |
| Small Business Administration (Paycheck Protection Program) | 4 |
| U.S. Department of Veterans Affairs | 4 |
| HRSA COVID-19 Uninsured Program | 4 |
| other federal health care programs | 4 |
| Social Security Administration | 3 |
| Anthem | 3 |
| IRS | 3 |
| U.S. Department of Labor Office of Workers' Compensation Programs | 3 |
| Amtrak health care plan | 2 |
| U.S. Department of Health and Human Services | 2 |
| other federal health care benefit programs | 2 |
| other insurance companies | 2 |
| UCare | 2 |
| other insurance providers | 2 |
| Louisiana unemployment insurance program | 2 |
| insurance companies | 2 |
| SNAP (USDA) | 2 |
| Maine Department of Labor) | 2 |
| American Family Life Assurance Company of Columbus (AFLAC) | 2 |
| U.S. Department of Labor (federal workers' compensation program) | 2 |
| other government payors | 1 |
| Small Business Administration (PPP and EIDL pandemic relief programs) | 1 |
| Amtrak employee health care plan | 1 |
| More than 10 health insurance plans (not individually named) | 1 |
| National Institutes of Health | 1 |
| Federal Employees Health Benefit Program (FEHBP) | 1 |
| Federal health care programs | 1 |
| National Institutes of Health (NIH) | 1 |
| Health Resources and Services Administration (HRSA) COVID-19 Uninsured Program | 1 |
| Insurance Company 1 (unnamed Canadian-headquartered workers' compensation insurer) | 1 |
| Veterans Affairs health care programs | 1 |
| Department of Veterans Affairs (Veterans Community Care Program) | 1 |
| VA | 1 |
| other federal health care benefit programs (including VA) | 1 |
| Department of Veterans Affairs health programs | 1 |
| Optima | 1 |
| U.S. Department of Health and Human Services' Health Resources and Services Administration (HRSA) | 1 |
| U.S. Department of Health and Human Services' Health Resources and Services Administration (HRSA) COVID-19 uninsured program | 1 |
| HRSA COVID-19 Claims Reimbursement to Health Care Providers and Facilities for Testing, Treatment, and Vaccine Administration for the Uninsured Program | 1 |
| Small Business Administration (U.S. government - Paycheck Protection Program) | 1 |
| New York State Workers' Compensation Board (benefits paid from the New York City Treasury) | 1 |
| Veterans Health Administration Community Care Program | 1 |
| U.S. Army | 1 |
| U.S. Small Business Administration (PPP/EIDL) | 1 |
| twelve other insurance companies | 1 |
| Affordable Care Act federal premium subsidies (federal government/ACA insurance plan) | 1 |
| USDA Federal Child Nutrition Program (via Feeding Our Future/MDE) | 1 |
| COVID-19 Provider Relief Fund | 1 |
| workers' compensation insurance companies | 1 |
| Pacific States Marine Fisheries Commission self-funded health care benefit program (health benefit trust account) | 1 |
| Pacific States Marine Fisheries Commission self-funded health care benefit program (health benefit trust account funded in part by federal grant money) | 1 |
| Small Business Administration (PPP/EIDL) | 1 |
| Department of Veterans Affairs (Caregiver Support Program) | 1 |
| Internal Revenue Service (U.S. Treasury) | 1 |
| U.S. Department of Health and Human Services (COVID-19 provider relief funds) | 1 |
| U.S. Department of Veterans Affairs (VA Dependency and Indemnity Compensation | 1 |
| Small Business Administration (SBA) | 1 |
| PPP approved lenders | 1 |
| Department of Labor Office of Workers Compensation Program (DOL-OWCP) | 1 |
| U.S. Department of Labor | 1 |
| North Carolina Department of Commerce, Division of Employment Security (NCDES) | 1 |
| other governmental health care programs | 1 |
| U.S. Navy (Department of Defense) | 1 |
| Virginia Employment Commission (state unemployment insurance and Federal Pandemic Unemployment Compensation) | 1 |
| Internal Revenue Service (IRS) | 1 |
| workers' compensation insurance carrier | 1 |
| IRS (tax loss) | 1 |
| U.S. Agency for International Development (USAID) - KEMSA Medical Commodities Program | 1 |
| health care benefit programs | 1 |
| Small Business Administration - Paycheck Protection Program | 1 |
| Department of Veterans Affairs (Post-9/11 GI Bill) | 1 |
| Small Business Administration (PPP) | 1 |
| Department of Defense (Defense Health Agency) | 1 |
| other insurance carriers | 1 |
| Federal Employees' Compensation Fund | 1 |
| USDA Women, Infants, and Children (WIC) program | 1 |
| Department of Veterans Affairs health care programs | 1 |
| Three unnamed health benefit programs (federal health care programs referenced by HHS-OIG) | 1 |
| U.S. Department of Veterans Affairs - Foreign Medical Program | 1 |
| Federal health care benefit programs | 1 |
| pharmacy benefit managers | 1 |
| Paycheck Protection Program (SBA) | 1 |
| Lowe's Home Improvement | 1 |
| U.S. Office of Personnel Management health plans | 1 |
| U.S. Office of Personnel Management (federal employee health plans) | 1 |
| Plaster's Local Union #9 health and welfare fund (union health care benefit program) | 1 |
| Federal government (Affordable Care Act premium subsidies) | 1 |
| Affordable Care Act federal premium subsidies (federal government) | 1 |
| New York City | 1 |
| City of New York agencies (Department of Citywide Administrative Services, Department of Education, Department of Environmental Protection, Department of Sanitation) | 1 |
| National Institutes of Health (grant funding) | 1 |
| Health Plan of Nevada | 1 |
| Molina Healthcare of Nevada | 1 |
| Silversummit Healthplan | 1 |
| State of Illinois | 1 |
| Veterans Administration | 1 |
| U.S. Small Business Administration (Paycheck Protection Program) | 1 |
| U.S. Department of Housing and Urban Development (Community Development Block Grant - Disaster Recovery funds) | 1 |
| First NBC Bank | 1 |
| a North Carolina bank | 1 |
| Chickasaw Nation Department of Health | 1 |
| SNAP | 1 |
| Paycheck Protection Program | 1 |
| Economic Injury Disaster Loan Program | 1 |
| CARES Act unemployment (Louisiana Workforce Commission | 1 |
| Paycheck Protection Program (PPP) | 1 |
| Economic Injury Disaster Loan (EIDL) Program | 1 |
| CARES Act unemployment benefits (Louisiana Workforce Commission | 1 |
| Federal Employees' Compensation Fund (FECA) | 1 |
| Express Scripts, Inc. | 1 |
| unspecified health care benefit programs | 1 |
| Arizona Department of Economic Security (unemployment insurance and Pandemic Unemployment Assistance programs) | 1 |
| New Jersey State Health Benefits Program (state and local government and education employee health plans) | 1 |
| U.S. Department of Veterans Affairs (VA) | 1 |
| pharmaceutical manufacturer copay assistance programs | 1 |
| Unspecified insurance companies | 1 |
| CareFirst BlueCross BlueShield | 1 |
| Department of Labor | 1 |
| U.S. Postal Service | 1 |
| HRSA COVID-19 Uninsured Program (federal) | 1 |
| Third-party Health Savings Account administrator companies (Maryland and Minnesota) | 1 |
| OPM FEHB | 1 |
| Department of Labor programs) | 1 |

## States

| State | Cases |
|---|---|
| Florida | 59 |
| California | 52 |
| New York | 46 |
| New Jersey | 43 |
| Texas | 39 |
| Pennsylvania | 35 |
| Louisiana | 30 |
| Virginia | 27 |
| Connecticut | 25 |
| Massachusetts | 25 |
| Illinois | 22 |
| North Carolina | 21 |
| Michigan | 18 |
| Washington | 17 |
| Tennessee | 15 |
| Missouri | 13 |
| Ohio | 12 |
| South Carolina | 10 |
| Georgia | 10 |
| Kentucky | 10 |
| Arizona | 9 |
| Maryland | 8 |
| Oklahoma | 8 |
| New Hampshire | 8 |
| District of Columbia | 7 |
| West Virginia | 6 |
| Wisconsin | 6 |
| Minnesota | 6 |
| Iowa | 6 |
| Nevada | 5 |
| Rhode Island | 4 |
| Indiana | 4 |
| Delaware | 4 |
| Mississippi | 4 |
| Alabama | 3 |
| Oregon | 3 |
| Kansas | 3 |
| District of Columbia (Washington, D.C.) | 2 |
| Maine | 2 |
| Vermont | 2 |
| Alaska | 1 |
| Wyoming | 1 |
| Montana | 1 |
| Nationwide (United States), including Illinois | 1 |
| Arkansas | 1 |
| Nebraska | 1 |
| Nationwide | 1 |
| Hawaii | 1 |
| Panama (Republic of Panama) | 1 |
| Puerto Rico | 1 |
| Colorado | 1 |
| Kentucky (Bowling Green/Louisville) | 1 |
| South Dakota | 1 |
| New Mexico | 1 |
| District of Columbia (Washington, DC) | 1 |
| Idaho | 1 |

## Case status

| Status | Cases |
|---|---|
| sentenced | 193 |
| civil settlement | 163 |
| charged | 129 |
| pleaded guilty | 124 |
| other | 41 |
| convicted at trial | 29 |

## Documents covering the same case

| Entity | Documents | Stages |
|---|---|---|
| Sanjeev Kumar (gynecologist) | acting-united-states-attorney-fondren-announces-fe<br>federal-grand-jury-returns-second-superseding-indi | charged, charged |
| Aesculap Implant Systems, LLC (medical device company) | aesculap-implant-systems-agrees-to-pay-38-5-millio<br>aesculap-implant-systems-agrees-to-pay-38-5m-to-re | civil settlement, civil settlement |
| Cody Lee Anderson (designated personal representative of the | aiken-man-pleads-guilty-to-conspiracy-to-commit-ba<br>aiken-men-sentenced-to-federal-prison-for-defraudi | pleaded guilty, sentenced |
| Tommie Robinson (physician) | alabama-doctor-charged-with-6-million-telemedicine<br>alabama-doctor-pleads-guilty-to-6-million-telemedi | charged, pleaded guilty |
| Dr. David Antonio Becerril (licensed Washington physician);  | amidst-the-government-shutdown-the-united-states-a<br>coeur-dalene-physician-found-guilty-in-telemarketi | convicted at trial, convicted at trial |
| Alexandra Gehrke (owner of Apex Medical LLC and Viking Medic | arizona-couple-pleads-guilty-to-1-2b-health-care-f<br>wound-graft-company-owners-sentenced-for-1-2b-heal | pleaded guilty, sentenced |
| Athira Pharma Inc.; Leen Kawas (former CEO) | athira-pharma-inc-agrees-to-pay-4m-to-settle-false<br>bothell-biopharmaceutical-company-pays-4-million-t | civil settlement, civil settlement |
| Thomasina E. Amponsah (unlicensed individual posing as regis | baltimore-county-woman-admits-to-impersonating-nur<br>baltimore-county-woman-sentenced-for-impersonating | pleaded guilty, sentenced |
| Armen Muradyan (owner/operator of Genex Laboratories Inc.);  | blood-test-lab-owner-pleads-guilty-to-evading-over<br>owner-of-california-blood-testing-laboratory-plead | pleaded guilty, pleaded guilty |
| Zakia Khan (owner of Happy Family Social Adult Day Care Cent | brooklyn-woman-pleads-guilty-to-leading-a-68-milli<br>leader-of-68m-adult-day-care-fraud-scheme-pleads-g | pleaded guilty, pleaded guilty |
| Avanish Kumar Jha (co-owner, Dhrishti Pharma International); | brothers-from-india-sentenced-to-prison-for-smuggl<br>two-brothers-from-india-arraigned-on-indictment-fo | sentenced, charged |
| Zaven Yeghiazaryan (business owner) | business-owner-pleads-guilty-to-fraud-and-money-la<br>business-owner-sentenced-to-more-than-five-years-i | pleaded guilty, sentenced |
| Advoque Safeguard LLC (mask manufacturer); Jason Azevedo (ow | california-company-and-three-employees-sentenced-f<br>california-company-pleads-guilty-to-conspiring-to- | sentenced, pleaded guilty |
| Juan Carlos Esparza (owner of House of Angels Hospice); Petr | california-man-pleads-guilty-in-connection-with-16<br>four-california-residents-sentenced-to-prison-in-c | pleaded guilty, sentenced |
| Petros Fichidzhyan (controlled sham hospice entities and a h | california-man-sentenced-to-12-years-imprisonment-<br>man-pleads-guilty-in-connection-with-17m-medicare- | sentenced, pleaded guilty |
| Krishna Gidwani (co-owner/operator of DME company); Raju Sha | canton-man-charged-in-national-health-care-fraud-t<br>canton-man-pleads-guilty-to-multi-million-dollar-h<br>canton-man-sentenced-for-multi-million-dollar-heal | charged, pleaded guilty, sentenced |
| Gary Cox (CEO of Power Mobility Doctor Rx, LLC (DMERx)); Pow | ceo-of-health-care-software-company-convicted-of-1<br>ceo-of-health-care-software-company-convicted-of-1<br>ceo-of-health-care-software-company-sentenced-for- | convicted at trial, convicted at trial, sentenced |
| Dr. Kingsley R. Chin (Founder, President and CEO of SpineFro | ceo-of-spine-device-company-pleads-guilty-to-false<br>ceo-of-spine-device-company-sentenced-for-false-st | pleaded guilty, sentenced |
| Chesapeake Regional Medical Center (hospital, formerly Chesa | chesapeake-hospital-indicted-for-healthcare-fraud-<br>media-advisory-chesapeake-regional-medical-center- | charged, charged |
| Zishan Alvi (owner/operator of Chicago Covid-19 testing labo | chicago-lab-owner-sentenced-to-seven-years-in-pris<br>chicago-lab-owner-sentenced-to-seven-years-in-pris | sentenced, sentenced |
| KBWB Operations LLC, d/b/a Atrium Health and Senior Living ( | corporation-and-former-chief-executive-officer-ple<br>corporation-and-former-chief-executive-officer-sen | pleaded guilty, sentenced |
| CVS Pharmacy Inc. (pharmacy chain) | cvs-pharmacy-inc-pays-18-2-million-to-resolve-alle<br>u-s-attorney-announces-37-76-million-settlement-wi | civil settlement, civil settlement |
| Jacquelyn Farrish (Medicaid Consumer Directed Care Program r | danville-woman-pleads-guilty-to-health-care-fraud_<br>danville-woman-sentenced-for-health-care-fraud_6da | pleaded guilty, sentenced |
| Patients Choice Laboratories (PCL) (diagnostic laboratory) | diagnostic-laboratory-agrees-to-pay-more-than-9-mi<br>indiana-laboratory-company-agrees-to-pay-more-than | civil settlement, civil settlement |
| Diopsys Inc. (medical device company) | diopsys-inc-agrees-to-pay-up-to-14-25-million-to-r<br>diopsys-inc-agrees-to-pay-up-to-14-25-million-to-r | civil settlement, civil settlement |
| James Rausch (director of operations and sales, Northeast re | director-of-mobile-medical-diagnostics-company-agr<br>new-york-man-pleads-guilty-to-70-million-kickback- | charged, pleaded guilty |
| Alexander Baldonado, M.D. (physician) | doctor-convicted-of-24m-medicare-fraud-scheme_a801<br>doctor-sentenced-to-seven-years-in-prison-for-24m- | convicted at trial, sentenced |
| Carrie Musselman (chiropractor) | eureka-chiropractor-convicted-of-defrauding-medica<br>eureka-chiropractor-sentenced-to-20-months-in-pris | convicted at trial, sentenced |
| Exactech Inc. (medical device manufacturer, Gainesville, Flo | exactech-agrees-to-pay-8-million-to-resolve-false-<br>medical-device-company-exactech-inc-agrees-to-pay- | civil settlement, civil settlement |
| Alexis Garcia (manager/director of Tape Drywall Services Inc | florida-man-pleads-guilty-for-role-in-an-off-the-b<br>naples-man-sentenced-to-federal-prison-for-conspir | pleaded guilty, sentenced |
| Lino Mallari Gutierrez, a/k/a 'Joe Gutierrez' (licensed brok | florida-man-sentenced-to-more-than-17-years-for-sc<br>jury-convicts-florida-man-for-stealing-10-9-millio | sentenced, convicted at trial |
| Pinellas Eye Care, P.A. d/b/a Gulfcoast Eye Care (ophthalmol | florida-ophthalmology-practice-agrees-to-pay-615-0<br>florida-ophthalmology-practice-agrees-to-pay-615-0 | civil settlement, civil settlement |
| OHM Pharmacy Services, aka "Benzer," aka "Auburndale" (Flori | florida-pharmacy-pleads-guilty-to-health-care-frau<br>florida-pharmacy-pleads-guilty-to-health-care-frau | sentenced, pleaded guilty |
| Andrew Park (co-founder and CEO of a startup technology comp | former-ceo-of-startup-software-company-sentenced-f<br>former-ceo-of-startup-software-company-sentenced-t | sentenced, sentenced |
| Pamela J. Kahut (former Chief Financial Officer, Pacific Sta | former-chief-financial-officer-pleads-guilty-to-th<br>former-chief-financial-officer-sentenced-to-federa | pleaded guilty, sentenced |
| Jariatu Jalloh (community support worker) | former-community-support-worker-pleads-guilty-to-d<br>maryland-woman-arraigned-for-defrauding-the-d-c-me | pleaded guilty, charged |
| Martin Elling (former senior partner, McKinsey & Company); M | former-senior-partner-at-mckinsey-amp-company-plea<br>former-senior-partner-at-mckinsey-amp-company-sent | pleaded guilty, sentenced |
| Richard E. Moore (executive vice president and part owner of | former-virginia-business-owner-pleads-guilty-to-em<br>former-virginia-business-owner-sentenced-for-emplo | pleaded guilty, sentenced |
| Dera Ogudo (operator of United Palliative & Hospice Company) | four-more-charged-in-110-million-hospice-fraud-sch<br>nearly-50-charged-in-southern-district-of-texas-as | charged, charged |
| Lindsay N. McCray (also known as Lindsay Rogers) (employee o | four-pensacola-women-charged-with-illegal-drug-div<br>four-pensacola-women-plead-guilty-to-illegal-drug- | charged, pleaded guilty |
| John Ageudo Rodriguez (pharmacist, owner of Pharr Family Pha | four-sentenced-in-110-million-dollar-kickback-cons<br>pharmacist-guilty-in-110-million-dollar-kickback-c | sentenced, pleaded guilty |
| Felipe Ruiz (podiatrist at West Coast Podiatry Inc.); Jose G | fresno-county-podiatrist-and-sales-representative-<br>fresno-county-podiatrist-and-sales-representative- | sentenced, sentenced |
| Jasmine Hoyle (owner of Harvest Focused & Consulting Service | greensboro-woman-pleads-guilty-to-health-care-frau<br>greensboro-woman-sentenced-in-conviction-with-mult | pleaded guilty, sentenced |
| Gerald Congdon, M.D.; Coastal Urgent Care LLC; Coastal Welln | health-care-providers-and-laboratory-marketers-agr<br>healthcare-providers-and-laboratory-marketers-agre | civil settlement, civil settlement |
| Amstrong Chapajong (personal care aide and community support | healthcare-worker-pleads-guilty-to-double-billing-<br>personal-health-care-aide-charged-with-health-care<br>u-s-attorneys-office-participates-in-record-settin | pleaded guilty, charged, charged |
| Paul Njoku (owner and CEO of Opnet Health Care Services Inc. | home-health-agency-owner-sentenced-to-more-than-si<br>jury-convicts-home-health-agency-owner-in-medicare | sentenced, convicted at trial |
| Krishnaswami Sriram (medical doctor) | illinois-doctor-pleads-guilty-to-evading-approxima<br>illinois-doctor-sentenced-to-34-months-in-prison-f | pleaded guilty, sentenced |
| Mohammed Asif (owner and director of American Labworks LLC); | indian-citizen-charged-in-multi-million-dollar-hea<br>indian-national-sentenced-to-prison-for-medicare-f | charged, sentenced |
| Ndubuisi Joseph Okafor, M.D. (sole practitioner and owner of | jury-finds-physician-guilty-of-operating-a-pill-mi<br>physician-sentenced-to-18-years-in-prison-for-oper | convicted at trial, sentenced |
| Walgreens Boots Alliance Inc.; Walgreen Co. and various subs | justice-department-files-nationwide-lawsuit-allegi<br>middle-district-of-florida-u-s-attorneys-office-co<br>walgreens-agrees-to-pay-up-to-350-million-for-ille<br>walgreens-agrees-to-pay-up-to-350m-for-illegally-f | other, civil settlement, civil settlement, civil settlement |
| Marieva Briceno (owner of three purported medical clinics) | justice-department-secures-denaturalization-of-hea<br>justice-department-secures-denaturalization-of-hea | other, other |
| Seoul Medical Group Inc. (Medicare Advantage provider); Adva | koreatown-based-medicare-advantage-provider-seoul-<br>medicare-advantage-provider-seoul-medical-group-an | civil settlement, civil settlement |
| Munef Fadhel (owner, Great Lake Transportation, Inc.); Great | lackawanna-man-pleads-guilty-to-defrauding-medicai<br>lackawanna-man-sentenced-for-defrauding-medicaid_e | pleaded guilty, sentenced |
| Magaly Travieso (advanced practitioner registered nurse, own | law-enforcement-recovers-over-6-million-in-forfeit<br>law-enforcement-seizes-range-rover-and-over-4-mill | sentenced, charged |
| Dr. Benjamin Tekippe (chiropractor, owner of Metairie Chirop | louisiana-chiropractor-convicted-of-health-care-fr<br>louisiana-chiropractor-sentenced-to-seven-years-in | convicted at trial, sentenced |
| Michael L. Riggins (owner of Bluewater Healthcare); Bluewate | louisiana-man-pleads-guilty-to-3-8-million-durable<br>u-s-attorney-zachary-a-keller-highlights-a-dozen-s | pleaded guilty, sentenced |
| Shanone Chatman-Ashley (nurse practitioner, independent cont | louisiana-nurse-practitioner-convicted-of-2m-medic<br>nurse-practitioner-from-opelousas-convicted-of-med | convicted at trial, convicted at trial |
| Amanda Nicole Manatt (registered nurse) | marshalltown-woman-pleads-guilty-to-charges-relate<br>marshalltown-woman-sentenced-to-six-months-in-fede | pleaded guilty, sentenced |
| Mohammed Rahman (controlled Caltech Trading Corporation); Ca | middlesex-county-man-admits-defrauding-south-korea<br>middlesex-county-man-sentenced-to-27-months-for-de | pleaded guilty, sentenced |
| Jamie P. McNamara (operator/owner of laboratories in Louisia | missouri-man-pleads-guilty-to-multimillion-dollar-<br>missouri-man-sentenced-to-10-years-in-prison-for-1<br>missouri-man-sentenced-to-10-years-in-prison-for-1 | pleaded guilty, sentenced, sentenced |
| David Fuhrmann (national sales director of mobile medical di | national-sales-director-for-new-york-based-mobile-<br>national-sales-director-for-new-york-based-mobile- | charged, pleaded guilty |
| Medsinbox Pharmacy LTC LLC, d/b/a Farmacia San Antonio (phar | new-jersey-pharmacy-agrees-to-resolve-false-claims<br>pharmacy-agrees-to-resolve-false-claims-act-allega | civil settlement, civil settlement |
| Anja Salamack (psychiatric nurse practitioner) | nurse-practitioner-pleads-guilty-to-health-care-fr<br>nurse-practitioner-sentenced-to-18-months-and-orde | pleaded guilty, sentenced |
| Raju Sharma (owner of Pharmagears, LLC and RR Medco, LLC); P | owner-of-durable-medical-equipment-companies-agree<br>owner-of-durable-medical-equipment-companies-charg | charged, charged |
| Kelley Oliver-Hollis (owner, Serenitycare LLC) | owner-of-facility-for-intellectually-disabled-adul<br>superseding-indictment-against-pittsburgh-health-c | pleaded guilty, charged |
| Daniel Dadoun (owner of several New Jersey businesses) | owner-of-new-jersey-businesses-admits-to-fraudulen<br>owner-of-new-jersey-businesses-sentenced-to-41-mon | pleaded guilty, sentenced |
| Pfizer Inc. (parent/acquirer); Biohaven Pharmaceutical Holdi | pfizer-agrees-to-pay-nearly-60-million-to-resolve-<br>pfizer-agrees-to-pay-nearly-60m-to-resolve-false-c | civil settlement, civil settlement |
| James Sessoms | philadelphia-man-pleads-guilty-to-defrauding-the-g<br>philadelphia-man-sentenced-to-over-two-years-in-pr | pleaded guilty, sentenced |
| Neil K. Anand M.D. (physician, owner of in-house pharmacies) | physician-convicted-at-trial-for-illegal-distribut<br>physician-sentenced-to-14-years-for-illegal-distri | convicted at trial, sentenced |
| Cory Lloyd (president of insurance brokerage firm); Steven S | president-of-insurance-brokerage-firm-and-ceo-of-m<br>president-of-insurance-brokerage-firm-and-ceo-of-m | charged, convicted at trial |
| Erik X. Alonso (psychotherapist, excluded provider) | repeat-offender-pleads-guilty-to-health-care-fraud<br>the-new-england-strike-force-joins-nationwide-crac | pleaded guilty, charged |
| Anthony Delmaro (owner of Kings Roofing commercial roofing/p | roofing-contractor-admits-tax-evasion-scheme_36ccd<br>roofing-contractor-sentenced-to-15-months-in-priso | pleaded guilty, sentenced |
| Robert Tassin, M.D. (physician, independent contractor for t | slidell-doctor-charged-with-health-care-fraud_af3d<br>slidell-doctor-convicted-of-health-care-fraud_899d | charged, pleaded guilty |
| Unified Care Services LLC (skilled nursing facilities chain) | south-bay-based-nursing-facilities-chain-and-owner<br>unified-care-services-llc-agrees-to-pay-18m-to-set | civil settlement, civil settlement |
| Patrick Britton-Harr (owner of Provista Health and AeroVanti | south-carolina-man-charged-for-multimillion-dollar<br>south-carolina-man-charged-in-maryland-for-multi-m | charged, charged |
| Ashley Hymel (executive assistant at Company 1) | st-charles-parish-woman-charged-with-wire-fraud_51<br>st-charles-parish-woman-convicted-of-wire-fraud_04 | charged, pleaded guilty |
| Dr. Asim Muhammad Ali (physician, owner of Central Diagnosti | st-louis-area-doctor-sentenced-to-70-months-in-pri<br>two-st-louis-area-doctors-admit-health-crimes_e78f | sentenced, pleaded guilty |
| Aetna Inc. and affiliates (Medicare Advantage insurer); Elev | the-united-states-files-false-claims-act-complaint<br>united-states-files-complaint-against-several-nati | charged, charged |
| John Christopher Barrilleaux (social worker) | thibodaux-social-worker-sentenced-to-30-months-for<br>thibodaux-social-worker-sentenced-to-30-months-for | sentenced, sentenced |
| Kevan Andre Hills; Devin Tyrone Stampley, Jr.; Asia Deshan G | three-baton-rouge-individuals-plead-guilty-in-fede<br>three-baton-rouge-individuals-sentenced-to-federal | pleaded guilty, sentenced |
| Amy Winslow (former CEO, Magellan Diagnostics, Inc.); Hossei | three-former-executives-for-magellan-diagnostics-p<br>three-former-executives-for-magellan-diagnostics-s | pleaded guilty, sentenced |
| Health First Urgent Care (urgent care clinic, Richland and P | tri-cities-urgent-care-clinic-agrees-to-pay-2-8-mi<br>tri-cities-urgent-care-clinic-agrees-to-pay-2-8-mi | civil settlement, civil settlement |
| Local Initiative Health Authority for Inland Empire Health P | united-states-files-lawsuit-against-san-bernardino<br>united-states-files-suit-against-california-based- | other, charged |

# Pattern analysis

## Recurring scheme patterns

### 1. Manufactured orders: telemarketing → "telemedicine" signature → supplier billing
This is the single most frequent mechanic in the sample and the one that produces the largest dollar figures. The structure is consistent: a call center (often offshore) harvests beneficiary identifiers, a marketing entity converts the lead into a pre-populated order, a licensed prescriber signs it for a per-order fee without examining or often without speaking to the patient, and a DME supplier, lab, or pharmacy bills the payer and pays the marketer a per-order kickback disguised as a flat "marketing" or "business process outsourcing" contract.

- Platform-level: Gary Cox / Power Mobility Doctor Rx (DMERx) and Gregory Schreck industrialized the signature step — DMERx generated orders and connected suppliers, pharmacies, and marketers to telemedicine companies, supporting >$1B billed and >$360M paid.
- Signing prescribers: Tommie Robinson ($6M), John R. Manning ($41M billed, >$812K in kickbacks), David M. Young (13,000+ beneficiaries, ~$475K for signing), Sophie Toya (7,900 prescriptions for 2,600 beneficiaries, ~$120K paid), Jerry Bruggeman (3,100 orders for ~$29,440), Scott Roethle (~$30/order, $674K total), Timothy Sutton, Mohammed Ahmad, Le Thu, Robert Tassin ($30/order), Shanone Chatman-Ashley (left knee brace for an amputee), Scharmaine Lawson Baker (calls under 60 seconds; cervical cancer diagnoses for male patients), David Becerril (average 26 seconds per order, including deceased patients and amputees), Sandra Jackson and Jordona Ndon (civil settlements for signing within seconds of opening).
- Marketer/supplier side: Alan Swiss, Ted Albin/Erin Foley ($38M), Manishkumar Patel ($48M), Jesse Foote ($7.8M), Raheel Naviwala (~$100M), Karlewicz/Romanowski's Empire Pain Center ($127M billed, >$63M kicked back), Aaron Williamsky (20+ NJ DME companies, $172M), Kenneth Kessler/Michael Gomez ($34.8M), Raju Sharma/Krishna Gidwani/Kartik Bhatia, Robert Desselle, Charles Kasbee, Adam Owens (routing kickbacks through a New Zealand company on false hourly invoices).

The same architecture appears for cancer genetic (CGx) testing — Fadel Alshalabi's Crestar Labs ($129M billed, $12M in kickbacks, Dr. Toh paid $20/order), Jamie McNamara ($174M billed in ~18 months), Premier Medical/Freedom Medical (swabs collected at bus stops and dollar stores; up to ~$12,000 per test billed to state Medicaid), and Genexe/Immerge (swabbing at malls, churches, and nursing facilities).

### 2. Nominee/straw ownership and exclusion evasion
Concealment of true control recurs across every service line, usually to hide an excluded or convicted principal or to make the entity disposable.

- Operation Gold Rush (EDNY): a Russia-based organization bought dozens of existing DME suppliers via paid foreign-national nominee owners, falsified corporate records, and billed $10.6B using identities of over a million Americans.
- Petros Fichidzhyan and co-defendants used foreign nationals who had left the U.S. as owners of four sham hospices, and misappropriated identities of doctors (two deceased) for certifications.
- Peter Roussonicolos (five DME suppliers behind nominees, felony convictions concealed), Mark Weinberger (excluded 15 years), Jacobo Melcer and Fernando Valenzuela Ayub (new companies opened under nominees after billing suspension), Kartik Bhatia (new DME company after CMS payment suspension), Chaudhry Ahmed (sham purchase agreement fronting $100M in DME billing), Armen Muradyan (paid a friend $2,000/month to pose as owner of Genex Laboratories), Kablazada/Hussain (nominee lab owners expected to flee), Nita Palma (excluded for prior kickback convictions; hospices held by daughter and husband), Terry Hill Jr. and Kenneth Harrison (excluded owners of behavioral health providers), Erik Alonso (excluded psychotherapist working through a NH telehealth provider — both criminal and a $300,000 LifeWorks settlement), Reginald Fullwood (second entity under a nominee after Medicare scrutiny).

### 3. Phantom services and physically impossible schedules
The most common single label in the set, and the easiest to prove: services billed for time that did not exist or people who could not have received them.

- Impossible volume/time: Rachel Collins (17,000+ claims, 12–24+ hours/day, 96 claims during a Disney World trip), Armand Ntchana (impossible hours, patients hospitalized or deceased), Steven Osbey/Aljihad Shabazz (100+ one-hour in-home visits by one physician in a day; 30,000 hours), Natasha Allmon (>24 hours of counseling in a day, family members as patients), Krameelah Banks (>130 sessions for deceased patients; billing from Florida and Mexico), Xuhan Zhang and Jing Qi Mei (inpatient services after the hospital closed, for nursing-home residents and the dead), Violetta Mailyan (Botox billed while she or the patient was abroad or the beneficiary was in federal prison), Clarence Brown III (services during international vacations and while his license was suspended), George Boykins (billed while outside the U.S. and while being interviewed by law enforcement), Absolute Physical & Aquatic Therapy (613 claims for a therapist who was on cruises).
- Time-sheet and visit-verification manipulation: Sola, Inc. (nursing units exceeding hours on time sheets), Favorite Home Care (owners personally placing EVV calls while absent), Amstrong Chapajong (overlapping personal care and behavioral health shifts, contradicted by EVV), Jacquelyn Farrish and Jamahl Burch (Virginia consumer-directed care timesheets for attendants who lived hundreds of miles away).
- Never-dispensed drugs: West End Services, five NJ pharmacies, A Plus, Medsinbox, People's Rx, Nestor Jaime (Dificid), Raad/Ramis Kouza, Nabil Fakih, Isaiah Okoh, the four Michigan pharmacist owners, Prime Aid, and SarJo Pharmacy (FECA). Walgreens' $106.8M exposure in the MDFL summary is the same idea at chain scale — prescriptions processed but never picked up.

### 4. Kickbacks papered as legitimate business relationships
Almost no case in the sample uses undisguised cash at the corporate level; the payment is dressed as rent, directorship, consulting, marketing, or "investment return."

- Rent/space: Niranjan Mittal (office-space "rent" to referring providers; $40M paid on referred patients); mobile TCD scan cases (Rausch, Fuhrmann, Doyle) used "fair market value" rental and administrative agreements to pay ~$100 per brain scan, ~$70.6M billed.
- Medical directorships/stipends: Creative Hospice (stipends scaling with referred patients, $9.2M), Dr. Patterson/Nursemind, Catholic Health System (above-FMV administrative arrangements, Stark), NY-Presbyterian Hudson Valley (>$4M for directorship work not performed).
- Sham marketing service agreements: GTI ($4,000–4,500/month per facility) and Patients Choice Laboratories ($5,000/month plus volume-based 1099 commissions) — both then stacked respiratory pathogen panels onto COVID swabs.
- MSO "investment distributions": True Health/Boston Heart/Little River (Grottenthaler, Kash, Love, Madison and physician investors), and the RiteRx4U/Naghshbandi settlements — the same structure resolved civilly in three districts.
- Speaker programs and meals: Gilead ($202M; >$20M honoraria, 157 James Beard House events), Pfizer/Biohaven ($59.7M, Nurtec ODT), Assertio/Depomed (Lazanda), Insys ($48.3M restitution collected).
- Device consulting/Open Payments: Aesculap (consulting fees, travel, entertainment to a Georgia surgeon); Kingsley Chin/SpineFrontier (a $4,750 "consulting" payment reported to Open Payments with no work performed).
- Beneficiary inducements: Zakia Khan's $68M adult day care scheme (cash bribes to Medicaid recipients), Life Touch (>$1M in gift cards keyed to attendance days), Community Health Care Solutions, NUWAY ($18.5M), Precious Cruse and Markita Barnes (baby goods and cash to enroll prenatal care coordination clients), Connecticut dental practices paying per-Medicaid-patient recruiting fees (Bethi, Makar/Losin, Advanced Dental).

### 5. Upcoding a cheap service into an expensive procedure code
A remarkably tight cluster: taped-on auricular electro-acupuncture devices (P-Stim/Stivax) billed as surgically implanted neurostimulators — Ajay Aggarwal ($2.05M), Benjamin Tiongson, Henry Goolsby, Ronald Ambrosia, Richard Akoto ($1.4M judgment), Carrie Musselman, and the Kevin Brown/Lipman/Woo-Ming settlements. Analogous code-substitution: Vohra Wound Physicians (non-surgical debridement billed as surgical, hard-coded in the EMR, plus automatic Modifier 25; $45M), Forefront Dermatology (linear repairs coded as flaps), BioReference (CBC with differential when without was ordered), Desert Imaging (billing under a hospital NPI for higher outpatient rates, hospital keeping 17%), Musselman and Charasika (mid-level services billed as physician services), Seoul Medical Group (fabricated spinal enthesopathy/sacroiliitis codes to inflate MA risk scores, $62.85M).

### 6. Lab overutilization: urine drug testing and respiratory panels
Standing/blanket orders and reflex definitive testing recur: Physicians Toxicology (blanket requisitions and in-office collectors), Genco Lab and Advanced Pain Care (presumptive + definitive same day with no clinical review), Rodney Yentzer/Pain Medicine of York ($10M+ to Medicare), Wendell Randall, Substance Abuse Treatment Labs, Sherif Khalil/Spectra, The Opportunity Alliance (standing orders for three tests a week for a year), Noah Associates (kickbacks to a treatment clinic; tests ordered under a physician's credentials over his objection). The COVID variant is stacking respiratory pathogen panels on nursing-home COVID swabs: Navarro/Shams (~$369M billed), Patients Choice, GTI, and Britton-Harr's Provista ($15M billed, tests for deceased patients).

### 7. Pandemic-program exploitation
HRSA Uninsured Program and OTC test kits were billed with no encounter at all: Zishan Alvi ($14M, diluted reagents), Willie Murray/Lab Tess (126,000+ claims using prisoner and decedent identities), Samad Khan (~400,000 specimen collections billed as level 2–5 E/M), Vincent Thayer, Jamil Elkoussa, Anosh Ahmed, Cemhan Biricik/Fast Lab ($500M billed off a "free test" website that harvested insurance data), Corey Alston, Dennis Peyroux (fabricated audio recordings of beneficiaries "requesting" kits), Rashid Naqvi, and VRA Enterprises (billed January, shipped April, kept the money). PPP/EIDL cases are numerous but mostly ancillary to health care billing.

### 8. Diversion, pill mills, and prescriber-identity capture
Cash-only prescribing (Joel Smithers, 500,000 pills; Ndubuisi Okafor; Adrian Talbot's pre-signed prescriptions; Charise Valentine's warehouse clinic; Duane Dixon's pre-signed blanks), pharmacy "ghosting" (Christopher Obaze, 2.27M pills sold in bulk with no prescriptions), nurse diversion with record falsification (Jacqueline Brewster diluting hydromorphone, Amanda Manatt, Ian Lindsey, Clinton Christian refilling vials with saline, Cristina Schasse), and identity capture of prescribers: Benjamin Washington (SIM swaps to hijack physicians' phone numbers and open e-prescribing accounts; 5,600 prescriptions), Lindsay McCray (forged DEA numbers of her employer physicians), Darrion Brooks, Kevin Whitman (using a hospital's DEA number), and the Kentucky veterinarian case (prescriptions in the names of dead and fictitious dogs).

## What the schemes have in common

- **The order, not the service, is the product.** In the DME/genetic/pain-cream cluster, what changes hands is a signed doctor's order. Medical necessity is decided by marketers; the clinician is a signature vendor paid per unit (Manning, Young, Becerril, Toya, Tassin, Bruggeman). The same logic runs through wound grafts (Gehrke/King: untrained sales reps decided graft size, NPs applied whatever was ordered) and TCD scans.
- **Payment is per-referral but documented as per-hour, per-month, or per-service.** Sham invoices with fabricated hours (Owens, Kasbee, Patrick Moore, Michael Comino), flat-fee marketing contracts masking per-lead pricing (Sharma), MSO distributions, directorships, rent, and speaker honoraria.
- **Ownership is engineered to be deniable and disposable.** Nominees, shell layers, and serial re-enrollment after suspension (Williamsky closing companies one by one to evade audits; Melcer, Valenzuela, Bhatia, Fullwood, Ogudo opening new hospices under straw owners after a search warrant).
- **Documentation is created reactively, to survive audits.** Fabricated charts after a records request (Njoku taping old signatures onto new orders), auto-generated records (Ali Rashan's software), post-hoc notes (Ali Farhan Hassan's Arizona clinics, Zamora-Quezada's employee ultrasound images, Palma's fake charts, Mailyan's falsified response to a grand jury subpoena, Tekippe rewriting charts for an insurer audit, Cruse/Barnes backdating).
- **Vulnerable, low-agency populations are the raw material.** Hospice and dementia patients (Gehrke/King, Arizona wound cases), homeless and substance-using people (Arizona AHCCCS clinics, Casey Mahoney's body brokers, Lloyd/Strong's ACA enrollments), Native American beneficiaries (Kenneth Harrison, AHCCCS), immigrant-language communities (Oleg Beretsky's Russian-speaking seniors; Somali-community autism cases in Minnesota), nursing home residents (RPP stacking).
- **Money exits fast and often offshore.** Crypto and foreign banks (Gold Rush), India (Reddy's ~200 accounts; Muradyan; Asif), Pakistan (Habib's $425,000), Kenya real estate (Asha Hassan), Mexico and crypto (Merida Medical), gold bars and watches (Muhammad/Feroze).
- **The same playbook migrates across payers.** Medicare dominates, but identical mechanics appear in state Medicaid (Minnesota Housing Stabilization Services and EIDBI autism; Virginia consumer-directed care; NC behavioral health), TRICARE/CHAMPVA, VA community care (Cashmir Luke's ~10,000 claims including care for dead veterans), DOL-OWCP and FECA (Nourian's $145M compound creams; Gilmore; SarJo), self-funded employer plans (Amtrak), and even supplemental insurance (the WMATA/AFLAC ring).

## Detection signals for a predictive model

**Provider-level velocity and impossibility (highest-yield, purely claims-derived)**
- Rendering-provider service minutes summed per day exceeding 16–24 hours, or overlapping timestamps across facilities (Collins, Allmon, Ntchana, Chapajong's overlapping EVV, Bruining's 45-minute sessions recorded without AM/PM).
- Claims on dates the provider was demonstrably absent: cross-reference license suspension/revocation dates, exclusion list dates, incarceration, and travel proxies (Brown, Boykins, Blankenship, Jacobsen, Musselman-type patterns; Absolute PT's cruise dates).
- Claims with service dates after beneficiary date of death, or referring-provider date of death (Spears, Asif, Banks, Baldonado's cohort, Naqvi, Sriram, White's group homes).

**Order-concentration and relationship signals**
- Share of a supplier's/lab's claims traceable to a small number of ordering NPIs, and conversely an ordering NPI whose orders concentrate in suppliers with no geographic or specialty relationship to the prescriber (Young: 13,000 beneficiaries; Becerril: WA physician ordering for nationwide leads; Robinson: Alabama physician, MA-charged case).
- Ordering provider specialty–item mismatch (anesthesiologist Roethle ordering DME/CGx; nurse practitioner orders for braces with no prior encounter).
- Absence of any prior or subsequent claim history between the ordering NPI and the beneficiary — no E/M before or after the order. This is the defining feature of nearly every telemedicine case in the set.
- Beneficiary receiving multiple braces (up to nine per patient in Naviwala's supplier), or bilateral/multiple high-cost items in one burst.

**Code-pair and modifier signatures**
- Presumptive and definitive UDT on the same beneficiary/same date without an intervening review (Genco, Advanced Pain Care, Yentzer, Physicians Toxicology).
- Panel components billed individually rather than the bundled code (Health First Urgent Care; Advanced Pain Care's 803XX analyte-by-analyte billing to VA).
- Modifier 25 attached to E/M at abnormally high rates alongside procedures (Halina Snowball; Vohra's EMR auto-appending).
- Neurostimulator implantation codes billed in office place-of-service with no facility, anesthesia, or operating-room claim (the entire P-Stim cluster) — a near-deterministic rule.
- Surgical vs non-surgical debridement ratios per provider (Vohra); flap vs linear repair mix after Mohs (Forefront); CBC-with-differential ratio (BioReference); telehealth originating-site facility fee Q3014 with a home place of service (Med-Surg).
- E/M level distribution shifts at COVID collection sites (Khan: level 2–5 for specimen collection; Austin Emergency Center's drive-through upcoding).

**Pharmacy and DME inventory reconciliation**
- Billed NDC units versus wholesaler acquisition data — this exact test made five NJ pharmacies, A Plus, Medsinbox, People's Rx, and Fakih. Claribel Tan's case gives the numeric form: 4,829 units billed against 369 purchased.
- Refill-timing anomalies from understated days-supply (CVS insulin pens), and dispensed-but-never-picked-up reversals not performed (Walgreens; Randy Yost re-billing returned drugs).

**Enrollment and entity signals (PECOS/claims joins)**
- New supplier with immediate high-volume billing in a narrow HCPCS band, then rapid decline or voluntary termination — the Williamsky "open and close" pattern; Espinosa Leon billed $7.6M in four months.
- Shared addresses, bank accounts, phone numbers, or billing agents across ostensibly unrelated NPIs (Grapevine billing for the Albin/Foley suppliers; Ali's ProMD credentialing 41 sham AHCCCS clinics from Pakistan).
- Ownership churn shortly after a payment suspension or revocation at a related NPI; recently naturalized/foreign-national owners with no prior health care footprint (Gold Rush, Fichidzhyan, Kablazada).
- Beneficiary-address dispersion: a supplier serving beneficiaries nationwide with no local encounter footprint (Habib's Middletown, CT company billing for 400+ beneficiaries nationwide; Merida billing New England from Florida).

**Beneficiary-side signals**
- Beneficiaries with no history of orthopedic, oncologic, or wound care suddenly receiving braces, CGx panels, or amniotic allografts.
- Cohorts of beneficiaries appearing simultaneously in one supplier's claims and traceable to a single event location — COVID testing events at assisted living facilities and adult day cares (Baldonado), health fairs (Crestar), sober homes (Genco, Davenport).
- Duplicate identity reuse: the same beneficiary ID across many unrelated suppliers in a short window, and beneficiary IDs appearing in claims from suppliers in states the beneficiary has never used.

**Cross-program joins**
- Provider simultaneously drawing unemployment/disability while billing (Tekippe, Collins, Salamack's PRF misuse) and providers whose entity received PPP/EIDL/PRF inconsistent with their claims volume.

## Caveats and sample limits

- **These are enforcement documents, not a claims sample.** Every pattern above is conditioned on being detected and charged. The distribution tells you what DOJ prosecuted in 2025, not what fraud exists. Schemes detectable by simple claims rules (impossible hours, dead beneficiaries) are almost certainly over-represented relative to sophisticated medical-necessity fraud.
- **No denominators.** Nothing here supports a base rate, a prior probability, or a false-positive estimate for any signal. A model built from these mechanics needs to be calibrated against legitimate claims data that this corpus does not contain.
- **Roughly 15% of the documents are not health care fraud cases at all** — personnel announcements, annual collections releases, PPP/EIDL-only prosecutions, employment-tax cases, a murder-for-hire, a child-exploitation case, a card-skimming ring. The aggregate counts include them; the health care-specific patterns should be read off the case narratives, not the totals.
- **Dollar fields are not comparable.** FraudAmt variously records amounts billed (Gold Rush's $10.6B billed vs. $41M paid by Medicare), amounts paid, intended loss, or street value of diverted pills. SettlementAmt mixes civil settlements, restitution, forfeiture, and fines, sometimes summed across co-defendants. Any modeling on these numbers will be dominated by definitional noise; the $14.6B takedown figure and the $10.6B Gold Rush figure alone drive most of the total.
- **Duplicate coverage inflates apparent frequency.** 679 documents cover 590 distinct cases, and single matters appear up to four times (Walgreens; Cox/DMERx; Gidwani; McNamara). Repeat coverage is also non-random — larger cases get more releases — so raw document counts overstate big-dollar schemes.
- **Charged ≠ proven.** About a fifth of the records are at the charging stage (Kumar, Chesapeake Regional, the Aetna/Elevance/Humana broker complaint, IEHP, Vohra's complaint before settlement). Civil settlements in this set are almost uniformly stated without admission of liability.
- **Some clusters are too small to generalize.** The P-Stim/neurostimulator pattern (roughly seven matters) and the amniotic wound graft pattern (Gehrke/King, the Arizona takedown, Huntly, Gonzalez, Ruiz/Aguirre, Pinnacle Health) look like distinct waves, but a handful of cases in one or two districts cannot establish a national trend. Similarly, the Minnesota Housing Stabilization Services and autism-EIDBI cases are a single-state phenomenon in this data.
- **Geography reflects prosecutorial capacity, not fraud density.** Florida, California, New York, New Jersey, and Texas lead the state counts; that tracks strike-force placement (the releases explicitly note new units in Massachusetts and Chicago) as much as underlying conduct.
- **Payer labels are coarse.** "Medicaid" spans fee-for-service, managed care organizations, and program-specific waivers with very different data; "commercial payer" is often an unnamed insurer. Medicare Advantage appears both as a risk-adjustment problem (Seoul Medical) and as a broker-kickback problem (the Aetna/Elevance/Humana complaint) — these are different data domains and should not be modeled together.

