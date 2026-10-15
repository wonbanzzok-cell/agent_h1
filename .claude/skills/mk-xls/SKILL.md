---
name: mk-xls
description: Build or edit Excel (.xlsx) workbooks in this project with openpyxl. Use this skill whenever the user asks for a spreadsheet, an Excel file, a data table to download, or 엑셀 / 스프레드시트 / 표 정리, wants research figures or report data turned into a workbook, or wants to read, change, or check an existing .xlsx file in this project, even if they do not say "openpyxl".
---

# mk-xls

Make and edit `.xlsx` files for this project by writing a Python build script that uses openpyxl, running it, and checking the result by reading the file back.

## Environment

- Python 3.13 and openpyxl 3.1.5 are installed globally for this user.
- `python` may not be on PATH in an older shell. If `python --version` fails, use the full path:
  - PowerShell: `& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"`
  - Bash: `"$LOCALAPPDATA/Programs/Python/Python313/python.exe"`
- The Windows console code page garbles Korean in `print()` output (the file itself is fine). Set `PYTHONIOENCODING=utf-8` when running scripts whose output you need to read.
- Run Python with `-B` so importing the helpers does not leave `__pycache__/` in the skill folder.
- Helper functions live in `.claude/skills/mk-xls/scripts/xlsx_helpers.py`. Import them by adding that folder to `sys.path` (see the template below) instead of copying code into each build script.

## Where files go

| What | Where | Name |
|------|-------|------|
| Build script | `scripts/` | `build_<topic>_xlsx.py` (English, snake_case) |
| Output workbook | `sheets/` | Korean title, e.g. `AI_투자_현황.xlsx` |

- Never overwrite an existing workbook. To change one, edit its build script and save under a new name (add a date such as `_2026-10-15`, or let `next_available_path()` add `_2`, `_3`, ...), then tell the user the new name. Move older workbooks to `archive/sheets/` only when the user agrees.
- Sheet names, headers, and labels are Korean unless the user asks otherwise.
- When the data comes from a research note in `research/`, keep the figures as they appear there. Put the source and the "indicative" mark for secondary-source figures in a `출처` column or a notes sheet, because a workbook gets copied around without the note.

## Workflow

1. **Plan the workbook.** Write the sheet list (sheet name, columns, rough row count, formulas, charts) and include it in the todo list you report to the user, so they approve the structure before you build.
2. **Write the build script** in `scripts/` from the template below. One function per sheet keeps it easy to edit later.
3. **Run it** and fix any errors.
4. **Verify by reading the workbook back** with openpyxl: sheet names, header row, row count, a few values, number formats, tables, and that every formula is in place (`list_formulas`). Report what you checked. Formula results cannot be checked here (see Limits), and you cannot see the rendered sheet, so say so and suggest the user open the file in Excel.

## Build script template

```python
"""Build sheets/<workbook>.xlsx. Run: python -B scripts/build_<topic>_xlsx.py"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "mk-xls" / "scripts"))

from openpyxl import Workbook
from xlsx_helpers import write_table, autofit_columns, apply_font, next_available_path

OUT = next_available_path(ROOT / "sheets" / "<통합문서_이름>.xlsx")

def build_summary(wb):
    ws = wb.active
    ws.title = "요약"
    headers = ["항목", "금액", "비율"]
    rows = [["가", 1200, 0.4], ["나", 1800, 0.6]]
    write_table(ws, headers, rows, number_formats={"금액": "#,##0", "비율": "0.0%"},
                as_table="SummaryTable")
    ws["A5"], ws["B5"] = "합계", "=SUM(B2:B3)"

def main():
    wb = Workbook()
    build_summary(wb)
    apply_font(wb)                    # after all cells are written
    for ws in wb.worksheets:
        autofit_columns(ws)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    print(f"saved {OUT}")

if __name__ == "__main__":
    main()
```

## Helpers (`scripts/xlsx_helpers.py`)

| Function | Why it exists |
|----------|---------------|
| `write_table(ws, headers, rows, start_row=1, start_col=1, number_formats=None, header_fill="1F4E79", as_table=None, freeze=True, borders=True)` | Styled header, data, borders, per-column number formats, frozen header, and either an Excel table (`as_table="Name"`) or a plain auto-filter. Returns the range, e.g. `"A1:C4"`. |
| `add_excel_table(ws, ref, name, style="TableStyleMedium2")` | Excel table over an existing range. Header cells must be unique strings; the name must be unique in the workbook and contain no spaces. |
| `autofit_columns(ws, min_width=8, max_width=60)` | openpyxl has no auto-fit. Estimates widths, counting Korean characters as 2. |
| `apply_font(wb, name="맑은 고딕")` | Sets the font on every non-empty cell, keeping size, bold, and color. Call it after writing data. |
| `list_formulas(ws)` | Lists `(coordinate, formula)` so you can verify formulas, which openpyxl never calculates. |
| `next_available_path(path)` | Returns a free file name so existing outputs are never overwritten. |

Do not put a sheet auto-filter and an Excel table on the same range. Excel then reports the file as damaged, which is why `write_table` applies only one of them.

## What openpyxl can do

Read `references/openpyxl-api.md` for code snippets when a sheet needs one of these:

- Workbook: new/open/save, templates, properties, defined names, workbook protection
- Sheets: create/copy/delete/rename/reorder, chart sheets, tab color, hide, freeze panes, zoom, gridlines, sheet protection
- Cells: values (numbers, text, dates, booleans), `append`, iterate ranges, insert/delete rows and columns, move ranges, merge, widths/heights, hide/group
- Formulas: formula strings, array formulas, reading cached results with `data_only=True`
- Styles: font, fill, border, alignment, number formats, cell protection, named styles
- Conditional formatting: cell/formula rules, color scales, data bars, icon sets
- Data tools: data validation (drop-downs, ranges), auto-filter, Excel tables
- Charts: bar/column, line, pie, doughnut, area, scatter, bubble, radar, stock, surface; axes, titles, legends, labels, secondary axis, combined charts
- Images, comments, hyperlinks
- Print setup: paper, orientation, margins, print area, print titles, header/footer, page breaks, fit to page
- Large files: `read_only=True` for reading, `write_only=True` for writing

## Limits — tell the user up front

When a request needs one of these, say so in the todo list and offer the workaround instead of silently dropping it:

| Limit | What to do |
|-------|------------|
| Formulas are not calculated | The file stores formulas with no results until Excel or LibreOffice opens and saves it. If a value must be known now (to report it or use it elsewhere), compute it in Python and write the number, or write both the formula and a Python-computed check value in a notes column. |
| Re-saving an existing file can drop charts, images, shapes, slicers, sparklines | Never edit a user's workbook in place. Load it, write the result to a new file, and tell the user what may be missing; rebuild charts in code when needed. |
| Legacy `.xls` | Not supported; ask the user to save it as `.xlsx`. |
| Pivot tables | Kept when loading and saving, but cannot be created or edited; build a summary table with Python instead. |
| Macros (VBA) | `.xlsm` opened with `keep_vba=True` keeps them, but they cannot be run or edited. |
| Filter and sort | `auto_filter` records the filter and sort settings but does not hide or reorder rows; sort the rows in Python before writing. |
| Render to PDF or images | Not possible without Excel or LibreOffice; verify by reading the file back. |
