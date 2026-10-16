# PPT Rules (v1)

These rules apply whenever you build or edit a PowerPoint (`.pptx`) deck in this project. They work alongside the `mk-ppt` skill.

## 0. Precedence

- Apply these rules first, before the `mk-ppt` skill or any other slide skill.
- When sources disagree, follow this order: **this rule file → the user's design file → the `mk-ppt` skill**.
- A design file may set stricter values, but never lower the minimums here (font sizes, margins, gaps).
- Use the project's `mk-ppt` skill for `.pptx` work, not the global `pptx` skill.

## 1. Default slide count: 8

- Build 8 slides by default, counting the title slide and the closing slide.
- If the user asks for a different number, use their number.
- If the content does not fit in 8 slides, do not cram it. Tell the user and suggest either splitting slides or cutting content.

## 2. Follow the user's design file

- Before building, read the design `.md` file the user provides (colors, fonts, layout, spacing, tone, and so on).
- Apply what it says to every slide. Where the file gives no guidance, use defaults that match its style.
- If no design file was provided, ask the user for one before building. Use the project defaults only if the user says to go ahead without one.
- In your final report, list which design rules you applied and where you deviated, with the reason.

## 3. No overflow, no overlap

Text must never spill past the slide edges, and no text or shape may overlap another in a way that hurts readability.

- **Limit text.** Keep each slide to about 6 bullets, and keep each bullet to about 2 lines. Move extra content to another slide or to the speaker notes.
- **Size boxes for their text.** Make every text box large enough for its text at the chosen font size. Turn on word wrap. If text still does not fit, shorten it or split the slide before you shrink the font. Do not go below 14 pt for body text or 24 pt for titles.
- **Keep margins and gaps.** Leave at least 0.4 in (about 1 cm) between every element and the slide edge, and at least 0.2 in between elements.
- **Plan the layout on a grid.** Before placing elements, decide each one's position and size so that titles, body text, images, charts, and shapes have their own areas.
- **Check after building.** Read the deck back with python-pptx and confirm that:
  - every shape lies inside the slide (`left >= 0`, `top >= 0`, `left + width <= slide_width`, `top + height <= slide_height`);
  - no two shapes' bounding boxes overlap, unless one is a deliberate background or a text box placed on top of a shape;
  - the text in each box is not likely to need more lines than its height allows (estimate from character count, font size, and box width).
- Fix any problem you find and check again. You cannot see the rendered slides, so say so in your report and ask the user to open the file in PowerPoint to confirm.
