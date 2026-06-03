"""CLI definition and dispatch for vibe-tool."""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from . import __version__
from .config import CONFIG_FILE, find_repo_root, save_repo_path
from .discovery import discover_manifests, discover_skills


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return 0

    try:
        return args.func(args)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vibe",
        description="Unified CLI for managing manifests and skills in the vibe-coding ecosystem.",
    )
    parser.add_argument("--version", action="version", version=f"vibe-tool {__version__}")

    subs = parser.add_subparsers(dest="command")

    # ── init ──
    init_p = subs.add_parser("init", help="Initialize a new project from a manifest")
    init_p.add_argument("manifest", help="Manifest name")
    init_p.add_argument("target", nargs="?", default=None, help="Target directory (default: <manifest>-project/)")
    init_p.add_argument("--scenario", default="", help="Comma-separated scenario names")
    init_p.add_argument("-f", "--force", action="store_true", help="Overwrite existing files")
    init_p.add_argument("-n", "--dry-run", action="store_true", help="Preview changes without writing")
    init_p.add_argument("-o", "--owner", default="", help="Default owner (github-enterprise)")
    init_p.add_argument("--org", default="", help="GitHub organization (github-enterprise)")
    init_p.add_argument("--repo", default="", help="GitHub repository (github-enterprise)")
    init_p.add_argument("--email", default="", help="Security contact (github-enterprise)")
    init_p.set_defaults(func=_cmd_init)

    # ── add ──
    add_p = subs.add_parser("add", help="Add a manifest or skill to a project")
    add_subs = add_p.add_subparsers(dest="add_target")

    # add manifest
    am_p = add_subs.add_parser("manifest", help="Add a manifest to an existing project")
    am_p.add_argument("manifest_name", help="Manifest name")
    am_p.add_argument("target", nargs="?", default=".", help="Target directory (default: current)")
    am_p.add_argument("-f", "--force", action="store_true", help="Overwrite existing files")
    am_p.add_argument("-n", "--dry-run", action="store_true", help="Preview changes without writing")
    am_p.add_argument("-o", "--owner", default="", help="Default owner (github-enterprise)")
    am_p.add_argument("--org", default="", help="GitHub organization (github-enterprise)")
    am_p.add_argument("--repo", default="", help="GitHub repository (github-enterprise)")
    am_p.add_argument("--email", default="", help="Security contact (github-enterprise)")
    am_p.set_defaults(func=_cmd_add_manifest)

    # add skill
    ask_p = add_subs.add_parser("skill", help="Add a skill to a project")
    ask_p.add_argument("skill_name", nargs="?", default=None, help="Skill name (omit with --all)")
    ask_p.add_argument("target", nargs="?", default=".", help="Target directory (default: current)")
    ask_p.add_argument("--all", action="store_true", help="Install all skills")
    ask_p.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompt for --all")
    ask_p.add_argument("-f", "--force", action="store_true", help="Overwrite existing skills")
    ask_p.add_argument("-n", "--dry-run", action="store_true", help="Preview changes without writing")
    ask_p.set_defaults(func=_cmd_add_skill)

    # ── list ──
    list_p = subs.add_parser("list", help="List available manifests and skills")
    list_p.add_argument("what", nargs="?", default="all", choices=["manifests", "skills", "all"])
    list_p.add_argument("--json", dest="json_out", action="store_true", help="JSON output")
    list_p.set_defaults(func=_cmd_list)

    # ── update ──
    upd_p = subs.add_parser("update", help="Update skill submodules (git submodule update --remote --merge)")
    upd_p.set_defaults(func=_cmd_update)

    # ── config ──
    cfg_p = subs.add_parser("config", help="Manage vibe-tool configuration")
    cfg_subs = cfg_p.add_subparsers(dest="config_action")

    csr_p = cfg_subs.add_parser("set-repo", help="Set the vibe-coding repository path")
    csr_p.add_argument("path", help="Path to the vibe-coding repository")
    csr_p.set_defaults(func=_cmd_config_set_repo)

    csh_p = cfg_subs.add_parser("show", help="Show current configuration")
    csh_p.set_defaults(func=_cmd_config_show)

    return parser


# ── Command handlers ──

def _get_repo_paths(args) -> tuple[Path, Path, Path]:
    """Resolve repo root, manifests dir, and skills dir."""
    root = find_repo_root()
    return root, root / "manifests", root / "skills"


def _cmd_init(args) -> int:
    from .manifest import init_manifest

    _, manifests_dir, _ = _get_repo_paths(args)
    target = Path(args.target or f"{args.manifest}-project")

    kwargs = _collect_kwargs(args)
    return init_manifest(
        manifests_dir,
        args.manifest,
        target,
        force=args.force,
        dry_run=args.dry_run,
        **kwargs,
    )


def _cmd_add_manifest(args) -> int:
    from .manifest import add_manifest

    _, manifests_dir, _ = _get_repo_paths(args)
    target = Path(args.target).resolve()

    kwargs = _collect_kwargs(args, source_attr="manifest_name")
    return add_manifest(
        manifests_dir,
        args.manifest_name,
        target,
        force=args.force,
        dry_run=args.dry_run,
        **kwargs,
    )


def _cmd_add_skill(args) -> int:
    from .skill import add_skill, add_all_skills

    _, _, skills_root = _get_repo_paths(args)
    target = Path(args.target).resolve()

    if args.all:
        if not args.yes and not args.dry_run:
            skills = discover_skills(skills_root)
            print(f"This will install {len(skills)} skills into {target}/.cursor/skills/")
            response = input("Continue? [y/N] ").strip().lower()
            if response not in ("y", "yes"):
                print("Aborted.")
                return 0
        return add_all_skills(skills_root, target, force=args.force, dry_run=args.dry_run)

    if not args.skill_name:
        print("Error: specify a skill name or use --all", file=sys.stderr)
        return 1

    return add_skill(skills_root, args.skill_name, target, force=args.force, dry_run=args.dry_run)


def _cmd_list(args) -> int:
    try:
        _, manifests_dir, skills_root = _get_repo_paths(args)
    except RuntimeError as e:
        if args.json_out:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.what in ("manifests", "all"):
        _list_manifests(manifests_dir, args.json_out)

    if args.what in ("skills", "all"):
        if args.what == "all":
            print()
        _list_skills(skills_root, args.json_out)

    return 0


def _list_manifests(manifests_dir: Path, json_out: bool) -> None:
    manifests = discover_manifests(manifests_dir)
    if json_out:
        print(json.dumps([asdict(m) for m in manifests], indent=2, default=str))
        return

    if not manifests:
        print("No manifests found.")
        return

    print(f"{'MANIFEST':<24} {'INIT':<6} {'DESCRIPTION'}")
    print("-" * 78)
    for m in manifests:
        marker = "script" if m.has_init_script else "generic"
        print(f"  {m.name:<22} {marker:<6} {m.description}")


def _list_skills(skills_root: Path, json_out: bool) -> None:
    skills = discover_skills(skills_root)
    if json_out:
        # Only print basic info to keep JSON manageable
        print(json.dumps([
            {"name": s.name, "id_path": s.id_path, "source": str(s.source_path)}
            for s in skills
        ], indent=2))
        return

    if not skills:
        print("No skills found.")
        return

    print(f"{len(skills)} skills found:")
    width = max(len(s.name) for s in skills[:50]) + 2 if skills else 20
    for s in skills[:50]:
        print(f"  {s.name:<{width}} ({s.id_path})")
    if len(skills) > 50:
        print(f"  ... and {len(skills) - 50} more")


def _cmd_update(args) -> int:
    try:
        root = find_repo_root()
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    import subprocess
    print("Updating skill submodules...")
    result = subprocess.run(
        ["git", "submodule", "update", "--remote", "--merge"],
        cwd=str(root),
    )
    return result.returncode


def _cmd_config_set_repo(args) -> int:
    try:
        repo_path = save_repo_path(args.path)
        print(f"vibe-coding repository set to: {repo_path}")
        return 0
    except (NotADirectoryError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def _cmd_config_show(args) -> int:
    if CONFIG_FILE.exists():
        print(CONFIG_FILE.read_text(encoding="utf-8"))
    else:
        print(f"No config file at {CONFIG_FILE}")
        print("Use 'vibe config set-repo /path/to/vibe-coding' to create one.")
    return 0


def _collect_kwargs(args, source_attr: str = "manifest") -> list:
    """Collect extra keyword arguments for init scripts from parsed args."""
    kwargs: dict[str, str] = {}
    for key in ("scenario", "owner", "org", "repo", "email"):
        val = getattr(args, key, None)
        if val:
            kwargs[key] = val
    return kwargs
