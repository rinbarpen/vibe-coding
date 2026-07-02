# GitHub Workflows

## Common CLI Commands

```bash
# 认证
gh auth login
gh auth status

# 仓库操作
gh repo list <user> --limit 100
gh repo create <name> --public --clone
gh repo fork <repo> --clone
gh repo archive <repo> --yes

# 分支与 PR
gh pr list --state open --limit 50
gh pr create --title "feat: ..." --body "..." --base main
gh pr merge <number> --merge --delete-branch
gh pr review <number> --approve

# Issue
gh issue list --state open --limit 50
gh issue create --title "..." --body "..."

# Release
gh release list --limit 20
gh release create v1.0.0 --title "v1.0.0" --notes "..."

# Actions
gh run list --limit 10
gh run watch <run-id>
gh workflow list
```

## API Rate Limits

| 认证状态 | 每小时请求数 |
|----------|-------------|
| 未认证 | 60 |
| 认证 (Token) | 5000 |

## Mirror Setup with GitHub Actions

```yaml
# .github/workflows/mirror.yml
name: Mirror to Gitee
on:
  push:
    branches: [main]
jobs:
  mirror:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Push to Gitee
        run: |
          git remote add gitee https://${{ secrets.GITEE_TOKEN }}@gitee.com/user/repo.git
          git push --all gitee
          git push --tags gitee
```

## Branch Protection API

```bash
# 启用分支保护
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --input - <<< '{
    "required_status_checks": {"strict": true, "contexts": ["continuous-integration"]},
    "enforce_admins": true,
    "required_pull_request_reviews": {"required_approving_review_count": 1}
  }'
```
