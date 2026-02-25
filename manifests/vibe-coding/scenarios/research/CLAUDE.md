# CLAUDE.md

## Architecture
- **Environment**: PyTorch / TensorFlow / JAX
- **Tracking**: W&B / MLflow / TensorBoard
- **Writing**: LaTeX / Overleaf / Markdown

## Research Commands
| Command | Description |
|---------|-------------|
| `uv run python train.py --config default.yaml` | Start training experiment |
| `uv run python plot_results.py` | Generate English plots for paper |
| `vibe-check research` | Verify experiment reproducibility & plot labels |
| `bibtex paper.aux` | Process bibliography |

## Development Standards
- **Reproducibility**: Always fix random seeds.
- **Visualization**: All plots must use English font and labels.
- **Data**: Large files must be tracked via DVC or Git LFS.

## Key Files
- `experiments/` - Experiment configurations and results
- `data/` - Raw and processed data (use DVC)
- `notebooks/` - Exploratory data analysis (EDA)
- `paper/` - LaTeX source and figures
- `scripts/` - Data preprocessing and plotting scripts
