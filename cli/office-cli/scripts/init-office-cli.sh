#!/bin/bash
# init-office-cli.sh — 初始化 Office CLI 项目
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MANIFEST_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_DIR="${1:-$(pwd)}"

echo "================================================"
echo " Office CLI — 项目初始化"
echo "================================================"
echo ""
echo "目标目录: $TARGET_DIR"
echo ""

# 1. 创建项目目录结构
mkdir -p "$TARGET_DIR"/{inputs,outputs,templates,scripts,configs,_backups}

# 2. 复制核心配置文件（不覆盖已有）
for f in CLAUDE.md AGENTS.md .cursorrules README.md; do
    if [ ! -f "$TARGET_DIR/$f" ]; then
        cp "$MANIFEST_DIR/$f" "$TARGET_DIR/$f"
        echo "  [OK] $f"
    fi
done

echo ""
echo "================================================"
echo " Office CLI 项目初始化完成！"
echo "================================================"
echo ""
echo "后续步骤："
echo "  1. 确保 Python 3.x 及依赖已安装："
echo "     pip install python-docx openpyxl python-pptx"
echo ""
echo "  2. 将源文件放入 inputs/ 目录"
echo "  3. 使用 office-cli 命令开始处理"
echo ""
