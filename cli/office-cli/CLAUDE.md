# CLAUDE.md (Office CLI)

Manifest for unified office document CLI — manage Word (docx), Excel (xlsx), and PowerPoint (ppt) documents through a single command-line interface. Combines Anthropic official document skills for programmatic office automation.

## Data Safety (CRITICAL)

1. **NEVER modify original files directly.**
2. **ALWAYS copy**: `cp original.docx working.docx` before any modification.
3. **ALWAYS validate** the working copy before replacing the original.
4. **ALWAYS keep a backup**: `mv original.docx _backups/original-{date}.docx`.
5. **EVERY modification on a git branch.**

## Commands

| Command | Description |
|---------|-------------|
| `office-cli docx create <template> <data>` | Create docx from template with data |
| `office-cli docx merge <files...>` | Merge multiple docx files |
| `office-cli docx convert <input> <format>` | Convert docx (md, pdf, latex) |
| `office-cli docx stats <file>` | Report document statistics |
| `office-cli docx validate <file>` | Validate document structure |
| `office-cli xlsx create <data>` | Create xlsx from JSON/CSV data |
| `office-cli xlsx analyze <file>` | Analyze spreadsheet structure |
| `office-cli xlsx chart <file> <config>` | Generate chart in spreadsheet |
| `office-cli xlsx convert <input> <format>` | Convert xlsx format |
| `office-cli ppt create <template> <slides>` | Create pptx from markdown outline |
| `office-cli ppt merge <files...>` | Merge multiple pptx files |
| `office-cli ppt convert <input> <format>` | Convert pptx (pdf, images) |
| `office-cli ppt stats <file>` | Report presentation statistics |
| `office-cli batch <config>` | Run batch office processing from config |

## Architecture

```
<root>/
  inputs/             # Source files for processing
  outputs/            # Generated office files
  templates/          # Office document templates (.dotx, .xltx, .potx)
  scripts/            # Custom office automation scripts
  configs/            # Batch processing configurations
  _backups/           # Timestamped backups of originals
   manifests/          # References to sub-manifests
     docx/             # -> manifests/office/docx
     xlsx/             # -> manifests/office/xlsx
     pptx/             # -> manifests/office/pptx
```

## Key Files

- `skills/anthropics/skills/docx` — Anthropic official docx skill
- `skills/anthropics/skills/xlsx` — Anthropic official xlsx skill
- `skills/anthropics/skills/pptx` — Anthropic official pptx skill
- `manifests/office/docx` — Docx-specific manifest (docx-polar pipeline)
- `manifests/office/xlsx` — Xlsx-specific manifest (uv+python)
- `manifests/office/pptx` — PPT-specific manifest (ppt-master)

## Workflow

1. **Select mode**: docx | xlsx | ppt | batch
2. **Copy**: Create working copy of source file
3. **Transform**: Apply template, merge, convert, or analyze
4. **Validate**: Check structural integrity of output
5. **Backup**: Timestamp original before replacement
6. **Export**: Deliver final files in required formats

## Gotchas

- **python-docx**: Cannot preserve all native Word features (tracked changes, OLE objects).
- **openpyxl**: Large xlsx files (>100MB) consume significant memory.
- **python-pptx**: Images are embedded, not linked; embedding large images inflates file size.
- **Format fidelity**: Round-trip conversions (docx→md→docx) may lose formatting.
- **Dependency**: Requires `skills/anthropics` submodule with docx, xlsx, pptx skills.
