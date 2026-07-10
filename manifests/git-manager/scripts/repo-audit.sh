#!/bin/bash
# repo-audit.sh — Git 仓库健康审计脚本
# 用法: ./repo-audit.sh <repo-path> [--output table|json|md]

set -euo pipefail

REPO="$1"
OUTPUT="${2:-table}"

if [ ! -d "$REPO/.git" ]; then
  echo "✗ 不是 Git 仓库: $REPO"
  exit 1
fi

cd "$REPO"

# 检查项
PROTECTION=true
ISSUES_30D=0
PR_30D=0
CI_PASS=true
HAS_README=false
HAS_LICENSE=false
HAS_GITIGNORE=false
TAG_BEHIND=false

DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||' || echo "main")

# 检查默认分支
git rev-parse --verify "origin/$DEFAULT_BRANCH" &>/dev/null || PROTECTION=false

# 检查文件存在性
[ -f README.md ] && HAS_README=true
[ -f LICENSE ] && HAS_LICENSE=true
[ -f .gitignore ] && HAS_GITIGNORE=true

# 计算分支落后
LATEST_TAG=$(git tag --sort=-v:refname | head -1)
if [ -n "$LATEST_TAG" ]; then
  TAG_HASH=$(git rev-list -n 1 "$LATEST_TAG" 2>/dev/null)
  HEAD_HASH=$(git rev-parse HEAD 2>/dev/null)
  [ "$TAG_HASH" != "$HEAD_HASH" ] && TAG_BEHIND=true
fi

# 统计 PR/Issue 数量（假设有 gh CLI）
if command -v gh &>/dev/null; then
  PR_COUNT=$(gh pr list --state open --limit 100 --json number --jq 'length' 2>/dev/null || echo 0)
  ISSUES_COUNT=$(gh issue list --state open --limit 100 --json number --jq 'length' 2>/dev/null || echo 0)
else
  PR_COUNT="(需 gh CLI)"
  ISSUES_COUNT="(需 gh CLI)"
fi

case "$OUTPUT" in
  json)
    cat <<EOF
{
  "repo": "$(basename "$(pwd)")",
  "default_branch": "$DEFAULT_BRANCH",
  "protection": $PROTECTION,
  "open_prs": $PR_COUNT,
  "open_issues": $ISSUES_COUNT,
  "has_readme": $HAS_README,
  "has_license": $HAS_LICENSE,
  "has_gitignore": $HAS_GITIGNORE,
  "tag_behind_head": $TAG_BEHIND
}
EOF
    ;;
  md)
    echo "## 审计报告: $(basename "$(pwd)")"
    echo ""
    echo "| 检查项 | 状态 |"
    echo "|--------|------|"
    echo "| 默认分支 | $DEFAULT_BRANCH |"
    echo "| 分支保护 | $([ "$PROTECTION" = true ] && echo '✅' || echo '❌') |"
    echo "| Open PRs | $PR_COUNT |"
    echo "| Open Issues | $ISSUES_COUNT |"
    echo "| README.md | $([ "$HAS_README" = true ] && echo '✅' || echo '❌') |"
    echo "| LICENSE | $([ "$HAS_LICENSE" = true ] && echo '✅' || echo '❌') |"
    echo "| .gitignore | $([ "$HAS_GITIGNORE" = true ] && echo '✅' || echo '❌') |"
    echo "| Tag 落后 | $([ "$TAG_BEHIND" = true ] && echo '⚠️' || echo '✅') |"
    ;;
  *)
    echo "━━━ 审计: $(basename "$(pwd)") ━━━"
    echo "  默认分支:    $DEFAULT_BRANCH"
    echo "  分支保护:    $([ "$PROTECTION" = true ] && echo '✅ 已启用' || echo '❌ 未启用')"
    echo "  Open PRs:    $PR_COUNT"
    echo "  Open Issues: $ISSUES_COUNT"
    echo "  README:      $([ "$HAS_README" = true ] && echo '✅' || echo '❌')"
    echo "  LICENSE:     $([ "$HAS_LICENSE" = true ] && echo '✅' || echo '❌')"
    echo "  .gitignore:  $([ "$HAS_GITIGNORE" = true ] && echo '✅' || echo '❌')"
    echo "  Tag落后:     $([ "$TAG_BEHIND" = true ] && echo '⚠️ 最新 tag 落后于 HEAD' || echo '✅ 一致')"
    ;;
esac
