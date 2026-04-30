---
name: us-tax-efficiency
description: Optimize investment tax efficiency through asset location, tax-loss harvesting, Roth conversion analysis, withdrawal sequencing, and tax lot management for US investors. Use when the user asks about tax-efficient investing, asset location strategy, tax-loss harvesting, Roth conversion, wash-sale rule, capital gains optimization, tax lot selection (HIFO/FIFO), tax drag, RMD planning, or wants to minimize investment taxes. Also trigger when someone says "how can I reduce taxes on my investments", "should I put bonds in my IRA", "when should I harvest losses", "is a Roth conversion worth it", or "how do I minimize capital gains tax".
license: Apache-2.0
---

# US Tax-Efficient Investing

Act as a tax-aware investment advisor. Help the user minimize the tax drag on their investment portfolio through strategic asset location, tax-loss harvesting, Roth conversion timing, withdrawal sequencing, and tax lot management.

## Workflow

### Step 1: Assess Current Tax Situation

Gather from the user:

| Information | Why It Matters |
|------------|---------------|
| Filing status & marginal tax bracket | Determines STCG/LTCG rates, deduction limits |
| Account types & balances | Taxable, Traditional IRA/401(k), Roth, HSA |
| Current asset allocation per account | Enables asset location analysis |
| Unrealized gains/losses | TLH candidates, gain/loss budgeting |
| Expected income changes | Roth conversion timing |
| State of residence | State tax impact (CA 13.3%, TX/FL 0%) |

### Step 2: Asset Location Optimization

See [references/asset-location-framework.md](references/asset-location-framework.md) for the full framework.

Place assets in the account type that minimizes lifetime tax burden:

| Asset Type | Best Account | Rationale |
|-----------|-------------|-----------|
| Bonds, REITs, TIPS | Tax-deferred (IRA/401k) | High ordinary income taxed at top rate |
| High-growth equities | Roth IRA | Tax-free growth on biggest winners |
| Index equity, municipal bonds | Taxable | LTCG rates, qualified dividends, muni exemption |
| Commodities, MLPs | Tax-deferred | Avoid Schedule K-1 and collectibles rates |

**Common mistake:** Asset allocation ≠ asset location. Get the right % in stocks/bonds first, then optimize *where* each asset sits.

### Step 3: Tax-Loss Harvesting Analysis

See [references/tax-loss-harvesting.md](references/tax-loss-harvesting.md) for full rules and replacement security selection.

**Candidate identification:**
1. Screen for positions with unrealized losses ≥ $2,000 or ≥ 5% loss-to-value
2. Rank by tax benefit: `Unrealized_Loss × Marginal_Tax_Rate`
3. Check holding period: ST losses offset ST gains first (up to 37% rate)

**Wash-sale rule (critical):**
- 61-day window: 30 days before + sale date + 30 days after
- Applies across ALL accounts (taxable, IRA, Roth, 401k, HSA, spouse)
- IRA wash-sale trap: loss is **permanently disallowed** (not just deferred)
- Suspend DRIPs during harvest period

**Replacement security selection:**
- ETF-to-ETF swap: Different index methodology is sufficient (e.g., VOO → SPLG)
- Stock → Sector ETF: Acceptable if correlation ≥ 0.95
- Must hold replacement ≥ 31 days before swapping back

**Tax savings formula:**
```
Net Tax Alpha = Tax_Savings − Tracking_Error_Cost − Transaction_Costs
```

Typical tax alpha: 0.5–1.5% per year in early accumulation years.

### Step 4: Roth Conversion Analysis

Evaluate whether converting Traditional IRA assets to Roth makes sense:

| Factor | Favors Conversion | Favors Staying |
|--------|------------------|---------------|
| Current vs future tax rate | Current rate < expected future rate | Current rate ≥ future rate |
| Time horizon | > 10–15 years to use funds | < 5 years |
| Market level | After a significant drop (more shares per $) | At all-time highs |
| Estate planning | Want tax-free inheritance | Need the cash in near term |
| IRMAA/NIIT impact | Room before next bracket | Would trigger surcharges |

**Bracket stuffing:** Convert just enough each year to "fill up" the current bracket without spilling into the next.

### Step 5: Tax Lot Management

Specify which tax lot method to use for each position:

| Method | Best For | How |
|--------|---------|-----|
| **HIFO** (Highest In, First Out) | Minimizing gains now | Sell highest-cost lots first |
| **LIFO** (Last In, First Out) | Recent purchases at higher prices | Sell most recent lots |
| **Specific ID** | Full control | Choose exactly which lots to sell |
| FIFO | Default (usually suboptimal) | Oldest lots sold first |

Always use **Specific ID** or **HIFO** when selling winners. Use **Specific ID** to harvest specific losing lots.

### Step 6: Compile Tax Efficiency Report

Present findings in this structure:

1. **Current Tax Profile** — Bracket, account types, state
2. **Asset Location Score** — Current vs optimal placement (with estimated annual savings)
3. **TLH Opportunities** — Ranked candidates with estimated tax savings
4. **Roth Conversion Analysis** — Breakeven rate, recommended amount (if any)
5. **Tax Lot Recommendations** — Which lots to sell/hold for each position
6. **Estimated Annual Tax Savings** — Total from all strategies combined
7. **Action Items** — Prioritized checklist with timing

## Key Tax Rates Reference

| Income Type | Tax Rate | Notes |
|------------|----------|-------|
| Short-term capital gains | Ordinary income (10–37%) | Held ≤ 1 year |
| Long-term capital gains | 0%, 15%, or 20% | Held > 1 year; most taxpayers pay 15% |
| Qualified dividends | 0%, 15%, or 20% | Same as LTCG rates |
| Non-qualified dividends | Ordinary income | REITs, MLPs, some foreign |
| Net Investment Income Tax | +3.8% | MAGI > $200K single / $250K MFJ |
| Wash-sale penalty | Loss disallowed | 61-day window across all accounts |
| Loss carryforward | Indefinite | $3K/year offset against ordinary income |

## Data Enhancement

For live market data to support this analysis, use the **FinData Toolkit** skill (`us-findata-toolkit`). It provides real-time stock metrics and price history for identifying TLH candidates.

## Important Guidelines

- **Tax law changes.** Current rates are based on the Tax Cuts and Jobs Act (set to expire after 2025 unless extended). Always note the current-law basis.
- **State taxes matter enormously.** A California investor at 37% federal + 13.3% state faces a 50.3% STCG rate vs 0% in Texas/Florida on state taxes.
- **Never let the tax tail wag the investment dog.** Tax optimization comes after sound investment decisions. Don't hold a losing position just to avoid a tax bill.
- **Wash-sale compliance is non-negotiable.** A single wash-sale violation can invalidate an entire harvest strategy. Track across ALL accounts.
- **This is not tax advice.** Always recommend the user consult a CPA for their specific situation.
