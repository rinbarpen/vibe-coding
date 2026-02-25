---
name: vibe-coding-toolkit
description: 全面的 Vibe Coding 开发工具包，旨在通过集成 skill-seekers、subagent 调度和开源标准，简化从需求到交付的完整开发流程。适用于构建高质量开源项目和遵循正规开发流程。
---

# Vibe Coding Toolkit

这是一个为 Cursor 深度优化的开发枢纽，旨在通过 "Vibe Coding"（意图驱动、AI 协作、快速迭代）的方式，构建符合工业级标准和开源规范的软件。

## 核心流程 (The Vibe Flow)

遵循以下六个阶段进行开发：

1.  **探索 (Explore)**: 使用 `skill-seekers` 快速摄取未知库的文档，或调用 `explore` subagent 了解现有代码库。
2.  **设计 (Design)**: 调用 `code-architect` subagent 进行架构设计，确保符合 [standards/open-source-standards.md](standards/open-source-standards.md)。
3.  **实现 (Implement)**: 采用小步快跑的方式编写代码，优先使用 `uv` 管理 Python 环境。
4.  **验证 (Verify)**: 强制执行 `ReadLints`，并调用 `code-reviewer` 进行质量把关。
5.  **维护 (Maintain)**: 及时更新 `CLAUDE.md` 以反映最新的架构、命令和 Gotchas。
6.  **交付 (Deliver)**: 自动生成符合规范的 PR 描述，并更新项目文档。

## 集成工具

### 1. Skill Seekers (文档即技能)
当遇到不熟悉的库、框架或 API 时，立即调用 `skill-seekers` 将其转换为当前可用的技能。
> 注意：此功能依赖外部工具 [skill-seekers](https://github.com/skill-seekers/skill-seekers)。

- `skill-seekers scrape --url <URL> --name <NAME>`: 快速抓取在线文档。
- `skill-seekers github --repo <OWNER/REPO>`: 分析 GitHub 仓库。

### 2. CLAUDE.md 管理
当需要审计或优化项目上下文时，调用 `claude-md-improver` skill：
- 审计质量：评估 `CLAUDE.md` 是否符合 A 级标准。
- 自动更新：根据项目变更自动补充命令和架构信息。

### 3. Subagent 调度策略
根据任务复杂度，主动建议并启动以下 subagent：
- **`explore`**: 用于快速定位代码、理解逻辑。
- **`code-architect`**: 用于大型功能设计、重构方案。
- **`code-reviewer`**: 用于提交前的最后检查。
- **`shell`**: 用于执行复杂的环境配置或 Git 操作。

## 开发规范

- **环境管理**: 优先使用 `uv`，其次是 `conda` (Python 3.10)。
- **代理**: 下载文件前必须执行 `proxy_on`。
- **可视化**: `matplotlib` 绘图必须使用英文。
- **开源标准**: 详见 [standards/open-source-standards.md](standards/open-source-standards.md)。

## 常用命令

- `vibe-init`: 初始化项目结构（包含 .cursor/rules/*.mdc, CLAUDE.md, AGENTS.md）。
- `vibe-check`: 运行全套 lint 和测试。
- `vibe-claude-md-audit`: 审计 `CLAUDE.md` 质量。
- `vibe-ship`: 准备发布，检查 README 和 CHANGELOG。

---
更多详细信息请参考：
- [agents/subagent-roles.md](agents/subagent-roles.md)
- [standards/development-workflow.md](standards/development-workflow.md)
- [standards/claude-md-maintenance.md](standards/claude-md-maintenance.md)
