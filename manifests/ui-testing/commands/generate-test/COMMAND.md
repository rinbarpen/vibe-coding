---
description: AI-assisted test generation from component or page analysis
globs: ["src/**/*.{tsx,jsx,ts,js}", "app/**/*.{tsx,jsx}"]
---

# Generate Test

## `/generate-test`

**Purpose**: Analyze a target component, page, or utility and generate comprehensive tests following the UI testing manifest patterns.

**Usage**:
```
/generate-test --target=src/components/LoginForm.tsx
/generate-test --target=src/pages/Dashboard.tsx --type=e2e
/generate-test --target=src/utils/format.ts --type=unit
/generate-test --target=app/api/users/route.ts --type=integration
```

**Execution Logic**:
1. Read the target file to understand its interface and dependencies
2. Detect test type defaults: `.tsx` → component test, utility → unit test, `page/` → e2e
3. Identify existing patterns: check existing test files in the same directory for conventions
4. Generate test file at the standard location:
   - Component: `tests/unit/components/LoginForm.test.tsx`
   - E2E: `tests/e2e/specs/dashboard.spec.ts`
   - Integration: `tests/integration/users.test.ts`
5. Apply relevant rules:
   - Component: Testing Library queries, userEvent, MSW if API calls
   - E2E: Page Object Model, locator actions, page.route for API
   - Unit: pure function tests, no DOM

**Parameters**:
- `--target=<path>`: Target file to test (required)
- `--type=<unit|integration|e2e>`: Override auto-detected test type (optional)
