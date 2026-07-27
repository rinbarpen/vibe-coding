# AGENTS.md (Office CLI)

Instructions for AI agents working on office document automation tasks across Word, Excel, and PowerPoint.

## Repository Overview

Unified office CLI manifest that aggregates docx, xlsx, and pptx capabilities into a single command interface. Uses Anthropic official document skills and python-docx/openpyxl/python-pptx under the hood.

## Iron Rule: Data Safety First

Every file modification follows this mandatory sequence:

1. **Branch**: Create a git branch (`office/<task>`).
2. **Copy**: Work on a copy, never the original.
3. **Validate**: Verify structural integrity after every modification.
4. **Backup**: Timestamp the original before replacing it.
5. **Commit**: Checkpoint after each successful replacement.
6. **Merge**: Only merge after full validation.

## Agent Roles

### 1. Document Engineer
- **Scope**: Word document creation, template processing, format conversion.
- **Skills**: `docx` skill, PreTeXt XML, python-docx.
- **Patterns**: Copy-first safety, style separation, modular authoring.

### 2. Spreadsheet Analyst
- **Scope**: Excel data processing, chart generation, formula application, analysis.
- **Skills**: `xlsx` skill, openpyxl, pandas.
- **Patterns**: Data validation, formula integrity, chart rendering.

### 3. Presentation Designer
- **Scope**: PowerPoint creation, slide layout, template application, batch conversion.
- **Skills**: `pptx` skill, python-pptx.
- **Patterns**: Slide master usage, template inheritance, image optimization.

### 4. Batch Processor
- **Scope**: Multi-file, multi-format batch office automation workflows.
- **Skills**: All office skills, shell scripting.
- **Patterns**: Config-driven processing, parallel execution, error aggregation.

## Subagent Dispatching

| Domain | Tool/Skill | Trigger |
|--------|-----------|---------|
| **Document Authoring** | `office/docx` sub-manifest | Word document creation/modification |
| **Spreadsheet Processing** | `office/xlsx` sub-manifest | Excel data/chart tasks |
| **Presentation Creation** | `office/pptx` sub-manifest | PowerPoint generation |
| **Format Conversion** | `pandoc` | Cross-format conversion |
| **Visual Design** | `canvas-design` skill | Chart/table visual polish |

## Office Processing Standards

- **Source of Truth**: For docx, PreTeXt XML is authoritative; DOCX/PDF/HTML are derived.
- **Template Over Content**: Reuse templates for consistent formatting; avoid ad-hoc styling.
- **Validation Before Replace**: Always run `validate` before `mv working.docx original.docx`.
- **Batch Safety**: Batch operations use dry-run mode first (`--dry-run`).
- **Encoding**: All text files are UTF-8; specify encoding explicitly in scripts.

## Git Branch Workflow

- **Branch naming**: `office/<task>` (e.g., `office/merge-reports`, `office/update-charts`)
- **Commit frequency**: After each successful validate→backup→replace cycle
- **Never work on main**: All modifications start from and merge back to main only after validation

## Maintenance

- Sync CLI commands with upstream Anthropic skill updates.
- Keep template libraries organized and versioned.
- Maintain cross-format conversion compatibility matrix.
