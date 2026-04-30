# KYC and Client Onboarding Framework

## Regulatory Requirements

Client onboarding in the US is governed by overlapping federal and self-regulatory requirements:

| Requirement | Rule | Purpose |
|------------|------|---------|
| Know Your Customer | FINRA Rule 2090 | Know essential facts about every customer |
| Customer Identification | USA PATRIOT Act §326 / CIP | Verify customer identity at account opening |
| Customer Due Diligence | FinCEN CDD Rule (31 CFR 1010.230) | Beneficial ownership + ongoing monitoring |
| Suitability Profile | FINRA Rule 2111 | Gather profile for recommendation suitability |
| OFAC Screening | OFAC regulations | Screen against sanctions lists |

## FINRA Rule 2090 — Know Your Customer

Must use reasonable diligence to know and retain the essential facts concerning every customer and the authority of each person acting on their behalf.

**Essential facts** are those required to:
- Effectively service the account
- Act in accordance with special handling instructions
- Understand the authority of each person acting for the customer
- Comply with applicable laws, regulations, and rules

## Customer Identification Program (CIP)

Required under USA PATRIOT Act Section 326. Must include:

### Information Collection
| Data Point | Individuals | Legal Entities |
|-----------|------------|----------------|
| Name | Full legal name | Legal entity name |
| Date of birth | Required | N/A (formation date for entities) |
| Address | Physical address (no PO boxes as sole address) | Principal place of business |
| ID number | SSN (US) or passport number + country (non-US) | EIN/TIN |

### Verification Methods

**Documentary:** Unexpired government-issued photo ID (driver's license, passport, state ID). For entities: articles of incorporation, partnership agreement.

**Non-documentary:** Credit bureau inquiries, public database searches (LexisNexis, etc.), financial statement review. Required when:
- Customer not physically present (online account opening)
- Documents are unfamiliar
- Other circumstances increase risk

### Recordkeeping
- Retain identifying information and verification records for 5 years after account closure
- Maintain records of verification methods used

### Government List Screening
- Check customer names against OFAC SDN list and other government terrorist/sanctions lists at account opening

## Beneficial Ownership (CDD Rule)

For legal entity customers, identify:

1. **Ownership prong:** Each individual owning ≥ 25% of equity interests
2. **Control prong:** One individual with significant responsibility for managing the entity (CEO, CFO, COO, Managing Member, General Partner, etc.)

**Exempt entities:** Publicly traded companies, regulated financial institutions, government entities, entities registered with the SEC, insurance companies.

## Enhanced Due Diligence (EDD)

Higher-risk customers require additional scrutiny:

| Risk Factor | EDD Measures |
|------------|-------------|
| Politically Exposed Persons (PEPs) | Source of wealth verification, senior management approval |
| Foreign correspondent accounts | Heightened due diligence per BSA Section 312 |
| High-risk jurisdictions (FATF-flagged) | Enhanced transaction monitoring, more frequent reviews |
| Complex ownership structures | Trace through all layers, identify ultimate beneficial owners |
| Unusual account activity | Investigate deviations from expected patterns |

## Suitability Profile Collection

For making recommendations under Reg BI or FINRA suitability rules, collect:

| Factor | Questions to Ask |
|--------|-----------------|
| Investment objectives | What is the primary goal? (growth, income, preservation, speculation) |
| Time horizon | When will funds be needed? |
| Risk tolerance | How much loss can you tolerate? (willingness + capacity) |
| Financial situation | Income, net worth, liquid assets, liabilities |
| Investment experience | What types of investments have you owned? |
| Tax status | What is your marginal tax bracket? Account types available? |
| Liquidity needs | Any anticipated large expenses? |
| Existing holdings | What do you currently own? Any concentrated positions? |

A customer may decline to provide information. Document the refusal — the more information withheld, the narrower the range of suitable recommendations.

## Ongoing Monitoring Triggers

KYC is not a one-time event. Update the profile when:

- Material life events (retirement, marriage/divorce, inheritance, job change)
- Transaction patterns deviate from the established profile
- Customer provides new information
- Regulatory changes require additional data
- Periodic risk-based review (annual for high-risk, every 3 years for standard)

## Onboarding Checklist

1. Collect CIP identification information
2. Verify identity (documentary and/or non-documentary)
3. Screen against OFAC SDN list
4. Collect beneficial ownership (for legal entities)
5. Complete suitability profile questionnaire
6. Assign customer risk rating
7. Deliver Form CRS (for broker-dealer or investment adviser)
8. Obtain required agreements and disclosures
9. Set up account in compliance systems
10. Schedule first periodic review based on risk rating
