# AGENTS.md

Instructions for AI agents working on spreadsheet creation, data analysis, and automation projects.

## Repository Overview

Spreadsheet automation project using openpyxl for programmatic Excel workbook creation, data analysis, charting, and reporting. All operations are Python-only — never manipulate files directly.

## Iron Rule: Data Safety First

Every file modification follows this mandatory sequence:

1. **Branch**: Create a git branch for the operation.
2. **Copy**: Work on a copy, never the original.
3. **Validate**: Verify structural integrity after every modification.
4. **Backup**: Timestamp the original before replacing it.
5. **Commit**: Checkpoint after each successful replacement.
6. **Merge**: Only merge after full validation.

## Core Flow

1. **Acquire**: Load data from external sources (CSV, databases, APIs) via Python.
2. **Clean**: Validate types, handle missing data, standardize column formats.
3. **Transform**: Add calculated columns, apply lookup tables, normalize structure.
4. **Analyze**: Build pivot tables, apply statistical functions, identify patterns.
5. **Visualize**: Create charts (bar, line, pie, scatter), apply conditional formatting.
6. **Export**: Generate final workbook and supplementary reports.

## Subagent Dispatching

Actively suggest and launch subagents based on task complexity:

- **`data-cleaner`**: Expert in data validation, type coercion, missing value imputation, and outlier detection via openpyxl.
- **`formula-builder`**: Specializes in Excel formula creation (VLOOKUP, INDEX-MATCH, IF, SUMIFS, array formulas) written through openpyxl.
- **`pivot-analyst`**: Designs pivot tables with appropriate row/column/value fields and filtering.
- **`chart-designer`**: Creates charts with proper axis scaling, labels, color schemes, and data-to-ink ratio.
- **`workbook-architect`**: Structures multi-sheet workbooks with navigational consistency and documentation.

## Data Standards

- **Raw Data Immutable**: Keep original data on a dedicated "Raw" sheet; never modify in place. Always work on copies.
- **Naming Conventions**: Column headers in Title Case, no spaces (use underscores). Named ranges follow `tbl_DatasetName` convention.
- **Type Consistency**: Each column should have a uniform data type. Mixed-type columns must be split or documented.
- **Missing Data**: Represent as empty cells (not "N/A" or 0). Document handling strategy.
- **Documentation Sheet**: Every workbook should include a "README" sheet documenting data sources, definitions, and assumptions.

## Formula Standards

- Prefer `INDEX-MATCH` over `VLOOKUP` for lookup operations (more flexible, faster).
- Use `IFERROR` or `IFNA` to handle expected error cases gracefully.
- Document complex formulas with adjacent comment cells or named ranges.
- Avoid volatile functions (INDIRECT, OFFSET, TODAY, RAND) in large workbooks.
- Range references should be absolute (`$A$1:$A$100`) in formula templates; relative for repeated calculations.

## Git Branch Workflow

- **Branch naming**: `excel/<task-description>` (e.g., `excel/add-revenue-pivot`, `excel/fix-formula-q2`)
- **Commit frequency**: After each successful validate→backup→replace cycle
- **Rollback**: `git checkout main && git branch -D excel/<task>` to abandon; `git revert <commit>` to undo one step
- **Never work on main**: All modifications start from and merge back to main only after validation

## Maintenance

- Keep `CLAUDE.md` updated with new commands and gotchas.
- When adding new analysis patterns, document them in the relevant skill files.
- Periodically audit `_backups/` and prune old backups.
