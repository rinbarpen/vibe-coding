from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
OMNIDRAW = (REPO_ROOT / "mine" / "omnidraw" / "SKILL.md").read_text(encoding="utf-8")
ROUTING = (
    REPO_ROOT / "mine" / "omnidraw" / "references" / "routing-matrix.md"
).read_text(encoding="utf-8")
GITMODULES = (REPO_ROOT / ".gitmodules").read_text(encoding="utf-8")


def test_ccfa_skills_is_the_registered_upstream() -> None:
    assert GITMODULES.count('[submodule "skills/CCFA-Skills"]') == 1
    assert "https://github.com/mikubaka88/CCFA-Skills" in GITMODULES
    assert (REPO_ROOT / "skills" / "CCFA-Skills" / "ccf-visual-composer" / "SKILL.md").is_file()


def test_omnidraw_routes_publication_visuals_to_ccf_visual_composer() -> None:
    assert "../../skills/CCFA-Skills/ccf-visual-composer/SKILL.md" in OMNIDRAW
    assert "../../../skills/CCFA-Skills/ccf-visual-composer/SKILL.md" in ROUTING


def test_happy_figure_skill_is_fully_replaced() -> None:
    assert not (REPO_ROOT / "mine" / "omnidraw" / "research-figure-generation").exists()
    combined = (OMNIDRAW + "\n" + ROUTING).lower()
    assert "happy figure" not in combined
    assert "research-figure-generation" not in combined
