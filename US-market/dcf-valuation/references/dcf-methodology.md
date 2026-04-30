# DCF Valuation Methodology

## Core Formula

The enterprise value under DCF is the sum of discounted projected free cash flows plus the discounted terminal value:

```
EV = Σ(FCF_t / (1 + WACC)^t) + TV / (1 + WACC)^n
```

Where:
- **FCF_t** = Free Cash Flow in year t
- **WACC** = Weighted Average Cost of Capital
- **TV** = Terminal Value
- **n** = Number of projection years

## Free Cash Flow Calculation

```
FCF = EBIT × (1 - Tax Rate) + Depreciation - CapEx - ΔWorking Capital
```

### Step-by-step:

1. **Revenue** = Prior Year Revenue × (1 + Growth Rate)
2. **EBITDA** = Revenue × EBITDA Margin
3. **EBIT** = EBITDA - Depreciation (approximated as CapEx for simplicity)
4. **NOPAT** = EBIT × (1 - Tax Rate)
5. **FCF** = NOPAT + Depreciation - CapEx - ΔNWC

## WACC (Weighted Average Cost of Capital)

```
WACC = (E/V) × Ke + (D/V) × Kd × (1 - T)
```

Where:
- **E/V** = Equity weight = 1 / (1 + D/E)
- **D/V** = Debt weight = D/E / (1 + D/E)
- **Ke** = Cost of Equity = Rf + β × (Rm - Rf)
- **Kd** = Cost of Debt (pre-tax)
- **T** = Corporate Tax Rate

### CAPM Components:
- **Rf** = Risk-free rate (10Y US Treasury, ~4%)
- **β** = Equity beta (from yfinance, typically 0.8-1.5)
- **Rm - Rf** = Equity market risk premium (typically 5-7%)

## Terminal Value

### Perpetuity Growth Method (default):
```
TV = FCF_n × (1 + g) / (WACC - g)
```
Where **g** = terminal growth rate (typically 2-3%, should not exceed long-term GDP growth).

### Exit Multiple Method:
```
TV = EBITDA_n × Exit Multiple
```
Typical exit multiples: 8-12x EV/EBITDA depending on industry.

## Sensitivity Analysis

### Two-Way Sensitivity
Vary WACC and terminal growth simultaneously to produce a valuation matrix:
- WACC range: ±30% from base (e.g., 6.3% to 11.7% for 9% base)
- Terminal growth range: ±1.5% from base (e.g., 1.0% to 4.0% for 2.5% base)

### Tornado Analysis
Rank variables by impact on enterprise value:
1. WACC — generally the most impactful
2. Terminal Growth Rate
3. EBITDA Margin
4. Revenue Growth
5. Tax Rate

## Interpretation Guidelines

### Terminal Value Percentage
- **> 85%**: Highly dependent on terminal assumptions; wide confidence interval
- **70-85%**: Typical for stable, mature companies
- **60-70%**: Strong near-term cash flow contribution; common for growth companies
- **< 60%**: Unusual for DCF; check for abnormally high near-term projections

### WACC Benchmarks by Company Type
| Company Type | Typical WACC Range |
|-------------|-------------------|
| Large-cap, stable (e.g., JNJ, PG) | 6-8% |
| Mid-cap, moderate growth | 8-10% |
| Small-cap, high growth | 10-12% |
| High-beta tech | 10-14% |

### Value Gap Assessment
| Premium/Discount to Intrinsic Value | Assessment |
|-------------------------------------|------------|
| > 30% above intrinsic | Significantly overvalued |
| 10-30% above | Moderately overvalued |
| ±10% | Fairly valued |
| 10-30% below | Moderately undervalued |
| > 30% below | Significantly undervalued |

## Common Pitfalls

1. **Terminal growth > GDP growth**: Implies the company outgrows the economy forever — unsustainable
2. **WACC too low**: Below 6% for non-utility companies is usually aggressive
3. **Double-counting growth**: High near-term growth AND high terminal growth
4. **Ignoring dilution**: Share count from yfinance may not reflect fully diluted shares
5. **Static margins**: Margins should reflect competitive dynamics over time
