import json
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "validate_figure.py"


def run_validator(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def test_reports_sufficient_pixels_and_ppi(tmp_path: Path) -> None:
    spec = tmp_path / "spec.json"
    spec.write_text(json.dumps({"width_in": 7, "height_in": 4, "min_ppi": 600}))
    image = tmp_path / "figure.tiff"

    # A 4200x2400 image with 600 PPI metadata meets both dimensions.
    from PIL import Image

    Image.new("RGB", (4200, 2400), "white").save(image, dpi=(600, 600))
    result = run_validator("--spec", str(spec), "--image", str(image))

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "pass"
    assert report["effective_ppi"]["x"] >= 600
    assert report["pixel_requirements"]["width"] == 4200


def test_distinguishes_metadata_only_ppi_from_insufficient_pixels(tmp_path: Path) -> None:
    spec = tmp_path / "spec.json"
    spec.write_text(json.dumps({"width_in": 7, "height_in": 4, "min_ppi": 600}))
    image = tmp_path / "small.tiff"

    from PIL import Image

    Image.new("RGB", (1024, 768), "white").save(image, dpi=(600, 600))
    result = run_validator("--spec", str(spec), "--image", str(image))

    assert result.returncode == 2
    report = json.loads(result.stdout)
    assert report["status"] == "fail"
    assert report["checks"]["pixel_dimensions"] == "fail"
    assert report["checks"]["ppi_metadata"] == "pass"
    assert "metadata_only" in report["failure_reasons"]
