---
name: ralph-decompose
enabled: true
event: prompt
pattern: (rfc|decompos|work.?unit|dag|dependency)\s*
action: warn
---

## Ralph Loop: DAG Decomposition

You're working on RFC decomposition. Break the RFC into independently verifiable work units.

### Work Unit Template

```typescript
interface WorkUnit {
  id: string;              // kebab-case identifier
  name: string;            // Human-readable name
  rfcSections: string[];   // Which RFC sections this addresses
  description: string;     // Detailed description
  deps: string[];          // Dependencies (other unit IDs)
  acceptance: string[];    // Concrete acceptance criteria
  tier: "trivial" | "small" | "medium" | "large";
}
```

### Decomposition Rules
- Prefer fewer, cohesive units (minimize merge risk)
- Minimize cross-unit file overlap (avoid conflicts)
- Keep tests WITH implementation (never split "implement X" + "test X")
- Dependencies only where real code dependency exists

### Dependency DAG

```
Layer 0: [unit-a, unit-b]     ← no deps, run in parallel
Layer 1: [unit-c]             ← depends on unit-a
Layer 2: [unit-d, unit-e]     ← depend on unit-c
```

### Complexity Tier → Pipeline Depth

| Tier | Pipeline Stages |
|------|----------------|
| trivial | implement → test |
| small | implement → test → code-review |
| medium | research → plan → implement → test → review-fix |
| large | research → plan → implement → test → review-fix → final-review |

### Output
Document the decomposition in `docs/rfc/{feature-name}-units.md`.
