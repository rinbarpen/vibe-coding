---
description: 自动更新 CLAUDE.md 文档，确保 AI 拥有最准确的项目上下文（命令、架构、规范）。
globs: ["CLAUDE.md"]
---

# Update CLAUDE.md Command

此规则定义了 `/update-claude-md` 命令，用于维护 AI 的项目“长期记忆”。

## 命令定义

### `/update-claude-md`

**目的**: 提取项目最新的构建命令、测试指令、目录架构和编码规范，更新 `CLAUDE.md`。

**使用方式**: 在对话框中输入 `/update-claude-md`。

**执行逻辑**:
1. **审计上下文**: 检查当前的 `CLAUDE.md` 是否过时。
2. **提取关键信息**:
   - 扫描 `pyproject.toml`, `package.json` 等获取最新命令。
   - 扫描目录结构更新 Architecture 部分。
   - 识别新引入的编码模式。
3. **执行更新**: 运行 `python3 .cursor/commands/update-claude-md/update_claude_md.py`。
4. **同步**: 确保 `CLAUDE.md` 与项目实际状态 100% 同步。

**示例**:
- `/update-claude-md`
