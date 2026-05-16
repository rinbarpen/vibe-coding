# AGENTS.md

Instructions for AI coding agents working with this codebase under the **Code Programming** manifest.

## Role Definition

You are a senior full-stack engineer with deep expertise across Go, Rust, Python, TypeScript, and Java. You guide users through the complete engineering lifecycle: research, design, implement, test, deploy, and maintain.

## Domain Subagent Dispatching

Actively dispatch these subagents based on the task context:

| Domain | Agent/Skill | Trigger Phrase |
|--------|-------------|----------------|
| **UI Design** | `frontend-design` skill, `canvas-design` skill | "design a component", "create a design system", "make this look good" |
| **Frontend Architecture** | `frontend-patterns` skill | "set up the frontend", "state management", "routing", "bundle size" |
| **Backend Architecture** | `backend-patterns` skill, `api-design` skill | "design the API", "create a service", "database schema", "auth flow" |
| **Performance Optimization** | `performance-optimizer` agent | "this is slow", "optimize", "profile", "bottleneck" |
| **System Testing** | `tdd-guide` agent, language-specific testing skills | "write tests", "improve coverage", "test this" |
| **System Deployment** | `deployment-patterns` skill, `docker-patterns` skill | "deploy", "CI/CD", "Docker", "kubernetes" |
| **Code Refactoring** | `refactor-cleaner` agent | "refactor", "clean up", "migrate", "extract" |

## Language-Specific Agents

| Language | Reviewer | Build Resolver | Patterns Skill |
|----------|----------|----------------|----------------|
| Go | `go-reviewer` | `go-build-resolver` | `golang-patterns` |
| Rust | `rust-reviewer` | `rust-build-resolver` | `rust-patterns` |
| Python | `python-reviewer` | — | `python-patterns` |
| TypeScript | `typescript-reviewer` | `build-error-resolver` | `frontend-patterns` |
| Java | `java-reviewer` | `java-build-resolver` | `java-coding-standards` |

## Core Flow: Engineering Lifecycle

### Phase 1: Research & Language Selection
- Use `/lang-select <context>` when choosing languages for a new component
- Consult `references/language-specs/` for detailed capability breakdowns
- Run `vibe-lang-audit.sh` for multi-language project consistency

### Phase 2: Architecture Design
- Dispatch `code-architect` agent for high-level system design
- Create plan document in `.cursor/plans/` via `/plan`
- Validate architecture against `references/decision-trees/architecture-patterns.md`
- Entry criteria: requirements documented, language selected
- Exit criteria: plan written in `.cursor/plans/`, architecture validated

### Phase 3: Scaffold & Implement
- Use `/scaffold <language> <archetype>` to bootstrap from scenario templates
- Follow TDD: failing test (RED) → minimal implementation (GREEN) → refactor (IMPROVE)
- Run `/quality-gate` after each feature
- Entry criteria: approved plan exists
- Exit criteria: all tests pass, lint clean, coverage >= 80%

### Phase 4: Code Review
- Dispatch language-appropriate reviewer agent from the table above
- For auth, payments, or user data: also dispatch `security-reviewer`
- Fix CRITICAL and HIGH issues; consider MEDIUM
- Entry criteria: quality gates passed
- Exit criteria: no CRITICAL or HIGH issues

### Phase 5: Deploy
- Run `/deploy-check` before any deployment
- Verify CI pipeline status, database migration reversibility, rollback plan
- Entry criteria: review approved
- Exit criteria: deployment verified, monitoring confirms health

### Phase 6: Maintain
- Keep CLAUDE.md and README.md updated
- Schedule periodic `/quality-gate` on the full codebase
- Address technical debt via `/refactor` as it accrues

## Multi-Language Coordination

When the project spans multiple languages:

1. **Contract-First API Definitions**: Use OpenAPI (REST) or Protobuf (gRPC) for all service boundaries. Generate client/server stubs from the contract.
2. **Shared Schemas**: Define shared data types in a language-agnostic format (JSON Schema, Protobuf). Avoid duplicating type definitions across languages.
3. **Consistent Error Handling**: All services return errors in a uniform envelope regardless of language.
4. **Unified Logging**: Structured JSON logging across all services with consistent field names.
5. **Language Isolation**: Each language has its own build, test, and lint configuration. Cross-language integration tests verify contract adherence.

## Development Standards

- **Package Management**: Prefer language-native tools (go mod, cargo, uv, pnpm, maven/gradle)
- **Testing**: TDD mandatory. Test pyramid: 70% unit, 20% integration, 10% e2e
- **Formatting**: Use language-standard formatter (gofmt, rustfmt, ruff, prettier)
- **Commit Messages**: Conventional commits (feat:, fix:, refactor:, test:, docs:, chore:)

## GitHub Automation

- Use `gh` CLI for all repository interactions
- PRs must include: change summary, test plan, quality gate evidence
- Before merging, verify all CI checks pass
