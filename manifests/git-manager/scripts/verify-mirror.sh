#!/bin/bash
# verify-mirror.sh — 验证镜像同步完整性
# 用法: ./verify-mirror.sh <source_remote> <target_remote>
# 返回: 列出差异的分支和标签，无输出 = 完全一致

set -euo pipefail

SOURCE="$1"
TARGET="$2"
WORKDIR="$(mktemp -d)"
PASS=true

cleanup() {
  rm -rf "$WORKDIR"
}
trap cleanup EXIT

echo "▸ 源:   $SOURCE"
echo "▸ 目标: $TARGET"
echo ""

# 克隆两个仓库的 bare copy
git clone --bare --quiet "$SOURCE" "$WORKDIR/source.git"
git clone --bare --quiet "$TARGET" "$WORKDIR/target.git"

echo "━━━ 分支对比 ━━━"
SOURCE_BRANCHES=$(cd "$WORKDIR/source.git" && git branch -a | sed 's/.*\///' | sort -u)
TARGET_BRANCHES=$(cd "$WORKDIR/target.git" && git branch -a | sed 's/.*\///' | sort -u)
MISSING_BRANCHES=$(comm -23 <(echo "$SOURCE_BRANCHES") <(echo "$TARGET_BRANCHES"))
EXTRA_BRANCHES=$(comm -13 <(echo "$SOURCE_BRANCHES") <(echo "$TARGET_BRANCHES"))

[ -z "$MISSING_BRANCHES" ] && echo "  ✓ 无缺失分支" || { echo "  ✗ 目标缺少分支:"; echo "$MISSING_BRANCHES" | sed 's/^/    /'; PASS=false; }
[ -z "$EXTRA_BRANCHES" ]  && echo "  ✓ 无多余分支" || { echo "  ⚠ 目标多出分支:"; echo "$EXTRA_BRANCHES" | sed 's/^/    /'; }

echo ""
echo "━━━ 标签对比 ━━━"
SOURCE_TAGS=$(cd "$WORKDIR/source.git" && git tag | sort)
TARGET_TAGS=$(cd "$WORKDIR/target.git" && git tag | sort)
MISSING_TAGS=$(comm -23 <(echo "$SOURCE_TAGS") <(echo "$TARGET_TAGS"))
EXTRA_TAGS=$(comm -13 <(echo "$SOURCE_TAGS") <(echo "$TARGET_TAGS"))

[ -z "$MISSING_TAGS" ] && echo "  ✓ 标签一致" || { echo "  ✗ 目标缺少标签:"; echo "$MISSING_TAGS" | sed 's/^/    /'; PASS=false; }
[ -z "$EXTRA_TAGS" ]   && echo "  ✓ 无多余标签" || { echo "  ⚠ 目标多出标签:"; echo "$EXTRA_TAGS" | sed 's/^/    /'; }

echo ""
if [ "$PASS" = true ]; then
  echo "✅ 镜像完整一致"
else
  echo "❌ 镜像存在差异，请运行 mirror-sync.sh 补全"
  exit 1
fi
