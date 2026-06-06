# /release

Execute the enterprise release workflow.

## Usage

```
/release <version> [options]
```

### Version Format

SemVer 2.0: `MAJOR.MINOR.PATCH`

```
/release major        # Bump major version (breaking changes)
/release minor        # Bump minor version (new features)
/release patch        # Bump patch version (bug fixes)
/release 1.2.3        # Specific version
```

### Options

| Option | Description |
|--------|-------------|
| `--pre=<label>` | Pre-release label (alpha, beta, rc) |
| `--notes=<file>` | Release notes file |
| `--dry-run` | Preview release without executing |

## Workflow

1. **Verify Pre-Release Checklist**
   - [ ] All quality gates passed
   - [ ] CHANGELOG.md updated with new version entry
   - [ ] README.md reflects current state

2. **Create Release Branch** (if not already on one)
   ```bash
   git checkout -b release/v1.2.3
   ```

3. **Bump Version**
   - Update version in package files (package.json, pyproject.toml, Cargo.toml, go.mod, etc.)
   - Commit: `chore: bump version to 1.2.3`

4. **Create GPG-Signed Tag**
   ```bash
   git tag -s v1.2.3 -m "Release v1.2.3"
   ```

5. **Push Tag**
   ```bash
   git push origin v1.2.3
   ```

6. **Verify Release**
   - `release.yml` workflow triggers automatically
   - Monitor: `gh run watch`
   - Verify release appears: `gh release view v1.2.3`

## Merge Strategy

| Branch | Merge Method | Target |
|--------|-------------|--------|
| Feature → main | Squash merge | Clean history |
| Release → main | Merge commit | Preserve release record |
| Hotfix → main | Merge commit | Preserve fix record |

## Post-Release

- [ ] Verify deployment health
- [ ] Update project board
- [ ] Notify stakeholders
- [ ] Close related milestone/issues

## References

- `references/release-process.md` — detailed release process
- `references/tag-convention.md` — tag naming and GPG signing
- `references/branching-strategy.md` — branch strategy decision guide
