#!/bin/bash
# vibe-init: 模块化初始化脚本，支持独立场景选择

set -e

# 获取 manifest 源路径
MANIFEST_DIR="${VIBE_MANIFEST:-$(cd "$(dirname "$0")/../.." && pwd)}"
PROJECT_ROOT=$(pwd)
RELATIVE_MANIFEST_DIR=$(realpath --relative-to="$PROJECT_ROOT" "$MANIFEST_DIR")

echo "Initializing Vibe Coding project from: $RELATIVE_MANIFEST_DIR"

# 1. 解析场景参数
SCENARIOS=""
for arg in "$@"; do
    if [[ $arg == --scenario=* ]]; then
        SCENARIOS="${arg#*=}"
    fi
done

# 2. 创建基础目录
mkdir -p .cursor/rules .cursor/plans docs tests templates

# 3. 复制核心规则 (Core)
echo "Installing Core rules..."
if [ -d "$MANIFEST_DIR/core/rules" ]; then
    for file in "$MANIFEST_DIR/core/rules"/*.mdc; do
        filename=$(basename "$file")
        sed "s|{{VIBE_MANIFEST}}|$RELATIVE_MANIFEST_DIR|g" "$file" > ".cursor/rules/$filename"
    done
fi

# 4. 复制场景规则 (Scenarios)
IFS=',' read -ra ADDR <<< "$SCENARIOS"
for scenario in "${ADDR[@]}"; do
    scenario_dir="$MANIFEST_DIR/scenarios/$scenario"
    if [ -d "$scenario_dir" ]; then
        echo "Installing Scenario: $scenario..."
        # 复制规则
        if [ -d "$scenario_dir/rules" ]; then
            for file in "$scenario_dir/rules"/*.mdc; do
                filename=$(basename "$file")
                sed "s|{{VIBE_MANIFEST}}|$RELATIVE_MANIFEST_DIR|g" "$file" > ".cursor/rules/$filename"
            done
        fi
        # 复制场景专属模板 (如果存在且根目录没有对应文件)
        if [ -f "$scenario_dir/CLAUDE.md" ] && [ ! -f CLAUDE.md ]; then
            cp "$scenario_dir/CLAUDE.md" CLAUDE.md
        fi
    fi
done

# 5. 默认初始化 (如果场景没有提供)
if [ ! -f CLAUDE.md ] && [ -f "$MANIFEST_DIR/CLAUDE.md" ]; then
    cp "$MANIFEST_DIR/CLAUDE.md" CLAUDE.md
fi

if [ ! -f AGENTS.md ] && [ -f "$MANIFEST_DIR/AGENTS.md" ]; then
    sed "s|{{VIBE_MANIFEST}}|$RELATIVE_MANIFEST_DIR|g" "$MANIFEST_DIR/AGENTS.md" > AGENTS.md
fi

# 6. 基础项目文件
[ ! -f README.md ] && cp "$MANIFEST_DIR/core/README.md" README.md || true
[ ! -f CONTRIBUTING.md ] && cp "$MANIFEST_DIR/core/CONTRIBUTING.md" CONTRIBUTING.md || true

echo "Project initialized successfully with scenarios: ${SCENARIOS:-default}"
