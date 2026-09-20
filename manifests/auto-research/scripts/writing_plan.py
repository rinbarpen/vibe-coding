# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "PyYAML>=6.0.2,<7",
#   "jsonschema>=4.23,<5",
#   "Pillow>=10,<13",
# ]
# ///
"""Versioned Writing Plan tooling for the auto-research scaffold."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator


EXIT_OK = 0
EXIT_INVALID = 1
EXIT_ERROR = 2
SCRIPT_DIR = Path(__file__).resolve().parent
MANIFEST_DIR = SCRIPT_DIR.parent
WRITING_DIR = MANIFEST_DIR / "writing"
SCHEMA_PATH = WRITING_DIR / "writing-plan.schema.json"
PROFILES_PATH = WRITING_DIR / "profiles.yaml"
VENUES_PATH = WRITING_DIR / "venue-profiles.yaml"
FIGURE_TYPES_PATH = WRITING_DIR / "figure-types.yaml"
MIGRATION_DEFAULTS_PATH = WRITING_DIR / "migration-defaults.yaml"
CONFIG_KEYS = (
    "objective",
    "audience",
    "style",
    "length",
    "content",
    "evidence",
    "presentation",
    "acceptance",
    "approval",
)
PROFILE_CATEGORIES = ("audience", "style", "evidence", "presentation")
FIGURE_TYPES = (
    "architecture", "flowchart", "pipeline", "algorithm", "comparison", "ablation",
    "training_curve", "scaling", "distribution", "scatter", "heatmap", "confusion_matrix",
    "qualitative_grid", "attention", "timeline", "map", "concept_illustration",
)
IDENTITY_KEYS = ("id", "type", "parent_id", "title", "order", "output_path", "anchor")
ID_PATTERN = re.compile(r"^[a-z][a-z0-9-]{2,63}$")
ANCHOR_PATTERN = "<!-- node:{node_id}:{boundary} -->"
UNSET = object()


class PlanInvalid(Exception):
    """Raised for expected configuration/content failures."""

    def __init__(self, errors: list[dict[str, Any]]):
        super().__init__("writing plan is invalid")
        self.errors = errors


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise PlanInvalid([error("schema", "$", "document root must be an object")])
    return data


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise PlanInvalid([error("input", "$", "document root must be an object")])
    return data


def error(code: str, path: str, message: str, **extra: Any) -> dict[str, Any]:
    value: dict[str, Any] = {"code": code, "path": path, "message": message}
    value.update(extra)
    return value


def json_path(parts: Iterable[Any]) -> str:
    result = "$"
    for part in parts:
        result += f"[{part}]" if isinstance(part, int) else f".{part}"
    return result


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def write_json(path: Path, value: Any) -> None:
    atomic_write(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def write_yaml(path: Path, value: Any) -> None:
    atomic_write(path, yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=100))


def canonical_hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def schema_errors(plan: dict[str, Any]) -> list[dict[str, Any]]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    result = []
    for item in sorted(validator.iter_errors(plan), key=lambda e: (list(e.absolute_path), e.message)):
        result.append(error("schema_error", json_path(item.absolute_path), item.message))
    return result


def profile_pack(plan: dict[str, Any]) -> dict[str, Any]:
    builtins = load_yaml(PROFILES_PATH)
    profiles = copy.deepcopy(builtins.get("profiles", {}))
    for category, values in plan.get("profiles", {}).items():
        profiles.setdefault(category, {})
        profiles[category].update(copy.deepcopy(values))
    return {"defaults": copy.deepcopy(builtins.get("defaults", {})), "profiles": profiles}


def venue_pack() -> dict[str, Any]:
    data = load_yaml(VENUES_PATH)
    return {"version": data.get("version", 1), "profiles": copy.deepcopy(data.get("profiles", {}))}


def figure_type_pack() -> dict[str, Any]:
    data = load_yaml(FIGURE_TYPES_PATH)
    return {"version": data.get("version", 1), "types": copy.deepcopy(data.get("types", {})), "defaults": copy.deepcopy(data.get("defaults", {}))}


def resolve_venue(value: dict[str, Any] | None) -> dict[str, Any]:
    """Materialize a venue snapshot so every resolved node carries submission rules."""
    value = value or {}
    profile_name = value.get("profile")
    if not profile_name:
        return {"requirements": {}}
    profiles = venue_pack()["profiles"]
    if profile_name not in profiles:
        raise PlanInvalid([error("invalid_venue_profile", "$.venue.profile", f"unknown venue profile {profile_name!r}")])
    profile = copy.deepcopy(profiles[profile_name])
    overrides = value.get("overrides", {})
    if isinstance(overrides, dict):
        profile = merge_value(profile, overrides)
    profile.pop("profile", None)
    if value.get("source_url"):
        profile["source_url"] = value["source_url"]
    if value.get("checked_at"):
        profile["checked_at"] = value["checked_at"]
    return {"profile": profile_name, "requirements": clean_markers(profile)}


def semantic_errors(plan: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    nodes = plan.get("nodes", [])
    if not isinstance(nodes, list):
        return errors
    ids = [node.get("id") for node in nodes if isinstance(node, dict) and isinstance(node.get("id"), str)]
    counts = Counter(ids)
    for node_id, count in sorted(counts.items()):
        if count > 1:
            errors.append(error("duplicate_id", "$.nodes", f"node id {node_id!r} occurs {count} times", node_id=node_id))
    node_map = {node.get("id"): node for node in nodes if isinstance(node, dict) and counts[node.get("id")] == 1}

    for index, node in enumerate(nodes):
        if not isinstance(node, dict) or "id" not in node:
            continue
        node_id = node["id"]
        parent_id = node.get("parent_id")
        if parent_id is not None and parent_id not in node_map:
            errors.append(error("missing_parent", f"$.nodes[{index}].parent_id", f"parent {parent_id!r} does not exist", node_id=node_id))
        if parent_id == node_id:
            errors.append(error("parent_cycle", f"$.nodes[{index}].parent_id", "node cannot be its own parent", node_id=node_id))

    for node_id in sorted(node_map):
        seen: list[str] = []
        current = node_id
        while current in node_map:
            if current in seen:
                cycle = seen[seen.index(current) :] + [current]
                errors.append(error("parent_cycle", "$.nodes", "parent cycle: " + " -> ".join(cycle), node_id=node_id))
                break
            seen.append(current)
            current = node_map[current].get("parent_id")

    pack = profile_pack(plan)
    all_profiles = pack["profiles"]
    profile_checks: list[tuple[str, dict[str, Any]]] = []
    profile_checks.append(("$.defaults", plan.get("defaults", {})))
    profile_checks.append(("$.document.defaults", plan.get("document", {}).get("defaults", {})))
    for category, entries in plan.get("profiles", {}).items():
        for name, value in entries.items():
            profile_checks.append((f"$.profiles.{category}.{name}", {category: value}))
    for index, node in enumerate(nodes):
        if isinstance(node, dict):
            profile_checks.append((f"$.nodes[{index}]", node))
    for base_path, config in profile_checks:
        for category in PROFILE_CATEGORIES:
            value = config.get(category, {}) if isinstance(config, dict) else {}
            name = value.get("profile") if isinstance(value, dict) else None
            if name and name not in all_profiles.get(category, {}):
                errors.append(error("invalid_profile", f"{base_path}.{category}.profile", f"unknown {category} profile {name!r}"))
            if category == "audience" and isinstance(value, dict):
                primary = value.get("primary", {})
                primary_name = primary.get("profile") if isinstance(primary, dict) else None
                if primary_name and primary_name not in all_profiles.get("audience", {}):
                    errors.append(error("invalid_profile", f"{base_path}.audience.primary.profile", f"unknown audience profile {primary_name!r}"))
                secondary = value.get("secondary", [])
                if isinstance(secondary, list):
                    for audience_index, audience in enumerate(secondary):
                        secondary_name = audience.get("profile") if isinstance(audience, dict) else None
                        if secondary_name and secondary_name not in all_profiles.get("audience", {}):
                            errors.append(error("invalid_profile", f"{base_path}.audience.secondary[{audience_index}].profile", f"unknown audience profile {secondary_name!r}"))

    venue_cfg = plan.get("venue", {})
    if isinstance(venue_cfg, dict) and venue_cfg.get("profile"):
        venue_profiles = venue_pack()["profiles"]
        if venue_cfg["profile"] not in venue_profiles:
            errors.append(error("invalid_venue_profile", "$.venue.profile", f"unknown venue profile {venue_cfg['profile']!r}"))
        if venue_cfg.get("source_url") and not str(venue_cfg["source_url"]).startswith(("http://", "https://")):
            errors.append(error("invalid_venue_source", "$.venue.source_url", "venue source_url must be an HTTP(S) URL"))

    figure_types = figure_type_pack()["types"]
    figure_ids: dict[str, str] = {}

    def check_figures(base_path: str, presentation: Any, node_id: str | None = None) -> None:
        if not isinstance(presentation, dict) or not isinstance(presentation.get("figures"), list):
            return
        for figure_index, figure in enumerate(presentation["figures"]):
            path = f"{base_path}.figures[{figure_index}]"
            if not isinstance(figure, dict):
                errors.append(error("invalid_figure_spec", path, "figure specification must be an object"))
                continue
            figure_id = figure.get("id")
            if isinstance(figure_id, str):
                if not ID_PATTERN.fullmatch(figure_id):
                    errors.append(error("invalid_figure_id", f"{path}.id", "figure id must use lower kebab-case", figure_id=figure_id))
                elif figure_id in figure_ids:
                    errors.append(error("duplicate_figure_id", f"{path}.id", f"figure id {figure_id!r} already used by {figure_ids[figure_id]!r}"))
                else:
                    figure_ids[figure_id] = node_id or path
            figure_type = figure.get("type")
            if figure_type not in figure_types:
                errors.append(error("unknown_figure_type", f"{path}.type", f"unknown figure type {figure_type!r}"))
            renderer = figure.get("renderer")
            if figure_type in figure_types and renderer != figure_types[figure_type].get("renderer") and not (renderer == "plot" and figure_types[figure_type].get("renderer") == "paper-figure"):
                errors.append(error("figure_renderer_mismatch", f"{path}.renderer", f"figure type {figure_type!r} expects renderer {figure_types[figure_type].get('renderer')!r}"))
            if figure.get("outputs") and not figure.get("formats"):
                errors.append(error("figure_formats_missing", f"{path}.formats", "formats must be declared when figure outputs are listed"))
            if figure_type in {"comparison", "ablation", "training_curve", "scaling", "distribution", "scatter", "heatmap", "confusion_matrix", "qualitative_grid", "attention"} and not (figure.get("data_source") or figure.get("input_files")):
                errors.append(error("figure_data_source_missing", path, "data-driven figure requires data_source or input_files"))
            if figure_type == "concept_illustration" and not figure.get("alt_text"):
                errors.append(error("figure_alt_text_missing", f"{path}.alt_text", "concept illustrations require alt_text"))

    for base_path, config, node_id in [
        ("$.defaults", plan.get("defaults", {}), None),
        ("$.document.defaults", plan.get("document", {}).get("defaults", {}), None),
    ]:
        check_figures(base_path + ".presentation", config.get("presentation", {}) if isinstance(config, dict) else {}, node_id)
    for index, node in enumerate(nodes):
        if isinstance(node, dict):
            check_figures(f"$.nodes[{index}].presentation", node.get("presentation", {}), node.get("id"))

    for category, entries in all_profiles.items():
        for name in entries:
            seen: list[str] = []
            current = name
            while current:
                if current in seen:
                    errors.append(error("profile_cycle", f"$.profiles.{category}.{name}", "profile cycle: " + " -> ".join(seen + [current])))
                    break
                seen.append(current)
                current_value = entries.get(current, {})
                current = current_value.get("profile") if isinstance(current_value, dict) else None
                if current and current not in entries:
                    break

    output_paths: dict[str, str] = {}
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            continue
        node_id = node.get("id")
        output_path = node.get("output_path")
        if node.get("type") == "file":
            if not output_path:
                errors.append(error("missing_output", f"$.nodes[{index}].output_path", "file node requires output_path", node_id=node_id))
            elif output_path in output_paths:
                errors.append(error("output_conflict", f"$.nodes[{index}].output_path", f"file output conflicts with {output_paths[output_path]!r}", node_id=node_id))
            else:
                output_paths[output_path] = str(node_id)
        length = node.get("length", {})
        if isinstance(length, dict):
            minimum, target, maximum = length.get("min"), length.get("target"), length.get("max")
            if minimum is not None and target is not None and minimum > target:
                errors.append(error("invalid_length", f"$.nodes[{index}].length", "min must be <= target", node_id=node_id))
            if target is not None and maximum is not None and target > maximum:
                errors.append(error("invalid_length", f"$.nodes[{index}].length", "target must be <= max", node_id=node_id))
            if minimum is not None and maximum is not None and minimum > maximum:
                errors.append(error("invalid_length", f"$.nodes[{index}].length", "min must be <= max", node_id=node_id))
        cross_refs = node.get("content", {}).get("cross_references", []) if isinstance(node.get("content"), dict) else []
        if isinstance(cross_refs, list):
            for ref in cross_refs:
                if isinstance(ref, str) and ref not in node_map:
                    errors.append(error("broken_reference", f"$.nodes[{index}].content.cross_references", f"referenced node {ref!r} does not exist", node_id=node_id, referenced_id=ref))

    for node_id in sorted(plan.get("approvals", {})):
        if node_id not in node_map:
            errors.append(error("orphaned_approval", f"$.approvals.{node_id}", f"approval references missing node {node_id!r}", node_id=node_id))
    return deduplicate_errors(errors)


def deduplicate_errors(errors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique: dict[str, dict[str, Any]] = {}
    for item in errors:
        key = json.dumps(item, ensure_ascii=False, sort_keys=True)
        unique[key] = item
    return sorted(unique.values(), key=lambda item: (item["path"], item["code"], item["message"]))


def validate_plan(plan: dict[str, Any]) -> list[dict[str, Any]]:
    structural = schema_errors(plan)
    if structural:
        return structural
    return semantic_errors(plan)


def is_marker(value: Any, name: str) -> bool:
    return isinstance(value, dict) and set(value) == {name}


def merge_value(parent: Any, child: Any) -> Any:
    if is_marker(child, "unset") and child["unset"] is True:
        return UNSET
    if is_marker(child, "append"):
        base = copy.deepcopy(parent) if isinstance(parent, list) else []
        return base + copy.deepcopy(child["append"])
    if isinstance(parent, dict) and isinstance(child, dict):
        result = copy.deepcopy(parent)
        for key, value in child.items():
            merged = merge_value(result.get(key), value)
            if merged is UNSET:
                result.pop(key, None)
            else:
                result[key] = merged
        return result
    return copy.deepcopy(child)


def clean_markers(value: Any) -> Any:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if key == "profile":
                continue
            cleaned = clean_markers(item)
            if cleaned is not UNSET:
                result[key] = cleaned
        return result
    if isinstance(value, list):
        return [clean_markers(item) for item in value]
    return copy.deepcopy(value)


def resolve_profile(category: str, name: str, profiles: dict[str, Any], stack: tuple[str, ...] = ()) -> dict[str, Any]:
    if name in stack:
        raise PlanInvalid([error("profile_cycle", f"$.profiles.{category}.{name}", "profile cycle: " + " -> ".join(stack + (name,)))])
    value = copy.deepcopy(profiles[category][name])
    parent_name = value.pop("profile", None)
    base: dict[str, Any] = {}
    if parent_name:
        base = resolve_profile(category, parent_name, profiles, stack + (name,))
    merged = merge_value(base, value)
    return {} if merged is UNSET else clean_markers(merged)


def expand_audience(value: dict[str, Any], profiles: dict[str, Any]) -> dict[str, Any]:
    """Resolve audience profiles used at category, primary, or secondary level."""
    expanded = copy.deepcopy(value)
    primary = expanded.get("primary")
    if isinstance(primary, dict) and primary.get("profile"):
        name = primary["profile"]
        profile = resolve_profile("audience", name, profiles)
        base_primary = profile.get("primary", profile)
        local_primary = {key: item for key, item in primary.items() if key != "profile"}
        expanded["primary"] = merge_value(base_primary, local_primary)
    secondary = expanded.get("secondary")
    if isinstance(secondary, list):
        resolved_secondary = []
        for audience in secondary:
            if isinstance(audience, dict) and audience.get("profile"):
                name = audience["profile"]
                profile = resolve_profile("audience", name, profiles)
                base_secondary = profile.get("primary", profile)
                local_secondary = {key: item for key, item in audience.items() if key != "profile"}
                resolved_secondary.append(merge_value(base_secondary, local_secondary))
            else:
                resolved_secondary.append(copy.deepcopy(audience))
        expanded["secondary"] = resolved_secondary
    return expanded


def apply_config(base: dict[str, Any], layer: dict[str, Any], profiles: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for category in PROFILE_CATEGORIES:
        value = layer.get(category)
        if isinstance(value, dict) and value.get("profile"):
            profile_value = resolve_profile(category, value["profile"], profiles)
            merged = merge_value(result.get(category, {}), profile_value)
            result[category] = {} if merged is UNSET else merged
    for key in CONFIG_KEYS:
        if key not in layer:
            continue
        value = layer[key]
        if key in PROFILE_CATEGORIES and isinstance(value, dict):
            value = {k: v for k, v in value.items() if k != "profile"}
        if key == "audience" and isinstance(value, dict):
            value = expand_audience(value, profiles)
        merged = merge_value(result.get(key), value)
        if merged is UNSET:
            result.pop(key, None)
        else:
            result[key] = merged
    return clean_markers(result)


def resolve_plan(plan: dict[str, Any]) -> dict[str, Any]:
    errors = validate_plan(plan)
    if errors:
        raise PlanInvalid(errors)
    pack = profile_pack(plan)
    profiles = pack["profiles"]
    venue = resolve_venue(plan.get("venue"))
    figure_library = figure_type_pack()
    palette_library = load_yaml(WRITING_DIR / "figure-palettes.yaml")
    base = apply_config({}, pack["defaults"], profiles)
    base = apply_config(base, plan.get("defaults", {}), profiles)
    base = apply_config(base, plan.get("document", {}).get("defaults", {}), profiles)
    nodes = plan.get("nodes", [])
    node_map = {node["id"]: node for node in nodes}
    cache: dict[str, dict[str, Any]] = {}

    def resolve_node(node_id: str) -> dict[str, Any]:
        if node_id in cache:
            return copy.deepcopy(cache[node_id])
        node = node_map[node_id]
        parent_id = node.get("parent_id")
        inherited = base
        if parent_id:
            parent = resolve_node(parent_id)
            inherited = {key: copy.deepcopy(parent[key]) for key in CONFIG_KEYS if key in parent}
        resolved_config = apply_config(inherited, node, profiles)
        presentation = resolved_config.get("presentation")
        if isinstance(presentation, dict) and isinstance(presentation.get("figures"), list):
            materialized = []
            for figure in presentation["figures"]:
                if not isinstance(figure, dict):
                    materialized.append(copy.deepcopy(figure))
                    continue
                item = copy.deepcopy(figure)
                figure_type = item.get("type")
                if figure_type in figure_library["types"]:
                    item["type_requirements"] = copy.deepcopy(figure_library["types"][figure_type])
                visual = merge_value(palette_library["defaults"], presentation.get("figure_style", {}))
                visual = merge_value(visual, item.get("visual", {}))
                mode = visual.get("mode", figure_library["types"][figure_type]["implementation"]["color_mode"])
                visual["mode"] = mode
                visual["colors"] = visual.get("colors", copy.deepcopy(palette_library["palettes"][visual["palette"]][mode]))
                item["resolved_visual"] = visual
                item["generation_defaults"] = copy.deepcopy(figure_library["defaults"])
                materialized.append(item)
            resolved_config["presentation"]["figures"] = materialized
        result = {key: copy.deepcopy(node[key]) for key in IDENTITY_KEYS if key in node}
        result.update(resolved_config)
        result["venue"] = copy.deepcopy(venue)
        if "output_path" not in result and parent_id:
            ancestor = resolve_node(parent_id)
            if "output_path" in ancestor:
                result["output_path"] = ancestor["output_path"]
        requirement_view = {key: result.get(key) for key in CONFIG_KEYS if key in result}
        requirement_view["venue"] = venue
        plan_hash = canonical_hash(requirement_view)
        result["resolved_plan_hash"] = plan_hash
        approval = plan.get("approvals", {}).get(node_id)
        if result.get("approval", "auto") == "auto":
            result["approval_state"] = "not_required"
        elif not approval:
            result["approval_state"] = "pending"
        elif approval.get("resolved_plan_hash") != plan_hash:
            result["approval_state"] = "stale"
        else:
            result["approval_state"] = approval.get("status", "pending")
        cache[node_id] = result
        return copy.deepcopy(result)

    resolved_nodes = [resolve_node(node["id"]) for node in nodes]
    workflow = merge_value(
        {"review_after_write": True, "auto_fix": "constrained", "fail_on": ["schema_error", "missing_required_content"]},
        plan.get("workflow", {}),
    )
    gates = [
        {"node_id": node["id"], "state": node["approval_state"], "resolved_plan_hash": node["resolved_plan_hash"]}
        for node in resolved_nodes
        if node.get("approval") == "before_write" and node.get("approval_state") != "approved"
    ]
    return {
        "version": 1,
        "source_version": plan["version"],
        "document": {key: copy.deepcopy(value) for key, value in plan["document"].items() if key != "defaults"},
        "venue": copy.deepcopy(venue),
        "figure_library_version": figure_library["version"],
        "defaults": base,
        "workflow": workflow,
        "legacy_notes": copy.deepcopy(plan.get("legacy_notes", [])),
        "migration_notes": copy.deepcopy(plan.get("migration_notes", [])),
        "nodes": resolved_nodes,
        "approval_gates": gates,
    }


def flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    result: dict[str, Any] = {}
    if isinstance(value, dict):
        for key in sorted(value):
            path = f"{prefix}.{key}" if prefix else key
            result.update(flatten(value[key], path))
    else:
        result[prefix] = value
    return result


def changed_fields(parent: dict[str, Any], node: dict[str, Any]) -> list[str]:
    parent_flat = flatten({key: parent.get(key) for key in CONFIG_KEYS if key in parent})
    node_flat = flatten({key: node.get(key) for key in CONFIG_KEYS if key in node})
    return sorted(key for key in set(parent_flat) | set(node_flat) if parent_flat.get(key, UNSET) != node_flat.get(key, UNSET))


def inline(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, list):
        return "、".join(str(item) for item in value) if value else "—"
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def render_plan(resolved: dict[str, Any]) -> str:
    document = resolved.get("document", {})
    nodes = resolved.get("nodes", [])
    node_map = {node["id"]: node for node in nodes}
    children: dict[str | None, list[dict[str, Any]]] = {}
    for node in nodes:
        children.setdefault(node.get("parent_id"), []).append(node)
    for entries in children.values():
        entries.sort(key=lambda item: (item.get("order", 0), item["id"]))
    lines = [
        "<!-- 由 .auto-research/writing-plan.yaml 生成；人工编辑不会被读取。 -->",
        "# Writing Plan",
        "",
        "## 1. 文档目的与成功标准",
        "",
        f"- **ID**：`{document.get('id', '')}`",
        f"- **标题**：{document.get('title', '')}",
        f"- **目的**：{document.get('purpose', '—')}",
        f"- **语言**：`{document.get('language', '—')}`",
        f"- **成功标准**：{inline(document.get('success_criteria', []))}",
        "",
        "## 2. 全局受众和文风默认值",
        "",
        "```json",
        json.dumps({key: resolved.get("defaults", {}).get(key) for key in ("audience", "style")}, ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
        "## 3. 投稿目标与图生成策略",
        "",
        f"- **投稿 profile**：`{resolved.get('venue', {}).get('profile') or '未指定'}`",
        f"- **要求来源**：{resolved.get('venue', {}).get('requirements', {}).get('source_url', '—')}",
        f"- **要求快照时间**：`{resolved.get('venue', {}).get('requirements', {}).get('checked_at', '—')}`",
        f"- **图类型库版本**：`{resolved.get('figure_library_version', '—')}`",
        "- 生成规则：先按 figure type 选择 renderer，再按 venue requirements 校验尺寸、格式、分辨率、可访问性和提交阶段。",
        "",
        "## 4. 文件与内容节点树",
        "",
    ]

    def emit_tree(parent_id: str | None, depth: int) -> None:
        for node in children.get(parent_id, []):
            lines.append(f"{'  ' * depth}- `{node['id']}` [{node['type']}] {node['title']}")
            emit_tree(node["id"], depth + 1)

    emit_tree(None, 0)
    lines += ["", "## 5. 节点执行要求", ""]
    ordered: list[dict[str, Any]] = []

    def collect(parent_id: str | None) -> None:
        for node in children.get(parent_id, []):
            ordered.append(node)
            collect(node["id"])

    collect(None)
    for node in ordered:
        parent = node_map.get(node.get("parent_id"), resolved.get("defaults", {}))
        deltas = changed_fields(parent, node)
        objective = node.get("objective", {})
        lines += [
            f"### `{node['id']}` — {node['title']}",
            "",
            f"- **类型 / 顺序**：`{node['type']}` / {node.get('order', 0)}",
            f"- **父节点**：`{node.get('parent_id', '—')}`",
            f"- **输出位置**：`{node.get('output_path', '—')}`",
            f"- **目标问题**：{inline(objective.get('question'))}",
            f"- **核心信息**：{inline(objective.get('key_message'))}",
            f"- **读者行动**：{inline(objective.get('reader_action'))}",
            f"- **受众**：{inline(node.get('audience'))}",
            f"- **风格**：{inline(node.get('style'))}",
            f"- **篇幅**：{inline(node.get('length'))}",
            f"- **内容**：{inline(node.get('content'))}",
            f"- **证据**：{inline(node.get('evidence'))}",
            f"- **呈现**：{inline(node.get('presentation'))}",
            f"- **投稿要求**：{inline(node.get('venue'))}",
            f"- **验收**：{inline(node.get('acceptance'))}",
            f"- **审批**：`{node.get('approval', 'auto')}` / `{node.get('approval_state', 'not_required')}`",
            f"- **要求哈希**：`{node.get('resolved_plan_hash', '')}`",
            f"- **相对父节点变化**：{inline(deltas)}",
            "",
        ]
    lines += ["## 6. 待审批节点", ""]
    gates = resolved.get("approval_gates", [])
    if gates:
        for gate in gates:
            lines.append(f"- `{gate['node_id']}` — {gate['state']} — `{gate['resolved_plan_hash']}`")
    else:
        lines.append("- 无")
    lines += ["", "## 7. 警告、孤立引用与迁移备注", ""]
    notes = list(resolved.get("migration_notes", [])) + list(resolved.get("legacy_notes", []))
    lines.extend([f"- {note}" for note in notes] or ["- 无"])
    return "\n".join(lines).rstrip() + "\n"


def slugify(text: str, fallback: str, used: set[str]) -> str:
    value = text.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    if not value or not value[0].isalpha():
        value = fallback
    value = value[:60].rstrip("-")
    if len(value) < 3:
        value = fallback
    candidate = value
    suffix = 2
    while candidate in used:
        ending = f"-{suffix}"
        candidate = value[: 64 - len(ending)].rstrip("-") + ending
        suffix += 1
    used.add(candidate)
    return candidate


def parse_outline(path: Path) -> tuple[str, list[dict[str, Any]]]:
    text = path.read_text(encoding="utf-8")
    headings = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            headings.append((len(match.group(1)), re.sub(r"\s+#+$", "", match.group(2)).strip()))
    title = next((text for level, text in headings if level == 1), path.stem.replace("_", " ").title())
    content_headings = [(level, text) for level, text in headings if not (level == 1 and text == title)]
    used = {"file-main-report"}
    nodes: list[dict[str, Any]] = [{"id": "file-main-report", "type": "file", "title": "主报告", "order": 10, "output_path": "report/main.md"}]
    stack: list[tuple[int, str]] = [(0, "file-main-report")]
    counters: Counter[int] = Counter()
    for position, (level, heading) in enumerate(content_headings, start=1):
        counters[level] += 1
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_id = stack[-1][1] if stack else "file-main-report"
        prefix = "sec" if level <= 2 else "heading"
        node_id = slugify(f"{prefix}-{heading}", f"{prefix}-{position:03d}", used)
        node = {
            "id": node_id,
            "type": "section" if level <= 2 else "heading",
            "parent_id": parent_id,
            "title": heading,
            "order": counters[level] * 10,
        }
        nodes.append(node)
        stack.append((level, node_id))
    return title, nodes


def initial_plan(outline: Path) -> dict[str, Any]:
    title, nodes = parse_outline(outline)
    return {
        "version": 1,
        "document": {"id": "research-report", "title": title, "purpose": "", "language": "zh-CN", "success_criteria": []},
        "defaults": {"audience": {"profile": "general-research-reader"}, "style": {"profile": "academic"}, "approval": "auto"},
        "workflow": {"review_after_write": True, "auto_fix": "constrained", "fail_on": ["schema_error", "missing_required_content"]},
        "nodes": nodes,
    }


def sync_outline_plan(existing: dict[str, Any], outline: Path) -> dict[str, Any]:
    """Refresh an outline-derived tree while retaining reliably matched stable IDs and local plans."""
    fresh = initial_plan(outline)
    old_nodes = existing.get("nodes", [])
    new_nodes = fresh["nodes"]
    old_groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    new_groups: Counter[tuple[str, str]] = Counter()
    for node in old_nodes:
        if isinstance(node, dict):
            old_groups.setdefault((str(node.get("type")), str(node.get("title"))), []).append(node)
    for node in new_nodes:
        new_groups[(node["type"], node["title"])] += 1
    id_map: dict[str, str] = {}
    matched: dict[str, dict[str, Any]] = {}
    used_ids: set[str] = set()
    for node in new_nodes:
        key = (node["type"], node["title"])
        candidates = old_groups.get(key, [])
        if len(candidates) == 1 and new_groups[key] == 1 and candidates[0]["id"] not in used_ids:
            old = candidates[0]
            id_map[node["id"]] = old["id"]
            matched[node["id"]] = old
            used_ids.add(old["id"])
        else:
            id_map[node["id"]] = node["id"]
    synced_nodes = []
    for node in new_nodes:
        old = matched.get(node["id"])
        synced = copy.deepcopy(old) if old else copy.deepcopy(node)
        synced["id"] = id_map[node["id"]]
        for key in ("type", "title", "order"):
            synced[key] = copy.deepcopy(node[key])
        if node.get("parent_id"):
            synced["parent_id"] = id_map[node["parent_id"]]
        else:
            synced.pop("parent_id", None)
        if not old and "output_path" in node:
            synced["output_path"] = node["output_path"]
        synced_nodes.append(synced)
    result = copy.deepcopy(existing)
    result["version"] = 1
    result.setdefault("document", {})["title"] = fresh["document"]["title"]
    result["nodes"] = synced_nodes
    return result


def ensure_writable_output(path: Path, force: bool) -> None:
    if path.exists() and not force:
        raise PlanInvalid([error("output_exists", str(path), "output already exists; pass --force to replace it")])


def find_outline(root: Path) -> Path | None:
    candidates = [
        root / "PAPER_OUTLINE.md",
        root / "OUTLINE.md",
        root / "paper" / "PAPER_OUTLINE.md",
        root / "templates" / "PAPER_OUTLINE.md",
    ]
    return next((path for path in candidates if path.is_file()), None)


def migrate_plan(root: Path) -> dict[str, Any]:
    defaults = load_yaml(MIGRATION_DEFAULTS_PATH)
    outline = find_outline(root)
    if outline:
        plan = initial_plan(outline)
        plan["migration_notes"] = [f"从现有大纲 {outline.relative_to(root)} 创建节点。"]
    else:
        plan = copy.deepcopy(defaults)
        existing_outputs: list[Path] = []
        for directory in (root / "paper", root / "report"):
            if directory.is_dir():
                existing_outputs.extend(sorted(path for path in directory.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".tex"}))
        nodes = []
        used: set[str] = set()
        for index, path in enumerate(existing_outputs, start=1):
            rel = path.relative_to(root).as_posix()
            node_id = slugify(f"file-{path.stem}", f"file-{index:03d}", used)
            nodes.append({"id": node_id, "type": "file", "title": path.stem.replace("_", " "), "order": index * 10, "output_path": rel})
        if not nodes:
            nodes = [{"id": "file-main-report", "type": "file", "title": "主报告", "order": 10, "output_path": "report/main.md"}]
        plan["nodes"] = nodes
        plan["migration_notes"] = ["未找到现有大纲；根据已有输出文件和迁移默认值创建计划。"]
    if not outline:
        readme = root / "README.md"
        if readme.is_file():
            title_match = re.search(r"(?m)^#\s+(.+?)\s*$", readme.read_text(encoding="utf-8"))
            if title_match:
                plan["document"]["title"] = title_match.group(1).strip()
    legacy_files: list[tuple[str, str]] = []
    for name in ("WRITING.md", "WRITING_INSTRUCTIONS.md", "PAPER_INSTRUCTIONS.md"):
        path = root / name
        if path.is_file():
            legacy_files.append((name, path.read_text(encoding="utf-8")))
    if legacy_files:
        combined = "\n".join(content.lower() for _, content in legacy_files)
        audience_patterns = (
            ("executive-reader", ("executive", "高管", "决策者")),
            ("policy-maker", ("policy", "政策制定")),
            ("domain-researcher", ("researcher", "研究人员", "审稿")),
        )
        style_patterns = (
            ("technical", ("technical", "技术写作", "步骤化")),
            ("executive", ("executive", "结论优先", "决策摘要")),
            ("policy", ("policy", "政策建议")),
            ("popular_science", ("popular science", "科普", "低术语")),
            ("narrative", ("narrative", "叙事")),
            ("academic", ("academic", "学术", "论文")),
        )
        for profile, terms in audience_patterns:
            if any(term in combined for term in terms):
                plan.setdefault("defaults", {}).setdefault("audience", {})["profile"] = profile
                break
        for profile, terms in style_patterns:
            if any(term in combined for term in terms):
                plan.setdefault("defaults", {}).setdefault("style", {})["profile"] = profile
                break
        if re.search(r"[\u3400-\u9fff]", combined):
            plan.setdefault("document", {})["language"] = "zh-CN"
        plan["legacy_notes"] = [f"{name}:\n{content.rstrip()}" for name, content in legacy_files]
    return plan


def extract_node_text(full_text: str, node: dict[str, Any]) -> tuple[str, bool]:
    node_id = node["id"]
    start = re.escape(ANCHOR_PATTERN.format(node_id=node_id, boundary="start"))
    end = re.escape(ANCHOR_PATTERN.format(node_id=node_id, boundary="end"))
    match = re.search(start + r"(.*?)" + end, full_text, flags=re.DOTALL)
    if match:
        return match.group(1).strip(), True
    if node.get("type") == "file":
        return full_text, True
    return "", False


def measure(text: str, unit: str) -> int:
    if unit == "words":
        return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))
    if unit == "chinese_characters":
        return len(re.findall(r"[\u3400-\u9fff]", text))
    if unit == "characters":
        return len(re.sub(r"\s+", "", text))
    if unit == "pages":
        return max(1, round(len(re.findall(r"\S+", text)) / 500)) if text.strip() else 0
    if unit == "items":
        return len(re.findall(r"(?m)^\s*(?:[-*+] |\d+[.)] )", text))
    return len(text)


def add_check(checks: list[dict[str, Any]], category: str, status: str, message: str, auto_fixable: bool = False) -> None:
    checks.append({"category": category, "status": status, "message": message, "auto_fixable": auto_fixable})


def review_node(node: dict[str, Any], text: str, located: bool, node_map: dict[str, dict[str, Any]]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    if not located:
        add_check(checks, "content", "fail", f"missing node anchors for {node['id']}", True)
    objective = node.get("objective", {})
    key_message = objective.get("key_message")
    if key_message and isinstance(key_message, str) and key_message not in text:
        add_check(checks, "objective", "warning", "key message is not stated verbatim; reviewer confirmation required")
    length = node.get("length", {})
    unit = length.get("unit", "characters")
    count = measure(text, unit)
    if length.get("min") is not None and count < length["min"]:
        add_check(checks, "length", "fail", f"length {count} {unit} is below minimum {length['min']}", True)
    if length.get("max") is not None and count > length["max"]:
        add_check(checks, "length", "fail", f"length {count} {unit} exceeds maximum {length['max']}", True)
    content = node.get("content", {})
    for required in content.get("required", []):
        if isinstance(required, str) and required not in text:
            add_check(checks, "missing_required_content", "fail", f"missing required content: {required}", True)
    for excluded in content.get("excluded", []):
        if isinstance(excluded, str) and excluded in text:
            add_check(checks, "content", "fail", f"excluded content is present: {excluded}", True)
    for keyword in content.get("keywords", []):
        if isinstance(keyword, str) and keyword not in text:
            add_check(checks, "content", "warning", f"keyword not found: {keyword}", True)
    for ref in content.get("cross_references", []):
        target = node_map.get(ref, {})
        if ref not in text and target.get("title", "") not in text:
            add_check(checks, "broken_reference", "fail", f"cross-reference is not present in content: {ref}", True)
    style = node.get("style", {})
    for expression in style.get("prohibited_expressions", []):
        if isinstance(expression, str) and expression in text:
            add_check(checks, "style", "fail", f"prohibited expression is present: {expression}", True)
    if style.get("person") == "third" and re.search(r"(?:^|[，。；\s])(我|我们)(?:[，。；\s]|认为|发现|建议)", text):
        add_check(checks, "style", "warning", "first-person wording may conflict with third-person style", True)
    primary = node.get("audience", {}).get("primary", {})
    if primary.get("knowledge_level") == "advanced" and re.search(r"简单来说|小朋友|零基础", text):
        add_check(checks, "audience", "fail", "introductory phrasing conflicts with advanced primary audience", True)
    evidence = node.get("evidence", {})
    citations = re.findall(r"\[[0-9,@][^\]]*\]|\([^)]*(?:19|20)\d{2}[^)]*\)|https?://|doi:", text, flags=re.IGNORECASE)
    if evidence.get("citation_density") == "high" and not citations and text.strip():
        add_check(checks, "evidence", "blocked_missing_evidence", "high citation density requires at least one traceable citation")
    presentation = node.get("presentation", {})
    if node.get("type") != "figure" and presentation.get("figures") and not re.search(r"!\[[^]]*\]\(|<figure|图\s*\d", text, flags=re.IGNORECASE):
        add_check(checks, "presentation", "fail", "required figure is not represented", True)
    if presentation.get("tables") and not re.search(r"(?m)^\s*\|.+\|\s*$|<table|表\s*\d", text, flags=re.IGNORECASE):
        add_check(checks, "presentation", "fail", "required table is not represented", True)
    if presentation.get("formulas") and not re.search(r"\$[^$]+\$|\\\[|\\begin\{equation", text):
        add_check(checks, "presentation", "fail", "required formula is not represented", True)
    if not checks:
        add_check(checks, "all", "pass", "all automated checks passed")
    statuses = {item["status"] for item in checks}
    if "blocked_missing_evidence" in statuses:
        status = "blocked_missing_evidence"
    elif "fail" in statuses:
        status = "fail"
    elif "warning" in statuses:
        status = "warning"
    else:
        status = "pass"
    return {
        "node_id": node["id"],
        "status": status,
        "output_path": node.get("output_path"),
        "anchor": node.get("anchor", node["id"]),
        "measured_length": {"value": count, "unit": unit},
        "checks": checks,
        "allowed_auto_fixes": sorted({item["category"] for item in checks if item.get("auto_fixable")}),
        "resolved_plan_hash": node.get("resolved_plan_hash"),
    }


def refresh_result_status(result: dict[str, Any]) -> None:
    statuses = {item["status"] for item in result.get("checks", [])}
    if "blocked_missing_evidence" in statuses:
        result["status"] = "blocked_missing_evidence"
    elif "fail" in statuses:
        result["status"] = "fail"
    elif "warning" in statuses:
        result["status"] = "warning"
    else:
        result["status"] = "pass"
    result["allowed_auto_fixes"] = sorted({item["category"] for item in result.get("checks", []) if item.get("auto_fixable")})


def figure_file_error(path: Path) -> str | None:
    """Structural checks only: passing does not certify visible scientific content."""
    data = path.read_bytes()
    if not data:
        return "empty figure file"
    suffix = path.suffix.lower()
    if suffix == ".svg":
        try:
            root = ET.fromstring(data)
        except ET.ParseError:
            return "malformed SVG XML"
        if root.tag != "{http://www.w3.org/2000/svg}svg":
            return "invalid SVG root or namespace"
        if not any(e.tag.split("}")[-1] in {"path", "rect", "circle", "ellipse", "line", "polyline", "polygon", "text", "image", "use"} for e in root.iter()):
            return "SVG has no graphical elements"
    elif suffix == ".pptx":
        try:
            with zipfile.ZipFile(path) as archive:
                slides = [n for n in archive.namelist() if re.fullmatch(r"ppt/slides/slide[0-9]+\.xml", n)]
                if not slides:
                    return "PPTX has no slides"
                ns = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
                for slide in slides:
                    tree = ET.fromstring(archive.read(slide))
                    if not tree.findall(".//p:sp", ns) or not tree.findall(".//p:txBody", ns):
                        return "PPTX slide lacks editable shapes or native text"
        except (zipfile.BadZipFile, ET.ParseError, KeyError):
            return "invalid PPTX package"
    elif suffix == ".pdf":
        if not data.startswith(b"%PDF-") or b"%%EOF" not in data[-1024:]:
            return "invalid PDF envelope"
    elif suffix in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}:
        try:
            from PIL import Image
        except ImportError:
            return "raster decoder missing: install Pillow to verify figure"
        try:
            expected = {".png": "PNG", ".jpg": "JPEG", ".jpeg": "JPEG", ".tif": "TIFF", ".tiff": "TIFF"}[suffix]
            with Image.open(path) as im:
                if im.format != expected:
                    return "raster format disagrees with extension"
                im.verify()
            with Image.open(path) as im:
                im.load()
        except (OSError, ValueError, SyntaxError):
            return "corrupt raster figure"
    elif suffix == ".eps":
        if not data.startswith(b"%!PS-Adobe-") or b"BoundingBox:" not in data:
            return "invalid EPS envelope"
    else:
        return "unsupported figure extension"
    return None


def review_figure_specs(result: dict[str, Any], node: dict[str, Any], content_root: Path, venue: dict[str, Any]) -> None:
    presentation = node.get("presentation", {})
    figures = presentation.get("figures", []) if isinstance(presentation, dict) else []
    if not isinstance(figures, list):
        return
    venue_figures = venue.get("requirements", {}).get("figures", {}) if isinstance(venue, dict) else {}
    allowed_formats = set(venue_figures.get("allowed_formats", []))
    caption_limit = venue_figures.get("caption_max_words")
    for figure in figures:
        if not isinstance(figure, dict):
            continue
        figure_id = figure.get("id", "unknown-figure")
        caption = figure.get("caption", "")
        if not caption:
            add_check(result["checks"], "figure", "fail", f"{figure_id}: caption is required", True)
        if not figure.get("alt_text"):
            add_check(result["checks"], "figure", "fail", f"{figure_id}: alt_text is required", True)
        provenance = figure.get("provenance", {})
        if not isinstance(provenance, dict) or not provenance.get("command") or not provenance.get("code_revision"):
            add_check(result["checks"], "figure", "blocked_missing_evidence", f"{figure_id}: command and code_revision provenance are required")
        declared_formats = set(figure.get("formats", []))
        if allowed_formats and declared_formats - allowed_formats:
            add_check(result["checks"], "figure", "fail", f"{figure_id}: formats {sorted(declared_formats - allowed_formats)} are not allowed by venue", True)
        if isinstance(caption_limit, int) and caption and len(re.findall(r"\b[\w'-]+\b", caption)) > caption_limit:
            add_check(result["checks"], "figure", "fail", f"{figure_id}: caption exceeds venue limit of {caption_limit} words", True)
        if venue_figures.get("resolution_dpi") and not figure.get("resolution_dpi"):
            add_check(result["checks"], "figure", "warning", f"{figure_id}: final resolution_dpi is not declared")
        sources = list(figure.get("input_files", []))
        if figure.get("data_source"):
            sources.append(figure["data_source"])
        for source in dict.fromkeys(sources):
            if source.startswith(("http://", "https://")):
                add_check(result["checks"], "figure", "blocked_missing_evidence", f"{figure_id}: archive remote source locally before review: {source}")
                continue
            source_path = safe_content_path(content_root, source)
            if not source_path.is_file() or source_path.stat().st_size == 0:
                add_check(result["checks"], "figure", "blocked_missing_evidence", f"{figure_id}: input missing or empty: {source}")
        if not figure.get("outputs"):
            add_check(result["checks"], "figure", "fail", f"{figure_id}: outputs must be declared")
        for output in figure.get("outputs", []):
            output_path = safe_content_path(content_root, output)
            extension = output_path.suffix.lower().lstrip(".")
            extension = {"jpg": "jpeg", "tif": "tiff"}.get(extension, extension)
            if extension not in declared_formats:
                add_check(result["checks"], "figure", "fail", f"{figure_id}: output extension not in declared formats: {output}")
            if not output_path.is_file():
                add_check(result["checks"], "figure", "fail", f"{figure_id}: output file not found: {output}")
            else:
                problem = figure_file_error(output_path)
                if problem:
                    add_check(result["checks"], "figure", "fail", f"{figure_id}: {problem}: {output}")
                elif extension in {"pdf", "eps"}:
                    add_check(result["checks"], "figure", "warning", f"{figure_id}: envelope checked; full document rendering still requires visual review")
    refresh_result_status(result)


def safe_content_path(root: Path, relative: str) -> Path:
    root_resolved = root.resolve()
    path = (root_resolved / relative).resolve()
    if path != root_resolved and root_resolved not in path.parents:
        raise PlanInvalid([error("unsafe_output_path", relative, "output path escapes content root")])
    return path


def review_plan(resolved: dict[str, Any], content_root: Path) -> dict[str, Any]:
    nodes = resolved.get("nodes", [])
    node_map = {node["id"]: node for node in nodes}
    file_cache: dict[str, str | None] = {}
    results = []
    for node in nodes:
        output_path = node.get("output_path")
        if not output_path:
            result = review_node(node, "", False, node_map)
            review_figure_specs(result, node, content_root, resolved.get("venue", {}))
            results.append(result)
            continue
        if output_path not in file_cache:
            path = safe_content_path(content_root, output_path)
            file_cache[output_path] = path.read_text(encoding="utf-8") if path.is_file() else None
        full_text = file_cache[output_path]
        if full_text is None:
            result = review_node(node, "", False, node_map)
            result["checks"].insert(0, {"category": "content", "status": "fail", "message": f"output file not found: {output_path}", "auto_fixable": False})
            result["status"] = "fail"
        else:
            text, located = extract_node_text(full_text, node)
            result = review_node(node, text, located, node_map)
        review_figure_specs(result, node, content_root, resolved.get("venue", {}))
        results.append(result)
    counts = Counter(result["status"] for result in results)
    overall = "pass"
    if counts["blocked_missing_evidence"]:
        overall = "blocked_missing_evidence"
    elif counts["fail"]:
        overall = "fail"
    elif counts["warning"]:
        overall = "warning"
    return {
        "version": 1,
        "document_id": resolved.get("document", {}).get("id"),
        "resolved_plan_hash": canonical_hash(resolved),
        "overall_status": overall,
        "summary": {key: counts[key] for key in ("pass", "warning", "fail", "blocked_missing_evidence")},
        "nodes": results,
    }


def render_review(report: dict[str, Any]) -> str:
    lines = [
        "# Writing Review",
        "",
        f"- **文档**：`{report.get('document_id', '')}`",
        f"- **总体状态**：`{report['overall_status']}`",
        f"- **Resolved plan hash**：`{report['resolved_plan_hash']}`",
        "",
        "## 汇总",
        "",
    ]
    for status in ("pass", "warning", "fail", "blocked_missing_evidence"):
        lines.append(f"- `{status}`：{report['summary'].get(status, 0)}")
    lines += ["", "## 节点结果", ""]
    for node in report["nodes"]:
        lines += [
            f"### `{node['node_id']}` — {node['status']}",
            "",
            f"- 输出：`{node.get('output_path') or '—'}`",
            f"- 篇幅：{node['measured_length']['value']} {node['measured_length']['unit']}",
            f"- 允许的受限自动修订：{inline(node['allowed_auto_fixes'])}",
        ]
        for check in node["checks"]:
            lines.append(f"- [{check['status']}] **{check['category']}**：{check['message']}")
        lines.append("")
    lines += [
        "## 修订边界",
        "",
        "仅局部重写 fail、warning 或 blocked 节点。受限自动修订仅处理报告明确列出的篇幅、格式、措辞或遗漏说明；核心结论、证据标准、章节结构和已审批目标需回到计划与审批阶段。",
    ]
    return "\n".join(lines).rstrip() + "\n"


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def cmd_validate(args: argparse.Namespace) -> int:
    plan = load_yaml(args.plan)
    errors = validate_plan(plan)
    result = {"valid": not errors, "error_count": len(errors), "errors": errors}
    print_json(result)
    print(f"validate: {'ok' if not errors else 'failed'} ({len(errors)} errors)", file=sys.stderr)
    return EXIT_OK if not errors else EXIT_INVALID


def cmd_resolve(args: argparse.Namespace) -> int:
    resolved = resolve_plan(load_yaml(args.plan))
    write_json(args.output, resolved)
    print(f"resolve: wrote {args.output} ({len(resolved['nodes'])} nodes)", file=sys.stderr)
    return EXIT_OK


def cmd_render(args: argparse.Namespace) -> int:
    resolved = load_json(args.resolved_plan)
    atomic_write(args.output, render_plan(resolved))
    print(f"render: wrote {args.output}", file=sys.stderr)
    return EXIT_OK


def cmd_init(args: argparse.Namespace) -> int:
    existing = load_yaml(args.output) if args.output.exists() and args.force else None
    ensure_writable_output(args.output, args.force)
    plan = sync_outline_plan(existing, args.outline) if existing else initial_plan(args.outline)
    errors = validate_plan(plan)
    if errors:
        raise PlanInvalid(errors)
    write_yaml(args.output, plan)
    print(f"init: wrote {args.output} ({len(plan['nodes'])} nodes)", file=sys.stderr)
    return EXIT_OK


def cmd_migrate(args: argparse.Namespace) -> int:
    ensure_writable_output(args.output, args.force)
    plan = migrate_plan(args.project_root)
    errors = validate_plan(plan)
    if errors:
        raise PlanInvalid(errors)
    write_yaml(args.output, plan)
    print(f"migrate: wrote {args.output} ({len(plan['nodes'])} nodes); existing content unchanged", file=sys.stderr)
    return EXIT_OK


def cmd_review(args: argparse.Namespace) -> int:
    resolved = load_json(args.resolved_plan)
    report = review_plan(resolved, args.content_root)
    write_json(args.json_output, report)
    atomic_write(args.markdown_output, render_review(report))
    print_json(report)
    print(f"review: {report['overall_status']} ({len(report['nodes'])} nodes)", file=sys.stderr)
    return EXIT_OK if report["overall_status"] in {"pass", "warning"} else EXIT_INVALID


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate", help="validate schema and semantic constraints")
    validate.add_argument("plan", type=Path)
    validate.set_defaults(func=cmd_validate)
    resolve = subparsers.add_parser("resolve", help="resolve profiles and inheritance")
    resolve.add_argument("plan", type=Path)
    resolve.add_argument("--output", type=Path, required=True)
    resolve.set_defaults(func=cmd_resolve)
    render = subparsers.add_parser("render", help="render the readable plan")
    render.add_argument("resolved_plan", type=Path)
    render.add_argument("--output", type=Path, required=True)
    render.set_defaults(func=cmd_render)
    init = subparsers.add_parser("init", help="create a plan from a Markdown outline")
    init.add_argument("--outline", type=Path, required=True)
    init.add_argument("--output", type=Path, required=True)
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)
    migrate = subparsers.add_parser("migrate", help="create a plan for an existing project")
    migrate.add_argument("--project-root", type=Path, required=True)
    migrate.add_argument("--output", type=Path, required=True)
    migrate.add_argument("--force", action="store_true")
    migrate.set_defaults(func=cmd_migrate)
    review = subparsers.add_parser("review", help="review written content node by node")
    review.add_argument("resolved_plan", type=Path)
    review.add_argument("--content-root", type=Path, required=True)
    review.add_argument("--json-output", type=Path, required=True)
    review.add_argument("--markdown-output", type=Path, required=True)
    review.set_defaults(func=cmd_review)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except PlanInvalid as exc:
        print_json({"valid": False, "error_count": len(exc.errors), "errors": exc.errors})
        print(f"{args.command}: failed ({len(exc.errors)} errors)", file=sys.stderr)
        return EXIT_INVALID
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print_json({"error": type(exc).__name__, "message": str(exc)})
        print(f"{args.command}: tool error: {exc}", file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
