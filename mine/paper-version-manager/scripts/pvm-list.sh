#!/usr/bin/env bash
set -euo pipefail

# pvm-list.sh — List all versions with timestamps and changelog
# Usage: pvm-list.sh <paper-dir>

PAPER_DIR="${1:-}"
if [ -z "$PAPER_DIR" ]; then
    echo "Usage: pvm-list.sh <paper-dir>"
    exit 1
fi

VERSIONS_DIR="$PAPER_DIR/.versions"
if [ ! -f "$VERSIONS_DIR/CHANGELOG.md" ]; then
    echo "Error: version tracking not initialized in $PAPER_DIR"
    exit 1
fi

CURRENT_VERSION=$(cat "$VERSIONS_DIR/VERSION" 2>/dev/null || echo "unknown")

echo "Paper Version History"
echo "====================="
echo "Current version: $CURRENT_VERSION"
echo ""

# List all snapshot directories sorted by version
echo "Snapshots:"
for ver_dir in "$VERSIONS_DIR"/v*; do
    [ -d "$ver_dir" ] || continue
    ver=$(basename "$ver_dir")
    # Skip if it looks like a version directory (starts with v followed by digit)
    if [[ "$ver" =~ ^v[0-9] ]]; then
        indicator=""
        [ "$ver" = "$CURRENT_VERSION" ] && indicator="  ← active"
        echo "  $ver$indicator"
    fi
done

echo ""
echo "Changelog:"
if [ -f "$VERSIONS_DIR/CHANGELOG.md" ]; then
    cat "$VERSIONS_DIR/CHANGELOG.md"
fi
