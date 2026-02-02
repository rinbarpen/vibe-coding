---
description: 将项目中所有包含 SKILL.md 的 skill 复制到用户 ~/.cursor/skills/ 目录。
globs:
---

# Install Skills Command

此规则定义了 `/install-skills` 命令，用于将项目 `skills/` 下所有有效 skill 安装到用户的 Cursor 全局 skill 目录，使这些 skill 在所有项目中可用。

## 命令定义

### `/install-skills`

**目的**: 扫描 `skills/` 目录下所有包含 `SKILL.md` 的目录，并将它们复制到 `~/.cursor/skills/`，以便在 Cursor 中全局使用。

**使用方式**: 在对话框中输入 `/install-skills`，或直接运行脚本。

**执行逻辑**:
1. **运行脚本**: 执行 `python3 .cursor/commands/install-skills/install_skills_to_user.py`。
2. **可选参数**:
   - `--overwrite`: 若目标目录已存在则覆盖（默认跳过已存在的 skill）。
   - `--dry-run`: 仅列出将要安装的 skill，不实际复制。
   - `--target-dir PATH`: 指定目标目录（默认 `~/.cursor/skills`）。
3. **输出**: 显示找到的 skill 数量、安装成功数、跳过数及失败信息。

**示例**:
- 安装到默认目录（已存在则跳过）:
  `python3 .cursor/commands/install-skills/install_skills_to_user.py`
- 预览将要安装的 skill:
  `python3 .cursor/commands/install-skills/install_skills_to_user.py --dry-run`
- 覆盖已存在的 skill:
  `python3 .cursor/commands/install-skills/install_skills_to_user.py --overwrite`

## 说明

- 有效 skill 指包含 `SKILL.md` 文件的目录。
- 同名 skill（仅目录名相同）会使用路径前缀区分，例如 `awesome-claude-skills-artifacts-builder`。
- 复制时会排除 `.git`、`__pycache__`、`node_modules` 等目录及 `.pyc` 等文件。
- 安装前可先使用 `--dry-run` 查看列表，或备份现有 `~/.cursor/skills/`。
