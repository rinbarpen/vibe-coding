# Office CLI Manifest

## 概述

统一办公文档 CLI 配置包 —— 在一个命令界面下管理 Word (docx)、Excel (xlsx) 和 PowerPoint (ppt) 文档操作。基于 Anthropic 官方文档技能构建。

## 核心特性

- **统一 CLI**: docx / xlsx / ppt 三种文档类型通过 `office-cli` 一个入口管理
- **Copy-First 安全**: 所有修改都基于副本，绝不直接操作原始文件
- **批量处理**: 通过配置文件批量处理多文件、多格式任务
- **模板驱动**: 复用 .dotx / .xltx / .potx 模板保持格式一致
- **Git 回滚**: 每次修改在独立 Git 分支上进行

## 依赖

- Python 3.x + python-docx / openpyxl / python-pptx
- `skills/anthropics` 子模块

## 快速开始

```bash
# 在目标项目中初始化
bash manifests/office-cli/scripts/init-office-cli.sh
```

## 文件结构

```
<root>/
  inputs/        # 源文件
  outputs/       # 生成的文件
  templates/     # 文档模板 (.dotx, .xltx, .potx)
  scripts/       # 自定义自动化脚本
  configs/       # 批量处理配置
  _backups/      # 原始文件备份
  manifests/     # 子配置引用 (docx/, excel/, ppt/)
```
