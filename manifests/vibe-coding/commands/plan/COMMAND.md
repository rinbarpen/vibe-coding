# /plan

Create a detailed implementation plan for a domain or feature.

## Execution

1. Determine the domain (ui, frontend, backend, optimization, testing, deployment, refactoring)
2. Determine the target language(s) (see `references/decision-trees/language-selection.md`)
3. Research existing implementations (no reinventing wheels)
4. Invoke `code-architect` or `planner` agent for architecture design
5. Create plan document in `.cursor/plans/<feature-name>.md`

## Plan Template

```markdown
# Plan: <Title>

## Problem
<What needs to be solved, one sentence>

## Approach
<High-level approach>

## Files to Create/Modify
- `path/to/file.go` — what will change

## Test Strategy
- Unit tests: <what>
- Integration tests: <what>
- E2E tests: <what>

## Risks
- <risk> → <mitigation>
```

## Exit Criteria

- [ ] Plan includes: problem statement, approach, file manifest, test strategy, risks
- [ ] Plan approved by user
