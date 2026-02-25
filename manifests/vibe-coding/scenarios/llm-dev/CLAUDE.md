# CLAUDE.md

## Architecture
- **Models**: OpenAI / Anthropic / Local (Ollama/vLLM)
- **Orchestration**: LangChain / LlamaIndex / DSPy
- **Eval**: RAGAS / DeepEval / Custom Judge

## LLM Commands
| Command | Description |
|---------|-------------|
| `uv run python eval.py` | Run evaluation suite |
| `uv run python data_prep.py` | Prepare training/eval datasets |
| `vibe-check llm` | Verify prompt templates & model connectivity |
| `uv run streamlit run app.py` | Launch LLM playground/demo |

## Development Standards
- **Prompt Management**: Keep prompts in `src/prompts/` as `.txt` or `.yaml`.
- **Testing**: Every major prompt change requires an evaluation report.
- **RAG**: Ensure retrieval quality (Hit Rate, Faithfulness) is monitored.

## Key Files
- `data/` - Datasets (JSONL/Parquet)
- `src/prompts/` - Versioned prompt templates
- `src/eval/` - Evaluation scripts and metrics
- `src/models/` - Model wrappers and API clients
