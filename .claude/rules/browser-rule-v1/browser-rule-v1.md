# Browser Control Rules (v1)

These rules apply whenever a task involves controlling a web browser in this project: opening pages, clicking, typing, filling forms, taking screenshots, or reading pages that need a real browser.

## 0. Scope and tool

- Use the Playwright MCP tools (`mcp__playwright__*`) for browser control.
- Load the tool schemas with ToolSearch (e.g. `select:mcp__playwright__browser_navigate,mcp__playwright__browser_snapshot`) before the first call.

## 1. Trigger keywords: use Playwright without asking

If the user's request contains any of the following phrases, or a phrase with the same meaning, use Playwright MCP for the task without asking which tool to use:

- "브라우저를 열어서 작업" / "브라우저 열어" / "브라우저로"
- "웹 제어" / "웹을 제어해"
- "직접 작업" / "직접 들어가서" / "직접 해줘"
- "사이트에 접속해서"
- English equivalents such as "open the browser", "control the web", "do it directly in the browser"

## 2. No trigger keyword: ask first

If the request has no trigger keyword, but Playwright MCP could do the task or do it better, do not call it yet. First ask the user, for example: "Playwright로 브라우저를 열어 작업해도 될까요?" Call it only after the user agrees.

- Typical cases: pages that need a login, pages rendered by JavaScript, tasks that need screenshots, and blog editor work (e.g. Naver blog drafts in `blog/`).
- Consent covers only the task it was given for. Ask again for a new task.
- For simple lookups, prefer WebSearch or WebFetch when they are enough, and do not ask about Playwright.

## 3. Precedence and safety

- These rules do not override the CLAUDE.md workflow. A trigger keyword decides only which tool to use. The todo list must still be reported and approved before execution.
- Before any action that is hard to undo or visible to others (payment, publishing a post, sending a message, changing account settings), confirm with the user right before doing it.
- Never type passwords or other credentials yourself. Ask the user to enter them in the browser.
- Close the browser with `mcp__playwright__browser_close` when the task is finished.
