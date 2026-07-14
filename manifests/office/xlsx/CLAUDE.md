# xlsx — uv+python Spreadsheet Engineering

Excel workbook automation via the fastest and most stable Python libraries, all run through `uv`.

## Library Selection

| Operation | Library | Why |
|-----------|---------|-----|
| **Create** new xlsx with formatting | `xlsxwriter` | 2.4x faster than openpyxl; best formatting |
| **Edit** existing xlsx (formulas/styles) | `openpyxl` | Only library supporting read+write with formula preservation |
| **Analyze** spreadsheets | `pandas` + `openpyxl` engine | Most stable data analysis pipeline |
| **Recalculate** formulas | `LibreOffice --headless` | Only reliable formula recalculation |

## Dependencies

```bash
uv add xlsxwriter openpyxl pandas
```

## Commands

| Command | Library | Description |
|---------|---------|-------------|
| `uv run xlsx/scripts/create.py <data.json> <output.xlsx>` | xlsxwriter | Create xlsx from JSON with formatting |
| `uv run xlsx/scripts/analyze.py <input.xlsx>` | pandas+openpyxl | Analyze spreadsheet structure and data |
| `bash xlsx/scripts/recalc.sh <output.xlsx>` | LibreOffice | Recalculate all formulas |
| `office-cli xlsx chart <file> <config>` | openpyxl | Generate chart in spreadsheet |

## Workflow

1. **Select tool** — pandas (data) vs openpyxl (formulas/formatting) vs xlsxwriter (create)
2. **Create/Load** — `Workbook()` or `load_workbook('existing.xlsx')`
3. **Modify** — Add data, formulas, and formatting
4. **Save** — `wb.save('output.xlsx')`
5. **Recalculate** — `bash xlsx/scripts/recalc.sh output.xlsx [timeout_seconds]`
6. **Verify** — Check output for `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?` — fix and recalculate again until zero errors

## Financial Model Color Coding

| Color | Meaning |
|-------|---------|
| Blue | Input cells (hardcoded assumptions) |
| Black | Formula cells (calculations) |
| Green | Same-workbook cross-references |
| Red | External links |
| Yellow | Assumption annotations |

## CRITICAL Gotchas

- **ALWAYS use formulas, never hardcoded values** — spreadsheets must be dynamic
- **NEVER save a workbook opened with `data_only=True`** — formulas are permanently replaced with values
- **MUST recalculate after creation** — openpyxl writes formulas as strings, not calculated values
- **Pandas rows 0-indexed, Excel rows 1-indexed** — row 5 in DataFrame = row 6 in Excel
- **Formula verification**: test on 2-3 cells first → verify all dependencies exist → test edge cases (division by zero, NaN)
- **Cross-sheet references**: format must be `Sheet1!A1`
- **Check denominators** before using `/` in formulas (prevents `#DIV/0!`)
