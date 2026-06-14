---
name: omnisheet
description: Unified sheet/spreadsheet generation command center. Routes user requests to the right sub-skill based on scenario — financial models, data analysis, project management, personal life, business operations, academic research. Use when the user asks to create any kind of spreadsheet, Excel file, tracker, or tabular report. 一键生成各类场景的 Excel 表格，提供丰富的预设模板。
---

# Omnisheet

Routes sheet generation requests to the right sub-skill based on **what you need** and **what scenario you're in**.

## Sub-Skills

| Sub-Skill | Best For | Deps |
|-----------|----------|------|
| [financial](financial/SKILL.md) | Budgets, investment tracking, loan calculators, cash flow forecasts | openpyxl, pandas |
| [data-analysis](data-analysis/SKILL.md) | Sales reports, survey statistics, A/B tests, data cleaning | openpyxl, pandas |
| [project-management](project-management/SKILL.md) | Gantt timelines, task trackers, OKRs, risk registers | openpyxl |
| [personal-life](personal-life/SKILL.md) | Expense tracking, fitness plans, travel planners, habit trackers | openpyxl |
| [business-ops](business-ops/SKILL.md) | CRM, inventory, invoices, sales pipelines | openpyxl |
| [academic-research](academic-research/SKILL.md) | Experiment logs, literature matrices, grant budgets, thesis trackers | openpyxl, pandas |

## Scenario Dispatch

### 财务 / 金融
→ [financial](financial/SKILL.md) (预算、投资、贷款、现金流)

### 数据分析 / 报表
→ [data-analysis](data-analysis/SKILL.md) (销售、问卷、A/B、数据清洗)

### 项目管理
→ [project-management](project-management/SKILL.md) (甘特图、任务、OKR、风险)

### 个人生活
→ [personal-life](personal-life/SKILL.md) (记账、健身、旅行、打卡)

### 业务运营
→ [business-ops](business-ops/SKILL.md) (CRM、库存、发票、销售管道)

### 科研学术
→ [academic-research](academic-research/SKILL.md) (实验、文献、经费、论文)

### 简单表格 / 无特定场景
→ 直接使用 openpyxl/pandas 创建，参考 [style-guide](references/style-guide.md)

### 现有文件编辑 / 修复
→ 参考 [skills/anthropics/skills/xlsx](../../skills/anthropics/skills/xlsx/SKILL.md) 的编辑工作流

### Google Sheets 集成
→ 参考 [skills/ai-skills/skills/google-sheets](../../skills/ai-skills/skills/google-sheets/SKILL.md) (OAuth API)

## Routing Matrix

### Sheet Types

| Intent | Primary | Fallback |
|--------|---------|----------|
| Budget / expense tracker | [financial](financial/SKILL.md) | [personal-life](personal-life/SKILL.md) |
| Investment / portfolio | [financial](financial/SKILL.md) | [data-analysis](data-analysis/SKILL.md) |
| Loan / mortgage | [financial](financial/SKILL.md) | — |
| Cash flow forecast | [financial](financial/SKILL.md) | — |
| Sales report / dashboard | [data-analysis](data-analysis/SKILL.md) | [business-ops](business-ops/SKILL.md) |
| Survey / questionnaire | [data-analysis](data-analysis/SKILL.md) | — |
| A/B test analysis | [data-analysis](data-analysis/SKILL.md) | — |
| Data quality / cleaning | [data-analysis](data-analysis/SKILL.md) | — |
| Gantt chart | [project-management](project-management/SKILL.md) | — |
| Task / to-do tracker | [project-management](project-management/SKILL.md) | [personal-life](personal-life/SKILL.md) |
| OKR / goal tracking | [project-management](project-management/SKILL.md) | — |
| Risk register | [project-management](project-management/SKILL.md) | — |
| Personal finance | [personal-life](personal-life/SKILL.md) | [financial](financial/SKILL.md) |
| Fitness / meal plan | [personal-life](personal-life/SKILL.md) | — |
| Travel planner | [personal-life](personal-life/SKILL.md) | — |
| Habit tracker | [personal-life](personal-life/SKILL.md) | — |
| CRM / contacts | [business-ops](business-ops/SKILL.md) | — |
| Inventory / stock | [business-ops](business-ops/SKILL.md) | — |
| Invoice template | [business-ops](business-ops/SKILL.md) | — |
| Sales pipeline | [business-ops](business-ops/SKILL.md) | — |
| Experiment log | [academic-research](academic-research/SKILL.md) | [data-analysis](data-analysis/SKILL.md) |
| Literature review matrix | [academic-research](academic-research/SKILL.md) | — |
| Grant budget | [academic-research](academic-research/SKILL.md) | [financial](financial/SKILL.md) |
| Thesis / paper tracker | [academic-research](academic-research/SKILL.md) | [project-management](project-management/SKILL.md) |

## Multi-Tool Workflows

### Financial Analysis → Presentation
1. [financial](financial/SKILL.md) → generate financial model with `.xlsx`
2. [data-analysis](data-analysis/SKILL.md) → create summary charts from model data
3. Export charts to PPTX using pptx skill

### Data Cleaning → Report
1. [data-analysis](data-analysis/SKILL.md) → clean and validate raw data
2. [data-analysis](data-analysis/SKILL.md) → generate analysis report `.xlsx`
3. Optionally convert to PDF or embed in docx

### Project Plan → Executive Summary
1. [project-management](project-management/SKILL.md) → create Gantt + OKR sheets
2. [business-ops](business-ops/SKILL.md) → generate stakeholder summary
3. Export key sheets as PDF for distribution

### Research → Publication
1. [academic-research](academic-research/SKILL.md) → experiment log + literature matrix
2. [academic-research](academic-research/SKILL.md) → grant budget
3. Charts exportable to paper-quality figures via matplotlib

## Best Practices

1. **Scenario first** — 财务？科研？个人？场景决定模板选择。
2. **Formula-first** — Always use Excel formulas, never hardcode calculated values. Sheets must remain dynamic.
3. **Preset as starting point** — Copy a preset prompt, fill in your details, generate.
4. **Style matters** — Financial models use industry-standard color coding; academic sheets use clean minimal style.
5. **Recalculate** — After generating formulas, run `python scripts/recalc.py output.xlsx` to compute values.
6. **Single-sheet preferred** — Keep related data in one workbook with multiple sheets, not multiple files.
7. **Validate** — Spot-check 2-3 formula references before trusting the full model.

## Template Reference

- [references/style-guide.md](references/style-guide.md) — Color palettes, fonts, formatting standards per scenario
- [skills/anthropics/skills/xlsx](../../skills/anthropics/skills/xlsx/SKILL.md) — openpyxl + pandas usage, recalc script
- [skills/ai-skills/skills/google-sheets](../../skills/ai-skills/skills/google-sheets/SKILL.md) — Google Sheets API integration
