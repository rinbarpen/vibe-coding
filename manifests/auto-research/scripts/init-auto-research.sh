#!/usr/bin/env bash
set -euo pipefail

MANIFEST_DIR="$(cd "$(dirname "$0")/.." && pwd)"

print_usage() {
  cat <<EOF
Usage: $(basename "$0") <target-dir> [options]

Initialize a research project with Auto-Research configuration.

Options:
  -o, --owner <owner>     Default owner for CODEOWNERS (default: researcher)
  --org <org>             GitHub organization name (default: org)
  --repo <repo>           GitHub repository name (default: repo)
  -h, --help              Show this help message

Example:
  $(basename "$0") /path/to/research-project --owner pi-name --org lab --repo awesome-vit
EOF
  exit 0
}

DEFAULT_OWNER="researcher"
ORG_NAME="org"
REPO_NAME="repo"
TARGET_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--owner) DEFAULT_OWNER="$2"; shift 2 ;;
    --org) ORG_NAME="$2"; shift 2 ;;
    --repo) REPO_NAME="$2"; shift 2 ;;
    -h|--help) print_usage ;;
    -*)
      echo "Unknown option: $1"
      print_usage
      ;;
    *)
      if [[ -z "$TARGET_DIR" ]]; then
        TARGET_DIR="$1"
        shift
      else
        echo "Unexpected argument: $1"
        print_usage
      fi
      ;;
  esac
done

if [[ -z "$TARGET_DIR" ]]; then
  echo "Error: target directory is required"
  print_usage
fi

if [[ ! -d "$TARGET_DIR" ]]; then
  mkdir -p "$TARGET_DIR"
fi

TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

echo "Initializing Auto-Research project in: $TARGET_DIR"

# Create directory structure
mkdir -p "$TARGET_DIR/.github/ISSUE_TEMPLATE"
mkdir -p "$TARGET_DIR/.github/workflows"
mkdir -p "$TARGET_DIR/references"
mkdir -p "$TARGET_DIR/templates"
mkdir -p "$TARGET_DIR/paper"
mkdir -p "$TARGET_DIR/figures"
mkdir -p "$TARGET_DIR/data"

# Copy and substitute
substitute() {
  local src="$1"
  local dst="$2"
  sed \
    -e "s/\${DEFAULT_OWNER}/$DEFAULT_OWNER/g" \
    -e "s/\${ORG_NAME}/$ORG_NAME/g" \
    -e "s/\${REPO_NAME}/$REPO_NAME/g" \
    "$src" > "$dst"
}

# GitHub config
echo "  → Installing GitHub configuration..."
substitute "$MANIFEST_DIR/.github/ISSUE_TEMPLATE/config.yml" "$TARGET_DIR/.github/ISSUE_TEMPLATE/config.yml"

for tmpl in "$MANIFEST_DIR/.github/ISSUE_TEMPLATE/"0*.yml; do
  cp "$tmpl" "$TARGET_DIR/.github/ISSUE_TEMPLATE/"
done

for wf in "$MANIFEST_DIR/.github/workflows/"*.yml; do
  cp "$wf" "$TARGET_DIR/.github/workflows/"
done

# Templates
echo "  → Installing templates..."
for tmpl in "$MANIFEST_DIR/templates/"*; do
  cp "$tmpl" "$TARGET_DIR/templates/"
done

# Reference docs
echo "  → Installing reference documentation..."
for ref in "$MANIFEST_DIR/references/"*; do
  cp "$ref" "$TARGET_DIR/references/"
done

echo ""
echo "✓ Auto-Research project initialized!"
echo ""
echo "Next steps:"
echo "  1. Create a research idea: open an issue using 'Research Idea' template"
echo "  2. Start the pipeline: aris/research-pipeline \"topic\" or ars/academic-pipeline \"topic\""
echo "  3. Deep research: ars/deep-research \"question\""
echo "  4. Write paper: ars/academic-paper \"paper\""
echo "  5. Submit for review: use 'Paper Submission' issue template"
echo "  6. Generate figures: use 'Figure Request' issue template"
echo ""
echo "Project structure created:"
echo "  paper/        - Paper source files"
echo "  figures/      - Generated figures"
echo "  data/         - Experiment data"
echo "  references/   - Research references"
echo "  templates/    - Research plan/paper templates"
