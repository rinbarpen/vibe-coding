# paper-review skill

## Source and ownership

The Auto-Research manifest consumes the upstream skill as the root repository
submodule `skills/paper-review`:

- Source: `https://github.com/jam-cc/paper-review.skill.git`
- Skill entrypoint: `skills/paper-review/SKILL.md`
- Current upstream baseline: `2413acb23934a325ef9b653968d1da0aaa26d779`
- License: MIT (per the upstream repository)

The upstream checkout is the source of truth. Do not fork, flatten, or duplicate
its `references/` and `examples/` directories in this manifest.

## Lifecycle integration

Use `paper-review` after the Writing Plan has produced a reviewable draft and
before or alongside `aris/auto-review-loop`:

1. Identify whether the request is a full review, self-review, focused critique,
   or revision of an existing review.
2. Read the full paper, including tables, figures, supplement, and bibliography,
   before making claims about evidence or novelty.
3. Build a frontier map from primary sources and record search scope, dates,
   comparison conditions, and unresolved coverage.
4. Bind every material concern to a claim, location, observed evidence, and
   implication; check baseline fairness and ablation isolation.
5. Produce the requested venue/language format, then prune and verify references.
6. Save review outputs under the research project's `outputs/` directory and
   append the result to `MANIFEST.md`.

## Fetch, update, and rollback

From the repository root:

```bash
git submodule update --init -- skills/paper-review
vibe update
git -C skills/paper-review log -1 --oneline
```

Inspect local changes before updating. To return to the manifest's pinned
submodule revision after an update, use the revision recorded by the parent
repository and run:

```bash
git -C skills/paper-review checkout <PARENT_RECORDED_SHA>
```

The installed skill must keep `SKILL.md` directly under
`skills/paper-review/`; its relative `references/` links depend on that layout.
