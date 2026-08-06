# Agent Instructions for Auto-Research

## 核心流程（4 阶段）

### Plan 前置规则

在执行任何计划类步骤前，先直接调用 `grill-me`，逐项追问并压力测试计划，直到研究目标、假设、约束、方法、产出和验收标准达成共识。该规则适用于 `research-plan`、`experiment-plan`、`paper-plan` 以及其他 `*-plan` 步骤；`grill-me` 也可以在流程的任意阶段单独调用。

### Phase 1: Discover
文献调研 → 想法生成 → 新颖性检查

0. 调用 `grill-me`，明确研究计划后再开始本阶段
1. 使用 `aris/research-lit "query"` 进行文献检索和综述
2. 使用 `aris/idea-discovery "brief"` 生成研究想法
3. 使用 `aris/novelty-check` 进行新颖性验证
4. 产出：研究纲要 + 新颖性报告

### Phase 2: Produce
实验规划 → 实验执行 → 结果分析

1. 使用 `aris/experiment-bridge` 将想法转化为实验方案
2. 先调用 `grill-me`，再使用 `aris/experiment-plan` 制定详细的实验计划
3. 使用 `aris/run-experiment` 执行实验
4. 使用 `aris/analyze-results` 分析实验结果
5. 产出：实验结果 + 图表数据

### Phase 3: Review
论文写作 → 版本管理 → 自动评审 → 迭代改进

1. 先调用 `grill-me`，再使用 `aris/paper-plan` 生成论文大纲
2. 使用 `aris/paper-write` 撰写论文草稿
3. 使用 `mine/paper-version-manager init` 初始化版本追踪（v1）
4. 使用 `aris/auto-review-loop` 启动自动评审循环（最多 4 轮）
5. 根据评审意见修改论文
6. 使用 `mine/paper-version-manager bump --minor` 标记修改（v1 → v1.1 等）
7. 重复步骤 4-6 直到评审收敛（每轮评审后 bump --minor）
8. 使用 `mine/paperreview-ai-review` 提交 paperreview.ai 外部评审
9. 使用 `aris/paper-claim-audit` 校验数值声明一致性
10. 使用 `aris/citation-audit` 校验引用
11. 对于重大改写使用 `mine/paper-version-manager bump --major`
12. 使用 `aris/auto-paper-improvement-loop` 深度改进论文
13. 产出：评审意见 + 改进清单 + 版本历史

### Phase 4: Polish
图表生成 → 论文编译 → 终稿

1. 使用 `aris/figure-spec "desc"` 生成确定性图表（架构图/工作流图）
2. 使用 `aris/paper-illustration "desc"` 生成 AI 插图
3. 使用 `aris/paper-compile` 编译终稿
4. 产出：定稿论文 + 图表

### Phase 5: Export
论文导出 → 打包 → 投稿 ZIP

1. 使用 `mine/export-paper-zip "path" --mode submission --venue <venue>` 导出投稿 ZIP
2. 或使用 `mine/export-paper-zip "path" --mode bundle --include <files...>` 自定义打包
3. 产出：`paper-submission_<venue>_YYYYMMDD.zip` + 记录到 MANIFEST.md

## Subagent Dispatch

| Agent | When | Responsibility |
|-------|------|----------------|
| lit-reviewer | Phase 1 | 文献调研和综述 |
| idea-generator | Phase 1 | 研究想法生成 |
| experiment-designer | Phase 2 | 实验方案设计 |
| paper-reviewer | Phase 3 | 自动评审（调用 auto-review-loop） |
| figure-designer | Phase 4 | 图表规格和生成 |
| citation-auditor | Phase 3 | 引用校验 |
| version-manager | Phase 3 | 版本追踪和变更记录 |

## Output Manifest 协议

- 每个阶段产出记录到 `MANIFEST.md`
- 格式：`| Timestamp | Skill | File | Stage | Description |`
- 阶段值：`idea-discovery` / `implementation` / `review` / `paper` / `version`
- 文件版本化：带时间戳副本 + 固定名称最新副本并存；使用 `mine/paper-version-manager` 管理论文版本历史

## 评审者独立性协议

- 评审者必须从原始论文草稿直接形成评估意见
- 执行者不得在评审前预先消化或总结论文内容
- 每轮评审使用独立会话（fresh review threads）
- 不同轮次之间不共享上下文
