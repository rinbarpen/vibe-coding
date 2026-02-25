# Fund Proposal Manifest (Fund_Craft_Pro)

这是一个专门为**中文科研基金申请书（基金本子）**设计的 Vibe Coding 配置包，由 **Fund_Craft_Pro** 专家系统驱动。

## 核心功能

- **专家角色**: 集成了选题导航员、架构设计师、学术主笔、毒舌评审专家四个子角色。
- **全流程指令**: 提供 `/init`, `/brainstorm`, `/outline`, `/draft`, `/polish`, `/review` 覆盖从0到1的撰写全过程。
- **复合 Skills**: 深度整合了调研、写作、绘图、评审四大复合技能。
- **红线规则**: 严守概念边界，防止 AI 幻觉，确保学术严谨性。

## 快速开始

### 1. 初始化项目

在您的新基金项目根目录下，执行：

```bash
bash /path/to/vibe-coding/manifests/fund-proposal/scripts/vibe-init-fund.sh
```

### 2. 开始协作

初始化完成后，在 Cursor 或 Claude Code 中输入：

> /init

## 目录结构

- `draft/`: 各章节草稿。
- `outline/`: 提纲、创新点、关键科学问题。
- `refs/`: 参考文献。
- `assets/`: 技术路线图、图片素材。
- `commands/`: 指令定义。
- `rules/`: 核心撰写规则。
- `skills/`: 复合技能定义。
