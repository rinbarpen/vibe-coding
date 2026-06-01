---
name: docx-advanced
description: python-docx 高级操作技能。覆盖节管理、页眉页脚、复杂表格、图片操作、样式管理与修订跟踪。
dependencies:
  - skills/anthropics/skills/docx
  - manifests/docx/skills/pretext-authoring/SKILL.md
---

# Advanced python-docx Operations

## 概述

本技能提供基于 python-docx 的高级 Word 文档操作能力，包括模板处理、样式管理、复杂表格构建和文档结构验证。

## 核心准则

1. **安全第一**: 所有操作在副本上进行。永远不直接修改原始文件。
2. **验证后替换**: 每次修改后必须验证 working copy 结构完整，然后才能替换原始文件。
3. **样式一致性**: 使用命名样式而非内联格式，确保文档外观统一。

## 关键能力

- 文档合并 (Merge): 将多个 docx 的内容合并到单个文档
- 模板填充 (Templating): 使用数据字典替换模板中的占位符
- 样式管理: 创建、修改和应用命名样式
- 表格操作: 动态创建和格式化复杂表格
- 图片嵌入: 程序化插入和定位图片
- 结构验证: 检查 sections、paragraphs、styles 的完整性

## 使用场景

- 批量生成标准化文档（报告、信函、证书）
- 从 PreTeXt 编译的 DOCX 进行后处理和微调
- 多个协作文档的合并
- 文档格式迁移和样式统一

## 指令集成

- 执行 `vibe-docx-merge` 时，必须启动此技能。
- 执行 `vibe-docx-templating` 时，以此技能为核心进行模板处理。
- 执行 `vibe-docx-validate` 时，使用此技能的验证检查清单。
