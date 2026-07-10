#!/bin/bash
# branch-prune.sh — 批量清理已合并/过期的 Git 分支
# 用法: ./branch-prune.sh <repo-path> [--stale-days 90] [--merged-only] [--dry-run]

set -euo pipefail

REPO="$1"
STALE_DAYS=90
MERGED_ONLY=false
DRY_RUN=false

shift
while [[ $# -gt 0 ]]; do
  case "$1" in
    --stale-days) STALE_DAYS="$2"; shift 2 ;;
    --merged-only) MERGED_ONLY=true; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    *) echo "✗ 未知选项: $1"; exit 1 ;;
  esac
done

if [ ! -d "$REPO/.git" ]; then
  echo "✗ 不是 Git 仓库: $REPO"
  exit 1
fi

cd "$REPO"
DEFAULT_BRANCH="$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||' || echo 'main')"

echo "▸ 仓库: $REPO"
echo "▸ 默认分支: $DEFAULT_BRANCH"
echo "▸ 过期天数: ${STALE_DAYS}d"
echo ""

# 获取远程分支列表
git remote update --prune origin 2>/dev/null || true

BRANCHES=$(git branch -r --merged "origin/$DEFAULT_BRANCH" 2>/dev/null | sed 's/.*origin\///' | grep -v "^$DEFAULT_BRANCH$" | sort -u || true)

DELETED=0
SKIPPED=0

for BRANCH in $BRANCHES; do
  # 跳过保护分支
  case "$BRANCH" in
    main|master|develop|release/*) 
      echo "  ~ 跳过保护分支: $BRANCH"
      ((SKIPPED++)) || true
      continue
      ;;
  esac

  if [ "$MERGED_ONLY" = true ]; then
    echo "  ✓ 已合并: $BRANCH"
    if [ "$DRY_RUN" = false ]; then
      git push origin --delete "$BRANCH" 2>/dev/null && ((DELETED++)) || ((SKIPPED++))
    else
      echo "    [DRY-RUN] 将删除"
      ((DELETED++))
    fi
  else
    LAST_COMMIT=$(git log -1 --format="%ct" "origin/$BRANCH" 2>/dev/null || echo 0)
    NOW=$(date +%s)
    AGE=$(( (NOW - LAST_COMMIT) / 86400 ))
    if [ "$AGE" -gt "$STALE_DAYS" ]; then
      echo "  ✓ ${AGE}d 过期: $BRANCH"
      if [ "$DRY_RUN" = false ]; then
        git push origin --delete "$BRANCH" 2>/dev/null && ((DELETED++)) || ((SKIPPED++))
      else
        echo "    [DRY-RUN] 将删除"
        ((DELETED++))
      fi
    else
      echo "  · ${AGE}d 活跃: $BRANCH (跳过)"
      ((SKIPPED++)) || true
    fi
  fi
done

echo ""
echo "━━━ 清理报告 ━━━"
echo "  已删除: $DELETED"
echo "  已跳过: $SKIPPED"
if [ "$DRY_RUN" = true ]; then
  echo "  模式: DRY-RUN (未实际删除)"
fi
