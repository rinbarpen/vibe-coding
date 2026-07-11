#!/usr/bin/env bash
set -euo pipefail

# pvm-rollback.sh — Rollback paper files to a specific version
# Usage: pvm-rollback.sh <paper-dir> <version>

PAPER_DIR="${1:-}"
TARGET_VERSION="${2:-}"

if [ -z "$PAPER_DIR" ] || [ -z "$TARGET_VERSION" ]; then
    echo "Usage: pvm-rollback.sh <paper-dir> <version>"
    echo "Example: pvm-rollback.sh /path/to/paper v1"
    exit 1
fi

VERSIONS_DIR="$PAPER_DIR/.versions"
SNAPSHOT_DIR="$VERSIONS_DIR/$TARGET_VERSION"

if [ ! -d "$SNAPSHOT_DIR" ]; then
    echo "Error: version $TARGET_VERSION not found in $VERSIONS_DIR"
    echo "Available versions:"
    for d in "$VERSIONS_DIR"/v*; do
        [ -d "$d" ] && echo "  $(basename "$d")"
    done
    exit 1
fi

CURRENT_VERSION=$(cat "$VERSIONS_DIR/VERSION" 2>/dev/null || echo "none")
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "Rolling back: $CURRENT_VERSION → $TARGET_VERSION"
echo ""

# Remove current working files (everything except .versions)
for item in "$PAPER_DIR"/* "$PAPER_DIR"/.*; do
    basename_item=$(basename "$item")
    if [ "$basename_item" = "." ] || [ "$basename_item" = ".." ] || [ "$basename_item" = ".versions" ]; then
        continue
    fi
    rm -rf "$item"
done

# Copy snapshot files back to paper directory
for item in "$SNAPSHOT_DIR"/* "$SNAPSHOT_DIR"/.*; do
    basename_item=$(basename "$item")
    if [ "$basename_item" = "." ] || [ "$basename_item" = ".." ]; then
        continue
    fi
    cp -a "$item" "$PAPER_DIR/"
done

# Update VERSION
echo "$TARGET_VERSION" > "$VERSIONS_DIR/VERSION"

# Append rollback to CHANGELOG
cat >> "$VERSIONS_DIR/CHANGELOG.md" << EOF
| $TARGET_VERSION (rollback) | $TIMESTAMP | Rollback from $CURRENT_VERSION to $TARGET_VERSION |
EOF

echo "Rollback complete: $CURRENT_VERSION → $TARGET_VERSION"
echo "Paper files restored to $TARGET_VERSION state."
