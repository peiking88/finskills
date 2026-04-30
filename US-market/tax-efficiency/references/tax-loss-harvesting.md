# Tax-Loss Harvesting (TLH) Guide

## Candidate Identification

Screen for positions meeting all three filters:

1. **Materiality:** Minimum loss of $2,000 or loss exceeding 5% of position market value
2. **Holding period:** Positions held > 31 days; positions approaching 1 year (days 335–365) may benefit from waiting for LTCG treatment
3. **Tax benefit ranking:** `Unrealized_Loss × Applicable_Tax_Rate`. Prioritize ST losses (up to 37% rate) over LT losses (15–20% rate)

## Wash-Sale Rule (Critical)

IRC Section 1091 disallows a loss if a substantially identical security is acquired within the **61-day window** (30 days before + sale date + 30 days after).

**Cross-account scope** applies across ALL accounts:
- Taxable brokerage, Traditional IRA, Roth IRA, 401(k), HSA
- Spouse's accounts (including retirement)
- DRIP reinvestments (suspend during harvest period)

**IRA wash-sale trap:** If a wash sale is triggered by a purchase in an IRA, the disallowed loss is **permanently lost** — it cannot be added to the IRA cost basis. This is the most dangerous wash-sale scenario.

## Replacement Security Selection

The replacement must maintain market exposure without being "substantially identical":

| Strategy | Example | Requirement |
|----------|---------|-------------|
| ETF-to-ETF swap | VOO → SPLG | Different index methodology sufficient |
| Stock → Sector ETF | AAPL → XLK | Correlation ≥ 0.95 |
| International swap | VXUS → IXUS | Different fund family, different index |

**Quality checks:**
- Tracking error < 2% annualized relative to original
- Expense ratio delta should not exceed tax benefit
- Must hold replacement ≥ 31 days before swapping back

## Gain/Loss Budgeting

Before harvesting, build the year-to-date tax budget:

1. Realized gains YTD (ST and LT separately, including fund distributions)
2. Planned gain exposure (pending rebalancing, expected fund CG distributions)
3. Loss carryforward balance from prior years
4. **Target harvest amount** = (Realized Gains YTD + Planned Gains) − Loss Carryforward − $3,000

Harvest at least the target amount to zero out the current-year tax bill; harvest more to build carryforward.

## Tax Savings Calculation

```
Net Tax Alpha = Tax_Savings − Tracking_Error_Cost − Transaction_Costs
```

| Formula | Expression |
|---------|-----------|
| Tax benefit | Realized_Loss × Applicable_Tax_Rate |
| Break-even holding period | Tax_Savings / (Annual_Tracking_Error_Cost + Annual_Expense_Delta) |
| Annual TLH capacity | Portfolio_Value × Expected_Volatility × Loss_Capture_Rate |

Include state tax (0–13.3%) and NIIT (3.8% above $200K/$250K MAGI) in the applicable rate.

## Worked Example

**Given:** 500 shares at $80 cost basis ($40K total), current price $62 ($31K value), held 8 months. $12K ST realized gains YTD. Federal 35%, state 9.3%, NIIT 3.8%.

1. Unrealized loss: $31K − $40K = −$9,000 (short-term)
2. Applicable rate: 35% + 9.3% + 3.8% = 48.1%
3. Tax benefit: $9,000 × 48.1% = **$4,329**
4. Transaction + tracking error costs: ~$67
5. Net tax alpha: **$4,262**

## Execution Best Practices

- **Lot selection:** Use Specific ID (HIFO) to sell highest-cost lots first
- **Coordinate with rebalancing:** A position that is both overweight and at a loss is ideal — harvest and rebalance in one trade
- **Timing:** Year-end (Oct–Dec) captures full year's losses; opportunistic harvesting during 5%+ drawdowns captures losses that may recover
- **Trade list fields:** Security, account, action, shares, lot IDs, estimated loss, replacement security, wash-sale window dates

## Common Pitfalls

- Harvesting without checking substantially identical holdings in retirement accounts (permanent loss disallowance in IRAs)
- Forgetting to suspend DRIP across all household accounts during the 61-day window
- Harvesting small losses (< $1,000) where operational costs exceed benefit
- Over-harvesting in early years, depressing cost basis for future gains
- Not coordinating with spouse's automated investments (401(k) contributions, robo-advisor purchases)
- Selecting a replacement that is substantially identical (same index, same fund family, different share class)
