# PPT Manifest

## 概述

面向演示文稿创建、模板管理和自动化的 AI 配置包。使用 ppt-master 管理幻灯片母版和模板，python-pptx 实现程序化演示文稿生成。内置 Copy-First 数据安全保障和 Git 分支回滚机制。

## 核心特性

- **ppt-master 模板管理**: 幻灯片母版创建、主题应用、多格式导出
- **python-pptx 集成**: 程序化幻灯片创建、内容填充、动画编排
- **Copy-First 安全策略**: 修改前必先复制，验证后再替换原始文件
- **Git 分支回滚**: 每次修改在独立分支上进行，支持任意回滚
- **多格式导出**: PPTX、PDF、图片序列

## 依赖

- `skills/anthropics/skills/pptx` — Anthropic 官方 pptx 技能
- Slide master management via `skills/anthropics/skills/pptx` + python-pptx
- Python 3.x + python-pptx

## 快速开始

```bash
# 在目标项目中初始化
bash manifests/ppt/scripts/vibe-init-ppt.sh
```

## 文件结构

```
<root>/
  source/        # 幻灯片内容定义（YAML/JSON/Markdown）
  templates/     # ppt-master 幻灯片母版和主题配置
  output/        # 生成的演示文稿
  assets/        # 图片、图标、Logo、媒体文件
  scripts/       # python-pptx 自动化脚本
  notes/         # 演讲者备注和演示脚本
  _backups/      # 原始文件的时间戳备份
```
