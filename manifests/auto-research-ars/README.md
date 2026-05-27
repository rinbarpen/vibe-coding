# Auto-Research ARS Manifest

基于 Academic Research Skills (ARS) 的自动科研 manifest 包。

## 场景

提供四套 ARS 核心技能：
- **deep-research** — 13-agent 深度研究，7 种模式
- **academic-paper** — 12-agent 论文写作，10 种模式
- **academic-paper-reviewer** — 5 角色独立评审，6 种模式
- **academic-pipeline** — 10 阶段端到端流水线

## 使用方式

```bash
# 初始化到目标研究项目
./scripts/init-auto-research-ars.sh /path/to/your/research-project
```

## 快速开始

1. 研究：`ars/deep-research "research topic"`
2. 写作：`ars/academic-paper "paper title"`
3. 评审：`ars/academic-paper-reviewer "paper"`
4. 一键全流程：`ars/academic-pipeline "topic"`
