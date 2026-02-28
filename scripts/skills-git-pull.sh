#!/usr/bin/env bash
# 在 skills 目录下所有 Git 仓库执行 git pull
# 用法: ./scripts/skills-git-pull.sh

set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failed=""
for dir in skills/*/; do
  [ -e "${dir}.git" ] || continue
  name=$(basename "$dir")
  echo "--- Pulling: $name ---"
  if (cd "$dir" && git pull); then
    echo "OK: $name"
  else
    echo "FAILED: $name"
    failed="$failed $name"
  fi
  echo ""
done

echo "=== Summary ==="
if [ -n "$failed" ]; then
  echo "Failed repos:$failed"
  exit 1
else
  echo "All repos pulled successfully"
fi
