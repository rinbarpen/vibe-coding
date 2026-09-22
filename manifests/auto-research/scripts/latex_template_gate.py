#!/usr/bin/env python3
"""Create and verify an immutable manifest for an official LaTeX template.

The venue requirements file is the source of the required-file list.  This tool
only records and verifies template metadata; it never edits .cls/.sty files.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys


class GateError(ValueError):
    pass


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise GateError(f"invalid JSON: {path}: {exc}") from exc


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def project_relative(root: Path, value: str) -> str:
    candidate = (root / value).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise GateError(f"path escapes project root: {value}")
    return candidate.relative_to(root.resolve()).as_posix()


def required_files(requirements: dict) -> list[str]:
    files = requirements.get("required_files", [])
    if not isinstance(files, list) or not all(isinstance(item, str) and item for item in files):
        raise GateError("requirements.required_files must be a list of non-empty strings")
    return files


def style_files(template_root: Path, requirements: dict) -> list[Path]:
    patterns = requirements.get("style_globs", ["**/*.cls", "**/*.sty", "**/*.bst"])
    if not isinstance(patterns, list) or not all(isinstance(item, str) and item for item in patterns):
        raise GateError("requirements.style_globs must be a list of strings")
    found = set()
    for pattern in patterns:
        found.update(path for path in template_root.glob(pattern) if path.is_file())
    return sorted(found)


def make_manifest(root: Path, args) -> dict:
    template_root_rel = project_relative(root, args.template_root)
    template_root = root / template_root_rel
    if not template_root.is_dir():
        raise GateError(f"template root does not exist: {template_root_rel}")
    requirements = read_json(root / project_relative(root, args.requirements))
    files = required_files(requirements)
    styles = style_files(template_root, requirements)
    if not styles:
        raise GateError("no template style files found; check style_globs and official template")
    normalized_required = [project_relative(root, str(Path(template_root_rel) / item)) for item in files]
    return {
        "schema_version": 1,
        "venue": requirements.get("venue", args.venue),
        "source_url": requirements.get("source_url", args.source_url),
        "checked_at": requirements.get("checked_at", dt.date.today().isoformat()),
        "template_root": template_root_rel,
        "required_files": normalized_required,
        "style_files_immutable": True,
        "style_files": [
            {"path": project_relative(root, str(path)), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in styles
        ],
    }


def verify(root: Path, manifest_path: Path) -> dict:
    manifest = read_json(manifest_path)
    if manifest.get("style_files_immutable") is not True:
        raise GateError("manifest does not lock style files")
    missing = []
    changed = []
    for item in manifest.get("required_files", []):
        if not (root / project_relative(root, item)).exists():
            missing.append(item)
    for item in manifest.get("style_files", []):
        path = root / project_relative(root, item["path"])
        if not path.is_file():
            changed.append({"path": item["path"], "reason": "missing"})
        elif sha256(path) != item.get("sha256"):
            changed.append({"path": item["path"], "reason": "sha256_changed"})
    result = {"valid": not missing and not changed, "missing_required_files": missing, "changed_style_files": changed}
    if not result["valid"]:
        raise GateError(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Lock and verify official LaTeX template styles")
    parser.add_argument("--project-root", default=".")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("manifest", help="create a template integrity manifest")
    init.add_argument("--template-root", required=True)
    init.add_argument("--requirements", required=True)
    init.add_argument("--output", required=True)
    init.add_argument("--venue", default=None)
    init.add_argument("--source-url", default=None)
    check = sub.add_parser("verify", help="verify required files and immutable style hashes")
    check.add_argument("--manifest", required=True)
    args = parser.parse_args(argv)
    root = Path(args.project_root).resolve()
    try:
        if args.command == "manifest":
            result = make_manifest(root, args)
            output = root / project_relative(root, args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            result = verify(root, root / project_relative(root, args.manifest))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (GateError, OSError) as exc:
        print(f"latex-template-gate: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
