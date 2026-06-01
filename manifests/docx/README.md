# Docx Manifest

## 概述

面向 Word 文档创建、排版和自动化的 AI 配置包。使用 PreTeXt XML 作为文本排版引擎，python-docx 实现程序化文档操作。内置 Copy-First 数据安全保障和 Git 分支回滚机制。

## 核心特性

- **PreTeXt 排版引擎**: 基于 XML 的学术级文本排版，支持交叉引用、自动编号、多格式输出
- **python-docx 集成**: 程序化文档创建、样式管理、模板处理
- **Copy-First 安全策略**: 修改前必先复制，验证后再替换原始文件
- **Git 分支回滚**: 每次修改在独立分支上进行，支持任意回滚
- **多格式输出**: HTML（预览）、PDF（提交）、DOCX（协作）

## 依赖

- `skills/anthropics/skills/docx` — Anthropic 官方 docx 技能
- PreTeXt CLI (`pip install pretext`)
- LaTeX 发行版 (TeX Live，PDF 输出需要)
- Python 3.x + python-docx

## 快速开始

```bash
# 在目标项目中初始化
bash manifests/docx/scripts/vibe-init-docx.sh
```

## 文件结构

```
<root>/
  source/        # PreTeXt XML 源文件
    main.ptx     # 根文档
    chapters/    # 章节文件
    frontmatter/ # 前置内容（标题页、摘要、目录）
    backmatter/  # 后置内容（附录、参考文献、索引）
  assets/        # 图片、图表等资源
  output/        # 生成的输出文件
  styles/        # CSS/XSL/Publisher 配置
  templates/     # docx 参考模板
  scripts/       # python-docx 自动化脚本
  _backups/      # 原始文件的时间戳备份
```
