#!/bin/bash
# install-deps.sh — Install dependencies for DOCX/PreTeXt manifest
# Idempotent: safe to run multiple times.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

echo "==> Installing DOCX manifest dependencies..."

# --- Anthropics skills submodule ---
echo ""
echo "--- Anthropics skills submodule ---"
cd "$REPO_ROOT"
if [ -f skills/anthropics/skills/docx/SKILL.md ]; then
    echo "[OK] skills/anthropics already initialized"
else
    echo "Initializing skills/anthropics submodule..."
    git submodule update --init skills/anthropics
    if [ -f skills/anthropics/skills/docx/SKILL.md ]; then
        echo "[OK] skills/anthropics initialized"
    else
        echo "[WARN] skills/anthropics initialized but docx skill not found — check submodule remote"
    fi
fi

# --- python-docx ---
echo ""
echo "--- python-docx ---"
if python3 -c "import docx" 2>/dev/null; then
    echo "[OK] python-docx $(python3 -c 'import docx; print(docx.__version__)')"
else
    echo "Installing python-docx..."
    pip3 install python-docx
    echo "[OK] python-docx installed"
fi

# --- PreTeXt CLI ---
echo ""
echo "--- PreTeXt ---"
if command -v pretext &>/dev/null; then
    echo "[OK] pretext $(pretext --version 2>&1 | head -1)"
else
    echo "Installing pretext..."
    pip3 install pretext
    if command -v pretext &>/dev/null; then
        echo "[OK] pretext installed"
    else
        echo "[WARN] pretext pip install succeeded but CLI not on PATH — check your Python bin directory"
    fi
fi

echo ""
echo "==> DOCX manifest dependencies ready."
