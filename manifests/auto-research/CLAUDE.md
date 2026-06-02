# Auto-Research Manifest

面向自动化学术研究的 manifest 包。整合 aris（研究编排框架）、paperreview（自动论文评审）、autofigure（自动图表生成）三条能力线。

## Commands

| Command | Description |
|---------|-------------|
| `aris/research-pipeline "topic"` | 端到端研究流水线 |
| `aris/auto-review-loop "paper"` | 自动论文评审循环 |
| `aris/auto-paper-improvement-loop` | 自动论文改进循环 |
| `aris/figure-spec "description"` | 生成确定性图表 (JSON→SVG) |
| `aris/paper-illustration "desc"` | AI 论文插图生成 |
| `aris/paper-figure "results"` | 数据驱动图表生成 |
| `aris/rebuttal "reviews"` | 自动生成审稿回复 |
| `mine/paperreview-ai-review "paper.pdf"` | paperreview.ai 自动论文评审 |
| `aris/research-lit "query"` | 文献调研与综述 |
| `aris/citation-audit` | 引用校验 (DBLP/arXiv) |
| `aris/paper-claim-audit` | 数值声明校验 |
| `aris/experiment-bridge` | 实验桥接 |

## 仓库结构

```
auto-research/
├── references/
│   ├── research-lifecycle.md     # 自动化科研生命周期
│   ├── paper-review-guide.md     # 自动论文评审
│   ├── figure-generation.md      # 自动图表生成
│   └── integration-guide.md      # 三线集成
├── templates/
│   ├── RESEARCH_PLAN.md.example
│   ├── PAPER_OUTLINE.md.example
│   ├── REVIEW_RESPONSE.md.example
│   └── FIGURE_SPEC.md.example
├── scripts/
│   └── init-auto-research.sh
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── config.yml
│   │   ├── 01-research-idea.yml
│   │   ├── 02-paper-submission.yml
│   │   └── 03-figure-request.yml
│   └── workflows/
│       └── auto-research-ci.yml
├── CLAUDE.md
├── AGENTS.md
└── README.md
```

## 三条核心流水线

### 1. Research Pipeline
aris/research-pipeline 端到端：文献调研 → 想法生成 → 新颖性检查 → 实验计划 → 论文写作

### 2. Auto Review Loop
aris/auto-review-loop 四轮自主评审：论文草稿 → AI 评审 → 改进 → 再审 → 收敛

### 3. Auto Figure Pipeline
aris/figure-spec + aris/paper-illustration：图规格 (JSON) → 确定性 SVG → AI 精修 → 论文集成

## 关键文件

| File | Purpose |
|------|---------|
| `references/research-lifecycle.md` | 完整自动化科研流程说明 |
| `references/paper-review-guide.md` | 自动评审机制和评审者独立性协议 |
| `references/figure-generation.md` | 自动图表生成管线 |
| `references/integration-guide.md` | aris / paperreview / autofigure 集成方式 |
| `templates/RESEARCH_PLAN.md.example` | 研究计划模板 |
| `templates/PAPER_OUTLINE.md.example` | 论文大纲模板 |
| `templates/FIGURE_SPEC.md.example` | 图表规格模板 |

## Issues

- 研究想法提交 — 提交新的研究方向或课题
- 论文审阅 — 提交论文草稿请求 AI 评审
- 图表生成 — 提交图表生成请求

## Gotchas

- 评审者独立性：评审者必须从原始工件直接评估，执行者不可提前消化或总结
- 输出清单协议：每次输出后向 MANIFEST.md 追加一行（Timestamp / Skill / File / Stage / Description）
- 跨模型协议：建议执行者和评审者使用不同模型家族
- 文件版本化：每个产出需要带时间戳副本 + 固定名称最新副本
