---
name: pretext-authoring
description: PreTeXt XML 撰写技能。覆盖 PreTeXt XML schema、元素使用规范、交叉引用、编译输出与学术/专业出版最佳实践。
dependencies:
  - skills/anthropics/skills/docx
---

# PreTeXt XML Authoring

## 概述

本技能提供基于 PreTeXt (pretextbook.org) 的结构化文档撰写能力。PreTeXt 是一个开源的 XML 文档撰写和出版系统，面向学术论文、教材和专业文档。

## 核心准则

1. **XML 为源**: PreTeXt XML 是唯一的内容来源。DOCX/PDF/HTML 均为从 XML 编译生成的派生输出。
2. **模块化**: 使用 `<xi:include>` 将大文档拆分为章级别的 XML 文件。
3. **编译验证**: 每次提交前运行 `pretext build`，零错误才能提交。
4. **交叉引用**: 使用 `<xref>` 和 `<cite>`，绝不手动硬编码编号。

## 关键元素

| 元素 | 用途 |
|------|------|
| `<pretext>` | 根元素 |
| `<chapter>` / `<section>` / `<subsection>` | 文档层级 |
| `<p>` | 段落 |
| `<figure>` + `<image>` + `<caption>` | 图表 |
| `<table>` + `<tabular>` | 表格 |
| `<xref ref="id"/>` | 交叉引用 |
| `<cite ref="key"/>` | 文献引用 |
| `<xi:include href="file.ptx"/>` | 模块引入 |

## 使用场景

- 学术论文撰写与出版
- 技术文档编写
- 教材与讲义制作
- 需要多格式输出 (HTML/PDF/DOCX) 的专业文档

## 指令集成

- 执行 `pretext build` 时，使用此技能的编译验证逻辑。
- 执行文档结构审查时，使用此技能的 XML schema 检查。
