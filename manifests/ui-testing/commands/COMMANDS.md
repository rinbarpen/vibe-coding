---
description: Master command registry for UI testing commands
globs: ["**/*.test.*", "**/*.spec.*", "**/tests/**", "**/e2e/**"]
---

# UI Testing Commands

| Command | Description | When to Use |
|---------|-------------|-------------|
| `/run-tests` | Detect framework and run matching tests | Before commit, after changes |
| `/generate-test` | AI-assisted test generation from component/page analysis | New feature, uncovered code |
| `/diagnose-flaky` | Analyze test output for flakiness patterns | Intermittent CI failures |

## Subagent Dispatch

- `/run-tests` → `test-runner`
- `/generate-test` → `test-planner` → `test-writer` → `test-runner`
- `/diagnose-flaky` → `flaky-diagnoser`
