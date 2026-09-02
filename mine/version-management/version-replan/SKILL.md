---
name: version-replan
description: |
  Replan phase for version management. Reads current TODO.md and ROADMAP.md,
  analyzes execution state (completed / pending / blocked), and adjusts remaining
  tasks. Handles blocked tasks, new requirements, and mid-execution changes.
  Designed to be called from the pipeline Replan Gate or manually by the user.
---

# Version Replan — Mid-Execution Replanning

## 概述

Version-Replan 负责在执行过程中动态调整计划。它不是全量重做，而是**增量修正**：保留已完成的 work，只调整 pending/blocked 及其依赖。

---

## 触发时机

| 触发场景 | 触发方式 | 示例 |
|---------|---------|------|
| Sub-agent 返回 blocked | 自动（Level 完成后） | 依赖库冲突，实现方案不可行 |
| 用户提出新需求 | 手动 | "再加一个日志功能" |
| 每个 Level 完成后 | 自动（Replan Gate） | 周期性审查，确保方向正确 |
| 用户主动调用 | 手动调用 | "replan" 或 /replan |

---

## 工作流

### Step 1: 读取当前状态

从 `TODO.md` 读取任务列表，识别每个任务的状态：

| # | 任务 | 分支 | 状态 | 备注 |
|---|------|------|------|------|
| 1 | 用户模型 | feat/user-model | completed | 3 files |
| 2 | 登录 API | feat/login-api | pending | |
| 3 | 权限中间件 | feat/auth-middleware | blocked | JWT 库版本冲突 |

### Step 2: 分析 & 决策

根据 TODO.md 状态和用户输入，执行对应策略：

| 场景 | 状态 | 处理方式 |
|------|------|---------|
| 任务 blocked 且可重试 | blocked | 重置为 `pending`，更新分支名或策略 |
| 任务 blocked 不可重试 | blocked | 标记为 `cancelled`，调整依赖任务 |
| 依赖任务被取消 | — | 依赖该任务的任务解除阻止或重新分配 |
| 用户新增需求 | new | 拆解为新任务，计算依赖，加入 TODO.md |
| 现有任务需变更 | pending | 更新任务描述或调整依赖 |
| 拆分大任务 | blocked/pending | 用一个或多个子任务替换原任务 |

### Step 3: 重新计算依赖

根据调整后的任务列表，重新计算执行顺序分组：

```
调整前:        调整后:
Level 0: T1     Level 0: T1 (已完成，跳过)
Level 1: T2, T3 Level 1: T2
               Level 2: T3a, T3b (从 T3 拆分)
               Level 3: T4 (新增)
```

### Step 4: 写入更新

1. 更新 `ROADMAP.md` — 新版本的时间戳、变更说明、调整后的任务分解
2. 更新 `TODO.md` — 保留已完成任务，更新 pending/blocked/new 任务

### Step 5: 返回

将更新后的 TODO.md 路径返回给调用方（version-execute 或 pipeline），继续执行。

---

## 决策树

```
读取 TODO.md + ROADMAP.md
    │
    ├─ 有 blocked 任务?
    │   ├─ 是 → 判断能否重试
    │   │   ├─ 可重试 → 重置为 pending，调整策略
    │   │   └─ 不可重试 → 标记 cancelled，调整依赖
    │   └─ 否 → 继续
    │
    ├─ 有新需求?
    │   ├─ 是 → 拆解为新任务，插入依赖图
    │   └─ 否 → 继续
    │
    ├─ 需变更?
    │   ├─ 是 → 更新对应任务描述
    │   └─ 否 → 继续
    │
    └─ 重新计算 Level → 写入更新
```

---

## Replan Gate（自动调用）

在每个 Level 完成后，version-execute 应自动检查是否需要 replan：

```
Level N 完成
    │
    ├─ 检查本 Level 所有任务状态
    │
    ├─ 全部 completed → 继续 Level N+1（不触发 replan）
    ├─ 有 blocked → 触发 version-replan，调整后继续
    │
    ├─ 询问用户是否有新需求
    │   ├─ 有 → 触发 version-replan，追加后继续
    │   └─ 无 → 继续
    │
    └─ 进入 Level N+1
```

---

## TODO.md 备注约定

Replan 更新时应保留原始任务备注，并在备注中附加 replan 日志：

```
| 1 | 用户模型 | feat/user-model | completed | 3 files |
| 2 | 登录 API | feat/login-api | pending | replan@10:30 调整了注册接口依赖 |
| 3 | 权限中间件 | feat/auth-middleware | cancelled | replan@10:30 JWT 版本冲突，拆分 T3a+T3b |
| 3a | 基础认证 | feat/auth-core | pending | replan@10:30 从 T3 拆分 |
| 3b | 权限中间件 v2 | feat/auth-middleware-v2 | pending | replan@10:30 从 T3 拆分 |
| 4 | 日志记录 | feat/request-logging | pending | replan@10:32 用户新增需求 |
```

---

## 与 `version-execute` 的交互

1. version-execute 检测到 blocked → 调用 version-replan
2. version-replan 返回更新后的 TODO.md 路径
3. version-execute 重新读取 TODO.md，继续执行剩余 Level
4. 如果 replan 新增了已完成的 Level 中的依赖，version-execute 会重新调度该 Level

---

## 使用示例

```markdown
Agent 检测到 Task 3 返回 blocked（JWT 库版本冲突）:

1. 读取 TODO.md → Task 3 状态为 blocked
2. 分析: JWT 实现比预期复杂，拆分为基础认证 + 权限中间件两部分
3. 更新 ROADMAP.md: 添加 Task 3a, 3b
4. 更新 TODO.md: T3 cancelled, T3a+T3b pending
5. 返回 → version-execute 继续 Level 2
```
