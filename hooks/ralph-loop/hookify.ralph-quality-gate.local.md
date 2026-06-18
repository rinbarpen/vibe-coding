---
name: ralph-quality-gate
enabled: true
event: bash
pattern: git\s+(merge|rebase|push|checkout\s+-b)
action: warn
---

## Ralph Loop: Merge Queue Rules

You're about to perform a git operation. Ensure the ralph-loop merge queue rules are followed:

### Before Merging
- [ ] All unit quality pipelines completed (research → plan → implement → test → review)
- [ ] No unresolved dependency failures
- [ ] Unit branch rebased on latest integration branch
- [ ] Integration tests pass after rebase

### Merge Queue Flow

```
Unit branch
    │
    ├─ Rebase onto main
    │   └─ Conflict? → EVICT (capture conflict context)
    │
    ├─ Run build + tests
    │   └─ Fail? → EVICT (capture test output)
    │
    └─ Pass → Fast-forward main, push, delete branch
```

### File Overlap Intelligence
- Non-overlapping units → land speculatively in parallel
- Overlapping units → land one-by-one, rebasing each time

### Eviction Recovery
If evicted, capture full context and feed back to implementation:
```markdown
## MERGE CONFLICT
Conflicting files: {paths}
Previous unit: {id}
Rebase instructions: {details}
```
