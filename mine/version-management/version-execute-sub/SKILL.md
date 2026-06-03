---
name: version-execute-sub
description: |
  Sub-agent task executor for version management. Runs inside an isolated git
  worktree, creates a task-specific branch, implements, commits, and updates
  TODO.md. Designed to be invoked by version-execute via Agent(isolation:worktree).
---

# Version Execute Sub — Task Executor

## 概述

这是 version-management 的最小执行单元。它在**隔离的 git worktree** 中为单个任务创建分支、实现代码、提交变更、更新 TODO.md。

执行上下文：
- 由 `version-execute` 通过 `Agent(isolation: "worktree")` 启动
- 在一个全新的、与主工作区隔离的 git worktree 中运行
- 只负责一个任务，完成后自动退出

---

## 执行流程

### Step 1: 确认任务信息

从 agent prompt 中获取：

- 任务编号（Task #N）
- 分支名（如 `feat/user-model`）
- 任务描述
- TODO.md 路径（通常是项目根目录 `TODO.md`）
- ROADMAP.md 路径（可选，用于查看上下文）

### Step 2: 创建分支

当前已在 isolation worktree 中（HEAD 指向当前基准分支）：

```bash
# 创建并切换到任务分支
git checkout -b <branch-name>
# 示例: git checkout -b feat/user-model
```

分支命名已由 version-plan 在 ROADMAP.md 中定义，直接使用。

### Step 3: 实现任务

按照任务描述实现代码：

1. **读** — 阅读相关文件理解现有代码结构
2. **改** — 按需求修改或新增文件
3. **验** — 确保代码可运行（编译/语法正确）

不需要在该步骤执行完整 TDD（但如果有测试框架应该确保测试通过）。

### Step 4: 提交变更

遵循 Conventional Commits 格式：

```bash
git add <files>
git commit -m "<type>(<scope>): <description>"
```

示例：

```bash
git add src/models/user.ts
git commit -m "feat(model): add User entity with email and password fields"

# 或更短格式：
git commit -m "feat: add User entity"
```

### Step 5: 更新 TODO.md

退出 worktree 前，更新 TODO.md 中对应任务的状态：

```markdown
| N | <任务名> | <分支> | completed | <时间戳> <branch>: <文件数> files, +/-<行数> |
```

通过 Bash 或 Write 工具修改 TODO.md。如果 worktree 中有 TODO.md 的副本，确保写回主项目目录的版本。

### Step 6: 退出

worktree 代理会在完成后自动退出，无需额外操作。

---

## 提交规范

遵循 Conventional Commits，类型与分支命名对应：

| 分支前缀 | Commit Type | 示例 |
|---------|------------|------|
| feat/ | `feat:` | `feat: add user login API` |
| fix/ | `fix:` | `fix: handle null pointer in auth` |
| docs/ | `docs:` | `docs: update API usage guide` |
| refactor/ | `refactor:` | `refactor: extract auth middleware` |
| test/ | `test:` | `test: add auth unit tests` |
| chore/ | `chore:` | `chore: update dependencies` |

提交消息应简洁（一行式，< 72 字符），不包含 Co-Authored-By 行（项目已全局禁用）。

---

## 约束

- **不要修改** 非任务范围内的文件
- **不要创建** 多个分支 — 一个 sub-agent 只做一个任务
- **提交前** 确保代码无语法错误
- **更新 TODO.md** 是必须的最后一步
- **不要推送** 到远程 — 只需本地提交

---

## 使用示例

```markdown
Sub-agent 启动（由 version-execute 调度）:

1. 确认任务: #3 feat/login-api
2. git checkout -b feat/login-api
3. 实现 JWT 登录接口 (修改 src/auth/login.ts, 新增 src/auth/jwt.ts)
4. git add src/auth/ && git commit -m "feat: add JWT login API"
5. 更新 TODO.md: | 3 | JWT 登录 API | feat/login-api | completed | 2 files, +85 lines
6. 退出 worktree（自动）
```
