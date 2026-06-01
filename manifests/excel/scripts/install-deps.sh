#!/bin/bash
# install-deps.sh — Install dependencies for Excel spreadsheet manifest
# Idempotent: safe to run multiple times.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

echo "==> Installing Excel manifest dependencies..."

# --- Anthropics skills submodule ---
echo ""
echo "--- Anthropics skills submodule ---"
cd "$REPO_ROOT"
if [ -f skills/anthropics/skills/xlsx/SKILL.md ]; then
    echo "[OK] skills/anthropics already initialized"
else
    echo "Initializing skills/anthropics submodule..."
    git submodule update --init skills/anthropics
    if [ -f skills/anthropics/skills/xlsx/SKILL.md ]; then
        echo "[OK] skills/anthropics initialized"
    else
        echo "[WARN] skills/anthropics initialized but xlsx skill not found — check submodule remote"
    fi
fi

# --- openpyxl ---
echo ""
echo "--- openpyxl ---"
if python3 -c "import openpyxl" 2>/dev/null; then
    echo "[OK] openpyxl $(python3 -c 'import openpyxl; print(openpyxl.__version__)')"
else
    echo "Installing openpyxl..."
    pip3 install openpyxl
    echo "[OK] openpyxl installed"
fi

echo ""
echo "==> Excel manifest dependencies ready."
