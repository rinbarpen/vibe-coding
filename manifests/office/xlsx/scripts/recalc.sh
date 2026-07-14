#!/bin/bash
# Recalculate all formulas in xlsx using LibreOffice headless.
# Usage: bash scripts/recalc.sh <input.xlsx> [timeout_seconds]
set -euo pipefail

INPUT="${1:?Usage: recalc.sh <input.xlsx> [timeout]}"
TIMEOUT="${2:-30}"
DIR=$(dirname "$INPUT")
FILE=$(basename "$INPUT")
TMP="${DIR}/.recalc-$$"

mkdir -p "$TMP"
cp "$INPUT" "$TMP/"

# LibreOffice recalculates formulas on open+save
timeout "$TIMEOUT" libreoffice --headless --calc \
    --convert-to xlsx:"Calc MS Excel 2007 XML" \
    --outdir "$TMP" "$TMP/$FILE" 2>/dev/null

if [ -f "$TMP/$FILE" ]; then
    cp "$TMP/$FILE" "$INPUT"
    rm -rf "$TMP"
    echo "[OK] Formulas recalculated: $INPUT"
else
    rm -rf "$TMP"
    echo "[ERROR] Recalculation failed" >&2
    exit 1
fi
