#!/bin/bash
# install-deps.sh — Install dependencies for PPT/PowerPoint manifest
# Idempotent: safe to run multiple times.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

echo "==> Installing PPT manifest dependencies..."

# --- Anthropics skills submodule ---
echo ""
echo "--- Anthropics skills submodule ---"
cd "$REPO_ROOT"
if [ -f skills/anthropics/skills/pptx/SKILL.md ]; then
    echo "[OK] skills/anthropics already initialized"
else
    echo "Initializing skills/anthropics submodule..."
    git submodule update --init skills/anthropics
    if [ -f skills/anthropics/skills/pptx/SKILL.md ]; then
        echo "[OK] skills/anthropics initialized"
    else
        echo "[WARN] skills/anthropics initialized but pptx skill not found — check submodule remote"
    fi
fi

# --- python-pptx ---
echo ""
echo "--- python-pptx ---"
if python3 -c "import pptx" 2>/dev/null; then
    echo "[OK] python-pptx $(python3 -c 'import pptx; print(pptx.__version__)')"
else
    echo "Installing python-pptx..."
    pip3 install python-pptx
    echo "[OK] python-pptx installed"
fi

# --- ppt-master CLI (optional, may not be available on npm) ---
echo ""
echo "--- ppt-master (slide master/template management) ---"
if command -v ppt-master &>/dev/null; then
    echo "[OK] ppt-master $(ppt-master --version 2>&1 | head -1)"
else
    echo "[NOTE] ppt-master is not on npm. Slide master management is handled by:"
    echo "       - skills/anthropics/skills/pptx (template application)"
    echo "       - python-pptx (programmatic slide manipulation)"
    echo "      No additional install needed."
fi

echo ""
echo "==> PPT manifest dependencies ready."
