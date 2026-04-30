#!/usr/bin/env python3
"""
DCF Valuation Model
===================
Discounted Cash Flow valuation with enterprise value, equity value, WACC,
and built-in sensitivity analysis.

Usage:
    python dcf_model.py AAPL                         # Full DCF valuation
    python dcf_model.py AAPL --wacc-only             # Just WACC calculation
    python dcf_model.py AAPL --sensitivity           # Two-way sensitivity
    python dcf_model.py AAPL --tornado               # Tornado chart data
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common.utils import output_json, output_table, safe_div, safe_float, error_exit


# ---------------------------------------------------------------------------
# Data fetching helpers
# ---------------------------------------------------------------------------

def _fetch_financials(symbol: str) -> dict:
    """Fetch key financial data from yfinance for DCF inputs."""
    import yfinance as yf

    t = yf.Ticker(symbol)
    info = t.info

    # Extract financial statements
    inc = t.income_stmt
    bs = t.balance_sheet
    cf = t.cashflow
    history = t.history(period="5y")

    result = {}

    # Revenue (trailing 3 years)
    if inc is not None and not inc.empty:
        try:
            rev_rows = inc.loc["Total Revenue"] if "Total Revenue" in inc.index else inc.iloc[0]
            result["revenue"] = [float(v) for v in rev_rows.iloc[:3].values[::-1] if v and v != 0]
        except Exception:
            result["revenue"] = []

    # EBITDA
    try:
        ebitda = safe_float(info.get("ebitda"))
        if ebitda and not result.get("revenue"):
            result["revenue"] = [safe_float(info.get("totalRevenue", 0)) or 1000]
        if ebitda:
            result["ebitda"] = [ebitda / 1e6]  # Convert to millions
    except Exception:
        pass

    # Market cap, beta, shares
    result["market_cap"] = safe_float(info.get("marketCap")) or 0
    result["beta"] = safe_float(info.get("beta"), 1.0)
    result["shares_outstanding"] = safe_float(info.get("sharesOutstanding"), 100) / 1e6  # millions
    result["total_debt"] = safe_float(info.get("totalDebt"), 0)
    result["total_cash"] = safe_float(info.get("totalCash"), 0)

    # Historical returns for beta calculation
    if not history.empty and len(history) > 60:
        result["price_history"] = history["Close"].pct_change().dropna().tolist()

    return result


# ---------------------------------------------------------------------------
# DCF Model
# ---------------------------------------------------------------------------

class DCFModel:
    """Build and calculate DCF valuation models."""

    def __init__(self, company_name: str = "Company"):
        self.company_name = company_name
        self.historical_financials = {}
        self.projections = {}
        self.assumptions = {}
        self.wacc_components = {}
        self.valuation_results = {}

    def set_historical_financials(
        self,
        revenue: list[float],
        ebitda: list[float],
        capex: list[float],
        nwc: list[float],
        years: list[int],
    ):
        self.historical_financials = {
            "years": years,
            "revenue": revenue,
            "ebitda": ebitda,
            "capex": capex,
            "nwc": nwc,
            "ebitda_margin": [safe_div(ebitda[i], revenue[i], 0) for i in range(len(revenue))],
            "capex_percent": [safe_div(capex[i], revenue[i], 0) for i in range(len(revenue))],
        }

    def set_assumptions(
        self,
        projection_years: int = 5,
        revenue_growth: list[float] = None,
        ebitda_margin: list[float] = None,
        tax_rate: float = 0.25,
        capex_percent: list[float] = None,
        nwc_percent: list[float] = None,
        terminal_growth: float = 0.03,
    ):
        if revenue_growth is None:
            revenue_growth = [0.10] * projection_years
        if ebitda_margin is None:
            if self.historical_financials and self.historical_financials.get("ebitda_margin"):
                avg_margin = float(np.mean(self.historical_financials["ebitda_margin"]))
                ebitda_margin = [avg_margin] * projection_years
            else:
                ebitda_margin = [0.20] * projection_years
        if capex_percent is None:
            capex_percent = [0.05] * projection_years
        if nwc_percent is None:
            nwc_percent = [0.10] * projection_years

        self.assumptions = {
            "projection_years": projection_years,
            "revenue_growth": revenue_growth,
            "ebitda_margin": ebitda_margin,
            "tax_rate": tax_rate,
            "capex_percent": capex_percent,
            "nwc_percent": nwc_percent,
            "terminal_growth": terminal_growth,
        }

    def calculate_wacc(
        self,
        risk_free_rate: float,
        beta: float,
        market_premium: float,
        cost_of_debt: float,
        debt_to_equity: float,
        tax_rate: float | None = None,
    ) -> float:
        if tax_rate is None:
            tax_rate = self.assumptions.get("tax_rate", 0.25)

        cost_of_equity = risk_free_rate + beta * market_premium
        equity_weight = 1 / (1 + debt_to_equity)
        debt_weight = debt_to_equity / (1 + debt_to_equity)
        wacc = equity_weight * cost_of_equity + debt_weight * cost_of_debt * (1 - tax_rate)

        self.wacc_components = {
            "risk_free_rate": risk_free_rate,
            "beta": beta,
            "market_premium": market_premium,
            "cost_of_equity": cost_of_equity,
            "cost_of_debt": cost_of_debt,
            "debt_to_equity": debt_to_equity,
            "equity_weight": equity_weight,
            "debt_weight": debt_weight,
            "tax_rate": tax_rate,
            "wacc": wacc,
        }
        return wacc

    def project_cash_flows(self) -> dict[str, list[float]]:
        years = self.assumptions["projection_years"]
        if self.historical_financials and self.historical_financials.get("revenue"):
            base_revenue = self.historical_financials["revenue"][-1]
        else:
            base_revenue = 1000

        projections = {
            "year": list(range(1, years + 1)),
            "revenue": [],
            "ebitda": [],
            "ebit": [],
            "tax": [],
            "nopat": [],
            "capex": [],
            "nwc_change": [],
            "fcf": [],
        }

        prev_revenue = base_revenue
        prev_nwc = base_revenue * 0.10

        for i in range(years):
            revenue = prev_revenue * (1 + self.assumptions["revenue_growth"][i])
            projections["revenue"].append(revenue)
            ebitda = revenue * self.assumptions["ebitda_margin"][i]
            projections["ebitda"].append(ebitda)
            depreciation = revenue * self.assumptions["capex_percent"][i]
            ebit = ebitda - depreciation
            projections["ebit"].append(ebit)
            tax = ebit * self.assumptions["tax_rate"]
            projections["tax"].append(tax)
            nopat = ebit - tax
            projections["nopat"].append(nopat)
            capex = revenue * self.assumptions["capex_percent"][i]
            projections["capex"].append(capex)
            nwc = revenue * self.assumptions["nwc_percent"][i]
            nwc_change = nwc - prev_nwc
            projections["nwc_change"].append(nwc_change)
            fcf = nopat + depreciation - capex - nwc_change
            projections["fcf"].append(fcf)
            prev_revenue = revenue
            prev_nwc = nwc

        self.projections = projections
        return projections

    def calculate_terminal_value(
        self, method: str = "growth", exit_multiple: float | None = None
    ) -> float:
        if not self.projections:
            raise ValueError("Must project cash flows first")
        if method == "growth":
            final_fcf = self.projections["fcf"][-1]
            terminal_growth = self.assumptions["terminal_growth"]
            wacc_val = self.wacc_components["wacc"]
            terminal_fcf = final_fcf * (1 + terminal_growth)
            return terminal_fcf / (wacc_val - terminal_growth)
        elif method == "multiple":
            if exit_multiple is None:
                exit_multiple = 10
            final_ebitda = self.projections["ebitda"][-1]
            return final_ebitda * exit_multiple
        else:
            raise ValueError("Method must be 'growth' or 'multiple'")

    def calculate_enterprise_value(
        self, terminal_method: str = "growth", exit_multiple: float | None = None
    ) -> dict[str, Any]:
        if not self.projections:
            self.project_cash_flows()
        if "wacc" not in self.wacc_components:
            raise ValueError("Must calculate WACC first")

        wacc_val = self.wacc_components["wacc"]
        years = self.assumptions["projection_years"]

        pv_fcf = []
        for i, fcf in enumerate(self.projections["fcf"]):
            discount_factor = (1 + wacc_val) ** (i + 1)
            pv_fcf.append(fcf / discount_factor)

        total_pv_fcf = sum(pv_fcf)
        terminal_value = self.calculate_terminal_value(terminal_method, exit_multiple)
        terminal_discount = (1 + wacc_val) ** years
        pv_terminal = terminal_value / terminal_discount
        enterprise_value = total_pv_fcf + pv_terminal

        self.valuation_results = {
            "enterprise_value": enterprise_value,
            "pv_fcf": total_pv_fcf,
            "pv_terminal": pv_terminal,
            "terminal_value": terminal_value,
            "terminal_method": terminal_method,
            "pv_fcf_detail": pv_fcf,
            "terminal_percent": safe_div(pv_terminal, enterprise_value, 0) * 100,
        }
        return self.valuation_results

    def calculate_equity_value(
        self, net_debt: float, cash: float = 0, shares_outstanding: float = 100
    ) -> dict[str, Any]:
        if "enterprise_value" not in self.valuation_results:
            raise ValueError("Must calculate enterprise value first")

        ev = self.valuation_results["enterprise_value"]
        equity_value = ev - net_debt + cash
        value_per_share = equity_value / shares_outstanding if shares_outstanding > 0 else 0

        equity_results = {
            "equity_value": equity_value,
            "shares_outstanding": shares_outstanding,
            "value_per_share": value_per_share,
            "net_debt": net_debt,
            "cash": cash,
        }
        self.valuation_results.update(equity_results)
        return equity_results


# ---------------------------------------------------------------------------
# Sensitivity helpers (inline, no pandas dependency required)
# ---------------------------------------------------------------------------

def _tornado_analysis(
    model: DCFModel, variables: dict, output_func
) -> list[dict]:
    """Tornado analysis returning list of dicts (no pandas dependency)."""
    base_output = output_func()
    results = []

    for name, var in variables.items():
        var["update_func"](var["low"])
        low_output = output_func()
        var["update_func"](var["high"])
        high_output = output_func()
        var["update_func"](var["base"])

        impact = abs(high_output - low_output)
        results.append({
            "variable": name,
            "base_value": var["base"],
            "low_value": var["low"],
            "high_value": var["high"],
            "low_output": low_output,
            "high_output": high_output,
            "impact": impact,
            "impact_pct": safe_div(impact, base_output, 0) * 100,
        })

    results.sort(key=lambda x: x["impact"], reverse=True)
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_model(symbol: str) -> DCFModel:
    """Build a DCF model from live data for a symbol."""
    data = _fetch_financials(symbol)
    revenue = data.get("revenue", [1000])
    ebitda_vals = data.get("ebitda", [revenue[-1] * 0.22])
    ebitda_margin_hist = safe_div(ebitda_vals[0], revenue[-1], 0.22) if revenue and ebitda_vals else 0.22

    model = DCFModel(symbol.upper())

    # Pad revenue/ebitda to 3 years if needed
    while len(revenue) < 3:
        revenue.insert(0, revenue[0] * 0.9)
    while len(ebitda_vals) < 3:
        ebitda_vals.insert(0, ebitda_vals[0] * 0.9)

    model.set_historical_financials(
        revenue=revenue,
        ebitda=ebitda_vals,
        capex=[r * 0.05 for r in revenue],
        nwc=[r * 0.10 for r in revenue],
        years=list(range(2022, 2022 + len(revenue))),
    )

    # Derive growth from historical
    hist_growth = 0.10
    if len(revenue) >= 2:
        hist_growth = (revenue[-1] / revenue[0]) ** (1 / (len(revenue) - 1)) - 1
    growth_rates = [max(hist_growth - i * 0.02, 0.02) for i in range(5)]

    model.set_assumptions(
        projection_years=5,
        revenue_growth=growth_rates,
        ebitda_margin=[ebitda_margin_hist] * 5,
        tax_rate=0.21,
        terminal_growth=0.025,
    )

    beta = data.get("beta", 1.0)
    rf_rate = 0.04

    # Estimate WACC inputs
    model.calculate_wacc(
        risk_free_rate=rf_rate,
        beta=beta,
        market_premium=0.06,
        cost_of_debt=0.05,
        debt_to_equity=0.5,
    )

    model.project_cash_flows()
    return model


def main():
    parser = argparse.ArgumentParser(description="DCF Valuation Model")
    parser.add_argument("symbol", help="Stock ticker symbol")
    parser.add_argument("--wacc-only", action="store_true", help="Only calculate WACC")
    parser.add_argument("--sensitivity", action="store_true", help="Two-way sensitivity on WACC vs growth")
    parser.add_argument("--tornado", action="store_true", help="Tornado analysis of key drivers")
    parser.add_argument("--terminal-method", choices=["growth", "multiple"], default="growth",
                        help="Terminal value method")
    parser.add_argument("--exit-multiple", type=float, default=None, help="EV/EBITDA exit multiple")
    args = parser.parse_args()

    model = _build_model(args.symbol)

    if args.wacc_only:
        wacc_data = {k: (v if not isinstance(v, float) else round(v, 6))
                     for k, v in model.wacc_components.items()}
        output_json(wacc_data)
        return

    if args.tornado:
        model.calculate_enterprise_value(args.terminal_method, args.exit_multiple)

        def _ev_output():
            model.calculate_enterprise_value(args.terminal_method, args.exit_multiple)
            return model.valuation_results["enterprise_value"]

        variables = {
            "WACC": {
                "base": model.wacc_components["wacc"],
                "low": model.wacc_components["wacc"] * 0.7,
                "high": model.wacc_components["wacc"] * 1.3,
                "update_func": lambda v: model.wacc_components.update({"wacc": v}),
            },
            "Terminal Growth": {
                "base": model.assumptions["terminal_growth"],
                "low": 0.015,
                "high": 0.04,
                "update_func": lambda v: model.assumptions.update({"terminal_growth": v}),
            },
            "EBITDA Margin": {
                "base": model.assumptions["ebitda_margin"][0],
                "low": model.assumptions["ebitda_margin"][0] * 0.7,
                "high": model.assumptions["ebitda_margin"][0] * 1.3,
                "update_func": lambda v: model.assumptions.update(
                    {"ebitda_margin": [v] * model.assumptions["projection_years"]}
                ),
            },
            "Revenue Growth": {
                "base": model.assumptions["revenue_growth"][0],
                "low": max(model.assumptions["revenue_growth"][0] * 0.5, 0.01),
                "high": model.assumptions["revenue_growth"][0] * 1.5,
                "update_func": lambda v: model.assumptions.update(
                    {"revenue_growth": [v * (1 - i * 0.1) for i in range(model.assumptions["projection_years"])]}
                ),
            },
            "Tax Rate": {
                "base": model.assumptions["tax_rate"],
                "low": 0.15,
                "high": 0.30,
                "update_func": lambda v: model.assumptions.update({"tax_rate": v}),
            },
        }

        tornado_results = _tornado_analysis(model, variables, _ev_output)
        output_json({
            "symbol": args.symbol.upper(),
            "tornado": tornado_results,
            "base_enterprise_value": model.valuation_results["enterprise_value"],
        })
        return

    if args.sensitivity:
        wacc_base = model.wacc_components["wacc"]
        growth_base = model.assumptions["terminal_growth"]
        wacc_range = [round(wacc_base * (1 + p), 4) for p in [-0.3, -0.15, 0, 0.15, 0.3]]
        growth_range = [round(growth_base + p, 4) for p in [-0.015, -0.0075, 0, 0.0075, 0.015]]
        growth_range = [max(g, 0.005) for g in growth_range]

        grid = []
        for w in wacc_range:
            row = []
            for g in growth_range:
                model.wacc_components["wacc"] = w
                model.assumptions["terminal_growth"] = g
                model.project_cash_flows()
                ev = model.calculate_enterprise_value(args.terminal_method, args.exit_multiple)
                row.append(round(ev["enterprise_value"], 2))
            grid.append(row)

        # Restore base
        model.wacc_components["wacc"] = wacc_base
        model.assumptions["terminal_growth"] = growth_base

        output_json({
            "symbol": args.symbol.upper(),
            "sensitivity": {
                "wacc_range": wacc_range,
                "growth_range": growth_range,
                "grid": grid,
            },
            "base_enterprise_value": model.valuation_results["enterprise_value"],
        })
        return

    # Default: full DCF valuation
    model.calculate_enterprise_value(args.terminal_method, args.exit_multiple)

    shares = _fetch_financials(args.symbol).get("shares_outstanding", 100)
    net_debt = (model.wacc_components.get("debt_to_equity", 0.5) * 0.3
                * model.valuation_results["enterprise_value"])

    model.calculate_equity_value(net_debt=net_debt, shares_outstanding=shares)

    result = {
        "symbol": args.symbol.upper(),
        "company_name": args.symbol.upper(),
        "assumptions": {
            "projection_years": model.assumptions["projection_years"],
            "revenue_growth_avg": round(float(np.mean(model.assumptions["revenue_growth"])) * 100, 1),
            "ebitda_margin_avg": round(float(np.mean(model.assumptions["ebitda_margin"])) * 100, 1),
            "terminal_growth": round(model.assumptions["terminal_growth"] * 100, 1),
            "tax_rate": round(model.assumptions["tax_rate"] * 100, 1),
        },
        "wacc": {
            "wacc": round(model.wacc_components["wacc"] * 100, 2),
            "cost_of_equity": round(model.wacc_components["cost_of_equity"] * 100, 2),
            "beta": model.wacc_components["beta"],
        },
        "projections": {
            "years": model.projections["year"],
            "revenue": [round(v, 2) for v in model.projections["revenue"]],
            "ebitda": [round(v, 2) for v in model.projections["ebitda"]],
            "fcf": [round(v, 2) for v in model.projections["fcf"]],
        },
        "valuation": {
            "enterprise_value": round(model.valuation_results["enterprise_value"], 2),
            "pv_fcf": round(model.valuation_results["pv_fcf"], 2),
            "pv_terminal": round(model.valuation_results["pv_terminal"], 2),
            "terminal_pct": round(model.valuation_results["terminal_percent"], 1),
            "equity_value": round(model.valuation_results.get("equity_value", 0), 2),
            "value_per_share": round(model.valuation_results.get("value_per_share", 0), 2),
        },
        "note": "Values in millions USD unless otherwise noted. Live data from yfinance; assumptions use industry defaults.",
    }

    output_json(result)


if __name__ == "__main__":
    main()
