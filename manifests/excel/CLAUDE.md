# CLAUDE.md

Manifest for spreadsheet creation, data analysis, and automation using Python (openpyxl) for programmatic workbook manipulation. All operations are Python-only — no direct file mutation.

## Data Safety (CRITICAL)

1. **NEVER modify the original file directly.**
2. **ALWAYS copy**: `cp original.xlsx working.xlsx`
3. **ALWAYS validate** the working copy before replacing the original.
4. **ALWAYS keep a backup**: `mv original.xlsx _backups/original-{date}.xlsx`
5. **ALL excel operations MUST use Python (openpyxl).**
6. **EVERY modification happens on a git branch.**
7. **MERGE only after validation passes.**

## Commands

| Command | Description |
|---------|-------------|
| `git checkout -b excel/<task>` | Create a branch before any file modification |
| `cp original.xlsx working.xlsx` | Create a safe working copy |
| `python -c "from openpyxl import load_workbook; wb = load_workbook('working.xlsx'); ..."` | Modify the working copy via openpyxl |
| `python -c "from openpyxl import load_workbook; wb = load_workbook('working.xlsx'); print(wb.sheetnames)"` | Validate structure integrity |
| `mv original.xlsx _backups/original-$(date +%Y%m%d).xlsx && mv working.xlsx original.xlsx` | Replace original after validation |
| `git add -A && git commit -m "excel: <description>"` | Commit checkpoint |
| `git checkout main && git merge excel/<task>` | Merge only after full validation |
| `vibe-excel-create <name> <columns>` | Create a new workbook with defined columns and sheet structure |
| `vibe-excel-import <file> <format>` | Import data from CSV/JSON into xlsx |
| `vibe-excel-validate <file>` | Validate data types, formulas, sheet structure, and cross-sheet references |
| `vibe-excel-analyze <file>` | Run statistical analysis on workbook data |
| `vibe-excel-pivot <file> <rows> <values>` | Generate pivot table from data range |
| `vibe-excel-chart <file> <type> <range>` | Create chart (bar, line, pie, scatter) from data |
| `vibe-excel-export <file> <format>` | Export to CSV, JSON, or PDF |

## Architecture

```
<root>/
  data/          # Raw and processed data files (CSV, JSON, XLSX)
  workbooks/     # Generated workbook files
  scripts/       # openpyxl automation scripts
  templates/     # Workbook templates with predefined styles and layouts
  reports/       # Analysis reports and chart exports
  schemas/       # Data validation schemas and column definitions
  _backups/      # Timestamped backups of original files before modification
```

## Key Files

- `workbooks/*.xlsx` — Generated workbook output files
- `scripts/analysis.py` — Data analysis automation scripts
- `skills/anthropics/skills/xlsx` — Anthropic official xlsx manipulation skill

## Data Analysis Guidelines

- **Python Only**: Every operation goes through openpyxl. Never open and manually edit a workbook.
- **Clean Data First**: Always validate and clean raw data before analysis.
- **Use Named Ranges**: Define named ranges for data sources in formulas.
- **Formula Consistency**: Ensure formulas use consistent references (absolute vs. relative) across rows.
- **Data Validation**: Apply data validation rules to input cells to prevent corruption.
- **Separate Data from Presentation**: Raw data in one sheet, analysis/charts in separate sheets.

## Workflow

1. **Branch**: `git checkout -b excel/<task>` to isolate changes.
2. **Copy**: `cp original.xlsx working.xlsx` to create a safe working copy.
3. **Modify**: Use openpyxl to modify the working copy programmatically.
4. **Validate**: Open the working copy, verify all sheets, formulas, and data are intact.
5. **Backup**: Move the original to `_backups/` with a timestamp.
6. **Replace**: Move the validated working copy to the original filename.
7. **Commit**: `git add -A && git commit -m "excel: <description>"` to checkpoint.
8. **Merge**: Only after full validation passes, merge back to main.

## Workflow Example

```bash
# Start a task
git checkout -b excel/add-q1-summary-sheet

# Safe copy
cp report.xlsx report_working.xlsx

# Modify via Python
python -c "
from openpyxl import load_workbook
wb = load_workbook('report_working.xlsx')
ws = wb.create_sheet('Q1 Summary')
ws['A1'] = 'Category'
ws['B1'] = 'Revenue'
# ... add data and formulas ...
wb.save('report_working.xlsx')
"

# Validate
python -c "
from openpyxl import load_workbook
wb = load_workbook('report_working.xlsx')
print('Sheets:', wb.sheetnames)  # Verify all sheets present
for name in wb.sheetnames:
    ws = wb[name]
    print(f'  {name}: {ws.max_row} rows x {ws.max_column} cols')
"

# Replace with backup
mv report.xlsx _backups/report-$(date +%Y%m%d-%H%M%S).xlsx
mv report_working.xlsx report.xlsx

# Commit checkpoint
git add -A && git commit -m "excel: add Q1 summary sheet with revenue categories"

# After all validations pass
git checkout main && git merge excel/add-q1-summary-sheet
```

## Gotchas

- **openpyxl Read-Only Mode**: For large workbooks (>100MB), use `load_workbook(read_only=True)` for memory efficiency.
- **Formula Evaluation**: openpyxl writes formulas but does not evaluate them. Formulas are evaluated when opened in Excel or LibreOffice Calc.
- **Date Handling**: Excel dates use a serial number format. Always convert datetime objects using `openpyxl.utils.datetime`.
- **Cell Styles**: Setting a style on a cell overwrites existing styles. Modify individual style properties rather than replacing the full style object.
- **Merged Cells**: Avoid merged cells in data tables; they cause issues with sorting, filtering, and pivot tables.
- **Chart Data Series**: Charts must reference data by range string (e.g., `"Sheet1!A1:A10"`), not by cell values.
- **Performance**: For bulk operations (100k+ rows), use `ws.append()` or `ws.iter_rows()` instead of cell-by-cell writes.
- **Never Skip Validation**: A corrupted working copy that overwrites the original = data loss. Always validate first.
