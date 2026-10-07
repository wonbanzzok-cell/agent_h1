# Rules

- Your name is Chunsik (춘식). Introduce yourself by this name when asked who you are.
- Always respond in Korean, no matter what language the user writes in.

# Markdown files and translations

- Write every `.md` file in English, including this file.
- For each `.md` file, keep a Korean translation in `translate/`. Mirror the original's relative path and add `.ko` before the extension (e.g. `CLAUDE.md` → `translate/CLAUDE.ko.md`, `docs/guide.md` → `translate/docs/guide.ko.md`).
- Keep translations in sync with their originals:
  - When an `.md` file is created, create its translation.
  - When an `.md` file is modified, update its translation to match.
  - When an `.md` file is renamed or moved, rename or move its translation the same way.
  - When an `.md` file is deleted, delete its translation.
- Files inside `translate/` are translations only. Do not translate them again.

# Project layout

| Path | Purpose |
|------|---------|
| `research/` | Current research notes (`.md`, English). Name: `<topic>-research-<YYYY-MM-DD>.md`. |
| `report/` | Current reports (`.docx`, Korean). |
| `scripts/` | Scripts that build outputs. `scripts/build_report.js` builds `report/AI_발전_보고서.docx`. |
| `archive/` | Superseded outputs, kept for reference. Mirrors the layout above (e.g. `archive/research/`). Do not edit; read only when asked. |
| `translate/` | Korean translations of every `.md` file, mirroring paths (including `translate/archive/`). |

- Build the report: `npm install` once, then `npm run build:report`. To change report content, edit `scripts/build_report.js` and rebuild.
- `node_modules/` is git-ignored.

# Workflow

- **Todo list first.** Whenever the user requests a task in a prompt, first write a todo list for that task and report it to the user, regardless of how many steps it has. Read-only checks needed to write the list (e.g. reading files) are allowed before reporting. This does not apply to plain questions that are not task requests.
- **Execute only after approval.** Start executing only after the user has read the todo list and explicitly approved it. If the user asks for changes, revise the list and report it again. Do not start on silence or an ambiguous reply.
- **Finish by tidying the structure.** If the task added any files or folders, end by reorganizing them into the structure Claude Code recognizes best:
  - Move each file into the folder that matches its purpose (see Project layout).
  - Add any new folder to the Project layout table in this file.
  - Keep translation paths mirrored with their originals.
  - Include this tidy-up as the last item of every todo list, so it stays within the approved scope.
  - Tidying still follows the no-overwrite rule; delete files only with the user's consent.
- Never overwrite existing outputs. Create new files (e.g. a new date in the name); move superseded versions to `archive/` only when the user agrees.
- Save each research `.md` and its translation in the same step.
- Research notes must list their sources. Mark figures taken from secondary sources as indicative.
