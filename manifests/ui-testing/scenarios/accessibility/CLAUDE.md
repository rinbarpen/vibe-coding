# Accessibility Testing Scenario

## Context

You are writing accessibility tests that audit web pages for WCAG compliance. These tests run against a real browser (Playwright) and check against WCAG Level AA standards.

## Key Conventions

- **Tool**: axe-core (via `@axe-core/playwright`)
- **Standard**: WCAG 2.1 Level AA
- **Tag**: All a11y tests tagged with `@a11y`
- **Scope**: One audit per unique page template

## Commands

```bash
npx playwright test --grep @a11y              # Run a11y tests only
npx playwright test homepage.a11y.spec.ts     # Run single a11y test
```

## Rules

See `rules/ui-testing-a11y.mdc` for detailed rules.
