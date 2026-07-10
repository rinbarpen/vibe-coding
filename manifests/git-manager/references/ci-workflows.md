# CI/CD 工作流参考

> ⚠️ **参考文件定位**：本文件聚焦**多工作流协同编排**和**高级 CI/CD 模式**。
> 各平台的单工作流模板（镜像、自动标签、发布）已分别放在：
> - `github-workflows.md` — GitHub Actions 专属
> - `gitee-workflows.md` — Gitee Go / API 专属
> - `self-hosted-git.md` — GitLab / Gitea 专属

---

## 多平台综合编排

以下是一个在 GitHub 上实现**镜像 + 自动标签 + 发布**三合一的工作流：

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main, "release/*"]
    tags: ["v*"]
  pull_request:
    branches: [main]

jobs:
  # 主 CI 流程
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: echo "Tests passed"

  # main 分支推送时自动打 tag
  auto-tag:
    if: github.ref == 'refs/heads/main'
    needs: ci
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: anothrNick/github-tag-action@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          DEFAULT_BUMP: patch
          WITH_V: true

  # 推 tag 时发布 Release
  release:
    if: startsWith(github.ref, 'refs/tags/v')
    needs: ci
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
```

## 多源镜像（GitHub → Gitee + GitLab + Gitea）

```yaml
# .github/workflows/multi-mirror.yml
name: Multi-Platform Mirror
on:
  push:
    branches: [main, "release/*"]
    tags: ["v*"]

jobs:
  mirror-to-gitee:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Push to Gitee
        run: |
          git remote add gitee https://${{ secrets.GITEE_TOKEN }}@gitee.com/${{ github.repository }}.git
          git push --all gitee
          git push --tags gitee

  mirror-to-gitlab:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Push to GitLab
        run: |
          git remote add gitlab https://oauth2:${{ secrets.GITLAB_TOKEN }}@gitlab.example.com/${{ github.repository }}.git
          git push --all gitlab
          git push --tags gitlab
```

## 条件发布（手动审批门禁）

```yaml
# .github/workflows/release-with-approval.yml
name: Release (Manual Gate)
on:
  workflow_dispatch:
    inputs:
      bump:
        description: "Version bump level"
        default: "patch"
        type: choice
        options: [patch, minor, major]

jobs:
  # 1. 版本晋升（自动计算）
  bump:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.bump.outputs.version }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - id: bump
        run: |
          LATEST=$(git tag --sort=-v:refname | head -1)
          [ -z "$LATEST" ] && LATEST="v0.0.0"
          IFS='.' read -r M m p <<< "${LATEST#v}"
          case "${{ inputs.bump }}" in
            major) echo "version=v$((M+1)).0.0"  ;;
            minor) echo "version=v${M}.$((m+1)).0" ;;
            patch) echo "version=v${M}.${m}.$((p+1))" ;;
          esac >> $GITHUB_OUTPUT

  # 2. 人工审批门禁（需要有人在 GitHub 上 approve）
  approve:
    runs-on: ubuntu-latest
    needs: bump
    environment: release-approval
    steps:
      - run: echo "✅ Approved by ${{ github.actor }}"

  # 3. 创建 tag + release
  release:
    runs-on: ubuntu-latest
    needs: [bump, approve]
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - name: Tag
        run: |
          git tag ${{ needs.bump.outputs.version }}
          git push origin ${{ needs.bump.outputs.version }}
      - uses: softprops/action-gh-release@v2
        with:
          tag_name: ${{ needs.bump.outputs.version }}
          generate_release_notes: true
```

## CICD 发布流水线：完整发布策略

```
test ──→ tag promote ──→ ci run ──→ release
  ↑            ↑              ↑           ↑
 单元测试   版本晋升       触发构建   发布 Release
 集成测试   自动 bump      CI 通过    Release Notes
 lint 检查   push tag      deploy     通知
```

## GitLab CI 镜像 → GitHub

```yaml
# .gitlab-ci.yml
stages:
  - mirror

mirror-to-github:
  stage: mirror
  only:
    - main
    - tags
  script:
    - git remote add github https://$GITHUB_TOKEN@github.com/user/repo.git
    - git push --all github
    - git push --tags github
```

## 关键点

- **Token 安全**：所有 Token 使用 GitHub Secrets / Gitee Secrets 管理，勿硬编码
- **fetch-depth: 0**：镜像/标签操作需要完整 git 历史
- **权限配置**：自动标签需要 `contents: write` 权限
- **镜像触发**：建议按分支过滤，避免临时分支触发不必要的同步
- **标签同步**：`git push --tags` 确保标签跨平台同步
- **环境门禁**：使用 GitHub Environments + required reviewers 实现发布审批
- **Gitea 兼容**：Gitea 兼容 GitHub API，可用 `gh` CLI + 自定义端点操作
