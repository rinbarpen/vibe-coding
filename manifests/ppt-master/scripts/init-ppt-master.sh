#!/bin/bash
# init-ppt-master.sh — 初始化 PPT Master 演示文稿项目
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MANIFEST_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_DIR="$MANIFEST_DIR/../../skills/ppt-master/skills/ppt-master"
TARGET_DIR="${1:-$(pwd)}"
PROJECT_NAME=""
FORMAT="ppt169"

# 参数解析
shift 2>/dev/null || true
while [[ $# -gt 0 ]]; do
    case "$1" in
        --name)
            PROJECT_NAME="$2"
            shift 2
            ;;
        --format)
            FORMAT="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [target-dir] [--name <project_name>] [--format ppt169]"
            echo ""
            echo "Initialize a PPT Master presentation project."
            echo ""
            echo "Options:"
            echo "  --name <name>     Project name (runs project_manager.py init)"
            echo "  --format <fmt>    Canvas format (default: ppt169)"
            echo "  --help, -h        Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage."
            exit 1
            ;;
    esac
done

echo "================================================"
echo " PPT Master — 演示文稿项目初始化"
echo "================================================"
echo ""
echo "目标目录: $TARGET_DIR"
echo "Manifest:  $MANIFEST_DIR"
echo ""

# 1. 创建项目目录结构
mkdir -p "$TARGET_DIR"/{sources,svg_output,svg_final,exports,images,notes,templates}
mkdir -p "$TARGET_DIR"/.cursor/{rules,references}

# 2. 复制核心配置文件（不覆盖已有）
if [ ! -f "$TARGET_DIR/CLAUDE.md" ]; then
    cp "$MANIFEST_DIR/CLAUDE.md" "$TARGET_DIR/CLAUDE.md"
    echo "  [OK] CLAUDE.md"
else
    echo "  [SKIP] CLAUDE.md (已存在)"
fi

if [ ! -f "$TARGET_DIR/AGENTS.md" ]; then
    cp "$MANIFEST_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"
    echo "  [OK] AGENTS.md"
else
    echo "  [SKIP] AGENTS.md (已存在)"
fi

if [ ! -f "$TARGET_DIR/.cursorrules" ]; then
    cp "$MANIFEST_DIR/.cursorrules" "$TARGET_DIR/.cursorrules"
    echo "  [OK] .cursorrules"
else
    echo "  [SKIP] .cursorrules (已存在)"
fi

# 3. 安装规则文件
if [ -d "$MANIFEST_DIR/rules" ]; then
    for file in "$MANIFEST_DIR/rules"/*.mdc; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            cp "$file" "$TARGET_DIR/.cursor/rules/$filename"
            echo "  [OK] rule: $filename"
        fi
    done
fi

# 4. 复制参考存根
if [ -d "$MANIFEST_DIR/references" ]; then
    for file in "$MANIFEST_DIR/references"/*.md; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            cp "$file" "$TARGET_DIR/.cursor/references/$filename"
            echo "  [OK] reference: $filename"
        fi
    done
fi

# 5. 复制模板示例
if [ -d "$MANIFEST_DIR/templates" ]; then
    for file in "$MANIFEST_DIR/templates"/*.md.example; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            cp "$file" "$TARGET_DIR/templates/$filename"
            echo "  [OK] template: $filename"
        fi
    done
fi

# 6. 创建空的初始文件
if [ ! -f "$TARGET_DIR/design_spec.md" ]; then
    touch "$TARGET_DIR/design_spec.md"
    echo "  [OK] design_spec.md (空文件)"
fi

if [ ! -f "$TARGET_DIR/spec_lock.md" ]; then
    touch "$TARGET_DIR/spec_lock.md"
    echo "  [OK] spec_lock.md (空文件)"
fi

# 7. 如果提供了项目名称，运行 project_manager.py init
if [ -n "$PROJECT_NAME" ]; then
    echo ""
    echo "运行 project_manager.py init..."
    if python3 "$SKILL_DIR/scripts/project_manager.py" init "$PROJECT_NAME" --format "$FORMAT" --dir "$TARGET_DIR"; then
        echo "  [OK] project_manager.py 初始化完成"
    else
        echo "  [WARN] project_manager.py 执行失败，请手动运行"
    fi
fi

echo ""
echo "================================================"
echo " PPT Master 项目初始化完成！"
echo "================================================"
echo ""
echo "后续步骤："
echo "  1. 安装依赖："
echo "     pip install -r skills/ppt-master/requirements.txt"
echo ""
echo "  2.（可选）配置图片生成："
echo "     cp skills/ppt-master/.env.example .env"
echo "     # 编辑 .env 设置 IMAGE_BACKEND 与 API Key"
echo ""
echo "  3. 将源文件放入 sources/ 目录"
echo ""
echo "  4. 在对话框输入 /init <项目名称> 开始制作演示文稿"
echo ""
