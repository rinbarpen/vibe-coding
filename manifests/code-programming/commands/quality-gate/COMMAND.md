# /quality-gate

Execute all 5 quality gates before committing.

## Gates

### 1. Lint Gate
- Go: `golangci-lint run`
- Rust: `cargo clippy -- -D warnings`
- Python: `ruff check`
- TypeScript: `eslint && tsc --noEmit`
- Java: `mvn checkstyle:check` or `gradle checkstyleMain`
- **Exit**: Zero warnings

### 2. Test Gate
- Run full test suite with coverage
- **Exit**: All tests pass, coverage >= 80%

### 3. Security Gate
- Dispatch `security-reviewer` agent for changed files
- Check for: hardcoded secrets, injection vulnerabilities, auth bypasses
- **Exit**: No CRITICAL or HIGH security issues

### 4. Review Gate
- Dispatch language-appropriate reviewer agent:
  - Go: `go-reviewer`
  - Rust: `rust-reviewer`
  - Python: `python-reviewer`
  - TypeScript: `typescript-reviewer`
  - Java: `java-reviewer`
- **Exit**: Reviewer approved, no CRITICAL or HIGH issues

### 5. Doc Gate
- Verify CLAUDE.md reflects current architecture
- Verify README.md is current
- **Exit**: Documentation is accurate

## Manual Checklist

Before calling `/quality-gate`, confirm:
- [ ] No uncommitted debug code
- [ ] No commented-out code
- [ ] No hardcoded URLs or IPs
- [ ] Error handling covers failure paths
- [ ] Inputs are validated at system boundaries
