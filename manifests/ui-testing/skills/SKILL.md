---
name: ui-testing-manifest
description: UI testing knowledge and patterns for AI-assisted testing workflows
---

# UI Testing Skill

## Description

Comprehensive UI testing knowledge base covering testing patterns, framework guides, and best practices for web, mobile, and accessibility testing.

## Core Flow

1. **Analyze** — Understand component/page structure and test gaps
2. **Select Pattern** — Choose the right pattern from `skills/patterns/`
3. **Generate** — Write tests following the pattern and rules
4. **Run** — Execute tests and verify results
5. **Iterate** — Fix failures, improve coverage, diagnose flakiness

## Pattern Reference

See `skills/patterns/` for detailed guides:

| Pattern | When to Use |
|---------|-------------|
| Page Object | E2E tests across multiple spec files |
| Component Test | Isolated component behavior verification |
| API Mocking | Integration tests with external dependencies |
| Visual Regression | UI with intentional visual design |
| Accessibility | WCAG compliance verification |

## Framework Guides

Primary frameworks (recommended):
- **Playwright**: Cross-browser E2E testing
- **Vitest + Testing Library**: Component and unit testing
- **MSW**: API mocking for integration tests

Secondary (scenario-specific):
- **Cypress**: Alternative E2E (prefer Playwright unless team uses Cypress)
- **Detox**: React Native E2E
- **Percy/Chromatic**: Visual regression
- **axe-core**: Accessibility audits
