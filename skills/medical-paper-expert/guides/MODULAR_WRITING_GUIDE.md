# 模块化医学论文写作指南 (Modular Writing Guide)

为了提高大型医学论文的编写效率和可维护性，建议采用模块化文件结构。

## 1. 推荐目录结构

```text
paper-project/
├── main.html (或 main.tex)      # 主入口文件，负责引入各章节
├── metadata.yaml               # 论文元数据（标题、作者、关键词等）
├── sections/                   # 章节目录
│   ├── 01_abstract.html
│   ├── 02_introduction.html
│   ├── 03_methods.html
│   ├── 04_results.html
│   ├── 05_discussion.html
│   └── 06_references.html
├── figures/                    # 图像文件
│   ├── fig1_flowchart.png
│   └── fig2_results.jpg
├── tables/                     # 独立表格文件（可选）
│   └── table1_baseline.html
└── bibliography.bib            # 参考文献数据库（仅限 LaTeX）
```

## 2. 模块化编写规范

### 文件命名
- 使用数字前缀确保章节顺序（如 `01_`, `02_`）。
- 使用小写字母和下划线，避免空格。

### 章节编写原则
- **独立性**: 每个章节文件应专注于其核心内容。
- **无头编写**: 章节文件内部不需要包含 `<html>` 或 `\documentclass` 等全局标签，直接从标题或正文开始。

## 3. 合并与输出指令

### HTML (中文) 合并
使用 Pandoc 将多个 HTML 片段合并为一个 DOCX：
```bash
pandoc sections/*.html -o full_manuscript.docx --metadata-file=metadata.yaml
```

### LaTeX (英文) 合并
在 `main.tex` 中使用 `\input` 或 `\include`：
```latex
\begin{document}
\input{sections/01_abstract}
\input{sections/02_introduction}
% ... 依此类推
\end{document}
```

## 4. 自动化初始化脚本 (Python)
你可以要求 Agent 运行以下逻辑来快速创建结构：
```python
import os

dirs = ['sections', 'figures', 'tables']
for d in dirs:
    os.makedirs(d, exist_ok=True)

sections = [
    '01_abstract.html', '02_introduction.html', 
    '03_methods.html', '04_results.html', 
    '05_discussion.html'
]
for s in sections:
    with open(f'sections/{s}', 'w') as f:
        f.write(f'<!-- {s} content -->\n')
```
