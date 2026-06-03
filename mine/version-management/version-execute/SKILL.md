---
name: version-execute
description: |
  Execute phase for version management. Reads TODO.md, resolves dependency
  levels, and spawns parallel version-execute-sub agents in isolated git
  worktrees. Designed to be composed into pipeline orchestrators or other skills.
---

# Version Execute

## 概述

Version-Execute 负责将 `TODO.md` 中的任务按依赖关系调度执行。核心策略：

- **同 Level 无依赖的任务** → 通过 `Agent(run_in_background, isolation: "worktree")` **并行**执行
- **跨 Level 有依赖的任务** → **串行**等待前置 Level 完成后执行
- **任务失败** → 标记 `blocked`，不影响同 Level 其他任务

---

## 工作流

### Step 1: 读取任务

1. 读取 `TODO.md` 解析任务列表
2. 从 `ROADMAP.md` 解析执行顺序（Level 分组）

### Step 2: 按依赖 Level 分组

从 ROADMAP.md 的「执行顺序」段提取：

```
Level 0: 任务 1, 3    ← 无依赖，可并行
Level 1: 任务 2       ← 依赖 Level 0
Level 2: 任务 4       ← 依赖 Level 1
```

### Step 3: 逐 Level 调度

对于每个 Level：

1. **更新 TODO.md** — 将该 Level 所有任务标记为 `in_progress`
2. **并行启动** — 对每个任务启动一个 sub-agent：
   ```
   Agent(
     description: "Execute task <N>: <name>",
     prompt: "参照 version-execute-sub/SKILL.md，执行任务 <N>..."
     isolation: "worktree",    # 每个 sub-agent 在独立 worktree 中
     run_in_background: true   # 并行执行
   )
   ```
3. **等待完成** — 等待所有 sub-agent 返回
4. **更新 TODO.md** — 根据 sub-agent 返回结果更新状态

### Step 4: 处理并行结果

| Sub-agent 返回 | TODO.md 更新 | 后续处理 |
|---------------|-------------|---------|
| 成功 | `completed` | 继续下一个 Level |
| 失败 | `blocked` + 备注 | 继续（不影响其他任务） |
| 部分完成 | `blocked` + 备注 | 手动恢复 |

### Step 5: 合并分支

所有 Level 执行完毕后：

1. 确认所有任务状态（无 pending）
2. 列出所有创建的分支
3. 如果需要，切换回 base branch 进行合并
4. 更新 TODO.md 添加完成时间戳

---

## Sub-agent 调度模板

每个 sub-agent 的 prompt 应包含：

```markdown
请参照 `mine/version-management/version-execute-sub/SKILL.md` 执行以下任务：

## 任务信息
- 任务 #N: <任务名称>
- 分支: <分支名>
- 描述: <任务描述>

## 执行要求
1. 读取 version-execute-sub/SKILL.md 了解执行流程
2. 在 worktree 中创建分支并实现
3. 提交变更（遵循 Conventional Commits）
4. 更新 TODO.md 标记任务完成

## 技术背景
<如果有前置任务，补充上下文信息>
```

---

## 错误处理策略

| 场景 | 处理方式 |
|------|---------|
| Sub-agent 超时 | 标记为 `blocked`，备注"超时"，继续下一个任务 |
| Worktree 创建失败 | 重试 1 次，失败则标记 `blocked` |
| 分支冲突 | 标记 `blocked`，备注冲突原因，留给手动处理 |
| Git 提交失败 | 捕获错误信息，标记 `blocked` + 错误详情 |

---

## TODO.md 更新规范

Sub-agent 执行前后应及时更新 TODO.md：

### 状态变更规则

| 变更 | 条件 | 执行者 |
|------|------|--------|
| pending → in_progress | Level 开始执行时 | version-execute 或 sub-agent |
| in_progress → completed | 任务提交成功 | sub-agent |
| in_progress → blocked | 执行失败 | sub-agent 或 version-execute |

### 更新格式

```markdown
| N | <任务名> | <分支> | completed | 2026-06-02T10:30 feat/user-model: 3 files, +120 lines |
| N | <任务名> | <分支> | blocked | JWT 库版本冲突，需手动解决 |
```

---

## 使用示例

```markdown
Agent 读取 version-execute/SKILL.md：

1. 读取 TODO.md:
   - Task 1: feat/user-entity (Level 0, pending)
   - Task 2: feat/jwt-utils (Level 0, pending)
   - Task 3: feat/login-api (Level 1, pending)

2. Level 0 → 并行启动 sub-agent 1 + 2
3. 等待 → Task 1 completed, Task 2 completed
4. Level 1 → 启动 sub-agent 3
5. 等待 → Task 3 completed
6. 全部完成 → 报告
```
