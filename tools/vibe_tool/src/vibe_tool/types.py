"""Shared dataclasses."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ManifestInfo:
    name: str
    path: Path
    description: str
    has_init_script: bool
    init_script_path: Path | None
    scenarios: list[str] = field(default_factory=list)
    init_blacklisted: bool = False


@dataclass
class SkillInfo:
    name: str
    source_path: Path
    id_path: str
