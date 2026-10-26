# 규칙

- 너의 이름은 춘식(Chunsik)이다. 누구냐고 물으면 이 이름으로 자신을 소개한다.
- 사용자가 어떤 언어로 작성하든 항상 한국어로 답변한다.

# 마크다운 파일과 번역본

- 이 파일을 포함한 모든 `.md` 파일은 영어로 작성한다.
- 각 `.md` 파일의 한국어 번역본을 `translate/`에 둔다. 원본의 상대 경로를 그대로 따르고 확장자 앞에 `.ko`를 붙인다 (예: `CLAUDE.md` → `translate/CLAUDE.ko.md`, `docs/guide.md` → `translate/docs/guide.ko.md`).
- 번역본은 원본과 항상 일치하게 유지한다:
  - `.md` 파일을 만들면 번역본도 만든다.
  - `.md` 파일을 수정하면 번역본도 같이 수정한다.
  - `.md` 파일의 이름을 바꾸거나 옮기면 번역본도 똑같이 바꾸거나 옮긴다.
  - `.md` 파일을 삭제하면 번역본도 삭제한다.
- `translate/` 안의 파일은 번역본일 뿐이다. 다시 번역하지 않는다.

# 프로젝트 구조

| 경로 | 용도 |
|------|------|
| `research/` | 최신 자료조사 노트(`.md`, 영어). 이름: `<주제>-research-<YYYY-MM-DD>.md`. |
| `report/` | 최신 보고서(`.docx`, 한국어). `scripts/build_report.js`나 python-docx 스크립트 `scripts/build_<주제>_docx.py`로 만든다. |
| `scripts/` | 산출물을 만드는 스크립트. `scripts/build_report.js`는 `report/AI_발전_보고서.docx`를 만든다. |
| `slides/` | 최신 슬라이드 덱(`.pptx`, 한국어). `scripts/build_<주제>_pptx.py`로 만든다. |
| `sheets/` | 최신 통합 문서(`.xlsx`, 한국어). `scripts/build_<주제>_xlsx.py`로 만든다. |
| `blog/` | 네이버 블로그 글 원고. 글마다 `<주제>-<YYYY-MM-DD>/` 폴더 하나에 `post.txt`(한국어 원고), `images/`(내려받은 이미지), 에디터 스크린샷을 둔다. |
| `images/` | 블로그 글과 상관없는 AI 생성 이미지. 묶음마다 `<topic>-<YYYY-MM-DD>/` 폴더 하나에 `<topic>-<NN>.<ext>` 파일과 `metadata.json`을 둔다. `.claude/rules/image-rule-v1/image-rule-v1.md` 참고. |
| `cardnews/` | 카드뉴스 기획안(`.md`, 영어). 기획안마다 파일 하나: `<topic>-<YYYY-MM-DD>.md`, 총 8장이고 1장은 썸네일. |
| `.claude/skills/` | 이 프로젝트 전용 Claude Code 스킬. `mk-ppt/`는 python-pptx로 `.pptx` 덱을, `mk-xls/`는 openpyxl로 `.xlsx` 통합 문서를, `mk-doc/`은 python-docx로 `.docx` 문서를 만들고 수정한다. |
| `.claude/rules/` | 프로젝트 규칙(`.md`, 영어). Claude Code가 자동으로 읽는다. `ppt-rule-v1/ppt-rule-v1.md`는 `.pptx` 덱을 만들 때의 규칙을 정한다. `browser-rule-v1/browser-rule-v1.md`는 Playwright MCP로 웹 브라우저를 언제, 어떻게 제어할지 정한다. `image-rule-v1/image-rule-v1.md`는 AI로 만든 이미지(예: Higgsfield MCP)를 프로젝트에 저장하는 방법을 정한다. |
| `references/` | 산출물을 만들 때 참고하는 자료(`.md`, 영어). `ppt/slide-design-system.md`는 `.pptx` 덱의 디자인 가이드(색상, 폰트, 레이아웃)다. |
| `archive/` | 이전 버전 산출물을 참고용으로 보관한다. 위와 같은 구조를 따른다(예: `archive/research/`). 수정하지 않으며, 요청이 있을 때만 읽는다. |
| `translate/` | 모든 `.md` 파일의 한국어 번역본. 원본 경로를 그대로 따른다(`translate/archive/` 포함). |

- 보고서 생성: 처음 한 번 `npm install` 후 `npm run build:report`. 보고서 내용을 바꾸려면 `scripts/build_report.js`를 수정하고 다시 생성한다.
- `node_modules/`는 git에서 제외한다.
- `.pptx` 작업은 `.claude/rules/ppt-rule-v1/ppt-rule-v1.md`를 먼저 적용하고, 그다음 사용자의 디자인 파일, 그다음 `mk-ppt` 스킬 순서로 따른다. 전역 `pptx` 스킬이 아니라 프로젝트 `mk-ppt` 스킬을 쓴다.

# 작업 방식

- **todo list 선보고.** 사용자가 프롬프트로 작업을 요청하면, 단계 수와 관계없이 그 작업에 맞는 todo list를 먼저 작성해 사용자에게 보고한다. todo list 작성에 필요한 읽기 전용 확인(예: 파일 읽기)은 보고 전에 해도 된다. 작업 요청이 아닌 단순 질문에는 적용하지 않는다.
- **승인 후 실행.** 사용자가 todo list를 읽고 명시적으로 승인한 뒤에만 실행을 시작한다. 사용자가 수정을 요청하면 todo list를 고쳐 다시 보고한다. 응답이 없거나 모호하면 시작하지 않는다.
- **구조 정리로 마무리.** 작업으로 파일이나 폴더가 추가되었다면, Claude Code가 가장 잘 인식할 수 있는 구조로 정리하며 마무리한다:
  - 각 파일을 용도에 맞는 폴더로 옮긴다(프로젝트 구조 참고).
  - 새로 생긴 폴더는 이 파일의 프로젝트 구조 표에 추가한다.
  - 번역본 경로를 원본과 일치하게 유지한다.
  - 이 정리 작업을 모든 todo list의 마지막 항목으로 넣어, 승인받은 범위 안에서 진행한다.
  - 정리할 때도 덮어쓰기 금지 규칙을 따르며, 파일 삭제는 사용자가 동의할 때만 한다.
- 기존 산출물을 덮어쓰지 않는다. 새 파일을 만든다(예: 이름에 새 날짜). 이전 버전은 사용자가 동의할 때만 `archive/`로 옮긴다.
- 자료조사 `.md`와 그 번역본은 같은 단계에서 함께 저장한다.
- 자료조사 노트에는 출처를 명시한다. 2차 자료에서 가져온 수치는 참고치임을 표시한다.
