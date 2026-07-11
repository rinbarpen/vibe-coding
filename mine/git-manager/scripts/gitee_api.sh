#!/usr/bin/env bash
#
# gitee_api.sh — Gitee OpenAPI v5 辅助脚本
#
# 封装 curl 调用，自动添加认证 header 和错误检查。
#
# Usage:
#   export GITEE_TOKEN="your_token"
#   ./gitee_api.sh GET /user
#   ./gitee_api.sh POST /user/repos '{"name":"my-repo","auto_init":true}'
#
set -euo pipefail

API_BASE="https://gitee.com/api/v5"

if [ -z "${GITEE_TOKEN:-}" ]; then
  echo "ERROR: GITEE_TOKEN 环境变量未设置" >&2
  echo "在 https://gitee.com/profile/personal_access_tokens 生成" >&2
  exit 1
fi

METHOD="${1:?Usage: gitee_api.sh <METHOD> <path> [body]}"
PATH_ARG="${2:?Usage: gitee_api.sh <METHOD> <path> [body]}"
BODY="${3:-}"

URL="${API_BASE}${PATH_ARG}"

do_curl() {
  if [ -n "$BODY" ]; then
    curl -s -X "$METHOD" "$URL" \
      -H "Authorization: token $GITEE_TOKEN" \
      -H "Content-Type: application/json" \
      -d "$BODY"
  else
    curl -s -X "$METHOD" "$URL" \
      -H "Authorization: token $GITEE_TOKEN"
  fi
}

RESPONSE=$(do_curl)

# 检查 API 错误
if echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if isinstance(data, dict) and 'error' in data:
        sys.exit(1) if data.get('error') else sys.exit(0)
    sys.exit(0)
except:
    sys.exit(0)
" 2>/dev/null; then
  echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
else
  echo "API ERROR:" >&2
  echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
  exit 1
fi
