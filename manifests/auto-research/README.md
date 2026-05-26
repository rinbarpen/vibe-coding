# Auto-Research Manifest

面向自动化学术研究的独立 manifest 包。

## 场景

整合四条 AI 驱动的研究自动化能力线：
- **aris** — 研究编排框架（文献调研、想法发现、实验规划、论文写作）
- **paperreview** — 自动论文评审（4 轮自主评审循环、数值声明校验、引用校验）
- **autofigure** — 自动图表生成（确定性 SVG 架构图、AI 插图、数据驱动图表）
- **ARS (Academic Research Skills)** — 深度研究 + 论文写作 + 多角色评审 + 端到端流水线

技能套件包含：

| 仓库 | 路径 | 版本 |
|------|------|------|
| [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | `skills/academic-research-skills/` | Claude Code 版 |
| [academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex) | `skills/academic-research-skills-codex/` | Codex CLI 版 |

ARS 提供 4 个核心技能：
- `ars/deep-research` — 13-agent 深度研究（7 种模式）
- `ars/academic-paper` — 12-agent 论文写作（10 种模式）
- `ars/academic-paper-reviewer` — 5 角色独立评审（6 种模式）
- `ars/academic-pipeline` — 10 阶段端到端流水线

## 使用方式

```bash
# 初始化到目标研究项目
./scripts/init-auto-research.sh /path/to/your/research-project
```

## 快速开始

1. 创建一个研究方向 issue
2. 选择流水线：`aris/research-pipeline "topic"`（aris）或 `ars/academic-pipeline "topic"`（ARS）
3. 论文草稿完成后运行 `aris/auto-review-loop` 或 `ars/academic-paper-reviewer` 获取评审意见
4. 使用 `aris/figure-spec` 生成论文图表
