---
name: excel-visualization
description: openpyxl 图表创建与格式化技能。覆盖图表类型选择、坐标轴配置、系列管理、调色板与条件格式化。
dependencies:
  - skills/anthropics/skills/xlsx
  - manifests/excel/skills/excel-analysis/SKILL.md
---

# Excel Chart Visualization

## 概述

本技能提供基于 openpyxl 的图表创建和格式化能力，将数据分析结果转化为清晰、专业、可访问的可视化图表。

## 核心准则

1. **图表类型匹配数据**: 柱状图用于比较，折线图用于趋势，散点图用于关系，饼图仅用于少量分类。
2. **可访问性**: 使用色盲友好调色板，不单独依赖颜色区分数据。
3. **数据墨水比**: 最小化非数据元素（网格线、边框、3D 效果），优先使用干净的 2D 图表。

## 支持的图表类型

- BarChart / ColumnChart — 类别比较
- LineChart — 时间序列与趋势
- ScatterChart — 变量关系
- PieChart — 组成比例（仅限 ≤5 个类别）
- RadarChart — 多维对比

## 使用场景

- 数据趋势可视化
- 分类对比图表
- 条件格式化热力图
- 多系列组合图表

## 指令集成

- 执行 `vibe-excel-chart` 时，必须启动此技能。
- 执行 `vibe-excel-analyze` 后，建议使用此技能生成辅助图表。
