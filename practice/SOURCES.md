# Sources searched for medical / health care fraud cases

Coverage: documents dated **2021-01-01** or later.

This file is generated from [`sources.json`](sources.json), which is what the
scrapers actually read. Edit the JSON, not this file.

## DOJ - U.S. Department of Justice (Main Justice + all 93 U.S. Attorney's Offices)

**Why this source.** Primary publisher of federal health care fraud criminal charges, convictions, sentencings, False Claims Act civil settlements and the annual National Health Care Fraud Takedowns. Covers Medicare, Medicaid, TRICARE and private/commercial insurers.

**Websites searched**

- <https://www.justice.gov/news>
- <https://www.justice.gov/criminal/criminal-fraud/health-care-fraud-unit>
- <https://www.justice.gov/civil/false-claims-act>
- <https://www.justice.gov/opa/pr>

**How.** official JSON API, paginated newest-first, then filtered on the 'Healthcare Fraud' topic tag and on health-care-fraud keywords

- `https://www.justice.gov/api/v1/press_releases.json?pagesize=50&page={n}&sort=date&direction=DESC`

*Note:* justice.gov HTML is behind an Akamai bot-manager interstitial, so pages are fetched with headless Chrome; if that fails the press release is rebuilt from the API 'body' field. PDF attachments (indictments, complaints, settlement agreements) are downloaded as well.

**Document types:** press release, indictment/complaint PDF, settlement agreement PDF

## HHS-OIG - U.S. Department of Health and Human Services, Office of Inspector General

**Why this source.** Publishes the government-wide enforcement-action database (criminal, civil and Civil Monetary Penalty actions, including state Medicaid Fraud Control Unit cases), audits and evaluations of Medicare/Medicaid improper payments, and the LEIE exclusions list.

**Websites searched**

- <https://oig.hhs.gov/fraud/enforcement/>
- <https://oig.hhs.gov/reports/all/>
- <https://oig.hhs.gov/exclusions/>
- <https://oig.hhs.gov/fraud/medicaid-fraud-control-units-mfcu/>

**How.** paginated HTML listings (20 items/page, newest first) walked until the coverage cut-off date; reports are keyword-filtered and their full-text PDFs are downloaded too

- `https://oig.hhs.gov/fraud/enforcement/?page={n}`
- `https://oig.hhs.gov/reports/all/?page={n}`

**Document types:** enforcement action, audit report, evaluation report, CMP action, MFCU annual report, LEIE data file

## FBI - Federal Bureau of Investigation (national + 55 field offices)

**Why this source.** Lead investigative agency for federal health care fraud; field-office press releases cover cases against Medicare, Medicaid and private/commercial insurers.

**Websites searched**

- <https://www.fbi.gov/news/press-releases>
- <https://www.fbi.gov/investigate/white-collar-crime/healthcare-fraud>
- <https://www.fbi.gov/contact-us/field-offices>

**How.** full site sitemap is downloaded and every /news/press-releases/ and field-office press-release URL is keyword-matched, then each candidate page is fetched and filtered on its published date

- `https://www.fbi.gov/sitemap.xml.gz`

**Document types:** press release, story, program page

## CMS - Centers for Medicare & Medicaid Services

**Why this source.** Payer-side program-integrity announcements, Medicare/Medicaid improper-payment and fraud-prevention reporting, provider-enrollment moratoria and Strike Force partnership news.

**Websites searched**

- <https://www.cms.gov/about-cms/contact/newsroom>
- <https://www.cms.gov/data-research/monitoring-programs/medicare-fee-service-compliance-programs>
- <https://www.cms.gov/data-research/monitoring-programs/improper-payment-measurement-programs>

**How.** newsroom sitemap is downloaded and press releases / fact sheets / news alerts are keyword-matched, then fetched with headless Chrome (cms.gov blocks plain HTTP clients) and filtered on published date

- `https://www.cms.gov/sitemap-newsroom.xml`

**Document types:** press release, fact sheet, news alert, program-integrity report

## GAO - U.S. Government Accountability Office

**Why this source.** Independent audits and testimony on Medicare/Medicaid fraud risk, improper payments and program-integrity oversight - useful context documents for the case corpus.

**Websites searched**

- <https://www.gao.gov/reports-testimonies>
- <https://www.gao.gov/health-care>

**How.** faceted reports-and-testimonies listing browsed with headless Chrome (gao.gov blocks plain HTTP clients); each product page plus its full-text PDF is saved

- `https://www.gao.gov/reports-testimonies?page={n}`

**Document types:** report, testimony, report PDF

## Considered but not scraped

- **NHCAA (National Health Care Anti-Fraud Association)** (<https://www.nhcaa.org/>) - Commercial-payer case material is behind a members-only login; only high-level statistics are public.
- **State Medicaid Fraud Control Unit websites (50 states)** (<https://oig.hhs.gov/fraud/medicaid-fraud-control-units-mfcu/>) - State MFCU press releases are already syndicated into the HHS-OIG enforcement database, which is scraped instead.
- **PACER / CourtListener dockets** (<https://www.courtlistener.com/>) - Underlying court filings are useful but require per-document fees or a separate API key; DOJ press-release attachments cover the key filings.

