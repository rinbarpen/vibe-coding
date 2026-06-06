# Branch Strategy Guide

## Strategy Comparison

| 维度 | GitHub Flow | Git Flow | Trunk-based Development |
|------|-------------|----------|------------------------|
| **适用场景** | 快速迭代 SaaS、小团队 | 多版本维护、合规要求高 | DevOps 极致效率、大团队 |
| **主要分支** | `main` + short feature branches | `main`, `develop`, `release/*`, `hotfix/*` | `main` + short-lived feature branches |
| **Feature 分支** | 从 `main` 创建，PR 合并回 `main` | 从 `develop` 创建，PR 合并回 `develop` | 从 `main` 创建，rebase 后 fast-forward |
| **合并方式** | Squash merge | Merge commit | Rebase + fast-forward |
| **Release** | 从 `main` 打 tag | `release/*` 分支 → `main` + `develop` | 从 `main` 打 tag |
| **Hotfix** | 从 `main` 创建 → 修复 → PR | `hotfix/*` → `main` + `develop` | 从 `main` 创建 → 修复 → PR |
| **保护规则** | 2 reviews + status checks | 分层保护（develop/release/main） | 1 review + 自动合并 |
| **优势** | 简单、快速部署 | 多版本并行、严格的发布管理 | 最小化分支冲突、持续集成 |
| **劣势** | 不适合多版本维护 | 复杂、merge 频繁 | 需要高测试覆盖率 |

## 选择建议

- **SaaS / Web 应用**：GitHub Flow（最简单）
- **库/框架/SDK**：Git Flow（需要维护多个版本）
- **合规/监管行业**：Git Flow（审计追踪）
- **大型团队（>50 人）**：Trunk-based（减小 merge 冲突）
- **移动 App**：Git Flow（发版节奏明确）

## Branch Naming Convention

```
<type>/<issue-number>-<kebab-description>
```

### Types

| Prefix | Purpose | Source Branch | Merge Into |
|--------|---------|---------------|------------|
| `feat/` | 新功能 | `main` (GitHub Flow) / `develop` (Git Flow) | 源分支 |
| `fix/` | Bug 修复 | `main` / `develop` | 源分支 |
| `docs/` | 文档 | `main` | `main` |
| `refactor/` | 重构 | `main` / `develop` | 源分支 |
| `test/` | 测试 | `main` | `main` |
| `chore/` | 工具/CI/杂项 | `main` | `main` |

### Special Branches

| Branch Pattern | Purpose |
|----------------|---------|
| `release/vMAJOR.MINOR.PATCH` | 发布准备分支（Git Flow） |
| `hotfix/vMAJOR.MINOR.PATCH` | 紧急修复分支 |
| `feat/42-add-login` | 功能分支（含 issue 编号） |
| `fix/87-npe-on-null` | 修复分支（含 issue 编号） |

## Branch Lifecycle

```
创建 feature 分支
    ↓
开发 + commits（遵循 Conventional Commits）
    ↓
提交 PR（使用 PR 模板）
    ↓
CI 自动运行（lint → test → build → coverage）
    ↓
Code review（CODEOWNERS 自动分配）
    ↓
合并（squash / merge commit）
    ↓
自动删除源分支
```

## Branch Protection Rules

在 GitHub Web UI 中配置（Settings > Branches > Add rule）：

### main 分支保护

| Rule | Value |
|------|-------|
| Require pull request reviews | 2 |
| Dismiss stale reviews | ✅ |
| Require review from Code Owners | ✅ |
| Require status checks | ci (lint, test, build, coverage) |
| Require branches up-to-date | ✅ |
| Require signed commits | ✅ |
| Include administrators | ✅ |
| Allow squash merging | ✅ |
| Allow auto-merge | ✅ |
| Do not allow bypass | ✅ |

### develop 分支保护（Git Flow）

| Rule | Value |
|------|-------|
| Require pull request reviews | 1 |
| Require status checks | ci (lint, test) |
| Allow squash merging | ✅ |
| Allow auto-merge | ✅ |

### release/* 分支保护（Git Flow）

| Rule | Value |
|------|-------|
| Require pull request reviews | 1 |
| Require status checks | ci (lint, test) |
| Allow merge commits | ✅ |
| Restrict deletions | ✅ |
