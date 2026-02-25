# AGENTS.md

Instructions for AI coding agents (Cursor, Claude Code, etc.) working with this codebase.

## Repository Overview

Brief description of the project and its goals.

## Core Flow (Vibe Coding)

Follow these phases for development:

1.  **Plan**: Create a detailed plan in `.cursor/plans/` before major changes.
2.  **Explore**: Use `SemanticSearch` or `explore` subagent to understand existing logic.
3.  **Implement**: Small, incremental changes with immediate `ReadLints` verification.
4.  **Verify**: Run tests and provide evidence of success.
5.  **Review**: Call `code-reviewer` subagent for quality check.
6.  **Ship**: Create PR with a detailed test plan and update `CLAUDE.md`.

## Subagent Dispatching

Actively suggest and launch subagents based on task complexity:

- **`explore`**: For codebase analysis and navigation.
- **`code-architect`**: For high-level design and refactoring.
- **`code-reviewer`**: For pre-commit quality checks.
- **`shell`**: For complex environment or Git operations.

## Development Standards

- **Environment**: Prefer `uv` for Python project management.
- **Network**: Run `proxy_on` before downloading files.
- **Visualization**: Matplotlib plots must use English.
- **Open Source**: Follow standards in `{{VIBE_MANIFEST}}/standards/open-source-standards.md`.

## Maintenance

- Keep `CLAUDE.md` updated with architecture and command changes.
- Use `vibe-claude-md-audit` to ensure project context quality.
