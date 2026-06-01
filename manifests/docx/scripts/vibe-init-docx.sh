#!/bin/bash
# vibe-init-docx: Document creation project initialization script

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MANIFEST_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_ROOT=$(pwd)

echo "Initializing document creation project from: $MANIFEST_DIR"

# 1. Create project directory structure
mkdir -p source/chapters source/frontmatter source/backmatter
mkdir -p assets output styles templates scripts _backups
mkdir -p .cursor/rules

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

# 4. Create scaffold PreTeXt source
if [ ! -f source/main.ptx ]; then
    cat > source/main.ptx << 'PTXEOF'
<?xml version="1.0" encoding="UTF-8"?>
<pretext xml:lang="en">
  <frontmatter>
    <title>A PreTeXt Document</title>
    <author>
      <personname>Author Name</personname>
    </author>
  </frontmatter>
  <chapter xml:id="ch:introduction">
    <title>Introduction</title>
    <p>Start writing here.</p>
  </chapter>
</pretext>
PTXEOF
    echo "Created source/main.ptx (scaffold)"
fi

[ ! -f publication.ptx ] && touch publication.ptx && echo "Created publication.ptx (empty — configure for your project)"

# 5. Create .gitignore
cat > .gitignore << 'GITIGNORE'
_backups/
output/
__pycache__/
*.pyc
.DS_Store
*.tmp
*.temp
~$*.docx
*.aux
*.log
*.out
*.toc
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
    git commit -m "chore: initialize document creation project"
    echo "Created initial commit"
fi

echo "------------------------------------------------"
echo "Document creation project initialized!"
echo ""
echo "Project structure:"
echo "  source/        - PreTeXt XML source files"
echo "  source/chapters/ - Modular chapter files"
echo "  assets/        - Images and resources"
echo "  output/        - Generated outputs (HTML, PDF, DOCX)"
echo "  styles/        - CSS/XSL/Publisher config"
echo "  templates/     - docx reference templates"
echo "  _backups/      - Timestamped file backups"
echo ""
echo "Next steps:"
echo "  1. Edit source/main.ptx"
echo "  2. Run: pretext build"
echo "  3. Run: pretext view"
echo ""
echo "Safety workflow for docx modifications:"
echo "  1. git checkout -b docx/<task>"
echo "  2. cp original.docx working.docx"
echo "  3. Modify working copy via python-docx"
echo "  4. Validate working copy"
echo "  5. Backup original + replace"
echo "  6. git commit"
echo "------------------------------------------------"
