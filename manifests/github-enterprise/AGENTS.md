# Agent Instructions for Enterprise Development

## Core Flow

### Phase 1: Plan
- 所有开发必须由 Issue 或 PR 驱动
- 开始前先阅读 CONTRIBUTING.md 和相关参考资料
- 确认分支策略（GitHub Flow / Git Flow / Trunk-based）

### Phase 2: Branch
- 从 main 创建分支，遵守 `<type>/<issue>-<desc>` 命名规范
- 分支生命周期短（不超过 1 周），避免长期分支

### Phase 3: Implement
- Incremental commits，每个 commit 有 meaningful message
- 遵循 Conventional Commits 格式
- 保持测试覆盖率和代码质量标准

### Phase 4: Pull Request
- 严格按 PR 模板填写：description、checklist、testing
- 等待 CI 全部通过
- Draft PR 用于 WIP 状态，ready 后标记为 Ready for Review

### Phase 5: Review
- CODEOWNERS 自动分配 reviewer
- 必须解决所有 conversation 后才能合并
- 安全相关改动必须有 security-reviewer 参与

### Phase 6: Ship
- feature branch → squash merge（保持 main 历史清晰）
- release branch → merge commit（保留发布记录）
- hotfix branch → merge commit（保留修复记录）
- 合并后自动删除源分支

## Subagent Dispatching

| Agent | When | Responsibility |
|-------|------|----------------|
| code-architect | 涉及架构变更的 PR | 审查设计决策、模块边界 |
| code-reviewer | 所有 PR | 代码质量、模式一致性 |
| security-reviewer | auth/支付/数据处理 | 安全检查 |
| ci-watcher | PR 提交后 | 监控 CI 状态直到通过 |

## Release Management Rules

1. 只有 release manager 可以创建和推送 tag
2. 所有发布版本必须在 CHANGELOG.md 中有对应条目
3. Hotfix 必须走 hotfix branch 流程，不可在 release tag 上直接修改
4. 版本号必须一致：git tag = package version = CHANGELOG entry
5. Release tag 必须 GPG 签名

## Security Management

- SECURITY.md 定义了完整的漏洞披露流程
- CodeQL 分析在每次 PR 和每周定时执行
- Dependabot 自动创建依赖更新 PR
- Dependency Review 在每次 PR 中检查 license 和已知漏洞
- Critical 级别的安全 issue 自动通知 project owner
