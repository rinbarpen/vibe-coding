#!/usr/bin/env bash
# init-enterprise: Install the GitHub Enterprise Manifest into a target project.
# Installs into .claude/ (AI rules), .github/ (GitHub governance),
# and project root.  Idempotent — skips existing files unless --force.
set -euo pipefail

MANIFEST_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# ── Defaults ──
DEFAULT_OWNER="default-owner"
ORG_NAME="org"
REPO_NAME="repo"
SECURITY_EMAIL="security@example.com"
FORCE=false
DRY_RUN=false
TARGET=""

# ── Help ──
print_usage() {
  cat <<EOF
Usage: $(basename "$0") [target-dir] [options]

Install the GitHub Enterprise Development Manifest into a project.
Files are placed in .claude/ (AI rules), .github/ (GitHub governance),
and project root.  Idempotent — skips existing files unless --force.

Options:
  -o, --owner <owner>     Default owner/team for CODEOWNERS (default: default-owner)
  --org <org>             GitHub organization name (default: org)
  --repo <repo>           GitHub repository name (default: repo)
  --email <email>         Security contact email (default: security@example.com)
  -f, --force             Overwrite existing files
  -n, --dry-run           Preview what would be installed without writing
  -h, --help              Show this help message

Examples:
  $(basename "$0") . --owner team-lead --org mycompany --repo my-app
  $(basename "$0") /path/to/project --dry-run
  $(basename "$0") --owner octocat --force
EOF
  exit 0
}

# ── Parse args ──
while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--owner) DEFAULT_OWNER="$2"; shift 2 ;;
    --org) ORG_NAME="$2"; shift 2 ;;
    --repo) REPO_NAME="$2"; shift 2 ;;
    --email) SECURITY_EMAIL="$2"; shift 2 ;;
    -f|--force) FORCE=true; shift ;;
    -n|--dry-run) DRY_RUN=true; shift ;;
    -h|--help) print_usage ;;
    -*)
      echo "Unknown option: $1"
      print_usage ;;
    *)
      if [[ -z "$TARGET" ]]; then TARGET="$1"; shift
      else echo "Unexpected argument: $1"; print_usage; fi ;;
  esac
done

TARGET="${TARGET:-$(pwd)}"
mkdir -p "$TARGET"
TARGET="$(cd "$TARGET" && pwd)"

echo "GitHub Enterprise Manifest — init"
echo "  Source:  $MANIFEST_DIR"
echo "  Target:  $TARGET"
$DRY_RUN && echo "  Mode:    DRY RUN (no files will be written)"
echo ""

# ── Variable substitution helper ──
substitute() {
  local src="$1" dst="$2"
  sed \
    -e "s/\${DEFAULT_OWNER}/$DEFAULT_OWNER/g" \
    -e "s/\${ORG_NAME}/$ORG_NAME/g" \
    -e "s/\${REPO_NAME}/$REPO_NAME/g" \
    -e "s/\${SECURITY_EMAIL}/$SECURITY_EMAIL/g" \
    "$src" > "$dst"
}

# ── Install helper ──
# Usage: install_file <source> <dest> [needs_subst]
install_file() {
  local src="$1" dst="$2" needs_subst="${3:-false}"
  local label="${dst#$TARGET/}"

  if [[ -f "$dst" && "$FORCE" != true ]]; then
    echo "  SKIP  $label"
    return
  fi

  mkdir -p "$(dirname "$dst")"

  if $DRY_RUN; then
    echo "  WILL  $label"
    return
  fi

  if [[ "$needs_subst" == true ]]; then
    substitute "$src" "$dst"
  else
    cp "$src" "$dst"
  fi
  echo "  COPY  $label"
}

# ── Zone 1: .claude/ — AI rules, references, commands ──
echo "── Zone 1: .claude/ (AI rules, references, commands) ──"

install_file "$MANIFEST_DIR/CLAUDE.md" \
  "$TARGET/.claude/rules/github-enterprise.md"

install_file "$MANIFEST_DIR/AGENTS.md" \
  "$TARGET/AGENTS.md"

for ref in "$MANIFEST_DIR/references/"*; do
  [[ -f "$ref" ]] || continue
  install_file "$ref" "$TARGET/.claude/references/github-$(basename "$ref")"
done

for tmpl in "$MANIFEST_DIR/templates/"*; do
  [[ -f "$tmpl" ]] || continue
  install_file "$tmpl" "$TARGET/.claude/templates/github-$(basename "$tmpl")"
done

# ── Zone 2: .github/ — project governance ──
echo ""
echo "── Zone 2: .github/ (workflows, templates, governance) ──"

install_file "$MANIFEST_DIR/.github/CODEOWNERS" \
  "$TARGET/.github/CODEOWNERS" true

install_file "$MANIFEST_DIR/.github/SECURITY.md" \
  "$TARGET/.github/SECURITY.md" true

install_file "$MANIFEST_DIR/.github/CODE_OF_CONDUCT.md" \
  "$TARGET/.github/CODE_OF_CONDUCT.md" true

install_file "$MANIFEST_DIR/.github/dependabot.yml" \
  "$TARGET/.github/dependabot.yml" true

install_file "$MANIFEST_DIR/.github/ISSUE_TEMPLATE/config.yml" \
  "$TARGET/.github/ISSUE_TEMPLATE/config.yml" true

for tmpl in "$MANIFEST_DIR/.github/ISSUE_TEMPLATE/"*.yml; do
  [[ -f "$tmpl" && "$(basename "$tmpl")" != "config.yml" ]] || continue
  install_file "$tmpl" "$TARGET/.github/ISSUE_TEMPLATE/$(basename "$tmpl")"
done

install_file "$MANIFEST_DIR/.github/PULL_REQUEST_TEMPLATE/default.md" \
  "$TARGET/.github/PULL_REQUEST_TEMPLATE/default.md"

for wf in "$MANIFEST_DIR/.github/workflows/"*.yml; do
  [[ -f "$wf" ]] || continue
  install_file "$wf" "$TARGET/.github/workflows/$(basename "$wf")"
done

# ── Zone 3: Root config files ──
echo ""
echo "── Zone 3: Root config files ──"

install_file "$MANIFEST_DIR/.editorconfig" "$TARGET/.editorconfig"
install_file "$MANIFEST_DIR/.gitignore" "$TARGET/.gitignore"

# ── Summary ──
echo ""
echo "✓ GitHub Enterprise Manifest installed"
echo ""
echo "Next steps:"
echo "  1. Edit .github/CODEOWNERS with your actual teams"
echo "  2. Update .github/SECURITY.md with your security contact"
echo "  3. Configure branch protection rules in GitHub Web UI"
echo "  4. Adjust workflow language versions if needed"
echo "  5. Commit and push the changes"
echo ""
echo "Files installed under: $TARGET"
