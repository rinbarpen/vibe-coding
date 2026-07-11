#!/usr/bin/env bash
set -euo pipefail

VERSION="1.0.0"

print_usage() {
  cat <<EOF
export-paper-zip v${VERSION}

Export finalized research paper files as a ZIP archive.

Usage:
  $(basename "$0") <path> [options]

Modes:
  submission (default)   Auto-discover and bundle submission-ready files
  bundle                 Pack explicitly listed files/directories

Options:
  --mode <mode>          submission (default) or bundle
  --venue <name>         Target venue name (e.g. ICLR2026, NeurIPS2026)
  --output <dir>         Output directory (default: <path>/../paper-export/)
  --name <name>          Custom ZIP filename (without .zip extension)
  --include <paths...>   Bundle mode: space-separated list of files/dirs to pack
  --dry-run              Preview files, do not create ZIP
  -h, --help             Show this help message

Examples:
  $(basename "$0") /path/to/paper --venue ICLR2026
  $(basename "$0") /path/to/paper --mode bundle --include paper.pdf figures/
  $(basename "$0") /path/to/paper --venue NeurIPS2026 --name camera-ready --dry-run
EOF
  exit 0
}

error() { echo "Error: $*" >&2; exit 1; }
warn()  { echo "Warning: $*" >&2; }
info()  { echo "=> $*"; }

MODE="submission"
VENUE=""
OUTPUT_DIR=""
CUSTOM_NAME=""
INCLUDE_PATHS=()
DRY_RUN=0
PAPER_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) print_usage ;;
    --mode)
      shift
      if [[ "$1" != "submission" && "$1" != "bundle" ]]; then
        error "Invalid mode: $1 (use 'submission' or 'bundle')"
      fi
      MODE="$1"; shift
      ;;
    --venue) shift; VENUE="$1"; shift ;;
    --output) shift; OUTPUT_DIR="$1"; shift ;;
    --name) shift; CUSTOM_NAME="$1"; shift ;;
    --include)
      shift
      INCLUDE_PATHS=()
      while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
        INCLUDE_PATHS+=("$1"); shift
      done
      ;;
    --dry-run) DRY_RUN=1; shift ;;
    -*)
      error "Unknown option: $1"
      ;;
    *)
      if [[ -z "$PAPER_DIR" ]]; then
        PAPER_DIR="$1"; shift
      else
        error "Unexpected argument: $1"
      fi
      ;;
  esac
done

# --- Validation ---
if [[ -z "$PAPER_DIR" ]]; then
  error "Paper directory is required. Usage: $(basename "$0") <path> [options]"
fi

if [[ ! -d "$PAPER_DIR" ]]; then
  error "Directory does not exist: $PAPER_DIR"
fi

PAPER_DIR="$(cd "$PAPER_DIR" && pwd)"

if [[ -z "$OUTPUT_DIR" ]]; then
  OUTPUT_DIR="$(dirname "$PAPER_DIR")/paper-export"
fi
mkdir -p "$OUTPUT_DIR"
OUTPUT_DIR="$(cd "$OUTPUT_DIR" && pwd)"

# --- Generate timestamp ---
TIMESTAMP=$(date +%Y%m%d_%H%M)

# --- Collect files & create ZIP ---

if [[ "$MODE" == "submission" ]]; then
  # --- Submission mode ---
  VENUE_PREFIX="${VENUE:+${VENUE}/}"

  # Collect files
  TEX_FILES=()
  BIB_FILES=()
  CLS_FILES=()
  FIGURE_DIR=""
  SUPP_DIR=""
  PAPER_PDF=""

  while IFS= read -r -d '' f; do
    TEX_FILES+=("$f")
  done < <(find "$PAPER_DIR" -maxdepth 2 -name '*.tex' -type f -print0 2>/dev/null || true)

  while IFS= read -r -d '' f; do
    BIB_FILES+=("$f")
  done < <(find "$PAPER_DIR" -maxdepth 2 -name '*.bib' -type f -print0 2>/dev/null || true)

  while IFS= read -r -d '' f; do
    CLS_FILES+=("$f")
  done < <(find "$PAPER_DIR" -maxdepth 2 \( -name '*.cls' -o -name '*.sty' -o -name '*.bst' -o -name '*.cfg' \) -type f -print0 2>/dev/null || true)

  if [[ -d "$PAPER_DIR/figures" ]]; then
    FIGURE_DIR="$PAPER_DIR/figures"
  fi

  if [[ -d "$PAPER_DIR/supplementary" ]]; then
    SUPP_DIR="$PAPER_DIR/supplementary"
  fi

  if [[ -f "$PAPER_DIR/paper.pdf" ]]; then
    PAPER_PDF="$PAPER_DIR/paper.pdf"
  fi

  # Try to compile if no PDF
  if [[ -z "$PAPER_PDF" && ${#TEX_FILES[@]} -gt 0 ]]; then
    MAIN_TEX=""
    for f in "${TEX_FILES[@]}"; do
      BASENAME="$(basename "$f")"
      if [[ "$BASENAME" == "main.tex" || "$BASENAME" == "paper.tex" || "$BASENAME" == "ms.tex" ]]; then
        MAIN_TEX="$f"
        break
      fi
    done
    if [[ -z "$MAIN_TEX" ]]; then
      MAIN_TEX="${TEX_FILES[0]}"
    fi
    info "No paper.pdf found. Attempting LaTeX compilation: $MAIN_TEX"
    if command -v latexmk &>/dev/null; then
      latexmk -pdf -interaction=nonstopmode -cd "$MAIN_TEX" 2>/dev/null || warn "LaTeX compilation failed (latexmk)"
    elif command -v pdflatex &>/dev/null; then
      cd "$(dirname "$MAIN_TEX")"
      pdflatex -interaction=nonstopmode "$(basename "$MAIN_TEX")" 2>/dev/null || warn "LaTeX compilation failed (pdflatex)"
    else
      warn "No LaTeX compiler found. Skipping compilation."
    fi
    # Re-check for PDF after compilation attempt
    if [[ -f "$PAPER_DIR/paper.pdf" ]]; then
      PAPER_PDF="$PAPER_DIR/paper.pdf"
    fi
  fi

  # Build ZIP in temp dir
  TMPDIR="$(mktemp -d)"
  STAGING="$TMPDIR/${VENUE:+${VENUE}}"
  mkdir -p "$STAGING/src"
  mkdir -p "$STAGING/figures"
  [[ -n "$SUPP_DIR" ]] && mkdir -p "$STAGING/supplementary"

  # Copy files into staging
  if [[ -n "$PAPER_PDF" ]]; then
    cp "$PAPER_PDF" "$STAGING/paper.pdf"
  fi

  for f in "${TEX_FILES[@]}"; do
    cp "$f" "$STAGING/src/"
  done

  for f in "${BIB_FILES[@]}"; do
    cp "$f" "$STAGING/src/"
  done

  for f in "${CLS_FILES[@]}"; do
    cp "$f" "$STAGING/src/"
  done

  if [[ -n "$FIGURE_DIR" ]]; then
    cp -r "$FIGURE_DIR"/* "$STAGING/figures/" 2>/dev/null || true
  fi

  if [[ -n "$SUPP_DIR" ]]; then
    cp -r "$SUPP_DIR"/* "$STAGING/supplementary/" 2>/dev/null || true
  fi

  # Build file list for dry-run or zipping
  FILE_LIST=$(find "$STAGING" -type f | sort)

  if [[ -n "$CUSTOM_NAME" ]]; then
    ZIP_NAME="${CUSTOM_NAME}.zip"
  else
    ZIP_NAME="paper-submission_${VENUE:+${VENUE}_}${TIMESTAMP}.zip"
  fi
  ZIP_PATH="$OUTPUT_DIR/$ZIP_NAME"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    info "Dry-run: files to be included in submission ZIP"
    echo ""
    # Show relative paths
    while IFS= read -r f; do
      rel="${f#$TMPDIR/}"
      echo "  $rel"
    done <<< "$FILE_LIST"
    echo ""
    echo "Would create: $ZIP_PATH"
    rm -rf "$TMPDIR"
    exit 0
  fi

  # Create ZIP preserving relative paths
  (cd "$TMPDIR" && zip -rq "$ZIP_PATH" ./*)

  if [[ ! -f "$ZIP_PATH" ]]; then
    error "Failed to create ZIP archive"
  fi

  ZIP_SIZE=$(du -h "$ZIP_PATH" | cut -f1)
  FILE_COUNT=$(echo "$FILE_LIST" | wc -l)

  echo ""
  info "Submission ZIP created successfully"
  echo "  Path: $ZIP_PATH"
  echo "  Size: $ZIP_SIZE"
  echo "  Files: $FILE_COUNT"
  echo ""
  info "Contents:"
  while IFS= read -r f; do
    rel="${f#$TMPDIR/}"
    echo "  $rel"
  done <<< "$FILE_LIST"

  rm -rf "$TMPDIR"

elif [[ "$MODE" == "bundle" ]]; then
  # --- Bundle mode ---
  if [[ ${#INCLUDE_PATHS[@]} -eq 0 ]]; then
    error "Bundle mode requires --include with at least one path"
  fi

  # Validate include paths
  TMPDIR="$(mktemp -d)"
  for path in "${INCLUDE_PATHS[@]}"; do
    FULL_PATH=""
    if [[ "$path" = /* ]]; then
      FULL_PATH="$path"
    else
      FULL_PATH="$PAPER_DIR/$path"
    fi
    if [[ ! -e "$FULL_PATH" ]]; then
      error "Include path does not exist: $path (resolved: $FULL_PATH)"
    fi
  done

  if [[ -n "$CUSTOM_NAME" ]]; then
    ZIP_NAME="${CUSTOM_NAME}.zip"
  else
    ZIP_NAME="paper-bundle_${TIMESTAMP}.zip"
  fi
  ZIP_PATH="$OUTPUT_DIR/$ZIP_NAME"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    info "Dry-run: files to be included in bundle ZIP"
    echo ""
    for path in "${INCLUDE_PATHS[@]}"; do
      FULL_PATH=""
      if [[ "$path" = /* ]]; then
        FULL_PATH="$path"
      else
        FULL_PATH="$PAPER_DIR/$path"
      fi
      echo "  $FULL_PATH"
    done
    echo ""
    echo "Would create: $ZIP_PATH"
    exit 0
  fi

  # Copy included paths to staging
  for path in "${INCLUDE_PATHS[@]}"; do
    FULL_PATH=""
    if [[ "$path" = /* ]]; then
      FULL_PATH="$path"
    else
      FULL_PATH="$PAPER_DIR/$path"
    fi
    DEST="$TMPDIR/$(basename "$FULL_PATH")"
    if [[ -d "$FULL_PATH" ]]; then
      cp -r "$FULL_PATH" "$DEST"
    else
      cp "$FULL_PATH" "$DEST"
    fi
  done

  (cd "$TMPDIR" && zip -rq "$ZIP_PATH" ./*)

  if [[ ! -f "$ZIP_PATH" ]]; then
    error "Failed to create ZIP archive"
  fi

  ZIP_SIZE=$(du -h "$ZIP_PATH" | cut -f1)

  echo ""
  info "Bundle ZIP created successfully"
  echo "  Path: $ZIP_PATH"
  echo "  Size: $ZIP_SIZE"
  echo "  Contents: ${INCLUDE_PATHS[*]}"

  rm -rf "$TMPDIR"
fi
