---
name: domain-dispatcher
description: Routes development tasks to the correct domain (UI, Frontend, Backend,
  Optimization, Testing, Deployment, Refactoring) and dispatches the appropriate
  subagents, skills, and rule sets from the code-programming manifest.
triggers:
  - pattern: "(design|implement|fix|improve|optimize|refactor) (the |this |our )?(ui|frontend|backend|API|test|deploy)"
    description: Domain-specific task dispatch
---

# Domain Dispatcher

## Dispatch Logic

Map task keywords to domain, then dispatch the appropriate agent, skill, and rule set.

| Task Keywords | Domain | Agent | Skill | Rule File |
|---------------|--------|-------|-------|-----------|
| "UI", "design", "component", "layout", "accessibility", "responsive" | UI Design | `frontend-design` | `canvas-design`, `ui-ux-pro-max-skill` | `vibe-coding-ui-design.mdc` |
| "frontend", "state", "data fetching", "routing", "bundle", "CWV" | Frontend | `frontend-patterns` | `frontend-patterns` | `vibe-coding-frontend.mdc` |
| "backend", "API", "service", "database", "auth", "middleware" | Backend | `code-architect` | `backend-patterns`, `api-design` | `vibe-coding-backend.mdc` |
| "slow", "optimize", "profile", "performance", "cache", "bottleneck" | Optimization | `performance-optimizer` | — | `vibe-coding-optimization.mdc` |
| "test", "coverage", "TDD", "integration", "e2e" | Testing | `tdd-guide` | Language-specific testing skills | `vibe-coding-testing.mdc` |
| "deploy", "CI/CD", "Docker", "release", "rollout" | Deployment | — | `deployment-patterns`, `docker-patterns` | `vibe-coding-deployment.mdc` |
| "refactor", "clean", "migrate", "extract", "dead code" | Refactoring | `refactor-cleaner` | — | `vibe-coding-refactoring.mdc` |
| "agent", "eval", "prompt quality", "llm eval" | Agent Eval | `eval-harness` | `prompt-optimizer`, `superpowers` | `vibe-coding-agent-dev.mdc` |
| "agent", "context engineering", "multi-agent", "agent architecture" | Agent Dev | `code-architect` | `Agent-Skills-for-Context-Engineering`, `agent-skills`, `superpowers` | `vibe-coding-agent-dev.mdc` |
| "desktop", "electron", "tauri", "flutter desktop", "native app" | Desktop | `build-error-resolver` + framework reviewer | `dart-flutter-patterns` | `vibe-coding-desktop.mdc` |
| "frontend", "css", "i18n", "a11y", "component library" | Frontend | `frontend-patterns` | `frontend-design`, `ui-ux-pro-max-skill` | `vibe-coding-frontend.mdc` |

## Cross-Domain Dispatch

When a task spans multiple domains (e.g., "refactor the backend API and add tests"):

1. Identify all domains involved
2. Dispatch sequentially in dependency order:
   - Backend (change the code)
   - Testing (write tests for the change)
3. Each domain uses its own rule set and agents

## Language Dispatch

After domain is determined, dispatch the language-specific agent:

| Language | Reviewer | Build Resolver | Patterns Skill |
|----------|----------|----------------|----------------|
| Go | `go-reviewer` | `go-build-resolver` | `golang-patterns` |
| Rust | `rust-reviewer` | `rust-build-resolver` | `rust-patterns` |
| Python | `python-reviewer` | — | `python-patterns` |
| TypeScript | `typescript-reviewer` | `build-error-resolver` | `frontend-patterns` |
| Java | `java-reviewer` | `java-build-resolver` | `java-coding-standards` |
