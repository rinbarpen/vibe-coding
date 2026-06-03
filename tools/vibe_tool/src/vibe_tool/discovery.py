"""Dynamic discovery of manifests and skills."""

from collections import defaultdict
from pathlib import Path

from .types import ManifestInfo, SkillInfo

INIT_BLACKLIST = {"agent-browser"}


def discover_manifests(manifests_dir: Path) -> list[ManifestInfo]:
    """Scan manifests_dir for valid manifests (must have CLAUDE.md)."""
    manifests: list[ManifestInfo] = []
    for entry in sorted(manifests_dir.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        if entry.name in INIT_BLACKLIST:
            continue

        claude_md = entry / "CLAUDE.md"
        if not claude_md.exists():
            continue

        description = _read_description(claude_md)

        init_scripts = sorted(entry.glob("scripts/*init*.sh"))
        has_init = len(init_scripts) > 0
        init_path = init_scripts[0] if has_init else None

        scenarios_dir = entry / "scenarios"
        scenarios: list[str] = []
        if scenarios_dir.is_dir():
            scenarios = sorted(
                d.name for d in scenarios_dir.iterdir()
                if d.is_dir() and not d.name.startswith(".")
            )

        manifests.append(ManifestInfo(
            name=entry.name,
            path=entry,
            description=description,
            has_init_script=has_init,
            init_script_path=init_path,
            scenarios=scenarios,
        ))

    return manifests


def discover_skills(skills_root: Path) -> list[SkillInfo]:
    """Recursively find all directories containing SKILL.md under skills_root.

    Name collisions (same directory name in different sub-paths) are resolved
    by encoding the relative path with hyphens.
    """
    skill_md_files = sorted(skills_root.rglob("SKILL.md"))

    # Group by base directory name to detect collisions
    by_name: dict[str, list[tuple[Path, str]]] = defaultdict(list)
    for skill_md in skill_md_files:
        skill_dir = skill_md.parent
        try:
            rel = skill_dir.relative_to(skills_root)
        except ValueError:
            continue
        by_name[skill_dir.name].append((skill_dir, str(rel)))

    skills: list[SkillInfo] = []
    for entries in by_name.values():
        for skill_dir, rel_path in entries:
            if len(entries) == 1:
                name = skill_dir.name
            else:
                name = rel_path.replace("/", "-").replace("\\", "-")
            skills.append(SkillInfo(
                name=name,
                source_path=skill_dir,
                id_path=rel_path,
            ))

    return skills


def resolve_manifest(manifests_dir: Path, name: str) -> ManifestInfo:
    """Look up a single manifest by name. Raises ValueError with candidates."""
    manifests = discover_manifests(manifests_dir)
    by_name = {m.name: m for m in manifests}

    if name in by_name:
        return by_name[name]

    # Try case-insensitive match
    lower = name.lower()
    for m in manifests:
        if m.name.lower() == lower:
            return m

    # Try substring match
    candidates = [m.name for m in manifests if lower in m.name.lower()]
    if len(candidates) == 1:
        return by_name[candidates[0]]

    all_names = [m.name for m in manifests]
    raise ValueError(
        f"Manifest '{name}' not found.\n"
        f"Available: {', '.join(all_names)}"
    )


def resolve_skill(skills_root: Path, name: str) -> SkillInfo:
    """Look up a single skill by name. Raises ValueError with candidates."""
    skills = discover_skills(skills_root)
    by_name = {s.name: s for s in skills}
    by_lower = {s.name.lower(): s for s in skills}

    if name in by_name:
        return by_name[name]
    if name.lower() in by_lower:
        return by_lower[name.lower()]

    # Substring match
    lower = name.lower()
    candidates = [s.name for s in skills if lower in s.name.lower()]
    if len(candidates) == 1:
        return by_name[candidates[0]]
    if len(candidates) > 1:
        raise ValueError(
            f"Skill '{name}' is ambiguous. Candidates: {', '.join(candidates[:10])}"
        )

    raise ValueError(f"Skill '{name}' not found among {len(skills)} skills.")


def _read_description(claude_md: Path) -> str:
    """Extract the first meaningful line from CLAUDE.md as description."""
    try:
        content = claude_md.read_text(encoding="utf-8")
        for line in content.split("\n"):
            stripped = line.strip().lstrip("#").strip()
            if stripped and not stripped.startswith("---"):
                return stripped
    except OSError:
        pass
    return ""
