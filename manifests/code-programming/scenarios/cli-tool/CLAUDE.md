# CLAUDE.md — CLI Tool Scenario

## Architecture
- **Language**: Go (cobra) or Rust (clap)
- **Distribution**: Single binary (go build / cargo build --release)
- **Config**: Environment variables + config file (~/.config/tool/config.yaml)
- **Output**: Structured (JSON) and human-readable (text table) output modes

## Commands
| Command | Description |
|---------|-------------|
| `go build ./cmd/tool` | Build Go tool |
| `cargo build` | Build Rust tool |
| `cargo run -- --help` | Show usage |
| `go test ./...` or `cargo test` | Run tests |
| `go install ./cmd/tool@latest` | Install from source |

## Key Rules
- `--help` output must be comprehensive and well-organized
- Support `--json` flag for machine-readable output
- Exit codes: 0 success, 1 general error, 2 usage error
- Config file in XDG-compliant location
- Auto-completion scripts for bash/zsh/fish (cobra supports this natively)

## Environment Variables
```
TOOL_CONFIG_DIR=~/.config/tool
TOOL_LOG_LEVEL=info
```
