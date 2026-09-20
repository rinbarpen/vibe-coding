from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "writing_plan.py"
WRITING = ROOT / "writing"
FIXTURES = Path(__file__).parent / "fixtures"

spec = importlib.util.spec_from_file_location("writing_plan", SCRIPT)
assert spec and spec.loader
wp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wp)


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def minimal_plan() -> dict:
    return load_yaml(WRITING / "writing-plan.minimal.yaml")


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        text=True,
        capture_output=True,
        check=False,
    )


@pytest.mark.parametrize(
    "path",
    [
        WRITING / "writing-plan.minimal.yaml",
        WRITING / "writing-plan.full.yaml",
        WRITING / "migration-defaults.yaml",
    ],
)
def test_examples_and_migration_defaults_validate(path: Path) -> None:
    assert wp.validate_plan(load_yaml(path)) == []


@pytest.mark.parametrize(
    ("fixture", "code"),
    [
        ("invalid-duplicate-id.yaml", "duplicate_id"),
        ("invalid-parent-cycle.yaml", "parent_cycle"),
        ("invalid-profile.yaml", "invalid_profile"),
        ("invalid-unknown-type.yaml", "schema_error"),
        ("invalid-output-conflict.yaml", "output_conflict"),
    ],
)
def test_invalid_fixtures_are_rejected(fixture: str, code: str) -> None:
    errors = wp.validate_plan(load_yaml(FIXTURES / fixture))
    assert code in {item["code"] for item in errors}


def test_missing_parent_and_broken_reference_are_rejected() -> None:
    plan = minimal_plan()
    plan["nodes"][1]["parent_id"] = "file-missing"
    plan["nodes"][1]["content"]["cross_references"] = ["sec-deleted"]
    codes = {item["code"] for item in wp.validate_plan(plan)}
    assert {"missing_parent", "broken_reference"} <= codes


def test_scalar_object_list_append_and_unset_inheritance() -> None:
    plan = minimal_plan()
    plan["defaults"]["style"]["tone"] = "neutral"
    plan["defaults"]["content"] = {
        "keywords": ["base"],
        "optional": ["remove-me"],
    }
    plan["nodes"][0]["style"] = {"tone": "precise", "formality": "medium"}
    plan["nodes"][1]["style"] = {"formality": "high"}
    plan["nodes"][1]["content"]["keywords"] = {"append": ["child"]}
    plan["nodes"][1]["content"]["optional"] = {"unset": True}
    node = {item["id"]: item for item in wp.resolve_plan(plan)["nodes"]}["sec-introduction"]
    assert node["style"]["tone"] == "precise"
    assert node["style"]["formality"] == "high"
    assert node["content"]["keywords"] == ["base", "child"]
    assert "optional" not in node["content"]


def test_multilevel_file_section_heading_figure_resolution() -> None:
    plan = minimal_plan()
    plan["nodes"].extend(
        [
            {"id": "heading-design", "type": "heading", "parent_id": "sec-introduction", "title": "设计", "order": 10},
            {"id": "fig-design", "type": "figure", "parent_id": "heading-design", "title": "流程图", "order": 10},
        ]
    )
    nodes = {item["id"]: item for item in wp.resolve_plan(plan)["nodes"]}
    assert nodes["fig-design"]["output_path"] == "report/main.md"
    assert nodes["fig-design"]["style"]["tone"] == "analytical"


def test_audience_secondary_and_style_overrides_are_resolved() -> None:
    plan = minimal_plan()
    plan["nodes"][1]["audience"] = {
        "profile": "domain-researcher",
        "secondary": [{"profile": "executive-reader", "goal": "decide"}],
    }
    plan["nodes"][1]["style"] = {"profile": "technical", "tone": "cautious"}
    node = wp.resolve_plan(plan)["nodes"][1]
    assert node["audience"]["primary"]["knowledge_level"] == "advanced"
    assert node["audience"]["secondary"][0]["goal"] == "decide"
    assert node["audience"]["secondary"][0]["knowledge_level"] == "overview"
    assert node["style"]["sentence_length"] == "short"
    assert node["style"]["tone"] == "cautious"
    assert "profile" not in json.dumps(node)


def test_venue_profile_and_figure_type_are_materialized() -> None:
    plan = minimal_plan()
    plan["venue"] = {
        "profile": "nature-article-reference",
        "checked_at": "2026-09-19",
        "overrides": {"figures": {"caption_max_words": 250}},
    }
    plan["nodes"].append(
        {
            "id": "fig-results",
            "type": "figure",
            "parent_id": "sec-introduction",
            "title": "结果比较图",
            "order": 20,
            "presentation": {
                "figures": [
                    {
                        "id": "fig-results-main",
                        "type": "comparison",
                        "title": "主结果比较",
                        "renderer": "paper-figure",
                        "data_source": "results/summary.csv",
                        "outputs": ["figures/fig-results-main.pdf"],
                        "formats": ["pdf"],
                        "caption": "不同方法的结果比较。",
                        "alt_text": "不同方法在主要指标上的比较",
                        "provenance": {"command": "python scripts/plot.py", "code_revision": "abc123"},
                    }
                ]
            },
        }
    )
    resolved = wp.resolve_plan(plan)
    node = next(item for item in resolved["nodes"] if item["id"] == "fig-results")
    figure = node["presentation"]["figures"][0]
    assert resolved["venue"]["profile"] == "nature-article-reference"
    assert node["venue"]["requirements"]["figures"]["caption_max_words"] == 250
    assert figure["type_requirements"]["renderer"] == "paper-figure"
    assert figure["generation_defaults"]["require_reproducible_command"] is True


def test_figure_review_checks_outputs_provenance_and_venue(tmp_path: Path) -> None:
    plan = minimal_plan()
    plan["venue"] = {"profile": "nature-article-reference", "checked_at": "2026-09-19"}
    plan["nodes"].append(
        {
            "id": "fig-missing",
            "type": "figure",
            "parent_id": "sec-introduction",
            "title": "缺失输出图",
            "order": 20,
            "presentation": {
                "figures": [
                    {
                        "id": "fig-missing-output",
                        "type": "comparison",
                        "title": "比较",
                        "renderer": "paper-figure",
                        "data_source": "results/summary.csv",
                        "outputs": ["figures/missing.pdf"],
                        "formats": ["pdf"],
                        "caption": "比较结果。",
                        "alt_text": "比较结果",
                        "provenance": {"command": "python plot.py", "code_revision": "abc"},
                    }
                ]
            },
        }
    )
    resolved = wp.resolve_plan(plan)
    report = wp.review_plan(resolved, tmp_path)
    result = next(item for item in report["nodes"] if item["node_id"] == "fig-missing")
    assert result["status"] == "blocked_missing_evidence"
    assert any("output file not found" in item["message"] for item in result["checks"])


def test_identity_survives_title_move_and_reorder() -> None:
    plan = minimal_plan()
    before = wp.resolve_plan(plan)["nodes"][1]
    changed = copy.deepcopy(plan)
    changed["nodes"][1].update({"title": "新标题", "order": 999, "output_path": "moved/report.md"})
    after = wp.resolve_plan(changed)["nodes"][1]
    assert before["id"] == after["id"] == "sec-introduction"
    assert before["resolved_plan_hash"] == after["resolved_plan_hash"]


def test_requirement_change_invalidates_approval() -> None:
    plan = minimal_plan()
    plan["nodes"][1]["approval"] = "before_write"
    first = wp.resolve_plan(plan)["nodes"][1]
    plan["approvals"] = {
        "sec-introduction": {"status": "approved", "resolved_plan_hash": first["resolved_plan_hash"]}
    }
    assert wp.resolve_plan(plan)["nodes"][1]["approval_state"] == "approved"
    plan["nodes"][1]["objective"]["key_message"] = "实质变化"
    assert wp.resolve_plan(plan)["nodes"][1]["approval_state"] == "stale"


def test_only_before_write_nodes_create_gates() -> None:
    plan = minimal_plan()
    plan["nodes"][1]["approval"] = "before_write"
    resolved = wp.resolve_plan(plan)
    assert [gate["node_id"] for gate in resolved["approval_gates"]] == ["sec-introduction"]


def test_resolve_and_render_are_byte_stable(tmp_path: Path) -> None:
    plan = load_yaml(WRITING / "writing-plan.full.yaml")
    first = wp.resolve_plan(plan)
    second = wp.resolve_plan(copy.deepcopy(plan))
    assert json.dumps(first, ensure_ascii=False, sort_keys=True) == json.dumps(second, ensure_ascii=False, sort_keys=True)
    assert wp.render_plan(first) == wp.render_plan(second)
    rendered = wp.render_plan(first)
    assert "由 .auto-research/writing-plan.yaml 生成" in rendered
    assert "相对父节点变化" in rendered


def test_init_from_outline_and_no_overwrite(tmp_path: Path) -> None:
    output = tmp_path / ".auto-research" / "writing-plan.yaml"
    first = run_cli("init", "--outline", str(FIXTURES / "outline.md"), "--output", str(output))
    assert first.returncode == 0, first.stderr
    plan = load_yaml(output)
    ids = [node["id"] for node in plan["nodes"]]
    assert "file-main-report" in ids
    assert len(ids) == len(set(ids)) == 6
    original = output.read_bytes()
    second = run_cli("init", "--outline", str(FIXTURES / "outline.md"), "--output", str(output))
    assert second.returncode == 1
    assert output.read_bytes() == original


def test_init_force_reuses_reliably_matched_ids_and_local_config(tmp_path: Path) -> None:
    outline = tmp_path / "outline.md"
    outline.write_text("# Report\n\n## Methods\n\n## Results\n", encoding="utf-8")
    output = tmp_path / ".auto-research" / "writing-plan.yaml"
    assert run_cli("init", "--outline", str(outline), "--output", str(output)).returncode == 0
    plan = load_yaml(output)
    methods = next(node for node in plan["nodes"] if node["title"] == "Methods")
    methods["id"] = "sec-stable-methods"
    methods["style"] = {"tone": "cautious"}
    for node in plan["nodes"]:
        if node.get("parent_id") == "sec-methods":
            node["parent_id"] = methods["id"]
    wp.write_yaml(output, plan)
    outline.write_text("# Report\n\n## Results\n\n## Methods\n\n## Discussion\n", encoding="utf-8")
    result = run_cli("init", "--outline", str(outline), "--output", str(output), "--force")
    assert result.returncode == 0, result.stderr
    updated = load_yaml(output)
    methods_after = next(node for node in updated["nodes"] if node["title"] == "Methods")
    assert methods_after["id"] == "sec-stable-methods"
    assert methods_after["style"]["tone"] == "cautious"
    assert methods_after["order"] == 20
    assert any(node["title"] == "Discussion" for node in updated["nodes"])


def test_migrate_old_project_preserves_body(tmp_path: Path) -> None:
    paper = tmp_path / "paper"
    paper.mkdir()
    body = paper / "draft.md"
    body.write_text("existing body\n", encoding="utf-8")
    tmp_path.joinpath("README.md").write_text("# Existing Study\n", encoding="utf-8")
    instructions = "Audience: executive decision makers\nStyle: technical\nKeep the legacy constraint.\n"
    tmp_path.joinpath("WRITING_INSTRUCTIONS.md").write_text(instructions, encoding="utf-8")
    output = tmp_path / ".auto-research" / "writing-plan.yaml"
    result = run_cli("migrate", "--project-root", str(tmp_path), "--output", str(output))
    assert result.returncode == 0, result.stderr
    assert body.read_text(encoding="utf-8") == "existing body\n"
    plan = load_yaml(output)
    assert plan["document"]["title"] == "Existing Study"
    assert plan["defaults"]["audience"]["profile"] == "executive-reader"
    assert plan["defaults"]["style"]["profile"] == "technical"
    assert plan["workflow"]["auto_fix"] == "constrained"
    assert instructions.rstrip() in plan["legacy_notes"][0]


def review_fixture_plan() -> dict:
    plan = minimal_plan()
    section = plan["nodes"][1]
    section["length"] = {"min": 40, "max": 300, "target": 100, "unit": "characters"}
    section["content"] = {
        "required": ["方法"],
        "excluded": ["绝对保证"],
        "keywords": ["证据"],
        "cross_references": [],
    }
    section["style"] = {"profile": "academic", "prohibited_expressions": ["显然"]}
    section["audience"] = {"profile": "domain-researcher"}
    section["evidence"] = {"profile": "research-standard"}
    return wp.resolve_plan(plan)


def test_review_detects_length_style_content_evidence_and_audience(tmp_path: Path) -> None:
    resolved = review_fixture_plan()
    report_dir = tmp_path / "report"
    report_dir.mkdir()
    report_dir.joinpath("main.md").write_text(
        "<!-- node:sec-introduction:start -->\n简单来说，显然这是绝对保证。\n<!-- node:sec-introduction:end -->\n",
        encoding="utf-8",
    )
    report = wp.review_plan(resolved, tmp_path)
    node = next(item for item in report["nodes"] if item["node_id"] == "sec-introduction")
    categories = {item["category"] for item in node["checks"]}
    assert {"length", "missing_required_content", "content", "style", "audience", "evidence"} <= categories
    assert node["status"] == "blocked_missing_evidence"
    assert "evidence" not in node["allowed_auto_fixes"]


def test_review_pass_and_outputs_are_stable(tmp_path: Path) -> None:
    plan = minimal_plan()
    section = plan["nodes"][1]
    section["length"] = {"min": 5, "max": 100, "target": 20, "unit": "characters"}
    section["content"] = {"required": ["方法"], "keywords": ["证据"], "cross_references": []}
    section["evidence"] = {"citation_density": "low"}
    resolved = wp.resolve_plan(plan)
    report_dir = tmp_path / "report"
    report_dir.mkdir()
    report_dir.joinpath("main.md").write_text(
        "<!-- node:sec-introduction:start -->\n方法基于证据，结论保持谨慎。\n<!-- node:sec-introduction:end -->\n",
        encoding="utf-8",
    )
    first = wp.review_plan(resolved, tmp_path)
    second = wp.review_plan(resolved, tmp_path)
    node = next(item for item in first["nodes"] if item["node_id"] == "sec-introduction")
    assert node["status"] == "warning"  # key message still requires human confirmation
    assert first == second
    assert wp.render_review(first) == wp.render_review(second)


def test_end_to_end_init_resolve_render_review_and_local_revision(tmp_path: Path) -> None:
    plan_path = tmp_path / ".auto-research" / "writing-plan.yaml"
    resolved_path = tmp_path / ".auto-research" / "resolved-writing-plan.json"
    rendered_path = tmp_path / "WRITING_PLAN.md"
    review_json = tmp_path / ".auto-research" / "writing-review.json"
    review_md = tmp_path / "WRITING_REVIEW.md"
    assert run_cli("init", "--outline", str(FIXTURES / "outline.md"), "--output", str(plan_path)).returncode == 0
    plan = load_yaml(plan_path)
    target_id = plan["nodes"][-1]["id"]
    plan["nodes"][-1]["content"] = {"required": ["背景"]}
    plan["nodes"][-1]["evidence"] = {"citation_density": "low"}
    wp.write_yaml(plan_path, plan)
    assert run_cli("validate", str(plan_path)).returncode == 0
    assert run_cli("resolve", str(plan_path), "--output", str(resolved_path)).returncode == 0
    assert run_cli("render", str(resolved_path), "--output", str(rendered_path)).returncode == 0
    report_dir = tmp_path / "report"
    report_dir.mkdir()
    other_nodes = [node["id"] for node in plan["nodes"] if node["type"] != "file" and node["id"] != target_id]
    other_text = "\n".join(
        f"<!-- node:{node_id}:start -->\n节点内容\n<!-- node:{node_id}:end -->" for node_id in other_nodes
    )
    report_dir.joinpath("main.md").write_text(
        f"<!-- node:{target_id}:start -->\n缺少内容\n<!-- node:{target_id}:end -->\n{other_text}\n",
        encoding="utf-8",
    )
    failed = run_cli(
        "review",
        str(resolved_path),
        "--content-root",
        str(tmp_path),
        "--json-output",
        str(review_json),
        "--markdown-output",
        str(review_md),
    )
    assert failed.returncode == 1
    first_report = json.loads(review_json.read_text(encoding="utf-8"))
    target = next(item for item in first_report["nodes"] if item["node_id"] == target_id)
    assert target["status"] == "fail"
    # Local revision touches the failed node only and preserves the same node ID.
    report_dir.joinpath("main.md").write_text(
        f"<!-- node:{target_id}:start -->\n背景说明完整。\n<!-- node:{target_id}:end -->\n{other_text}\n",
        encoding="utf-8",
    )
    revised = run_cli(
        "review",
        str(resolved_path),
        "--content-root",
        str(tmp_path),
        "--json-output",
        str(review_json),
        "--markdown-output",
        str(review_md),
    )
    assert revised.returncode == 0
    assert target_id in rendered_path.read_text(encoding="utf-8")


def test_all_figure_recipes_and_palette_resolution():
    library = wp.figure_type_pack()['types']
    assert len(library) == 17
    for kind, spec in library.items():
        plan = minimal_plan()
        plan['defaults']['presentation'] = {'figure_style': {'palette': 'earth'}}
        figure = {'id': 'fig-demo', 'type': kind, 'title': kind,
                  'renderer': spec['renderer'], 'data_source': 'data.csv', 'alt_text': 'Example'}
        plan['nodes'][1]['presentation'] = {'figures': [figure]}
        result = wp.resolve_plan(plan)['nodes'][1]['presentation']['figures'][0]
        assert result['resolved_visual']['palette'] == 'earth'
        assert len(result['resolved_visual']['colors']) >= 2
        assert result['type_requirements']['implementation']['procedure']
        assert result['type_requirements']['implementation']['scientific_review']


def test_visual_overrides_and_approval_invalidation():
    plan = minimal_plan()
    plan['defaults']['presentation'] = {'figure_style': {'palette': 'contrast', 'font_size_pt': 10}}
    node = plan['nodes'][1]
    node['approval'] = 'before_write'
    node['presentation'] = {'figures': [{'id': 'fig-demo', 'type': 'comparison', 'title': 'Compare',
        'renderer': 'plot', 'data_source': 'data.csv', 'visual': {'colors': ['#123456', '#ABCDEF']}}]}
    first = wp.resolve_plan(plan)['nodes'][1]
    fig = first['presentation']['figures'][0]
    assert fig['resolved_visual']['colors'] == ['#123456', '#ABCDEF']
    assert fig['resolved_visual']['font_size_pt'] == 10
    plan['approvals'] = {node['id']: {'status': 'approved', 'resolved_plan_hash': first['resolved_plan_hash']}}
    node['presentation']['figures'][0]['visual']['colors'][0] = '#654321'
    assert wp.resolve_plan(plan)['nodes'][1]['approval_state'] == 'stale'
    node['presentation']['figures'][0]['visual']['colors'] = ['red', 'blue']
    assert wp.validate_plan(plan)


def test_unknown_palette_and_duplicate_colors_rejected():
    plan = minimal_plan()
    plan['defaults']['presentation'] = {'figure_style': {'palette': 'unknown'}}
    assert wp.validate_plan(plan)
    plan['defaults']['presentation'] = {'figure_style': {'colors': ['#123456', '#123456']}}
    assert wp.validate_plan(plan)


@pytest.mark.parametrize('kind', list(wp.figure_type_pack()['types']))
def test_each_figure_integrity_gate(kind, tmp_path):
    spec = wp.figure_type_pack()['types'][kind]
    node = {'presentation': {'figures': [{'id':'fig-test','type':kind,'title':'Test','renderer':spec['renderer'],
        'data_source':'data.json','outputs':['test.svg'],'formats':['svg'], 'caption':'Synthetic', 'alt_text':'Synthetic',
        'provenance':{'command':'fixture','code_revision':'fixture'}}]}}
    def review():
        result = {'checks': []}
        wp.review_figure_specs(result,node,tmp_path,{})
        return result
    (tmp_path/'test.svg').write_bytes(b'')
    first = review()
    assert first['status'] == 'blocked_missing_evidence'
    assert any('empty figure file' in x['message'] for x in first['checks'])
    (tmp_path/'data.json').write_text('{"synthetic":true}')
    assert review()['status'] == 'fail'
    (tmp_path/'test.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"><rect width="5" height="5"/></svg>')
    assert review()['status'] == 'pass'
    (tmp_path/'test.svg').write_text('<svg>broken')
    assert review()['status'] == 'fail'
    node['presentation']['figures'][0]['outputs'] = []
    assert review()['status'] == 'fail'


@pytest.mark.parametrize('filename,content', [('test.png',b'not png'),('test.pdf',b'%PDF-1.4'),('test.svg',b'<svg xmlns="http://www.w3.org/2000/svg"/>')])
def test_corrupt_figure_rejected(filename,content,tmp_path):
    p=tmp_path/filename;p.write_bytes(content)
    assert wp.figure_file_error(p)


def test_gpt_dual_delivery_contract():
    types = load_yaml(WRITING / "figure-types.yaml")["types"]
    selected = {"architecture", "flowchart", "pipeline", "algorithm", "concept_illustration"}
    assert {name for name, value in types.items() if value["renderer"] == "gpt-image"} == selected
    for name in selected:
        assert types[name]["editable_renderer"] == "gpt-pptx"
        assert types[name]["outputs"] == ["png", "pptx"]
        assert "native_text" in types[name]["editable_contract"]["required"]


def test_pptx_native_gate(tmp_path):
    import zipfile
    path = tmp_path / "figure.pptx"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("ppt/slides/slide1.xml", '<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:pic/></p:sld>')
    assert "editable" in wp.figure_file_error(path)
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("ppt/slides/slide1.xml", '<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:sp><p:txBody/></p:sp></p:sld>')
    assert wp.figure_file_error(path) is None
    path.write_bytes(b"not a zip")
    assert "invalid" in wp.figure_file_error(path)
