# 提交摘要

## 版本
FinSkills — 金融分析技能集合，初始提交。

## 内容概览

- **US-market (26 个技能)**：覆盖美股市场的投资分析技能，包括价值筛选、内幕交易分析、情绪偏差识别、股息贵族评估、科技股估值、行业轮动、小盘成长股发现、组合优化、组合健康诊断、适当性报告、财务报表分析、事件驱动、因子筛选、ESG、DCF估值、SEPA策略、SaaS估值、税务优化、合规基础，以及社交媒体阅读器和数据工具包。
- **China-market (15 个技能)**：覆盖A股市场的投资分析技能，对应美股的核心分析能力，并针对A股市场特征（CAS会计准则、涨跌停板、行业轮动、政策驱动等）做了全面改写。
- **external (3 个流水线技能)**：金融内容生成流水线（每日财经 → 核心分析 → 爆款文章）。
- **数据工具包**：US-market/findata-toolkit + China-market/findata-toolkit-cn，提供可执行的 Python 脚本，支持免费数据源（yfinance、SEC EDGAR、FRED、AKShare）。

## 目录结构
```
finskills/
├── US-market/          # 26 个技能（英文）
├── China-market/       # 15 个技能（中文）
├── external/           # 3 个内容流水线技能
├── README.md / README.zh.md
├── CLAUDE.md
└── LICENSE
```

## 本次提交
初始化仓库，导入全部 44 个技能（41 个金融分析 + 3 个外部流水线）及相关配置文件。
