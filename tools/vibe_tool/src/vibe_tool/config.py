"""Multi-strategy discovery of the vibe-coding repository root."""

import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "vibe-tool"
CONFIG_FILE = CONFIG_DIR / "config.json"


def _from_env() -> Path | None:
    """Check VIBE_HOME environment variable."""
    val = os.environ.get("VIBE_HOME", "").strip()
    if val and Path(val).is_dir():
        return Path(val)
    return None


def _from_cwd_walk() -> Path | None:
    """Walk up from current directory looking for manifests/ + skills/."""
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / "manifests").is_dir() and (parent / "skills").is_dir():
            return parent
    return None


def _from_config_file() -> Path | None:
    """Read repo path from ~/.config/vibe-tool/config.json."""
    if not CONFIG_FILE.exists():
        return None
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        path = Path(data.get("repo_path", ""))
        if path.is_dir() and (path / "manifests").is_dir():
            return path
    except (json.JSONDecodeError, KeyError, OSError):
        return None
    return None


def find_repo_root() -> Path:
    """Resolve the vibe-coding repository root.

    Priority: VIBE_HOME env > cwd walk-up > config file.
    Raises RuntimeError if not found.
    """
    for strategy in (_from_env, _from_cwd_walk, _from_config_file):
        result = strategy()
        if result is not None:
            return result.resolve()

    raise RuntimeError(
        "vibe-coding repository not found.\n"
        "  Set VIBE_HOME environment variable:\n"
        "    export VIBE_HOME=/path/to/vibe-coding\n"
        "  Or configure it permanently:\n"
        f"    vibe config set-repo /path/to/vibe-coding\n"
        "  Or run vibe from within the vibe-coding repo tree."
    )


def save_repo_path(path: str) -> Path:
    """Save repo path to config file, return resolved path."""
    resolved = Path(path).resolve()
    if not resolved.is_dir():
        raise NotADirectoryError(f"Not a directory: {resolved}")
    if not (resolved / "manifests").is_dir():
        raise ValueError(
            f"{resolved}: does not contain manifests/ directory — "
            "not a valid vibe-coding repository"
        )

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(
        json.dumps({"repo_path": str(resolved)}, indent=2) + "\n",
        encoding="utf-8",
    )
    return resolved
