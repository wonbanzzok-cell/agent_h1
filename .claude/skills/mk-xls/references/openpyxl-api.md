# openpyxl 3.1.5 quick reference

Snippets for the mk-xls skill. Rows and columns are 1-based. Colors are hex strings without `#`, e.g. `"1F4E79"`.

## Contents

1. Workbook
2. Sheets
3. Cells and data
4. Formulas
5. Styles
6. Conditional formatting
7. Data validation, filters, tables
8. Charts
9. Images, comments, hyperlinks
10. Print setup
11. Large files

## 1. Workbook

```python
from openpyxl import Workbook, load_workbook
wb = Workbook()                                   # one sheet named "Sheet"
wb = load_workbook("in.xlsx")                     # .xlsx .xlsm .xltx .xltm
wb = load_workbook("in.xlsm", keep_vba=True)      # keep macros (not runnable)
wb.save("sheets/결과.xlsx")
wb.template = True                                # save as a template (.xltx)

wb.properties.title = "제목"; wb.properties.creator = "작성자"

from openpyxl.workbook.defined_name import DefinedName
wb.defined_names["세율"] = DefinedName("세율", attr_text="설정!$B$1")

from openpyxl.workbook.protection import WorkbookProtection
wb.security = WorkbookProtection(workbookPassword="pw", lockStructure=True)
```

## 2. Sheets

```python
ws = wb.active; ws.title = "요약"
ws2 = wb.create_sheet("데이터")                 # append; create_sheet("앞", 0) inserts first
copy_ws = wb.copy_worksheet(ws2)                  # same workbook only; charts/images not copied
wb.remove(wb["Sheet"])
wb.move_sheet("데이터", offset=-1)
cs = wb.create_chartsheet("차트")                 # cs.add_chart(chart)

ws.sheet_properties.tabColor = "1F4E79"
ws.sheet_state = "hidden"
ws.freeze_panes = "B2"                            # freeze row 1 and column A
ws.sheet_view.zoomScale = 90
ws.sheet_view.showGridLines = False
ws.protection.sheet = True; ws.protection.password = "pw"
```

## 3. Cells and data

```python
from datetime import date
ws["A1"] = "이름"; ws.cell(row=2, column=1, value=date(2026, 10, 15))
ws.append(["서울", 1200, 0.12])                   # next empty row

for row in ws.iter_rows(min_row=2, max_col=3, values_only=True):
    print(row)
for col in ws.iter_cols(min_col=2, max_col=2):
    ...
cells = ws["A1:C10"]; ws.max_row; ws.max_column

ws.insert_rows(2, amount=3); ws.delete_cols(4)
ws.move_range("A1:C3", rows=2, cols=1, translate=True)   # translate shifts formulas
ws.merge_cells("A1:D1"); ws.unmerge_cells("A1:D1")

ws.column_dimensions["A"].width = 20
ws.row_dimensions[1].height = 30
ws.column_dimensions["E"].hidden = True
ws.row_dimensions.group(5, 10, hidden=True)      # outline group

from openpyxl.utils import get_column_letter, column_index_from_string
get_column_letter(28)  # "AB"
```

## 4. Formulas

```python
ws["B6"] = "=SUM(B2:B5)"
ws["C2"] = "=IFERROR(B2/B$6,0)"
ws["D2"] = '=VLOOKUP(A2,데이터!A:B,2,FALSE)'      # quote names with spaces: '\'시트 1\'!A1'

from openpyxl.worksheet.formula import ArrayFormula
ws["E2"] = ArrayFormula("E2:E5", "=B2:B5*C2:C5")

wb_values = load_workbook("in.xlsx", data_only=True)   # cached results, None if never calculated
```

Use English function names and commas as separators, whatever the user's Excel locale. Newer functions (e.g. `XLOOKUP`, `FILTER`) may need the `_xlfn.` prefix, as in `"=_xlfn.XLOOKUP(...)"`, to show up correctly.

## 5. Styles

```python
from openpyxl.styles import Font, PatternFill, GradientFill, Border, Side, Alignment, Protection, NamedStyle

c = ws["A1"]
c.font = Font(name="맑은 고딕", size=12, bold=True, italic=False, underline="single", color="FFFFFF")
c.fill = PatternFill("solid", start_color="1F4E79")
c.fill = GradientFill(stop=("FFFFFF", "1F4E79"))
thin = Side(style="thin", color="BFBFBF")
c.border = Border(left=thin, right=thin, top=thin, bottom=thin)
c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True, text_rotation=0, indent=0)
c.number_format = "#,##0"        # "0.0%", "yyyy-mm-dd", '#,##0"원"', "₩#,##0"
c.protection = Protection(locked=False)          # editable when the sheet is protected

header = NamedStyle(name="header")
header.font = Font(bold=True, color="FFFFFF"); header.fill = PatternFill("solid", start_color="1F4E79")
wb.add_named_style(header); ws["B1"].style = "header"
```

Style objects are immutable: to change one attribute, `f = copy(c.font); f.bold = True; c.font = f`.

## 6. Conditional formatting

```python
from openpyxl.formatting.rule import CellIsRule, FormulaRule, ColorScaleRule, DataBarRule, IconSetRule
red = PatternFill("solid", start_color="F8CBAD")

ws.conditional_formatting.add("C2:C100", CellIsRule(operator="lessThan", formula=["0"], fill=red))
ws.conditional_formatting.add("A2:D100", FormulaRule(formula=["$D2>1000"], fill=red))
ws.conditional_formatting.add("C2:C100", ColorScaleRule(start_type="min", start_color="F8696B",
                                                         mid_type="percentile", mid_value=50, mid_color="FFEB84",
                                                         end_type="max", end_color="63BE7B"))
ws.conditional_formatting.add("B2:B100", DataBarRule(start_type="min", end_type="max", color="5B9BD5"))
ws.conditional_formatting.add("E2:E100", IconSetRule("3Arrows", "percent", [0, 33, 67]))
```

## 7. Data validation, filters, tables

```python
from openpyxl.worksheet.datavalidation import DataValidation
dv = DataValidation(type="list", formula1='"진행,완료,보류"', allow_blank=True)
dv.error = "목록에서 고르세요"; dv.prompt = "상태 선택"
ws.add_data_validation(dv); dv.add("D2:D200")
DataValidation(type="whole", operator="between", formula1="0", formula2="100")
DataValidation(type="list", formula1="=목록!$A$2:$A$20")   # list from a range

ws.auto_filter.ref = "A1:D200"                    # filter buttons only; rows are not hidden
ws.auto_filter.add_sort_condition("B2:B200")      # recorded, not applied

from openpyxl.worksheet.table import Table, TableStyleInfo
t = Table(displayName="Sales", ref="A1:D200")
t.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
ws.add_table(t)                                   # do not also set ws.auto_filter on this range
```

## 8. Charts

```python
from openpyxl.chart import BarChart, LineChart, PieChart, DoughnutChart, AreaChart, ScatterChart, Reference, Series
from openpyxl.chart.label import DataLabelList

ch = BarChart(); ch.type = "col"                  # "bar" for horizontal; ch.grouping = "stacked"; ch.overlap = 100
ch.title = "지역별 매출"; ch.y_axis.title = "원"; ch.x_axis.title = "지역"
data = Reference(ws, min_col=2, max_col=3, min_row=1, max_row=5)   # include header row for series names
cats = Reference(ws, min_col=1, min_row=2, max_row=5)
ch.add_data(data, titles_from_data=True); ch.set_categories(cats)
ch.width, ch.height = 18, 9                       # cm
ch.legend.position = "b"                          # r, l, t, b, tr; ch.legend = None to hide
ch.dataLabels = DataLabelList(); ch.dataLabels.showVal = True
ch.y_axis.numFmt = "#,##0"; ch.y_axis.majorGridlines = None
ch.x_axis.delete = False; ch.y_axis.delete = False   # axes can be hidden by default in newer Excel
ws.add_chart(ch, "F2")

line = LineChart(); line.add_data(Reference(ws, min_col=4, min_row=1, max_row=5), titles_from_data=True)
line.y_axis.axId = 200; line.y_axis.crosses = "max"   # secondary axis
ch += line                                        # combined bar + line

sc = ScatterChart(); xs = Reference(ws, min_col=1, min_row=2, max_row=20)
s = Series(Reference(ws, min_col=2, min_row=1, max_row=20), xs, title_from_data=True); sc.series.append(s)
```

Other chart classes: `BubbleChart`, `RadarChart`, `StockChart`, `SurfaceChart`, `BarChart3D`, `PieChart3D`.

## 9. Images, comments, hyperlinks

```python
from openpyxl.drawing.image import Image       # needs Pillow (installed)
img = Image("logo.png"); img.width, img.height = 120, 40; ws.add_image(img, "H1")

from openpyxl.comments import Comment
ws["A1"].comment = Comment("검토 필요", "작성자")

ws["A2"].hyperlink = "https://example.com"; ws["A2"].style = "Hyperlink"
ws["A3"].hyperlink = "#'데이터'!A1"             # jump inside the workbook
```

## 10. Print setup

```python
ws.page_setup.paperSize = ws.PAPERSIZE_A4
ws.page_setup.orientation = "landscape"
ws.page_margins.left = 0.5                       # inches
ws.print_area = "A1:F50"
ws.print_title_rows = "1:1"                      # repeat header row on every page
ws.oddHeader.center.text = "&[File]"; ws.oddFooter.right.text = "&[Page] / &N"
ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0

from openpyxl.worksheet.pagebreak import Break
ws.row_breaks.append(Break(id=40))
```

## 11. Large files

```python
wb = load_workbook("big.xlsx", read_only=True)   # stream rows; call wb.close() when done
for row in wb["데이터"].iter_rows(values_only=True):
    ...

wb = Workbook(write_only=True); ws = wb.create_sheet("데이터")
ws.append(["a", 1])                              # append only; no random cell access
wb.save("sheets/큰파일.xlsx")
```
