# CI/CD 工作流参考

## 自动镜像同步

### GitHub Actions → Gitee

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

### GitLab CI → GitHub

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

## 自动版本标签

### 基于 Conventional Commits 自动 bump

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
      - name: Bump version and push tag
        uses: anothrNick/github-tag-action@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          DEFAULT_BUMP: patch
          WITH_V: true
      # 或手动计算：
      # - name: Manual bump
      #   run: |
      #     LATEST=$(git tag --sort=-v:refname | head -1)
      #     [ -z "$LATEST" ] && LATEST="v0.0.0"
      #     NEW=$(echo $LATEST | awk -F. '{$NF+=1; print $1"."$2"."$NF}')
      #     git tag $NEW
      #     git push origin $NEW
```

### Gitee Go 自动标签

```yaml
# .gitee/workflows/auto-tag.yml
name: Auto Tag
on:
  push:
    branches: [main]
jobs:
  tag:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Bump version
        run: |
          # 安装 gitee-api 工具或使用 curl
          LATEST_TAG=$(curl -s "https://gitee.com/api/v5/repos/$GITEE_REPO/tags" \
            -H "Authorization: Bearer $GITEE_TOKEN" | jq -r '.[0].name')
          echo "Latest tag: $LATEST_TAG"
          # ... bump and create tag via Gitee API
```

## 版本晋升 + 发布流水线

```yaml
# .github/workflows/release.yml
name: Release
on:
  workflow_dispatch:
    inputs:
      bump:
        description: "Version bump level"
        required: true
        default: "patch"
        type: choice
        options: [patch, minor, major]

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Bump version
        id: bump
        run: |
          LATEST=$(git tag --sort=-v:refname | head -1)
          [ -z "$LATEST" ] && LATEST="v0.0.0"
          IFS='.' read -r major minor patch <<< "${LATEST#v}"
          case "${{ inputs.bump }}" in
            major) MAJOR=$((major+1)); MINOR=0; PATCH=0 ;;
            minor) MAJOR=$major; MINOR=$((minor+1)); PATCH=0 ;;
            patch) MAJOR=$major; MINOR=$minor; PATCH=$((patch+1)) ;;
          esac
          echo "version=v${MAJOR}.${MINOR}.${PATCH}" >> $GITHUB_OUTPUT

      - name: Create tag
        run: |
          git tag ${{ steps.bump.outputs.version }}
          git push origin ${{ steps.bump.outputs.version }}

      - name: Create Release
        uses: softprops/action-gh-release@v2
        with:
          tag_name: ${{ steps.bump.outputs.version }}
          generate_release_notes: true
```

## GitHub Actions 综合示例

同时包含镜像 + 自动标签 + 发布：

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

## 关键点

- **Token 安全**：所有 Token 使用 GitHub Secrets / Gitee Secrets 管理，勿硬编码
- **fetch-depth: 0**：镜像/标签操作需要完整 git 历史
- **权限配置**：自动标签需要 `contents: write` 权限
- **镜像触发**：建议按分支过滤，避免临时分支触发不必要的同步
- **标签同步**：`git push --tags` 确保标签跨平台同步
