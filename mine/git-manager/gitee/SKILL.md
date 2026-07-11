---
name: git-manager-gitee
description: |
  Gitee (码云, gitee.com) repository management via OpenAPI v5.
  Repo CRUD, Pull Requests, issues, releases, Gitee Pages, and
  GitHub-to-Gitee mirror sync. Requires GITEE_TOKEN.
---

# Git Manager — Gitee (码云)

通过 Gitee OpenAPI v5 管理码云仓库资源。

## Prerequisites

```bash
# 1. 在 https://gitee.com/profile/personal_access_tokens 生成 token
# 2. 配置环境变量
export GITEE_TOKEN="your_personal_access_token"

# 3. 验证 token 是否有效（应返回你的用户名）
GITEE_TOKEN="your_token"
curl -s https://gitee.com/api/v5/user \
  -H "Content-Type: application/json" \
  -H "Authorization: token $GITEE_TOKEN"
```

> 快捷脚本：见 [scripts/gitee_api.sh](scripts/gitee_api.sh)，自动处理 header 和错误检查。

## Repository Operations

```bash
OWNER="your_username"
REPO="repo-name"

# 查看仓库信息
curl -s "https://gitee.com/api/v5/repos/$OWNER/$REPO" \
  -H "Authorization: token $GITEE_TOKEN"

# 创建仓库（用户下）
curl -s -X POST "https://gitee.com/api/v5/user/repos" \
  -H "Authorization: token $GITEE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"'$REPO'","description":"description","auto_init":true}'

# 创建组织仓库
curl -s -X POST "https://gitee.com/api/v5/orgs/$ORG/repos" \
  -H "Authorization: token $GITEE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"'$REPO'","private":true}'

# 删除仓库
curl -s -X DELETE "https://gitee.com/api/v5/repos/$OWNER/$REPO" \
  -H "Authorization: token $GITEE_TOKEN"

# 搜索仓库
curl -s "https://gitee.com/api/v5/search/repositories?q=$KEYWORD&page=1&per_page=20" \
  -H "Authorization: token $GITEE_TOKEN"

# 查看用户所有仓库
curl -s "https://gitee.com/api/v5/users/$OWNER/repos?page=1&per_page=20" \
  -H "Authorization: token $GITEE_TOKEN"
```

## Pull Request Management

```bash
# 列出 PR
curl -s "https://gitee.com/api/v5/repos/$OWNER/$REPO/pulls?state=open&page=1&per_page=20" \
  -H "Authorization: token $GITEE_TOKEN"

# 创建 PR
curl -s -X POST "https://gitee.com/api/v5/repos/$OWNER/$REPO/pulls" \
  -H "Authorization: token $GITEE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"PR title",
    "body":"PR description",
    "head":"feature-branch",
    "base":"main",
    "assignees":"username",
    "labels":"enhancement"
  }'

# 合并 PR
curl -s -X POST "https://gitee.com/api/v5/repos/$OWNER/$REPO/pulls/$PULL_NUMBER/merge" \
  -H "Authorization: token $GITEE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"merge_method":"merge"}'  # merge / squash / rebase

# 查看 PR 详情
curl -s "https://gitee.com/api/v5/repos/$OWNER/$REPO/pulls/$PULL_NUMBER" \
  -H "Authorization: token $GITEE_TOKEN"

# 查看 PR 文件变更
curl -s "https://gitee.com/api/v5/repos/$OWNER/$REPO/pulls/$PULL_NUMBER/files" \
  -H "Authorization: token $GITEE_TOKEN"
```

## Issue Management

```bash
# 创建 issue
curl -s -X POST "https://gitee.com/api/v5/repos/$OWNER/$REPO/issues" \
  -H "Authorization: token $GITEE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"issue title",
    "body":"issue description",
    "labels":"bug",
    "assignees":"username"
  }'

# 列出 issues
curl -s "https://gitee.com/api/v5/repos/$OWNER/$REPO/issues?state=open&page=1&per_page=20" \
  -H "Authorization: token $GITEE_TOKEN"

# 更新 issue 状态（关闭）
curl -s -X PATCH "https://gitee.com/api/v5/repos/$OWNER/$REPO/issues/$ISSUE_NUMBER" \
  -H "Authorization: token $GITEE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"state":"closed"}'

# 添加评论
curl -s -X POST "https://gitee.com/api/v5/repos/$OWNER/$REPO/issues/$ISSUE_NUMBER/comments" \
  -H "Authorization: token $GITEE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"body":"comment text"}'
```

## Releases

```bash
# 创建 release
curl -s -X POST "https://gitee.com/api/v5/repos/$OWNER/$REPO/releases" \
  -H "Authorization: token $GITEE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tag_name":"v1.0.0",
    "name":"v1.0.0",
    "body":"release notes",
    "prerelease":false
  }'

# 列出 releases
curl -s "https://gitee.com/api/v5/repos/$OWNER/$REPO/releases?page=1&per_page=20" \
  -H "Authorization: token $GITEE_TOKEN"

# 删除 release
curl -s -X DELETE "https://gitee.com/api/v5/repos/$OWNER/$REPO/releases/$RELEASE_ID" \
  -H "Authorization: token $GITEE_TOKEN"
```

## Gitee Pages

```bash
# 部署 Pages
curl -s -X POST "https://gitee.com/api/v5/repos/$OWNER/$REPO/pages/build" \
  -H "Authorization: token $GITEE_TOKEN"

# 查看 Pages 配置
curl -s "https://gitee.com/api/v5/repos/$OWNER/$REPO/pages" \
  -H "Authorization: token $GITEE_TOKEN"
```

## Common Workflows

### GitHub → Gitee 镜像同步

```bash
# 添加 Gitee 作为第二个 remote
git remote add gitee https://gitee.com/$OWNER/$REPO.git

# 推送所有分支
git push gitee --all
git push gitee --tags

# 或在 Gitee 仓库设置中开启 "强制同步"（Gitee 内置功能）
# 路径：仓库 → 管理 → 仓库设置 → 强制同步（需配置 GitHub 仓库地址）
```

### 批量操作：fork 所有组织仓库

```bash
ORG="organization"
curl -s "https://gitee.com/api/v5/orgs/$ORG/repos?page=1&per_page=100" \
  -H "Authorization: token $GITEE_TOKEN" | \
  python3 -c "
import sys, json
for r in json.load(sys.stdin):
    print(f\"{r['full_name']} - {r['html_url']}\")
  "
```
