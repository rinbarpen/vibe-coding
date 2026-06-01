#!/usr/bin/env python3
"""Analyze test results for flakiness patterns."""
import sys
import json
from pathlib import Path


FLAKY_PATTERNS = {
    "timeout": {"keywords": ["timeout", "Timed out"], "fix": "Use locator actions instead of sleep/waitForTimeout"},
    "stale_element": {"keywords": ["stale", "detached from DOM"], "fix": "Re-query element before interaction"},
    "network": {"keywords": ["net::ERR_CONNECTION", "ECONNREFUSED"], "fix": "Mock the network endpoint or add retry"},
    "selector_not_found": {"keywords": ["strict mode violation", "multiple elements"], "fix": "Use more specific selector (role/label/testid)"},
    "ordering": {"keywords": ["Cannot find", "has already finished"], "fix": "Ensure test isolation — no shared state"},
}


def analyze_results(results_path: Path) -> dict:
    if not results_path.exists():
        return {"error": "Results file not found"}

    try:
        data = json.loads(results_path.read_text())
    except (json.JSONDecodeError, Exception):
        return {"error": "Unable to parse results file. Check format (expected JSON)."}

    findings = {pattern: {"count": 0, "fix": info["fix"]} for pattern, info in FLAKY_PATTERNS.items()}

    def scan(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str):
                    for pattern, info in FLAKY_PATTERNS.items():
                        if any(kw in value for kw in info["keywords"]):
                            findings[pattern]["count"] += 1
                else:
                    scan(value)
        elif isinstance(obj, list):
            for item in obj:
                scan(item)

    scan(data)
    return findings


if __name__ == "__main__":
    default_paths = [
        Path("test-results.json"),
        Path("playwright-report/results.json"),
        Path("test-results/.last-run.json"),
    ]

    target = None
    for arg in sys.argv[1:]:
        if arg.startswith("--file="):
            target = Path(arg.split("=", 1)[1])

    if not target:
        for p in default_paths:
            if p.exists():
                target = p
                break

    if not target:
        print("[diagnose-flaky] No test results found. Run tests first or specify --file=<path>")
        sys.exit(1)

    findings = analyze_results(target)
    if "error" in findings:
        print(f"[diagnose-flaky] {findings['error']}")
        sys.exit(1)

    total_flaky = sum(f["count"] for f in findings.values())
    print(f"[diagnose-flaky] Analyzed: {target}")
    print(f"[diagnose-flaky] Flaky patterns found: {total_flaky}")
    print()
    for pattern, info in findings.items():
        if info["count"] > 0:
            print(f"  ⚠  {pattern}: {info['count']} occurrence(s)")
            print(f"     Fix: {info['fix']}")
