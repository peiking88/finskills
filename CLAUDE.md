# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FinSkills is a collection of 30 Claude Skills (markdown-based prompt/workflow definitions) for financial investment analysis — 15 for US markets, 15 for China A-share markets. Each skill guides Claude through a structured analysis workflow. This is **not a traditional application** — there is no build system, test framework, or package manager at the top level.

## Repository Structure

```
US-market/                          # US market skills (English)
├── <skill-name>/                    # Analysis skill: SKILL.md + references/
│   ├── SKILL.md                     # YAML frontmatter (name, description, license) + workflow steps
│   └── references/
│       ├── <xxx>-methodology.md     # Formulas, thresholds, benchmarks
│       └── output-template.md      # Structured report format
├── findata-toolkit/                 # Data toolkit with live Python scripts
│   ├── SKILL.md                     # Toolkit skill definition + CLI usage reference
│   ├── requirements.txt             # yfinance, pandas-datareader, pandas, numpy, scipy, requests, tabulate
│   ├── config/data_sources.yaml     # Data source configuration
│   └── scripts/
│       ├── common/                  # config.py, utils.py (shared across all scripts)
│       ├── stock_data.py            # yfinance: quotes, metrics, screening
│       ├── sec_edgar.py             # SEC EDGAR: insider trades, filings, CIK lookup
│       ├── financial_calc.py        # DuPont, Z/M/F-Score calculators
│       ├── portfolio_analytics.py   # VaR, stress testing, health scoring
│       ├── factor_screener.py       # Multi-factor scoring engine
│       └── macro_data.py            # FRED macro indicators
China-market/                        # A-share market skills (Chinese)
├── <skill-name>/                    # Same SKILL.md + references/ structure as US
├── findata-toolkit-cn/              # Note: folder name has -cn suffix
│   ├── scripts/
│   │   ├── common/                  # Same config.py, utils.py as US
│   │   ├── stock_data.py            # AKShare: quotes, metrics, screening
│   │   └── macro_data.py            # LPR, PMI, CPI, M2 (via AKShare)
```

## Key Architecture Rules

### Skill naming consistency

The skill manifest `name` in SKILL.md **must match the directory name**. The China toolkit directory is `findata-toolkit-cn` but its manifest name was changed to `findata-toolkit-cn` in commit `5b75535`. Cross-references between skills use the manifest name — when renaming a directory, update both the SKILL.md frontmatter AND all cross-referencing SKILL.md files.

### Skill file structure

Each analysis SKILL.md follows this pattern:
1. YAML frontmatter with `name`, `description`, `license` fields
2. Role assignment ("Act as a professional equity research analyst...")
3. Step-by-step workflow with references to `references/*.md` files
4. Output compilation instructions

The data toolkit SKILL.md adds CLI usage examples showing exact commands for each script.

### Data toolkit Python scripts

- All scripts are self-contained CLI tools. Run from the toolkit root directory.
- Shared utilities live in `scripts/common/`:
  - `config.py` — Loads YAML config, resolves `${ENV_VAR}` references, provides fallback defaults
  - `utils.py` — JSON output with date/numpy/pandas handling, rate-limit decorator, safe arithmetic (`safe_div`, `safe_float`, `pct`)
- Scripts output JSON to stdout, errors to stderr
- Data sources are all free, no API keys required (optional Alpha Vantage key supported via env var)

### Running Python scripts

```bash
# US market
cd US-market/findata-toolkit
pip install -r requirements.txt
python scripts/stock_data.py AAPL --metrics

# China market
cd China-market/findata-toolkit-cn
pip install -r requirements.txt
python scripts/stock_data.py 600519 --metrics
```

## Development Notes

- Conventional commits are used (`fix:`, `refactor:`, `chore:`)
- Single-branch workflow on `main`
- `.cursor/` is gitignored — used for local Cursor IDE testing copies of skills
