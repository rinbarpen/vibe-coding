# Anything CLI Manifest

## 概述

[CLI-Anything](https://github.com/HKUDS/CLI-Anything) 配置包 —— 将任何软件代码库转换为 AI Agent 可控的 CLI 界面。一条命令即可为任意软件生成生产级 CLI 接口。

## 核心特性

- **一键生成**: `/cli-anything <路径或仓库>` 自动完成 7 阶段流水线
- **Agent 原生**: 每条命令支持 `--json` 输出，Agent 可自动发现和使用
- **CLI-Hub 注册表**: 浏览、安装社区预构建的 CLI，无需自己生成
- **REPL 模式**: 默认进入交互式 REPL，支持撤销/重做和会话状态
- **命名空间隔离**: PEP 420 命名空间包，多个 CLI 共存无冲突

## 依赖

- Python 3.10+
- 目标软件（如需 E2E 测试）
- Claude Code / OpenCode / Cursor 等 AI Agent

## 快速开始

```bash
# 推荐方式：安装 CLI-Hub 包管理器
pip install cli-anything-hub

# 搜索并安装社区预构建的 CLI
cli-hub search <name>
cli-hub install <name>

# 或使用生成器为任意代码库创建 CLI
# (在 Claude Code 中)
# /cli-anything <path-or-url>
```

## 文件结构

```
<root>/
  harnesses/     # 生成的 CLI 项目目录
  registry/      # CLI-Hub 本地缓存
  configs/       # 生成配置
  tests/         # 跨 CLI 集成测试
```
