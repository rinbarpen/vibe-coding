# Agent Browser Manifest

## 概述

AI 驱动的浏览器自动化配置包，基于 [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)。为 AI Agent 提供无头浏览器控制能力：网页导航、数据提取、表单填写、截图等。

## 核心特性

- **无头浏览器控制**: 导航、点击、输入、提取、截图
- **脚本化自动化**: 可编写、保存、回放浏览器操作脚本
- **会话管理**: 保存和恢复浏览器会话，避免重复登录
- **Trace 调试**: 录制浏览器操作轨迹用于调试

## 依赖

- Node.js 18+
- `npx agent-browser` CLI

## 快速开始

```bash
# 在目标项目中初始化
bash manifests/agent-browser/scripts/init-agent-browser.sh
```

## 文件结构

```
<root>/
  scripts/       # 浏览器自动化脚本
  sessions/      # 保存的浏览器会话
  fixtures/      # 测试数据、表单输入
  screenshots/   # 截图
  traces/        # 调试轨迹
  reports/       # 运行报告
```
