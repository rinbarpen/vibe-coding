# CLAUDE.md

Multi-language software engineering project managed under the **Code Programming** manifest. Covers the complete engineering lifecycle from idea to deployed system across Go, Rust, Python, TypeScript/JavaScript, and Java.

## Commands

| Command | Description |
|---------|-------------|
| `/plan <domain>` | Create implementation plan for a domain or feature |
| `/scaffold <language> <archetype>` | Bootstrap new project from scenario template |
| `/implement <task>` | Implement a feature following TDD (RED-GREEN-IMPROVE) |
| `/quality-gate` | Run all 5 quality gates before commit |
| `/deploy-check` | Pre-deployment verification checklist |
| `/lang-select <context>` | Get language recommendation for a use case |

## Architecture

```
<root>/
  src/           # Source code (language-dependent structure)
  tests/         # Tests mirroring src structure
  docs/          # Architecture Decision Records, API docs, guides
  scripts/       # Build, CI, and utility scripts
  infra/         # Infrastructure as Code (Docker, Terraform, etc.)
  .cursor/
    plans/       # Implementation plans (Plan-First)
    rules/       # Active manifest rules
```

## Language Selection (Concise)

| Context | Recommended | Why |
|---------|-------------|-----|
| Web frontend | TypeScript | Only browser-native option |
| Full-stack web | TypeScript + Go | TS for UI, Go for API services |
| Backend API / microservice | Go | Fast compile, great stdlib, goroutines |
| CLI tool | Go or Rust | Single binary; Rust for perf-critical |
| Systems / performance-critical | Rust | Zero-cost abstractions, memory safety |
| Data science / ML/AI | Python | Dominant ecosystem |
| Enterprise / large-scale | Java | Mature JVM, Spring ecosystem |
| Rapid prototyping | Python or TypeScript | Fastest path to working code |

See `references/decision-trees/language-selection.md` for the full decision tree.

## Quality Gates (Mandatory Before Every Commit)

1. **Lint Gate**: Zero warnings from language-appropriate linter
2. **Test Gate**: 80%+ coverage, all tests pass
3. **Security Gate**: No secrets, validated inputs, authorized access
4. **Review Gate**: Language-appropriate code reviewer approval
5. **Doc Gate**: CLAUDE.md and README.md reflect current state

## Code Style

- KISS, DRY, YAGNI — start simple, refactor when pressure is real
- Immutability by default — never mutate in place, always return new copies
- Many small files over few large ones (200-400 lines typical, 800 max)
- Domain-driven organization, not type-driven
- Full type annotations in typed languages; no `any` in TS, no `interface{}` in Go

## Environment

- Secrets managed via environment variables or secret manager
- No hardcoded credentials in source code
- `LOG_LEVEL` convention across services (debug/info/warn/error)
- Language-specific environment files (`.env` for local dev, not committed)

## Gotchas

- Cross-language RPC serialization: always use Protobuf or OpenAPI for service boundaries
- Database migrations must be reversible; test rollbacks in staging
- Environment parity: dev/staging/prod mismatch is the #1 deployment failure cause
- When using 2+ languages, each language gets its own CLAUDE.md section

## Workflow

1. **Research & Language Selection** — Use `/lang-select` for unopinionated choices
2. **Architecture Design** — Create plan in `.cursor/plans/` via `/plan`
3. **Scaffold** — `/scaffold <lang> <archetype>` to bootstrap
4. **Implement** — `/implement <task>` with TDD loop
5. **Quality Gate** — `/quality-gate` before every commit
6. **Review** — Language-specific reviewer, security for sensitive code
7. **Deploy** — `/deploy-check` before release
8. **Maintain** — Keep CLAUDE.md current, refactor as debt accrues
