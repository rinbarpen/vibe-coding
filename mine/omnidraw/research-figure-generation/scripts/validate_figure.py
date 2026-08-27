#!/usr/bin/env python3
"""Validate a raster figure against physical size and PPI requirements.

The check intentionally separates embedded PPI metadata from effective pixel
coverage. A file can claim 600 PPI while still being too small for its final
print size; that case is reported as metadata_only.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - exercised by CLI environments
    raise SystemExit("Pillow is required: python -m pip install Pillow") from exc


def _positive_number(value: Any, name: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a positive number") from exc
    if not math.isfinite(number) or number <= 0:
        raise ValueError(f"{name} must be a positive number")
    return number


def load_spec(path: Path) -> dict[str, float]:
    data = json.loads(path.read_text(encoding="utf-8"))
    width = _positive_number(data.get("width_in"), "width_in")
    height = _positive_number(data.get("height_in"), "height_in")
    min_ppi = _positive_number(data.get("min_ppi", 600), "min_ppi")
    return {"width_in": width, "height_in": height, "min_ppi": min_ppi}


def _ppi(value: Any) -> float:
    """Convert Pillow's pixels-per-metre value to pixels per inch."""
    if isinstance(value, tuple):
        value = value[0]
    if value is None:
        return 0.0
    # Pillow reports TIFF/PNG density as pixels per inch, but some formats
    # expose pixels per metre. Values above 10,000 are unambiguously metric.
    number = float(value)
    return number * 0.0254 if number > 10_000 else number


def validate(spec_path: Path, image_path: Path) -> dict[str, Any]:
    spec = load_spec(spec_path)
    with Image.open(image_path) as image:
        width_px, height_px = image.size
        dpi = image.info.get("dpi", (0.0, 0.0))
        if not isinstance(dpi, tuple):
            dpi = (dpi, dpi)
        ppi_x, ppi_y = _ppi(dpi[0]), _ppi(dpi[1])

    required_width = math.ceil(spec["width_in"] * spec["min_ppi"])
    required_height = math.ceil(spec["height_in"] * spec["min_ppi"])
    dimensions_pass = width_px >= required_width and height_px >= required_height
    metadata_pass = ppi_x >= spec["min_ppi"] and ppi_y >= spec["min_ppi"]
    effective_x = width_px / spec["width_in"]
    effective_y = height_px / spec["height_in"]
    reasons: list[str] = []
    if not dimensions_pass:
        reasons.append("pixel_dimensions")
        if metadata_pass:
            reasons.append("metadata_only")
    if not metadata_pass:
        reasons.append("ppi_metadata")

    return {
        "status": "pass" if dimensions_pass and metadata_pass else "fail",
        "image": str(image_path),
        "spec": str(spec_path),
        "target": spec,
        "actual_pixels": {"width": width_px, "height": height_px},
        "pixel_requirements": {"width": required_width, "height": required_height},
        "effective_ppi": {"x": round(effective_x, 3), "y": round(effective_y, 3)},
        "embedded_ppi": {"x": round(ppi_x, 3), "y": round(ppi_y, 3)},
        "checks": {
            "pixel_dimensions": "pass" if dimensions_pass else "fail",
            "ppi_metadata": "pass" if metadata_pass else "fail",
        },
        "failure_reasons": reasons,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path, help="JSON with width_in, height_in, min_ppi")
    parser.add_argument("--image", required=True, type=Path, help="PNG, TIFF, or JPEG figure")
    args = parser.parse_args(argv)
    try:
        report = validate(args.spec, args.image)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 2


if __name__ == "__main__":
    sys.exit(main())
