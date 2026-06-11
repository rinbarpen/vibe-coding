---
name: chinese-patent-writer
description: |
  Generates full Chinese patent specification in HTML format, following legal structure
  (技术领域, 背景技术, 发明内容, 附图说明, 具体实施方式, 权利要求书, 摘要).
  Output ready for DOCX conversion via scripts/html_to_docx.py.
---

# 中国专利撰写 (Chinese Patent Writer)

根据专利规划生成完整的专利说明书 HTML 文件，可直接通过 `scripts/html_to_docx.py` 导出为提交用 docx。

## 何时使用

- 用户要求：撰写专利说明书、生成专利 HTML、写专利正文
- 前提条件：需有专利规划（来自 `chinese-patent-plan`）或详细用户指令
- 作为 `chinese-patent-pipeline` 的第三步（在 figure drawing 之后）

## 前置准备

- 专利规划文档（来自 `chinese-patent-plan`）或详细的用户指令
- 附图已生成并保存到 `images/` 目录（来自 `chinese-patent-drawer`）
- 参考模板：`../templates/patent_spec_template.html`
- 参考示例：`../templates/reference-patent-example.html`
- 撰写规则：`../rules/writing-rules.md`

## 撰写工作流程

### Step 1: 审阅规划文档
确认专利类型、技术方案、权利要求结构和附图清单。

### Step 2: 参考撰写规则
通读 `../rules/writing-rules.md`，确保理解每个章节的写作要求。

### Step 3: 参考示例专利
阅读 `../templates/reference-patent-example.html`，学习：
- 章节结构的 HTML 组织方式
- 中文专利语言的表达模式
- 附图引用格式

### Step 4: 基于模板生成 HTML
- 以 `../templates/patent_spec_template.html` 为结构基础
- 按 `../rules/writing-rules.md` 填充各章节内容
- 七大必备章节：
  1. 技术领域
  2. 背景技术
  3. 发明内容（技术问题 + 技术方案 + 有益效果）
  4. 附图说明
  5. 具体实施方式
  6. 权利要求书（`<section id="claims">`）
  7. 摘要（`<section id="abstract">`）

### Step 5: 插入附图
- 使用 `<figure><img src="images/图N.png" alt="描述" /><figcaption>图N 描述</figcaption></figure>`
- 图片路径使用相对本地路径，严禁 HTTP URL
- 图注在图片下方，图号不在图片像素内

### Step 6: 验证输出
检查：
- [ ] 七大章节齐全且顺序正确
- [ ] 所有图片路径使用本地相对路径
- [ ] 图文引用一致（图号在正文、附图说明、文件名中对应）
- [ ] 数学公式使用 LaTeX 格式
- [ ] 无外部 HTTP 链接

## HTML 格式规范

### 文档结构
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>专利说明书</title>
</head>
<body>
  <h1>说明书</h1>
  <h2>技术领域</h2>
  ...
  <h2>具体实施方式</h2>
  ...
  <section id="claims">
    <h2>权利要求书</h2>
    ...
  </section>
  <section id="abstract">
    <h2>摘要</h2>
    ...
  </section>
</body>
</html>
```

### 图片插入示例
```html
<figure>
  <img src="images/图1.png" alt="系统结构示意图" />
  <figcaption>图1 本发明实施例一的系统结构示意图</figcaption>
</figure>
```

### 数学公式
```html
<p>损失函数定义为 \(L = \frac{1}{N}\sum_{i=1}^{N}(y_i - \hat{y}_i)^2\)。</p>
<p>目标优化公式为：$$\min_{W} \|XW - Y\|_2^2 + \lambda\|W\|_1$$</p>
```

## 输出

- 完整的 HTML 文件（如 `说明书.html`）
- 文件内所有图片路径指向本地的 `images/` 目录
- 可直接执行 `python ../scripts/html_to_docx.py 说明书.html -o 说明书.docx` 导出 docx

## 注意事项

- 必须使用「本发明」或「本申请」的统称，同一篇不混用
- 权利要求书用语必须与说明书用语一致
- 实施方式必须结合附图详细描述，不可只有笼统概括
- 如附图尚未生成，先提醒用户运行 `chinese-patent-drawer`
