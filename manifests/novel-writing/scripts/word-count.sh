#!/bin/bash
# word-count.sh — 小说字数统计与进度报告
# 用法: ./word-count.sh [--daily] [--target 200000] [--output table|json|markdown]

set -euo pipefail

OUTPUT="${2:-table}"
TARGET=0
DAILY=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --daily) DAILY=true; shift ;;
    --target) TARGET="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    *) break ;;
  esac
done

CHAPTER_DIR="${VIBE_NOVEL_DIR:-.}/chapters"
[ ! -d "$CHAPTER_DIR" ] && { echo "✗ chapters/ 目录不存在"; exit 1; }

TOTAL_WORDS=0
CHAPTER_COUNT=0
CHAPTER_DATA=""

while IFS= read -r FILE; do
  [ -z "$FILE" ] && continue
  WORDS=$(wc -m < "$FILE")
  NAME=$(basename "$FILE" .md)
  TOTAL_WORDS=$((TOTAL_WORDS + WORDS))
  CHAPTER_COUNT=$((CHAPTER_COUNT + 1))
  CHAPTER_DATA="$CHAPTER_DATA{\"name\":\"$NAME\",\"words\":$WORDS,\"path\":\"$FILE\"},"
done < <(find "$CHAPTER_DIR" -name '*.md' -type f | sort)

CHAPTER_DATA="[${CHAPTER_DATA%,}]"

case "$OUTPUT" in
  json)
    jq -n --argjson chapters "$CHAPTER_DATA" \
          --argjson total $TOTAL_WORDS \
          --argjson count $CHAPTER_COUNT \
          --argjson target $TARGET \
          '{total_words: $total, chapter_count: $count, target: $target, chapters: $chapters}'
    ;;
  markdown)
    echo "## 字数统计报告"
    echo ""
    echo "| 章节 | 字数 |"
    echo "|------|:----:|"
    echo "$CHAPTER_DATA" | jq -r '.[] | "| \(.name) | \(.words) |"'
    echo "| **合计** | **$TOTAL_WORDS** |"
    echo ""
    [ "$TARGET" -gt 0 ] && {
      PERCENT=$((TOTAL_WORDS * 100 / TARGET))
      echo "**进度**: $TOTAL_WORDS / $TARGET 字 ($PERCENT%)"
    }
    ;;
  *)
    echo "━━━ 字数统计 ━━━"
    echo "总章节: $CHAPTER_COUNT"
    echo "总字数: $TOTAL_WORDS"
    [ "$TARGET" -gt 0 ] && {
      PERCENT=$((TOTAL_WORDS * 100 / TARGET))
      echo "目标:   $TARGET 字 ($PERCENT%)"
    }
    echo ""
    echo "章节分布:"
    echo "$CHAPTER_DATA" | jq -r '.[] | "  \(.name): \(.words) 字"'
    ;;
esac
