# AML and Financial Crime Framework

## BSA/AML Regulatory Structure

| Component | Authority | Key Requirement |
|-----------|-----------|----------------|
| Bank Secrecy Act | US Treasury / FinCEN | Recordkeeping, reporting, compliance programs |
| USA PATRIOT Act | FinCEN | Enhanced due diligence, information sharing, AML programs |
| FINRA Rule 3310 | FINRA | Member firm AML compliance programs |
| OFAC Regulations | US Treasury / OFAC | Sanctions screening and compliance |

## Four Pillars of AML Program (FINRA Rule 3310)

### 1. Written Procedures
- Tailored to the firm's business model, products, customer types, and geographic exposure
- Cover detection, escalation, and reporting of suspicious activity
- Include customer risk rating methodology
- Address all stages: onboarding, ongoing monitoring, investigation, reporting

### 2. Designated AML Compliance Officer (AMLCO)
- Qualified individual with day-to-day AML oversight responsibility
- Identified by name and title in written procedures
- Registered with FINRA
- Must have sufficient authority, resources, and expertise

### 3. Independent Testing (Audit)
- At least every calendar year (or every two years for non-transaction firms)
- Performed by qualified internal personnel not involved in the AML program, or an outside party
- Test covers: policy adequacy, transaction sampling, SAR filing decisions, training effectiveness, OFAC screening, and customer risk rating accuracy

### 4. Ongoing Training
- All relevant personnel must receive AML training appropriate to their responsibilities
- Cover: applicable BSA/AML regulations, firm policies, red flags, escalation procedures
- Document frequency and content

## Currency Transaction Reports (CTRs)

**FinCEN Form 112** — Required for cash transactions exceeding $10,000 in a single business day.

| Rule | Detail |
|------|--------|
| Threshold | $10,000 cash (currency, coin) in a single business day |
| Aggregation | Multiple transactions by same person on same day must be aggregated |
| Filing deadline | 15 calendar days after transaction |
| Structuring prohibition | Federal crime to break transactions into smaller amounts to evade CTR (31 USC § 5324) |
| Exemptions | Listed companies, government agencies, banks (must be documented and reviewed) |

**Structuring is illegal regardless of the source of funds.** Even legitimate funds broken into sub-$10K amounts trigger criminal liability for both the customer and any employee who assists.

## Suspicious Activity Reports (SARs)

**FinCEN Form 111** — Report known or suspected violations of law or suspicious transactions.

| Institution | Threshold | Filing Deadline |
|------------|-----------|----------------|
| Broker-dealers | ≥ $5,000 suspicious activity | 30 days (60 if no suspect identified) |
| Banks | ≥ $5,000 with known suspect; ≥ $25,000 regardless | 30 days (60 if no suspect) |

**Continuing activity:** File continuing SARs at least every 90 days.

**Tipping-off prohibition (31 USC § 5318(g)(2)):** It is a violation to notify the SAR subject that a SAR has been or will be filed. Extends to all employees, officers, and directors.

**Safe harbor (31 USC § 5318(g)(3)):** Protection from civil liability for good-faith SAR filings, even if reported activity turns out to be legitimate.

**SAR confidentiality:** Cannot be produced in response to subpoenas, discovery, or FOIA (with narrow law enforcement exceptions). The underlying facts are not themselves privileged.

## OFAC Sanctions Screening

The Office of Foreign Assets Control administers US economic and trade sanctions.

### Key Lists

| List | What It Covers | Action Required |
|------|---------------|----------------|
| SDN List | Specially Designated Nationals — individuals/entities controlled by sanctioned countries, terrorists, narcotics traffickers | Block (freeze) transactions, report within 10 business days |
| SSI List | Sectoral Sanctions Identifications — specific transaction types restricted | Reject prohibited transaction types |
| Country sanctions | Comprehensive programs for Cuba, Iran, North Korea, Syria, Crimea | Block or reject all transactions |

### Screening Requirements

- **When:** Account opening, transaction receipt, list updates
- **What:** Names, aliases, addresses, DOB, passport numbers, all identifiers
- **Strict liability:** Penalties even without knowledge of sanctions status
- **Voluntary self-disclosure:** Significant mitigating factor in enforcement

## Money Laundering Red Flags

Money laundering follows three stages: placement → layering → integration.

### Placement Red Flags
- Cash deposits or withdrawals just below $10,000
- Multiple deposits at different branches on the same day
- Large cash deposits from businesses that typically don't deal in cash

### Layering Red Flags
- Rapid movement of funds (received and immediately wired out)
- Multiple transfers between accounts at different institutions
- Frequent conversion between asset types with no business purpose
- Round-dollar transactions with no apparent rationale
- Use of intermediary accounts or shell companies

### Integration Red Flags
- Purchase of high-value assets with funds of unclear origin
- Investment accounts generating appearance of legitimate returns from illicit funds
- Accounts held by entities with no apparent business operations, nominal capital, or nominee directors
- Unexplained wealth inconsistent with known employment

### Customer Behavior Red Flags
- Reluctance to provide identification or information
- Use of multiple SSNs or TINs
- Frequent changes to account ownership or signatory authority
- Wire transfers to high-risk jurisdictions without business explanation
- No economic rationale for transaction speed or complexity

## SAR Decision Framework

When evaluating whether to file a SAR:

1. **Is the activity suspicious?** Does it lack apparent lawful purpose, involve potentially illegal funds, or appear designed to evade BSA requirements?
2. **Does it meet the threshold?** ≥ $5,000 for broker-dealers
3. **Is there a reasonable explanation?** If the customer provides a satisfactory explanation and documentation, a SAR may not be necessary — but document the review
4. **File within deadlines:** 30 days from initial detection (60 if no suspect)
5. **Document everything:** The investigation, analysis, and filing decision (whether or not you file)

## FinCEN Information Sharing

- **Section 314(a):** Law enforcement can request financial institutions search for accounts or transactions of persons suspected of terrorism or money laundering. Institutions must respond within 2 weeks.
- **Section 314(b):** Voluntary information sharing between financial institutions about suspicious activity. Provides safe harbor from liability for sharing.
