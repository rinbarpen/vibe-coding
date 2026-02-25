# CLAUDE.md 维护标准 (Maintenance Standards)

CLAUDE.md 是 AI 代理（如 Claude Code）获取项目上下文的核心。高质量的 CLAUDE.md 能够显著提升 AI 的理解能力和工作效率。

## 1. 质量评分维度 (Quality Criteria)

参考以下 6 个维度对 CLAUDE.md 进行审计：

- **Commands/Workflows (20分)**: 核心命令（build, test, lint, dev）是否完整且准确。
- **Architecture Clarity (20分)**: 是否提供了清晰的代码库地图和模块关系。
- **Non-Obvious Patterns (15分)**: 是否记录了 Gotchas、非直观模式或特殊约定。
- **Conciseness (15分)**: 内容是否密集且无冗余，避免陈述显而易见的代码。
- **Currency (15分)**: 是否反映了当前代码库的状态（命令、路径、技术栈）。
- **Actionability (15分)**: 指令是否可直接执行，路径是否真实。

## 2. 维护时机 (When to Update)

在以下场景发生后，应立即更新 CLAUDE.md：
- **架构变更**: 新增/删除核心目录，或改变模块间的依赖关系。
- **命令变更**: 修改了 `pyproject.toml`, `package.json` 或 Makefile 中的常用命令。
- **关键文件**: 增加了重要的配置文件、入口文件或核心 API。
- **约定变更**: 引入了新的编码规范、测试模式或部署流程。

## 3. 维护流程 (Workflow)

1. **审计**: 使用 `vibe-claude-md-audit` 或调用 `claude-md-improver` 进行质量评估。
2. **更新**: 针对审计发现的问题，进行针对性补充或修正。
3. **验证**: 确保新增的命令可执行，引用的路径正确。

## 4. 本地与全局配置

- **`.claude.local.md`**: 用于存放个人偏好或本地环境配置（应加入 `.gitignore`）。
- **`~/.claude/CLAUDE.md`**: 用于存放跨项目的全局默认配置。
