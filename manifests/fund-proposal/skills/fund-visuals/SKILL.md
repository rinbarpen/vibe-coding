---
name: fund-visuals
description: 基金本子视觉架构技能。整合Draw.io、Mermaid及Canvas设计能力，负责技术路线图、逻辑架构图的绘制与美化。
dependencies:
  - skills/drawio-skills/skills/drawio/SKILL.md
  - skills/Pretty-mermaid-skills/SKILL.md
  - skills/anthropics/skills/canvas-design/SKILL.md
  - skills/claude-scientific-skills/scientific-skills/scientific-schematics/SKILL.md
---

# 基金本子视觉架构 (Fund Visuals)

## 概述
本技能旨在提升基金本子的“颜值”与逻辑可视化水平。通过自动生成精美的 Mermaid 图表、绘制专业的技术路线图以及利用 Canvas 进行视觉优化，使复杂的科学逻辑一目了然。

## 核心准则
1. **逻辑可视化**: 优先使用 `Pretty-mermaid-skills` 生成逻辑流程图或甘特图，确保大纲层级的视觉化呈现。
2. **专业路线图**: 对于核心技术路线，调用 `drawio` 或 `scientific-schematics` 绘制具有出版质量的架构图。
3. **视觉一致性**: 确保所有图表的字体、颜色风格与基金本子的学术调性保持一致。
4. **Canvas 协同**: 利用 `canvas-design` 在侧边栏实时展示和调整图表，方便用户预览和修改。

## 使用场景
- 在 `/outline` 阶段，同步输出逻辑架构图。
- 在 `/draft` 阶段，为“研究方案”和“技术路线”部分绘制示意图。
- 优化已有的低质量图片或手绘草图。

## 指令集成
- 配合 `/outline` 和 `/draft` 指令使用，负责所有 `[此处插入图...]` 占位符的实际内容填充。
