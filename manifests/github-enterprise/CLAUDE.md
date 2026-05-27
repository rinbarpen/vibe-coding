# GitHub Enterprise Development Manifest

## Commands

| Command | Description |
|---------|-------------|
| `git checkout -b feat/42-login` | 创建 feature branch |
| `git commit -m "feat(scope): desc"` | 遵循 Conventional Commits |
| `gh pr create --fill` | 创建 PR |
| `gh pr review --approve` | 批准 PR |
| `gh pr merge --squash` | Squash merge feature branch |
| `git tag -s v1.2.3 -m "v1.2.3"` | 创建 GPG 签名 tag |
| `gh release create v1.2.3` | 创建 GitHub Release |
| `yamllint .github/workflows/*.yml` | 验证 workflow YAML |

## Repository Structure

```
.github/
├── CODEOWNERS                   # 代码所有权
├── CODE_OF_CONDUCT.md           # 行为准则
├── SECURITY.md                  # 安全披露策略
├── dependabot.yml               # 依赖自动更新
├── ISSUE_TEMPLATE/              # Issue 表单模板
├── PULL_REQUEST_TEMPLATE/       # PR 描述模板
└── workflows/                   # CI/CD 工作流
    ├── ci.yml                   # 构建+测试+覆盖率
    ├── deploy-pages.yml         # GitHub Pages 部署
    ├── pr-conventions.yml       # PR 标题/大小/内容检查
    ├── pr-auto-assign.yml       # 自动分配 reviewer
    ├── merge-queue.yml          # 合并队列验证
    ├── release.yml              # 标准发布
    ├── release-branch.yml       # Release branch 管理
    ├── hotfix.yml               # 紧急修复
    ├── issue-triage.yml         # Issue 自动分类
    ├── codeql-analysis.yml      # 安全扫描
    ├── dependency-review.yml    # 依赖审查
    └── stale.yml                # 陈旧 issue/PR 管理

references/                      # 策略参考文档
templates/                       # 项目模板
scripts/                         # 初始化脚本
```

## Enterprise Conventions

### Branch
- 命名：`<type>/<issue-number>-<kebab-description>`
- 示例：`feat/42-user-auth`、`fix/87-npe-on-null`、`hotfix/v1.2.3`、`release/v2.0.0`
- 生命周期：feature 分支合并后自动删除
- 保护规则：main 需要 2 个 review + 所有 status checks 通过 + up-to-date

### PR
- 标题格式：`<type>(<scope>): <description>` — 由 `pr-conventions.yml` 强制
- 大小标签：XS(0-10) / S(11-50) / M(51-200) / L(201-800) / XL(>800)
- 合并策略：feature → squash，release → merge commit，hotfix → merge commit

### Release
- 版本化：SemVer 2.0（MAJOR.MINOR.PATCH）
- CHANGELOG.md 必须维护，Keep-a-Changelog 格式
- 所有 release tag 必须 GPG 签名
- 发布流程：tag push → `release.yml` 触发自动发布

## Key Files

| File | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | 构建、lint、矩阵测试、覆盖率 |
| `.github/workflows/release.yml` | 标准发布流水线 |
| `.github/workflows/hotfix.yml` | 紧急修复流水线 |
| `.github/workflows/pr-conventions.yml` | PR 规范强制 |
| `references/branching-strategy.md` | 分支策略决策指南 |
| `references/release-process.md` | 发布流程详细说明 |
| `references/tag-convention.md` | Tag 命名和保护规则 |
| `references/pr-conventions.md` | PR 规范详细说明 |

## Environment

| Variable | Purpose |
|----------|---------|
| `GITHUB_TOKEN` | 需要 `contents: write` + `pull-requests: write` 权限 |
| `CODECOV_TOKEN` | 覆盖率报告上传 |
| `DOCKER_USERNAME` | Docker Hub 发布 |
| `NPM_TOKEN` / `PYPI_TOKEN` | 包管理器发布 |

## Gotchas

- Merge Queue 冲突：队列中 PR 冲突时需要手动 rebase 并重新加入队列
- workflow 并发：使用 `concurrency` 组防止同一分支重复运行
- 分支保护规则需在 GitHub Web UI 中手动配置，不在代码中管理
- `release.yml` 响应 tag push，不会自动创建 tag — tag 由 release manager 负责
- hotfix 从最近 release tag 创建分支，不可在 release tag 上直接修改
