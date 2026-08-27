import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "render_method_figure.py"


def test_renders_deterministic_editable_svg(tmp_path: Path) -> None:
    spec = tmp_path / "method.json"
    out = tmp_path / "method.svg"
    spec.write_text(
        json.dumps(
            {
                "title": "Method Overview",
                "stages": [
                    {"id": "input", "title": "Input", "items": ["Samples", "Metadata"]},
                    {"id": "encoder", "title": "Encoder", "items": ["Backbone", "Projection"]},
                    {"id": "output", "title": "Output", "items": ["Prediction"]},
                ],
                "edges": [
                    {"from": "input", "to": "encoder", "label": "features"},
                    {"from": "encoder", "to": "output", "label": "embedding"},
                ],
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--spec", str(spec), "--output", str(out)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert out.exists()
    svg = out.read_text(encoding="utf-8")
    ET.fromstring(svg)
    for text in ("Method Overview", "Input", "Encoder", "Output", "features", "embedding"):
        assert text in svg
    assert "linearGradient" not in svg
    assert "filter=" not in svg


def test_rejects_edge_to_unknown_stage(tmp_path: Path) -> None:
    spec = tmp_path / "broken.json"
    out = tmp_path / "broken.svg"
    spec.write_text(
        json.dumps(
            {
                "stages": [{"id": "input", "title": "Input"}],
                "edges": [{"from": "input", "to": "missing"}],
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--spec", str(spec), "--output", str(out)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "unknown stage" in result.stderr.lower()
    assert not out.exists()
