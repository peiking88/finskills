---
name: us-findata-toolkit
description: Financial data toolkit for US market analysis. Provides scripts to fetch real-time stock data (yfinance), SEC filings and insider trades (EDGAR), financial statement calculators (DuPont, Z-Score, M-Score, F-Score), portfolio analytics (VaR, stress testing, health scoring), multi-factor screening, and macro indicators (FRED). Use when you need live US market data to ground investment analysis. Also trigger when someone says "pull up AAPL's financials", "get me the latest stock data", "what are the macro numbers saying", "run a DCF on this stock", "check insider trades", "show me the yield curve", "fetch earnings data", "get portfolio risk metrics", or "what does the balance sheet look like". All data sources are free — no API keys required.
license: Apache-2.0
---

# FinData Toolkit — US Market

A self-contained data toolkit providing live financial data and quantitative calculations for US market analysis. All data sources are **free** and require **no API keys**.

## Setup

Install dependencies (one-time):

```bash
pip install -r requirements.txt
```

## Available Tools

All scripts are in the `scripts/` directory. Run from the skill root directory.

### 1. Stock Data (`scripts/stock_data.py`)

Fetch stock fundamentals, price history, and financial metrics via yfinance.

| Command | Purpose |
|---------|---------|
| `python scripts/stock_data.py AAPL` | Basic company info |
| `python scripts/stock_data.py AAPL --metrics` | Full financial metrics (valuation, profitability, leverage, growth, analyst consensus) |
| `python scripts/stock_data.py AAPL --history --period 1y` | OHLCV price history |
| `python scripts/stock_data.py AAPL --financials` | Income statement, balance sheet, cash flow |
| `python scripts/stock_data.py AAPL MSFT GOOGL --screen` | Screen stocks against value filters |
| `python scripts/stock_data.py AAPL --options` | Options chain (calls & puts) |
| `python scripts/stock_data.py AAPL --options --expiration 2026-06-20` | Options for specific expiration |
| `python scripts/stock_data.py AAPL --earnings` | Earnings history and estimates |
| `python scripts/stock_data.py AAPL --analysts` | Analyst recommendations and price targets |
| `python scripts/stock_data.py AAPL --dividends` | Dividend history and splits |
| `python scripts/stock_data.py AAPL --news` | Recent news articles |

### 2. SEC EDGAR (`scripts/sec_edgar.py`)

Fetch insider trading data (Form 4), company filings, and CIK lookups.

| Command | Purpose |
|---------|---------|
| `python scripts/sec_edgar.py insider AAPL` | Recent insider trades |
| `python scripts/sec_edgar.py insider AAPL --days 90` | Insider trades in last 90 days |
| `python scripts/sec_edgar.py filings AAPL --form-type 10-K` | Recent 10-K filings |
| `python scripts/sec_edgar.py cik AAPL` | Look up CIK number |

### 3. Financial Calculators (`scripts/financial_calc.py`)

DuPont decomposition, Altman Z-Score, Beneish M-Score, Piotroski F-Score, earnings quality, working capital analysis, and industry benchmark comparison.

| Command | Purpose |
|---------|---------|
| `python scripts/financial_calc.py AAPL --all` | All calculations |
| `python scripts/financial_calc.py AAPL --dupont` | 5-factor DuPont decomposition |
| `python scripts/financial_calc.py AAPL --zscore` | Altman Z-Score (bankruptcy risk) |
| `python scripts/financial_calc.py AAPL --mscore` | Beneish M-Score (manipulation detection) |
| `python scripts/financial_calc.py AAPL --fscore` | Piotroski F-Score (financial strength) |
| `python scripts/financial_calc.py AAPL --quality` | Earnings quality assessment |
| `python scripts/financial_calc.py AAPL --working-capital` | Working capital & CCC analysis |
| `python scripts/financial_calc.py AAPL --benchmarks` | Industry benchmark comparison (general) |
| `python scripts/financial_calc.py AAPL --benchmarks --industry technology` | Benchmark against specific industry (technology, retail, financial, manufacturing, healthcare) |

### 4. Portfolio Analytics (`scripts/portfolio_analytics.py`)

Portfolio risk analysis: concentration, correlation clusters, VaR/CVaR, stress testing, and health scoring.

| Command | Purpose |
|---------|---------|
| `python scripts/portfolio_analytics.py --holdings "AAPL:30,MSFT:25,GOOGL:20,AMZN:15,META:10"` | Full health score (0–100) |
| `... --concentration` | Concentration analysis (HHI, sector) |
| `... --correlation` | Correlation clusters & EDR |
| `... --risk` | VaR/CVaR, Sharpe, Sortino, beta |
| `... --stress` | Historical stress testing (5 scenarios) |

### 5. Factor Screener (`scripts/factor_screener.py`)

Multi-factor stock scoring: value, momentum, quality, low volatility, size, growth.

| Command | Purpose |
|---------|---------|
| `python scripts/factor_screener.py --universe "AAPL,MSFT,GOOGL,AMZN" --top 5` | Screen custom universe |
| `python scripts/factor_screener.py --sp500-sample --top 10` | Screen S&P 500 sample |
| `... --factors value,quality` | Use specific factors only |

### 6. Macro Data (`scripts/macro_data.py`)

US macroeconomic indicators from FRED.

| Command | Purpose |
|---------|---------|
| `python scripts/macro_data.py --dashboard` | Full macro dashboard |
| `python scripts/macro_data.py --rates` | Interest rates & yield curve |
| `python scripts/macro_data.py --inflation` | CPI, PCE, breakevens |
| `python scripts/macro_data.py --gdp` | GDP & leading indicators |
| `python scripts/macro_data.py --employment` | Unemployment, payrolls, JOLTS |
| `python scripts/macro_data.py --cycle` | Business cycle phase assessment |

### 7. Sensitivity Analysis (`scripts/sensitivity_analysis.py`)

Generic sensitivity analysis toolkit: scenario analysis (probability-weighted), breakeven search, and tornado analysis. Works with any callable model.

| Command | Purpose |
|---------|---------|
| `python scripts/sensitivity_analysis.py --example` | Run built-in demo |
| `python scripts/sensitivity_analysis.py --scenario '{"bull":{"revenue":1200,"margin":0.25},"base":{"revenue":1000,"margin":0.20}}' --target 'revenue*margin*10'` | Scenario analysis |
| `python scripts/sensitivity_analysis.py --scenario '...' --target '...' --weights '{"bull":0.3,"base":0.7}'` | Probability-weighted scenario analysis |
| `python scripts/sensitivity_analysis.py --breakeven --variable margin --target-value 2000 --range 0.05,0.50 --formula 'revenue*margin*10' --fixed '{"revenue":1000}'` | Breakeven search |

### 8. Risk & Performance Analytics (`scripts/risk_performance.py`)

Comprehensive risk and performance analysis: historical risk metrics (VaR, CVaR, drawdown), risk-adjusted ratios (Sharpe, Sortino, Calmar, Treynor, Omega), return analytics (CAGR, TWR), volatility modeling (EWMA, rolling), and multi-asset portfolio VaR.

| Command | Purpose |
|---------|---------|
| `python scripts/risk_performance.py AAPL` | Full risk + performance analysis |
| `python scripts/risk_performance.py AAPL --risk` | Historical risk metrics (VaR, drawdown, downside deviation) |
| `python scripts/risk_performance.py AAPL --performance` | Risk-adjusted ratios (Sharpe, Sortino, Calmar, Treynor, Omega, capture) |
| `python scripts/risk_performance.py AAPL --volatility` | EWMA and rolling volatility |
| `python scripts/risk_performance.py AAPL --returns` | Return analytics (CAGR, best/worst day) |
| `python scripts/risk_performance.py AAPL MSFT GOOGL --portfolio 100000` | Multi-asset portfolio VaR (parametric, historical, CVaR) |

### 9. DCF Valuation (`scripts/dcf_model.py`)

Discounted Cash Flow valuation with enterprise/equity value, WACC calculation, tornado and sensitivity analysis.

| Command | Purpose |
|---------|---------|
| `python scripts/dcf_model.py AAPL` | Full DCF valuation (EV, equity, per-share) |
| `python scripts/dcf_model.py AAPL --wacc-only` | WACC components only |
| `python scripts/dcf_model.py AAPL --sensitivity` | WACC vs growth sensitivity grid |
| `python scripts/dcf_model.py AAPL --tornado` | Tornado analysis of key drivers |
| `python scripts/dcf_model.py AAPL --terminal-method multiple --exit-multiple 12` | Exit multiple method |

## Data Sources

| Source | Data | API Key |
|--------|------|---------|
| Yahoo Finance (yfinance) | Stock quotes, financials, history | Not required |
| SEC EDGAR | Filings, insider trades (Form 4) | Not required |
| FRED | Macro indicators | Not required |

## Output Format

All scripts output **JSON to stdout** for easy parsing. Errors go to stderr.

## Configuration

Optional: Edit `config/data_sources.yaml` to customize rate limits or add API keys for premium data sources.
