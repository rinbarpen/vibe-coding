# paperreview.ai Notes

Use this reference when the script or workflow needs to be updated.

## Current flow

- Submit page: `https://paperreview.ai/`
- Review page: `https://paperreview.ai/review`
- Frontend upload flow:
  - `POST /api/get-upload-url`
  - upload PDF to returned presigned S3 URL with returned form fields
  - `POST /api/confirm-upload`
- Frontend review flow:
  - `GET /api/review/{token}`

## Current user-visible constraints

- File type: PDF
- Max size: 10 MB
- Analysis limit: first 15 pages

## Observed response behavior

- Submission success includes a token in the frontend response payload.
- Review lookup may return HTTP `202` when processing is still underway.
- Review payload may include:
  - `title`
  - `venue`
  - `submission_date`
  - `content`
  - `numerical_score`
  - `has_feedback`
  - `sections.summary`
  - `sections.strengths`
  - `sections.weaknesses`
  - `sections.detailed_comments`
  - `sections.questions`
  - `sections.assessment`
  - `sections.full_review`

## Update guidance

- Prefer preserving backward-compatible parsing.
- If the site starts requiring browser state or auth, reevaluate whether the skill should switch from direct HTTP calls to browser automation.
