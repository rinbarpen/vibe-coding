---
name: ralph-validation
enabled: true
event: bash
pattern: (npm\s+(test|run\s+test|run\s+check)|pytest|go\s+test|cargo\s+test|make\s+test)
action: warn
---

## Ralph Loop: Validation Checklist

Running tests is part of the ralph-loop quality pipeline. Verify the full validation stage:

### Per-Tier Validation Requirements

| Tier | Must Pass | Should Check |
|------|-----------|-------------|
| trivial | Unit tests | Lint |
| small | Unit tests, lint | Type check |
| medium | Unit tests, lint, type check | Integration tests |
| large | All tests, lint, type check | Security scan, perf benchmark |

### Before Declaring Done
- [ ] All acceptance criteria met
- [ ] No regression in existing tests
- [ ] No new lint/type errors
- [ ] Edge cases documented or handled
- [ ] Test coverage thresholds maintained

### De-Sloppify Check
After tests pass, run a cleanup pass to remove:
- Tests that verify language/framework internals (not business logic)
- Overly defensive runtime checks the type system guarantees
- Console.log / debugger statements
- Commented-out code
