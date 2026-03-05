# Vibe Coding Toolkit 快捷开发命令清单

本清单列出了 `vibe-coding-toolkit` 提供的常用命令和 subagent 调度指令。

## 1. 自动化脚本 (Scripts)

| 命令 | 描述 | 用法 |
| :--- | :--- | :--- |
| `vibe-init` | 初始化项目结构（目录、.cursor/rules/*.mdc, CLAUDE.md, AGENTS.md 模板） | `./manifests/vibe-coding/scripts/vibe-init.sh` (路径需根据实际位置调整) |
| `vibe-skill-fetch` | 快捷调用 `skill-seekers` 抓取文档或 GitHub 仓库 | `./manifests/vibe-coding/scripts/vibe-skill-fetch.sh <URL_OR_REPO> [NAME]` |
| `vibe-post-commit` | Commit 后的自动化维护（同步文档、检查测试、GitHub 状态） | `./manifests/vibe-coding/scripts/vibe-post-commit.sh` |
| `vibe-claude-md-audit` | 审计 CLAUDE.md 质量（调用 claude-md-improver skill） | `CallMcpTool("claude-md-improver", "audit", ...)` |
| `/update-readme` | 自动更新项目 README.md 文档 | `/update-readme [更新说明]` |
| `/update-claude-md` | 自动更新 CLAUDE.md 项目上下文 | `/update-claude-md` |
| `/update-docker` | 同步 Docker 配置与项目状态 | `/update-docker` |
| `/update-docs` | 同步 docs/ 文档与实现 | `/update-docs [可选说明]` |
| `/update-examples` | 同步 examples/ 示例代码 | `/update-examples [可选说明]` |
| `/update-scripts` | 同步 scripts/ 工具脚本 | `/update-scripts [可选说明]` |
| `gh pr create` | 自动创建 GitHub PR | `gh pr create --title "..." --body "..."` |
| `vibe-ci-check` | 监控 GitHub CI 状态 | `gh pr checks` 或启动 `ci-watcher` subagent |

## 2. Subagent 调度指令 (Subagent Dispatching)

在对话中，你可以直接要求我启动以下 subagent：

- **`explore`**: "启动 explore subagent 帮我分析项目结构。"
- **`code-architect`**: "启动 code-architect subagent 设计一个新的插件系统。"
- **`code-reviewer`**: "启动 code-reviewer subagent 评审我刚才的代码修改。"
- **`shell`**: "启动 shell subagent 处理 Git 合并冲突。"

## 3. 核心流程参考 (Flow Reference)

1.  **Plan**: `SwitchMode(plan)` 制定详细计划。
2.  **Explore**: 使用 `vibe-skill-fetch` 摄取文档。
3.  **Implement**: `SwitchMode(agent)` 编写代码。
4.  **Verify**: 运行 `ReadLints` 和单元测试。
5.  **Maintain**: 更新 `CLAUDE.md` 反映架构和命令变更。
6.  **Review**: 调用 `code-reviewer` 评审。
7.  **Ship**: 提交 PR 并更新文档。

---
*注：所有脚本路径均为相对于项目根目录的路径。*
