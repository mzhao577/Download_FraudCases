"""The extraction schema.

Field names and the FraudType taxonomy come from instruction_extractInfo.md.
That file is the source of truth: when the taxonomy changes there, change
FRAUD_TYPES and FRAUD_TYPE_GUIDE here to match.

Deviations from the brief, all deliberate and all listed in the instruction file:
  * `urisdictionName` is read as `JurisdictionName` (dropped J), and `jailTime`
    is normalised to `JailTime`, so every column is PascalCase.
  * Taxonomy labels are spelling-corrected ("Upcodiong" -> "Upcoding",
    "Other - Unknow" -> "Other - Unknown", "Device, DE" -> "Device, DME") and
    shortened to a stable key, because these strings become categorical values
    in a model and must not carry typos.
  * `FraudTypeAll`, `CaseStatus` and `SchemeSummary` are added. A single case
    routinely combines two schemes (kickbacks *and* phantom claims), and the
    stated goal is finding the patterns fraudsters use - one primary label alone
    throws away most of that signal.
"""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

# The 18-type taxonomy from instruction_extractInfo.md. This is a CLOSED set:
# anything that fits none of these is "Other - Unknown". Declaring it as a
# Literal makes structured outputs enforce it, so an invalid label cannot be
# returned at all.
FRAUD_TYPES = [
    "Phantom Claims",
    "FakeEncounter",
    "Upcoding",
    "Unbundling",
    "Falsify certificate",
    "kickback_Bribery For Referral",
    "Drug_Prescriptions",
    "Benefit & Eligibility Fraud",
    "Wire Fraud",
    "Covid or General Loan Fraud",
    "Tax, Payroll or Coupon Fraud",
    "IdentityFraud",
    "Device, DME",
    "Other - Embezzlement of federal grant funds",
    "Other - FDA Submission Fraud",
    "Other - Arson insurance fraud",
    "Retention of Overpayment",
    "Other - Unknown",
]

FraudTypeLiteral = Literal[
    "Phantom Claims",
    "FakeEncounter",
    "Upcoding",
    "Unbundling",
    "Falsify certificate",
    "kickback_Bribery For Referral",
    "Drug_Prescriptions",
    "Benefit & Eligibility Fraud",
    "Wire Fraud",
    "Covid or General Loan Fraud",
    "Tax, Payroll or Coupon Fraud",
    "IdentityFraud",
    "Device, DME",
    "Other - Embezzlement of federal grant funds",
    "Other - FDA Submission Fraud",
    "Other - Arson insurance fraud",
    "Retention of Overpayment",
    "Other - Unknown",
]

FRAUD_TYPE_GUIDE = """
 1) Phantom Claims - billing for encounters, visits or items that never happened
    at all, including billing for dead, incarcerated, hospitalised or absent
    patients.
 2) FakeEncounter - an encounter did occur but was fabricated or staged to
    create a billable event: sham visits, recruited or paid patients, services
    by unlicensed or unqualified staff, services not medically necessary.
 3) Upcoding - a real service billed under a higher-paying code, level of care,
    acuity or risk-adjustment diagnosis than what was actually delivered.
 4) Unbundling - one bundled or global service split into component codes to
    collect more than the bundled rate.
 5) Falsify certificate - falsified certifications, plans of care, physician
    orders, timesheets, licences, training certificates or medical records used
    to make an otherwise unpayable claim payable.
 6) kickback_Bribery For Referral - payments, bribes or anything of value for
    patient referrals or to induce ordering of services; includes Anti-Kickback
    Statute and Stark Law self-referral cases.
 7) Drug_Prescriptions - anything centred on drugs or prescriptions: pill mills,
    diversion, medically unnecessary prescribing, compounding schemes,
    prescription forgery, drug adulteration or misbranding.
 8) Benefit & Eligibility Fraud - fraud about who is entitled to participate or
    be covered: concealed ownership, nominee owners, enrolment by an excluded or
    disqualified person, false enrolment or participation certifications, false
    beneficiary eligibility.
 9) Wire Fraud - laundering or moving the proceeds; shell companies, structured
    transfers, wire and mail fraud counts centred on moving money.
10) Covid or General Loan Fraud - PPP, EIDL, Provider Relief Fund, COVID
    testing/vaccine funds, or other government loan and grant programme fraud.
11) Tax, Payroll or Coupon Fraud - tax evasion, employment-tax and payroll
    fraud, ghost employees, coupon or rebate fraud.
12) IdentityFraud - theft or misuse of patient, provider or beneficiary
    identities, including aggravated identity theft and stolen Medicare numbers.
13) Device, DME - durable medical equipment, orthotics, prosthetics, braces and
    medical device schemes.
14) Other - Embezzlement of federal grant funds - diversion of federal grant
    money.
15) Other - FDA Submission Fraud - false or misleading submissions to the FDA.
16) Other - Arson insurance fraud - arson or property-insurance fraud.
17) Retention of Overpayment - knowingly keeping a payment known to be
    unearned, including failure to report and return an identified overpayment.
18) Other - Unknown - use ONLY when nothing above fits. Do not invent a new
    label; this taxonomy is closed.
""".strip()

# Suggested values for Service. Open-ended by design ("such as ... etc." in the
# brief), so this steers the vocabulary without constraining it.
SERVICE_EXAMPLES = (
    "HomeHealth, PersonalCare, NursingHome, Hospice, AdultDayCare, "
    "BehavioralHealth, SubstanceUseTreatment, Pharmacy, Laboratory, "
    "GeneticTesting, DME, Telehealth, PhysicianPractice, Hospital, Dental, "
    "Ambulance, Transportation, Optometry, Chiropractic, Podiatry, Other"
)


class CaseRecord(BaseModel):
    """One medical fraud case, extracted from one source document."""

    ReportDT: Optional[str] = Field(
        description="Publication date of the document, yyyy-mm-dd. Null if absent."
    )
    JurisdictionName: Optional[str] = Field(
        description="The prosecuting office and/or court, as named in the document - "
                    "e.g. 'U.S. Attorney's Office, Eastern District of New York' or "
                    "'U.S. District Court for the District of New Jersey'. Null if absent."
    )
    OccurDt: Optional[str] = Field(
        description="When the fraud occurred, as a period 'yyyy-mm to yyyy-mm'. "
                    "Use 'yyyy to yyyy' if only years are given, and a single value "
                    "if the document gives only one date. Null if the document never "
                    "says when the conduct happened. This is the conduct period, NOT "
                    "the charging, plea, or sentencing date."
    )
    FraudEntity: Optional[str] = Field(
        description="The individual(s) and/or company(ies) that committed the fraud. "
                    "Semicolon-separated if several. Include a role in parentheses "
                    "where the document gives one, e.g. 'Jane Doe (owner)'. Do not "
                    "list prosecutors, agents, judges, or victim payers here."
    )
    Service: Optional[str] = Field(
        description="Type of health care service involved, semicolon-separated if "
                    f"several. Use these values where they fit: {SERVICE_EXAMPLES}. "
                    "Coin a short CamelCase label only if none fits. Null if the "
                    "document identifies no health care service (for example a pure "
                    "loan-fraud case). This is the service line, NOT the fraud "
                    "scheme - never put one of these values in FraudType."
    )
    State_County: Optional[str] = Field(
        description="State and county/city where the fraud occurred, e.g. "
                    "'New York - Kings County (Brooklyn)'. Semicolon-separated and "
                    "combined into one string if several. Null if absent."
    )
    PayerName: Optional[str] = Field(
        description="The payer(s) defrauded: Medicare, Medicaid (name the state "
                    "programme if given), TRICARE, or a named commercial insurer. "
                    "Semicolon-separated if several."
    )
    FraudAmt: Optional[float] = Field(
        description="Total dollar amount of the fraud - amount billed, claimed, or "
                    "the loss, in whole US dollars with no symbols or commas. Null "
                    "if the document gives no amount. If the document gives both a "
                    "billed amount and a paid/loss amount, use the larger (billed)."
    )
    SettlementAmt: Optional[float] = Field(
        description="Civil settlement, judgment, restitution, forfeiture or fine the "
                    "defendant agreed or was ordered to pay, in whole US dollars. "
                    "Null if none stated. This is money flowing back, and is distinct "
                    "from FraudAmt. Where several defendants owe separate amounts, "
                    "give the total across all of them."
    )
    JailTime: Optional[int] = Field(
        description="Custodial sentence actually imposed, in MONTHS (convert years: "
                    "3 years = 36). Where several defendants were sentenced, give the "
                    "LONGEST sentence imposed in the case. Null only if nobody in the "
                    "case has been sentenced to custody yet. Do NOT use the maximum "
                    "penalty faced, the statutory maximum, probation, or a "
                    "supervised-release term - only custody actually handed down."
    )
    FraudType: FraudTypeLiteral = Field(
        description="The single most central scheme type. Must be one of the 18 "
                    "taxonomy values; use 'Other - Unknown' if none fits."
    )
    FraudTypeAll: List[FraudTypeLiteral] = Field(
        description="Every scheme type present in the case, most central first. One "
                    "element when only one applies. Same closed 18-value taxonomy - "
                    "a service type such as GeneticTesting, Laboratory or HomeHealth "
                    "belongs in Service and must never appear here."
    )
    CaseStatus: Optional[str] = Field(
        description="Stage of the case as of the document: one of 'charged', "
                    "'pleaded guilty', 'convicted at trial', 'sentenced', "
                    "'civil settlement', or 'other'."
    )
    SchemeSummary: Optional[str] = Field(
        description="One or two sentences on the actual mechanics: what was billed, "
                    "to whom, and how the money was obtained. Concrete, not generic - "
                    "this is what makes the case useful for pattern analysis."
    )


# CSV column order follows the field order in instruction_extractInfo.md.
# DocumentName is filled in from the filename, not by the model.
CSV_COLUMNS = [
    "DocumentName",
    "ReportDT",
    "JurisdictionName",
    "OccurDt",
    "FraudEntity",
    "Service",
    "State_County",
    "PayerName",
    "FraudAmt",
    "SettlementAmt",
    "JailTime",
    "FraudType",
    "FraudTypeAll",
    "CaseStatus",
    "SchemeSummary",
]
