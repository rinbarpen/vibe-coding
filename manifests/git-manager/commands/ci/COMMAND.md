# ci

CI/CD 工作流管理命令。支持跨平台的自动构建、版本发布、镜像同步。

## Usage

```
ci <command> [options]
```

### Commands

| 子命令 | 描述 |
|--------|------|
| `run <repo>` | 触发 CI/CD 流水线 |
| `status <repo>` | 查看最近 CI/CD 运行状态 |
| `setup-mirror <repo>` | 配置 CI 自动镜像同步 |
| `setup-auto-tag <repo>` | 配置 CI 自动版本标签 |
| `promote <repo>` | 自动晋升版本 → 打标签 → 触发 CI 发布 |

### Options

| 选项 | 描述 |
|------|------|
| `--branch <name>` | 指定触发分支（默认当前分支） |
| `--platform <name>` | 目标平台：`github`、`gitee`、`gitlab`（默认自动） |
| `--bump <level>` | 晋升级别（promote 专用）：`patch`、`minor`、`major` |
| `--dry-run` | 模拟运行 |

## Examples

```bash
# 触发 CI 流水线
ci run github/user/repo

# 查看最近 CI 运行状态
ci status github/user/repo

# 配置 GitHub Actions 自动镜像到 Gitee
ci setup-mirror github/user/repo

# 配置 CI 自动打标签（基于 conventional commits）
ci setup-auto-tag github/user/repo

# 晋升版本 → 打 tag → 触发发布流水线
ci promote github/user/repo --bump minor

# 指定分支触发
ci run github/user/repo --branch release/2.0
```

## CI 配置文件说明

### setup-mirror 生成的工作流

```yaml
# .github/workflows/mirror.yml
name: Auto Mirror
on:
  push:
    branches: [main, "release/*"]
    tags: ["v*"]
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

### setup-auto-tag 生成的工作流

```yaml
# .github/workflows/auto-tag.yml
name: Auto Tag
on:
  push:
    branches: [main]
jobs:
  tag:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Auto tag
        uses: anothrNick/github-tag-action@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          DEFAULT_BUMP: patch
          WITH_V: true
```

## Notes

- `promote` 整合了 `tag promote` + `git push` + `ci run` 三步
- 首次使用需确保 CI 平台已认证
- 镜像同步工作流需要先在目标平台配置 Access Token 到 Secrets
