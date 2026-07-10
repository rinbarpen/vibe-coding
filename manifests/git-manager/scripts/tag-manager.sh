#!/bin/bash
# tag-manager.sh — 标签管理（semver 版本晋升、同步、清理）
# 用法: ./tag-manager.sh <repo-path> <command> [options]
#   command: list | promote | prune | diff

set -euo pipefail

REPO="$1"
CMD="${2:-list}"
shift 2 || true

if [ ! -d "$REPO/.git" ]; then
  echo "✗ 不是 Git 仓库: $REPO"
  exit 1
fi

cd "$REPO"
git fetch --tags origin 2>/dev/null || true

case "$CMD" in
  list)
    echo "▸ 标签列表:"
    git tag --sort=-v:refname | head -20
    echo ""
    TOTAL=$(git tag | wc -l)
    echo "共 $TOTAL 个标签"
    ;;

  promote)
    BUMP="${1:-patch}"
    LATEST=$(git tag --sort=-v:refname | head -1)
    if [ -z "$LATEST" ]; then
      NEW_TAG="v0.1.0"
    else
      IFS='.' read -r MAJOR MINOR PATCH <<< "${LATEST#v}"
      case "$BUMP" in
        major) MAJOR=$((MAJOR+1)); MINOR=0; PATCH=0 ;;
        minor) MAJOR=$MAJOR; MINOR=$((MINOR+1)); PATCH=0 ;;
        patch) MAJOR=$MAJOR; MINOR=$MINOR; PATCH=$((PATCH+1)) ;;
        *) echo "✗ 未知 bump: $BUMP (patch|minor|major)"; exit 1 ;;
      esac
      NEW_TAG="v${MAJOR}.${MINOR}.${PATCH}"
    fi
    echo "▸ 最新标签: ${LATEST:-无}"
    echo "▸ 新标签:   $NEW_TAG (bump=$BUMP)"
    git tag -a "$NEW_TAG" -m "Release $NEW_TAG"
    git push origin "$NEW_TAG"
    echo "✓ 标签 $NEW_TAG 已创建并推送"
    ;;

  prune)
    PATTERN="${1:-}"
    if [ -z "$PATTERN" ]; then
      echo "✗ 需要指定模式匹配（如 'v1.0.0-rc*'）"
      exit 1
    fi
    echo "▸ 删除匹配 '$PATTERN' 的标签:"
    for TAG in $(git tag -l "$PATTERN"); do
      echo "  删除: $TAG"
      git push origin --delete "$TAG" 2>/dev/null || true
      git tag -d "$TAG" 2>/dev/null || true
    done
    echo "✓ 清理完成"
    ;;

  diff)
    REMOTE="${1:-origin}"
    echo "▸ 对比本地 vs $REMOTE:"
    LOCAL_TAGS=$(git tag | sort)
    REMOTE_TAGS=$(git ls-remote --tags "$REMOTE" 2>/dev/null | grep -v '\^{}' | sed 's|.*refs/tags/||' | sort || true)
    ONLY_LOCAL=$(comm -23 <(echo "$LOCAL_TAGS") <(echo "$REMOTE_TAGS"))
    ONLY_REMOTE=$(comm -13 <(echo "$LOCAL_TAGS") <(echo "$REMOTE_TAGS"))
    [ -n "$ONLY_LOCAL" ]  && echo "  仅本地: $ONLY_LOCAL"  || echo "  仅本地: (无)"
    [ -n "$ONLY_REMOTE" ] && echo "  仅远端: $ONLY_REMOTE" || echo "  仅远端: (无)"
    ;;

  *)
    echo "用法: $0 <repo-path> <command> [options]"
    echo "  command: list | promote [patch|minor|major] | prune <pattern> | diff"
    exit 1
    ;;
esac
