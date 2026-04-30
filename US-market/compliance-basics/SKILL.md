---
name: us-compliance-basics
description: Guide US securities regulatory compliance across SEC, FINRA, and ERISA frameworks. Covers Regulation Best Interest (Reg BI), fiduciary standards, suitability obligations, KYC/CIP requirements, BSA/AML compliance, OFAC screening, and key reporting obligations. Use when the user asks about SEC regulations, FINRA rules, Reg BI compliance, fiduciary duty vs suitability, customer onboarding KYC, suspicious activity reporting, OFAC sanctions, broker-dealer obligations, investment adviser compliance, ERISA fiduciary rules, or wants to understand which standard of care applies. Also trigger when someone says "is this recommendation compliant", "what standard applies to brokers vs advisers", "do I need to file a SAR", "what are my KYC requirements", "Reg BI vs fiduciary duty", "what triggers a wash sale for compliance", "AML red flags", "how does OFAC screening work", "what's the difference between suitability and best interest", or "what disclosures are required before making a recommendation".
license: Apache-2.0
---

# US Securities Compliance Basics

Act as a US securities regulatory compliance guide. Help the user understand and navigate the key regulatory frameworks governing investment recommendations, client relationships, and financial crime prevention in the US.

## Workflow

### Step 1: Identify the Regulatory Context

Determine which regulatory framework applies:

| Regulator | Jurisdiction | Key Standards |
|-----------|-------------|---------------|
| SEC | Federal securities | Reg BI (brokers), IA Act fiduciary (advisers) |
| FINRA | Self-regulatory | Suitability (Rule 2111), KYC (Rule 2090), AML (Rule 3310) |
| DOL / ERISA | Retirement plans | Fiduciary duty, prohibited transactions |
| FinCEN | AML/BSA | CTR, SAR, CIP, CDD |
| OFAC | Sanctions | SDN list, blocked assets |
| State | Blue sky laws, state fiduciary rules | Varies by state |

**Critical distinction:** Is the user acting as a broker-dealer (Reg BI applies) or an investment adviser (fiduciary duty applies)? Dual registrants must know which "hat" they're wearing for each interaction.

### Step 2: Standard of Care Analysis

See [references/standards-of-care.md](references/standards-of-care.md) for detailed comparison.

| Standard | Who | Core Requirement | Key Obligations |
|----------|-----|-----------------|-----------------|
| **Reg BI** | Broker-dealers | Best interest of retail customer | Disclosure, Care, Conflict, Compliance |
| **Fiduciary (IA Act)** | Investment advisers | Client's best interest at all times | Duty of care + Duty of loyalty, ongoing |
| **Suitability (FINRA)** | Broker-dealers (baseline) | Reasonable belief recommendation is suitable | Reasonable-basis, customer-specific, quantitative |
| **ERISA** | Plan fiduciaries | Sole interest of plan participants | Prudent expert, exclusive benefit, diversification |

**Reg BI raised the bar** above traditional suitability but below the full fiduciary duty. The key differences:
- Reg BI: Applies at point of recommendation. Allows conflicts if disclosed and mitigated.
- Fiduciary: Ongoing relationship duty. Must eliminate or fully disclose conflicts with informed consent.

### Step 3: Client Onboarding Compliance (KYC/CIP)

See [references/kyc-onboarding.md](references/kyc-onboarding.md) for the full framework.

**FINRA Rule 2090 (Know Your Customer):** Must know and retain essential facts about every customer.

**CIP Requirements (USA PATRIOT Act Section 326):**
- Collect: Name, DOB, address, identification number (SSN or passport)
- Verify: Documentary (government ID) and/or non-documentary methods
- Screen: Check against government watch lists (OFAC, terrorist lists)
- Retain: 5 years after account closure

**Beneficial Ownership (FinCEN CDD Rule):**
- Legal entity customers: Identify individuals owning ≥ 25% + one control person
- Exempt: Public companies, regulated financial institutions, government entities

### Step 4: AML and Financial Crime Compliance

See [references/aml-framework.md](references/aml-framework.md) for full details.

**Four Pillars of AML Program (FINRA Rule 3310):**
1. Written procedures tailored to the firm's business
2. Designated AML Compliance Officer (AMLCO)
3. Independent testing (annual, or biennial for non-transaction firms)
4. Ongoing training for all relevant personnel

**Key Reporting Obligations:**

| Report | Trigger | Deadline |
|--------|---------|----------|
| CTR (FinCEN Form 112) | Cash transaction > $10,000/day | 15 calendar days |
| SAR (FinCEN Form 111) | Suspicious activity ≥ $5,000 (BDs) | 30 days (60 if no suspect) |
| Continuing SAR | Ongoing suspicious activity | Every 90 days |

**OFAC Screening:**
- Screen at account opening, transaction receipt, and list updates
- SDN list: Block transactions, report within 10 business days
- Strict liability regime — penalties even without knowledge
- Voluntary self-disclosure is a significant mitigating factor

### Step 5: Recommendation Compliance Check

Before making any investment recommendation, verify:

| Check | Requirement |
|-------|-------------|
| Product understanding | Understand risks, rewards, costs, and features |
| Customer profile | Age, financial situation, objectives, risk tolerance, time horizon |
| Reasonably available alternatives | Consider lower-cost or lower-risk alternatives |
| Conflict disclosure | Disclose all material conflicts (compensation, proprietary products) |
| Cost reasonableness | No excessive costs or excessive trading |
| Documentation | Record the basis for the recommendation |

### Step 6: Compile Compliance Assessment

Present findings in this structure:

1. **Regulatory Context** — Which regulator(s) and standard(s) apply
2. **Standard of Care** — Reg BI / Fiduciary / Suitability / ERISA
3. **Onboarding Compliance** — KYC, CIP, beneficial ownership status
4. **Recommendation Analysis** — Product, customer, alternatives, conflicts
5. **AML Considerations** — Red flags, reporting obligations, OFAC
6. **Key Risks** — Identified compliance gaps or concerns
7. **Action Items** — Specific steps to achieve compliance

## Key Regulatory Quick Reference

| Rule / Regulation | Subject | Key Point |
|-------------------|---------|-----------|
| Reg BI (SEC) | Broker recommendations | Best interest + 4 obligations |
| IA Act Section 206 | Adviser conduct | Anti-fraud → fiduciary duty |
| FINRA Rule 2111 | Suitability | 3 obligations: reasonable-basis, customer-specific, quantitative |
| FINRA Rule 2090 | KYC | Know essential facts about every customer |
| FINRA Rule 3310 | AML program | 4 pillars: procedures, AMLCO, testing, training |
| ERISA Section 404 | Plan fiduciaries | Prudent expert + exclusive benefit |
| BSA / FinCEN | AML reporting | CTR > $10K cash, SAR > $5K suspicious |
| OFAC | Sanctions | SDN screening, strict liability |
| Form CRS | Relationship summary | Deliver before/at first recommendation |
| SEC Rule 17a-4 | Recordkeeping | Retain records 3–6 years depending on type |

## Data Enhancement

For live market data to support compliance analysis (e.g., product cost comparisons, fee analysis), use the **FinData Toolkit** skill (`us-findata-toolkit`).

## Important Guidelines

- **This is regulatory guidance, not legal advice.** Always recommend consulting a compliance attorney for specific situations.
- **Standards evolve.** Reg BI was adopted in 2019 and effective June 2020. DOL fiduciary rules continue to evolve. State-level standards are emerging. Note the current-law basis.
- **Dual registrants face the highest complexity.** When a professional is registered as both a broker-dealer and investment adviser, the applicable standard depends on the capacity in which they are acting — document which hat is being worn for each interaction.
- **Compliance is a process, not a checklist.** Documentation, training, supervisory review, and periodic testing are all required elements of a compliance program.
- **When in doubt, disclose.** More disclosure is almost always better than less. The cost of over-disclosure is minimal; the cost of under-disclosure can be enforcement action.
