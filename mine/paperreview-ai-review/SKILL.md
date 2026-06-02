---
name: paperreview-ai-review
description: "Submit a local research-paper PDF to paperreview.ai, capture the returned review token, poll until the AI review is ready, and summarize or save the review artifacts. Use when Codex needs to upload a paper to paperreview.ai, check review status, retrieve a review by token, extract strengths and weaknesses, or save the raw and structured review output."
---

# PaperReview AI Review

## Overview

Use this skill to interact with `paperreview.ai` through its HTTP workflow instead of manual browser steps. Prefer the bundled script for submission, token capture, polling, and artifact export.

## Workflow

1. Collect `pdf_path` and `email`.
2. Optionally collect a target venue such as `ICLR` or `NeurIPS`.
3. Run `scripts/paperreview_submit.py` instead of reimplementing the upload flow.
4. Surface the returned token immediately.
5. If the user wants the finished review now, enable polling and wait until the review is ready.
6. Return the review summary plus paths to saved raw artifacts when `--save-dir` is used.

## Quick Start

Run the script directly:

```bash
python3 mine/paperreview-ai-review/scripts/paperreview_submit.py /path/to/paper.pdf \
  --email you@example.com \
  --venue ICLR \
  --poll \
  --save-dir /tmp/paperreview-output
```

Token-only mode:

```bash
python3 mine/paperreview-ai-review/scripts/paperreview_submit.py /path/to/paper.pdf \
  --email you@example.com \
  --token-only
```

Review lookup by existing token:

```bash
python3 mine/paperreview-ai-review/scripts/paperreview_submit.py \
  --token existing-token \
  --poll \
  --save-dir /tmp/paperreview-output
```

## Operating Rules

- Prefer the script over browser automation unless the site changes and the HTTP flow breaks.
- Ask for `pdf_path` and `email` when the user wants a new submission and has not provided them.
- Accept `--venue Other --custom-venue ...` for custom venues.
- Treat HTTP `202` from the review endpoint as pending work, not failure.
- Tell the user that the site states a `10 MB` max file size and only the first `15 pages` are analyzed.
- Warn before upload if the paper is confidential, because this sends the PDF to an external service.
- Preserve raw output. Do not invent missing sections if the service returns only a free-form review.

## Output Contract

The script prints JSON to stdout with these top-level keys when available:

- `token`
- `status`
- `message`
- `review`
- `saved_files`

When a review is ready, summarize these fields if present:

- `title`
- `venue`
- `submission_date`
- `numerical_score`
- `sections.summary`
- `sections.strengths`
- `sections.weaknesses`
- `sections.detailed_comments`
- `sections.questions`
- `sections.assessment`
- `sections.full_review`

## Resources

### `scripts/paperreview_submit.py`

Use for submission, token capture, polling, and artifact export.

### `references/paperreview-ai.md`

Read when you need the current endpoint flow or expected response shape.
