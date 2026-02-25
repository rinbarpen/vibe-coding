#!/bin/bash

# Vibe Manifest Generator Helper Script
# Usage: ./vibe-gen.sh [target_directory]

TARGET_DIR=${1:-"."}
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "🚀 Initializing Vibe Manifest in $TARGET_DIR..."

# Create directories if they don't exist
mkdir -p "$TARGET_DIR/.cursor/rules"

# Copy templates if they don't exist in target
if [ ! -f "$TARGET_DIR/CLAUDE.md" ]; then
    cp "$SKILL_DIR/templates/CLAUDE.md.example" "$TARGET_DIR/CLAUDE.md"
    echo "✅ Created CLAUDE.md"
else
    echo "⚠️ CLAUDE.md already exists, skipping."
fi

if [ ! -f "$TARGET_DIR/AGENTS.md" ]; then
    cp "$SKILL_DIR/templates/AGENTS.md.example" "$TARGET_DIR/AGENTS.md"
    echo "✅ Created AGENTS.md"
else
    echo "⚠️ AGENTS.md already exists, skipping."
fi

if [ ! -f "$TARGET_DIR/.cursorrules" ]; then
    cp "$SKILL_DIR/templates/.cursorrules.example" "$TARGET_DIR/.cursorrules"
    echo "✅ Created .cursorrules"
else
    echo "⚠️ .cursorrules already exists, skipping."
fi

echo "🎉 Vibe Manifest initialization complete!"
echo "Please review and customize the generated files for your project."
