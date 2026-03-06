# CLAUDE.md

针对小说创作的项目上下文管理。

## 创作命令

| 命令 | 描述 |
|---------|-------------|
| `vibe-outline` | 查看/更新小说大纲 |
| `vibe-characters` | 查看角色设定卡 |
| `vibe-world` | 查看世界观设定 |
| `vibe-progress` | 统计章节字数与进度 |
| `vibe-check-logic` | 检查剧情逻辑一致性 |

## 项目结构

```
<root>/
  chapters/    # 章节正文 (Markdown)
  outline/     # 大纲与剧情线
  characters/  # 角色设定文件
  world/       # 世界观、地理、力量体系
  research/    # 资料收集与参考（项目特定资料）
  references/  # 通用知识域参考（神秘学、神话等）
  drafts/      # 废弃稿件与灵感碎片
```

## 知识参考 (Knowledge References)

创作涉及神秘学或神话元素时，AI 应优先查阅以下参考以保持术语与典故的准确性：

| 领域 | 文件 |
|------|------|
| 神秘学 | `references/occult-knowledge.md` |
| 希腊神话 | `references/greek-mythology.md` |
| 北欧神话 | `references/norse-mythology.md` |
| 中式神话 | `references/chinese-mythology.md` |
| 日式神话 | `references/japanese-mythology.md` |
| 修仙 | `references/cultivation-knowledge.md` |
| 异世界 | `references/isekai-knowledge.md` |
| SCP 基金会 | `references/scp-foundation.md` |
| 灵能 | `references/psionic-knowledge.md` |

- `references/` 为通用知识域，`research/` 为项目特定资料。

## 关键文件

- `outline/main.md` - 主线剧情大纲
- `characters/list.md` - 核心角色索引
- `world/setting.md` - 核心世界观说明

## 创作风格指南

- 视角控制：明确每一章的 POV (Point of View)
- 描写偏好：侧重动作与心理，避免过度形容词堆砌
- 对话风格：符合角色身份背景，避免 OOC (Out Of Character)

## 验证流程

- 逻辑自洽：新章节是否与之前的设定冲突？
- 伏笔检查：是否有未回收的伏笔或逻辑漏洞？
- 语气校验：是否符合小说整体基调？

## 协作流

- 灵感阶段：在 `drafts/` 记录碎片。
- 细化阶段：将灵感转化为 `outline/` 中的具体情节。
- 创作阶段：在 `chapters/` 编写正文。
- 润色阶段：使用 AI 进行遣词造句的优化。
