#!/usr/bin/env bash
# install.sh — One-click install of vibe-tool via uv
#
# Usage:
#   curl -sSL https://.../install.sh | bash          # remote (future)
#   ./tools/vibe_tool/install.sh                      # local
#   uv tool install -e tools/vibe_tool                # manual
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== vibe-tool installer ==="

# Check uv is available
if ! command -v uv &>/dev/null; then
    echo "Error: uv is not installed."
    echo "  Install it: curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "  Or: pip install uv"
    exit 1
fi

echo "Installing vibe-tool from: $SCRIPT_DIR"
uv tool install --force -e "$SCRIPT_DIR"

echo ""
echo "=== Done ==="
echo "Try: vibe list manifests"
echo ""
echo "If 'vibe' is not found, add this to your PATH:"
echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
echo ""
echo "To uninstall: uv tool uninstall vibe-tool"
