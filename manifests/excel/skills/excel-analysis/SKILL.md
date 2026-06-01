---
name: excel-analysis
description: openpyxl 数据分析技能。覆盖数据加载、统计函数、过滤、排序、数据透视表构建、公式编写与数据验证。
dependencies:
  - skills/anthropics/skills/xlsx
---

# Excel Data Analysis

## 概述

本技能提供基于 openpyxl 的数据分析工作流，涵盖从原始数据加载到统计分析和报表输出的完整流程。

## 核心准则

1. **安全第一**: 永远在副本上操作。原始文件不可变。
2. **数据清洗优先**: 分析前必须验证数据类型、处理缺失值、检测重复行。
3. **可追溯性**: 所有分析和公式通过 git commit 记录，支持回滚。

## 使用场景

- 从 CSV/JSON 导入数据到 xlsx
- 数据清洗与标准化
- 统计分析与数据透视表
- 公式构建与批量计算
- 数据验证规则应用

## 指令集成

- 执行 `vibe-excel-import` 时，必须启动此技能的数据加载逻辑。
- 执行 `vibe-excel-analyze` 时，以此技能为核心进行统计分析。
- 执行 `vibe-excel-validate` 时，使用此技能的验证检查清单。
