---
description: Run tests with automatic framework detection
globs: ["**/*.test.*", "**/*.spec.*", "**/tests/**", "**/e2e/**"]
---

# Run Tests

## `/run-tests`

**Purpose**: Detect the testing framework in the current project and run the appropriate tests with sensible defaults.

**Usage**:
```
/run-tests                        # Auto-detect and run all tests
/run-tests --file=auth.spec.ts    # Run specific test file
/run-tests --tag=@smoke           # Run tests with a specific tag
/run-tests --watch                # Watch mode (component tests only)
/run-tests --coverage             # Run with coverage
```

**Execution Logic**:
1. Detect framework: check for `playwright.config.*`, `vitest.config.*`, `cypress.config.*`
2. Detect package manager: `pnpm-lock.yaml` → pnpm, `package-lock.json` → npm, `yarn.lock` → yarn
3. Build and run appropriate command
4. Parse test results and report summary
5. If `--coverage`, check coverage threshold (80%)

**Framework Detection Priority**:
- `playwright.config.*` present + file in `tests/e2e/` → `npx playwright test`
- `vitest.config.*` present + file in `tests/unit/` or `tests/integration/` → `npx vitest run`
- `cypress.config.*` present → `npx cypress run`
- Fallback: `npx vitest run` (most common)
