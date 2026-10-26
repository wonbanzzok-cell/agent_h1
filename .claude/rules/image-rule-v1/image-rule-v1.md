# Image Saving Rules (v1)

These rules apply whenever you generate an image with an AI tool (such as the Higgsfield MCP, `mcp__higgsfield__*`) and save it into this project.

## 0. Why this rule exists

- The Higgsfield MCP is a remote server. It cannot write files to this computer. Generated images stay in Higgsfield's cloud and come back as URLs.
- Each result has a `rawUrl` (the original file, e.g. a 2048×2048 PNG) and a `minUrl` (a small WebP preview). The `rawUrl` can be downloaded without logging in.
- So images are never saved to the project automatically. Download them yourself, following the steps below.
- The `folder_id` parameter of the generation tools sets a folder inside Higgsfield, not a folder on this computer.

## 1. Before generating: check the cost

- Call the generation tool with `get_cost: true` first. It returns the credit cost without generating anything.
- Report the cost and the current balance (`balance`) to the user, and generate only after the user approves.
- Do not set `use_unlim` or `use_free_gens` unless the user explicitly asks for them.

## 2. Where to save

| Use | Folder |
|-----|--------|
| Images for a blog post | `blog/<topic>-<YYYY-MM-DD>/images/` (the post's own folder) |
| Everything else (slides, reports, general use) | `images/<topic>-<YYYY-MM-DD>/` |

- Use the generation date for `<YYYY-MM-DD>`, and a short English kebab-case name for `<topic>`.
- Create the folder when you save the first image into it.

## 3. File names

- Name each file `<topic>-<NN>.<ext>`, e.g. `camping-gear-01.png`.
- `<NN>` is a two-digit number. Continue from the highest number already in the folder.
- Keep the extension of the original file (e.g. `.png`, `.jpg`, `.webp`).

## 4. How to download

- Download the `rawUrl`, not the `minUrl`. Get it from the generation result, `jobs_wait`, or `show_generations`.
- Use `curl`, e.g. `curl -sSfL -o "<path>" "<rawUrl>"`.
- After downloading, check that the file exists, that its size is not zero, and that its type is an image (e.g. with `file` or by checking the `Content-Type`).

## 5. Generation log: `metadata.json`

- Keep a `metadata.json` in each folder that holds saved images. Add one entry per image, and never remove existing entries.
- Each entry records:

```json
{
  "file": "camping-gear-01.png",
  "tool": "higgsfield",
  "model": "z_image",
  "prompt": "...",
  "job_id": "5f756190-...",
  "raw_url": "https://...",
  "credits": 1.0,
  "created_at": "2026-10-26"
}
```

- Use JSON, not Markdown, so no translation file is needed.
- For the blog folder layout, `metadata.json` sits in `images/` next to the images.

## 6. Safety

- Never overwrite an existing file. If a name is taken, use the next number.
- Delete files only with the user's consent.
- These rules do not override the CLAUDE.md workflow. Report the todo list and get approval before generating or saving.
