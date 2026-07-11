#!/usr/bin/env bash
set -euo pipefail

# pvm-diff.sh — Diff between two paper versions
# Usage: pvm-diff.sh <paper-dir> --from v1 --to v1.1

PAPER_DIR=""
FROM_VER=""
TO_VER=""

while [ $# -gt 0 ]; do
    case "$1" in
        --from)
            FROM_VER="$2"
            shift 2
            ;;
        --to)
            TO_VER="$2"
            shift 2
            ;;
        *)
            if [ -z "$PAPER_DIR" ]; then
                PAPER_DIR="$1"
            else
                echo "Unknown argument: $1"
                exit 1
            fi
            shift
            ;;
    esac
done

if [ -z "$PAPER_DIR" ] || [ -z "$FROM_VER" ] || [ -z "$TO_VER" ]; then
    echo "Usage: pvm-diff.sh <paper-dir> --from <version> --to <version>"
    echo "Example: pvm-diff.sh /path/to/paper --from v1 --to v1.1"
    exit 1
fi

VERSIONS_DIR="$PAPER_DIR/.versions"
FROM_DIR="$VERSIONS_DIR/$FROM_VER"
TO_DIR="$VERSIONS_DIR/$TO_VER"

if [ ! -d "$FROM_DIR" ]; then
    echo "Error: version $FROM_VER not found"
    exit 1
fi
if [ ! -d "$TO_DIR" ]; then
    echo "Error: version $TO_VER not found"
    exit 1
fi

echo "Diff: $FROM_VER → $TO_VER"
echo "=================="
echo ""

# Use diff if available, show which files changed
if command -v diff &>/dev/null; then
    diff_output=$(diff -rq "$FROM_DIR" "$TO_DIR" 2>/dev/null || true)
    if [ -z "$diff_output" ]; then
        echo "No differences found between $FROM_VER and $TO_VER."
    else
        echo "$diff_output"
        echo ""
        echo "--- Detailed diffs for .tex and .md files ---"
        # Find common files that differ and show their diff
        while IFS= read -r line; do
            if [[ "$line" =~ ^Files\ (.+)\ and\ (.+)\ differ$ ]]; then
                file_a="${BASH_REMATCH[1]}"
                file_b="${BASH_REMATCH[2]}"
                rel_path="${file_a#$FROM_DIR/}"
                case "$rel_path" in
                    *.tex|*.md|*.txt|*.bib)
                        echo ""
                        echo "=== $rel_path ==="
                        diff -u "$file_a" "$file_b" 2>/dev/null || true
                        ;;
                esac
            fi
        done <<< "$diff_output"
    fi
else
    echo "diff tool not available. Compare manually:"
    echo "  $FROM_DIR/  →  $TO_DIR/"
fi
