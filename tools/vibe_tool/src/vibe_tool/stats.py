"""Skill usage statistics: persistence, recording, and aggregation."""

import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

from .config import find_repo_root

STATS_FILENAME = "skill-stats.json"
STATS_DIR = Path(".vibe-tool")


def _stats_path() -> Path:
    try:
        root = find_repo_root()
    except RuntimeError:
        return STATS_DIR / STATS_FILENAME
    return root / STATS_DIR / STATS_FILENAME


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def load_stats() -> dict:
    path = _stats_path()
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except (json.JSONDecodeError, OSError):
        pass
    return {}


def save_stats(data: dict) -> None:
    path = _stats_path()
    _ensure_dir(path)
    tmp = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        delete=False,
        suffix=".tmp",
    )
    try:
        json.dump(data, tmp, indent=2, ensure_ascii=False)
        tmp.write("\n")
        tmp.close()
        os.replace(tmp.name, path)
    except OSError:
        os.unlink(tmp.name)
        raise


def record_usage(skill_name: str, tool_name: str | None = None) -> None:
    if not skill_name or not skill_name.strip():
        return
    skill_name = skill_name.strip()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    data = load_stats()
    entry = data.setdefault(skill_name, {"total": 0, "by_tool": {}, "last_used": ""})
    entry["total"] = entry.get("total", 0) + 1
    if tool_name:
        by_tool = entry.setdefault("by_tool", {})
        by_tool[tool_name] = by_tool.get(tool_name, 0) + 1
    entry["last_used"] = now
    save_stats(data)


def get_usage_stats() -> dict:
    return load_stats()


def format_stats(data: dict, by_tool: bool = False) -> str:
    if not data:
        return "No skill usage recorded yet."

    lines: list[str] = []
    total_uses = sum(
        entry.get("total", 0) or sum(entry.get("by_tool", {}).values())
        for entry in data.values()
    )
    lines.append(f"Skill Usage Statistics ({total_uses} total uses)")
    lines.append("─" * 60)

    sorted_skills = sorted(data.items(), key=lambda x: x[1].get("total", 0), reverse=True)

    if by_tool:
        header = f"{'skill':<30} {'tool':<20} {'count':>6}"
        lines.append(header)
        lines.append("─" * 60)
        for skill_name, entry in sorted_skills:
            by_tool_data = entry.get("by_tool", {})
            if by_tool_data:
                for t, c in sorted(by_tool_data.items(), key=lambda x: x[1], reverse=True):
                    lines.append(f"{skill_name:<30} {t:<20} {c:>6}")
            else:
                lines.append(f"{skill_name:<30} {'(unknown)':<20} {entry.get('total', 0):>6}")
    else:
        header = f"{'skill':<30} {'total':>6}  {'last used'}"
        lines.append(header)
        lines.append("─" * 60)
        for skill_name, entry in sorted_skills:
            total = entry.get("total", 0)
            last = entry.get("last_used", "")
            if last:
                last_short = last[:10]  # YYYY-MM-DD
            else:
                last_short = "-"
            lines.append(f"{skill_name:<30} {total:>6}  {last_short}")

    return "\n".join(lines)


def reset_stats(force: bool = False) -> bool:
    if not force:
        data = load_stats()
        if not data:
            return True
        print(f"This will reset {len(data)} skill statistics.", file=sys.stderr)
        response = input("Are you sure? [y/N] ").strip().lower()
        if response not in ("y", "yes"):
            print("Aborted.", file=sys.stderr)
            return False
    save_stats({})
    return True
