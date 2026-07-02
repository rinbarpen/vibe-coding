# Self-Hosted Git 服务

## 常见自搭建服务

| 服务 | 语言 | 特点 |
|------|------|------|
| GitLab CE | Ruby | 功能最全，内置 CI/CD，社区版免费 |
| Gitea | Go | 轻量级，资源占用低，兼容 GitHub API |
| GitBucket | Scala | 类 GitHub 界面，JVM 部署 |
| Onedev | Java | 内置 CI/CD 和看板 |

## GitLab CE

```bash
# 通过 GitLab API 创建仓库
curl -s -X POST "https://gitlab.example.com/api/v4/projects" \
  -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  -d "name=repo-name&visibility=public"

# 列出用户仓库
curl -s "https://gitlab.example.com/api/v4/projects?membership=true&per_page=100" \
  -H "PRIVATE-TOKEN: $GITLAB_TOKEN"

# 创建 Merge Request
curl -s -X POST "https://gitlab.example.com/api/v4/projects/{id}/merge_requests" \
  -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  -d "source_branch=feature&target_branch=main&title=..."
```

### GitLab CI 镜像同步

```yaml
# .gitlab-ci.yml
mirror-to-github:
  stage: deploy
  only:
    - main
  script:
    - git remote add github https://$GITHUB_TOKEN@github.com/user/repo.git
    - git push --all github
    - git push --tags github
```

## Gitea

Gitea 兼容大部分 GitHub API，可直接使用 `gh` CLI（需配置自定义端点）。

```bash
# 配置 gh 使用 Gitea
gh config set -h gitea.example.com git_protocol ssh

# 通过 Gitea API 操作
curl -s "https://gitea.example.com/api/v1/repos/{owner}/{repo}" \
  -H "Authorization: token $GITEA_TOKEN"

# 创建仓库
curl -s -X POST "https://gitea.example.com/api/v1/user/repos" \
  -H "Authorization: token $GITEA_TOKEN" \
  -d '{"name": "repo-name", "private": false}'
```

## 通用注意事项

- 自搭建服务需要额外维护备份策略
- API 端点地址不同，需要在配置中灵活处理
- 速率限制通常由管理员配置或不做限制
- SSL 证书可能是自签名的，curl 需要 `-k` 或配置 CA
- SSH 端口可能不是 22，需配置 `~/.ssh/config`
