# Web E2E Testing Scenario

## Context

You are writing end-to-end tests that run in a real browser against a running application. Tests simulate real user interactions — clicks, typing, navigation — and verify the application behaves correctly from the user's perspective.

## Key Conventions

- **Framework**: Playwright (preferred) or Cypress
- **Browser targets**: Chromium (default), Firefox, WebKit (smoke tests only)
- **Page Objects**: Every spec file that interacts with a page uses a Page Object
- **Test data**: Use factories + API seeding, never type through the UI to set up state
- **Mobile**: Test critical flows at 390px viewport (iPhone 14 size)

## Commands

```bash
npx playwright test                    # Run all E2E tests
npx playwright test --grep @smoke     # Smoke tests only
npx playwright test --project=firefox # Single browser
npx playwright show-report            # View HTML report
```

## Rules

See `rules/ui-testing-web-e2e.mdc` for detailed rules.
