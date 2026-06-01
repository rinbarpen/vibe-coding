#!/bin/bash
# vibe-init-ppt: Presentation creation project initialization script

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MANIFEST_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_ROOT=$(pwd)

echo "Initializing presentation creation project from: $MANIFEST_DIR"

# 1. Create project directory structure
mkdir -p source templates output assets scripts notes _backups .cursor/rules

# 2. Copy core configuration files
[ ! -f CLAUDE.md ] && cp "$MANIFEST_DIR/CLAUDE.md" CLAUDE.md && echo "Created CLAUDE.md"
[ ! -f AGENTS.md ] && cp "$MANIFEST_DIR/AGENTS.md" AGENTS.md && echo "Created AGENTS.md"
[ ! -f .cursorrules ] && cp "$MANIFEST_DIR/.cursorrules" .cursorrules && echo "Created .cursorrules"

# 3. Copy rule files
if [ -d "$MANIFEST_DIR/rules" ]; then
    for file in "$MANIFEST_DIR/rules"/*.mdc; do
        filename=$(basename "$file")
        cp "$file" ".cursor/rules/$filename"
        echo "Installed rule: $filename"
    done
fi

# 4. Create scaffold slide outline
if [ ! -f source/outline.yaml ]; then
    cat > source/outline.yaml << 'YMLEOF'
# Slide Outline
# Define slides with title, content, layout, and notes

presentation:
  title: "Sample Presentation"
  author: "Author Name"
  date: "$(date +%Y-%m-%d)"

slides:
  - title: "Title Slide"
    layout: title
    content: ""
    notes: "Welcome and introduction."

  - title: "Agenda"
    layout: content
    content:
      - "Topic 1"
      - "Topic 2"
      - "Topic 3"
    notes: "Overview of today's presentation structure."

  - title: "Summary"
    layout: content
    content:
      - "Key takeaway 1"
      - "Key takeaway 2"
    notes: "Recap and next steps. Open for questions."
YMLEOF
    echo "Created source/outline.yaml (scaffold)"
fi

# 5. Create .gitignore
cat > .gitignore << 'GITIGNORE'
_backups/
output/
__pycache__/
*.pyc
.DS_Store
*.tmp
*.temp
~$*.pptx
GITIGNORE
echo "Created .gitignore"

# 6. Initialize git repository if needed
if [ ! -d .git ]; then
    git init
    echo "Initialized git repository"
fi

# 7. Make initial commit
git add -A
if ! git diff --cached --quiet; then
    git commit -m "chore: initialize presentation creation project"
    echo "Created initial commit"
fi

echo "------------------------------------------------"
echo "Presentation creation project initialized!"
echo ""
echo "Project structure:"
echo "  source/        - Slide content definitions (YAML/JSON/MD)"
echo "  templates/     - ppt-master slide masters and themes"
echo "  output/        - Generated presentations"
echo "  assets/        - Images, icons, media files"
echo "  scripts/       - python-pptx automation scripts"
echo "  notes/         - Speaker notes and scripts"
echo "  _backups/      - Timestamped file backups"
echo ""
echo "Next steps:"
echo "  1. Edit source/outline.yaml"
echo "  2. Run: ppt-master init <name>"
echo "  3. Run: vibe-ppt-create <title> <slides>"
echo ""
echo "Safety workflow for pptx modifications:"
echo "  1. git checkout -b ppt/<task>"
echo "  2. cp original.pptx working.pptx"
echo "  3. Modify working copy via python-pptx or ppt-master"
echo "  4. Validate working copy"
echo "  5. Backup original + replace"
echo "  6. git commit"
echo "------------------------------------------------"
