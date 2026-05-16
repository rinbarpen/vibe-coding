#!/bin/bash
set -e

# ============================================================
# vibe-init-code.sh — Initialize a Code Programming project
# ============================================================
# Run from the target project root (the directory you want to
# turn into a code-programming managed project).
#
# Usage:
#   bash manifests/code-programming/scripts/vibe-init-code.sh
# ============================================================

MANIFEST_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT_ROOT="$(pwd)"

echo "=== Code Programming Manifest Initialization ==="
echo "Project root: $PROJECT_ROOT"
echo "Manifest source: $MANIFEST_DIR"
echo ""

# 1. Create directory structure
echo "[1/6] Creating project directory structure..."
mkdir -p src tests docs scripts infra .cursor/plans .cursor/rules .cursor/commands .cursor/references/language-specs .cursor/references/decision-trees

# 2. Copy core files (don't overwrite existing)
echo "[2/6] Installing core files..."
[ ! -f CLAUDE.md ] && cp "$MANIFEST_DIR/CLAUDE.md" CLAUDE.md && echo "  → CLAUDE.md"
[ ! -f AGENTS.md ] && cp "$MANIFEST_DIR/AGENTS.md" AGENTS.md && echo "  → AGENTS.md"
[ ! -f .cursorrules ] && cp "$MANIFEST_DIR/.cursorrules" .cursorrules && echo "  → .cursorrules"

# 3. Install rules
echo "[3/6] Installing rules..."
for file in "$MANIFEST_DIR/rules"/*.mdc; do
    filename=$(basename "$file")
    dest=".cursor/rules/$filename"
    if [ ! -f "$dest" ]; then
        cp "$file" "$dest"
        echo "  → rules/$filename"
    fi
done

# 4. Install commands
echo "[4/6] Installing commands..."
for cmd_dir in "$MANIFEST_DIR/commands"/*/; do
    [ -d "$cmd_dir" ] || continue
    cmd_name=$(basename "$cmd_dir")
    mkdir -p ".cursor/commands/$cmd_name"
    cp "$cmd_dir"COMMAND.md ".cursor/commands/$cmd_name/" 2>/dev/null && echo "  → commands/$cmd_name" || true
done

# 5. Install references
echo "[5/6] Installing references..."
cp "$MANIFEST_DIR/references/language-specs/"*.md ".cursor/references/language-specs/" 2>/dev/null || true
cp "$MANIFEST_DIR/references/decision-trees/"*.md ".cursor/references/decision-trees/" 2>/dev/null || true
[ -f "$MANIFEST_DIR/references/lifecycle-guide.md" ] && cp "$MANIFEST_DIR/references/lifecycle-guide.md" ".cursor/references/" && echo "  → lifecycle-guide.md"

# 6. Git init (if not already)
echo "[6/6] Checking git repository..."
if [ ! -d ".git" ]; then
    git init
    echo "  → Git repository initialized"
else
    echo "  → Git repository already exists"
fi

echo ""
echo "=== Initialization Complete ==="
echo ""
echo "Next steps:"
echo "  1. Review CLAUDE.md and customize for your project"
echo "  2. Run /lang-select to choose languages"
echo "  3. Run /plan to create your first implementation plan"
echo ""
