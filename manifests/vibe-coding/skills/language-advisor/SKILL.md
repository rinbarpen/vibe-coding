---
name: language-advisor
description: Consults the language selection decision tree and specification sheets
  to recommend the optimal language for a given use case across Go, Rust, Python,
  TypeScript, and Java. Provides rationale, spec sheet reference, and agent+skill
  recommendations.
triggers:
  - pattern: "what language (should|to) (use|choose|pick)"
    description: Language selection advice
  - pattern: "choose (a|the) (programming )?language"
    description: Language selection for a project
---

# Language Advisor

## Selection Process

1. **Gather context**: What type of application? Performance requirements? Team expertise? Deployment constraints?
2. **Run decision tree**: Walk through `references/decision-trees/language-selection.md`
3. **Present recommendation**: Language name + 2-3 sentence rationale
4. **Show spec sheet**: Link to `references/language-specs/<lang>.md`
5. **Suggest agents+skills**: Reviewer, patterns skill, build resolver

## Quick Reference

| Context | Best Fit | Also Consider |
|---------|----------|---------------|
| Web frontend | TypeScript | — |
| Backend API | Go | TypeScript, Python |
| Full-stack | TypeScript + Go | TypeScript only, Python + React |
| CLI tool | Go | Rust (perf-critical) |
| Systems programming | Rust | — |
| ML/AI service | Python | Rust (via burn/candle for inference) |
| Enterprise microservice | Go or Java | — |
| Rapid prototype | Python or TypeScript | — |
| Event processing | Go | Rust (low-latency) |
| Data pipeline | Python | Go (high throughput) |
| Desktop (Electron) | TypeScript | Rust (via Tauri) |
| Desktop (Tauri) | TypeScript + Rust | — |
| Desktop (Flutter) | Dart | — |
