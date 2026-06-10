"""PostToolUse hook handler: records skill tool usage from hook stdin."""

import json
import sys

from .stats import record_usage

SKILL_TOOL_NAMES = {"Skill", "skill"}


def main() -> int:
    try:
        raw = sys.stdin.read()
        if not raw or not raw.strip():
            return 0
        hook_input = json.loads(raw)
    except (json.JSONDecodeError, OSError):
        return 0

    tool_name = hook_input.get("tool_name", "")
    if tool_name not in SKILL_TOOL_NAMES:
        return 0

    tool_input = hook_input.get("tool_input", {}) or {}
    skill_name = tool_input.get("name", "")
    if not skill_name:
        return 0

    record_usage(skill_name, tool_name=tool_name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
