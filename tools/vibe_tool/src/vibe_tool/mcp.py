"""MCP server management: list available servers and install them into projects."""

import json
import sys
from pathlib import Path

MCP_FILENAME = "mcp.json"


def discover_mcp_servers(mcp_json: Path) -> dict[str, dict]:
    """Read available MCP servers from the repo's mcp.json."""
    if not mcp_json.exists():
        return {}
    try:
        data = json.loads(mcp_json.read_text(encoding="utf-8"))
        return data.get("mcpServers", {})
    except (json.JSONDecodeError, OSError):
        return {}


def _read_target_mcp(target_dir: Path) -> dict:
    """Read target project's mcp.json, return {mcpServers: {...}}."""
    path = target_dir / MCP_FILENAME
    if not path.exists():
        return {"mcpServers": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"mcpServers": {}}


def _write_target_mcp(target_dir: Path, data: dict, dry_run: bool = False) -> None:
    """Write merged mcp.json to target project."""
    path = target_dir / MCP_FILENAME
    if dry_run:
        print(f"[dry-run] Would write: {path}")
        return
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def add_mcp_servers(
    source_mcp: Path,
    target_dir: Path,
    names: list[str] | None = None,
    all_servers: bool = False,
    force: bool = False,
    dry_run: bool = False,
) -> int:
    """Add MCP servers from source to target project (merge, never overwrite)."""
    available = discover_mcp_servers(source_mcp)
    if not available:
        print("No MCP servers found in source.", file=sys.stderr)
        return 1

    if all_servers:
        to_add = list(available.keys())
    elif names:
        to_add = names
    else:
        print("Specify server name(s) or --all", file=sys.stderr)
        return 1

    target_data = _read_target_mcp(target_dir)
    servers = target_data.setdefault("mcpServers", {})
    added = 0
    skipped = 0

    for name in to_add:
        if name not in available:
            print(f"Unknown MCP server: {name}", file=sys.stderr)
            print(f"Available: {', '.join(available.keys())}", file=sys.stderr)
            return 1

        if name in servers and not force:
            print(f"  Skipping {name} (already exists, use --force to overwrite)")
            skipped += 1
            continue

        servers[name] = available[name]
        added += 1

    if added == 0 and skipped == len(to_add):
        print("All servers already installed. Nothing to do.")
        return 0

    _write_target_mcp(target_dir, target_data, dry_run=dry_run)
    label = "[dry-run] " if dry_run else ""
    if added:
        print(f"{label}Added {added} MCP server(s): {', '.join(to_add[:added])}")
    if skipped:
        print(f"  ({skipped} already existed, skipped)")
    return 0
