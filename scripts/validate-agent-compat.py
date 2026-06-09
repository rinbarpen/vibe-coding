#!/usr/bin/env python3
"""Validate native Claude Code and Codex agent compatibility files."""

from __future__ import annotations

import re
import sys
import tempfile
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = ROOT / "manifests"

NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
CLAUDE_TOOLS_RE = re.compile(r"^[A-Za-z0-9_:-]+(?:,\s*[A-Za-z0-9_:-]+)*$")


def main() -> int:
    errors: list[str] = []

    for role_doc in sorted(MANIFESTS.glob("*/agents/subagent-roles.md")):
        manifest = role_doc.parents[1]
        names = _role_names(role_doc)
        if not names:
            errors.append(f"{role_doc.relative_to(ROOT)}: no role names found")
            continue

        for name in names:
            errors.extend(_validate_claude_agent(manifest, name))
            errors.extend(_validate_codex_agent(manifest, name))

        errors.extend(_validate_install_script_mentions(manifest))

    errors.extend(_validate_generic_installer_copy())

    if errors:
        print("Agent compatibility validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Agent compatibility validation passed")
    return 0


def _role_names(path: Path) -> list[str]:
    names: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        numbered = re.match(r"^###\s+\d+\.\s+`([^`]+)`", line)
        if numbered:
            names.append(numbered.group(1))
            continue

        heading = re.match(r"^##\s+([a-z][a-z0-9-]+)\s*$", line)
        if heading:
            names.append(heading.group(1))

    return names


def _validate_claude_agent(manifest: Path, name: str) -> list[str]:
    errors: list[str] = []
    path = manifest / ".claude" / "agents" / f"{name}.md"
    label = path.relative_to(ROOT)

    if not path.is_file():
        return [f"{label}: missing Claude Code agent file"]

    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not match:
        return [f"{label}: missing YAML frontmatter"]

    frontmatter, body = match.groups()
    fields = _parse_simple_frontmatter(frontmatter)
    errors.extend(_require_field(label, fields, "name", name))
    errors.extend(_require_field(label, fields, "description"))

    if fields.get("name") and not NAME_RE.match(fields["name"]):
        errors.append(f"{label}: name must be lowercase kebab-case")
    if fields.get("tools") and not CLAUDE_TOOLS_RE.match(fields["tools"]):
        errors.append(f"{label}: tools must be a comma-separated tool list")
    if not body.strip():
        errors.append(f"{label}: body prompt is empty")

    return errors


def _validate_codex_agent(manifest: Path, name: str) -> list[str]:
    errors: list[str] = []
    path = manifest / ".codex" / "agents" / f"{name}.toml"
    label = path.relative_to(ROOT)

    if not path.is_file():
        return [f"{label}: missing Codex custom agent file"]

    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        return [f"{label}: invalid TOML: {exc}"]

    errors.extend(_require_field(label, data, "name", name))
    errors.extend(_require_field(label, data, "description"))
    errors.extend(_require_field(label, data, "developer_instructions"))

    if data.get("name") and not NAME_RE.match(data["name"]):
        errors.append(f"{label}: name must be lowercase kebab-case")

    return errors


def _parse_simple_frontmatter(frontmatter: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip("\"'")
    return fields


def _require_field(
    label: Path,
    fields: dict[str, object],
    name: str,
    expected: str | None = None,
) -> list[str]:
    value = fields.get(name)
    if not isinstance(value, str) or not value.strip():
        return [f"{label}: missing required field {name!r}"]
    if expected is not None and value != expected:
        return [f"{label}: {name!r} must be {expected!r}, got {value!r}"]
    return []


def _validate_install_script_mentions(manifest: Path) -> list[str]:
    scripts = sorted((manifest / "scripts").glob("*.sh"))
    if not scripts:
        return []

    script_text = "\n".join(script.read_text(encoding="utf-8") for script in scripts)
    errors: list[str] = []
    if ".claude/agents" not in script_text:
        errors.append(f"{manifest.relative_to(ROOT)}: init scripts do not install .claude/agents")
    if ".codex/agents" not in script_text:
        errors.append(f"{manifest.relative_to(ROOT)}: init scripts do not install .codex/agents")
    return errors


def _validate_generic_installer_copy() -> list[str]:
    sys.path.insert(0, str(ROOT / "tools" / "vibe_tool" / "src"))
    from vibe_tool.manifest import _generic_init  # noqa: PLC0415
    from vibe_tool.types import ManifestInfo  # noqa: PLC0415

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        source = base / "source"
        target = base / "target"
        (source / ".claude" / "agents").mkdir(parents=True)
        (source / ".codex" / "agents").mkdir(parents=True)
        (source / "CLAUDE.md").write_text("# Test\n", encoding="utf-8")
        (source / ".claude" / "agents" / "sample.md").write_text(
            "---\nname: sample\ndescription: Sample\n---\nPrompt\n",
            encoding="utf-8",
        )
        (source / ".codex" / "agents" / "sample.toml").write_text(
            'name = "sample"\ndescription = "Sample"\ndeveloper_instructions = "Prompt"\n',
            encoding="utf-8",
        )
        target.mkdir()

        manifest = ManifestInfo(
            name="sample",
            path=source,
            description="sample",
            has_init_script=False,
            init_script_path=None,
        )
        result = _generic_init(manifest, target, force=False, dry_run=False)
        if result != 0:
            return ["generic installer returned a non-zero exit code"]

        missing = []
        if not (target / ".claude" / "agents" / "sample.md").is_file():
            missing.append("generic installer did not copy .claude/agents")
        if not (target / ".codex" / "agents" / "sample.toml").is_file():
            missing.append("generic installer did not copy .codex/agents")
        return missing


if __name__ == "__main__":
    raise SystemExit(main())
