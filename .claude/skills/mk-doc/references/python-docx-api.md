# python-docx 1.2.0 quick reference

Snippets for the mk-doc skill. Import the package as `docx`. Units: `Cm()`, `Mm()`, `Inches()`, `Pt()` from `docx.shared`.

## Contents

1. File and document
2. Paragraphs and headings
3. Runs (character formatting)
4. Styles
5. Lists
6. Tables
7. Images
8. Pages and sections
9. Headers and footers
10. Comments
11. Reading an existing document
12. Raw XML

## 1. File and document

```python
from docx import Document
doc = Document()                         # built-in template: US Letter, theme fonts
doc = Document("report/기존.docx")        # also the way to use a .docx as a template
doc.core_properties.title = "제목"        # author, subject, keywords, created, modified, ...
doc.save("report/새_문서.docx")
```

Prefer `new_document()` from the helpers for a blank document; it sets A4 and the Korean font.

## 2. Paragraphs and headings

```python
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER

doc.add_heading("문서 제목", 0)            # 0 = Title style, 1-9 = Heading 1-9
p = doc.add_paragraph("본문", style="Normal")
before = p.insert_paragraph_before("앞에 끼워 넣기")

pf = p.paragraph_format
pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY    # LEFT, CENTER, RIGHT, JUSTIFY
pf.left_indent = Cm(1); pf.right_indent = Cm(0.5)
pf.first_line_indent = Cm(0.5)               # negative value = hanging indent
pf.space_before = Pt(6); pf.space_after = Pt(6)
pf.line_spacing = 1.5                        # or Pt(18); pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
pf.keep_with_next = True; pf.keep_together = True
pf.page_break_before = True; pf.widow_control = True
pf.tab_stops.add_tab_stop(Cm(15), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
```

## 3. Runs (character formatting)

```python
from docx.enum.text import WD_COLOR_INDEX, WD_UNDERLINE, WD_BREAK

run = p.add_run("강조")
f = run.font
f.size = Pt(12); f.bold = True; f.italic = True
f.underline = WD_UNDERLINE.DOUBLE                # or True
f.strike = True; f.subscript = True; f.superscript = False
f.all_caps = True; f.small_caps = False; f.hidden = False
f.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
f.highlight_color = WD_COLOR_INDEX.YELLOW
run.add_break()                                   # line break; WD_BREAK.PAGE, WD_BREAK.COLUMN
run.add_tab()
```

Korean text: `font.name` sets only the Latin font. Use `set_run_font(run, "맑은 고딕")` or `apply_korean_font(doc)`.

## 4. Styles

```python
from docx.enum.style import WD_STYLE_TYPE

normal = doc.styles["Normal"]
normal.font.size = Pt(11)
normal.paragraph_format.line_spacing = 1.5

st = doc.styles.add_style("강조 문단", WD_STYLE_TYPE.PARAGRAPH)   # also CHARACTER, TABLE
st.base_style = doc.styles["Normal"]
st.next_paragraph_style = doc.styles["Normal"]
st.font.bold = True; st.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
doc.add_paragraph("내용", style="강조 문단")

[s.name for s in doc.styles if s.type == WD_STYLE_TYPE.PARAGRAPH]  # available styles
```

Built-in styles include `Title`, `Subtitle`, `Heading 1`-`9`, `Quote`, `Intense Quote`, `Caption`, `List Bullet`, `List Number`, `Table Grid`, `Light List Accent 1`, and more. A template only has the styles saved in it.

## 5. Lists

```python
doc.add_paragraph("항목", style="List Bullet")
doc.add_paragraph("하위 항목", style="List Bullet 2")    # up to List Bullet 3
doc.add_paragraph("단계", style="List Number")           # List Number 2, 3
```

Numbering continues across the whole document; restarting at 1 is not supported by the API.

## 6. Tables

```python
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL, WD_ROW_HEIGHT_RULE

table = doc.add_table(rows=1, cols=3)
table.style = "Table Grid"
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.autofit = False
row = table.add_row(); col = table.add_column(Cm(3))

cell = table.cell(0, 0)
cell.text = "항목"
cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
cell.width = Cm(4)                                # set on every cell in the column
cell.paragraphs[0].runs[0].font.bold = True
cell.add_paragraph("두 번째 문단")
cell.paragraphs[0].add_run().add_picture("img.png", width=Cm(3))
inner = cell.add_table(rows=2, cols=2)            # nested table

table.rows[0].height = Cm(1); table.rows[0].height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
merged = table.cell(1, 0).merge(table.cell(2, 0))

for r in table.rows:                              # read; merged cells appear repeatedly
    print([c.text for c in r.cells])
```

Use `add_table()` from the helpers for a styled header row, `set_cell_background()` for shading.

## 7. Images

```python
doc.add_picture("chart.png", width=Cm(15))        # height keeps the ratio
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run().add_picture("logo.png", height=Cm(2)) # inside a paragraph, cell, header
doc.add_paragraph("그림 1. 설명", style="Caption")
```

PNG, JPEG, GIF, BMP, TIFF. Only inline images; no text wrapping.

## 8. Pages and sections

```python
from docx.enum.section import WD_ORIENT, WD_SECTION

doc.add_page_break()
sec = doc.add_section(WD_SECTION.NEW_PAGE)        # CONTINUOUS, ODD_PAGE, EVEN_PAGE
sec.orientation = WD_ORIENT.LANDSCAPE
sec.page_width, sec.page_height = sec.page_height, sec.page_width   # swap too
sec.left_margin = Cm(2); sec.gutter = Cm(0)
sec.header_distance = Cm(1.25); sec.footer_distance = Cm(1.25)
```

## 9. Headers and footers

```python
sec = doc.sections[0]
sec.header.paragraphs[0].text = "사내 보고서"
sec.footer.add_paragraph().add_run().add_picture("logo.png", height=Cm(0.8))

sec.different_first_page_header_footer = True
sec.first_page_header.paragraphs[0].text = ""     # e.g. empty on the cover

doc.settings.odd_and_even_pages_header_footer = True
sec.even_page_header.paragraphs[0].text = "짝수 쪽"

doc.sections[1].header.is_linked_to_previous = False   # own header for section 2
```

Page numbers: `add_page_number(section)` from the helpers.

## 10. Comments

```python
run = p.add_run("검토할 문장")
doc.add_comment(run, text="수치 확인 필요", author="작성자", initials="AB")   # runs: one Run or a sequence
for c in doc.comments:
    print(c.author, c.text)
```

## 11. Reading an existing document

```python
from docx.table import Table
from docx.text.paragraph import Paragraph

doc = Document("report/기존.docx")
for block in doc.iter_inner_content():            # paragraphs and tables in document order
    if isinstance(block, Paragraph):
        print(block.style.name, block.text)
        for link in block.hyperlinks:
            print("  link:", link.text, link.address)
        if block.contains_page_break:             # page breaks Word rendered when last saved
            print("  -- page break --")
    elif isinstance(block, Table):
        print([[c.text for c in r.cells] for r in block.rows])

for img in doc.inline_shapes:
    print(img.width.cm, img.height.cm)
```

## 12. Raw XML

Every proxy object exposes its lxml element (`paragraph._p`, `run._r`, `cell._tc`, `doc.element`, `style.element`). Use it for features the API lacks; build elements with `from docx.oxml import OxmlElement` and tag names with `from docx.oxml.ns import qn`. Keep such code in a helper with a docstring saying why it is needed.
