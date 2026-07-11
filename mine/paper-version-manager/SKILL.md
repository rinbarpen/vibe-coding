---
name: paper-version-manager
description: "Track paper revisions with a major.minor versioning scheme (v1, v1.1, v2, etc.). Initialize version tracking after first draft, bump versions after each review round or major rewrite, list history, diff between versions, and rollback. Use in the auto-research Phase 3 (Review) paper-writing workflow to maintain traceable revision history across multiple writing rounds."
---

# Paper Version Manager (PVM)

## Overview

Snapshot-based version management for research paper writing. Each time you bump a version, the current state of the paper directory is copied to `.versions/` with a changelog entry.

**Version scheme:**

| Version | Meaning |
|---------|---------|
| v1 | Initial draft (after `aris/paper-write`) |
| v1.1 | Minor edits – review round 1 fixes, polish, formatting |
| v1.2 | Minor edits – review round 2 fixes, figure updates |
| v2 | Major rewrite – restructuring, new methodology, significant changes |
| v2.1 | Minor edits on v2 base |
| ... | ... |

## Quick Start

```bash
# Phase 3 — after aris/paper-write produces paper/
bash mine/paper-version-manager/scripts/pvm-init.sh /path/to/paper \
  "Initial draft — complete paper with experiments"

# After applying review round 1 fixes (minor bump)
bash mine/paper-version-manager/scripts/pvm-bump.sh --minor /path/to/paper \
  "Round 1 review fixes — clarified method section, fixed Figure 3"

# After major restructuring (major bump)
bash mine/paper-version-manager/scripts/pvm-bump.sh --major /path/to/paper \
  "Major rewrite — reorganized experiments, added ablation study"

# List all versions
bash mine/paper-version-manager/scripts/pvm-list.sh /path/to/paper

# Diff between two versions
bash mine/paper-version-manager/scripts/pvm-diff.sh /path/to/paper \
  --from v1 --to v1.1

# Rollback to a previous version
bash mine/paper-version-manager/scripts/pvm-rollback.sh /path/to/paper v1
```

## Commands

| Command | Description |
|---------|-------------|
| `pvm-init.sh <paper-dir> "message"` | Initialize version tracking, snapshot as v1 |
| `pvm-bump.sh --minor <paper-dir> "message"` | Minor version bump (v1 → v1.1) |
| `pvm-bump.sh --major <paper-dir> "message"` | Major version bump (v1 → v2, resets minor) |
| `pvm-list.sh <paper-dir>` | List all versions with timestamps and changelog |
| `pvm-diff.sh <paper-dir> --from vX --to vY` | Show file diff between two versions |
| `pvm-rollback.sh <paper-dir> <version>` | Restore paper files from a saved version |

## Operating Rules

- Always call `pvm-init.sh` first — it creates the `.versions/` directory and VERSION tracker.
- Use `--minor` for small, targeted edits (review feedback fixes, formatting, figure replacement).
- Use `--major` for significant rewrites (restructuring sections, new contributions, methodology changes).
- Always provide a changelog message describing what changed.
- The active paper files in `<paper-dir>` are considered the "working latest" — version bumps snapshot them.
- Rollback overwrites the working files with the selected version's snapshot.
- All snapshots are plain file copies inside `.versions/` — no git dependency required.
- Record each bump in MANIFEST.md with stage=`version`.

## Integration with auto-research

Insert into Phase 3 (Review) workflow:

```
aris/paper-write → mine/paper-version-manager init  (v1)
    ↓
aris/auto-review-loop (Round 1)
    → apply fixes
    → mine/paper-version-manager bump --minor  (v1.1)
aris/auto-review-loop (Round 2)
    → apply fixes
    → mine/paper-version-manager bump --minor  (v1.2)
    ...
aris/auto-paper-improvement-loop
    → apply deep fixes
    → mine/paper-version-manager bump --major  (v2)
aris/paper-compile
    → mine/paper-version-manager bump --minor  (v2.1) — final polish
```
