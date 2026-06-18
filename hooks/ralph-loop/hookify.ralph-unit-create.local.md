---
name: ralph-unit-create
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: .*units?\.(md|json|yaml|yml)$
  - field: new_text
    operator: regex_match
    pattern: (tier|work.?unit|acceptance)
action: warn
---

## Ralph Loop: Quality Pipeline Selection

You're creating a work unit definition. Choose the right complexity tier:

| Tier | Pipeline Stages | When |
|------|----------------|------|
| **trivial** | implement → test | Obvious change, no risk |
| **small** | implement → test → code-review | Multi-file but contained |
| **medium** | research → plan → implement → test → review-fix | New behavior, moderate risk |
| **large** | research → plan → implement → test → review-fix → final-review | Architectural change, high risk |

### Quality Pipeline per Unit (Medium/Large)

1. **Research** — Read codebase + RFC, produce context doc
2. **Plan** — Design implementation steps
3. **Implement** — Write code following the plan
4. **Test** — Run build + test suite
5. **Review** — Spec compliance + code quality
6. **Review Fix** — Address review issues
7. **Final Review** — Quality gate (large tier only)

### Key Rules
- Each stage runs in its **own context window** (separate agent call)
- The reviewer **never wrote the code** it reviews (eliminate author bias)
- Worktree isolation: each unit runs in its own worktree
