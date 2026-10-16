# Slide Design System — Orange Business

Design reference for building `.pptx` decks, based on the "PPT PRESENTATION" orange template image. Use it together with `.claude/rules/ppt-rule-v1/ppt-rule-v1.md`. Where the two differ, the rule file's minimums win.

Colors and fonts below were estimated from the image, so treat them as approximate.

## 1. Tone

- Clean, modern, and corporate. Most of the slide is white, with orange as the single accent color.
- Use plenty of white space. Show data as circles, rings, and bars rather than dense text.

## 2. Colors (approximate)

| Role | HEX | Use |
|------|-----|-----|
| Primary orange | `#F26522` | Accent shapes, icons, rings, highlight row, labels |
| Light orange | `#F7A27A` | Secondary ring segments, chart fills |
| Pale orange | `#FDE3D6` | Soft backgrounds, ring tracks |
| Red-orange | `#E8432B` | Second bar series, emphasis text (sparingly) |
| Black | `#1A1A1A` | Titles, header text, dark pill |
| Dark gray | `#444444` | Body text |
| Mid gray | `#9A9A9A` | Captions, sub-text |
| Light gray | `#EDEDED` | Dividers, ring tracks, note boxes |
| White | `#FFFFFF` | Slide background |

- Keep orange to about 10–20% of the slide area. Do not add other hues.

## 3. Fonts

| Element | Font | Style | Size |
|---------|------|-------|------|
| Cover title | Montserrat (fallback: Arial Black) | Extra Bold Italic, black | 54–60 pt |
| Slide header title | Montserrat (fallback: Arial) | Bold Italic, black | 24–28 pt |
| Section label ("CONTENTS A") | Malgun Gothic | Bold, black or orange | 16–18 pt |
| Body (Korean) | Malgun Gothic (맑은 고딕) | Regular, dark gray | 14–16 pt |
| Caption | Malgun Gothic | Regular, mid gray | 14 pt |
| Big numbers ("75%") | Montserrat (fallback: Arial) | Bold, black | 28–40 pt |

- Use uppercase English for labels (CONTENTS, TEXT A). Put Korean in the body text.
- The template's captions are smaller than 14 pt. Keep them at 14 pt or larger, per ppt-rule-v1.

## 4. Canvas and grid

- 16:9, 13.333 × 7.5 in. White background.
- Margins: 0.5 in on all sides. Gaps between elements: at least 0.2 in.
- Content area: below the header (top ≈ 1.2 in) down to 7.0 in.
- Use a 3-column grid for most content slides (column ≈ 3.8 in, gutter ≈ 0.4 in).

## 5. Common header (all content slides)

- **Top left:** a small orange tab (≈1.3 × 0.35 in), rounded or slanted on the right, with white "CONTENTS" text inside. Put the italic bold slide title right next to it.
- **Thin gray line** (`#EDEDED`, 0.75 pt) running from the title to the right margin.
- **Top right:** a small black pill (≈0.9 × 0.25 in) with a white label (page or section).
- **Bottom:** a thin orange line (1 pt) across the slide, inside the margins.

## 6. Slide layouts

| Layout | Description |
|--------|-------------|
| Cover | A wide orange capsule on the left (rounded on the right), holding a photo with an orange overlay (~70% opacity) and a white headline. The title is on the right in black bold italic, with a gray subtitle under it. Faint diagonal orange lines and thin concentric gray circles sit in the background. Two small pills (orange and black) go in the bottom left. |
| 3-column icon pie | Three circles in a row, each with an orange partial ring, a white center, and an orange icon. A small orange triangle points down to a label and a short description. |
| 3-column donut | Three donut charts (orange, light orange, and pale segments), each with an orange icon badge on top, "CONTENTS" in the center, and text below. |
| Image + list | A large circular photo (grayscale) on the right with orange icon circles along its arc, and 3 label + text items to their left. One featured card sits on the far left. |
| Percentage rings | Three thin orange arcs with a big % number inside, connected by thin gray lines to labels below. At the bottom: a gray note box with an orange "Check" tag. |
| Table | 3 columns (label, text, dot rating). Rows have thin gray dividers. One highlighted row has an orange fill with white text. An orange pill button sits at the bottom right. |
| Bar comparison | Two groups, each a bracket line with a label, and two horizontal bars (orange and red-orange) with % values. A black circle "Check" marker links the groups. |

## 7. Shapes and graphics

- Shapes: circles, rings or arcs, capsules (fully rounded rectangles), and pill labels. Avoid sharp boxes except for tables.
- Lines: thin (0.75–1 pt), in gray or orange.
- Icons: simple flat line or filled glyphs, white on an orange circle or orange on white.
- Photos: grayscale, or under an orange overlay. Crop to circles or capsules.
- Shadows: none or very soft. No gradients except for faint background decorations.

## 8. Do / Don't

- **Do:** keep one accent color, align to the grid, repeat the same header on every content slide, and use at most 3 items per row.
- **Don't:** use more than about 6 bullets, add other bright colors, go below 14 pt, or let decorations overlap text.
