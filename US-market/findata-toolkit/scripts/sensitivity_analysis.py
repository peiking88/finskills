#!/usr/bin/env python3
"""
Sensitivity Analysis Toolkit
=============================
Generic sensitivity analysis tools: tornado analysis, scenario analysis
(with probability weighting), and breakeven search. Designed to work with
any callable model (DCF, valuation, portfolio, etc.).

Usage:
    python sensitivity_analysis.py --scenario '{"base":{"revenue":1000,"margin":0.2},"bull":{"revenue":1200,"margin":0.25},"bear":{"revenue":800,"margin":0.15}}' --target 'revenue*margin*10' --weights '{"base":0.5,"bull":0.3,"bear":0.2}'
    python sensitivity_analysis.py --breakeven --variable margin --target-value 100 --range 0.05,0.50 --formula 'revenue*margin*10' --fixed '{"revenue":1000}'
    python sensitivity_analysis.py --example   # Run built-in demo
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common.utils import output_json, error_exit


# ---------------------------------------------------------------------------
# Tornado Analysis
# ---------------------------------------------------------------------------

def tornado_analysis(
    variables: dict[str, dict],
    output_func,
) -> list[dict]:
    """
    One-variable-at-a-time tornado analysis.

    Args:
        variables: {name: {"base": v, "low": v, "high": v, "set": callable}}
        output_func: Callable returning a numeric output.

    Returns:
        List of dicts sorted by impact (descending).
    """
    base_output = output_func()
    results = []

    for name, var in variables.items():
        var["set"](var["low"])
        low_out = output_func()

        var["set"](var["high"])
        high_out = output_func()

        var["set"](var["base"])  # restore

        impact = abs(high_out - low_out)
        results.append({
            "variable": name,
            "base_value": var["base"],
            "low_value": var["low"],
            "high_value": var["high"],
            "output_at_low": low_out,
            "output_at_high": high_out,
            "impact": impact,
            "impact_pct": (impact / abs(base_output) * 100) if base_output else 0,
        })

    results.sort(key=lambda x: x["impact"], reverse=True)
    return results


# ---------------------------------------------------------------------------
# Scenario Analysis
# ---------------------------------------------------------------------------

def scenario_analysis(
    scenarios: dict[str, dict[str, float]],
    output_func,
    weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """
    Probability-weighted scenario analysis.

    Args:
        scenarios: {name: {variable: value, ...}}
        output_func: Callable accepting keyword args, returning numeric output.
        weights: Optional {scenario_name: probability}. If omitted, equal weight.

    Returns:
        Dict with per-scenario results and probability-weighted expected value.
    """
    if weights is None:
        weights = {name: 1.0 / len(scenarios) for name in scenarios}

    results = []
    for name, variables in scenarios.items():
        output = output_func(**variables)
        prob = weights.get(name, 1.0 / len(scenarios))
        results.append({
            "scenario": name,
            "probability": prob,
            "output": output,
            "variables": variables,
        })

    expected_value = sum(r["output"] * r["probability"] for r in results)

    return {
        "scenarios": results,
        "expected_value": expected_value,
        "weights": weights,
    }


# ---------------------------------------------------------------------------
# Breakeven Analysis
# ---------------------------------------------------------------------------

def breakeven_search(
    output_func,
    target_value: float,
    var_range: tuple[float, float],
    tolerance: float = 0.01,
    max_iter: int = 100,
) -> dict[str, Any]:
    """
    Binary search for the variable value where output equals target.

    Args:
        output_func: Callable accepting a single float, returning numeric output.
        target_value: Output value to find.
        var_range: (min, max) search range.
        tolerance: Convergence tolerance on the variable.
        max_iter: Safety limit.

    Returns:
        Dict with breakeven value and search details.
    """
    low, high = var_range

    # Verify the target is within range
    out_low = output_func(low)
    out_high = output_func(high)

    if (out_low - target_value) * (out_high - target_value) > 0:
        return {
            "converged": False,
            "message": "Target not bracketed by range — output at low and high have same sign relative to target",
            "output_at_low": out_low,
            "output_at_high": out_high,
            "target": target_value,
        }

    for _ in range(max_iter):
        mid = (low + high) / 2
        out_mid = output_func(mid)

        if abs(out_mid - target_value) < tolerance:
            return {
                "converged": True,
                "breakeven_value": round(mid, 6),
                "output_at_breakeven": round(out_mid, 6),
                "iterations": _ + 1,
                "target": target_value,
            }

        if (out_mid - target_value) * (out_low - target_value) < 0:
            high = mid
        else:
            low = mid

    return {
        "converged": False,
        "message": "Max iterations reached",
        "approximate_value": round((low + high) / 2, 6),
        "target": target_value,
    }


# ---------------------------------------------------------------------------
# Formula evaluator for CLI usage
# ---------------------------------------------------------------------------

def _eval_formula(formula: str, **kwargs) -> float:
    """Evaluate a simple arithmetic formula with variable substitution."""
    allowed_names = {k: v for k, v in kwargs.items()}
    allowed_names.update({"abs": abs, "min": min, "max": max, "round": round})
    return float(eval(formula, {"__builtins__": {}}, allowed_names))  # noqa: S307


def _make_func(formula: str, fixed: dict, variable_name: str | None = None):
    """Create a callable from a formula string and fixed variables."""
    def func(**kwargs):
        params = {**fixed, **kwargs}
        return _eval_formula(formula, **params)

    def single_var_func(value):
        params = {**fixed, variable_name: value}
        return _eval_formula(formula, **params)

    return single_var_func if variable_name else func


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Sensitivity Analysis Toolkit (tornado, scenario, breakeven)"
    )
    parser.add_argument("--scenario", metavar="JSON",
                        help="Scenario definitions as JSON string")
    parser.add_argument("--target", metavar="FORMULA",
                        help="Output formula (e.g., 'revenue*margin*10')")
    parser.add_argument("--weights", metavar="JSON",
                        help="Scenario probability weights as JSON string")
    parser.add_argument("--breakeven", action="store_true",
                        help="Run breakeven analysis")
    parser.add_argument("--variable", help="Variable to search for breakeven")
    parser.add_argument("--target-value", type=float, help="Target output for breakeven")
    parser.add_argument("--range", metavar="MIN,MAX",
                        help="Search range for breakeven (comma-separated)")
    parser.add_argument("--fixed", metavar="JSON",
                        help="Fixed variable values as JSON string")
    parser.add_argument("--tolerance", type=float, default=0.01,
                        help="Convergence tolerance (default: 0.01)")
    parser.add_argument("--example", action="store_true",
                        help="Run built-in demo with sample data")
    args = parser.parse_args()

    if args.example:
        _run_example()
        return

    if args.target is None:
        error_exit("--target formula is required (e.g., --target 'revenue*margin*10')")

    fixed = json.loads(args.fixed) if args.fixed else {}

    # --- Scenario analysis ---
    if args.scenario:
        scenarios = json.loads(args.scenario)
        weights = json.loads(args.weights) if args.weights else None
        func = _make_func(args.target, fixed)

        result = scenario_analysis(scenarios, func, weights)
        output_json({"analysis": "scenario", **result})
        return

    # --- Breakeven analysis ---
    if args.breakeven:
        if not args.variable or not args.target_value or not args.range:
            error_exit("--breakeven requires --variable, --target-value, and --range")

        range_vals = [float(x) for x in args.range.split(",")]
        func = _make_func(args.target, fixed, args.variable)

        result = breakeven_search(func, args.target_value, tuple(range_vals), args.tolerance)
        output_json({"analysis": "breakeven", "variable": args.variable, **result})
        return

    error_exit("Specify --scenario, --breakeven, or --example")


def _run_example():
    """Demo scenario and breakeven analysis with a simple model."""
    formula = "revenue * margin * multiple"

    # Scenario analysis
    scenarios = {
        "bull": {"revenue": 1200, "margin": 0.25, "multiple": 12},
        "base": {"revenue": 1000, "margin": 0.20, "multiple": 10},
        "bear": {"revenue": 800, "margin": 0.15, "multiple": 8},
    }
    weights = {"bull": 0.3, "base": 0.5, "bear": 0.2}
    func = _make_func(formula, {})

    scenario_result = scenario_analysis(scenarios, func, weights)

    # Breakeven: what margin gives a target output of 2000?
    be_func = _make_func(formula, {"revenue": 1000, "multiple": 10}, "margin")
    breakeven_result = breakeven_search(be_func, 2000.0, (0.05, 0.50))

    output_json({
        "demo": True,
        "model": f"output = {formula}",
        "scenario_analysis": scenario_result,
        "breakeven_analysis": breakeven_result,
    })


if __name__ == "__main__":
    main()
