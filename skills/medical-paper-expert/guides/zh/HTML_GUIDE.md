# 中文医学论文 HTML 结构化编写指南

使用 HTML 编写中文论文可以更好地支持结构化数据，并能通过 Pandoc 完美转换为 DOCX 格式。

## 1. 基础结构模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>论文标题</title>
    <style>
        body { font-family: "SimSun", serif; line-height: 1.5; }
        h1, h2, h3 { font-family: "SimHei", sans-serif; }
        .table-title { text-align: center; font-weight: bold; margin-bottom: 5px; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        /* 三线表样式 */
        .three-line-table { border-top: 2px solid black; border-bottom: 2px solid black; }
        .three-line-table thead { border-bottom: 1px solid black; }
        th, td { padding: 8px; text-align: center; }
    </style>
</head>
<body>
    <h1>研究论文标题</h1>
    <div class="authors">作者1, 作者2</div>

    <section id="abstract">
        <h2>摘要</h2>
        <p><strong>目的：</strong>... <strong>方法：</strong>... <strong>结果：</strong>... <strong>结论：</strong>...</p>
    </section>

    <section id="introduction">
        <h2>1. 前言</h2>
        <p>背景与目的...</p>
    </section>

    <section id="methods">
        <h2>2. 方法</h2>
        <p>伦理批准号：XXX...</p>
    </section>

    <section id="results">
        <h2>3. 结果</h2>
        <div class="table-title">表1 两组基线资料比较</div>
        <table class="three-line-table">
            <thead>
                <tr><th>组别</th><th>例数</th><th>年龄</th></tr>
            </thead>
            <tbody>
                <tr><td>观察组</td><td>50</td><td>65.4±8.2</td></tr>
                <tr><td>对照组</td><td>50</td><td>64.8±7.9</td></tr>
            </tbody>
        </table>
    </section>

    <section id="discussion">
        <h2>4. 讨论</h2>
        <p>结果解释与局限性...</p>
    </section>
</body>
</html>
```

## 2. 编写建议

- **语义化标签**: 使用 `<section>`, `<article>`, `<h1>`-`<h6>` 以便 Pandoc 生成正确的 DOCX 大纲。
- **三线表**: 在 HTML 中使用 `border-top` 和 `border-bottom` 模拟三线表，转换时 Pandoc 会尽可能保留这些样式。
- **公式**: 建议使用 MathJax 格式的 LaTeX 公式，Pandoc 在转换时会自动处理。
    - 示例：`\( P < 0.05 \)`
- **图片**: 使用 `<img>` 标签，并确保路径正确。
    - 示例：`<figure><img src="fig1.png" alt="图1"><figcaption>图1 流程图</figcaption></figure>`
