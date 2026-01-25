---
description: 根据任务需求提取并推荐最相关的 Skills。
globs: 
---

# Extract Skills Command

此规则定义了 `/extract-skills` 命令，用于从项目已标注的技能库中检索最符合当前任务需求的 Skills。

## 命令定义

### `/extract-skills`

**目的**: 通过分析用户提供的任务描述，从 `skills/ANNOTATIONS.md` 中筛选出最相关的技能。

**使用方式**: 在对话框中输入 `/extract-skills [任务描述]`。

**执行逻辑**:
1. **运行脚本**: 执行 `python3 .cursor/commands/extract-skills/extract_skills.py "[input]"`。
2. **输出结果**: 脚本将返回一个按相关性排序的技能列表，包含：
   - 技能名称
   - 相对路径
   - 简介
   - 匹配的关键词
3. **后续建议**: AI 应根据推荐的技能路径，读取相应的 `SKILL.md` 或 `AGENTS.md` 以获取详细指令。

**示例**:
- `/extract-skills 我需要处理 PDF 文件并提取文本`
- `/extract-skills 帮我设计一个具有毛玻璃风格的 UI 界面`
- `/extract-skills 如何进行单细胞 RNA-seq 数据分析？`
