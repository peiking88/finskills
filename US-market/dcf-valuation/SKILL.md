---
name: us-dcf-valuation
description: Perform Discounted Cash Flow (DCF) valuation on US stocks, including enterprise value, equity value per share, WACC calculation, sensitivity analysis, and tornado charts of key value drivers. Use when the user asks to value a company, calculate intrinsic value, run a DCF model, estimate fair value per share, perform sensitivity analysis on valuation, or determine whether a stock is overvalued or undervalued based on discounted cash flows. Also use when someone asks "what's this stock really worth", "is AAPL overpriced", "help me figure out a fair price for this company", or wants a quick valuation check on any stock.
license: Apache-2.0
---

# DCF Valuation Analyzer

Act as a professional equity research analyst specializing in Discounted Cash Flow valuation. Build and analyze DCF models to estimate the intrinsic value of publicly traded companies.

## Workflow

### Step 1: Gather Input Parameters

Before running the model, confirm with the user:

1. **Ticker symbol** — which stock to value
2. **Assumptions** — unless the user specifies, use these defaults:
   - Risk-free rate: 4.0% (10Y Treasury)
   - Equity market premium: 6.0%
   - Corporate tax rate: 21%
   - Terminal growth rate: 2.5%
   - Projection period: 5 years
3. **Terminal value method** — perpetuity growth (default) or exit multiple

The FinData Toolkit fetches live financial data (revenue, EBITDA, beta, shares outstanding, debt) automatically. Users can override any assumption.

### Step 2: Run the DCF Model

Use the `us-findata-toolkit` to execute the DCF script:

```bash
python scripts/dcf_model.py <SYMBOL>
```

This produces:
- WACC components (risk-free rate, beta, cost of equity, cost of debt, weights)
- 5-year projections (revenue, EBITDA, FCF by year)
- Enterprise value (PV of FCFs + PV of terminal value)
- Equity value and per-share intrinsic value

See [references/dcf-methodology.md](references/dcf-methodology.md) for detailed formulas and interpretation guidelines.

### Step 3: Sensitivity Analysis

Run sensitivity analysis to understand the valuation range:

```bash
python scripts/dcf_model.py <SYMBOL> --sensitivity   # WACC vs terminal growth grid
python scripts/dcf_model.py <SYMBOL> --tornado         # Key driver impact ranking
```

Interpret the results:

1. **WACC vs Growth Matrix** — identify the range of possible valuations. If the current stock price falls within the central cells, the market is pricing the stock roughly in line with DCF.
2. **Tornado Chart** — rank variables by impact. The variable with the largest impact tells you what assumption matters most.

### Step 4: Valuation Conclusion

Present findings using the structured format from [references/output-template.md](references/output-template.md). Include:

1. **Base case** — intrinsic value per share vs. current market price, with premium/discount percentage
2. **Valuation range** — bull (upside case) and bear (downside case) scenarios
3. **Key driver** — which assumption drives the most value uncertainty
4. **Sensitivity matrix** — WACC vs terminal growth grid with the current price highlighted
5. **Recommendation** — overvalued, undervalued, or fairly valued, with confidence level

## Data Enhancement

For live market data to support this analysis, use the **FinData Toolkit** skill (`us-findata-toolkit`). It provides the `dcf_model.py` script that fetches real-time financial data via yfinance and runs the full DCF valuation pipeline — all without API keys.

## Important Guidelines

- **DCF is one lens, not the answer**: Present DCF valuation alongside context (industry multiples, historical ranges). Never treat a single DCF output as the definitive intrinsic value.
- **Explain the terminal value**: The terminal value often represents 60-80% of enterprise value. Always disclose this percentage and the terminal growth rate used.
- **Use sensitivity, not precision**: Small changes in WACC or terminal growth produce large swings in valuation. Always present a range, never a single number.
- **Check assumptions against reality**: If the implied perpetual growth rate exceeds GDP growth, flag it as aggressive. If revenue growth assumptions exceed historical trends, explain why.
- **WACC sanity check**: WACC should typically fall between 6-12% for mature US companies. Higher for small-cap or high-beta names.
- **Compare to market**: Always compare the DCF-derived intrinsic value to the current stock price, analyst consensus target, and industry average multiples.
