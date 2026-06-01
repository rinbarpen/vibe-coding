# Visual Regression Testing Scenario

## Context

You are writing visual regression tests that compare screenshots against baselines to detect unintended visual changes.

## Key Conventions

- **Tool**: Playwright Snapshots (built-in) or Percy (cloud review)
- **Baselines**: Committed to repo (Playwright) or stored in cloud (Percy)
- **Threshold**: 2% max diff pixel ratio by default
- **Review**: All visual changes reviewed in PR (not just approved blindly)

## Commands

```bash
npx playwright test --grep @visual              # Run visual tests
npx playwright test --update-snapshots           # Update baselines
npx percy exec -- npx playwright test --grep @visual  # Percy run
```

## Rules

See `rules/ui-testing-visual.mdc` for detailed rules.
