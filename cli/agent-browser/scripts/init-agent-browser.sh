#!/bin/bash
# init-agent-browser.sh — 初始化 Agent Browser 项目
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MANIFEST_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_DIR="${1:-$(pwd)}"

echo "================================================"
echo " Agent Browser — 项目初始化"
echo "================================================"
echo ""
echo "目标目录: $TARGET_DIR"
echo ""

# 1. 创建项目目录结构
mkdir -p "$TARGET_DIR"/{scripts,sessions,fixtures,screenshots,traces,reports}

# 2. 复制核心配置文件（不覆盖已有）
for f in CLAUDE.md AGENTS.md .cursorrules README.md; do
    if [ ! -f "$TARGET_DIR/$f" ]; then
        cp "$MANIFEST_DIR/$f" "$TARGET_DIR/$f"
        echo "  [OK] $f"
    fi
done

echo ""
echo "================================================"
echo " Agent Browser 项目初始化完成！"
echo "================================================"
echo ""
echo "后续步骤："
echo "  1. 确保 Node.js 18+ 已安装"
echo "  2. 运行 npx agent-browser --help 验证 CLI 可用"
echo ""
echo "  3. 编写自动化脚本放入 scripts/ 目录"
echo ""
