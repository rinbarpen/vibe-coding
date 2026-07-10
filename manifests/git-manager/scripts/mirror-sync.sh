#!/bin/bash
# mirror-sync.sh — 跨平台 Git 仓库镜像同步脚本
# 用法: ./mirror-sync.sh <source_remote> <target_remote> [mode]
#   mode: mirror (全量) | branch (仅分支) | tag (仅标签)  (默认: branch)

set -euo pipefail

SOURCE="$1"
TARGET="$2"
MODE="${3:-branch}"
WORKDIR="$(mktemp -d)"
TMPDIR="$WORKDIR"

cleanup() {
  rm -rf "$WORKDIR"
}
trap cleanup EXIT

# 克隆源仓库（bare clone 节省空间）
echo "▸ 克隆源仓库: $SOURCE"
git clone --mirror "$SOURCE" "$WORKDIR/repo.git" 2>/dev/null || {
  echo "✗ 克隆失败: $SOURCE"
  exit 1
}

cd "$WORKDIR/repo.git"
git remote add target "$TARGET"

case "$MODE" in
  mirror)
    echo "▸ 全量镜像 → $TARGET"
    git push --mirror target
    ;;
  branch)
    echo "▸ 推送分支 → $TARGET"
    git push --all target
    ;;
  tag)
    echo "▸ 推送标签 → $TARGET"
    git push --tags target
    ;;
  *)
    echo "✗ 未知模式: $MODE (可选: mirror|branch|tag)"
    exit 1
    ;;
esac

echo "✓ 同步完成: $SOURCE → $TARGET (mode=$MODE)"
