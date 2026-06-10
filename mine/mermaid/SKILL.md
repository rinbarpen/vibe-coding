---
name: mermaid
description: Text-to-diagram generation using Mermaid.js syntax. Create flowcharts, sequence diagrams, class diagrams, state machines, ER diagrams, Gantt charts, pie charts, git graphs, mindmaps, timelines, C4 architecture, and more. Zero dependencies — outputs inline code fences renderable in GitHub, Notion, Obsidian, and any Mermaid-compatible viewer.
---

# Mermaid Diagram Skill

Text-to-diagram generation using Mermaid.js syntax. Zero external dependencies — write Mermaid code fences and render everywhere.

## When to Use

- Flowcharts and process diagrams (simple to medium complexity)
- Sequence diagrams (API flows, protocols)
- Gantt charts and timelines (project planning)
- Entity-relationship diagrams (database schema)
- Class diagrams (OOP design)
- State machines and state charts
- Git branch graphs
- Mind maps and radial diagrams
- Pie charts and simple data visualizations
- C4 architecture diagrams
- Text-first workflows (no GUI needed)

**Not ideal for**: pixel-precise layout, complex network topology, cloud architecture with official icons. Use [Draw.io](../drawio/SKILL.md) for those.

## Diagram Type Reference

### Flowchart (`graph TD` / `graph LR`)

```mermaid
graph TD
    A[Start] --> B{Decision?}
    B -->|Yes| C[Action A]
    B -->|No| D[Action B]
    C --> E[End]
    D --> E
```

Node shapes: `[rectangle]`, `(rounded)`, `{diamond}`, `((circle))`, `[[subroutine]]`, `[(database)]`, `>flag]`

### Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant A as API
    participant D as Database
    U->>A: POST /login
    A->>D: SELECT user
    D-->>A: user record
    A-->>U: JWT token
```

### Class Diagram

```mermaid
classDiagram
    class User {
        +String id
        +String email
        +login()
        +logout()
    }
    class Order {
        +String orderId
        +Date createdAt
        +calculateTotal()
    }
    User "1" --> "*" Order : places
```

### State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Loading : fetch
    Loading --> Success : ok
    Loading --> Error : fail
    Error --> Loading : retry
    Success --> [*]
```

### ER Diagram

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    USER {
        string id PK
        string email UK
        string name
    }
    ORDER {
        string orderId PK
        date createdAt
        float total
    }
```

### Gantt Chart

```mermaid
gantt
    title Project Plan
    dateFormat  YYYY-MM-DD
    section Phase 1
    Research     :a1, 2026-01-01, 14d
    Design       :a2, after a1, 10d
    section Phase 2
    Development  :a3, after a2, 21d
    Testing      :a4, after a3, 7d
```

### Pie Chart

```mermaid
pie title Tech Stack Distribution
    "TypeScript" : 45
    "Python" : 30
    "Go" : 15
    "Rust" : 10
```

### Git Graph

```mermaid
gitGraph
    commit
    branch develop
    checkout develop
    commit
    branch feature
    checkout feature
    commit
    commit
    checkout develop
    merge feature
    checkout main
    merge develop
```

### Mind Map

```mermaid
mindmap
  root((Project))
    Frontend
      React
      CSS Modules
    Backend
      API Gateway
      Microservices
        Auth
        Users
        Orders
    DevOps
      CI/CD
      Docker
```

### Timeline

```mermaid
timeline
    title Release History
    2025-Q4 : v1.0 MVP
    2026-Q1 : v1.1 Performance
    2026-Q2 : v2.0 Redesign
```

### C4 Container Diagram

```mermaid
C4Context
    title System Context for E-Commerce
    Person(customer, "Customer")
    System(shop, "E-Shop", "Online shopping platform")
    System_Ext(payment, "Payment Gateway")
    System_Ext(email, "Email Service")
    Rel(customer, shop, "Browses, orders")
    Rel(shop, payment, "Processes payment")
    Rel(shop, email, "Sends confirmation")
```

### Block Diagram (XY Chart)

```mermaid
block-beta
    columns 3
    Frontend:3
    API["API Gateway"] DB[("Database")]
    space:2 Cache[("Redis Cache")]
```

## Live Preview Options

- **GitHub**: Mermaid renders natively in markdown files
- **mermaid.live**: Paste code at https://mermaid.live for instant preview + export
- **Obsidian**: Native Mermaid support
- **Notion**: Mermaid code blocks via integration
- **VSCode**: "Mermaid Preview" extension

## Quick Tips

- Use `TD` (top-down) for flowcharts, `LR` (left-right) for wide diagrams
- Add `%%` comments to document complex diagrams
- Use subgraphs to group related nodes: `subgraph title ... end`
- Style with `classDef` and `style` for custom colors
- Link nodes with `click nodeId "url"` for interactive diagrams
- For complex diagrams, break into subgraphs rather than one flat graph

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Diagram doesn't render | Check syntax at https://mermaid.live |
| Text overflows nodes | Use shorter labels or `<br/>` for line breaks |
| Arrows crossing | Reorder node definitions; use `LR` instead of `TD` |
| Subgraph not showing | Ensure subgraph has a title and `end` statement |
| Chinese characters garbled | Mermaid supports Unicode; check file encoding |

## Templates

See [templates/mermaid-prompts.md](./templates/mermaid-prompts.md) for 20+ copy-paste prompt templates organized by diagram type.
