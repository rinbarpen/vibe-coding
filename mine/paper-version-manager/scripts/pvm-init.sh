#!/usr/bin/env bash
set -euo pipefail

# pvm-init.sh — Initialize version tracking for a paper directory
# Usage: pvm-init.sh <paper-dir> [changelog message]

PAPER_DIR="${1:-}"
shift || true
CHANGELOG_MSG="${*:-Initial snapshot}"

if [ -z "$PAPER_DIR" ]; then
    echo "Usage: pvm-init.sh <paper-dir> [changelog message]"
    exit 1
fi

if [ ! -d "$PAPER_DIR" ]; then
    echo "Error: directory $PAPER_DIR does not exist"
    exit 1
fi

VERSIONS_DIR="$PAPER_DIR/.versions"
if [ -d "$VERSIONS_DIR" ]; then
    echo "Error: version tracking already initialized at $VERSIONS_DIR"
    exit 1
fi

mkdir -p "$VERSIONS_DIR"
echo "v1" > "$VERSIONS_DIR/VERSION"

# Record start time
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Copy all non-.versions files as v1 snapshot
SNAPSHOT_DIR="$VERSIONS_DIR/v1"
mkdir -p "$SNAPSHOT_DIR"

# Use rsync if available, fallback to cp -r
if command -v rsync &>/dev/null; then
    rsync -a --exclude='.versions' "$PAPER_DIR/" "$SNAPSHOT_DIR/"
else
    # Exclude .versions by copying individual items
    for item in "$PAPER_DIR"/* "$PAPER_DIR"/.*; do
        basename_item=$(basename "$item")
        if [ "$basename_item" = "." ] || [ "$basename_item" = ".." ] || [ "$basename_item" = ".versions" ]; then
            continue
        fi
        cp -a "$item" "$SNAPSHOT_DIR/"
    done
fi

# Initialize CHANGELOG
cat > "$VERSIONS_DIR/CHANGELOG.md" << EOF
# Paper Version Changelog

| Version | Date | Description |
|---------|------|-------------|
| v1 | $TIMESTAMP | $CHANGELOG_MSG |
EOF

echo "Initialized version tracking at $VERSIONS_DIR"
echo "Current version: v1"
