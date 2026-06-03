# Composition Guide — 为 Skill 添加 Version Management 能力

## 概述

本指南说明其他 SKILL.md 如何集成 version-management 模板，获得「需求 → 任务拆解 → 多 sub-agent 并行执行」的能力。

集成后，Skill 的工作流中会自动加入 Plan → Execute → Report 三个阶段，所有输出持久化为本地文件。

---

## 集成方式

### 方式 A：完整 Pipeline 集成（推荐）

在目标 Skill 的 SKILL.md 中声明依赖并串联全部三个阶段。

#### Step 1: 声明依赖

在 frontmatter 中添加 `dependencies`：

```yaml
---
name: my-skill
description: "我的 Skill，集成了版本管理能力"
dependencies:
  - mine/version-management
---
```

#### Step 2: 在 Workflow 中引用

在工作流节中添加 Pipeline 步骤：

```markdown
## 工作流

### 阶段 1: 规划
遵循 `mine/version-management/version-plan/SKILL.md`：
- 分析需求 → 拆解任务
- 生成 ROADMAP.md + TODO.md

### 阶段 2: 执行（含 Replan）
遵循 `mine/version-management/version-execute/SKILL.md`：
- 读取 TODO.md，按依赖 Level 分组
- 并行调度 sub-agent（每个任务一个 worktree）
- 每个 sub-agent 遵循 `mine/version-management/version-execute-sub/SKILL.md`
- **Replan Gate**: 每个 Level 完成后自动检查
  - 有 blocked 任务 → 遵循 `mine/version-management/version-replan/SKILL.md` 调整
  - 用户提出新需求 → 遵循 `mine/version-management/version-replan/SKILL.md` 追加

### 阶段 3: 报告
- 汇总任务完成状态
- 输出变更摘要
```

### 方式 B：选择性集成（灵活）

只使用 version-management 的部分组件。

#### 只用 Plan

```markdown
## 工作流

### 任务规划
遵循 `mine/version-management/version-plan/SKILL.md` 将需求拆解为任务列表，
输出 ROADMAP.md + TODO.md。后续执行由本 Skill 自行控制。
```

#### 只用 Execute

```markdown
## 执行策略
遵循 `mine/version-management/version-execute/SKILL.md` 的 sub-agent 调度策略，
将预定义的任务列表并行分发执行。
```

#### 集成 Replan

```markdown
## 执行中调整
- 遵循 `mine/version-management/version-replan/SKILL.md` 处理执行中失败的任务
- Replan 时机：每个 Level 完成后自动检查，或用户手动触发
- 支持场景：任务失败重分配、新增需求追加、任务描述变更
```

---

## 完整示例

### 示例：`mine/paper-reviewer-pro/SKILL.md`

```yaml
---
name: paper-reviewer-pro
description: "论文批量评审工具，集成 version-management 并行处理多篇论文"
dependencies:
  - mine/version-management
---
```

```markdown
# Paper Reviewer Pro

## 工作流

### 1. 规划阶段
遵循 `mine/version-management/version-plan/SKILL.md`：
- 输入：论文列表 + 评审标准
- 输出：ROADMAP.md（每篇论文一个任务）+ TODO.md
- 分支命名：`feat/review-paper-1`, `feat/review-paper-2`

### 2. 执行阶段
遵循 `mine/version-management/version-execute/SKILL.md`：
- 所有论文评审任务为 Level 0（无依赖），全部并行
- 每个 sub-agent 在独立 worktree 中处理一篇论文
- 每个 sub-agent 遵循 `mine/version-management/version-execute-sub/SKILL.md` 的流程
- Replan Gate：某篇论文下载失败 → 遵循 `version-replan/SKILL.md` 重试

### 3. 汇总阶段
- 收集所有评审结果
- 输出综合评审报告
```

---

## 集成检查清单

在将 version-management 集成到你的 Skill 后，检查：

- [ ] frontmatter 中添加了 `dependencies: [mine/version-management]`
- [ ] 工作流中的阶段明确引用对应 SKILL.md 文件
- [ ] 输出文件（ROADMAP.md, TODO.md）的路径已定义
- [ ] 任务拆解的粒度符合 version-plan 的规范
- [ ] Sub-agent 的 prompt 包含 version-execute-sub 的引用
- [ ] Replan 机制已集成（自动 Gate 或手动触发）
- [ ] 定义了 replan 触发场景（blocked / 新需求 / 变更）

---

## 常见问题

### Q: 集成后如何自定义任务拆分规则？

version-plan 的拆分规则是通用建议。你的 Skill 可以在工作流中补充额外的拆解要求，例如：

```markdown
遵循 `mine/version-management/version-plan/SKILL.md` 拆解任务，额外要求：
- 每篇论文评审作为一个独立任务
- 论文下载任务必须排在评审之前（有依赖）
```

### Q: 如何让 sub-agent 使用我 Skill 特有的逻辑？

Sub-agent 的 prompt 中除了引用 `version-execute-sub/SKILL.md`，还可以补充你的 Skill 特有的指令：

```markdown
Agent(
  prompt: """
  参照 version-execute-sub/SKILL.md 执行任务。
  此外，本任务特有的要求：
  - 使用 mine/paper-reviewer-pro/scripts/review.py 进行评审
  - 评审结果保存到 reviews/<paper-name>.md
  """
)
```

### Q: 并行数量有限制吗？

建议控制在 3-5 个并行 sub-agent。过多并行会影响上下文质量和稳定性。

### Q: 文件保存在哪里？

默认 ROADMAP.md + TODO.md 保存在项目根目录。可以在 pipeline 阶段通过参数指定路径。
