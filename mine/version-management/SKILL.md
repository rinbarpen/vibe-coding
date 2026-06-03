---
name: version-management
description: |
  Template skill for version management — decompose requirements into a roadmap,
  create feat/fix/xx branches, execute tasks via parallel sub-agents in isolated
  git worktrees. Works standalone or as a composable template for other skills.
---

# Version Management — Template Skill

## 概述

Version Management 是一个**可组合的模板技能**。它可以：

1. **独立使用** — 作为完整的 pipeline：需求 → ROADMAP.md + TODO.md → 多 sub-agent 并行执行
2. **作为模板集成** — 其他 Skill 通过 `dependencies` 引用，获得版本管理能力

核心流程：**Plan → Execute (with Replan Gate) → Verify → Report**，所有状态持久化为本地文件（ROADMAP.md / TODO.md）。

---

## 架构组件

```
version-management/
├── SKILL.md                    # [模板入口 + Pipeline 编排器]
├── version-plan/               # [Plan 阶段] 需求分析 → ROADMAP.md + TODO.md
├── version-replan/             # [Replan 阶段] 执行中动态修正
├── version-execute/            # [Execute 阶段] 按依赖层级调度 sub-agent
├── version-execute-sub/        # [Sub-agent] 单任务在隔离 worktree 中执行
└── references/
    └── composition-guide.md    # [集成指南] 如何将本模板组合到其他 Skill
```

### 组件职责

| 组件 | 输入 | 输出 | 关键行为 |
|------|------|------|---------|
| `pipeline` | 需求描述 | 完成状态报告 | 编排 Plan → Execute(含 Replan Gate) → Report |
| `version-plan` | 需求描述 | `ROADMAP.md` + `TODO.md` | 任务拆解、依赖分析、分支命名 |
| `version-replan` | `TODO.md` + 场景 | 更新后的 `ROADMAP.md` + `TODO.md` | 执行中动态调整：处理 blocked、新需求、任务变更 |
| `version-execute` | `TODO.md` 路径 | 更新后的 `TODO.md` | 按依赖 Level 分组，并行/串行调度 sub-agent，含 Replan Gate |
| `version-execute-sub` | 单个任务描述 | 提交的 commit | `EnterWorktree` → 建分支 → 实现 → 提交 → 退出 |

---

## 使用模式

### 模式 1：独立运行

直接调用本 skill，输入需求 → 完成执行：

```
User: "实现用户登录和权限管理"

Agent 读取 version-management/SKILL.md:
  └─ 调用 version-plan:  需求 → ROADMAP.md + TODO.md
  └─ 调用 version-execute: 逐 Level 调度 sub-agents
      └─ Replan Gate: 每个 Level 完成后检查 blocked / 新需求
  └─ 报告完成状态
```

### 模式 2：作为模板被其他 Skill 集成

其他 Skill 在其 SKILL.md 的 `dependencies` 中声明：

```yaml
---
name: my-skill
description: "使用 version-management 模板的示例 skill"
dependencies:
  - mine/version-management
---
```

然后在工作流中引用本模板的组件：

```markdown
## 工作流

### 1. 规划阶段
遵循 `mine/version-management/version-plan/SKILL.md` 将需求拆解为任务。

### 2. 执行阶段
遵循 `mine/version-management/version-execute/SKILL.md` 按依赖层级并行执行。

### 3. 子任务
遵循 `mine/version-management/version-execute-sub/SKILL.md` 在 worktree 中执行。
```

详见 `references/composition-guide.md`。

---

## Pipeline 工作流

### Step 1: Plan

1. 收集用户需求描述
2. 读取 `version-plan/SKILL.md` 并执行：
   - 分析需求 → 任务拆解
   - 分支命名（feat/xxx, fix/xxx, docs/xxx, refactor/xxx）
   - 识别任务依赖关系
   - 写入 `ROADMAP.md` + `TODO.md`

### Step 2: Execute

1. 读取 `version-execute/SKILL.md` 并执行：
   - 解析 `TODO.md` 任务列表
   - 按依赖分组（Level 0 → Level 1 → ...）
   - 同 Level 任务 → `Agent(isolation: "worktree", run_in_background)` 并行调度
   - 每个 sub-agent 读取 `version-execute-sub/SKILL.md`
   - 等待完成 → 更新 TODO.md
   - **Replan Gate**: 检查 blocked 任务或询问用户新需求
     - 有 blocked → 读取 `version-replan/SKILL.md` 调整
     - 有新需求 → 读取 `version-replan/SKILL.md` 追加
   - 下一 Level ...
   - 全部完成后合并分支

### Step 3: Verify & Report

- 验证 TODO.md 中没有 pending 或 blocked 任务
- 汇总每个任务的完成状态和分支
- 输出最终报告

---

## 输出文件

### ROADMAP.md

生成位置：项目根目录 `ROADMAP.md`（或 `docs/roadmap-<timestamp>.md`）

```markdown
# Version Roadmap

生成时间: 2026-06-02T10:00
需求来源: <requirement>

## 任务分解

| # | 任务 | 分支 | 依赖 | 复杂度 | 描述 |
|---|------|------|------|--------|------|
| 1 | 用户模型 | feat/user-model | - | M | 创建 User 表和 ORM 模型 |
| 2 | 登录 API | feat/login-api | 1 | M | JWT 登录接口 |

## 执行顺序
- Level 0: 任务 1
- Level 1: 任务 2（依赖任务 1）
```

### TODO.md

生成位置：项目根目录 `TODO.md`

```markdown
# TODO

| # | 任务 | 分支 | 状态 | 备注 |
|---|------|------|------|------|
| 1 | 用户模型 | feat/user-model | pending | |
| 2 | 登录 API | feat/login-api | pending | |

状态流转: pending → in_progress → completed | blocked
```

---

## 规范与约束

### 分支命名

遵循 `<type>/<kebab-description>` 格式：

| Type | 用途 | 示例 |
|------|------|------|
| feat/ | 新功能 | feat/user-login |
| fix/ | Bug 修复 | fix/npe-on-null |
| docs/ | 文档 | docs/api-spec |
| refactor/ | 重构 | refactor/auth-flow |

### 依赖层级

- Level 0: 无依赖的任务，可完全并行
- Level N: 依赖 Level 0..N-1 的任务，等待前置完成后执行

### 任务粒度

- 每个任务应在单次 session 内可完成（~5-30 分钟）
- 一个 worktree 执行一个任务，创建独立分支
- 过大任务应拆分为子任务

---

## 快速开始

```markdown
User: "添加用户注册和登录功能"
Agent: [参照本 SKILL.md 执行完整 pipeline]
1. Plan → 拆解为 3 个任务写入 ROADMAP.md + TODO.md
2. Execute → Level 0: 用户模型；Level 1: 注册 API + 登录 API（并行）
   Replan Gate → 检查无误，继续
3. Report → 3 个任务完成，3 个分支已提交
```
