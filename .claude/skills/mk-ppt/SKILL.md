---
name: mk-ppt
description: Build or edit PowerPoint (.pptx) decks in this project with python-pptx. Use this skill whenever the user asks for slides, a PPT, a presentation, a deck, or 발표 자료 / 슬라이드 / 피피티, wants to turn a research note or report into slides, or wants to change, inspect, or extract content from an existing .pptx file in this project, even if they do not say "python-pptx".
---

# mk-ppt

Make and edit `.pptx` files for this project by writing a Python build script that uses python-pptx, running it, and checking the result by reading the file back.

## Read first: PPT rules take precedence

- Before any `.pptx` work, apply `.claude/rules/ppt-rule-v1/ppt-rule-v1.md` (loaded automatically). If this skill and the rule file disagree, the rule file wins.
- Order of precedence: **rule file → the user's design file (e.g. `references/ppt/slide-design-system.md`) → this skill**. A design file may not go below the rule file's minimums (font sizes, margins, gaps).
- The pink theme (`PINK_THEME`, `apply_pink_theme`) and the `Noto Sans KR` font below are fallback defaults. Use them only when the user says to go ahead without a design file.

## Environment

- Python 3.13 and python-pptx 1.0.2 are installed globally for this user.
- `python` may not be on PATH in an older shell. If `python --version` fails, use the full path:
  - PowerShell: `& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"`
  - Bash: `"$LOCALAPPDATA/Programs/Python/Python313/python.exe"`
- The Windows console code page garbles Korean in `print()` output (the file itself is fine). Set `PYTHONIOENCODING=utf-8` when running scripts whose output you need to read (`$env:PYTHONIOENCODING="utf-8"` in PowerShell, or prefix the command in Bash).
- Helper functions live in `.claude/skills/mk-ppt/scripts/pptx_helpers.py`. Import them by adding that folder to `sys.path` (see the template below) instead of copying code into each build script.

## Where files go

| What | Where | Name |
|------|-------|------|
| Build script | `scripts/` | `build_<topic>_pptx.py` (English, snake_case) |
| Output deck | `slides/` | Korean title, e.g. `AI_발전_발표.pptx` |

- Never overwrite an existing deck. To change a deck, edit its build script and save the output under a new name (add a date such as `_2026-10-15`, or let `next_available_path()` from the helpers add `_2`, `_3`, ...), then tell the user the new name. Move older decks to `archive/slides/` only when the user agrees.
- Deck text is Korean unless the user asks otherwise, like the reports in `report/`.
- When the content comes from a research note in `research/`, keep the figures as they appear there and keep the "indicative" marks on secondary-source figures.

## Workflow

1. **Get the design file.** Read the design `.md` the user provides. If none was given, ask for one; use the fallback defaults only if the user says to go ahead without one.
2. **Plan the deck.** Use 8 slides unless the user asks otherwise. Write a short slide outline (slide title + key points per slide) and include it in the todo list you report to the user, so they approve the structure before you build. If the content does not fit, say so and suggest splitting or cutting.
3. **Write the build script** in `scripts/` from the template below. Plan each element's position on a grid first. One function per slide keeps the script easy to edit later.
4. **Run it** and fix any errors.
5. **Verify by reading the deck back** with python-pptx: slide count, each slide's title, that tables/charts/images exist where planned, and that Korean text uses the Korean font. Also run the rule file's checks: every shape inside the slide, no unintended overlaps, and no text likely to overflow its box. Fix and check again until clean.
6. **Report.** Say what you checked, which design rules you applied, and where you deviated and why. You cannot see the rendered slides, so say so instead of claiming the layout looks right; ask the user to open the file in PowerPoint.

## Build script template

```python
"""Build slides/<deck>.pptx. Run: python scripts/build_<topic>_pptx.py"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "mk-ppt" / "scripts"))

from pptx import Presentation
from pptx.util import Pt, Inches
from pptx_helpers import (
    new_presentation, add_title_slide, add_bullet_slide,
    apply_korean_font, next_available_path,
)

OUT = next_available_path(ROOT / "slides" / "<덱_이름>.pptx")

def main():
    prs = new_presentation()          # 16:9
    add_title_slide(prs, "제목", "부제목")
    add_bullet_slide(prs, "요점", ["첫째", ("세부 항목", 1), "둘째"])
    apply_korean_font(prs)            # last, so every text run gets the font
    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"saved {OUT}")

if __name__ == "__main__":
    main()
```

## Helpers (`scripts/pptx_helpers.py`)

| Function | Why it exists |
|----------|---------------|
| `new_presentation(template=None, widescreen=True)` | New or template-based deck, 16:9 by default (python-pptx defaults to 4:3). |
| `add_title_slide(prs, title, subtitle=None)` | Title slide from layout 0. |
| `add_bullet_slide(prs, title, items)` | Bullets; an item can be `"text"` or `("text", level)`. |
| `set_font(font, name=None, size=None, bold=None, color=None)` | `font` is `run.font` or `paragraph.font`. Sets both the Latin and East Asian font; `font.name` alone does not change Korean text. `color` is hex like `"1F4E79"`. |
| `apply_korean_font(prs, name="Noto Sans KR")` | Applies the Korean font to every run in every shape, group, and table (not charts). |
| `PINK_THEME` | Pink palette dict (hex): `background`, `primary` (titles), `secondary` (bars), `accent`, `text` (body). |
| `set_slide_background(slide, color)` | Solid background fill from a hex color. |
| `add_accent_bar(slide, prs, color=PINK_THEME["secondary"], top=..., height=...)` | Thin full-width bar, by default just under the title. |
| `apply_pink_theme(prs, theme=PINK_THEME, font="Noto Sans KR")` | Pink background on every slide, bold pink titles, gray body text, theme font everywhere. Call after all content is added. |
| `delete_slide(prs, slide)` | No official API for this. |
| `duplicate_slide(prs, slide)` | No official API; copies shapes, background, and image/link relationships. Notes are not copied, and a copied chart shares data with the original, so rebuild charts instead. |
| `move_slide(prs, slide, new_index)` | No official API for reordering. |
| `next_available_path(path)` | Returns a free file name so existing outputs are never overwritten. |

## What python-pptx can do

Read `references/python-pptx-api.md` for code snippets when a slide needs one of these:

- File: new/open/save, template-based decks, slide size, core properties
- Slides: add from layout, list masters/layouts, solid background, speaker notes
- Text: placeholders, text boxes, paragraph/run formatting, alignment, spacing, levels, auto-fit, hyperlinks
- Shapes: auto shapes, connectors, freeforms, fill/line, groups, click actions
- Images and media: insert/crop pictures, insert video (experimental), extract images
- Tables: add, cell text/format/fill, merge, column widths, style flags
- Charts: bar/column, line, pie/doughnut, area, XY scatter, bubble, radar; axes, legend, labels; replace data
- Reading: walk slides/shapes/text, read tables and chart data, raw XML access

## Limits — tell the user up front

When a request needs one of these, say so in the todo list and offer the workaround instead of silently dropping it:

| Not supported | What to do |
|---------------|------------|
| Delete / duplicate / reorder slides | Use the helpers above. |
| Animations, slide transitions | Not possible; the user adds them in PowerPoint. |
| Render to PDF or images, preview | Not possible without PowerPoint or LibreOffice; verify by reading the file back. |
| SmartArt, legacy `.ppt` | Not possible; build the diagram from shapes/connectors, or ask the user to save as `.pptx`. |
| Picture fills, 3D effects, some advanced formatting | Limited; use solid/gradient fills or a template that already has the look. |
