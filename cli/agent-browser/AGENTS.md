# AGENTS.md (Agent Browser)

Instructions for AI agents working on browser automation tasks using agent-browser.

## Repository Overview

Browser automation project using [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) — a library that provides AI agents with headless browser control for web navigation, data extraction, form filling, and screenshot capture.

## Agent Roles

### 1. Automation Architect
- **Responsibility**: Design the automation flow, select appropriate commands, handle edge cases.
- **Context**: Review target website structure before writing automation scripts.
- **Output**: Automation script with error handling, waits, and validation steps.

### 2. Data Extractor
- **Responsibility**: Extract structured data from web pages using selectors.
- **Context**: Inspect page DOM to determine robust selector strategies.
- **Output**: Structured JSON/CSV data with validation.

### 3. Test Engineer
- **Responsibility**: Write browser-based tests using agent-browser commands.
- **Context**: Define test scenarios, assertions, and reporting.
- **Output**: Test scripts with pass/fail assertions and screenshot evidence.

## Subagent Dispatching

| Domain | Tool/Skill | Trigger |
|--------|-----------|---------|
| **Test Authoring** | `e2e-testing` skill | Writing browser-based test suites |
| **Data Pipeline** | `data-scraper-agent` skill | Large-scale web data collection |
| **Screenshot Review** | `canvas-design` skill | Visual verification of page states |

## Core Principles

- **Progressive enhancement**: Start simple, add waits and error handling iteratively.
- **Selector robustness**: Prefer `[data-testid]`, `[aria-label]`, or `#id` over positional selectors.
- **Self-healing**: On selector failure, fall back to alternative selectors automatically.
- **Observability**: Always capture screenshots on failure for debugging.
- **Respect robots.txt**: Honor crawl delays and disallowed paths.

## Git Branch Workflow

- **Branch naming**: `browser/<task>` (e.g., `browser/login-flow`, `browser/extract-prices`)
- **Commit checkpoints**: After each successful script → screenshot → report cycle
- **Never automate on production**: Always use staging/sandbox first

## Maintenance

- Keep CLI commands in `CLAUDE.md` updated with upstream agent-browser releases.
- Document anti-bot bypass strategies and known site quirks.
- Maintain a library of reusable selector patterns.
