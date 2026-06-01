# Excel Manifest

## 概述

面向电子表格创建、数据分析和报表自动化的 AI 配置包。强制使用 Python (openpyxl) 进行所有操作，内置数据安全保障和 Git 分支回滚机制。

## 核心特性

- **Python-Only**: 所有 Excel 操作必须通过 openpyxl，严禁直接修改文件
- **Copy-First 安全策略**: 修改前必先复制，验证后再替换原始文件
- **Git 分支回滚**: 每次修改在独立分支上进行，支持任意回滚
- **自动备份**: 原始文件修改前自动存入 `_backups/` 目录

## 依赖

- `skills/anthropics/skills/xlsx` — Anthropic 官方 xlsx 技能
- Python 3.x + openpyxl

## 快速开始

```bash
# 在目标项目中初始化
bash manifests/excel/scripts/vibe-init-excel.sh
```

## 文件结构

```
<root>/
  data/          # 原始和处理后的数据文件
  workbooks/     # 生成的 workbook 文件
  scripts/       # openpyxl 自动化脚本
  templates/     # 预定义样式的模板
  reports/       # 分析报告和图表导出
  schemas/       # 数据验证 schema
  _backups/      # 原始文件的时间戳备份
```
