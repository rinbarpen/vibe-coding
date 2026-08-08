#!/usr/bin/env bash
# 在 skills 目录下所有 Git 仓库执行 git pull
# 用法: ./scripts/skills-git-pull.sh

set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

failed=""
skipped=""
for dir in skills/*/; do
  [ -e "${dir}.git" ] || continue
  name=$(basename "$dir")
  case "$name" in
    agent-skills|ai-investment-advisor)
      echo "--- Skipping unmanaged: $name ---"
      skipped="$skipped $name"
      echo ""
      continue
      ;;
  esac
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
if [ -n "$skipped" ]; then
  echo "Skipped unmanaged repos:$skipped"
fi
if [ -n "$failed" ]; then
  echo "Failed repos:$failed"
  exit 1
else
  echo "All repos pulled successfully"
fi
