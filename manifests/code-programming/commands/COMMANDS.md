# Code Programming Command Registry

## Lifecycle Commands

| Command | Description |
|---------|-------------|
| `/plan <domain>` | Create implementation plan for a domain or feature |
| `/scaffold <language> <archetype>` | Bootstrap new project from scenario template |
| `/implement <task>` | Implement a feature following TDD (RED-GREEN-IMPROVE) |
| `/quality-gate` | Run all 5 quality gates (lint, test, security, review, docs) |
| `/deploy-check` | Pre-deployment verification checklist |
| `/lang-select <context>` | Get language recommendation for a use case |

## Scripts

| Script | Description |
|--------|-------------|
| `scripts/vibe-init-code.sh` | Initialize project with code-programming manifest structure |
| `scripts/vibe-quality-gate.sh` | Run all 5 quality gates with language-specific tooling |
| `scripts/vibe-lang-audit.sh` | Audit multi-language project for cross-language consistency |
