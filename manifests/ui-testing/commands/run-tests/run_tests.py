#!/usr/bin/env python3
"""Run tests with auto-detection of the testing framework."""
import sys
import os
import subprocess
from pathlib import Path


def detect_framework(project_root: Path) -> str | None:
    configs = {
        "playwright.config": "playwright",
        "vitest.config": "vitest",
        "cypress.config": "cypress",
        "jest.config": "jest",
    }
    for pattern, framework in configs.items():
        for ext in [".ts", ".js", ".mjs", ".mts", ".cjs", ".cts"]:
            if (project_root / f"{pattern}{ext}").exists():
                return framework
    return None


def detect_package_manager(project_root: Path) -> str:
    lock_files = {
        "pnpm-lock.yaml": "pnpm",
        "package-lock.json": "npm",
        "yarn.lock": "yarn",
        "bun.lockb": "bun",
    }
    for lock, manager in lock_files.items():
        if (project_root / lock).exists():
            return manager
    return "npm"


def run_tests(framework: str, package_manager: str, args: list[str]) -> int:
    commands = {
        "playwright": ["npx", "playwright", "test"],
        "vitest": ["npx", "vitest", "run"],
        "cypress": ["npx", "cypress", "run"],
        "jest": ["npx", "jest"],
    }
    cmd = commands.get(framework, ["npx", "vitest", "run"]) + args
    print(f"[run-tests] Detected framework: {framework}")
    print(f"[run-tests] Package manager: {package_manager}")
    print(f"[run-tests] Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=project_root)
    return result.returncode


if __name__ == "__main__":
    project_root = Path.cwd()
    framework = detect_framework(project_root)
    if not framework:
        print("[run-tests] No test framework detected. Defaulting to vitest.")
        framework = "vitest"
    pm = detect_package_manager(project_root)
    sys.exit(run_tests(framework, pm, sys.argv[1:]))
