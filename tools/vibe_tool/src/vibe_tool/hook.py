"""Hook management: discover and install hook sets from hooks/ dir."""

import shutil
import sys
from pathlib import Path

HOOKS_DIRNAME = "hooks"


def discover_hooks(repo_root: Path) -> list[str]:
    """List available hook set names under repo_root/hooks/."""
    hooks_dir = repo_root / HOOKS_DIRNAME
    if not hooks_dir.is_dir():
        return []
    return sorted(
        e.name for e in hooks_dir.iterdir()
        if e.is_dir() and not e.name.startswith(".")
    )


def add_hooks(
    repo_root: Path,
    target_dir: Path,
    names: list[str] | None = None,
    all_hooks: bool = False,
    force: bool = False,
    dry_run: bool = False,
) -> int:
    """Install hooks from repo into target project's hooks/ dir (merge, never overwrite)."""
    available = discover_hooks(repo_root)
    if not available:
        print("No hooks found.", file=sys.stderr)
        return 1

    if all_hooks:
        to_add = available
    elif names:
        to_add = names
    else:
        print("Specify hook name(s) or --all", file=sys.stderr)
        return 1

    target_hooks_dir = target_dir / HOOKS_DIRNAME
    added = 0
    skipped = 0

    for name in to_add:
        if name not in available:
            print(f"Unknown hook set: {name}", file=sys.stderr)
            print(f"Available: {', '.join(available)}", file=sys.stderr)
            return 1

        src = repo_root / HOOKS_DIRNAME / name
        dst = target_hooks_dir / name

        if dst.exists() and not force:
            print(f"  Skipping {name} (already exists, use --force to overwrite)")
            skipped += 1
            continue

        if dry_run:
            print(f"[dry-run] Would copy: {src} -> {dst}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst, dirs_exist_ok=True)
        added += 1

    if added == 0 and skipped == len(to_add):
        print("All hooks already installed. Nothing to do.")
        return 0

    label = "[dry-run] " if dry_run else ""
    if added:
        print(f"{label}Installed {added} hook set(s): {', '.join(to_add[:added])}")
    if skipped:
        print(f"  ({skipped} already existed, skipped)")
    return 0
