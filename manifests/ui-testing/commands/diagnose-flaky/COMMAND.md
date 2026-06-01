---
description: Analyze test output for flakiness patterns and recommend fixes
globs: ["**/test-results/**", "**/playwright-report/**", "**/*.test.*", "**/*.spec.*"]
---

# Diagnose Flaky Tests

## `/diagnose-flaky`

**Purpose**: Analyze test run output (CI logs, local runs, Playwright trace) to identify patterns of flakiness and suggest root-cause fixes.

**Usage**:
```
/diagnose-flaky                      # Analyze latest test run results
/diagnose-flaky --file=test-results.json  # Analyze a specific results file
/diagnose-flaky --ci                  # Fetch and analyze latest CI run
```

**Execution Logic**:
1. Read test results (JUnit XML, Playwright JSON report, or CI log output)
2. Identify flakiness patterns:
   - **Timing**: `waitForTimeout`, sleep patterns, timeout errors
   - **Race condition**: test A depends on test B's state (ordering-dependent)
   - **Network**: flaky API calls, unhandled network errors
   - **Selector**: element not found → stale or non-unique selectors
3. Score each failure: P(pattern-matched) × frequency
4. Recommend fix per pattern:
   - Timing → use locator action, not sleep
   - Race → enforce test isolation
   - Network → add retry or mock
   - Selector → use role/label, add testid
5. Output: flakiness score (0-100) + prioritized fix recommendations
