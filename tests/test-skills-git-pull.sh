#!/usr/bin/env bash
set -euo pipefail

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

mkdir -p "$tmp_dir/bin"
cat > "$tmp_dir/bin/git" <<'EOF'
#!/usr/bin/env bash
printf '%s|%s\n' "$PWD" "$*" >> "$SKILLS_PULL_LOG"
EOF
chmod +x "$tmp_dir/bin/git"

SKILLS_PULL_LOG="$tmp_dir/pulls.log" \
  PATH="$tmp_dir/bin:$PATH" \
  bash ./scripts/skills-git-pull.sh >/dev/null

if grep -Eq '/skills/(agent-skills|ai-investment-advisor)\|pull$' "$tmp_dir/pulls.log"; then
  echo "unmanaged submodule was pulled" >&2
  exit 1
fi
