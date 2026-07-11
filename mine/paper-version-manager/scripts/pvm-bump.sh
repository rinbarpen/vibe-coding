#!/usr/bin/env bash
set -euo pipefail

# pvm-bump.sh — Bump paper version (major or minor)
# Usage: pvm-bump.sh --minor <paper-dir> "changelog message"
#        pvm-bump.sh --major <paper-dir> "changelog message"

BUMP_TYPE=""
PAPER_DIR=""
CHANGELOG_MSG=""

while [ $# -gt 0 ]; do
    case "$1" in
        --minor|--major)
            BUMP_TYPE="${1#--}"
            shift
            ;;
        *)
            if [ -z "$PAPER_DIR" ]; then
                PAPER_DIR="$1"
            else
                CHANGELOG_MSG="$*"
                break
            fi
            shift
            ;;
    esac
done

if [ -z "$BUMP_TYPE" ] || [ -z "$PAPER_DIR" ]; then
    echo "Usage: pvm-bump.sh --minor|--major <paper-dir> [changelog message]"
    exit 1
fi

if [ -z "$CHANGELOG_MSG" ]; then
    CHANGELOG_MSG="No description provided"
fi

VERSIONS_DIR="$PAPER_DIR/.versions"
if [ ! -f "$VERSIONS_DIR/VERSION" ]; then
    echo "Error: version tracking not initialized. Run pvm-init.sh first."
    exit 1
fi

CURRENT_VERSION=$(cat "$VERSIONS_DIR/VERSION")
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Parse current version
if [[ "$CURRENT_VERSION" =~ ^v([0-9]+)$ ]]; then
    MAJOR="${BASH_REMATCH[1]}"
    MINOR=""
elif [[ "$CURRENT_VERSION" =~ ^v([0-9]+)\.([0-9]+)$ ]]; then
    MAJOR="${BASH_REMATCH[1]}"
    MINOR="${BASH_REMATCH[2]}"
else
    echo "Error: unrecognized version format: $CURRENT_VERSION"
    exit 1
fi

# Compute next version
if [ "$BUMP_TYPE" = "major" ]; then
    NEW_MAJOR=$((MAJOR + 1))
    NEW_VERSION="v$NEW_MAJOR"
elif [ "$BUMP_TYPE" = "minor" ]; then
    if [ -z "$MINOR" ]; then
        # v1 → v1.1
        NEW_VERSION="${CURRENT_VERSION}.1"
    else
        NEW_MINOR=$((MINOR + 1))
        NEW_VERSION="v${MAJOR}.${NEW_MINOR}"
    fi
fi

# Check if snapshot already exists
SNAPSHOT_DIR="$VERSIONS_DIR/$NEW_VERSION"
if [ -d "$SNAPSHOT_DIR" ]; then
    echo "Warning: snapshot $NEW_VERSION already exists. Overwriting."
    rm -rf "$SNAPSHOT_DIR"
fi

mkdir -p "$SNAPSHOT_DIR"

# Snapshot current paper files (exclude .versions)
if command -v rsync &>/dev/null; then
    rsync -a --exclude='.versions' "$PAPER_DIR/" "$SNAPSHOT_DIR/"
else
    for item in "$PAPER_DIR"/* "$PAPER_DIR"/.*; do
        basename_item=$(basename "$item")
        if [ "$basename_item" = "." ] || [ "$basename_item" = ".." ] || [ "$basename_item" = ".versions" ]; then
            continue
        fi
        cp -a "$item" "$SNAPSHOT_DIR/"
    done
fi

# Update VERSION file
echo "$NEW_VERSION" > "$VERSIONS_DIR/VERSION"

# Append to CHANGELOG
cat >> "$VERSIONS_DIR/CHANGELOG.md" << EOF
| $NEW_VERSION | $TIMESTAMP | $CHANGELOG_MSG |
EOF

echo "Bumped version: $CURRENT_VERSION → $NEW_VERSION"
