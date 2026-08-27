from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
TEMPLATES = (SKILL_ROOT / "references" / "prompt-templates.md").read_text(encoding="utf-8")
OMNIDRAW = (SKILL_ROOT.parent / "SKILL.md").read_text(encoding="utf-8")


def test_skill_declares_all_seven_figure_types() -> None:
    for figure_type in (
        "technical route",
        "experimental setup",
        "mechanism",
        "multi-panel comparison",
        "graphical abstract",
        "presentation overview",
        "cover",
    ):
        assert figure_type in SKILL.lower()


def test_prompt_contract_has_scientific_boundaries_and_local_edits() -> None:
    for section in ("scientific boundaries", "render prompt", "local edit commands"):
        assert section in SKILL.lower()
    for heading in (
        "Technical route",
        "Experimental setup",
        "Mechanism",
        "Multi-panel comparison",
        "Graphical abstract",
        "Presentation overview",
        "Journal cover",
    ):
        assert heading in TEMPLATES


def test_omnidraw_routes_research_figures_to_new_skill() -> None:
    assert "research-figure-generation/SKILL.md" in OMNIDRAW
    assert "≥600 PPI TIFF" in OMNIDRAW
