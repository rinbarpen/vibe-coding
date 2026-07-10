#!/bin/bash
# foreshadow-tracker.sh — 伏笔追踪管理脚本
# 用法: ./foreshadow-tracker.sh <command> [options]
#   command: list | add | close | report

set -euo pipefail

TRACKER_FILE="${VIBE_NOVEL_DIR:-.}/.vibe-foreshadow.json"

init_tracker() {
  if [ ! -f "$TRACKER_FILE" ]; then
    echo '{"foreshadows": []}' > "$TRACKER_FILE"
  fi
}

CMD="${1:-list}"
init_tracker

case "$CMD" in
  list)
    echo "━━━ 伏笔追踪 ━━━"
    echo ""
    STATUS_FILTER="${2:-all}"
    jq -r --arg filter "$STATUS_FILTER" '
      .foreshadows[]
      | select(
          if $filter == "all" then true
          elif $filter == "open" then .status == "open"
          else .status == $filter end
        )
      | "  [\(.id)] \(.content)
    埋设: \(.planted_at // "?") ｜ 回收: \(.harvest_at // "?")
    状态: \(.status) ｜ 章节: \(.chapter)"' "$TRACKER_FILE" 2>/dev/null || echo "  (空)"
    ;;

  add)
    shift
    CONTENT="$*"
    [ -z "$CONTENT" ] && { echo "用法: $0 add <伏笔内容>"; exit 1; }
    ID=$(date +%s)
    jq --arg id "$ID" \
       --arg content "$CONTENT" \
       --arg chapter "${CHAPTER:-当前}" \
       '.foreshadows += [{
         "id": $id,
         "content": $content,
         "chapter": $chapter,
         "status": "open",
         "planted_at": (now | strftime("%Y-%m-%d %H:%M")),
         "harvest_at": null
       }]' "$TRACKER_FILE" > "${TRACKER_FILE}.tmp" && mv "${TRACKER_FILE}.tmp" "$TRACKER_FILE"
    echo "✓ 伏笔已记录 (ID: $ID)"
    ;;

  close)
    ID="${2:-}"
    [ -z "$ID" ] && { echo "用法: $0 close <id>"; exit 1; }
    jq --arg id "$ID" \
       '(.foreshadows[] | select(.id == $id) | .status) = "closed"
        | (.foreshadows[] | select(.id == $id) | .harvest_at) = (now | strftime("%Y-%m-%d %H:%M"))' \
       "$TRACKER_FILE" > "${TRACKER_FILE}.tmp" && mv "${TRACKER_FILE}.tmp" "$TRACKER_FILE"
    echo "✓ 伏笔 $ID 已标记为已回收"
    ;;

  report)
    echo "━━━ 伏笔统计报告 ━━━"
    TOTAL=$(jq '.foreshadows | length' "$TRACKER_FILE")
    OPEN=$(jq '[.foreshadows[] | select(.status == "open")] | length' "$TRACKER_FILE")
    CLOSED=$(jq '[.foreshadows[] | select(.status == "closed")] | length' "$TRACKER_FILE")
    echo "  总数: $TOTAL"
    echo "  待回收: $OPEN"
    echo "  已回收: $CLOSED"
    echo ""
    if [ "$OPEN" -gt 0 ]; then
      echo "⚠️  还有 $OPEN 个伏笔未回收，建议检查是否需要补充回收"
    fi
    ;;

  *)
    echo "用法: $0 <list|add|close|report>"
    exit 1
    ;;
esac
