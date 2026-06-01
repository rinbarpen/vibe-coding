---
name: ppt-master-integration
description: ppt-master 集成技能。覆盖演示文稿初始化、幻灯片母版管理、主题应用、模板继承链与多格式导出。
dependencies:
  - skills/anthropics/skills/pptx
---

# ppt-master Integration

## 概述

本技能提供基于 ppt-master 的幻灯片母版和模板管理能力。ppt-master 负责演示文稿的视觉一致性：母版创建、主题应用、模板继承和多格式导出。

## 核心准则

1. **母版优先**: 在添加内容前先确定幻灯片母版。中途更换母版会导致占位符引用丢失。
2. **主题一致性**: 整个演示文稿使用同一套主题配置。不要混用多个母版。
3. **模板版本控制**: 所有 `.potx` 模板文件纳入 Git 管理，变更可追溯。

## 关键能力

- 演示文稿初始化: `ppt-master init <name>`
- 幻灯片母版应用: `ppt-master apply <template>`
- 多格式导出: `ppt-master export pdf|images|video`
- 主题配置管理

## 使用场景

- 新演示文稿的模板初始化
- 已有文稿的主题/母版切换
- 品牌化输出（统一配色、字体、Logo）
- 批量导出为 PDF/图片

## 指令集成

- 执行 `vibe-ppt-template` 时，必须启动此技能。
- 执行 `vibe-ppt-export` 时，使用此技能的导出逻辑。
