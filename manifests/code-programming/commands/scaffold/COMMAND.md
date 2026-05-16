# /scaffold

Bootstrap a new project from scenario templates.

## Usage

```
/scaffold <language> <archetype>
/scaffold go api-service
/scaffold typescript fullstack-web
/scaffold rust cli-tool
/scaffold python data-pipeline
```

## Execution

1. Select scenario archetype from `scenarios/`:
   - `fullstack-web`: TypeScript frontend + Go backend + PostgreSQL
   - `cli-tool`: Go (cobra) or Rust (clap) — single binary
   - `api-service`: Go or Python (FastAPI) — PostgreSQL, Redis, OpenAPI
   - `data-pipeline`: Python — Prefect/Dagster, pandas/polars
2. Copy scenario template files to project root
3. Run language-specific init:
   - Go: `go mod init <project-name>`
   - Rust: `cargo init`
   - Python: `uv init`
   - TypeScript: `pnpm init`
   - Java: `mvn archetype:generate` or `gradle init`
4. Initialize git repo
5. Run `scripts/vibe-init-code.sh` to install manifest rules

## Exit Criteria

- [ ] Project compiles or runs
- [ ] Git repo initialized
- [ ] Manifest rules installed in `.cursor/rules/`
- [ ] CLAUDE.md customized for the project
