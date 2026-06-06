# CLAUDE.md — Data Pipeline Scenario

## Architecture
- **Language**: Python
- **Orchestration**: Prefect or Dagster
- **Data Storage**: Parquet files / PostgreSQL
- **Processing**: pandas or polars (Rust-based DataFrame library)
- **Optional**: PySpark for large-scale distributed processing
- **Monitoring**: Prefect Cloud / Dagster Cloud or self-hosted

## Commands
| Command | Description |
|---------|-------------|
| `uv run pipeline.py` | Run pipeline locally |
| `pytest` | Run tests |
| `uv run prefect deploy` | Deploy to Prefect |
| `ruff check` | Lint |

## Key Rules
- Idempotent pipeline steps (re-running a step produces the same result)
- Data validation at each stage (Pydantic or Great Expectations)
- Pipeline steps are independently testable
- Raw data is never modified (append-only, immutable)
- Schema evolution: handle new columns gracefully (backfill or default)

## Environment Variables
```
DATABASE_URL=postgres://user:pass@localhost:5432/db
PREFECT_API_URL=http://localhost:4200
DATA_DIR=./data
LOG_LEVEL=info
```
