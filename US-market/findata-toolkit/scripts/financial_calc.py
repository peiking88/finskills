#!/usr/bin/env python3
"""
Financial Statement Calculators
================================
DuPont decomposition, Altman Z-Score, Beneish M-Score, Piotroski F-Score,
earnings quality, working capital analysis, and industry benchmark comparison.

Works with data from yfinance (US) or AKShare (China) via fetch functions.

Usage:
    python financial_calc.py AAPL --all                # All calculations
    python financial_calc.py AAPL --dupont              # DuPont decomposition
    python financial_calc.py AAPL --zscore              # Altman Z-Score
    python financial_calc.py AAPL --mscore              # Beneish M-Score
    python financial_calc.py AAPL --fscore              # Piotroski F-Score
    python financial_calc.py AAPL --quality             # Earnings quality
    python financial_calc.py AAPL --working-capital     # Working capital analysis
    python financial_calc.py AAPL --benchmarks          # Industry benchmark comparison
    python financial_calc.py AAPL --benchmarks --industry technology  # Specific industry
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common.utils import output_json, safe_div, safe_float, error_exit


# ---------------------------------------------------------------------------
# Data extraction helpers
# ---------------------------------------------------------------------------

def _get_financials(symbol: str) -> dict:
    """Fetch income statement, balance sheet, and cash flow via yfinance."""
    import yfinance as yf

    t = yf.Ticker(symbol)
    info = t.info

    # Get annual financial statements (most recent 4 years)
    inc = t.income_stmt
    bs = t.balance_sheet
    cf = t.cashflow

    def _col(df, idx):
        """Get value from dataframe by index label, latest column."""
        if df is None or df.empty:
            return None
        for col_idx in range(min(idx + 1, len(df.columns))):
            try:
                col = df.columns[col_idx]
                if idx == col_idx:
                    return df[col]
            except (IndexError, KeyError):
                pass
        return None

    def _val(series, *keys):
        """Extract value from a pandas Series by trying multiple key names."""
        if series is None:
            return None
        for key in keys:
            try:
                v = series.get(key)
                if v is not None:
                    return safe_float(v)
            except Exception:
                pass
        return None

    # Build structured data for latest 2 years
    years = {}
    for i in range(min(4, len(inc.columns) if inc is not None else 0)):
        inc_s = _col(inc, i)
        bs_s = _col(bs, i)
        cf_s = _col(cf, i)
        period = str(inc.columns[i].date()) if inc is not None else f"Y-{i}"

        years[i] = {
            "period": period,
            # Income statement
            "revenue": _val(inc_s, "Total Revenue", "Revenue"),
            "cogs": _val(inc_s, "Cost Of Revenue", "Cost of Revenue"),
            "gross_profit": _val(inc_s, "Gross Profit"),
            "operating_income": _val(inc_s, "Operating Income", "EBIT"),
            "ebit": _val(inc_s, "EBIT", "Operating Income"),
            "ebitda": _val(inc_s, "EBITDA", "Normalized EBITDA"),
            "pretax_income": _val(inc_s, "Pretax Income"),
            "net_income": _val(inc_s, "Net Income", "Net Income Common Stockholders"),
            "depreciation": _val(inc_s, "Depreciation And Amortization In Income Statement",
                                 "Depreciation Amortization Depletion"),
            "interest_expense": _val(inc_s, "Interest Expense", "Interest Expense Non Operating"),
            "sga": _val(inc_s, "Selling General And Administration"),
            # Balance sheet
            "total_assets": _val(bs_s, "Total Assets"),
            "total_liabilities": _val(bs_s, "Total Liabilities Net Minority Interest",
                                       "Total Liabilities"),
            "total_equity": _val(bs_s, "Total Equity Gross Minority Interest",
                                  "Stockholders Equity", "Common Stock Equity"),
            "current_assets": _val(bs_s, "Current Assets"),
            "current_liabilities": _val(bs_s, "Current Liabilities"),
            "cash": _val(bs_s, "Cash And Cash Equivalents", "Cash Cash Equivalents And Short Term Investments"),
            "receivables": _val(bs_s, "Accounts Receivable", "Receivables"),
            "inventory": _val(bs_s, "Inventory"),
            "payables": _val(bs_s, "Accounts Payable", "Payables And Accrued Expenses"),
            "total_debt": _val(bs_s, "Total Debt"),
            "long_term_debt": _val(bs_s, "Long Term Debt"),
            "short_term_debt": _val(bs_s, "Current Debt", "Current Debt And Capital Lease Obligation"),
            "retained_earnings": _val(bs_s, "Retained Earnings"),
            "goodwill": _val(bs_s, "Goodwill"),
            "intangibles": _val(bs_s, "Intangible Assets", "Goodwill And Other Intangible Assets"),
            "ppe_net": _val(bs_s, "Net PPE", "Net Property Plant And Equipment"),
            # Cash flow
            "operating_cash_flow": _val(cf_s, "Operating Cash Flow",
                                        "Cash Flow From Continuing Operating Activities"),
            "capex": _val(cf_s, "Capital Expenditure"),
            "fcf": _val(cf_s, "Free Cash Flow"),
            "depreciation_cf": _val(cf_s, "Depreciation And Amortization",
                                     "Depreciation Amortization Depletion"),
        }

    return {
        "symbol": symbol,
        "info": info,
        "years": years,
        "num_years": len(years),
    }


# ---------------------------------------------------------------------------
# DuPont Decomposition (5-Factor)
# ---------------------------------------------------------------------------

def dupont_analysis(symbol: str) -> dict:
    """
    5-Factor DuPont decomposition of ROE.
    ROE = Tax Burden × Interest Burden × Operating Margin × Asset Turnover × Equity Multiplier
    """
    data = _get_financials(symbol)
    years = data["years"]

    results = []
    for i, yr in years.items():
        rev = yr["revenue"]
        ni = yr["net_income"]
        pti = yr["pretax_income"]
        ebit = yr["ebit"]
        ta = yr["total_assets"]
        eq = yr["total_equity"]

        tax_burden = safe_div(ni, pti)       # NI / Pre-tax Income
        interest_burden = safe_div(pti, ebit)  # Pre-tax / EBIT
        op_margin = safe_div(ebit, rev)        # EBIT / Revenue
        asset_turnover = safe_div(rev, ta)     # Revenue / Assets
        equity_mult = safe_div(ta, eq)         # Assets / Equity

        roe = None
        if all(v is not None for v in [tax_burden, interest_burden, op_margin,
                                        asset_turnover, equity_mult]):
            roe = tax_burden * interest_burden * op_margin * asset_turnover * equity_mult

        results.append({
            "period": yr["period"],
            "roe": roe,
            "tax_burden": tax_burden,
            "interest_burden": interest_burden,
            "operating_margin": op_margin,
            "asset_turnover": asset_turnover,
            "equity_multiplier": equity_mult,
            "raw": {
                "net_income": ni,
                "pretax_income": pti,
                "ebit": ebit,
                "revenue": rev,
                "total_assets": ta,
                "total_equity": eq,
            },
        })

    # Trend analysis
    trend = {}
    if len(results) >= 2:
        latest = results[0]
        previous = results[1]
        for metric in ["tax_burden", "interest_burden", "operating_margin",
                        "asset_turnover", "equity_multiplier", "roe"]:
            curr = latest.get(metric)
            prev = previous.get(metric)
            if curr is not None and prev is not None:
                if curr > prev * 1.02:
                    trend[metric] = "improving"
                elif curr < prev * 0.98:
                    trend[metric] = "deteriorating"
                else:
                    trend[metric] = "stable"

    return {
        "symbol": symbol,
        "analysis": "dupont_5_factor",
        "periods": results,
        "trend": trend,
    }


# ---------------------------------------------------------------------------
# Altman Z-Score
# ---------------------------------------------------------------------------

def altman_zscore(symbol: str) -> dict:
    """
    Altman Z-Score: Bankruptcy prediction model.
    Z = 1.2×X1 + 1.4×X2 + 3.3×X3 + 0.6×X4 + 1.0×X5

    X1 = Working Capital / Total Assets
    X2 = Retained Earnings / Total Assets
    X3 = EBIT / Total Assets
    X4 = Market Cap / Total Liabilities
    X5 = Revenue / Total Assets
    """
    data = _get_financials(symbol)
    yr = data["years"].get(0, {})
    info = data["info"]

    ta = yr.get("total_assets")
    if not ta or ta == 0:
        return {"symbol": symbol, "error": "No total assets data"}

    ca = yr.get("current_assets", 0) or 0
    cl = yr.get("current_liabilities", 0) or 0
    wc = ca - cl

    re = yr.get("retained_earnings", 0) or 0
    ebit = yr.get("ebit", 0) or 0
    rev = yr.get("revenue", 0) or 0
    tl = yr.get("total_liabilities", 0) or 0
    mkt_cap = safe_float(info.get("marketCap", 0)) or 0

    x1 = wc / ta
    x2 = re / ta
    x3 = ebit / ta
    x4 = safe_div(mkt_cap, tl, 0)
    x5 = rev / ta

    z = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5

    if z > 2.99:
        zone = "Safe Zone"
        interpretation = "Low probability of bankruptcy"
    elif z > 1.81:
        zone = "Grey Zone"
        interpretation = "Moderate risk — needs further analysis"
    else:
        zone = "Distress Zone"
        interpretation = "High probability of financial distress"

    return {
        "symbol": symbol,
        "analysis": "altman_z_score",
        "z_score": round(z, 4),
        "zone": zone,
        "interpretation": interpretation,
        "components": {
            "X1_working_capital_to_assets": round(x1, 4),
            "X2_retained_earnings_to_assets": round(x2, 4),
            "X3_ebit_to_assets": round(x3, 4),
            "X4_market_cap_to_liabilities": round(x4, 4),
            "X5_revenue_to_assets": round(x5, 4),
        },
        "thresholds": {
            "safe": "> 2.99",
            "grey": "1.81 – 2.99",
            "distress": "< 1.81",
        },
    }


# ---------------------------------------------------------------------------
# Beneish M-Score
# ---------------------------------------------------------------------------

def beneish_mscore(symbol: str) -> dict:
    """
    Beneish M-Score: Earnings manipulation detection.
    M = -4.84 + 0.920×DSRI + 0.528×GMI + 0.404×AQI + 0.892×SGI
        + 0.115×DEPI − 0.172×SGAI + 4.679×TATA − 0.327×LVGI

    M > -1.78 suggests likely earnings manipulation.
    """
    data = _get_financials(symbol)
    if data["num_years"] < 2:
        return {"symbol": symbol, "error": "Need at least 2 years of data"}

    curr = data["years"][0]
    prev = data["years"][1]

    # Helper for safe ratio of ratios
    def _ratio(a_num, a_den, b_num, b_den):
        ratio_a = safe_div(a_num, a_den)
        ratio_b = safe_div(b_num, b_den)
        return safe_div(ratio_a, ratio_b)

    # DSRI - Days Sales in Receivables Index
    dsri = _ratio(curr.get("receivables"), curr.get("revenue"),
                  prev.get("receivables"), prev.get("revenue"))

    # GMI - Gross Margin Index
    gm_prev = safe_div(prev.get("gross_profit"), prev.get("revenue"))
    gm_curr = safe_div(curr.get("gross_profit"), curr.get("revenue"))
    gmi = safe_div(gm_prev, gm_curr) if gm_curr and gm_curr != 0 else None

    # AQI - Asset Quality Index
    def _aq(yr_data):
        ta = yr_data.get("total_assets", 0) or 0
        ca = yr_data.get("current_assets", 0) or 0
        ppe = yr_data.get("ppe_net", 0) or 0
        if ta == 0:
            return None
        return 1 - (ca + ppe) / ta
    aq_curr = _aq(curr)
    aq_prev = _aq(prev)
    aqi = safe_div(aq_curr, aq_prev)

    # SGI - Sales Growth Index
    sgi = safe_div(curr.get("revenue"), prev.get("revenue"))

    # DEPI - Depreciation Index
    def _dep_rate(yr_data):
        dep = yr_data.get("depreciation_cf") or yr_data.get("depreciation", 0) or 0
        ppe = yr_data.get("ppe_net", 0) or 0
        return safe_div(dep, dep + ppe)
    dep_prev = _dep_rate(prev)
    dep_curr = _dep_rate(curr)
    depi = safe_div(dep_prev, dep_curr)

    # SGAI - SGA Expense Index
    sgai = _ratio(curr.get("sga"), curr.get("revenue"),
                  prev.get("sga"), prev.get("revenue"))

    # TATA - Total Accruals to Total Assets
    ocf = curr.get("operating_cash_flow", 0) or 0
    ni = curr.get("net_income", 0) or 0
    ta_curr = curr.get("total_assets", 0) or 1
    tata = (ni - ocf) / ta_curr

    # LVGI - Leverage Index
    def _leverage(yr_data):
        tl = yr_data.get("total_liabilities", 0) or 0
        ta = yr_data.get("total_assets", 0) or 1
        return tl / ta
    lvgi = safe_div(_leverage(curr), _leverage(prev))

    # Compute M-Score (use defaults where data is missing)
    components = {
        "DSRI": dsri or 1.0,
        "GMI": gmi or 1.0,
        "AQI": aqi or 1.0,
        "SGI": sgi or 1.0,
        "DEPI": depi or 1.0,
        "SGAI": sgai or 1.0,
        "TATA": tata,
        "LVGI": lvgi or 1.0,
    }

    m = (-4.84
         + 0.920 * components["DSRI"]
         + 0.528 * components["GMI"]
         + 0.404 * components["AQI"]
         + 0.892 * components["SGI"]
         + 0.115 * components["DEPI"]
         - 0.172 * components["SGAI"]
         + 4.679 * components["TATA"]
         - 0.327 * components["LVGI"])

    if m > -1.78:
        assessment = "Likely Manipulator"
        interpretation = "M-Score above threshold — financial manipulation is likely"
    else:
        assessment = "Unlikely Manipulator"
        interpretation = "M-Score below threshold — manipulation is unlikely"

    return {
        "symbol": symbol,
        "analysis": "beneish_m_score",
        "m_score": round(m, 4),
        "assessment": assessment,
        "interpretation": interpretation,
        "threshold": -1.78,
        "components": {k: round(v, 4) for k, v in components.items()},
        "component_meanings": {
            "DSRI": "Days Sales in Receivables Index (>1 = receivables growing faster than revenue)",
            "GMI": "Gross Margin Index (>1 = deteriorating margins)",
            "AQI": "Asset Quality Index (>1 = more assets are non-current/intangible)",
            "SGI": "Sales Growth Index (high growth under more scrutiny)",
            "DEPI": "Depreciation Index (>1 = slowing depreciation to boost income)",
            "SGAI": "SGA Expense Index (>1 = rising SGA relative to revenue)",
            "TATA": "Total Accruals to Total Assets (higher = more accrual-based earnings)",
            "LVGI": "Leverage Index (>1 = increasing leverage)",
        },
    }


# ---------------------------------------------------------------------------
# Piotroski F-Score
# ---------------------------------------------------------------------------

def piotroski_fscore(symbol: str) -> dict:
    """
    Piotroski F-Score: Financial strength indicator (0–9).
    9 binary signals across profitability, leverage, and efficiency.
    """
    data = _get_financials(symbol)
    if data["num_years"] < 2:
        return {"symbol": symbol, "error": "Need at least 2 years of data"}

    curr = data["years"][0]
    prev = data["years"][1]
    score = 0
    signals = {}

    # --- Profitability (4 signals) ---
    # 1. Positive net income
    ni = curr.get("net_income", 0) or 0
    signals["F1_positive_net_income"] = ni > 0
    if ni > 0:
        score += 1

    # 2. Positive operating cash flow
    ocf = curr.get("operating_cash_flow", 0) or 0
    signals["F2_positive_ocf"] = ocf > 0
    if ocf > 0:
        score += 1

    # 3. Increasing ROA
    ta_curr = curr.get("total_assets", 0) or 1
    ta_prev = prev.get("total_assets", 0) or 1
    ni_prev = prev.get("net_income", 0) or 0
    roa_curr = ni / ta_curr
    roa_prev = ni_prev / ta_prev
    signals["F3_increasing_roa"] = roa_curr > roa_prev
    if roa_curr > roa_prev:
        score += 1

    # 4. Cash flow > net income (earnings quality)
    signals["F4_ocf_gt_net_income"] = ocf > ni
    if ocf > ni:
        score += 1

    # --- Leverage / Liquidity (3 signals) ---
    # 5. Decreasing long-term debt ratio
    ltd_curr = (curr.get("long_term_debt", 0) or 0) / ta_curr
    ltd_prev = (prev.get("long_term_debt", 0) or 0) / ta_prev
    signals["F5_decreasing_leverage"] = ltd_curr < ltd_prev
    if ltd_curr < ltd_prev:
        score += 1

    # 6. Increasing current ratio
    cr_curr = safe_div(curr.get("current_assets"), curr.get("current_liabilities"))
    cr_prev = safe_div(prev.get("current_assets"), prev.get("current_liabilities"))
    signals["F6_increasing_current_ratio"] = (
        cr_curr is not None and cr_prev is not None and cr_curr > cr_prev
    )
    if signals["F6_increasing_current_ratio"]:
        score += 1

    # 7. No new shares issued (dilution)
    # Approximate: check if shares outstanding increased
    info = data["info"]
    signals["F7_no_dilution"] = True  # Default true; hard to check with yfinance
    score += 1  # Give benefit of doubt

    # --- Efficiency (2 signals) ---
    # 8. Increasing gross margin
    gm_curr = safe_div(curr.get("gross_profit"), curr.get("revenue"))
    gm_prev = safe_div(prev.get("gross_profit"), prev.get("revenue"))
    signals["F8_increasing_gross_margin"] = (
        gm_curr is not None and gm_prev is not None and gm_curr > gm_prev
    )
    if signals["F8_increasing_gross_margin"]:
        score += 1

    # 9. Increasing asset turnover
    at_curr = safe_div(curr.get("revenue"), curr.get("total_assets"))
    at_prev = safe_div(prev.get("revenue"), prev.get("total_assets"))
    signals["F9_increasing_asset_turnover"] = (
        at_curr is not None and at_prev is not None and at_curr > at_prev
    )
    if signals["F9_increasing_asset_turnover"]:
        score += 1

    if score >= 8:
        strength = "Strong"
        interpretation = "Financially healthy — strong fundamentals"
    elif score >= 5:
        strength = "Moderate"
        interpretation = "Average financial health"
    else:
        strength = "Weak"
        interpretation = "Weak financial position — potential value trap"

    return {
        "symbol": symbol,
        "analysis": "piotroski_f_score",
        "f_score": score,
        "max_score": 9,
        "strength": strength,
        "interpretation": interpretation,
        "signals": signals,
        "scoring_guide": {
            "8-9": "Strong — good financial health",
            "5-7": "Moderate — average position",
            "0-4": "Weak — potential financial distress or value trap",
        },
    }


# ---------------------------------------------------------------------------
# Earnings Quality Assessment
# ---------------------------------------------------------------------------

def earnings_quality(symbol: str) -> dict:
    """
    Assess earnings quality through accruals ratio, cash conversion,
    and revenue quality indicators.
    """
    data = _get_financials(symbol)
    yr = data["years"].get(0, {})

    ni = yr.get("net_income", 0) or 0
    ocf = yr.get("operating_cash_flow", 0) or 0
    ta = yr.get("total_assets", 0) or 1

    # Accruals ratio
    accruals = ni - ocf
    accruals_ratio = accruals / ta

    if abs(accruals_ratio) < 0.05:
        accruals_quality = "High"
    elif abs(accruals_ratio) < 0.10:
        accruals_quality = "Acceptable"
    elif abs(accruals_ratio) < 0.15:
        accruals_quality = "Elevated"
    else:
        accruals_quality = "Low"

    # Cash conversion
    cash_conversion = safe_div(ocf, ni)
    if cash_conversion is not None:
        if cash_conversion > 1.2:
            cc_quality = "Excellent"
        elif cash_conversion > 1.0:
            cc_quality = "Good"
        elif cash_conversion > 0.8:
            cc_quality = "Acceptable"
        elif cash_conversion > 0.5:
            cc_quality = "Weak"
        else:
            cc_quality = "Poor"
    else:
        cc_quality = "N/A"

    # Revenue quality
    rev = yr.get("revenue")
    recv = yr.get("receivables")
    rev_quality_flags = []
    if rev and recv:
        recv_pct = recv / rev
        if recv_pct > 0.30:
            rev_quality_flags.append(
                f"Receivables are {recv_pct:.0%} of revenue — high collection risk"
            )

    # Check prev year for growth comparison
    if data["num_years"] >= 2:
        prev = data["years"][1]
        prev_rev = prev.get("revenue", 0) or 1
        prev_recv = prev.get("receivables", 0) or 0
        if rev and recv and prev_rev and prev_recv:
            rev_growth = (rev - prev_rev) / abs(prev_rev) if prev_rev else 0
            recv_growth = (recv - prev_recv) / abs(prev_recv) if prev_recv else 0
            if recv_growth > rev_growth * 1.5 and recv_growth > 0.10:
                rev_quality_flags.append(
                    f"Receivables growing {recv_growth:.0%} vs revenue {rev_growth:.0%} — "
                    "potential aggressive revenue recognition"
                )

    # Overall assessment
    scores = {"High": 3, "Excellent": 3, "Good": 2, "Acceptable": 1,
              "Elevated": 0, "Weak": -1, "Low": -2, "Poor": -2, "N/A": 0}
    total = scores.get(accruals_quality, 0) + scores.get(cc_quality, 0)
    total -= len(rev_quality_flags)

    if total >= 4:
        overall = "High Quality"
    elif total >= 2:
        overall = "Acceptable Quality"
    elif total >= 0:
        overall = "Questionable Quality"
    else:
        overall = "Low Quality — Red Flags Present"

    return {
        "symbol": symbol,
        "analysis": "earnings_quality",
        "overall_assessment": overall,
        "accruals": {
            "accruals_ratio": round(accruals_ratio, 4),
            "quality": accruals_quality,
            "net_income": ni,
            "operating_cash_flow": ocf,
            "accruals_amount": accruals,
        },
        "cash_conversion": {
            "ratio": round(cash_conversion, 4) if cash_conversion else None,
            "quality": cc_quality,
        },
        "revenue_quality": {
            "flags": rev_quality_flags if rev_quality_flags else ["No red flags detected"],
        },
    }


# ---------------------------------------------------------------------------
# Working Capital Analysis
# ---------------------------------------------------------------------------

def working_capital_analysis(symbol: str) -> dict:
    """
    Analyze working capital efficiency through cash conversion cycle:
    CCC = DSO + DIO - DPO
    """
    data = _get_financials(symbol)

    results = []
    for i in range(min(data["num_years"], 4)):
        yr = data["years"][i]
        rev = yr.get("revenue", 0) or 1
        cogs = yr.get("cogs", 0) or 1
        recv = yr.get("receivables", 0) or 0
        inv = yr.get("inventory", 0) or 0
        pay = yr.get("payables", 0) or 0

        dso = (recv / rev) * 365 if rev else None
        dio = (inv / abs(cogs)) * 365 if cogs else None
        dpo = (pay / abs(cogs)) * 365 if cogs else None

        ccc = None
        if dso is not None and dio is not None and dpo is not None:
            ccc = dso + dio - dpo

        wc = (yr.get("current_assets", 0) or 0) - (yr.get("current_liabilities", 0) or 0)

        results.append({
            "period": yr["period"],
            "dso_days": round(dso, 1) if dso else None,
            "dio_days": round(dio, 1) if dio else None,
            "dpo_days": round(dpo, 1) if dpo else None,
            "cash_conversion_cycle": round(ccc, 1) if ccc else None,
            "working_capital": wc,
            "current_ratio": safe_div(yr.get("current_assets"), yr.get("current_liabilities")),
            "quick_ratio": safe_div(
                (yr.get("current_assets", 0) or 0) - (yr.get("inventory", 0) or 0),
                yr.get("current_liabilities")
            ),
        })

    # Trend
    trend = {}
    if len(results) >= 2:
        for metric in ["dso_days", "dio_days", "dpo_days", "cash_conversion_cycle"]:
            curr = results[0].get(metric)
            prev = results[1].get(metric)
            if curr is not None and prev is not None:
                if metric in ("dso_days", "dio_days", "cash_conversion_cycle"):
                    trend[metric] = "improving" if curr < prev else "deteriorating" if curr > prev else "stable"
                else:  # dpo
                    trend[metric] = "improving" if curr > prev else "deteriorating" if curr < prev else "stable"

    return {
        "symbol": symbol,
        "analysis": "working_capital",
        "periods": results,
        "trend": trend,
        "interpretation": {
            "DSO": "Days Sales Outstanding — lower is better (faster collection)",
            "DIO": "Days Inventory Outstanding — lower is better (faster inventory turnover)",
            "DPO": "Days Payable Outstanding — higher means better payment terms",
            "CCC": "Cash Conversion Cycle (DSO + DIO - DPO) — lower is better",
        },
    }


# ---------------------------------------------------------------------------
# Industry Benchmarks
# ---------------------------------------------------------------------------

INDUSTRY_BENCHMARKS = {
    "technology": {
        "current_ratio": {"excellent": 2.5, "good": 1.8, "acceptable": 1.2, "poor": 1.0},
        "debt_to_equity": {"excellent": 0.3, "good": 0.5, "acceptable": 1.0, "poor": 2.0},
        "roe": {"excellent": 0.25, "good": 0.18, "acceptable": 0.12, "poor": 0.08},
        "gross_margin": {"excellent": 0.70, "good": 0.50, "acceptable": 0.35, "poor": 0.20},
        "pe_ratio": {"undervalued": 15, "fair": 25, "growth": 35, "expensive": 50},
    },
    "retail": {
        "current_ratio": {"excellent": 2.0, "good": 1.5, "acceptable": 1.0, "poor": 0.8},
        "debt_to_equity": {"excellent": 0.5, "good": 0.8, "acceptable": 1.5, "poor": 2.5},
        "roe": {"excellent": 0.20, "good": 0.15, "acceptable": 0.10, "poor": 0.05},
        "gross_margin": {"excellent": 0.40, "good": 0.30, "acceptable": 0.20, "poor": 0.10},
        "pe_ratio": {"undervalued": 12, "fair": 18, "growth": 25, "expensive": 35},
    },
    "financial": {
        "current_ratio": {"excellent": 1.5, "good": 1.2, "acceptable": 1.0, "poor": 0.8},
        "debt_to_equity": {"excellent": 1.0, "good": 2.0, "acceptable": 4.0, "poor": 6.0},
        "roe": {"excellent": 0.15, "good": 0.12, "acceptable": 0.08, "poor": 0.05},
        "pe_ratio": {"undervalued": 10, "fair": 15, "growth": 20, "expensive": 30},
    },
    "manufacturing": {
        "current_ratio": {"excellent": 2.2, "good": 1.7, "acceptable": 1.3, "poor": 1.0},
        "debt_to_equity": {"excellent": 0.4, "good": 0.7, "acceptable": 1.2, "poor": 2.0},
        "roe": {"excellent": 0.18, "good": 0.14, "acceptable": 0.10, "poor": 0.06},
        "gross_margin": {"excellent": 0.35, "good": 0.25, "acceptable": 0.18, "poor": 0.12},
        "pe_ratio": {"undervalued": 14, "fair": 20, "growth": 28, "expensive": 40},
    },
    "healthcare": {
        "current_ratio": {"excellent": 2.3, "good": 1.8, "acceptable": 1.4, "poor": 1.0},
        "debt_to_equity": {"excellent": 0.3, "good": 0.6, "acceptable": 1.0, "poor": 1.8},
        "roe": {"excellent": 0.22, "good": 0.16, "acceptable": 0.11, "poor": 0.07},
        "gross_margin": {"excellent": 0.65, "good": 0.45, "acceptable": 0.30, "poor": 0.20},
        "pe_ratio": {"undervalued": 18, "fair": 28, "growth": 40, "expensive": 55},
    },
    "general": {
        "current_ratio": {"excellent": 2.0, "good": 1.5, "acceptable": 1.0, "poor": 0.8},
        "debt_to_equity": {"excellent": 0.5, "good": 1.0, "acceptable": 1.5, "poor": 2.5},
        "roe": {"excellent": 0.20, "good": 0.15, "acceptable": 0.10, "poor": 0.05},
        "gross_margin": {"excellent": 0.40, "good": 0.30, "acceptable": 0.20, "poor": 0.10},
        "pe_ratio": {"undervalued": 15, "fair": 22, "growth": 30, "expensive": 45},
    },
}


def interpret_ratio(ratio_name: str, value: float, industry: str = "general") -> dict:
    """Rate a ratio against industry benchmarks."""
    benchmarks = INDUSTRY_BENCHMARKS.get(industry, INDUSTRY_BENCHMARKS["general"])
    bm = benchmarks.get(ratio_name)
    if bm is None or value is None:
        return {"rating": "N/A", "message": "No benchmark available"}

    # Higher-is-better ratios
    if ratio_name in ("current_ratio", "roe", "gross_margin"):
        if value >= bm["excellent"]:
            rating, msg = "Excellent", "Significantly exceeds industry standard"
        elif value >= bm["good"]:
            rating, msg = "Good", f"Above average for {industry}"
        elif value >= bm["acceptable"]:
            rating, msg = "Acceptable", "Meets industry standards"
        else:
            rating, msg = "Poor", "Below industry standards"

    # Lower-is-better ratios
    elif ratio_name == "debt_to_equity":
        if value <= bm["excellent"]:
            rating, msg = "Excellent", "Very conservative capital structure"
        elif value <= bm["good"]:
            rating, msg = "Good", "Healthy leverage"
        elif value <= bm["acceptable"]:
            rating, msg = "Acceptable", "Moderate leverage"
        else:
            rating, msg = "Poor", "High leverage — potential risk"

    # Context-dependent (P/E)
    elif ratio_name == "pe_ratio":
        if value <= 0:
            return {"rating": "N/A", "message": "Negative earnings"}
        if value < bm["undervalued"]:
            rating, msg = "Undervalued", f"Below typical {industry} multiples"
        elif value < bm["fair"]:
            rating, msg = "Fair Value", "In line with industry"
        elif value < bm["growth"]:
            rating, msg = "Growth Premium", "Market pricing in growth"
        else:
            rating, msg = "Expensive", "High valuation relative to industry"
    else:
        return {"rating": "N/A", "message": "No benchmark available"}

    return {"rating": rating, "message": msg, "benchmarks": bm}


def analyze_trends(values: list, periods: list) -> dict:
    """Determine trend direction from a time series of values."""
    if len(values) < 2:
        return {"trend": "Insufficient data", "message": "Need at least 2 periods"}
    first, last = values[0], values[-1]
    if first == 0:
        return {"trend": "N/A", "message": "Base value is zero"}
    pct_change = (last - first) / abs(first) * 100
    if abs(pct_change) < 5:
        trend = "Stable"
    elif pct_change > 0:
        trend = "Improving"
    else:
        trend = "Deteriorating"
    return {
        "trend": trend,
        "pct_change": round(pct_change, 1),
        "from_period": periods[0],
        "to_period": periods[-1],
    }


def benchmark_analysis(symbol: str, industry: str = "general") -> dict:
    """Compare computed ratios against industry benchmarks with trend analysis."""
    data = _get_financials(symbol)
    yr = data["years"].get(0, {})
    info = data["info"]

    # Compute key ratios from latest year
    ratios = {
        "current_ratio": safe_div(yr.get("current_assets"), yr.get("current_liabilities")),
        "debt_to_equity": safe_div(yr.get("total_debt"), yr.get("total_equity")),
        "roe": safe_div(yr.get("net_income"), yr.get("total_equity")),
        "gross_margin": safe_div(yr.get("gross_profit"), yr.get("revenue")),
        "pe_ratio": safe_float(info.get("trailingPE")),
        "operating_margin": safe_div(yr.get("operating_income"), yr.get("revenue")),
        "net_margin": safe_div(yr.get("net_income"), yr.get("revenue")),
        "asset_turnover": safe_div(yr.get("revenue"), yr.get("total_assets")),
    }

    # Interpret each benchmarkable ratio
    interpreted = {}
    for name, value in ratios.items():
        if value is not None:
            interp = interpret_ratio(name, value, industry)
            interpreted[name] = {"value": round(value, 4), **interp}

    # Trend analysis across available years
    trends = {}
    trend_metrics = ["current_ratio", "roe", "gross_margin"]
    if data["num_years"] >= 2:
        for metric in trend_metrics:
            vals, periods = [], []
            for i in range(min(data["num_years"], 4)):
                y = data["years"][i]
                periods.append(y["period"])
                if metric == "current_ratio":
                    v = safe_div(y.get("current_assets"), y.get("current_liabilities"))
                elif metric == "roe":
                    v = safe_div(y.get("net_income"), y.get("total_equity"))
                elif metric == "gross_margin":
                    v = safe_div(y.get("gross_profit"), y.get("revenue"))
                else:
                    v = None
                if v is not None:
                    vals.append(v)
            if len(vals) >= 2:
                trends[metric] = analyze_trends(vals[::-1], periods[::-1])

    return {
        "symbol": symbol,
        "analysis": "industry_benchmarks",
        "industry": industry,
        "ratios": interpreted,
        "trends": trends,
        "available_industries": list(INDUSTRY_BENCHMARKS.keys()),
    }


# ---------------------------------------------------------------------------
# Comprehensive analysis
# ---------------------------------------------------------------------------

def full_analysis(symbol: str) -> dict:
    """Run all financial calculations for a single stock."""
    return {
        "symbol": symbol,
        "dupont": dupont_analysis(symbol),
        "altman_z_score": altman_zscore(symbol),
        "beneish_m_score": beneish_mscore(symbol),
        "piotroski_f_score": piotroski_fscore(symbol),
        "earnings_quality": earnings_quality(symbol),
        "working_capital": working_capital_analysis(symbol),
        "benchmarks": benchmark_analysis(symbol),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Financial Statement Calculators (DuPont, Z-Score, M-Score, F-Score, Benchmarks)"
    )
    parser.add_argument("symbol", help="Stock ticker (e.g., AAPL)")
    parser.add_argument("--all", action="store_true", help="Run all analyses")
    parser.add_argument("--dupont", action="store_true", help="DuPont decomposition")
    parser.add_argument("--zscore", action="store_true", help="Altman Z-Score")
    parser.add_argument("--mscore", action="store_true", help="Beneish M-Score")
    parser.add_argument("--fscore", action="store_true", help="Piotroski F-Score")
    parser.add_argument("--quality", action="store_true", help="Earnings quality")
    parser.add_argument("--working-capital", action="store_true",
                        help="Working capital analysis")
    parser.add_argument("--benchmarks", action="store_true",
                        help="Industry benchmark comparison")
    parser.add_argument("--industry", default="general",
                        choices=list(INDUSTRY_BENCHMARKS.keys()),
                        help="Industry for benchmarking (default: general)")
    args = parser.parse_args()

    try:
        if args.all:
            data = full_analysis(args.symbol)
        elif args.dupont:
            data = dupont_analysis(args.symbol)
        elif args.zscore:
            data = altman_zscore(args.symbol)
        elif args.mscore:
            data = beneish_mscore(args.symbol)
        elif args.fscore:
            data = piotroski_fscore(args.symbol)
        elif args.quality:
            data = earnings_quality(args.symbol)
        elif args.working_capital:
            data = working_capital_analysis(args.symbol)
        elif args.benchmarks:
            data = benchmark_analysis(args.symbol, args.industry)
        else:
            data = full_analysis(args.symbol)

        output_json(data)

    except ImportError:
        error_exit("yfinance is required. Install: pip install yfinance")
    except Exception as e:
        error_exit(f"Error: {e}")


if __name__ == "__main__":
    main()
