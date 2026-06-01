---
name: chinese-patent
description: |
  Comprehensive skill for Chinese patent specifications. Handles drafting, revising, and auditing/reviewing patent drafts. Supports HTML format with figures and outputs docx for filing. Use for writing new patents, rewriting existing ones, or reviewing drafts for compliance and quality.
---

# 中国专利 (Chinese Patent)

本技能提供中国专利说明书的完整生命周期支持，包括撰写、改写、审阅、复核以及格式转换（HTML 转 docx）。

## 何时使用

- **撰写/改写**：用户要求撰写新专利、改写已有专利稿、或需要处理带附图的发明/实用新型专利。
- **审阅/复核**：用户要求检查、审计、复核或审阅专利稿（说明书、权利要求书等）的质量与合规性。
- **关键词**：专利撰写、专利改写、专利审阅、专利复核、专利交底、附图说明、专利 docx、说明书审查。

---

## 1. 撰写与改写指南

### 说明书撰写结构
按以下顺序用 HTML 组织正文（与专利法/审查指南一致）：
1. **技术领域**：发明所属技术领域，简明说明涉及范围。
2. **背景技术**：现有技术现状及存在的问题、不足。
3. **发明内容**：要解决的技术问题、技术方案、有益效果。
4. **附图说明**：各附图的简要说明，与图片一一对应。
5. **具体实施方式**：结合附图对技术方案的具体描述。

### HTML 规范（便于转 docx）
- **标签**：使用语义化标签（`<h1>`~`<h3>`, `<p>`, `<ul>`/`<ol>`）。
- **表格**：使用 `<table class="patent-table" border="1">`，内容使用宋体。
- **图片路径**：必须使用本地路径（如 `images/图1.png`）。
- **图片图注**：使用 `<figure><img ... /><figcaption>图1 xxx</figcaption></figure>`，图注放在图片下方；图注不得写入图片像素。
- **数学表达**：正文数学表达使用 LaTeX（如 `\(...\)` 或 `$$...$$`），并通过 `scripts/html_to_docx.py` 导出可渲染的 Word 公式。
- **格式**：正文建议小四宋体，1.5 倍行距。

### 附图工作流（申请书推荐）
1. **原始需求整理**：先整理发明对象、模块、流程、输入输出。
2. **模型强化 prompt**：先由当前会话模型将原始需求改写为 A–H 结构化绘图规格（见 `drawio/references/structured-diagram-prompts.md`）。
3. **按图类型绘制**：
   - 结构图/关系图：使用 drawio（`drawio/SKILL.md`），图中文字统一 `15px`。
   - 数据图（曲线、统计图）：可使用 matplotlib，字号按可读性设置。
4. **插入说明书 HTML**：以 `figure+figcaption` 插入图片，编号格式统一为 `图1/图2/...`。
5. **导出 docx**：执行 `python scripts/html_to_docx.py 说明书.html -o 说明书.docx`。

### 申请书可用性（严格提交级）
提交前必须检查：
1. **结构完整**：技术领域、背景技术、发明内容、附图说明、具体实施方式、权利要求书、摘要齐全。
2. **术语一致**：说明书与权利要求书关键术语一致，无同义混用导致歧义。
3. **图文一致**：附图说明、正文引用、文件名（`图N`）一一对应。
4. **图注合规**：图注位于文档图片下方，格式为“图N xxx”，图内无图号/图题像素文字。
5. **数学可渲染**：LaTeX 表达在导出 docx 后应为可编辑公式对象，而非纯文本分隔符。

---

## 2. 审阅与复核指南

### 审阅维度（检查项）
1. **结构完整性**：各法定章节是否齐全，顺序是否正确。
2. **一致性**：说明书与权利要求书之间的术语、技术特征表述是否统一。
3. **附图对应性**：附图编号、说明与正文引用是否一一对应；图片路径是否正确。
4. **用语规范**：检查是否违反法律用语规范或存在常见错误（参考 `reference.md`）。
5. **实质性检查**：背景技术是否客观，具体实施方式是否充分支持权利要求。

### 输出格式
按维度列出问题，建议分级：
- **【必须改】**：影响授权或合规的严重问题。
- **【建议改】**：提升质量或减少审查意见的改进建议。

---

## 3. 附加资源

- **详细规范**：[reference.md](./reference.md)（含用语规范、常见错误速查）。
- **转换脚本**：[scripts/html_to_docx.py](./scripts/html_to_docx.py)。
- **绘图示例（数据图）**：[scripts/generate_figure_example.py](./scripts/generate_figure_example.py)。
- **drawio（结构图/关系图）**：[drawio/SKILL.md](./drawio/SKILL.md)。
- **空白模板**：[templates/patent_spec_template.html](./templates/patent_spec_template.html)。
