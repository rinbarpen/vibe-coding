# Accessibility Testing Pattern

**Category**: A11y Testing  
**When**: Verifying WCAG compliance as part of the test suite  
**Tools**: axe-core, Pa11y, Playwright axe integration

## Setup

```typescript
// tests/a11y/axe-helper.ts
import { type Page } from '@playwright/test';

// @ts-expect-error — axe-core injects onto window
const AxeBuilder = require('@axe-core/playwright').default;

export async function checkA11y(page: Page, context?: string) {
  const results = await new AxeBuilder({ page })
    .include(context || 'body')
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();

  return results.violations;
}
```

```typescript
// homepage.a11y.spec.ts
import { checkA11y } from './axe-helper';

test('homepage has no critical a11y violations @a11y', async ({ page }) => {
  await page.goto('/');
  const violations = await checkA11y(page);

  const critical = violations.filter(v =>
    ['critical', 'serious'].includes(v.impact),
  );

  expect(critical).toEqual([]);
});
```

## Rules

- **Tag a11y tests**: Use `@a11y` tag to run them separately: `npx playwright test --grep @a11y`
- **WCAG Level AA**: Minimum target. Use tags `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`.
- **Run per-page**: Each unique page template gets an a11y audit. Don't test all states — test the template.
- **Known violations**: If a11y issues are accepted (third-party widget, tech debt), document with a tracked issue link and exclude with `withRules()`.
- **CI integration**: Run a11y tests in a separate CI workflow (they don't need sharding).

## Excluding Known Issues

```typescript
const results = await new AxeBuilder({ page })
  .withRules(['color-contrast'])  // exclude specific rules
  .analyze();
```

Document WHY each rule is excluded, with a link to the tracking issue.

## WCAG Compliance Levels

| Level | Description | Minimum Requirement |
|-------|-------------|-------------------|
| A | Basic web accessibility | MUST pass all A criteria |
| AA | Stronger accessibility | MUST pass all AA criteria (standard target) |
| AAA | Highest accessibility | OPTIONAL — strive for specific criteria |
