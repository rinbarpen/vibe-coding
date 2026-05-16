# Code Programming Manifest (Full-Stack Multi-Language Software Engineering)

一个面向全栈、多语言软件工程的综合开发清单，覆盖从想法到部署的完整工程生命周期。

A comprehensive full-stack, multi-language software engineering manifest covering the complete lifecycle from idea to deployed system.

## 覆盖领域 / Covered Domains

| Domain | Description |
|--------|-------------|
| **UI Design** | Design systems, accessibility, responsive layouts, visual design |
| **Frontend Design** | State management, routing, data fetching, bundle optimization |
| **Backend Design** | API design, service architecture, database design, auth |
| **System Optimization** | Profiling, caching, concurrency, memory management |
| **System Testing** | TDD, test pyramid, property-based testing, coverage |
| **System Deployment** | CI/CD, containerization, monitoring, rollback strategies |
| **Code Refactoring** | Migration patterns, backward compatibility, dead code removal |

## 支持语言 / Supported Languages

| Language | Primary Use Cases |
|----------|-------------------|
| **Go** | Backend services, CLI tools, networking, concurrent systems |
| **Rust** | Systems programming, performance-critical, safety-critical |
| **Python** | Data science, ML/AI, rapid prototyping, automation |
| **TypeScript/JavaScript** | Web frontends, full-stack, Node.js services |
| **Java** | Enterprise backends, Android, large-scale distributed systems |

## 包含内容 / What's Included

- **CLAUDE.md / AGENTS.md** — Core AI context and agent dispatching instructions
- **rules/** — 10 Cursor rule files (.mdc) for core, lifecycle, language selection, and 7 domains
- **commands/** — 6 slash commands (plan, scaffold, implement, quality-gate, deploy-check, lang-select)
- **scripts/** — 3 automation scripts (init, quality gate runner, language auditor)
- **skills/** — 4 skill definitions (lifecycle orchestrator, language advisor, domain dispatcher)
- **references/** — 5 language specification sheets, 2 decision trees, lifecycle guide
- **scenarios/** — 4 pre-built project templates (fullstack-web, cli-tool, api-service, data-pipeline)

## 快速开始 / Quick Start

```bash
# 1. Initialize a new project with the manifest
bash manifests/code-programming/scripts/vibe-init-code.sh

# 2. Select a language for your task
# (in Claude Code)
/lang-select "build a real-time chat API"

# 3. Plan before implementing
/plan backend

# 4. Implement with TDD
/implement "user authentication endpoint"

# 5. Quality gate before commit
/quality-gate
```

## 核心原则 / Core Principles

- **Right Tool for the Job**: Clear guidance on when to use each language
- **Plan-First**: No non-trivial change without a plan in `.cursor/plans/`
- **Quality Gates**: 5 mandatory gates (lint, test, security, review, docs) before every commit
- **TDD by Default**: RED-GREEN-IMPROVE loop for every feature
- **Git-Native**: Conventional commits, PR test plans, local git workflow

## 依赖 / Dependencies

- **Bash**: Script execution environment
- **Claude Code / Cursor**: AI coding assistant
- **Language Toolchains**: go, rustc, python, node, java (as needed per project)
- **Docker** (recommended): For containerized development and deployment
