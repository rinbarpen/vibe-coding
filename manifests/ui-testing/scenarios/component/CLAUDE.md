# Component Testing Scenario

## Context

You are writing component-level tests that verify individual UI components in isolation. These tests run in a simulated browser environment (jsdom) without a real browser.

## Key Conventions

- **Framework**: Vitest + Testing Library
- **Queries**: Prefer `getByRole` / `getByLabelText` / `getByTestId` (in that order)
- **Interactions**: `@testing-library/user-event` (not `fireEvent`)
- **Providers**: Wrap in custom `renderWithProviders` (router, context, theme)

## Commands

```bash
npx vitest run                           # Run all component tests
npx vitest --watch                        # Watch mode
npx vitest run --coverage                 # With coverage
npx vitest run src/components/LoginForm   # Single file
```

## Rules

See `rules/ui-testing-component.mdc` for detailed rules.
