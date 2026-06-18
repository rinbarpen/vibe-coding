---
name: ralph-rfc-intake
enabled: true
event: prompt
pattern: (implement|add|build|create|develop)\s+(a\s+)?(large|complex|big|multi[-\s]?step|feature|system|module|service)
action: warn
---

## Ralph Loop: RFC Intake Required

You're describing a feature that may benefit from the **ralph-loop** (RFC-driven DAG orchestration) workflow.

### Before implementing, write an RFC document:

```markdown
# RFC: {Feature Name}

## Problem Statement
{What problem does this solve?}

## Proposed Solution
{High-level approach}

## Scope
{What's in / out of scope}

## Dependencies
{Related systems, services}

## Acceptance Criteria
{[ ] Concrete, testable criteria}
```

### Next Step
After writing the RFC, run the **decompose** pass to break it into work units with a dependency DAG.

### When NOT to use ralph-loop
- Single-file changes with no dependencies
- Quick fixes / hotfixes
- Refactoring with no behavioral change
