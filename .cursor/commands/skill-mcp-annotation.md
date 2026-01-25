---
description: 用于自动扫描并生成 Skills 和 MCP 的标注简介及使用场景的命令。
globs: 
---

# Skill & MCP Annotation Command

此规则定义了 `/annotate-skills-mcp` 命令，用于维护项目中的 Skills 和 MCP 索引。

## 命令定义

### `/annotate-skills-mcp`

**目的**: 扫描 `skills/` 和 `mcps/` 目录，提取元数据并生成结构化的标注文件 `skills/ANNOTATIONS.md`。

**执行逻辑**:
1. **运行脚本**: 执行 `python3 scripts/annotate_skills_mcp.py`。
2. **脚本功能**:
   - **扫描 Skills**: 递归扫描 `skills/` 目录，提取 `SKILL.md` 或 `AGENTS.md` 中的名称和描述。
   - **扫描 MCPs**: 扫描 `mcps/` 目录，提取 `SERVER_METADATA.json` 和 `INSTRUCTIONS.md` 中的信息。
   - **汇总**: 将所有信息生成到 `skills/ANNOTATIONS.md`。
3. **手动验证**: 检查生成的 `skills/ANNOTATIONS.md` 是否准确。

**使用指南**:
- 当新增或修改了 Skill 或 MCP 时，运行此命令以保持索引同步。
- AI 在处理复杂任务时，应优先参考 `skills/ANNOTATIONS.md` 以确定哪些工具可用。
