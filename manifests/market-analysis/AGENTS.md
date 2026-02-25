# AGENTS.md

Instructions for AI agents (Cursor, Claude Code, etc.) working on market analysis projects.

## Repository Overview

Project for analyzing market data (stocks, funds) and generating investment insights.

## Core Flow (Market Analysis)

Follow these phases for financial analysis and strategy development:

1.  **Data Acquisition**: Use `scripts/fetch_data.py` to collect market data. Ensure `proxy_on` is enabled.
2.  **Indicator Calculation**: Implement and verify technical indicators (MACD, RSI, KDJ, etc.) in `indicators/`.
3.  **Strategy Implementation**: Develop trading/investment strategies in `strategies/`.
4.  **Backtesting**: Run strategies through the backtest engine in `backtest/`.
5.  **Risk Assessment**: Analyze drawdown, volatility, and Sharpe ratio.
6.  **Visualization**: Generate performance charts using Matplotlib (English labels only).
7.  **Review**: Call `code-reviewer` to verify financial logic and data handling.

## Subagent Dispatching

Actively suggest and launch subagents based on task complexity:

- **`explore`**: For analyzing market data structures and existing indicator logic.
- **`code-architect`**: For designing backtest engines or complex strategy frameworks.
- **`code-reviewer`**: For verifying financial formulas and data integrity checks.
- **`shell`**: For managing data files (CSV/Parquet) and environment setup.
- **`data-analyzer`**: (Custom role) For interpreting backtest results and suggesting optimizations.

## Data Standards

- **Integrity**: Always check for missing values or data gaps before analysis.
- **Format**: Prefer Parquet for large datasets, CSV for small/intermediate outputs.
- **Privacy**: Never commit API tokens or sensitive financial account info.

## Development Standards

- **Environment**: Use `uv` for package management.
- **Network**: Run `proxy_on` before any external data fetching.
- **Visualization**: All plots must use English labels.
- **Compliance**: Adhere to financial data usage regulations.

## Maintenance

- Keep `CLAUDE.md` updated with new indicator/strategy commands.
- Use `vibe-claude-md-audit` to ensure project context quality.
