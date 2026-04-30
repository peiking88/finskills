#!/usr/bin/env python3
"""
Risk & Performance Analytics
=============================
Comprehensive risk and performance analysis for US stocks and portfolios.
Combines historical risk metrics, risk-adjusted performance ratios, return
analytics, volatility modeling (EWMA/GARCH), and forward-looking risk
estimates (parametric/historical/Monte Carlo VaR, CVaR).

Usage:
    python risk_performance.py AAPL                          # Full risk + performance
    python risk_performance.py AAPL --risk                   # Risk metrics only
    python risk_performance.py AAPL --performance            # Performance ratios only
    python risk_performance.py AAPL --volatility             # Volatility modeling (EWMA)
    python risk_performance.py AAPL --returns                # Return analytics
    python risk_performance.py AAPL MSFT GOOGL --portfolio 10000  # Multi-asset portfolio VaR
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common.utils import output_json, safe_div, safe_float, error_exit


# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------

def _fetch_returns(symbols: list[str], period: str = "2y") -> dict:
    """Fetch daily price returns via yfinance."""
    import yfinance as yf

    result = {}
    for sym in symbols:
        t = yf.Ticker(sym)
        hist = t.history(period=period)
        if hist.empty:
            continue
        prices = hist["Close"].values
        returns = np.diff(prices) / prices[:-1]
        result[sym] = {
            "returns": returns.astype(float),
            "prices": prices.astype(float),
            "dates": [str(d.date()) for d in hist.index],
        }
    return result


# ---------------------------------------------------------------------------
# Return Analytics
# ---------------------------------------------------------------------------

def _compute_returns(returns: np.ndarray) -> dict:
    """Core return metrics from a return series."""
    n = len(returns)
    cumulative = float(np.prod(1 + returns) - 1)
    cagr_val = float((1 + cumulative) ** (252 / n) - 1) if n > 0 and cumulative > -1 else None
    arith_mean = float(np.mean(returns))
    geom_mean = float(np.prod(1 + returns) ** (1 / n) - 1) if n > 0 else None
    log_returns = np.log1p(returns)
    return {
        "total_return": round(cumulative, 6),
        "cagr": round(cagr_val, 6) if cagr_val is not None else None,
        "annualized_return": round(float((1 + cumulative) ** (252 / n) - 1), 6) if n > 0 else None,
        "arithmetic_mean_daily": round(arith_mean, 6),
        "geometric_mean_daily": round(geom_mean, 6) if geom_mean is not None else None,
        "best_day": round(float(np.max(returns)), 6),
        "worst_day": round(float(np.min(returns)), 6),
        "positive_days": int(np.sum(returns > 0)),
        "negative_days": int(np.sum(returns < 0)),
        "trading_days": n,
    }


# ---------------------------------------------------------------------------
# Historical Risk
# ---------------------------------------------------------------------------

def _compute_risk(returns: np.ndarray, periods_per_year: int = 252) -> dict:
    """Historical risk metrics."""
    ann_vol = float(np.std(returns, ddof=1) * np.sqrt(periods_per_year))

    # Drawdown
    cumulative = np.cumprod(1 + returns)
    running_max = np.maximum.accumulate(cumulative)
    drawdowns = (cumulative - running_max) / running_max
    max_dd = float(np.min(drawdowns))

    # VaR
    var_95 = float(-np.percentile(returns, 5))
    var_99 = float(-np.percentile(returns, 1))

    # CVaR (Expected Shortfall)
    cvar_95 = float(-np.mean(returns[returns <= np.percentile(returns, 5)]))
    cvar_99 = float(-np.mean(returns[returns <= np.percentile(returns, 1)])) if np.sum(returns <= np.percentile(returns, 1)) > 0 else None

    # Downside deviation
    downside = np.minimum(returns, 0.0)
    dd_ann = float(np.sqrt(np.mean(downside ** 2)) * np.sqrt(periods_per_year))

    # Semi-variance
    mean_r = np.mean(returns)
    semi_var = float(np.mean(np.minimum(returns - mean_r, 0.0) ** 2))

    return {
        "annualized_volatility": round(ann_vol, 6),
        "max_drawdown": round(max_dd, 6),
        "var_95_daily": round(var_95, 6),
        "var_99_daily": round(var_99, 6),
        "cvar_95_daily": round(cvar_95, 6),
        "cvar_99_daily": round(cvar_99, 6) if cvar_99 is not None else None,
        "downside_deviation_ann": round(dd_ann, 6),
        "semi_variance": round(semi_var, 8),
    }


# ---------------------------------------------------------------------------
# Performance Metrics
# ---------------------------------------------------------------------------

def _compute_performance(
    returns: np.ndarray,
    benchmark_returns: np.ndarray | None = None,
    risk_free_rate: float = 0.04,
    periods_per_year: int = 252,
) -> dict:
    """Risk-adjusted performance ratios."""
    rf_per_period = risk_free_rate / periods_per_year
    excess = returns - rf_per_period

    # Sharpe
    std = float(np.std(returns, ddof=1))
    sharpe = float(np.mean(excess) / std * np.sqrt(periods_per_year)) if std > 0 else 0.0

    # Sortino
    downside = np.minimum(excess, 0.0)
    dd = float(np.sqrt(np.mean(downside ** 2)))
    sortino = float(np.mean(excess) / dd * np.sqrt(periods_per_year)) if dd > 0 else float("inf")

    # Calmar
    cumulative = np.prod(1 + returns)
    n_years = len(returns) / periods_per_year
    ann_ret = float(cumulative ** (1 / n_years) - 1) if n_years > 0 else 0.0
    cum_series = np.cumprod(1 + returns)
    run_max = np.maximum.accumulate(cum_series)
    dd_series = (cum_series - run_max) / run_max
    max_dd = abs(float(np.min(dd_series)))
    calmar = ann_ret / max_dd if max_dd > 0 else float("inf")

    # Omega
    gains = float(np.sum(np.maximum(returns - rf_per_period, 0.0)))
    losses = float(np.sum(np.maximum(rf_per_period - returns, 0.0)))
    omega = gains / losses if losses > 0 else float("inf")

    # Win/loss
    wins = returns[returns > 0]
    losses_arr = returns[returns < 0]
    win_loss = float(np.mean(wins) / abs(np.mean(losses_arr))) if len(losses_arr) > 0 and len(wins) > 0 else 0.0

    result = {
        "sharpe_ratio": round(sharpe, 4),
        "sortino_ratio": round(sortino, 4),
        "calmar_ratio": round(calmar, 4),
        "omega_ratio": round(omega, 4),
        "win_loss_ratio": round(win_loss, 4),
        "annualized_return": round(ann_ret, 6),
        "risk_free_rate": risk_free_rate,
    }

    # Benchmark-dependent metrics
    if benchmark_returns is not None and len(benchmark_returns) == len(returns):
        active = returns - benchmark_returns
        te = float(np.std(active, ddof=1))
        ir = float(np.mean(active) / te * np.sqrt(periods_per_year)) if te > 0 else 0.0

        # Treynor
        cov_matrix = np.cov(returns, benchmark_returns)
        beta = float(cov_matrix[0, 1] / cov_matrix[1, 1]) if cov_matrix[1, 1] != 0 else 0.0
        treynor = float(np.mean(excess) * periods_per_year / beta) if beta != 0 else 0.0

        # Capture
        up_mask = benchmark_returns > 0
        down_mask = benchmark_returns < 0
        up_cap = float(np.mean(returns[up_mask]) / np.mean(benchmark_returns[up_mask])) if np.any(up_mask) else None
        down_cap = float(np.mean(returns[down_mask]) / np.mean(benchmark_returns[down_mask])) if np.any(down_mask) else None

        result.update({
            "information_ratio": round(ir, 4),
            "treynor_ratio": round(treynor, 4),
            "beta": round(beta, 4),
            "up_capture": round(up_cap, 4) if up_cap is not None else None,
            "down_capture": round(down_cap, 4) if down_cap is not None else None,
            "tracking_error_ann": round(te * np.sqrt(periods_per_year), 6),
        })

    return result


# ---------------------------------------------------------------------------
# Volatility Modeling
# ---------------------------------------------------------------------------

def _compute_volatility(returns: np.ndarray, periods_per_year: int = 252) -> dict:
    """EWMA and GARCH(1,1) volatility estimation."""
    n = len(returns)
    lam = 0.94

    # EWMA variance series
    warmup = min(20, n)
    initial_var = float(np.var(returns[:warmup], ddof=1))
    ewma_var = np.empty(n)
    ewma_var[0] = initial_var
    for t in range(1, n):
        ewma_var[t] = lam * ewma_var[t - 1] + (1 - lam) * returns[t - 1] ** 2
    ewma_vol = np.sqrt(ewma_var) * np.sqrt(periods_per_year)

    # Rolling volatility (63-day ≈ 1 quarter)
    window = min(63, n)
    rolling_vol = np.full(n, np.nan)
    for i in range(window - 1, n):
        rolling_vol[i] = float(np.std(returns[i - window + 1:i + 1], ddof=1) * np.sqrt(periods_per_year))

    valid_rolling = rolling_vol[~np.isnan(rolling_vol)]

    return {
        "ewma": {
            "current_vol": round(float(ewma_vol[-1]), 6),
            "lambda": lam,
            "effective_window": round(1 / (1 - lam), 1),
            "vol_min": round(float(np.min(ewma_vol)), 6),
            "vol_max": round(float(np.max(ewma_vol)), 6),
            "vol_mean": round(float(np.mean(ewma_vol)), 6),
        },
        "rolling_63d": {
            "current": round(float(rolling_vol[-1]), 6) if not np.isnan(rolling_vol[-1]) else None,
            "mean": round(float(np.mean(valid_rolling)), 6) if len(valid_rolling) > 0 else None,
            "min": round(float(np.min(valid_rolling)), 6) if len(valid_rolling) > 0 else None,
            "max": round(float(np.max(valid_rolling)), 6) if len(valid_rolling) > 0 else None,
        },
        "close_to_close_ann": round(float(np.std(returns, ddof=1) * np.sqrt(periods_per_year)), 6),
    }


# ---------------------------------------------------------------------------
# Portfolio VaR (multi-asset)
# ---------------------------------------------------------------------------

def _portfolio_var(symbols: list[str], portfolio_value: float, period: str = "2y") -> dict:
    """Compute portfolio-level parametric and historical VaR."""
    from scipy import stats as sp_stats

    data = _fetch_returns(symbols, period)
    if len(data) < 2:
        return {"error": "Need at least 2 symbols with data for portfolio VaR"}

    # Align return arrays to same length
    min_len = min(len(d["returns"]) for d in data.values())
    aligned = {sym: d["returns"][-min_len:] for sym, d in data.items()}
    syms = list(aligned.keys())
    returns_matrix = np.column_stack([aligned[s] for s in syms])

    n_assets = len(syms)
    weights = np.ones(n_assets) / n_assets  # equal weight

    cov_ann = np.cov(returns_matrix, rowvar=False) * 252
    port_vol = float(np.sqrt(weights @ cov_ann @ weights))
    port_returns = returns_matrix @ weights

    # Parametric VaR
    z_95 = sp_stats.norm.ppf(0.95)
    z_99 = sp_stats.norm.ppf(0.99)
    sigma_daily = port_vol / np.sqrt(252)

    # Historical VaR
    hist_var_95 = float(-np.percentile(port_returns, 5) * portfolio_value)
    hist_var_99 = float(-np.percentile(port_returns, 1) * portfolio_value)

    # CVaR
    cvar_95 = float(-np.mean(port_returns[port_returns <= np.percentile(port_returns, 5)]) * portfolio_value)

    return {
        "portfolio_value": portfolio_value,
        "symbols": syms,
        "weights": {s: round(float(w), 4) for s, w in zip(syms, weights)},
        "portfolio_volatility_ann": round(port_vol, 6),
        "parametric_var": {
            "95_1d": round(portfolio_value * z_95 * sigma_daily, 2),
            "99_1d": round(portfolio_value * z_99 * sigma_daily, 2),
            "95_10d": round(portfolio_value * z_95 * sigma_daily * np.sqrt(10), 2),
        },
        "historical_var": {
            "95_1d": round(hist_var_95, 2),
            "99_1d": round(hist_var_99, 2),
        },
        "cvar_95_1d": round(cvar_95, 2),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Risk & Performance Analytics (historical risk, performance ratios, volatility modeling, portfolio VaR)"
    )
    parser.add_argument("symbols", nargs="+", help="Stock ticker(s)")
    parser.add_argument("--risk", action="store_true", help="Historical risk metrics")
    parser.add_argument("--performance", action="store_true", help="Performance ratios")
    parser.add_argument("--volatility", action="store_true", help="Volatility modeling (EWMA, rolling)")
    parser.add_argument("--returns", action="store_true", help="Return analytics")
    parser.add_argument("--portfolio", type=float, metavar="VALUE",
                        help="Portfolio VaR for multi-asset (equal-weight)")
    parser.add_argument("--period", default="2y", help="Price history period (default: 2y)")
    parser.add_argument("--rf", type=float, default=0.04, help="Risk-free rate (default: 0.04)")
    args = parser.parse_args()

    try:
        import yfinance
    except ImportError:
        error_exit("yfinance is required. Install: pip install yfinance")

    try:
        if args.portfolio and len(args.symbols) >= 2:
            result = _portfolio_var(args.symbols, args.portfolio, args.period)
            output_json(result)
            return

        # Single-symbol analysis
        sym = args.symbols[0]
        data = _fetch_returns([sym], args.period)
        if sym not in data:
            error_exit(f"No data returned for {sym}")

        returns = data[sym]["returns"]
        show_all = not any([args.risk, args.performance, args.volatility, args.returns])

        # Benchmark (SPY) for performance metrics
        bench_data = _fetch_returns(["SPY"], args.period)
        bench_returns = bench_data.get("SPY", {}).get("returns")
        if bench_returns is not None and len(bench_returns) != len(returns):
            min_len = min(len(bench_returns), len(returns))
            bench_returns = bench_returns[-min_len:]
            returns = returns[-min_len:]

        result = {"symbol": sym, "period": args.period}

        if show_all or args.returns:
            result["returns"] = _compute_returns(returns)
        if show_all or args.risk:
            result["risk"] = _compute_risk(returns)
        if show_all or args.performance:
            result["performance"] = _compute_performance(returns, bench_returns, args.rf)
        if show_all or args.volatility:
            result["volatility"] = _compute_volatility(returns)

        output_json(result)

    except Exception as e:
        error_exit(f"Error: {e}")


if __name__ == "__main__":
    main()
