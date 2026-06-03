#!/bin/bash
# init-anything-cli.sh — 初始化 Anything CLI (CLI-Anything) 项目
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MANIFEST_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_DIR="${1:-$(pwd)}"

echo "================================================"
echo " Anything CLI (CLI-Anything) — 项目初始化"
echo "================================================"
echo ""
echo "目标目录: $TARGET_DIR"
echo ""

# 1. 创建项目目录结构
mkdir -p "$TARGET_DIR"/{harnesses,registry,configs,tests}

# 2. 复制核心配置文件（不覆盖已有）
for f in CLAUDE.md AGENTS.md .cursorrules README.md; do
    if [ ! -f "$TARGET_DIR/$f" ]; then
        cp "$MANIFEST_DIR/$f" "$TARGET_DIR/$f"
        echo "  [OK] $f"
    fi
done

echo ""
echo "================================================"
echo " Anything CLI 项目初始化完成！"
echo "================================================"
echo ""
echo "后续步骤："
echo "  1. 安装 CLI-Hub 包管理器："
echo "     pip install cli-anything-hub"
echo ""
echo "  2. 使用 cli-hub search/install 安装社区 CLI"
echo "     或在 AI Agent 中使用 /cli-anything 生成新 CLI"
echo ""
echo "  3. 安装 Python 依赖："
echo "     pip install click pytest"
echo ""
