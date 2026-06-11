---
name: chinese-patent
description: |
  Full lifecycle orchestration for Chinese patent applications. Plans, generates figures,
  writes specification, reviews quality, and exports submission-ready DOCX. Use for
  end-to-end patent creation or any individual step: planning, figure drawing, writing,
  reviewing, or format conversion.
---

# 中国专利 (Chinese Patent Pipeline)

端到端的中国专利申请全流程编排，从发明构思到可提交的 docx 文件。支持单独调用任意子技能。

## 何时使用

- **全流程**：从发明想法直接生成可提交的专利 docx
- **仅规划**：分析发明、判定专利类型、生成撰写大纲
- **仅绘图**：生成符合中国专利规范的附图（中文标注、B&W）
- **仅撰写**：根据规划生成完整的说明书 HTML
- **仅审阅**：审查已有专利稿的合规性与质量
- **仅导出**：将 HTML 说明书转换为 docx/pdf
- **关键词**：写专利、专利申请、专利撰写、专利审阅、专利附图、导出docx

## 快速分发

| 用户意图 | 子技能 |
|---------|--------|
| 分析发明，确定专利类型，生成撰写计划 | [chinese-patent-plan](chinese-patent-plan/SKILL.md) |
| 绘制专利附图（中文标注，B&W） | [chinese-patent-drawer](chinese-patent-drawer/SKILL.md) |
| 撰写完整的专利说明书 HTML | [chinese-patent-writer](chinese-patent-writer/SKILL.md) |
| 审阅/检查专利稿合规性 | [chinese-patent-review](chinese-patent-review/SKILL.md) |
| 将说明书 HTML 导出为提交用 docx | 直接执行 `python scripts/html_to_docx.py` |
| 从头到尾生成可提交的专利 | 全流程执行（见下方） |

## 全流程工作流

```
用户输入（发明构思）
        │
        ▼
┌─────────────────────────────┐
│ Step 1: 专利规划             │
│ chinese-patent-plan/SKILL.md │
│ 输出：专利规划文档            │
│ 🚧 门禁：类型明确、≥1个独权  │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Step 2: 附图绘制             │
│ chinese-patent-drawer/SKILL.md│
│ 输出：images/图N.png         │
│ 🚧 门禁：全部生成、路径有效  │
│         B&W、中文验证        │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Step 3: 说明书撰写           │
│ chinese-patent-writer/SKILL.md│
│ 输出：说明书.html             │
│ 🚧 门禁：七大章节齐全        │
│         图文引用一致         │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Step 4: 质量审阅             │
│ chinese-patent-review/SKILL.md│
│ 输出：审阅报告               │
│ 🚧 门禁：无「必须改」问题    │
│         有则返回 Step 3 修复 │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Step 5: 导出 DOCX            │
│ python scripts/html_to_docx.py│
│  说明书.html -o 说明书.docx  │
│ 输出：可提交的 .docx 文件    │
└─────────────────────────────┘
```

### 门禁规则

- **Step 1 → 2**：专利类型已确定，权利要求结构已明确，附图清单完整
- **Step 2 → 3**：所有附图已生成并保存至 `images/`，文件名与清单一致，中文验证通过
- **Step 3 → 4**：HTML 文件包含全部七大章节，图片引用使用本地路径，数学公式使用 LaTeX
- **Step 4 → 5**：审阅报告中无「必须改」问题，所有严重问题已修复

用户可在任意步骤进入流程。例如，已有专利稿的用户可直接跳到 Step 4 审阅。

## 共享规则

所有子技能共用以下规则文件：

| 规则文件 | 内容 |
|---------|------|
| [rules/patent-type-guide.md](rules/patent-type-guide.md) | 专利类型判定决策树（发明/实用新型/外观设计） |
| [rules/writing-rules.md](rules/writing-rules.md) | 说明书撰写标准、结构规范、用语要求、HTML 格式 |
| [rules/review-checklist.md](rules/review-checklist.md) | 审阅维度、常见错误表、严重级别 |
| [rules/drawing-rules.md](rules/drawing-rules.md) | 附图绘制规则（中文文本、B&W、尺寸、字体） |

## 资源索引

| 资源 | 路径 | 用途 |
|------|------|------|
| 详细参考 | [reference.md](reference.md) | 全面的专利撰写参考文档 |
| HTML 模板 | [templates/patent_spec_template.html](templates/patent_spec_template.html) | 空白说明书 HTML 模板 |
| 参考示例 | [templates/reference-patent-example.html](templates/reference-patent-example.html) | 完整的示例专利（AI 学习参考） |
| Draw.io 子技能 | [drawio/SKILL.md](drawio/SKILL.md) | 结构图/流程图绘制（含中文专利规范） |
| DOCX 导出脚本 | [scripts/html_to_docx.py](scripts/html_to_docx.py) | HTML → DOCX（需 pandoc） |
| PDF 导出脚本 | [scripts/html_to_pdf.py](scripts/html_to_pdf.py) | HTML → PDF（需 Playwright） |
| 绘图示例脚本 | [scripts/generate_figure_example.py](scripts/generate_figure_example.py) | Matplotlib 框图生成示例 |
| Omnidraw 路由 | [../omnidraw/SKILL.md](../omnidraw/SKILL.md) | 绘图工具分发中枢（Drawer 引用） |

## 使用示例

### 全流程：从想法到 docx
```
用户：我有一个关于智能路灯节能控制的发明想法，帮我写一份专利申请。

→ 自动执行全流程：
  1. chinese-patent-plan：分析发明，判定为发明专利，输出规划文档
  2. 用户确认规划 → chinese-patent-drawer：生成系统架构图和方法流程图
  3. chinese-patent-writer：基于规划和附图生成说明书.html
  4. chinese-patent-review：审阅说明书，给出通过/修改建议
  5. 修复问题后 → python scripts/html_to_docx.py 说明书.html -o 说明书.docx
```

### 独立步骤：仅审阅已有专利稿
```
用户：帮我审阅这份专利说明书，看看有什么问题。

→ 直接调用 chinese-patent-review：
  1. 读取用户提供的 HTML 文件
  2. 按 review-checklist 逐项检查
  3. 输出分级审阅报告
```

### 独立步骤：仅画专利附图
```
用户：帮我画两张专利附图，一张系统结构图，一张方法流程图。

→ 直接调用 chinese-patent-drawer：
  1. 结构图 → drawio（A-H 格式，中文标注，B&W）
  2. 流程图 → drawio（A-H 格式，中文标注，B&W）
  3. 保存为 images/图1.png, images/图2.png
```
