# Vibe Coding Manifest (Programming & Development)

这是一个专门为**编程开发**设计的 Vibe Coding 配置包，可以轻松集成到任何软件工程项目中。

## 包含内容

- **AGENTS.md / CLAUDE.md**: 核心 AI 指令与项目记忆模板。
- **rules/**: 针对编程开发优化的 Cursor 规则（.mdc）。
- **scripts/**: 自动化初始化、提交钩子与工具脚本。
- **skills/**: 工业级开发标准、规范与 AI 技能模板。
- **scenarios/**: 针对特定开发场景（如 SaaS, Distributed, Cross-platform）的配置。
- **architectures/**: 软件架构参考（如 ESR 架构）。
- **agents/**: Subagent 角色定义与编程任务调度策略。

## 快速开始

### 1. 复制到新项目

在你的新项目根目录下，执行以下命令：

```bash
mkdir -p manifests
cp -r /path/to/vibe-coding/manifests/vibe-coding ./manifests/
```

### 2. 初始化项目结构

运行初始化脚本。它会自动创建必要的目录，并将规则与模板复制到项目根目录。

```bash
bash ./manifests/vibe-coding/scripts/vibe-init.sh
```

### 3. 配置说明

初始化后，你可以根据项目需求修改根目录下的 `CLAUDE.md` 和 `AGENTS.md`。

## 核心功能

- **意图驱动开发**: 强制执行 Plan-First 模式。
- **自动化 Lint 检查**: 每次修改后自动运行 ReadLints。
- **Subagent 调度**: 预设了 explore, code-architect, code-reviewer 等角色。
- **环境管理**: 默认推荐使用 `uv` 进行 Python 依赖管理。

## 依赖

- **Bash**: 脚本运行环境。
- **Skill Seekers (可选)**: 用于抓取外部文档并转化为 AI 技能。

---
*注：若你将此文件夹重命名或放置在不同路径，`vibe-init.sh` 会自动检测并更新规则中的引用路径。*
