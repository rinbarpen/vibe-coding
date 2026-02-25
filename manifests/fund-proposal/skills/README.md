# 基金本子推荐 Skills 索引

本目录定义了基金本子撰写过程中的**核心复合 Skills**。这些 Skill 深度整合了 Workspace 内的多个基础能力，为 AI 助手提供一站式的专家级指导。

## 核心复合 Skills (Top-level)

| 技能名称 | 路径 | 整合的基础能力 | 使用场景 |
| :--- | :--- | :--- | :--- |
| **基金学术主笔** | `fund-writing/SKILL.md` | `scientific-writing`, `chinese-copywriting`, `Humanizer-zh`, `beautiful_prose` | 负责正文撰写、学术润色、去 AI 化。 |
| **基金深度调研** | `fund-research/SKILL.md` | `deep-research`, `brainstorming-ideas`, `research-grants`, `x-research` | 负责选题、Gap 分析、搜集事实与图片素材。 |
| **基金视觉架构** | `fund-visuals/SKILL.md` | `drawio`, `Pretty-mermaid`, `canvas-design`, `scientific-schematics` | 负责技术路线图、逻辑图绘制与排版优化。 |
| **基金评审专家** | `fund-review/SKILL.md` | `peer-review`, `research-grants` (评审标准) | 负责逻辑审计、模拟评审、提出 Reject 理由。 |

## 基础 Skills 参考 (Base Skills)

AI 助手在执行上述复合技能时，会自动参考以下基础路径下的 `SKILL.md`：

- **排版**: `skills/chinese-copywriting-guidelines/SKILL.md`
- **文风**: `skills/beautiful_prose/SKILL.md`
- **结构**: `skills/claude-scientific-skills/scientific-skills/research-grants/SKILL.md`
- **写作**: `skills/claude-scientific-skills/scientific-skills/scientific-writing/SKILL.md`
- **意图**: `skills/superpowers/skills/brainstorming/SKILL.md`
- **计划**: `skills/superpowers/skills/writing-plans/SKILL.md`
- **选题**: `skills/AI-Research-SKILLs/21-research-ideation/brainstorming-research-ideas/SKILL.md`
- **绘图**: `skills/drawio-skills/skills/drawio/SKILL.md`, `skills/Pretty-mermaid-skills/SKILL.md`
- **调研**: `skills/ai-skills/skills/deep-research/SKILL.md`, `skills/x-research-skill/SKILL.md`

---
*注意：复合技能通过 `dependencies` 显式关联基础能力，确保执行过程中的逻辑一致性。*
