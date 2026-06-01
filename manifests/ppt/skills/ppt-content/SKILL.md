---
name: ppt-content
description: python-pptx 幻灯片内容构建技能。覆盖幻灯片创建、内容填充（文本/表格/图表/图片）、样式应用与演讲者备注生成。
dependencies:
  - skills/anthropics/skills/pptx
  - manifests/ppt/skills/ppt-master-integration/SKILL.md
---

# Slide Content Construction

## 概述

本技能提供基于 python-pptx 的幻灯片内容构建能力。处理从结构化大纲到完整演示文稿的转换，包括文本、表格、图表和图片的程序化创建。

## 核心准则

1. **安全第一**: 所有内容修改在副本上进行，验证后再替换原始文件。
2. **大纲驱动**: 先有结构化大纲 (`source/outline.yaml`)，再生成幻灯片。
3. **内容适配布局**: 根据幻灯片布局类型 (title, content, two-column, blank) 选择合适的内容结构。

## 关键能力

- 从 YAML/JSON 大纲生成完整幻灯片
- 文本内容填充与格式化
- 表格创建与样式应用
- 图表嵌入（引用 excel manifest 数据管道的结果）
- 图片插入与定位
- 演讲者备注自动生成

## 使用场景

- 从内容大纲批量生成演示文稿
- 数据驱动型演示文稿（报告、财报、数据分享）
- 品牌化内容填充
- 演示文稿内容迁移和更新

## 指令集成

- 执行 `vibe-ppt-create` 时，必须启动此技能。
- 执行 `vibe-ppt-notes` 时，使用此技能的备注生成逻辑。
- 执行 `vibe-ppt-validate` 时，使用此技能的验证检查清单。
