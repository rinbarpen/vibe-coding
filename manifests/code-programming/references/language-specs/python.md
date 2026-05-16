# Python Language Specification

## Overview
Interpreted, dynamically typed language with optional static typing. The de facto standard for data science, ML/AI, scripting, and rapid prototyping. Known for readability, extensive standard library, and the largest package ecosystem (PyPI).

## Strengths
- Fastest path from idea to working code (minimal boilerplate, REPL-driven development)
- Dominant ecosystem for ML/AI (PyTorch, TensorFlow, scikit-learn, Hugging Face, LangChain)
- Excellent for data manipulation (pandas, numpy, polars, xarray)
- Rich web frameworks (FastAPI, Django, Flask, Starlette)
- Massive package ecosystem (PyPI — 500k+ packages)
- Strong community and documentation
- Great for glue code, automation, and scripting
- uv (recent) has dramatically improved package management speed and reliability

## Weaknesses
- Slow runtime compared to compiled languages (2-10x slower than Go/Rust for CPU-bound work)
- GIL (Global Interpreter Lock) limits CPU-bound parallelism in multi-threaded code
- Dynamic typing requires discipline and tooling (mypy, pyright with strict mode)
- Dependency management fragmentation (pip, poetry, uv, conda, pipenv — uv is now preferred)
- Higher memory usage than compiled languages
- Startup latency (cold start matters for serverless functions)
- No true parallelism within a single process (use multiprocessing or async I/O)

## Best For
- Data science and machine learning (training, inference, data processing)
- AI/LLM application backends (LangChain, LlamaIndex, FastAPI + AI SDKs)
- Rapid prototyping and proof-of-concepts
- Automation scripts and DevOps tooling
- Scientific computing and research
- Web backends with moderate throughput (FastAPI is excellent for IO-bound work)
- ETL pipelines and data processing

## Not Ideal For
- High-throughput, low-latency services (Go or Rust are better)
- Mobile applications (use Kotlin, Swift, or React Native)
- Large-scale concurrent systems with many parallel CPU-bound tasks (Go/Elixir/Java)
- Memory-constrained environments (use Rust/C)
- Safety-critical systems (dynamic typing + GC make behavior less predictable)
- Client-side web applications (TypeScript is the only option)

## Testing
- Framework: `pytest` (plugins: pytest-cov, pytest-asyncio, pytest-xdist)
- Coverage: `pytest --cov=src --cov-report=term-missing` (80%+ threshold)
- Async: `pytest-asyncio` (mark tests with `@pytest.mark.asyncio`)
- Property-based: `hypothesis` (generates test cases from property descriptions)
- Mocking: `unittest.mock` (built-in) or `pytest-mock` (pytest fixture integration)
- Fixtures: pytest fixtures for test setup/teardown (prefer over `setUp`/`tearDown`)
- Parametrization: `@pytest.mark.parametrize` for test case matrices
- Task: `pytest --benchmark` for performance regression detection
- Lint: `ruff check` (fast Rust-based linter), `ruff format` (formatter)
- Type check: `mypy --strict` or `pyright`
- Skills: `python-testing`, `python-patterns`

## Key Libraries
- Web: `FastAPI` (async, Pydantic-based, OpenAPI generation) or `Django` (batteries-included)
- Validation: `Pydantic v2` (Rust-core, validation, serialization)
- ORM: `SQLAlchemy 2.0` (async support), `Django ORM`
- Data: `pandas`, `numpy`, `polars` (fast DataFrame library in Rust)
- ML/AI: `PyTorch`, `scikit-learn`, `transformers`, `langchain`
- CLI: `typer` or `click`
- Async: `asyncio` (stdlib), `anyio` (backend-agnostic async)
- Task queues: `celery` or `dramatiq`
- HTTP client: `httpx` (sync and async)
- Package management: `uv` (preferred), `poetry` (popular alternative)

## Type Annotations
- Use `mypy --strict` or `pyright` for type checking
- Annotate all function signatures (parameters and return types)
- Use `Protocol` for structural subtyping (duck typing with safety)
- Use `TypedDict` for dictionary shapes
- Use `dataclass` (frozen=True for immutability) for data containers
- Use `Literal`, `Union`, `Optional`, `Never` from `typing`
- Prefer `|` syntax for unions (Python 3.10+): `str | int` vs `Union[str, int]`

## References
- Skills: `python-patterns`, `python-testing`
- Agents: `python-reviewer`
- Rules: `~/.claude/rules/python/`
