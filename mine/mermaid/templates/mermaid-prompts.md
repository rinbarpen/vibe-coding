# Mermaid Prompt Templates

Copy-paste prompts for generating Mermaid diagrams. Replace placeholders in `[brackets]` with your content.

---

## Flowchart

### Basic Process Flow
```
Create a Mermaid flowchart (graph TD) for: [process name].
Steps: [step1] → [step2] → [step3] → [step4].
Add a decision diamond at [decision point]: if yes → [path A], if no → [path B].
Both paths converge to [final step].
Use subgraphs to group: [group1] ("[group1 label]") and [group2] ("[group2 label]").
Style start node green, end node blue, decision diamond yellow.
```

### User Journey
```
Create a Mermaid graph LR for a user journey:
[entry point] → [action A] → [action B] → {decision} → [outcome C] / [outcome D].
Add click events: click [node] "url".
```

### CI/CD Pipeline
```
Create a Mermaid graph LR for a CI/CD pipeline:
Code Commit → Build → Unit Test → Integration Test → Staging Deploy → {Approval Gate?} → Production Deploy / Rollback.
Add a subgraph "CI Phase" around Build and Tests.
Add a subgraph "CD Phase" around Deploy steps.
```

---

## Sequence Diagram

### API Flow
```
Create a Mermaid sequence diagram for: [API endpoint name].
Participants: Client, API Gateway, [Service A], [Service B], Database.
Flow:
1. Client → API Gateway: [request]
2. API Gateway → [Service A]: [validate request]
3. [Service A] → Database: [query]
4. Database → [Service A]: [result]
5. [Service A] → [Service B]: [enrich data]
6. [Service B] → [Service A]: [enriched result]
7. [Service A] → API Gateway: [response]
8. API Gateway → Client: [formatted response]
Add activation bars. Add Note blocks for error handling.
```

### Auth Flow
```
Create a Mermaid sequence diagram for an authentication flow:
Participants: User, Client, Auth Server, Resource Server.
Standard OAuth 2.0 authorization code flow with PKCE.
Include: authorize redirect, code exchange, token response, API call with Bearer token, refresh flow.
Add Note blocks explaining each grant type step.
```

### Payment Flow
```
Create a Mermaid sequence diagram for a payment flow:
Participants: Customer, App, Payment Service, Bank, Webhook Handler.
1. Customer initiates payment in App
2. App requests payment intent from Payment Service
3. Payment Service creates intent, returns client secret
4. App confirms with Customer's bank
5. Bank processes, returns success to App
6. Bank sends async webhook to Webhook Handler
7. Webhook Handler updates Payment Service
8. Payment Service notifies App via callback
Add alt/else for failure path. Add Note over Bank explaining PCI compliance boundary.
```

---

## Class Diagram

### Domain Model
```
Create a Mermaid classDiagram for a [domain] domain model:
- [Entity1]: +id: String, +createdAt: Date, [methods...]
- [Entity2]: +id: String, +[field]: [type], [methods...]
Relationships:
- [Entity1] "1" -- "*" [Entity2]: [relationship description]
- [Entity2] "*" -- "1" [Entity3]: [relationship description]
Add abstract class [BaseEntity] with +id, +createdAt, +updatedAt.
```

### Design Pattern
```
Create a Mermaid classDiagram showing the [pattern name] design pattern:
- Interface [Interface]: +[method signatures]
- ConcreteClass [Class A]: implements [Interface]
- ConcreteClass [Class B]: implements [Interface]
- Factory: creates appropriate concrete class
Show inheritance with <|-- and composition with *--.
```

---

## State Diagram

### Entity Lifecycle
```
Create a Mermaid stateDiagram-v2 for [entity] lifecycle:
States: Created → [State2] → [State3] → [State4] → [Archived/Completed]
Transitions:
- Created → [State2]: [trigger event]
- [State2] → [State3]: [trigger event]
- [State3] → [State2]: [rollback event]
- [State3] → [State4]: [trigger event]
- Any state → Error: [error event]
- Error → [Previous state]: retry
Add composite state for sub-states where appropriate.
```

### UI State Machine
```
Create a Mermaid stateDiagram-v2 for [component/screen] UI states:
Initial → Loading → [Loaded/Empty/Error]
- Loading → Loaded: data arrives
- Loading → Empty: no data
- Loading → Error: network error
- Error → Loading: retry
- Loaded → Loading: refresh
Add note on Loading state: "Show skeleton/spinner".
```

---

## ER Diagram

### Database Schema
```
Create a Mermaid erDiagram for [database name]:
- [Table1] { [type] [field1] PK "[description]", [type] [field2] UK "[description]", [type] [field3] "[description]" }
- [Table2] { [type] [field1] PK "[description]", [type] [field2] FK "[description]", [type] [field3] "[description]" }
Relationships:
- [Table1] ||--o{ [Table2]: "[relationship]"
- [Table2] }o--|| [Table3]: "[relationship]"
Use crow's foot notation (|| for one, o{ for zero-or-many, }| for one-or-many).
```

---

## Gantt Chart

### Project Plan
```
Create a Mermaid gantt chart for [project name]:
dateFormat YYYY-MM-DD
section [Phase 1 Name]
[Task 1] :[id], [start], [duration]
[Task 2] :[id], after [prev], [duration]
section [Phase 2 Name]
[Task 3] :[id], after [prev], [duration]
[Task 4] :[id], after [prev], [duration]
Mark critical tasks with crit.
Add todayMarker for current date.
```

---

## Git Graph

### Branch Strategy
```
Create a Mermaid gitGraph for:
- main branch with initial commit and v1.0 tag
- develop branch off main
- feature/login branch off develop with 3 commits, merged back
- feature/payment branch off develop with 2 commits, merged back
- release/1.0 branch off develop, commit, merge to main and develop
- hotfix off main, merged to main and develop
Tag releases: v1.0, v1.0.1
```

---

## Mind Map

### Feature Breakdown
```
Create a Mermaid mindmap for [feature/product]:
root(([Feature Name]))
  [Category 1]
    [Sub A]
      [Detail 1]
      [Detail 2]
    [Sub B]
  [Category 2]
    [Sub C]
    [Sub D]
  [Category 3]
    [Sub E]
    [Sub F]
Use icons: ::icon(fa fa-[icon-name]) where relevant.
```

---

## C4 Architecture

### System Context
```
Create a Mermaid C4Context diagram for [system name]:
Person([user type], "[Label]", "[Description]")
System([system name], "[Label]", "[Description]")
System_Ext([external system], "[Label]", "[Description]")
Rel([source], [target], "[Description]", "[Technology]")
```

### Container Diagram
```
Create a Mermaid C4Container diagram for [system name]:
Container([app component], "[Type]", "[Tech]")
ContainerDb([database], "[Type]", "[Tech]")
Add system boundary around internal containers.
```

---

## Pie Chart

### Distribution
```
Create a Mermaid pie chart for [title]:
"[Slice 1]" : [value]
"[Slice 2]" : [value]
"[Slice 3]" : [value]
"[Slice 4]" : [value]
Values should sum to 100 for percentages, or use raw values.
```

---

## Timeline

### Release History
```
Create a Mermaid timeline for [project] releases:
title [Project] Release Timeline
[date/section] : [event 1]
                : [event 2]
[date/section] : [event 3]
                : [event 4]
```

### Project Milestones
```
Create a Mermaid timeline for [project] milestones:
title [Project] Milestones
[Phase] : [milestone 1] : [milestone 2]
[Phase] : [milestone 3]
[Phase] : [milestone 4] : [milestone 5]
```

---

## Sankey Diagram

### Data Flow
```
Create a Mermaid sankey-beta diagram for [flow description]:
[Source A], [Target X], [amount]
[Source A], [Target Y], [amount]
[Source B], [Target X], [amount]
[Source B], [Target Z], [amount]
```

---

## Block Diagram (XY Chart)

### Architecture Blocks
```
Create a Mermaid block-beta diagram for [system architecture]:
columns [N]
[Block 1]:[span]
[Block 2] [Block 3] [Block 4]
space [Block 5]:[span]
```
