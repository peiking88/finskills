# SaaS Valuation Compression Framework

## How Compression Works

Valuation growth decomposes into two components:

```
Valuation_growth = ARR_growth + Multiple_change
```

If ARR grew 80% but valuation grew only 20%, the multiple compressed by ~60 percentage points. The multiple is the market's verdict on future expectations — when it compresses, expectations are resetting.

## Compression Metrics

| Metric | Formula |
|--------|---------|
| Multiple compression % | `(Current_Multiple - Previous_Multiple) / Previous_Multiple × 100` |
| Valuation growth % | `(Current_Valuation - Previous_Valuation) / Previous_Valuation × 100` |
| ARR growth % | `(Current_ARR - Previous_ARR) / Previous_ARR × 100` |
| Multiple change contribution | `Valuation_growth − ARR_growth` |

## Cause Attribution

Rate each cause as **Primary**, **Contributing**, or **N/A**.

### 1. Macro / Rate Environment

**What to check:** Changes in the risk-free rate (10-year Treasury), Fed policy shifts, risk appetite indicators.

**Thresholds:**
- 10-year Treasury rises > 100bps between rounds → likely Primary
- Fed tightening cycle active → Contributing or Primary
- ZIRP-to-normalization transition → Primary for 2021–2023 era rounds

**Mechanism:** Higher discount rates reduce the present value of far-future cash flows. Since SaaS companies derive most of their value from growth 5–10 years out, they are unusually sensitive to rate changes.

### 2. Growth Deceleration

**What to check:** Quarter-over-quarter ARR growth rate trend. Is the Rule of 40 declining?

**Thresholds:**
- ARR growth rate drops > 10pp between consecutive periods → Primary
- Rule of 40 drops below 30 → Contributing
- Rule of 40 drops below 20 → Primary (red flag)

**Mechanism:** The market pays premium multiples for growth. When growth slows, the multiple compresses even if the absolute business is still healthy. This is the most company-specific cause.

### 3. Narrative Shift

**What to check:** Has the market story changed for this category?

**Examples:**
- "Digital transformation" (2020) → "Efficient growth" (2023)
- "Cloud-first" → "AI will disrupt SaaS" (2024–2026)
- Category-specific: "Fintech is the future" → "Fintech is commoditized"

**Thresholds:** If 3+ major analyst reports or tech media pieces reflect a narrative shift in the same quarter → Contributing or Primary.

### 4. AI Premium / Discount

**What to check:** Is the company gaining an AI premium or being disrupted?

- **AI Premium:** Company has credible AI product line, AI-native features, or is positioned as AI infrastructure. Multiple may expand despite other headwinds.
- **AI Discount:** Company's core offering could be replicated by AI (e.g., basic content tools, simple automation). Multiple compresses even if current revenue is stable.

**Thresholds:**
- AI revenue > 10% of ARR → Premium
- No AI strategy articulated → Discount risk
- Competitors shipping AI alternatives → Primary Discount

### 5. Competitive / Market

**What to check:** New entrants, market saturation, pricing pressure, customer concentration risk.

**Signs of Primary attribution:**
- Major competitor enters market with 50%+ lower pricing
- Market share declining quarter-over-quarter
- NRR drops below 100% (net revenue retention — customers spending less over time)

### 6. Investor Supply/Demand

**What to check:** VC funding environment, IPO window, secondary market activity.

**Signs of Primary attribution:**
- VC funding in the sector drops > 50% YoY
- No IPOs in the sector for 6+ months
- Secondary market discounts > 30% to last primary round
- Major crossover funds (Tiger, Coatue) significantly reduced deployment

## ARR Estimation Heuristics (Private Companies)

When public data is unavailable:

| Stage | Typical ARR Range |
|-------|-------------------|
| Seed / Series A | $500K–$3M |
| Series B | $5M–$20M |
| Series C | $20M–$60M |
| Series D+ | Usually public data available |

## Rule of 40 Assessment

```
Rule_of_40 = Revenue_Growth_Rate + FCF_Margin
```

| Score | Assessment |
|-------|-----------|
| > 40 | Excellent — premium multiple justified |
| 20–40 | Acceptable — growth or efficiency must be strong |
| < 20 | Red flag — multiple compression likely |
| < 0 | Critical — business model viability in question |
