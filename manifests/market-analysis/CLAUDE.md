# CLAUDE.md

Market analysis project for stocks, funds, and financial data.

## Commands

| Command | Description |
|---------|-------------|
| `uv run fetch_data.py` | Fetch market data (requires `proxy_on`) |
| `uv run analyze.py` | Run technical analysis and indicators |
| `uv run backtest.py` | Run strategy backtesting |
| `uv run plot_trends.py` | Generate trend visualizations (English labels) |
| `pytest tests/` | Run unit tests for indicators/strategies |

## Architecture

```
<root>/
  data/       # Raw and processed market data (CSV/Parquet)
  indicators/ # Technical indicators (MACD, RSI, etc.)
  strategies/ # Trading/Investment strategies
  backtest/   # Backtesting engine and results
  scripts/    # Data fetching and utility scripts
  tests/      # Unit and integration tests
```

## Key Files

- `pyproject.toml` - Project configuration (uv)
- `indicators/core.py` - Core indicator implementations
- `strategies/base.py` - Base strategy class
- `backtest/engine.py` - Backtesting logic

## Code Style

- Use `pandas` and `numpy` for efficient data manipulation.
- All financial calculations must include unit tests.
- Use type hints for dataframes where possible (e.g., `pd.DataFrame`).
- Follow PEP 8 for Python code.

## Environment

Required:
- `TUSHARE_TOKEN` - Token for Tushare data API (if used)
- `AKSHARE_PROXY` - Proxy settings for AkShare (if needed)

## Gotchas

- **Data Compliance**: Ensure all data usage complies with provider terms.
- **Risk Warning**: AI-generated analysis is for reference only, not financial advice.
- **Network**: Run `proxy_on` before fetching external market data.
- **Visualization**: Matplotlib plots MUST use English labels for compatibility.

## Workflow

- **Data First**: Always verify data integrity before running analysis.
- **Backtest**: Every strategy must be backtested against historical data.
- **Risk Check**: Run risk assessment scripts before finalizing any report.
