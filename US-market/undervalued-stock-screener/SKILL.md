---
name: us-undervalued-stock-screener
description: Screen and identify undervalued stocks with strong fundamentals using professional equity research methodology. Use when the user asks to find undervalued stocks, screen for cheap or bargain stocks, identify value investing opportunities, perform fundamental stock analysis, find stocks trading below intrinsic value, or requests a stock screener based on financial metrics like P/E ratio, debt-to-equity, free cash flow, or ROIC. Also trigger when someone says "what's cheap right now", "find me bargain stocks", "show me stocks on sale", "what's trading below fair value", or asks "which stocks are undervalued".
license: Apache-2.0
---

# Undervalued Stock Screener

Act as a professional equity research analyst. Scan the current stock market to identify undervalued companies with strong fundamentals using a structured, multi-filter screening methodology.

## Workflow

### Step 1: Confirm Screening Parameters

Before screening, confirm with the user:

1. **Number of stocks** to identify (default: 10)
2. **Market scope** — US only, global, or specific regions/exchanges
3. **Sector preferences** — any sectors to include or exclude
4. **Market cap range** — large-cap, mid-cap, small-cap, or all
5. **Additional filters** — any custom criteria beyond the defaults

If the user wants defaults, proceed with the standard filters below.

### Step 2: Apply Screening Filters

Apply ALL of the following quantitative filters. See [references/screening-methodology.md](references/screening-methodology.md) for detailed criteria, thresholds, and edge cases.

| Filter | Criterion |
|--------|-----------|
| Valuation | P/E ratio below industry average |
| Growth | Consistent revenue and earnings growth over 3–5 years |
| Leverage | Debt-to-equity ratio below sector median |
| Cash Flow | Positive and growing free cash flow |
| Returns | ROIC above industry average |
| Upside | Analyst consensus upside ≥ 30% |

### Step 3: Deep-Dive Analysis

For each qualifying company, work through these sub-steps in order:

1. **Business Overview** — What the company does, its market position, and competitive moat. Identify the primary revenue drivers and geographic mix.
2. **Quantitative Deep-Dive** — Go beyond the initial screen filters:
   - DuPont decomposition of ROE to identify whether returns come from margin, efficiency, or leverage
   - FCF quality: FCF conversion ratio (FCF/net income) and trend over 3 years
   - Balance sheet: working capital trends, goodwill as % of equity, off-balance-sheet obligations
   - Earnings quality: accruals ratio, gap between reported and cash earnings
   For detailed calculation methods, refer to [references/screening-methodology.md](references/screening-methodology.md) sections on each filter.
3. **Why It Appears Undervalued** — Identify the specific cause of the valuation discount:
   - Market misperception or narrative driving the discount
   - Temporary headwinds vs. structural decline (distinguish clearly)
   - Catalysts that could close the gap (earnings inflection, product launch, regulatory change, management action)
   - Comparison to historical valuation range and peer multiples
4. **Key Risks** — Assess what could go wrong across three dimensions:
   - Macro: interest rates, recession, currency, commodity price exposure
   - Industry: competitive disruption, regulatory shifts, technological obsolescence
   - Company-specific: execution risk, customer/supplier concentration, management quality, litigation
5. **Intrinsic Value Range** — Estimate using at least two methods (use the `us-dcf-valuation` skill for rigorous DCF when possible):
   - DCF with WACC sensitivity (base/bull/bear)
   - Comparable company multiples (peer group average)
   - Sum-of-the-parts if the company has distinct business segments

See [references/output-template.md](references/output-template.md) for the structured report format.

### Step 3.5: Composite Scoring and Ranking

Rank all qualifying stocks using a weighted composite score. See [references/screening-methodology.md](references/screening-methodology.md) "Composite Scoring Model" section for the full model. In summary:

| Factor | Weight | What It Measures |
|--------|--------|-----------------|
| Valuation Gap | 25% | How far below fair value (P/E discount + FCF yield) |
| Growth Quality | 20% | Revenue/EPS consistency and trajectory |
| Financial Health | 20% | Leverage, FCF conversion, interest coverage |
| Capital Efficiency | 15% | ROIC vs. WACC spread, ROE trend |
| Catalyst Clarity | 10% | Near-term catalysts that could re-rate the stock |
| Risk Profile | 10% | Inverse of risk severity (lower risk = higher score) |

Each factor scored 1–5. Rank stocks by composite score and flag any with a single factor scoring 1 (automatic downgrade).

### Step 4: Compile and Present

Present findings in a structured report:

1. **Executive Summary** — High-level overview of the screening results, market conditions, and thematic observations
2. **Screening Criteria Summary** — Table of filters applied
3. **Individual Stock Profiles** — One section per company using the output template
4. **Comparative Table** — Side-by-side metrics for all identified stocks
5. **Disclaimers** — Standard investment research disclaimers

## Data Enhancement

For live market data to support this analysis, use the **FinData Toolkit** skill (`us-findata-toolkit`). It provides real-time stock metrics, SEC filings, financial calculators, portfolio analytics, factor screening, and macro indicators — all without API keys.

## Important Guidelines

- **Data currency**: Always state the date/period of data used. Acknowledge any data limitations.
- **Industry context**: Compare metrics to the correct industry/sector peers, not the broad market.
- **Qualitative overlay**: Numbers alone are insufficient. Layer in qualitative judgment — management quality, competitive dynamics, regulatory environment.
- **Avoid bias**: Do not favor popular or well-known names. Include lesser-known companies if they meet criteria.
- **Risk-first mindset**: For each stock, honestly assess what could go wrong. A good screener is not a buy list.
- **Transparency**: If unable to verify a specific metric, say so rather than fabricating data.
