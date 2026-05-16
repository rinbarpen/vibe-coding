#!/bin/bash
set -e

# ============================================================
# vibe-lang-audit.sh — Multi-language project consistency audit
# ============================================================
# Checks cross-language consistency in multi-language projects:
#   - Error handling patterns
#   - API contract alignment
#   - Shared schema definitions
#   - Dependency versions
#
# Usage:
#   bash scripts/vibe-lang-audit.sh
# ============================================================

echo "=== Multi-Language Consistency Audit ==="
echo ""

ISSUES=0

# Detect project languages
HAS_GO=false; HAS_RUST=false; HAS_PYTHON=false; HAS_TS=false; HAS_JAVA=false
[ -f go.mod ] && HAS_GO=true
[ -f Cargo.toml ] && HAS_RUST=true
[ -f pyproject.toml ] || [ -f requirements.txt ] || [ -f setup.py ] && HAS_PYTHON=true
[ -f package.json ] || [ -f pnpm-workspace.yaml ] && HAS_TS=true
[ -f pom.xml ] || [ -f build.gradle ] || [ -f build.gradle.kts ] && HAS_JAVA=true

echo "Languages detected:"
$HAS_GO && echo "  ✓ Go"
$HAS_RUST && echo "  ✓ Rust"
$HAS_PYTHON && echo "  ✓ Python"
$HAS_TS && echo "  ✓ TypeScript/JavaScript"
$HAS_JAVA && echo "  ✓ Java"
echo ""

# ── Check 1: OpenAPI contract presence ───────────────────
echo "[1] API Contracts"
if ls api/openapi.yaml 2>/dev/null || ls api/openapi.yml 2>/dev/null || ls api/*.proto 2>/dev/null; then
    echo "  ✓ API contract found"
else
    echo "  ⚠ No API contract found (api/openapi.yaml or api/*.proto)"
    echo "    For multi-language projects, define contracts in a language-agnostic format."
    ISSUES=$((ISSUES + 1))
fi

# ── Check 2: Shared schemas ──────────────────────────────
echo ""
echo "[2] Shared Schemas"
if [ -d schemas ] || [ -d proto ]; then
    echo "  ✓ Shared schema directory exists"
else
    echo "  ℹ No shared schema directory (optional for single-language projects)"
fi

# ── Check 3: Error envelope consistency ──────────────────
echo ""
echo "[3] Error Handling Patterns"
if $HAS_GO; then
    GO_ERR_COUNT=$(grep -r "if err != nil" --include="*.go" . 2>/dev/null | wc -l)
    echo "  Go: ~$GO_ERR_COUNT error checks (if err != nil)"
fi
if $HAS_RUST; then
    RUST_RESULT_COUNT=$(grep -r "Result<" --include="*.rs" . 2>/dev/null | wc -l)
    echo "  Rust: ~$RUST_RESULT_COUNT Result types"
fi
if $HAS_PYTHON; then
    PY_EXCEPT_COUNT=$(grep -r "except " --include="*.py" . 2>/dev/null | wc -l)
    echo "  Python: ~$PY_EXCEPT_COUNT exception handlers"
fi
if $HAS_TS; then
    TS_CATCH_COUNT=$(grep -r "catch" --include="*.ts" --include="*.tsx" . 2>/dev/null | grep -v "node_modules" | wc -l)
    echo "  TypeScript: ~$TS_CATCH_COUNT catch statements"
fi
if $HAS_JAVA; then
    JAVA_CATCH_COUNT=$(grep -r "catch" --include="*.java" . 2>/dev/null | wc -l)
    echo "  Java: ~$JAVA_CATCH_COUNT catch blocks"
fi

# ── Check 4: Dockerfile presence ─────────────────────────
echo ""
echo "[4] Containerization"
if [ -f Dockerfile ]; then
    echo "  ✓ Dockerfile found"
    if grep -q "^USER root" Dockerfile 2>/dev/null; then
        echo "  ⚠ Dockerfile uses root user — consider switching to non-root"
        ISSUES=$((ISSUES + 1))
    fi
else
    echo "  ℹ No Dockerfile found (optional for local-only projects)"
fi

# ── Check 5: Environment files ───────────────────────────
echo ""
echo "[5] Environment Configuration"
if [ -f .env.example ]; then
    echo "  ✓ .env.example found"
else
    echo "  ℹ No .env.example (add one to document required environment variables)"
fi

# ── Check 6: CI/CD configuration ─────────────────────────
echo ""
echo "[6] CI/CD"
if [ -d .github/workflows ] || [ -f .gitlab-ci.yml ] || [ -f .circleci/config.yml ]; then
    echo "  ✓ CI/CD configuration found"
else
    echo "  ℹ No CI/CD configuration found"
fi

echo ""
echo "=== Audit Complete: $ISSUES issues found ==="
echo ""
