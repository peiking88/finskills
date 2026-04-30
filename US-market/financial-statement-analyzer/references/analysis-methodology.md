# Analysis Methodology

Detailed formulas, scoring models, and interpretation guides for financial statement deep dive analysis.

## Table of Contents

1. [DuPont Decomposition](#dupont-decomposition)
2. [Earnings Quality Tests](#earnings-quality-tests)
3. [Financial Health Models](#financial-health-models)
4. [Working Capital Analysis](#working-capital-analysis)
5. [Balance Sheet Risk Indicators](#balance-sheet-risk-indicators)
6. [Red Flag Checklist](#red-flag-checklist)

## DuPont Decomposition

### 5-Factor DuPont Formula

```
ROE = (NI/EBT) × (EBT/EBIT) × (EBIT/Revenue) × (Revenue/Assets) × (Assets/Equity)
     Tax Burden × Interest Burden × Op Margin × Asset Turnover × Equity Multiplier
```

### Component Interpretation

| Component | Increasing Means | Healthy Range |
|-----------|-----------------|--------------|
| Tax burden (NI/EBT) | Lower effective tax rate | 0.70–0.85 |
| Interest burden (EBT/EBIT) | Lower debt cost | > 0.80 |
| Operating margin (EBIT/Rev) | Better operational efficiency | Industry-specific |
| Asset turnover (Rev/Assets) | Better asset utilization | Industry-specific |
| Equity multiplier (Assets/Eq) | Higher leverage | 1.5–3.0 (non-financial) |

### Trend Analysis

For each component, calculate 5-year trend:
- **Improving**: Component contributing more to ROE over time
- **Stable**: Component relatively unchanged
- **Deteriorating**: Component declining over time

Key diagnostic: If ROE is stable but the source is shifting (e.g., margin declining but leverage increasing), that is a negative signal — the company is maintaining ROE through financial engineering rather than operational improvement.

## Earnings Quality Tests

### Accruals Ratio (Balance Sheet Approach)

```
Accruals = (ΔCurrent Assets − ΔCash) − (ΔCurrent Liabilities − ΔShort-term Debt) − Depreciation
Accruals Ratio = Accruals / Average Total Assets
```

| Accruals Ratio | Quality Assessment |
|---------------|-------------------|
| < 5% | High quality — earnings largely cash-based |
| 5–10% | Acceptable — some accrual component |
| 10–15% | Elevated — investigate further |
| > 15% | Low quality — significant non-cash earnings |

### Cash Conversion Ratio

```
Cash Conversion = Operating Cash Flow / Net Income
```

| Ratio | Assessment |
|-------|-----------|
| > 1.2 | Excellent — cash earnings exceed reported earnings |
| 1.0–1.2 | Good |
| 0.8–1.0 | Acceptable |
| 0.5–0.8 | Weak — earnings not fully converting to cash |
| < 0.5 | Poor — major gap between reported and cash earnings |

Persistent CCR < 0.8 over 3+ years is a significant red flag.

### Revenue Quality Indicators

| Indicator | Green Flag | Red Flag |
|-----------|-----------|----------|
| Revenue growth vs AR growth | Revenue growing faster | AR growing 1.5x+ faster than revenue |
| Deferred revenue trend | Growing (prepaid backlog) | Declining (revenue pulled forward) |
| Revenue concentration | Diversifying | Concentrating in fewer customers |
| Channel stuffing indicators | Steady quarterly patterns | Large Q4 spikes, Q1 dips |
| Bill-and-hold revenue | Not present | Present and growing |

### Non-Recurring Items Analysis

Track "non-recurring" charges over 5 years:

| Pattern | Assessment |
|---------|-----------|
| Genuinely rare (1 in 5 years) | Legitimate non-recurring |
| Every 2–3 years | Questionable — may be recurring |
| Annual | These are recurring costs being excluded from "adjusted" earnings |

## Financial Health Models

### Altman Z-Score (Manufacturing)

```
Z = 1.2×X1 + 1.4×X2 + 3.3×X3 + 0.6×X4 + 1.0×X5
```

| Variable | Formula |
|----------|---------|
| X1 | Working Capital / Total Assets |
| X2 | Retained Earnings / Total Assets |
| X3 | EBIT / Total Assets |
| X4 | Market Cap / Total Liabilities |
| X5 | Revenue / Total Assets |

| Z-Score | Interpretation |
|---------|---------------|
| > 2.99 | Safe zone — low bankruptcy probability |
| 1.81–2.99 | Grey zone — moderate risk |
| < 1.81 | Distress zone — high bankruptcy probability |

### Altman Z-Score (Non-Manufacturing / Service)

```
Z'' = 6.56×X1 + 3.26×X2 + 6.72×X3 + 1.05×X4
```

(Same variables but excludes X5 and uses different coefficients)

| Z'' Score | Interpretation |
|-----------|---------------|
| > 2.60 | Safe zone |
| 1.10–2.60 | Grey zone |
| < 1.10 | Distress zone |

### Piotroski F-Score (0–9)

| # | Signal | Criterion | Score |
|---|--------|-----------|-------|
| 1 | ROA | Positive net income | +1 |
| 2 | Operating CF | Positive operating cash flow | +1 |
| 3 | ROA change | ROA improved year-over-year | +1 |
| 4 | Accrual quality | Operating CF > Net Income | +1 |
| 5 | Leverage change | Long-term debt/assets decreased | +1 |
| 6 | Liquidity change | Current ratio improved | +1 |
| 7 | Share issuance | No new shares issued | +1 |
| 8 | Gross margin change | Gross margin improved | +1 |
| 9 | Asset turnover change | Asset turnover improved | +1 |

| F-Score | Interpretation |
|---------|---------------|
| 8–9 | Strong financial position |
| 5–7 | Average |
| 0–4 | Weak financial position |

### Beneish M-Score (Earnings Manipulation)

```
M = -4.84 + 0.920×DSRI + 0.528×GMI + 0.404×AQI + 0.892×SGI
    + 0.115×DEPI − 0.172×SGAI + 4.679×TATA − 0.327×LVGI
```

| Variable | Name | Measures |
|----------|------|----------|
| DSRI | Days Sales in Receivables Index | AR manipulation |
| GMI | Gross Margin Index | Margin deterioration |
| AQI | Asset Quality Index | Asset capitalization |
| SGI | Sales Growth Index | Growth sustainability |
| DEPI | Depreciation Index | Depreciation policy changes |
| SGAI | SG&A Expense Index | Cost management |
| TATA | Total Accruals to Total Assets | Accrual quality |
| LVGI | Leverage Index | Leverage changes |

| M-Score | Interpretation |
|---------|---------------|
| < -2.22 | Unlikely manipulator |
| -2.22 to -1.78 | Grey zone — elevated risk |
| > -1.78 | Likely manipulator — significant risk |

## Working Capital Analysis

### Cash Conversion Cycle

```
CCC = DSO + DIO − DPO
```

| CCC Trend | Interpretation |
|-----------|---------------|
| Declining | Improving working capital efficiency — positive |
| Stable | Consistent operations |
| Increasing | Deteriorating efficiency — cash being tied up |

### Peer-Relative Working Capital

Compare each component (DSO, DIO, DPO) to the industry median:
- Better than median = operational advantage
- Worse than median = potential inefficiency or competitive weakness

### Working Capital Red Flags

| Indicator | What It Means |
|-----------|--------------|
| DSO increasing while revenue flat | Collection problems or channel stuffing |
| DIO increasing significantly | Demand weakness, obsolescence risk |
| DPO increasing sharply | May signal cash flow stress (stretching payables) |
| Inventory write-downs | Obsolescence, overproduction |

## Balance Sheet Risk Indicators

### Goodwill and Intangibles

| Metric | Threshold | Risk |
|--------|-----------|------|
| Goodwill / Equity | < 30% | Low |
| Goodwill / Equity | 30–60% | Moderate |
| Goodwill / Equity | > 60% | High — impairment could significantly impact equity |
| Goodwill growth rate | > Revenue growth | Acquisitive growth concern |

### Debt Quality

| Metric | Healthy | Concerning |
|--------|---------|-----------|
| Interest coverage (EBIT/Interest) | > 5x | < 3x |
| Net debt / EBITDA | < 2x | > 4x |
| Debt maturity | Well-distributed | Large near-term maturities |
| Fixed vs floating rate | Mostly fixed | > 50% floating |
| Covenant headroom | Ample | Tight |

### Off-Balance-Sheet Items

Checklist of items to investigate:
- Operating lease obligations (look for present value of future payments)
- Purchase commitments
- Guarantees and contingencies
- Joint ventures and partnerships
- Special purpose entities / VIEs
- Factored receivables
- Letters of credit

## Red Flag Checklist

### Accounting Red Flags

| # | Red Flag | What to Check |
|---|----------|---------------|
| 1 | Revenue growing faster than cash flow | Income statement vs cash flow statement |
| 2 | AR growing faster than revenue | Balance sheet trend analysis |
| 3 | Inventory growing faster than COGS | Balance sheet vs income statement |
| 4 | Frequent "non-recurring" charges | Income statement footnotes |
| 5 | Declining audit quality | Auditor changes, qualifications |
| 6 | Aggressive revenue recognition | Revenue recognition policy footnotes |
| 7 | Increasing capitalized costs | Cash flow statement (investing section) |
| 8 | Widening GAAP vs non-GAAP gap | Earnings releases vs 10-K |
| 9 | Related-party transactions | Related party footnotes |
| 10 | Pension assumption changes | Pension footnotes (discount rate, return assumptions) |

### Governance Red Flags

| # | Red Flag | Where to Find |
|---|----------|---------------|
| 1 | Auditor change | Proxy statement / 8-K |
| 2 | CFO turnover | Press releases / 8-K |
| 3 | Restatements | 10-K/A filings |
| 4 | Material weakness in internal controls | 10-K Item 9A |
| 5 | Related-party transactions | Proxy statement |
| 6 | Insider selling during buyback | Form 4 filings vs buyback announcements |
| 7 | Board independence concerns | Proxy statement |

## Industry Benchmarks

Financial ratios vary significantly by industry. Use these benchmarks to contextualize ratio analysis.

### Technology

| Ratio | Excellent | Good | Acceptable | Poor |
|-------|-----------|------|------------|------|
| Current Ratio | > 2.5 | 2.0-2.5 | 1.5-2.0 | < 1.5 |
| Debt-to-Equity | < 0.3 | 0.3-0.5 | 0.5-0.8 | > 0.8 |
| ROE | > 25% | 18-25% | 12-18% | < 12% |
| Gross Margin | > 65% | 50-65% | 35-50% | < 35% |
| P/E Ratio | < 20 | 20-30 | 30-50 | > 50 |

### Retail

| Ratio | Excellent | Good | Acceptable | Poor |
|-------|-----------|------|------------|------|
| Current Ratio | > 2.0 | 1.5-2.0 | 1.0-1.5 | < 1.0 |
| Debt-to-Equity | < 0.5 | 0.5-1.0 | 1.0-2.0 | > 2.0 |
| ROE | > 20% | 15-20% | 10-15% | < 10% |
| Gross Margin | > 40% | 30-40% | 20-30% | < 20% |
| P/E Ratio | < 15 | 15-25 | 25-40 | > 40 |

### Financial

| Ratio | Excellent | Good | Acceptable | Poor |
|-------|-----------|------|------------|------|
| Current Ratio | > 1.5 | 1.2-1.5 | 1.0-1.2 | < 1.0 |
| Debt-to-Equity | < 1.0 | 1.0-2.0 | 2.0-4.0 | > 4.0 |
| ROE | > 15% | 12-15% | 8-12% | < 8% |
| Gross Margin | N/A | N/A | N/A | N/A |
| P/E Ratio | < 12 | 12-18 | 18-30 | > 30 |

Financial companies have different margin structures — net interest margin (NIM) replaces gross margin. A healthy NIM is > 3% for banks.

### Manufacturing

| Ratio | Excellent | Good | Acceptable | Poor |
|-------|-----------|------|------------|------|
| Current Ratio | > 2.0 | 1.5-2.0 | 1.0-1.5 | < 1.0 |
| Debt-to-Equity | < 0.5 | 0.5-1.0 | 1.0-1.5 | > 1.5 |
| ROE | > 18% | 12-18% | 8-12% | < 8% |
| Gross Margin | > 35% | 25-35% | 15-25% | < 15% |
| P/E Ratio | < 15 | 15-22 | 22-35 | > 35 |

### Healthcare

| Ratio | Excellent | Good | Acceptable | Poor |
|-------|-----------|------|------------|------|
| Current Ratio | > 2.0 | 1.5-2.0 | 1.0-1.5 | < 1.0 |
| Debt-to-Equity | < 0.4 | 0.4-0.8 | 0.8-1.2 | > 1.2 |
| ROE | > 22% | 15-22% | 10-15% | < 10% |
| Gross Margin | > 70% | 55-70% | 40-55% | < 40% |
| P/E Ratio | < 18 | 18-30 | 30-50 | > 50 |

### How to Use Benchmarks

1. **Match the primary industry** — use the closest match; a SaaS company uses Technology even if it's in a different GICS sector
2. **Consider the business model** — asset-light vs asset-heavy within the same industry can shift benchmarks
3. **Trend matters more than point-in-time** — a ratio improving from Poor to Acceptable is a stronger signal than one always at Good
4. **Cross-check multiple ratios** — one Excellent ratio doesn't compensate for three Poor ones

*Benchmarks sourced from industry research and the interpret_ratios.py financial analysis framework.*
