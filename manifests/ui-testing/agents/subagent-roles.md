# UI Testing Subagent Roles

## test-planner

Analyzes code changes and recommends test strategy.

**Capabilities:**
- Reads git diff to identify changed components/pages
- Determines test type (unit vs integration vs E2E) based on what changed
- Estimates coverage impact
- Output: list of tests to write or update, with priority

**Triggers:**
- New component → component test (unit)
- New page → E2E test
- Bug fix → regression test
- API change → integration test with MSW

---

## test-writer

Generates test code following manifest patterns.

**Capabilities:**
- Reads component/page source to understand interface
- Writes tests using Testing Library queries (component) or Page Object (E2E)
- Creates MSW handlers for integration tests
- Follows naming conventions from existing tests

**Constraints:**
- No `sleep()` / `waitForTimeout`
- No testing of implementation details
- POM required for E2E page interactions

---

## test-runner

Executes tests and reports results.

**Capabilities:**
- Detects test framework (Playwright, Vitest, Cypress, Jest)
- Runs tests with appropriate flags (parallel, shard, grep)
- Parses test output (TAP, JUnit, JSON)
- Reports: passed, failed, skipped counts + failure details

**Output format:**
```
3 passed, 1 failed, 0 skipped
Failures:
  - LoginForm.test.tsx > shows error on invalid email
    AssertionError: Expected element to be visible
    at LoginForm.test.tsx:23
```

---

## flaky-diagnoser

Identifies flakiness patterns in test failures.

**Capabilities:**
- Parses test results JSON and CI logs
- Matches failures against known flaky patterns (timeout, race, network, selector)
- Calculates flakiness score
- Recommends fixes

**Patterns recognized:**
- Timed out waiting for locator → timeout too short or element condition wrong
- Strict mode violation → multiple elements match selector
- Page crashed → memory leak or infinite loop
- ECONNREFUSED → server not running or port mismatch

---

## coverage-analyzer

Analyzes coverage reports and identifies gaps.

**Capabilities:**
- Reads Vitest/Istanbul coverage output (JSON summary)
- Compares against 80% threshold
- Identifies uncovered files, lines, branches
- Groups uncovered code by component/page area

**Output format:**
```
Coverage: 76% (below 80% threshold)
Gaps:
  - src/components/PaymentForm.tsx (23% — high priority)
  - src/utils/validators.ts (45% — medium priority)
  - src/hooks/useDebounce.ts (0% — low priority)
```
