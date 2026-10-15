---
name: mk-doc
description: Build or edit Word (.docx) documents in this project with python-docx. Use this skill whenever the user asks for a Word file, a .docx, a report, a memo, a document to print or submit, or 문서 / 보고서 / 워드 파일, wants a research note turned into a document, or wants to read, change, check, or find-and-replace text in an existing .docx in this project, even if they do not say "python-docx".
---

# mk-doc

Make and edit `.docx` files for this project by writing a Python build script that uses python-docx, running it, and checking the result by reading the file back.

## Which tool builds which document

- `report/AI_발전_보고서.docx` is built by `scripts/build_report.js` (Node.js `docx` library), which already has a cover, a table of contents, and page numbers. To change that report, edit `build_report.js` and run `npm run build:report`; do not port it to Python.
- Use python-docx for new documents, and for reading or editing an existing `.docx` (python-docx is the only one of the two that can open a file).

## Environment

- Python 3.13 and python-docx 1.2.0 are installed globally for this user. Import it as `docx`.
- `python` may not be on PATH in an older shell. If `python --version` fails, use the full path:
  - PowerShell: `& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"`
  - Bash: `"$LOCALAPPDATA/Programs/Python/Python313/python.exe"`
- The Windows console code page garbles Korean in `print()` output (the file itself is fine). Set `PYTHONIOENCODING=utf-8` when running scripts whose output you need to read.
- Run Python with `-B` so importing the helpers does not leave `__pycache__/` in the skill folder.
- Helper functions live in `.claude/skills/mk-doc/scripts/docx_helpers.py`. Import them by adding that folder to `sys.path` (see the template below) instead of copying code into each build script.

## Where files go

| What | Where | Name |
|------|-------|------|
| Build script | `scripts/` | `build_<topic>_docx.py` (English, snake_case) |
| Output document | `report/` | Korean title, e.g. `AI_정책_요약.docx` |

- Never overwrite an existing document. To change one, edit its build script, or load the existing file and save the result under a new name (add a date such as `_2026-10-15`, or let `next_available_path()` add `_2`, `_3`, ...), then tell the user the new name. Move older documents to `archive/` only when the user agrees.
- Document text is Korean unless the user asks otherwise.
- When the content comes from a research note in `research/`, keep the figures as they appear there, keep the "indicative" marks on secondary-source figures, and include a sources section.

## Workflow

1. **Plan the document.** Write the outline (headings, what goes under each, tables and images) and include it in the todo list you report to the user, so they approve the structure before you build.
2. **Write the build script** in `scripts/` from the template below. One function per section keeps it easy to edit later.
3. **Run it** and fix any errors.
4. **Verify by reading the document back** with python-docx: headings in order, paragraph and table counts, table contents, images, hyperlinks, header/footer text, and that Korean text uses the Korean font. Report what you checked. You cannot see the rendered pages or the page count, so say so and suggest the user open the file in Word; if the document has a TOC, remind them it fills in when Word updates fields.

## Build script template

```python
"""Build report/<document>.docx. Run: python -B scripts/build_<topic>_docx.py"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "mk-doc" / "scripts"))

from docx.shared import Cm
from docx_helpers import (
    new_document, add_toc, add_table, add_hyperlink, add_page_number,
    apply_korean_font, next_available_path,
)

OUT = next_available_path(ROOT / "report" / "<문서_이름>.docx")

def build_intro(doc):
    doc.add_heading("1. 개요", 1)
    doc.add_paragraph("본문 문단.")
    doc.add_paragraph("요점", style="List Bullet")

def build_sources(doc):
    doc.add_heading("출처", 1)
    p = doc.add_paragraph()
    add_hyperlink(p, "출처 이름", "https://example.com")

def main():
    doc = new_document()              # A4, 2.5 cm margins, Korean font on all styles
    doc.add_heading("문서 제목", 0)
    add_toc(doc)
    build_intro(doc)
    build_sources(doc)
    add_page_number(doc.sections[0])
    apply_korean_font(doc)            # last, so every run gets the font
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(f"saved {OUT}")

if __name__ == "__main__":
    main()
```

## Helpers (`scripts/docx_helpers.py`)

| Function | Why it exists |
|----------|---------------|
| `new_document(template=None, font="맑은 고딕", size=11, a4=True, margin_cm=2.5)` | The built-in template is US Letter with theme fonts; this switches to A4 and applies the Korean font to every style. A template keeps its own page setup. |
| `set_run_font(run, name=None, size=None, bold=None, color=None)` | `font.name` alone does not change Korean text; this also sets `w:eastAsia`. `color` is hex like `"1F4E79"`. |
| `set_style_fonts(doc, name)` | Korean font in document defaults and all paragraph/character styles, removing theme-font links that would override it (headings use them). |
| `apply_korean_font(doc, name="맑은 고딕")` | `set_style_fonts` plus every run in body, tables, headers, and footers. |
| `add_hyperlink(paragraph, text, url)` | python-docx can read links but not create them. Returns the run for styling. |
| `add_page_number(section, pattern="{PAGE} / {NUMPAGES}", align=CENTER, header=False)` | Page-number fields in the footer or header. |
| `add_toc(doc, levels="1-3")` | TOC field from headings. Shows a placeholder until Word updates fields; the file asks Word to update fields on open. |
| `add_table(doc, headers, rows, style="Table Grid", header_fill="1F4E79", col_widths_cm=None)` | Table with a shaded, bold header row that repeats on each page. |
| `set_cell_background(cell, color)` | Cell shading, which has no python-docx API. |
| `replace_text(doc, old, new)` | Find and replace across body, tables, headers, footers, even when Word split the text across runs. The new text takes the formatting of the run where the match starts. Returns the count. Hyperlink text and text boxes are not searched. |
| `next_available_path(path)` | Returns a free file name so existing outputs are never overwritten. |

## What python-docx can do

Read `references/python-docx-api.md` for code snippets when a document needs one of these:

- File: new/open/save, using an existing `.docx` as a template, core properties
- Paragraphs and headings: add, insert before, alignment, indents, spacing, keep-with-next, page-break-before, tab stops
- Runs: font, size, bold/italic/underline/strike, color, highlight, sub/superscript, caps, hidden
- Styles: apply built-in styles, add or modify paragraph/character/table styles
- Lists: `List Bullet`, `List Number`, and their level 2-3 variants
- Tables: add rows/columns, cell text and nested content, merge, widths, row height, vertical alignment, table style and alignment
- Images: inline pictures in the body, in table cells, in headers/footers
- Pages and sections: page and line breaks, new sections, page size and orientation, margins
- Headers and footers: text, images, tables; different first page; different odd/even pages; link/unlink from previous section
- Comments (1.2.0): add comments to runs, read existing comments
- Reading: walk paragraphs and tables in order (`iter_inner_content`), read hyperlinks, rendered page breaks, raw XML

## Limits — tell the user up front

When a request needs one of these, say so in the todo list and offer the workaround instead of silently dropping it:

| Limit | What to do |
|-------|------------|
| Hyperlinks, page numbers, TOC, other fields | No API; use the helpers. A TOC and field values appear only after Word updates fields. |
| Find and replace | No API; use `replace_text`. Check the count it returns. |
| Footnotes/endnotes, tracked changes, equations, text boxes | Not supported. Use a "출처" or "주" section instead of footnotes; ask the user to add the rest in Word. |
| Floating (text-wrapped) images and shapes | Only inline pictures can be created; existing floating ones are kept. |
| Restarting list numbering, multi-level numbering control | Not supported directly; use separate numbered paragraphs written as text ("1.", "2.") when the numbering must restart. |
| Multiple columns | No API; needs `w:cols` in the section XML. Ask before doing it. |
| Legacy `.doc`, `.dotx` templates | `.doc` is not supported; ask the user to save as `.docx`. A `.dotx` must be converted to `.docx` before python-docx can open it. |
| Render to PDF or images, page count | Not possible without Word or LibreOffice; verify by reading the file back. |
