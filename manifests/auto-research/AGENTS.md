# Agent Instructions for Auto-Research

## 核心流程（4 阶段）

### Phase 1: Discover
文献调研 → 想法生成 → 新颖性检查

1. 使用 `aris/research-lit "query"` 进行文献检索和综述
2. 使用 `aris/idea-discovery "brief"` 生成研究想法
3. 使用 `aris/novelty-check` 进行新颖性验证
4. 产出：研究纲要 + 新颖性报告

### Phase 2: Produce
实验规划 → 实验执行 → 结果分析

1. 使用 `aris/experiment-bridge` 将想法转化为实验方案
2. 使用 `aris/experiment-plan` 制定详细的实验计划
3. 使用 `aris/run-experiment` 执行实验
4. 使用 `aris/analyze-results` 分析实验结果
5. 产出：实验结果 + 图表数据

### Phase 3: Review
论文写作 → 自动评审 → 反驳/修改

1. 使用 `aris/paper-plan` 生成论文大纲
2. 使用 `aris/paper-write` 撰写论文草稿
3. 使用 `aris/auto-review-loop` 启动自动评审循环（最多 4 轮）
4. 使用 `aris/paper-claim-audit` 校验数值声明一致性
5. 使用 `aris/citation-audit` 校验引用
6. 使用 `aris/auto-paper-improvement-loop` 改进论文
7. 产出：评审意见 + 改进清单

### Phase 4: Polish
图表生成 → 论文编译 → 终稿

1. 使用 `aris/figure-spec "desc"` 生成确定性图表（架构图/工作流图）
2. 使用 `aris/paper-illustration "desc"` 生成 AI 插图
3. 使用 `aris/paper-compile` 编译终稿
4. 产出：定稿论文 + 图表

## Subagent Dispatch

| Agent | When | Responsibility |
|-------|------|----------------|
| lit-reviewer | Phase 1 | 文献调研和综述 |
| idea-generator | Phase 1 | 研究想法生成 |
| experiment-designer | Phase 2 | 实验方案设计 |
| paper-reviewer | Phase 3 | 自动评审（调用 auto-review-loop） |
| figure-designer | Phase 4 | 图表规格和生成 |
| citation-auditor | Phase 3 | 引用校验 |

## Output Manifest 协议

- 每个阶段产出记录到 `MANIFEST.md`
- 格式：`| Timestamp | Skill | File | Stage | Description |`
- 阶段值：`idea-discovery` / `implementation` / `review` / `paper`
- 文件版本化：带时间戳副本 + 固定名称最新副本并存

## 评审者独立性协议

- 评审者必须从原始论文草稿直接形成评估意见
- 执行者不得在评审前预先消化或总结论文内容
- 每轮评审使用独立会话（fresh review threads）
- 不同轮次之间不共享上下文
