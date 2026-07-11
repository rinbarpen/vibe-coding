# Paper Version Lifecycle

## Overview

The Paper Version Manager (PVM) tracks revisions of a research paper during the writing and review process in the auto-research pipeline. It uses a simple major.minor versioning scheme.

## Version Scheme

```
v1        — Initial draft after aris/paper-write
  v1.1    — Review Round 1 fixes applied
  v1.2    — Review Round 2 fixes applied
  v1.3    — Review Round 3 fixes applied
v2        — Major rewrite (new experiments, restructured sections)
  v2.1    — Post-major-rewrite polish / review fixes
  v2.2    — Further minor edits
v3        — Another major revision
  ...
```

## Major vs Minor Classification

| Change Type | Bump | Examples |
|-------------|------|----------|
| Major structural change | `--major` | Adding/removing sections, rewriting methodology, new contributions/experiments, changing the core argument |
| Minor refinement | `--minor` | Applying review feedback, figure updates, formatting/bibliography fixes, polishing language, addressing reviewer questions |

## Lifecycle in auto-research Pipeline

```
Phase 3: Review
  aris/paper-write
    → pvm-init.sh           (v1)
  aris/auto-review-loop Round 1
    → apply fixes
    → pvm-bump.sh --minor   (v1.1)
  aris/auto-review-loop Round 2
    → apply fixes
    → pvm-bump.sh --minor   (v1.2)
  aris/paper-claim-audit + citation-audit
    → fix issues
    → pvm-bump.sh --minor   (v1.3)
  aris/auto-paper-improvement-loop
    → deep fixes (may be major)
    → pvm-bump.sh --major   (v2)

Phase 4: Polish
  aris/figure-spec + paper-illustration
    → integrate figures
    → pvm-bump.sh --minor   (v2.1)
  aris/paper-compile
    → final compilation fixes
    → pvm-bump.sh --minor   (v2.2)

Phase 5: Export
  mine/export-paper-zip     (no version bump — final artifact)
```

## Directory Structure

```
paper/
├── paper.tex          ← Active (working) version
├── figures/
├── refs.bib
├── MANIFEST.md
└── .versions/
    ├── VERSION        ← Current version string, e.g. "v1.2"
    ├── CHANGELOG.md   ← Historical changelog
    ├── v1/
    ├── v1.1/
    ├── v1.2/
    └── v2/
```

## MANIFEST.md Integration

Each version bump appends a row:

```
| 2026-07-11 14:30 | paper-version-manager init | .versions/v1/ | version | Initial draft |
| 2026-07-11 16:00 | paper-version-manager bump --minor | .versions/v1.1/ | version | Round 1 review fixes |
| 2026-07-12 09:00 | paper-version-manager bump --major | .versions/v2/ | version | Major rewrite — added ablation |
```

## Best Practices

1. Always init before any editing — version tracking is append-only.
2. Bump `--minor` after every targeted fix batch (e.g., each review round).
3. Bump `--major` when the paper's structure or core claims change significantly.
4. Write descriptive changelog messages so the version history is readable by reviewers.
5. Use `pvm-list.sh` to track progress across sessions.
6. Use `pvm-diff.sh` to verify what actually changed between versions.
7. Rollback is a safety net — prefer bumping forward rather than overwriting history.
