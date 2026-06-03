"""Manifest init and add operations.

Delegates to existing init scripts when present, falls back to generic file-copy
for manifests without scripts.
"""

import shutil
import subprocess
import sys
from pathlib import Path

from .discovery import resolve_manifest
from .types import ManifestInfo

# ── Flag mapping per manifest init script ──

_SCRIPT_FLAG_MAP: dict[str, dict[str, str]] = {
    "vibe-coding": {
        "scenario": "--scenario={value}",
    },
    "github-enterprise": {
        "owner": "-o {value}",
        "org": "--org {value}",
        "repo": "--repo {value}",
        "email": "--email {value}",
        "force": "-f",
        "dry_run": "-n",
    },
}


def init_manifest(
    manifests_dir: Path,
    name: str,
    target: Path,
    *,
    force: bool = False,
    dry_run: bool = False,
    **kwargs: str,
) -> int:
    """Initialize a NEW project from a manifest.

    Creates target directory, then delegates to the manifest's init script
    or performs a generic file-copy init.
    """
    manifest = resolve_manifest(manifests_dir, name)

    target = target.resolve()
    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)

    if manifest.init_script_path is not None:
        return _run_init_script(manifest, target, force, dry_run, **kwargs)

    return _generic_init(manifest, target, force, dry_run)


def add_manifest(
    manifests_dir: Path,
    name: str,
    target: Path,
    *,
    force: bool = False,
    dry_run: bool = False,
    **kwargs: str,
) -> int:
    """Add manifest files to an EXISTING project.

    Same as init but expects target to already exist.
    """
    manifest = resolve_manifest(manifests_dir, name)

    target = target.resolve()
    if not target.is_dir():
        print(f"Error: target directory does not exist: {target}", file=sys.stderr)
        return 1

    if manifest.init_script_path is not None:
        return _run_init_script(manifest, target, force, dry_run, **kwargs)

    return _generic_init(manifest, target, force, dry_run)


# ── Script delegation ──

def _run_init_script(
    manifest: ManifestInfo,
    target: Path,
    force: bool,
    dry_run: bool,
    **kwargs: str,
) -> int:
    """Call the manifest's init shell script as a subprocess."""
    script_path = manifest.init_script_path
    assert script_path is not None

    flag_map = _SCRIPT_FLAG_MAP.get(manifest.name, {})

    # Build script arguments
    script_args: list[str] = []

    # github-enterprise accepts target as first positional arg
    if manifest.name == "github-enterprise":
        script_args.append(str(target))

    for key, value in kwargs.items():
        if not value:
            continue
        if key in ("force", "dry_run"):
            bool_val = key == "force" and force or key == "dry_run" and dry_run
            if bool_val and key in flag_map:
                script_args.append(flag_map[key])
            continue

        if key in flag_map:
            script_args.append(flag_map[key].format(value=value))

    # force/dry_run for manifests where they aren't in flag_map
    if force and "force" not in flag_map:
        script_args.append("-f")
    if dry_run and "dry_run" not in flag_map:
        script_args.append("-n")

    # Build environment (VIBE_MANIFEST needed by vibe-coding init)
    env = dict(subprocess.os.environ)
    env["VIBE_MANIFEST"] = str(manifest.path)

    cmd = [str(script_path)] + script_args

    if dry_run:
        print(f"[dry-run] Would run: {' '.join(cmd)}")
        print(f"[dry-run]   in: {target}")
        return 0

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=str(target),
        env=env,
    )
    return result.returncode


# ── Generic init (no script) ──

def _generic_init(
    manifest: ManifestInfo,
    target: Path,
    force: bool,
    dry_run: bool,
) -> int:
    """Copy manifest files into target using a standard layout."""
    src = manifest.path
    actions: list[tuple[str, Path]] = []

    # Directory structure
    dirs = [
        ".cursor/rules",
        ".cursor/plans",
        ".cursor/commands",
    ]
    for d in dirs:
        dest = target / d
        if dry_run:
            actions.append(("mkdir", dest))
        else:
            dest.mkdir(parents=True, exist_ok=True)

    # Root-level files (non-overwriting unless --force)
    root_files = ["CLAUDE.md", "AGENTS.md", ".cursorrules", "README.md", "CONTRIBUTING.md"]
    for filename in root_files:
        src_file = src / filename
        if not src_file.is_file():
            continue
        dst_file = target / filename
        if dst_file.exists() and not force:
            actions.append(("skip", dst_file))
            continue
        rel_src = _relpath(src_file, manifest.path)
        if dry_run:
            actions.append(("copy", dst_file))
        else:
            shutil.copy2(src_file, dst_file)
            actions.append(("copy", dst_file))

    # Rules (*.mdc → .cursor/rules/)
    rules_dir = src / "rules"
    if rules_dir.is_dir():
        for rule_file in sorted(rules_dir.glob("*.mdc")):
            dst_file = target / ".cursor" / "rules" / rule_file.name
            if dst_file.exists() and not force:
                actions.append(("skip", dst_file))
                continue
            if dry_run:
                actions.append(("copy", dst_file))
            else:
                _copy_with_subst(rule_file, dst_file, manifest.path, target)
                actions.append(("copy", dst_file))

    # Commands (*/ → .cursor/commands/)
    commands_dir = src / "commands"
    if commands_dir.is_dir():
        for cmd_dir in sorted(commands_dir.iterdir()):
            if not cmd_dir.is_dir():
                continue
            dst_dir = target / ".cursor" / "commands" / cmd_dir.name
            dst_dir.mkdir(parents=True, exist_ok=True)
            for cmd_file in cmd_dir.iterdir():
                if not cmd_file.is_file():
                    continue
                dst_file = dst_dir / cmd_file.name
                if dst_file.exists() and not force:
                    actions.append(("skip", dst_file))
                    continue
                if dry_run:
                    actions.append(("copy", dst_file))
                else:
                    shutil.copy2(cmd_file, dst_file)
                    actions.append(("copy", dst_file))

    # Print summary
    copies = [a for a in actions if a[0] == "copy"]
    skips = [a for a in actions if a[0] == "skip"]
    mkdirs = [a for a in actions if a[0] == "mkdir"]

    label = "[dry-run] Would install" if dry_run else "Installed"
    print(f"{label} {len(copies)} files to {target}")
    for action, path in copies:
        rel = _relpath(path, target)
        print(f"  COPY  {rel}")
    for action, path in skips:
        rel = _relpath(path, target)
        print(f"  SKIP  {rel} (exists)")

    return 0


def _copy_with_subst(src: Path, dst: Path, manifest_path: Path, target: Path) -> None:
    """Copy a file, substituting {{VIBE_MANIFEST}} with relative path."""
    content = src.read_text(encoding="utf-8")
    try:
        rel = manifest_path.resolve().relative_to(target.resolve())
        content = content.replace("{{VIBE_MANIFEST}}", str(rel))
    except ValueError:
        content = content.replace("{{VIBE_MANIFEST}}", str(manifest_path.resolve()))
    dst.write_text(content, encoding="utf-8")


def _relpath(p: Path, base: Path) -> str:
    try:
        return str(p.resolve().relative_to(base.resolve()))
    except ValueError:
        return str(p)
