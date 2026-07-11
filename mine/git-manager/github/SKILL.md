---
name: git-manager-github
description: |
  GitHub repository and project management via gh CLI 2.89+.
  PRs, issues, Actions workflows, releases, secrets, variables, branch protection,
  repo admin, and common multi-step operations. Works with GitHub.com and
  GitHub Enterprise Server.
---

# Git Manager — GitHub

基于 `gh` CLI（v2.89.0 已安装）管理 GitHub 资源。`gh` 覆盖了 GitHub REST API 和 GraphQL 的常用功能，无需直接拼接 curl。

## Authentication

```bash
# 检查认证状态
gh auth status

# 登录（Web 浏览器交互或 token 方式）
gh auth login

# 查看当前用户
gh api user --jq .login
```

## Repository Operations

| 操作 | 命令 |
|------|------|
| 克隆 | `gh repo clone owner/repo [dir]` |
| 创建 | `gh repo create name --public/--private [--clone]` |
| Fork | `gh repo fork owner/repo --clone` |
| 查看 | `gh repo view owner/repo [--web]` |
| 列表 | `gh repo list owner [--limit 50]` |
| 删除 | `gh repo delete owner/repo` |
| 归档 | `gh api -X PATCH repos/owner/repo -F archived=true` |
| 重命名 | `gh api -X PATCH repos/owner/repo -F name=new-name` |

## Issue Management

```bash
# 创建 issue
gh issue create --title "title" --body "body" --assignee @me --label bug

# 列出（支持 --search, --label, --state, --author 过滤）
gh issue list --state open --limit 20

# 查看详情
gh issue view <number> [--comments]

# 关闭
gh issue close <number> [--comment "reason"]

# 重新打开
gh issue reopen <number>

# 添加评论
gh issue comment <number> --body "comment text"

# 编辑
gh issue edit <number> --title "new title" --body "new body"
```

## Pull Request Management

```bash
# 创建 PR
gh pr create --title "title" --body "body" --base main --head branch \
  --reviewer @me --assignee @me --label enhancement

# 列出现有 PR
gh pr list --state open --limit 20

# 查看详情（包括 diff）
gh pr view <number>
gh pr diff <number>

# 审阅
gh pr review <number> --approve
gh pr review <number> --comment --body "feedback"
gh pr review <number> --request-changes --body "reason"

# 合并
gh pr merge <number> --merge/--squash/--rebase [--delete-branch]

# 关闭（不合并）
gh pr close <number>

# 检出 PR 到本地
gh pr checkout <number>
```

## Actions (CI/CD)

```bash
# 列出 workflow runs
gh run list --limit 10 --workflow <name>

# 查看 run 详情与日志
gh run view <run-id>
gh run view <run-id> --log

# 触发 workflow_dispatch
gh workflow run <workflow-name> -f param=value

# 等待完成并查看结果
gh run watch <run-id>

# 取消
gh run cancel <run-id>

# 重新执行
gh run rerun <run-id> [--failed]
```

## Releases

```bash
# 创建 release
gh release create v1.0.0 --title "v1.0.0" --notes "release notes" \
  ./dist/artifact.zip

# 列出
gh release list --limit 10

# 查看
gh release view v1.0.0

# 下载
gh release download v1.0.0 --dir ./output

# 删除
gh release delete v1.0.0
```

## Secrets & Variables

```bash
# 设置 repository secret
gh secret set MY_SECRET --body "value"

# 设置 environment secret
gh secret set MY_SECRET --env production --body "value"

# 列出
gh secret list

# 删除
gh secret delete MY_SECRET

# Variables (非敏感配置)
gh variable set MY_VAR --body "value"
gh variable list
```

## Branch Protection

```bash
# 查看当前保护规则
gh api repos/owner/repo/branches/main/protection

# 设置保护规则（要求 PR 审查）
gh api -X PUT repos/owner/repo/branches/main/protection \
  -F required_status_checks='{"strict":true,"contexts":["continuous-integration"]}' \
  -F enforce_admins=true \
  -F required_pull_request_reviews='{"required_approving_review_count":1}'

# 删除保护
gh api -X DELETE repos/owner/repo/branches/main/protection
```

## Common Workflows

### Fork + Sync 上游
```bash
gh repo fork upstream/repo --clone
cd repo
git remote add upstream https://github.com/upstream/repo.git
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 批量关闭已合并的旧 issue
```bash
gh issue list --state open --label stale --json number --jq '.[].number' | \
  xargs -I{} gh issue close {} --comment "Auto-closing stale issue"
```

### 使用 GitHub Enterprise
```bash
# 配置 GHE 主机
gh auth login --hostname github.example.com

# 后续命令自动使用 GHE 实例
gh repo list --limit 50
```
