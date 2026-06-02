#!/usr/bin/env python3
"""Submit PDFs to paperreview.ai and retrieve reviews."""

from __future__ import annotations

import argparse
import json
import mimetypes
import sys
import time
import uuid
from pathlib import Path
from typing import Any
from urllib import error, parse, request


BASE_URL = "https://paperreview.ai"
MAX_FILE_SIZE = 10 * 1024 * 1024
DEFAULT_POLL_INTERVAL = 30
DEFAULT_TIMEOUT = 20 * 60


class PaperReviewError(RuntimeError):
    """Raised when the remote service or input validation fails."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Submit a paper to paperreview.ai and fetch the generated review."
    )
    parser.add_argument("pdf_path", nargs="?", help="Path to the PDF to submit.")
    parser.add_argument("--email", help="Email address used for the submission.")
    parser.add_argument("--venue", default="", help="Target venue name.")
    parser.add_argument("--custom-venue", default="", help="Custom venue text when venue is Other.")
    parser.add_argument("--poll", action="store_true", help="Poll until the review is ready.")
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=DEFAULT_POLL_INTERVAL,
        help=f"Seconds between polling attempts. Default: {DEFAULT_POLL_INTERVAL}.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Maximum seconds to wait while polling. Default: {DEFAULT_TIMEOUT}.",
    )
    parser.add_argument("--save-dir", help="Directory for saving submission and review artifacts.")
    parser.add_argument(
        "--token-only",
        action="store_true",
        help="Stop after submission succeeds and return only the token metadata.",
    )
    parser.add_argument("--token", help="Existing token to use instead of creating a new submission.")
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if args.token:
        if args.pdf_path or args.email:
            raise PaperReviewError("--token cannot be combined with pdf_path or --email")
        return

    if not args.pdf_path:
        raise PaperReviewError("pdf_path is required unless --token is provided")
    if not args.email:
        raise PaperReviewError("--email is required unless --token is provided")
    if args.venue == "Other" and not args.custom_venue.strip():
        raise PaperReviewError("--custom-venue is required when --venue Other is used")

    pdf_path = Path(args.pdf_path).expanduser().resolve()
    if not pdf_path.exists():
        raise PaperReviewError(f"PDF not found: {pdf_path}")
    if not pdf_path.is_file():
        raise PaperReviewError(f"PDF path is not a file: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise PaperReviewError(f"Expected a .pdf file: {pdf_path}")
    if pdf_path.stat().st_size > MAX_FILE_SIZE:
        size_mb = pdf_path.stat().st_size / (1024 * 1024)
        raise PaperReviewError(f"PDF exceeds 10 MB limit: {size_mb:.2f} MB")

    if args.poll_interval <= 0:
        raise PaperReviewError("--poll-interval must be positive")
    if args.timeout <= 0:
        raise PaperReviewError("--timeout must be positive")


def json_request(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    return open_json(req)


def open_json(req: request.Request) -> dict[str, Any]:
    try:
        with request.urlopen(req) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data) if data else {}
    except error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")
        detail = extract_error_detail(payload)
        if exc.code == 202:
            raise PendingReview(detail or "Review is still processing")
        raise PaperReviewError(detail or f"HTTP {exc.code} for {req.full_url}") from exc
    except error.URLError as exc:
        raise PaperReviewError(f"Network error contacting {req.full_url}: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise PaperReviewError(f"Invalid JSON response from {req.full_url}") from exc


def form_request(url: str, fields: dict[str, str], files: list[tuple[str, Path, str]] | None = None) -> bytes:
    body, content_type = encode_multipart(fields, files or [])
    req = request.Request(
        url,
        data=body,
        headers={"Content-Type": content_type, "Accept": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req) as resp:
            return resp.read()
    except error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")
        detail = extract_error_detail(payload)
        raise PaperReviewError(detail or f"HTTP {exc.code} for {url}") from exc
    except error.URLError as exc:
        raise PaperReviewError(f"Network error contacting {url}: {exc.reason}") from exc


def encode_multipart(fields: dict[str, str], files: list[tuple[str, Path, str]]) -> tuple[bytes, str]:
    boundary = f"----paperreview-{uuid.uuid4().hex}"
    chunks: list[bytes] = []

    for key, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode(),
                str(value).encode("utf-8"),
                b"\r\n",
            ]
        )

    for field_name, file_path, content_type in files:
        filename = file_path.name
        file_bytes = file_path.read_bytes()
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                (
                    f'Content-Disposition: form-data; name="{field_name}"; '
                    f'filename="{filename}"\r\n'
                ).encode(),
                f"Content-Type: {content_type}\r\n\r\n".encode(),
                file_bytes,
                b"\r\n",
            ]
        )

    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def extract_error_detail(payload: str) -> str:
    if not payload:
        return ""
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return payload.strip()
    if isinstance(data, dict):
        detail = data.get("detail") or data.get("message") or data.get("error")
        if isinstance(detail, str):
            return detail
    return payload.strip()


class PendingReview(PaperReviewError):
    """Raised when the review is not ready yet."""


def get_upload_url(filename: str, venue: str) -> dict[str, Any]:
    return json_request(
        f"{BASE_URL}/api/get-upload-url",
        {"filename": filename, "venue": venue},
    )


def upload_pdf(upload_payload: dict[str, Any], pdf_path: Path) -> None:
    presigned_url = upload_payload.get("presigned_url")
    presigned_fields = upload_payload.get("presigned_fields")
    if not presigned_url or not isinstance(presigned_fields, dict):
        raise PaperReviewError("Upload URL response missing presigned upload fields")

    content_type = mimetypes.guess_type(pdf_path.name)[0] or "application/pdf"
    form_request(
        presigned_url,
        {str(k): str(v) for k, v in presigned_fields.items()},
        [("file", pdf_path, content_type)],
    )


def confirm_upload(s3_key: str, venue: str, email: str) -> dict[str, Any]:
    response_bytes = form_request(
        f"{BASE_URL}/api/confirm-upload",
        {"s3_key": s3_key, "venue": venue, "email": email},
    )
    try:
        return json.loads(response_bytes.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise PaperReviewError("Invalid JSON response from confirm-upload") from exc


def load_review(token: str) -> dict[str, Any]:
    req = request.Request(
        f"{BASE_URL}/api/review/{parse.quote(token)}",
        headers={"Accept": "application/json"},
        method="GET",
    )
    return open_json(req)


def poll_review(token: str, interval: int, timeout: int) -> dict[str, Any]:
    deadline = time.time() + timeout
    while True:
        try:
            review = load_review(token)
            review["_poll_status"] = "ready"
            return review
        except PendingReview as exc:
            if time.time() >= deadline:
                raise PaperReviewError(f"Timed out waiting for review: {exc}") from exc
            time.sleep(interval)


def chosen_venue(args: argparse.Namespace) -> str:
    if args.venue == "Other":
        return args.custom_venue.strip()
    return args.venue.strip()


def ensure_save_dir(path: str | None) -> Path | None:
    if not path:
        return None
    save_dir = Path(path).expanduser().resolve()
    save_dir.mkdir(parents=True, exist_ok=True)
    return save_dir


def save_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def review_to_markdown(review: dict[str, Any]) -> str:
    lines: list[str] = []
    title = review.get("title")
    if title:
        lines.append(f"# {title}")
        lines.append("")

    meta_parts = []
    if review.get("venue"):
        meta_parts.append(f"Venue: {review['venue']}")
    if review.get("submission_date"):
        meta_parts.append(f"Submitted: {review['submission_date']}")
    if review.get("numerical_score") is not None:
        meta_parts.append(f"Score: {review['numerical_score']}/10")
    if meta_parts:
        lines.append(" | ".join(meta_parts))
        lines.append("")

    sections = review.get("sections") or {}
    ordered_sections = [
        ("summary", "Summary"),
        ("strengths", "Strengths"),
        ("weaknesses", "Weaknesses"),
        ("detailed_comments", "Detailed Comments"),
        ("questions", "Questions"),
        ("assessment", "Overall Assessment"),
        ("full_review", "Full Review"),
    ]
    for key, label in ordered_sections:
        content = sections.get(key)
        if content:
            lines.append(f"## {label}")
            lines.append("")
            lines.append(str(content).strip())
            lines.append("")

    if not lines:
        content = review.get("content")
        if content:
            lines.append(str(content).strip())
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def review_summary(review: dict[str, Any]) -> str:
    sections = review.get("sections") or {}
    pieces: list[str] = []
    if review.get("title"):
        pieces.append(f"Title: {review['title']}")
    if review.get("venue"):
        pieces.append(f"Venue: {review['venue']}")
    if review.get("numerical_score") is not None:
        pieces.append(f"Score: {review['numerical_score']}/10")

    for key, label in (
        ("summary", "Summary"),
        ("strengths", "Strengths"),
        ("weaknesses", "Weaknesses"),
        ("assessment", "Assessment"),
    ):
        value = sections.get(key)
        if value:
            pieces.append(f"{label}:\n{str(value).strip()}")

    if not pieces and review.get("content"):
        pieces.append(str(review["content"]).strip())
    return "\n\n".join(pieces).rstrip() + "\n"


def write_artifacts(save_dir: Path, submission: dict[str, Any], review: dict[str, Any] | None) -> dict[str, str]:
    saved: dict[str, str] = {}

    submission_path = save_dir / "submission.json"
    save_json(submission_path, submission)
    saved["submission_json"] = str(submission_path)

    if review is not None:
        review_json_path = save_dir / "review.json"
        review_md_path = save_dir / "review.md"
        summary_md_path = save_dir / "review-summary.md"
        save_json(review_json_path, review)
        review_md_path.write_text(review_to_markdown(review), encoding="utf-8")
        summary_md_path.write_text(review_summary(review), encoding="utf-8")
        saved["review_json"] = str(review_json_path)
        saved["review_md"] = str(review_md_path)
        saved["review_summary_md"] = str(summary_md_path)

    return saved


def build_result(
    token: str,
    status: str,
    message: str,
    review: dict[str, Any] | None = None,
    saved_files: dict[str, str] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {"token": token, "status": status, "message": message}
    if review is not None:
        payload["review"] = review
    if saved_files:
        payload["saved_files"] = saved_files
    return payload


def submit_new_review(args: argparse.Namespace) -> tuple[str, dict[str, Any]]:
    pdf_path = Path(args.pdf_path).expanduser().resolve()
    venue = chosen_venue(args)
    upload_payload = get_upload_url(pdf_path.name, venue)
    if not upload_payload.get("success"):
        raise PaperReviewError("Server did not accept get-upload-url request")
    s3_key = upload_payload.get("s3_key")
    if not s3_key:
        raise PaperReviewError("Upload URL response missing s3_key")

    upload_pdf(upload_payload, pdf_path)
    submission = confirm_upload(str(s3_key), venue, str(args.email))
    if not submission.get("success"):
        raise PaperReviewError(submission.get("message") or "Submission failed")
    token = submission.get("token")
    if not token:
        raise PaperReviewError("Submission succeeded but no token was returned")
    return str(token), submission


def main() -> int:
    args = parse_args()
    try:
        validate_args(args)
        save_dir = ensure_save_dir(args.save_dir)

        if args.token:
            token = args.token.strip()
            submission = {"success": True, "token": token, "source": "existing-token"}
        else:
            token, submission = submit_new_review(args)

        review: dict[str, Any] | None = None
        if args.poll:
            review = poll_review(token, args.poll_interval, args.timeout)

        status = "token_created"
        message = "Submission accepted. Save the token and check again later."
        if args.token:
            status = "token_loaded"
            message = "Using existing token."
        if args.poll and review is not None:
            status = "review_ready"
            message = "Review retrieved successfully."
        elif args.token_only and not args.token:
            status = "token_created"
            message = "Submission accepted and token captured."

        saved_files = write_artifacts(save_dir, submission, review) if save_dir else None
        result = build_result(token, status, message, review=review, saved_files=saved_files)
        json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0
    except PaperReviewError as exc:
        json.dump({"status": "error", "message": str(exc)}, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return 1
    except KeyboardInterrupt:
        json.dump({"status": "error", "message": "Interrupted by user"}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
