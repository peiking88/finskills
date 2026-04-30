---
name: us-saas-valuation-compression
description: Analyze SaaS company valuation compression across funding rounds or public market periods. Compute ARR multiple changes, attribute causes (macro rates, growth deceleration, narrative shift, AI premium), and compare against SaaS benchmark multiples. Use when the user asks about SaaS valuation, ARR multiples, valuation compression, funding round analysis, SaaS bubble, private market valuation, or wants to understand why a SaaS company's valuation changed between rounds. Also trigger when someone says "is this SaaS stock overvalued", "what happened to SaaS multiples", "how do ARR multiples compare", or "analyze this company's funding history".
license: Apache-2.0
---

# SaaS Valuation Compression Analysis

Act as a professional software equity analyst specializing in SaaS (Software as a Service) company valuation. Analyze how and why a SaaS company's ARR (Annual Recurring Revenue) multiple has compressed or expanded over time, attribute the causes, and provide forward-looking implications.

## Workflow

### Step 1: Gather Data

Collect the following through web search and `us-findata-toolkit`:

| Data Point | Source |
|-----------|--------|
| Company funding rounds (dates, amounts, valuations) | Web search (Crunchbase, PitchBook) |
| ARR or revenue at each round/quarter | Web search, SEC filings, earnings |
| SaaS-specific metrics (NRR, churn, growth rate) | Web search, yfinance |
| Macro SaaS median ARR multiples by period | Reference benchmarks below |
| Comparable companies | Web search |

### Step 2: Build the Valuation Model

For each funding round or valuation period, compute:

| Field | Description |
|-------|-------------|
| Round/Period | Date and stage (Seed, A, B, C, D, E+, Public) |
| Valuation | Post-money valuation (private) or market cap (public) |
| ARR | Annual recurring revenue (actual or estimated) |
| ARR Multiple | `Valuation / ARR` |
| Revenue Growth Rate | YoY ARR growth at that point |

**ARR estimation heuristics** (when public data unavailable):
- Seed/Series A: $500K–$3M ARR
- Series B: $5M–$20M ARR
- Series C: $20M–$60M ARR
- Series D+: Typically public data available

### Step 3: Compute Compression Metrics

For each period-to-period transition:

| Metric | Formula |
|--------|---------|
| Multiple compression | `(Current_Multiple - Previous_Multiple) / Previous_Multiple × 100` |
| Valuation growth | `(Current_Valuation - Previous_Valuation) / Previous_Valuation × 100` |
| ARR growth | `(Current_ARR - Previous_ARR) / Previous_ARR × 100` |
| Multiple change contribution | `Valuation_growth − ARR_growth` |

**Key insight:** `Valuation_growth = ARR_growth + Multiple_change`. If ARR grew 80% but valuation grew only 20%, the multiple compressed by ~60 percentage points.

### Step 4: Attribute Compression Causes

Rate each cause as **Primary**, **Contributing**, or **N/A**. See [references/compression-framework.md](references/compression-framework.md) for detailed benchmarks and thresholds.

| Cause | What to Check |
|-------|---------------|
| **Macro / Rate Environment** | Interest rate changes, risk appetite shifts, ZIRP-to-normalization impact |
| **Growth Deceleration** | Is ARR growth slowing quarter-over-quarter? Rule of 40 declining? |
| **Narrative Shift** | Has the market story changed? (e.g., "AI will disrupt SaaS") |
| **AI Premium / Discount** | Is the company gaining an AI premium or being disrupted by AI? |
| **Competitive / Market** | New entrants, market saturation, pricing pressure |
| **Investor Supply/Demand** | VC funding environment, IPO window, secondary market activity |

### Step 5: Contextualize with Benchmarks

Compare against SaaS market benchmarks. See [references/saas-benchmarks.md](references/saas-benchmarks.md) for historical data.

| Period | SaaS Median ARR Multiple | Context |
|--------|------------------------|---------|
| 2019 (pre-pandemic) | 8–12x | Normal |
| 2020 (pandemic surge) | 15–25x | Digital transformation rush |
| 2021 (peak bubble) | 35–45x | ZIRP, SPACs, growth-at-all-costs |
| 2022 (normalization) | 10–18x | Rate hikes begin |
| 2023 (correction) | 6–12x | "Efficient growth" era |
| 2024–2025 (recovery) | 8–15x | AI narrative premium |
| 2026 (current) | 6–12x | Software meltdown, AI disruption fears |

### Step 6: Compile Report

Present findings in this structure:

1. **Executive Summary** — One-sentence verdict on valuation trajectory
2. **Valuation Timeline** — Table of rounds/periods with ARR multiples
3. **Compression Analysis** — Period-by-period attribution table
4. **Primary Cause Assessment** — Which factor drove the most change
5. **Comparable Context** — How the company compares to peers
6. **Forward Implication** — What the current multiple implies for future rounds/IPO

## SaaS-Specific Considerations

- **Rule of 40:** Growth rate + FCF margin should exceed 40%. Below 20 is a red flag.
- **Net Revenue Retention (NRR):** >120% = excellent, 100–110% = adequate, <100% = churn problem.
- **ARR per employee:** Benchmark $200K–$400K for efficient SaaS. Below $150K signals bloat.
- **Gross margin:** Should be 70–85%. Below 65% is not true SaaS.
- **CAC payback period:** Target < 18 months. > 24 months is concerning.

## Data Enhancement

For live market data, use the **FinData Toolkit** skill (`us-findata-toolkit`). For private company data, supplement with web search for Crunchbase, PitchBook, or press releases.
