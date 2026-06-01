#!/bin/bash
# vibe-init-excel: Spreadsheet analysis project initialization script

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MANIFEST_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_ROOT=$(pwd)

echo "Initializing Excel spreadsheet analysis project from: $MANIFEST_DIR"

# 1. Create project directory structure
mkdir -p data workbooks scripts templates reports schemas _backups .cursor/rules

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

# 4. Create .gitignore
cat > .gitignore << 'GITIGNORE'
_backups/
__pycache__/
*.pyc
.DS_Store
*.tmp
*.temp
~$*.xlsx
GITIGNORE
echo "Created .gitignore"

# 5. Initialize git repository if needed
if [ ! -d .git ]; then
    git init
    echo "Initialized git repository"
fi

# 6. Make initial commit
git add -A
if ! git diff --cached --quiet; then
    git commit -m "chore: initialize excel spreadsheet analysis project"
    echo "Created initial commit"
fi

echo "------------------------------------------------"
echo "Excel spreadsheet analysis project initialized!"
echo ""
echo "Project structure:"
echo "  data/       - Raw and processed data files"
echo "  workbooks/  - Generated workbook files"
echo "  scripts/    - openpyxl automation scripts"
echo "  templates/  - Workbook templates"
echo "  reports/    - Analysis reports and exports"
echo "  schemas/    - Data validation schemas"
echo "  _backups/   - Timestamped original file backups"
echo ""
echo "Safety workflow:"
echo "  1. git checkout -b excel/<task>"
echo "  2. cp original.xlsx working.xlsx"
echo "  3. Modify working copy via Python (openpyxl)"
echo "  4. Validate working copy"
echo "  5. Backup original + replace"
echo "  6. git commit"
echo "------------------------------------------------"
