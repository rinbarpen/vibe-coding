---
name: ralph-completion
enabled: true
event: stop
pattern: .*
action: warn
---

## Ralph Loop: Completion Verification

Before closing this session, verify the ralph-loop workflow:

### Final Acceptance Checklist
- [ ] RFC written and all sections addressed
- [ ] All work units completed through their tier pipeline
- [ ] No unresolved dependency failures
- [ ] Integration tests pass on main branch
- [ ] All unit branches merged/deleted
- [ ] RFC execution log updated
- [ ] Unit scorecards reviewed

### Outputs to Archive
- RFC document → `docs/rfc/{feature-name}.md`
- Unit definitions → `docs/rfc/{feature-name}-units.md`
- Execution log
- Dependency graph snapshot
- Integration risk summary

### Next Steps
- Did any units stall? → Document lessons in RCA log
- Any architectural debt introduced? → File a follow-up issue
