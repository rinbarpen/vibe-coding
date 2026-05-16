---
name: code-programming
description: Full-stack multi-language software development manifest covering the
  complete engineering lifecycle from idea to deployed system across Go, Rust,
  Python, TypeScript, and Java. Integrates 7 domain rules, language selection
  decision trees, quality gates, and TDD workflow.
model: sonnet
triggers:
  - pattern: "build a (system|service|API|CLI|app)"
    description: Full-stack development request across any supported language
  - pattern: "create a project in (Go|Rust|Python|TypeScript|Java)"
    description: Language-specific project initialization
  - pattern: "(design|implement|deploy|refactor|test|optimize) the"
    description: Domain-specific engineering task
---
