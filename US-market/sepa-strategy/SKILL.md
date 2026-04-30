---
name: us-sepa-strategy
description: Apply the SEPA (Specific Entry Point Analysis) trading methodology by Mark Minervini to identify stocks in Stage 2 uptrends with proper trend template alignment, VCP or classic base patterns, and strong fundamentals. Use when the user asks about SEPA, Minervini strategy, trend template, VCP (Volatility Contraction Pattern), Stage 2 breakout, growth stock screening, pivot point entry, position sizing for breakouts, or wants to find stocks setting up for a potential breakout. Also trigger when someone says "find me stocks ready to break out", "which stocks are in an uptrend", "how do I spot a VCP", "is this stock in Stage 2", or "help me time my entry on this growth stock".
license: Apache-2.0
---

# SEPA Strategy (Minervini)

Act as a professional growth stock analyst applying the SEPA (Specific Entry Point Analysis) methodology. Identify stocks in Stage 2 advances that meet the Trend Template criteria, exhibit a valid base pattern (VCP, cup-with-handle, flat base, or high tight flag), and have the fundamental characteristics of a potential superperformer.

## Workflow

### Step 1: Gather Stock Data

Collect the following for the target stock (use `us-findata-toolkit` for live data):

| Data Point | Source |
|-----------|--------|
| Daily/weekly price chart (6+ months) | yfinance history |
| Moving averages (50-day, 150-day, 200-day) | Calculate from history |
| Volume data | yfinance history |
| EPS growth (quarterly & annual) | yfinance info |
| Revenue growth | yfinance financials |
| Profit margins (gross, operating, net) | yfinance financials |
| Institutional ownership % | yfinance info |
| Relative Strength ranking | Calculate vs S&P 500 |

### Step 2: Stage Analysis

Determine which of the 4 market stages the stock occupies. Only **Stage 2 (Advancing)** is actionable.

See [references/stage-analysis.md](references/stage-analysis.md) for the full stage framework and base counting rules.

| Stage | Characteristic | Action |
|-------|---------------|--------|
| Stage 1: Basing | Price consolidating, MAs flattening | Watch for breakout |
| **Stage 2: Advancing** | Price above rising MAs, higher highs/lows | **Actionable** |
| Stage 3: Topping | Price volatile, MAs flattening, distribution | Avoid |
| Stage 4: Declining | Price below declining MAs, lower highs/lows | Avoid |

Base counting matters: Bases 1–2 are safest. Base 3+ increases risk. Base 7+ = avoid.

### Step 3: Trend Template Checklist

All 8 conditions must pass. See [references/trend-template.md](references/trend-template.md) for detailed explanations.

| # | Condition | Pass? |
|---|-----------|-------|
| 1 | Current price > 150-day MA | — |
| 2 | Current price > 200-day MA | — |
| 3 | 150-day MA > 200-day MA | — |
| 4 | 200-day MA trending up (≥1 month) | — |
| 5 | Current price > 50-day MA | — |
| 6 | Current price ≥ 30% above 52-week low | — |
| 7 | Current price within 25% of 52-week high | — |
| 8 | Relative Strength ranking ≥ 70 (outperforming 70% of market) | — |

**Verdict:** 8/8 = passes. Any fail = does not meet SEPA criteria.

### Step 4: Fundamental Check

Grade the stock's fundamental strength. See [references/fundamentals.md](references/fundamentals.md) for detailed tiers.

| Metric | Minimum | Stock Value | Grade |
|--------|---------|-------------|-------|
| Quarterly EPS growth | ≥ 20% | — | A/B/C/D |
| EPS acceleration (increasing rate) | Yes | — | — |
| Annual EPS growth | ≥ 25% | — | — |
| Revenue growth | ≥ 15% | — | — |
| Margin trend | Stable/expanding | — | — |
| Institutional ownership | Increasing | — | — |
| Catalyst present | Yes | — | — |

Overall fundamental grade: **A** (superperformer), **B** (strong), **C** (acceptable), **D** (weak — avoid).

### Step 5: Pattern Recognition

Identify the base pattern forming. See [references/patterns.md](references/patterns.md) for identification rules.

| Pattern | Key Characteristics |
|---------|-------------------|
| VCP (Volatility Contraction) | 2–6 price contractions, each smaller, volume dries up on right side |
| Cup-with-Handle | U-shape 12–35% deep, 7–65 weeks, handle ≤ 15% deep |
| Flat Base | ≤ 15% deep, ≥ 5 weeks, tight price action |
| Bull Flag | Short pause in strong uptrend, ≤ 10% pullback |
| High Tight Flag | 100%+ advance in 8 weeks, 3–5 week flag ≤ 25% deep |

All patterns enter on **pivot breakout** (price exceeds consolidation high) with **volume ≥ 1.5x average**.

### Step 6: Entry Point Analysis

See [references/entry-rules.md](references/entry-rules.md) for full entry mechanics.

- **Pivot point:** The highest price in the consolidation (resistance level)
- **Buy zone:** Pivot price to +5% above pivot
- **Volume confirmation:** Must see ≥ 1.5x average daily volume on breakout day
- **Risk/reward:** Must be ≥ 2:1 (potential upside vs stop loss distance)
- **False breakout checklist:** Check for volume failure, immediate reversal, or gap-down within 3 days

### Step 7: Position Sizing & Stop Loss

See [references/position-sizing.md](references/position-sizing.md) for the full framework with worked examples.

**Position size formula:**
```
Shares = (Account × Risk%) / (Entry Price - Stop Price)
```

**Stop loss evolution:**

| Phase | Trigger | Stop Level |
|-------|---------|-----------|
| Initial | Entry | -7 to -8% below entry |
| Phase 2 | Stock up +8% | Move stop to breakeven |
| Phase 3 | Stock up +15% | Trailing stop (e.g., 50-day MA or -10% from peak) |

**Iron rules:** Stops only move UP. Never average down. Pyramiding in decreasing tranches (50/30/20).

### Step 8: Market Environment Check

Assess the overall market before committing capital.

See [references/market-environment.md](references/market-environment.md) for detailed criteria.

| Environment | Action | Max Risk |
|-------------|--------|----------|
| Bull (confirmed uptrend) | Full position sizes | 6–8% of account |
| Choppy (mixed signals) | Reduced sizes, tighter stops | 3–4% |
| Bear (distribution, declining MAs) | No new positions, all cash | 0% |

### Step 9: Compile SEPA Report

Present findings in this structure:

1. **Stock Identification** — Ticker, price, sector
2. **Stage Assessment** — Current stage and base count
3. **Trend Template Scorecard** — 8-condition pass/fail table
4. **Fundamental Grade** — A/B/C/D with justification
5. **Pattern Identified** — Type, pivot point, buy zone
6. **Entry Assessment** — Actionable or not, with specific entry/stop/target
7. **Position Sizing** — For a given account size (ask user)
8. **Market Environment** — Bull/Choppy/Bear
9. **Overall Verdict** — Strong Buy Setup / Watch List / Pass

## Data Enhancement

For live market data to support this analysis, use the **FinData Toolkit** skill (`us-findata-toolkit`). It provides real-time stock metrics, financials, price history, and financial calculators — all without API keys.

## Important Guidelines

- **The Trend Template is non-negotiable.** All 8 conditions must pass. No exceptions for "almost there" stocks.
- **Pattern quality matters more than pattern type.** A well-formed VCP in Base 1 is far superior to a sloppy cup-with-handle in Base 5.
- **Volume is the truth teller.** Breakouts without volume confirmation fail at a much higher rate.
- **Context over perfection.** A Grade B fundamental stock with a clean VCP in a bull market is a better setup than a Grade A stock with no pattern in a bear market.
- **Risk management first.** Even the best-looking setup can fail. Always define your stop before entering.
