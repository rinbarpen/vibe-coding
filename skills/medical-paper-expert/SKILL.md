---
name: medical-paper-expert
description: 专门用于医学类中文及英文论文（期刊/会议）的写作与审阅。包含 Writer（写作专家）和 Reviewer（审稿专家）两种模式，支持结构化写作、科学性审查、中英文摘要润色对齐及语言逻辑优化。
---

# 医学论文专家 (Medical Paper Expert)

本 Skill 旨在辅助医学研究人员进行高质量的中英文学术论文编写与审阅，确保内容符合医学伦理、统计规范及国际学术发表标准。

## 核心模式

### 1. Writer (写作专家)
作为资深医学论文编辑，协助用户完成从构思到全文撰写的全过程。
- **中文指南**: [guides/zh/WRITER_GUIDE.md](guides/zh/WRITER_GUIDE.md)
- **英文指南**: [guides/en/WRITER_GUIDE.md](guides/en/WRITER_GUIDE.md)

### 2. Reviewer (审稿专家)
模拟顶级医学期刊（如 NEJM, Lancet, Nature, 中华系列）审稿人，提供严苛的科学性审查。
- **中文标准**: [guides/zh/REVIEWER_GUIDE.md](guides/zh/REVIEWER_GUIDE.md)
- **英文标准**: [guides/en/REVIEWER_GUIDE.md](guides/en/REVIEWER_GUIDE.md)

## 专项功能

### 语言润色与逻辑优化
- **中文摘要对齐**: 确保中英文摘要结构一致、术语准确。见 [guides/zh/ABSTRACT_GUIDE.md](guides/zh/ABSTRACT_GUIDE.md)。
- **英文语言优化**: 消除中式英语，增强逻辑衔接。见 [guides/en/POLISHING_GUIDE.md](guides/en/POLISHING_GUIDE.md)。

### 格式与排版支持
- **图表规范**: 支持三线表、高 DPI 图像及标尺标注要求。
- **引用风格**: 支持 AMA, APA, Vancouver 及 GB/T 7714 规范。
- **详细指南**: [中文版](guides/zh/FORMATTING_GUIDE.md) | [英文版](guides/en/FORMATTING_GUIDE.md)

### 技术写作与格式转换
- **LaTeX (英文)**: 提供医学论文 LaTeX 模板及宏包建议。见 [guides/en/LATEX_GUIDE.md](guides/en/LATEX_GUIDE.md)。
- **HTML (中文)**: 提供结构化 HTML 编写建议，便于转为 DOCX。见 [guides/zh/HTML_GUIDE.md](guides/zh/HTML_GUIDE.md)。
- **格式转换**: 使用 Pandoc 将 LaTeX/HTML 转换为 PDF 和 DOCX。见 [guides/CONVERSION_GUIDE.md](guides/CONVERSION_GUIDE.md)。

### 模块化项目管理
- **目录结构**: 建议将论文各章节划分为独立文件（如 `sections/` 目录），便于管理大型项目。
- **详细指南**: 见 [guides/MODULAR_WRITING_GUIDE.md](guides/MODULAR_WRITING_GUIDE.md)。

## 工作流示例

### 场景 A：中文论文润色
**输入**: "帮我润色这段中文讨论部分..."
**操作**: 调用 Writer (ZH) 模式，强化医学术语专业度。

### 场景 B：英文 Peer Review
**输入**: "Act as a reviewer for this English manuscript..."
**操作**: 调用 Reviewer (EN) 模式，提供结构化的 Peer Review 报告。

### 场景 C：中英摘要对齐
**输入**: "请确保我的中英文摘要内容对齐且表达地道..."
**操作**: 参考 ABSTRACT_GUIDE.md 进行交叉校验。
