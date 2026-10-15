# python-pptx 1.0.2 quick reference

Snippets for the mk-ppt skill. Units: use `Inches()`, `Cm()`, `Pt()`, or `Emu()` from `pptx.util`. A 16:9 deck from `new_presentation()` is 13.333 in × 7.5 in.

## Contents

1. File and deck
2. Slides
3. Text
4. Shapes
5. Images and media
6. Tables
7. Charts
8. Reading an existing deck
9. Raw XML

## 1. File and deck

```python
from pptx import Presentation
prs = Presentation()                    # built-in 4:3 template
prs = Presentation("template.pptx")     # keep a template's theme, master, layouts
prs.slide_width, prs.slide_height       # EMU; set both to resize
prs.core_properties.title = "제목"       # also author, subject, keywords, created, modified
prs.save("slides/덱.pptx")
```

Prefer `new_presentation()` from the helpers for a blank 16:9 deck; it also stretches the layouts.

## 2. Slides

```python
for i, layout in enumerate(prs.slide_layouts):    # default: 0 Title, 1 Title+Content,
    print(i, layout.name)                         # 5 Title Only, 6 Blank
slide = prs.slides.add_slide(prs.slide_layouts[6])

for ph in slide.placeholders:
    print(ph.placeholder_format.idx, ph.placeholder_format.type, ph.name)

fill = slide.background.fill                      # solid background
fill.solid(); fill.fore_color.rgb = RGBColor(0xF5, 0xF7, 0xFA)

slide.notes_slide.notes_text_frame.text = "발표자 노트"
```

Delete, duplicate, reorder: use the helpers (`delete_slide`, `duplicate_slide`, `move_slide`).

## 3. Text

```python
from pptx.util import Pt, Inches
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE

box = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(6), Inches(1))
tf = box.text_frame
tf.word_wrap = True
tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE    # or SHAPE_TO_FIT_TEXT, NONE
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.1)

p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
p.level = 0                                       # 0-8, bullet depth in body placeholders
p.line_spacing = 1.2                              # or Pt(24)
p.space_before = Pt(6); p.space_after = Pt(6)

run = p.add_run(); run.text = "강조"
f = run.font
f.size = Pt(24); f.bold = True; f.italic = False; f.underline = True
f.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
run.hyperlink.address = "https://example.com"
```

Korean text: `font.name` sets only the Latin font. Use `set_font(run.font, "맑은 고딕")` or call `apply_korean_font(prs)` before saving.

## 4. Shapes

```python
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.action import PP_ACTION

shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(2), Inches(3), Inches(1))
shp.text_frame.text = "단계 1"
shp.fill.solid(); shp.fill.fore_color.rgb = RGBColor(0x1F, 0x4E, 0x79)
shp.fill.gradient(); shp.fill.gradient_angle = 90  # gradient instead of solid
shp.line.color.rgb = RGBColor(0, 0, 0); shp.line.width = Pt(1.5)
shp.line.dash_style = MSO_LINE_DASH_STYLE.DASH
shp.rotation = 15
shp.shadow.inherit = False                        # remove theme shadow

line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(4), Inches(2.5), Inches(5), Inches(2.5))
line.begin_connect(shp, 3); line.end_connect(other, 1)  # optional: glue to shapes

ff = slide.shapes.build_freeform(Inches(1), Inches(1))  # start point
ff.add_line_segments([(Inches(2), Inches(1)), (Inches(1.5), Inches(2))], close=True)
tri = ff.convert_to_shape()

grp = slide.shapes.add_group_shape()
grp.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1), Inches(1), Inches(1), Inches(1))

shp.click_action.hyperlink.address = "https://example.com"
shp.click_action.target_slide = prs.slides[0]     # jump to a slide
```

Diagrams (SmartArt is not supported): build them from shapes plus connectors.

## 5. Images and media

```python
pic = slide.shapes.add_picture("img.png", Inches(1), Inches(1), width=Inches(4))  # height keeps ratio
pic.crop_left = 0.1; pic.crop_right = 0.1          # fractions of the original size

movie = slide.shapes.add_movie("clip.mp4", Inches(1), Inches(1), Inches(4), Inches(3),
                               poster_frame_image="poster.png", mime_type="video/mp4")  # experimental

for shape in slide.shapes:                          # extract images
    if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
        Path(f"out.{shape.image.ext}").write_bytes(shape.image.blob)
```

## 6. Tables

```python
gf = slide.shapes.add_table(rows=4, cols=3, left=Inches(1), top=Inches(1.5),
                            width=Inches(8), height=Inches(3))
table = gf.table
table.columns[0].width = Inches(3)
table.rows[0].height = Inches(0.6)
table.first_row = True; table.horz_banding = True   # style flags

cell = table.cell(0, 0)
cell.text = "항목"
cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor(0x1F, 0x4E, 0x79)
cell.vertical_anchor = MSO_ANCHOR.MIDDLE
cell.margin_left = Inches(0.1)

table.cell(1, 0).merge(table.cell(2, 0))            # merge a range
cell.is_merge_origin, cell.is_spanned; cell.split()
```

Table cells are covered by `apply_korean_font`.

## 7. Charts

```python
from pptx.chart.data import CategoryChartData, XyChartData, BubbleChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION

data = CategoryChartData()
data.categories = ["2023", "2024", "2025"]
data.add_series("매출", (120, 150, 190))
data.add_series("비용", (80, 95, 110))
gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,
                            Inches(1), Inches(1.5), Inches(8), Inches(4.5), data)
chart = gf.chart

chart.has_title = True; chart.chart_title.text_frame.text = "연도별 추이"
chart.has_legend = True; chart.legend.position = XL_LEGEND_POSITION.BOTTOM
chart.legend.include_in_layout = False
chart.value_axis.has_major_gridlines = False
chart.value_axis.maximum_scale = 200
chart.category_axis.tick_labels.font.size = Pt(12)

plot = chart.plots[0]
plot.has_data_labels = True
plot.data_labels.number_format = '#,##0'; plot.data_labels.number_format_is_linked = False
plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END

series = plot.series[0]
series.format.fill.solid(); series.format.fill.fore_color.rgb = RGBColor(0x1F, 0x4E, 0x79)

chart.font.name = "맑은 고딕"; chart.font.size = Pt(12)   # chart-wide font
chart.replace_data(new_data)                               # swap data, keep formatting
```

Chart types (`XL_CHART_TYPE`): `COLUMN_CLUSTERED`, `COLUMN_STACKED`, `BAR_CLUSTERED`, `LINE`, `LINE_MARKERS`, `PIE`, `DOUGHNUT`, `AREA`, `XY_SCATTER`, `BUBBLE`, `RADAR`, and their variants. XY charts take `XyChartData` (`series.add_data_point(x, y)`); bubble charts take `BubbleChartData` (`add_data_point(x, y, size)`). A combo chart (bar + line) is not supported by the API.

## 8. Reading an existing deck

```python
from pptx.enum.shapes import MSO_SHAPE_TYPE

prs = Presentation("slides/덱.pptx")
for n, slide in enumerate(prs.slides, 1):
    title = slide.shapes.title.text if slide.shapes.title else ""
    print(n, slide.slide_layout.name, title)
    for shape in slide.shapes:
        print("  ", shape.shape_type, shape.name, shape.left, shape.top, shape.width, shape.height)
        if shape.has_text_frame:
            print("    ", shape.text_frame.text)
        if shape.has_table:
            rows = [[c.text for c in r.cells] for r in shape.table.rows]
        if shape.has_chart:
            ch = shape.chart
            cats = list(ch.plots[0].categories)
            vals = {s.name: list(s.values) for s in ch.plots[0].series}
    if slide.has_notes_slide:
        print("  notes:", slide.notes_slide.notes_text_frame.text)
```

## 9. Raw XML

Every proxy object has `._element` (an lxml element). Use it for features the API lacks; `from pptx.oxml.ns import qn` builds tag names such as `qn("a:ea")`. Keep such code in a helper with a docstring saying why it is needed.
