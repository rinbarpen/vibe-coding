#!/usr/bin/env python3
"""Render an editable conference-style method/flow figure from JSON to SVG."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any


PALETTE = (
    ("#EAF1FB", "#3568A8"),
    ("#E8F5F2", "#23837A"),
    ("#FFF1E5", "#C56828"),
    ("#F1EDFA", "#7256A5"),
    ("#EEF1F4", "#596673"),
)


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def load_spec(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    stages = data.get("stages")
    if not isinstance(stages, list) or not stages:
        raise ValueError("stages must be a non-empty list")

    seen: set[str] = set()
    for stage in stages:
        if not isinstance(stage, dict):
            raise ValueError("each stage must be an object")
        stage_id = str(stage.get("id", "")).strip()
        title = str(stage.get("title", "")).strip()
        if not stage_id or not title:
            raise ValueError("each stage requires id and title")
        if stage_id in seen:
            raise ValueError(f"duplicate stage id: {stage_id}")
        seen.add(stage_id)
        items = stage.get("items", [])
        if not isinstance(items, list) or len(items) > 5:
            raise ValueError(f"stage {stage_id} items must be a list with at most 5 entries")

    edges = data.get("edges", [])
    if not isinstance(edges, list):
        raise ValueError("edges must be a list")
    for edge in edges:
        if not isinstance(edge, dict):
            raise ValueError("each edge must be an object")
        for endpoint in ("from", "to"):
            stage_id = str(edge.get(endpoint, ""))
            if stage_id not in seen:
                raise ValueError(f"edge references unknown stage: {stage_id}")
    return data


def render_svg(spec: dict[str, Any]) -> str:
    stages: list[dict[str, Any]] = spec["stages"]
    edges: list[dict[str, Any]] = spec.get("edges", [])
    title = str(spec.get("title", "Method Overview"))
    gap = 96
    box_w, box_h = 190, 210
    width = max(960, 140 + len(stages) * box_w + (len(stages) - 1) * gap)
    height = 390
    total = len(stages) * box_w + (len(stages) - 1) * gap
    start_x = (width - total) / 2
    y = 105
    positions: dict[str, tuple[float, float]] = {}
    for index, stage in enumerate(stages):
        positions[str(stage["id"])] = (start_x + index * (box_w + gap), y)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
        "<metadata>Deterministic editable method figure; flat vector styling.</metadata>",
        "<defs>",
        '<marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="strokeWidth">',
        '<path d="M0,0 L8,4 L0,8 Z" fill="#39434D"/>',
        "</marker>",
        "</defs>",
        '<rect width="100%" height="100%" fill="#FFFFFF"/>',
        f'<text x="{width / 2:.1f}" y="43" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="21" font-weight="700" fill="#1F2933">{esc(title)}</text>',
        '<line x1="70" y1="65" x2="{}" y2="65" stroke="#D7DDE3" stroke-width="1"/>'.format(width - 70),
    ]

    # Draw connections first so stage shapes remain visually dominant.
    for edge in edges:
        sx, sy = positions[str(edge["from"])]
        tx, ty = positions[str(edge["to"])]
        x1, x2 = sx + box_w + 3, tx - 9
        cy = sy + box_h / 2
        if x2 > x1:
            path = f"M{x1:.1f},{cy:.1f} L{x2:.1f},{cy:.1f}"
            label_x, label_y = (x1 + x2) / 2, cy - 11
        else:
            lower = sy + box_h + 36
            path = f"M{x1:.1f},{cy:.1f} C{x1 + 30:.1f},{lower:.1f} {x2 - 30:.1f},{lower:.1f} {x2:.1f},{ty + box_h / 2:.1f}"
            label_x, label_y = (x1 + x2) / 2, lower - 7
        parts.append(f'<path d="{path}" fill="none" stroke="#39434D" stroke-width="1.8" marker-end="url(#arrow)"/>')
        label = str(edge.get("label", "")).strip()
        if label:
            label_w = max(42, len(label) * 6.7 + 10)
            parts.append(f'<rect x="{label_x - label_w / 2:.1f}" y="{label_y - 13:.1f}" width="{label_w:.1f}" height="17" fill="#FFFFFF"/>')
            parts.append(f'<text x="{label_x:.1f}" y="{label_y:.1f}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#4B5563">{esc(label)}</text>')

    for index, stage in enumerate(stages):
        x, sy = positions[str(stage["id"])]
        fill, accent = PALETTE[index % len(PALETTE)]
        parts.extend(
            [
                f'<g id="stage-{esc(stage["id"])}">',
                f'<rect x="{x:.1f}" y="{sy:.1f}" width="{box_w}" height="{box_h}" rx="4" fill="#FFFFFF" stroke="#65717D" stroke-width="1.4"/>',
                f'<rect x="{x:.1f}" y="{sy:.1f}" width="{box_w}" height="40" rx="4" fill="{fill}"/>',
                f'<path d="M{x:.1f},{sy + 34:.1f} H{x + box_w:.1f} V{sy + 40:.1f} H{x:.1f} Z" fill="{fill}"/>',
                f'<line x1="{x:.1f}" y1="{sy + 40:.1f}" x2="{x + box_w:.1f}" y2="{sy + 40:.1f}" stroke="{accent}" stroke-width="1.4"/>',
                f'<text x="{x + box_w / 2:.1f}" y="{sy + 26:.1f}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="15" font-weight="700" fill="#1F2933">{esc(stage["title"])}</text>',
            ]
        )
        items = [str(item) for item in stage.get("items", [])]
        if items:
            item_h = 36
            block_h = len(items) * item_h + (len(items) - 1) * 10
            item_y = sy + 40 + (box_h - 40 - block_h) / 2
            for item in items:
                parts.extend(
                    [
                        f'<rect x="{x + 22:.1f}" y="{item_y:.1f}" width="{box_w - 44}" height="{item_h}" rx="4" fill="{fill}" stroke="{accent}" stroke-width="1"/>',
                        f'<text x="{x + box_w / 2:.1f}" y="{item_y + 23:.1f}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#26323C">{esc(item)}</text>',
                    ]
                )
                item_y += item_h + 10
        parts.append("</g>")

    caption = str(spec.get("caption", "")).strip()
    if caption:
        parts.append(f'<text x="{width / 2:.1f}" y="360" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="12" fill="#59636E">{esc(caption)}</text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path, help="Method figure JSON specification")
    parser.add_argument("--output", required=True, type=Path, help="Destination .svg path")
    args = parser.parse_args(argv)
    try:
        spec = load_spec(args.spec)
        svg = render_svg(spec)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(svg, encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
