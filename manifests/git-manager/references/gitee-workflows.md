# Gitee Workflows

## API 基础

Gitee Open API 端点：`https://gitee.com/api/v5/`

```bash
# 认证方式：在请求中携带 access_token 参数
# 或通过 Authorization: Bearer <token> header
```

## Common API Calls

```bash
# 获取用户仓库列表
curl -s "https://gitee.com/api/v5/users/{username}/repos?access_token=$GITEE_TOKEN&type=owner&sort=updated&per_page=100"

# 创建仓库
curl -s -X POST "https://gitee.com/api/v5/user/repos?access_token=$GITEE_TOKEN" \
  -d "name=repo-name&description=..." \
  -d "private=false&has_issues=true&has_wiki=true"

# 获取仓库信息
curl -s "https://gitee.com/api/v5/repos/{owner}/{repo}?access_token=$GITEE_TOKEN"

# 列出 Pull Requests
curl -s "https://gitee.com/api/v5/repos/{owner}/{repo}/pulls?access_token=$GITEE_TOKEN&state=open"

# 创建 Pull Request
curl -s -X POST "https://gitee.com/api/v5/repos/{owner}/{repo}/pulls?access_token=$GITEE_TOKEN" \
  -d "title=..." -d "head=feature-branch&base=main"

# 获取仓库分支
curl -s "https://gitee.com/api/v5/repos/{owner}/{repo}/branches?access_token=$GITEE_TOKEN"

# 创建标签
curl -s -X POST "https://gitee.com/api/v5/repos/{owner}/{repo}/tags?access_token=$GITEE_TOKEN" \
  -d "tag_name=v1.0.0&ref=main&message=..."
```

## API Rate Limits

| 认证状态 | 每小时请求数（按账户等级） |
|----------|--------------------------|
| 未认证 | 60 |
| 认证 (Token, 标准) | ~3000 |
| 认证 (Token, 专业) | ~5000 |

> 具体配额请参考 Gitee API 官方文档：https://gitee.com/api/v5/swagger

## Gitee Webhook

Gitee Webhook 支持事件类型：Push、Pull Request、Issue、Tag Push、Note 等。

Webhook 配置路径：仓库 → 管理 → WebHooks

## 与 GitHub 的差异

| 功能 | GitHub | Gitee |
|------|--------|-------|
| CLI 工具 | `gh` | 无官方 CLI（使用 Open API） |
| Pull Request 术语 | PR | PR（与 GitHub 相同） |
| CI/CD | Actions | Gitee Go |
| Pages | GitHub Pages | Gitee Pages |
| 最大仓库大小 | 100MB (推荐) | 1GB |
| 私有仓库 | 免费 (有限制) | 免费 |
