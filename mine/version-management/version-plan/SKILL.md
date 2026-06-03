---
name: version-plan
description: |
  Plan phase for version management. Takes a natural-language requirement and
  produces a structured ROADMAP.md and task-tracking TODO.md. Designed to be
  referenced by pipeline orchestrators or composed into other skills.
---

# Version Plan

## 工作流

1. **理解需求** — 分析用户输入的需求描述
2. **任务拆解** — 将需求拆解为最小可执行单元
3. **分支命名** — 为每个任务分配分支名（feat/xxx, fix/xxx, ...）
4. **依赖分析** — 识别任务间的依赖关系，构建 DAG
5. **文件生成** — 写入 `ROADMAP.md` + `TODO.md`

---

## 任务拆解原则

### 单一职责

每个任务应该：
- 只做一件事（单一职责）
- 可在单次 session 内完成（5-30 分钟）
- 产出一个可提交的变更

### 依赖识别

| 依赖类型 | 说明 | 示例 |
|---------|------|------|
| 前置依赖 | B 必须在 A 之后执行 | 先建表 → 再写 API |
| 数据依赖 | B 依赖 A 的输出 | 先定义类型 → 再写实现 |
| 并行独立 | A 和 B 无关联 | 登录 API + 注册 API 可并行 |

### 复杂度评估

| 级别 | 预估时间 | 说明 |
|------|---------|------|
| S | < 10 min | 单一文件修改 |
| M | 10-30 min | 多文件，单一模块 |
| L | 30-60 min | 跨模块，需拆分为子任务 |

---

## 分支命名规范

```
<type>/<kebab-description>
```

| Type | 用途 | 何时使用 |
|------|------|---------|
| feat/ | 新功能、新特性 | 添加用户模型、新增 API |
| fix/ | Bug 修复 | 修复空指针、修复样式问题 |
| docs/ | 文档变更 | 更新 README、添加注释 |
| refactor/ | 重构 | 重命名、提取公共代码 |
| test/ | 测试 | 添加测试用例 |
| chore/ | 杂项 | 更新依赖、配置变更 |

示例：
- `feat/user-model`
- `feat/jwt-auth-middleware`
- `fix/npe-on-empty-result`
- `docs/api-usage-guide`

---

## 输出文件格式

### ROADMAP.md

```markdown
# Version Roadmap

生成时间: <ISO 8601 时间戳>
需求来源: <用户需求摘要>
分支基准: <base branch，默认 main>

## 总体目标

<1-3 句话描述本次版本管理的总体目标>

## 任务分解

| # | 任务 | 分支 | 依赖 | 复杂度 | 描述 |
|---|------|------|------|--------|------|
| 1 | <任务名> | feat/xxx | - | S | <简要描述> |
| 2 | <任务名> | fix/xxx | 1 | M | <简要描述> |

## 执行顺序

- Level 0: 任务 1, 3（无依赖）
- Level 1: 任务 2（依赖 1）
- Level 2: 任务 4（依赖 2, 3）
```

### TODO.md

```markdown
# TODO

| # | 任务 | 分支 | 状态 | 备注 |
|---|------|------|------|------|
| 1 | <任务名> | feat/xxx | pending | |
| 2 | <任务名> | fix/xxx | pending | |

状态流转: pending → in_progress → completed | blocked
```

> **文件位置**：默认写入项目根目录。如果 `docs/` 目录存在且需求中包含"文档"类任务，优先写入 `docs/`。

---

## 与 `references/composition-guide.md` 配合

当本组件作为模板被其他 Skill 集成时：

1. 其他 Skill 在其工作流中引用本 SKILL.md
2. 本组件输出的 `ROADMAP.md` + `TODO.md` 作为下游 `version-execute` 的输入
3. 输出文件的路径应传递给 pipeline 的下一阶段

---

## 使用示例

```markdown
Agent 读取 version-plan/SKILL.md：

1. 用户需求: "添加 JWT 用户认证系统"
2. 拆解任务:
   - Task 1: 用户实体模型  → feat/user-entity      (Level 0)
   - Task 2: JWT 工具类     → feat/jwt-utils         (Level 0)
   - Task 3: 登录 API       → feat/login-api         (依赖 Task 1, 2 → Level 1)
   - Task 4: 注册 API       → feat/register-api      (依赖 Task 1 → Level 1)
3. 写入 ROADMAP.md + TODO.md
```
