# AGENTS.md (Anything CLI)

Instructions for AI agents using CLI-Anything to generate and manage agent-native CLI interfaces for any software.

## Repository Overview

CLI-Anything (HKUDS/CLI-Anything, 41K+ stars) transforms any software codebase into an AI agent-controllable CLI interface through a fully automated 7-phase pipeline. Generated CLIs are Click-based, support REPL mode, JSON output, and include auto-generated SKILL.md files for agent discovery.

## Agent Roles

### 1. CLI Generator
- **Responsibility**: Run `/cli-anything <path-or-url>` to generate a CLI harness.
- **Input**: Software source code (local path or GitHub URL).
- **Output**: Complete Click-based CLI package with tests, docs, and SKILL.md.
- **Flow**: Run all 7 phases automatically; the pipeline handles everything.

### 2. CLI Refiner
- **Responsibility**: Expand coverage of an existing CLI harness.
- **Input**: Existing harness directory + focus area (e.g., "batch processing").
- **Output**: Updated harness with expanded command coverage and tests.
- **Flow**: Run `/cli-anything:refine [focus]` to analyze gaps and add commands.

### 3. CLI Validator
- **Responsibility**: Validate harness quality against HARNESS.md standards.
- **Input**: Harness directory.
- **Output**: Validation report with pass/fail per standard.
- **Flow**: Run `/cli-anything:validate <path>` for automated validation.

## Subagent Dispatching

| Domain | Tool/Skill | Trigger |
|--------|-----------|---------|
| **CLI-Hub Management** | `cli-hub` command | Installing/searching pre-built CLIs |
| **Harness Generation** | `/cli-anything` command | Generating CLI for new software |
| **Quality Validation** | `/cli-anything:validate` | Checking harness standards compliance |
| **Agent Skill Integration** | SKILL.md in generated CLI | Making generated CLI agent-discoverable |

## Core Principles

- **Agent-native by default**: Every generated CLI has `--json` for machine consumption, `--help` for discovery, and `which` for PATH detection.
- **Zero fragile automation**: No screenshots, no pixel-clicking, no RPA — pure CLI reliability.
- **Namespace isolation**: Generated CLIs use `cli_anything.*` namespace packages, allowing multiple CLIs to coexist without conflicts.
- **Self-documenting**: Each CLI auto-generates SKILL.md for agent discovery.
- **Test-proven**: Generated harnesses include unit, integration, E2E, and workflow tests.

## CLI-Hub Usage

```bash
# Install CLI-Hub
pip install cli-anything-hub

# Search for a CLI in the registry
cli-hub search blender

# Install a CLI
cli-hub install blender

# List installed CLIs
cli-hub list
```

## Git Branch Workflow

- **Branch naming**: `cli-anything/<software-name>` (e.g., `cli-anything/blender`, `cli-anything/gimp`)
- **Commit checkpoints**: After generation, after refinement, after validation
- **Generated code**: CLI harness output is committable but should be in a dedicated directory

## Maintenance

- Keep CLI-Hub registry updated: `cli-hub update`
- Re-validate harnesses after upstream software API changes
- Track upstream CLI-Anything releases for pipeline improvements
