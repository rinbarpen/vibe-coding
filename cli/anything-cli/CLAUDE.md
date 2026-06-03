# CLAUDE.md (Anything CLI)

Manifest for [CLI-Anything](https://github.com/HKUDS/CLI-Anything) — a tool that transforms any software into an AI agent-controllable CLI interface. One command generates a production-grade CLI harness for any codebase.

## Data Safety

1. **Source isolation**: Generated CLIs are created in isolated directories, never modifying the original codebase.
2. **Sandbox testing**: Test generated CLIs in a sandbox environment before production use.
3. **Permission awareness**: Some generated CLIs wrap software that requires elevated permissions.

## Commands

| Command | Description |
|---------|-------------|
| `pip install cli-anything-hub` | Install CLI-Hub package manager |
| `cli-hub install <name>` | Install a pre-built CLI from the registry |
| `cli-hub search <query>` | Search the CLI-Hub registry |
| `cli-hub list` | List all installed CLIs |
| `/cli-anything <path-or-url>` | Build a CLI harness for any software (plugin mode) |
| `/cli-anything:refine [focus]` | Refine an existing CLI harness |
| `/cli-anything:test <path>` | Run tests for a CLI harness |
| `/cli-anything:validate <path>` | Validate a CLI harness against standards |
| `/cli-anything:list` | List all CLI-Anything tools |
| `pip install cli-anything-<name>` | Install a generated CLI package |
| `cli-anything-<name> --help` | Get help for a generated CLI |
| `cli-anything-<name> --json <cmd>` | Run a CLI command with JSON output |

## Architecture

```
<root>/
  harnesses/          # Generated CLI harness directories
  registry/           # Locally cached CLI-Hub registry
  configs/            # CLI generation configuration overrides
  tests/              # Cross-harness integration tests
```

## Key Resources

- `https://github.com/HKUDS/CLI-Anything` — Upstream repository
- `https://clianything.cc/` — CLI-Hub web catalog
- CLI-Hub: `pip install cli-anything-hub` then `cli-hub install <name>`

## Pipeline (7-Phase CLI Generation)

1. **Source Acquisition**: Clone repo or use local path
2. **Codebase Analysis**: Parse architecture, APIs, data models
3. **CLI Architecture Design**: Design command groups and interface
4. **Implementation**: Build Click-based CLI with REPL mode
5. **Test Planning**: Design test strategies and synthetic data
6. **Test Implementation & Documentation**: Write tests and docs
7. **SKILL.md Generation**: Auto-generate skill definition for agent discovery

## Gotchas

- **Python 3.10+** required for CLI generation
- **Target software** must be installed locally for E2E testing
- Generated CLIs use PEP 420 namespace packages (`cli_anything.*`)
- REPL mode is the default entry point; pass a command to skip REPL
- `--json` flag on every command for machine-readable output
- Upstream software may need to be in PATH for the generated CLI to work
