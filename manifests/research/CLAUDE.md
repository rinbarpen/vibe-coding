# CLAUDE.md

## Architecture
- Computation: Python/C++/Rust
- Experiment Tracking: MLflow/WandB
- Data: Immutable datasets

## Research Commands
| Command | Description |
|---------|-------------|
| `uv run experiment.py` | Run research experiment |
| `vibe-check research` | Verify data consistency |
| `vibe-track-exp` | Log experiment metadata |

## Experiment Tracking
- Record Git Hash and parameters for every run.
- Results stored with metadata.
