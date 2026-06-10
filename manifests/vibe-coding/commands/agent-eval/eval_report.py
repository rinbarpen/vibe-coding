#!/usr/bin/env python3
"""Generate agent eval report from JSON/YAML results.

Loads eval results from data/eval/results.json or results.yaml,
compares against baseline thresholds, and generates a markdown report.

Usage:
  python eval_report.py [--input results.json] [--output docs/eval/report.md]
"""

import json
import sys
from datetime import datetime
from pathlib import Path

THRESHOLDS = {
    "task_success_rate": (85.0, 70.0),  # (target, alert)
    "tool_call_success_rate": (90.0, 80.0),
    "avg_latency_sec": (5.0, 10.0),
    "avg_tokens_per_run": (10000, 50000),
    "avg_cost_per_run": (0.05, 0.20),
}


def load_results(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def generate_report(results: dict, output: Path) -> str:
    lines = [
        f"# Agent Eval Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Summary",
        "",
    ]

    all_pass = True
    alerts = []

    for metric, (target, alert) in THRESHOLDS.items():
        value = results.get(metric, "N/A")
        if isinstance(value, (int, float)):
            status = "PASS" if value >= target else ("ALERT" if value < alert else "WARN")
            if status != "PASS":
                all_pass = False
            if status == "ALERT":
                alerts.append(metric)
            lines.append(f"| {metric} | {value:.2f} | {target} | {status} |")
        else:
            lines.append(f"| {metric} | {value} | {target} | N/A |")

    lines.insert(5, "| Metric | Value | Target | Status |")
    lines.insert(6, "|--------|-------|--------|--------|")

    lines.append("")
    if all_pass:
        lines.append("**Result: ALL METRICS PASS**")
    else:
        lines.append(f"**Result: {len(alerts)} alert(s) — {', '.join(alerts)}**")

    lines.append("")
    lines.append("## Per-Case Results")
    lines.append("")
    for case in results.get("cases", []):
        name = case.get("name", "unknown")
        passed = case.get("passed", False)
        lines.append(f"- [{'PASS' if passed else 'FAIL'}] {name}")

    report = "\n".join(lines)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report)
    return report


if __name__ == "__main__":
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/eval/results.json")
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("docs/eval/report.md")

    results = load_results(input_path)
    report = generate_report(results, output_path)
    print(report)
    print(f"\nReport saved to: {output_path}")
