# Git 仓库跨平台管理 Manifest

跨平台 Git 仓库管理项目。支持 GitHub、Gitee、自搭建 Git 服务（GitLab、Gitea 等）的仓库同步、镜像、审计与批量操作。

## Commands

| 命令 | 缩写 | 描述 |
|------|------|------|
| `mirror` | `m` | 跨平台仓库同步与镜像 |
| `br` |  | 分支批量管理 |
| `tag` |  | 标签管理（semver 版本晋升） |
| `ci` |  | CI/CD 流水线管理（自动镜像/标签/发布） |
| `audit` | `au` | 仓库健康度审计 |

## Architecture

```
<root>/
  repos/          # 本地仓库副本
  configs/        # 跨平台同步配置
  scripts/        # 自动化脚本（同步、审计、备份、CI 辅助）
  mirrors/        # 镜像映射配置
```

## Environment

| 变量 | 用途 |
|------|------|
| `GITHUB_TOKEN` | GitHub API 令牌 |
| `GITEE_TOKEN` | Gitee API 令牌 |
| `GITLAB_TOKEN` | 自搭建 GitLab API 令牌 |
| `GITEA_TOKEN` | Gitea API 令牌 |

## Conventions

- 仓库命名跨平台保持一致
- 每个平台的默认分支统一为 `main`
- 标签（tag）命名遵循 semver 规范：`v<major>.<minor>.<patch>`
- API 令牌使用环境变量管理，不硬编码
- CI 工作流使用平台原生 Secrets 存储令牌

## Gotchas

- **令牌安全**：API 令牌等同于密码，切勿提交到代码库
- **速率限制**：GitHub 未认证 60 req/h，认证 5000 req/h；Gitee 配额因账户等级而异（标准约 3000 req/h）
- **镜像冲突**：双向同步可能导致冲突，建议主从模式
- **Tag 同步**：`git push --tags` 推送所有标签，确保跨平台一致
- **Webhook 安全**：使用 Secret Token 验证 webhook 请求来源
- **大仓库**：含 LFS 或大文件的仓库镜像可能需要额外配置

## Workflow

1. **分支管理**：使用 `br` 管理分支生命周期（ls → prune → protect）
2. **同步镜像**：使用 `mirror` 跨平台同步分支与标签
3. **版本发布**：使用 `tag promote` 晋升版本 → `ci promote` 触发 CI 发布
4. **CI/CD 自动同步**：使用 `ci setup-mirror` 配置自动镜像流水线
5. **健康审计**：定期运行 `audit` 检查各仓库健康度
