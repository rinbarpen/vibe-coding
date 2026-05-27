# Agent Instructions for Auto-Research (ARS)

## 核心流程

### 1. 深度研究 (deep-research)
选择模式启动深度研究：
```
ars/deep-research "research question" — 选择模式
模式: full / quick / paper-review / lit-review / fact-check / socratic / systematic-review
```

### 2. 论文写作 (academic-paper)
完成研究后进入论文写作：
```
ars/academic-paper "paper topic" — 选择模式
模式: full / plan / outline / revision / revision-coach / abstract / lit-review / format-convert / citation-check / disclosure
```

### 3. 论文评审 (academic-paper-reviewer)
论文草稿完成后提交评审：
```
ars/academic-paper-reviewer "paper" — 选择模式
模式: full / re-review / quick / methodology / socratic / calibration
```

### 4. 端到端流水线 (academic-pipeline)
一键执行全部阶段：
```
ars/academic-pipeline "research topic"
```
阶段序列：research → write → integrity check → review → revise → re-review → re-revise → final integrity → finalize

## Subagent Dispatch

| Agent | Phase | Responsibility |
|-------|-------|----------------|
| deep-researcher | 研究 | ARS 13-agent 深度研究团队 |
| paper-writer | 写作 | ARS 12-agent 论文写作管线 |
| reviewer | 评审 | ARS 5-role 独立评审 |
| pipeline-orchestrator | 全流程 | ARS 10-stage 流水线编排 |

## 模式选择指南

| 场景 | 推荐模式 |
|------|----------|
| 探索新方向 | deep-research socratic |
| 快速了解领域 | deep-research quick |
| 系统综述 | deep-research systematic-review |
| 从头写论文 | academic-paper full |
| 已有初稿需修改 | academic-paper revision |
| 投稿前评审 | academic-paper-reviewer full |
| 修改后验证 | academic-paper-reviewer re-review |

## Output 管理

- 每个阶段产出记录到 `MANIFEST.md`
- 文件版本化：带时间戳副本 + 固定名称最新副本并存
