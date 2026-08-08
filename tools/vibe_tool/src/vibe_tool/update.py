"""Helpers for updating the repository's managed submodules."""

import subprocess
from pathlib import Path
from typing import Iterable


UNMANAGED_SUBMODULES = frozenset(
    {
        "skills/agent-skills",
        "skills/ai-investment-advisor",
    }
)


def filter_managed_submodule_paths(paths: Iterable[str]) -> list[str]:
    """Return submodule paths that participate in batch updates."""
    return [path for path in paths if path not in UNMANAGED_SUBMODULES]


def discover_submodule_paths(root: Path) -> list[str]:
    """Read registered submodule paths from the repository's .gitmodules."""
    result = subprocess.run(
        [
            "git",
            "config",
            "--file",
            str(root / ".gitmodules"),
            "--get-regexp",
            r"^submodule\..*\.path$",
        ],
        cwd=str(root),
        check=True,
        capture_output=True,
        text=True,
    )

    paths = []
    for line in result.stdout.splitlines():
        fields = line.split(maxsplit=1)
        if len(fields) == 2:
            paths.append(fields[1])
    return paths


def build_update_command(paths: Iterable[str]) -> list[str]:
    """Build a path-scoped batch update command for managed submodules."""
    managed_paths = filter_managed_submodule_paths(paths)
    if not managed_paths:
        return []
    return [
        "git",
        "submodule",
        "update",
        "--remote",
        "--merge",
        "--",
        *managed_paths,
    ]
