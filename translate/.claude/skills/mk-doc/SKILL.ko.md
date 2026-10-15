---
name: mk-doc
description: 이 프로젝트에서 python-docx로 Word(.docx) 문서를 만들거나 수정한다. 사용자가 Word 파일, .docx, 보고서, 메모, 인쇄하거나 제출할 문서, 문서 / 보고서 / 워드 파일을 요청하거나, 자료조사 노트를 문서로 만들고 싶어 하거나, 이 프로젝트에 있는 기존 .docx를 읽거나 수정하거나 확인하거나 텍스트를 찾아 바꾸려 할 때는 "python-docx"라고 말하지 않더라도 항상 이 스킬을 사용한다.
---

# mk-doc

python-docx를 쓰는 Python 빌드 스크립트를 작성하고 실행한 뒤, 결과 파일을 다시 읽어 확인하는 방식으로 이 프로젝트의 `.docx` 파일을 만들고 수정한다.

## 어떤 도구로 어떤 문서를 만드는가

- `report/AI_발전_보고서.docx`는 `scripts/build_report.js`(Node.js `docx` 라이브러리)가 만든다. 이 스크립트에는 이미 표지, 목차, 페이지 번호가 있다. 이 보고서를 바꾸려면 `build_report.js`를 수정하고 `npm run build:report`를 실행한다. Python으로 옮기지 않는다.
- 새 문서를 만들 때와 기존 `.docx`를 읽거나 수정할 때는 python-docx를 쓴다(둘 중 파일을 열 수 있는 것은 python-docx뿐이다).

## 환경

- 이 사용자 계정에 Python 3.13과 python-docx 1.2.0이 전역으로 설치되어 있다. `docx`로 import한다.
- 오래된 셸에서는 `python`이 PATH에 없을 수 있다. `python --version`이 실패하면 전체 경로를 쓴다:
  - PowerShell: `& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"`
  - Bash: `"$LOCALAPPDATA/Programs/Python/Python313/python.exe"`
- Windows 콘솔 코드 페이지 때문에 `print()` 출력의 한글이 깨진다(파일 자체는 정상이다). 출력을 읽어야 하는 스크립트를 실행할 때는 `PYTHONIOENCODING=utf-8`을 설정한다.
- 헬퍼를 import해도 스킬 폴더에 `__pycache__/`가 남지 않도록 Python을 `-B` 옵션으로 실행한다.
- 헬퍼 함수는 `.claude/skills/mk-doc/scripts/docx_helpers.py`에 있다. 빌드 스크립트마다 코드를 복사하지 말고, 그 폴더를 `sys.path`에 추가해 import한다(아래 템플릿 참고).

## 파일 위치

| 무엇 | 위치 | 이름 |
|------|------|------|
| 빌드 스크립트 | `scripts/` | `build_<주제>_docx.py` (영어, snake_case) |
| 결과 문서 | `report/` | 한국어 제목, 예: `AI_정책_요약.docx` |

- 기존 문서를 덮어쓰지 않는다. 바꾸려면 빌드 스크립트를 수정하거나, 기존 파일을 불러와 결과를 새 이름으로 저장한 뒤(`_2026-10-15` 같은 날짜를 붙이거나, `next_available_path()`가 `_2`, `_3`, ...을 붙이게 한다) 사용자에게 새 이름을 알린다. 이전 문서는 사용자가 동의할 때만 `archive/`로 옮긴다.
- 사용자가 따로 요청하지 않으면 문서의 텍스트는 한국어로 쓴다.
- 내용을 `research/`의 자료조사 노트에서 가져올 때는 수치를 노트에 있는 그대로 쓰고, 2차 자료 수치에 붙은 "참고치" 표시를 유지하며, 출처 절을 넣는다.

## 작업 흐름

1. **문서 구성 계획.** 개요(제목들, 각 제목 아래 들어갈 내용, 표와 이미지)를 작성해 사용자에게 보고하는 todo list에 넣는다. 그래야 사용자가 빌드 전에 구성을 승인할 수 있다.
2. **빌드 스크립트 작성.** 아래 템플릿으로 `scripts/`에 작성한다. 절마다 함수를 하나씩 두면 나중에 고치기 쉽다.
3. **실행**하고 오류를 고친다.
4. **문서를 다시 읽어 검증한다.** python-docx로 제목 순서, 문단과 표 개수, 표 내용, 이미지, 하이퍼링크, 머리글/바닥글 텍스트, 한글 텍스트에 한글 글꼴이 적용됐는지 확인한다. 무엇을 확인했는지 보고한다. 렌더링된 페이지와 페이지 수는 볼 수 없으므로 그 사실을 말하고 사용자에게 Word에서 파일을 열어 보라고 권한다. 문서에 목차가 있으면 Word에서 필드를 업데이트해야 채워진다고 알린다.

## 빌드 스크립트 템플릿

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

## 헬퍼 (`scripts/docx_helpers.py`)

| 함수 | 존재 이유 |
|------|-----------|
| `new_document(template=None, font="맑은 고딕", size=11, a4=True, margin_cm=2.5)` | 기본 템플릿은 US Letter 크기에 테마 글꼴을 쓴다. 이 함수는 A4로 바꾸고 모든 스타일에 한글 글꼴을 적용한다. 템플릿을 쓰면 그 템플릿의 페이지 설정을 유지한다. |
| `set_run_font(run, name=None, size=None, bold=None, color=None)` | `font.name`만으로는 한글 텍스트가 바뀌지 않는다. 이 함수는 `w:eastAsia`도 설정한다. `color`는 `"1F4E79"` 같은 16진수다. |
| `set_style_fonts(doc, name)` | 문서 기본값과 모든 문단/글자 스타일에 한글 글꼴을 넣고, 그 설정을 덮어쓰는 테마 글꼴 연결(제목 스타일이 사용)을 지운다. |
| `apply_korean_font(doc, name="맑은 고딕")` | `set_style_fonts`에 더해 본문, 표, 머리글, 바닥글의 모든 run에 적용한다. |
| `add_hyperlink(paragraph, text, url)` | python-docx는 링크를 읽을 수만 있고 만들 수는 없다. 서식 지정용으로 run을 돌려준다. |
| `add_page_number(section, pattern="{PAGE} / {NUMPAGES}", align=CENTER, header=False)` | 바닥글이나 머리글에 페이지 번호 필드를 넣는다. |
| `add_toc(doc, levels="1-3")` | 제목들로 목차 필드를 만든다. Word에서 필드를 업데이트하기 전까지는 안내 문구가 보이며, 파일을 열 때 Word가 필드 업데이트를 묻도록 설정한다. |
| `add_table(doc, headers, rows, style="Table Grid", header_fill="1F4E79", col_widths_cm=None)` | 배경색이 있는 굵은 머리글 행이 페이지마다 반복되는 표를 만든다. |
| `set_cell_background(cell, color)` | 셀 배경색. python-docx에 API가 없다. |
| `replace_text(doc, old, new)` | 본문, 표, 머리글, 바닥글에서 찾아 바꾼다. Word가 텍스트를 여러 run으로 나눠 놓아도 동작한다. 새 텍스트는 일치가 시작된 run의 서식을 따른다. 바꾼 횟수를 돌려준다. 하이퍼링크 텍스트와 텍스트 상자는 검색하지 않는다. |
| `next_available_path(path)` | 비어 있는 파일 이름을 돌려줘 기존 결과물을 덮어쓰지 않게 한다. |

## python-docx로 할 수 있는 작업

문서에 아래 기능이 필요하면 `references/python-docx-api.md`에서 코드 예제를 읽는다:

- 파일: 새로 만들기/열기/저장, 기존 `.docx`를 템플릿으로 사용, 문서 속성
- 문단과 제목: 추가, 앞에 끼워 넣기, 정렬, 들여쓰기, 간격, 다음 문단과 함께, 페이지 나누기 전 삽입, 탭 정지
- Run: 글꼴, 크기, 굵게/기울임/밑줄/취소선, 색, 형광펜, 위/아래 첨자, 대문자, 숨김
- 스타일: 기본 스타일 적용, 문단/글자/표 스타일 추가나 수정
- 목록: `List Bullet`, `List Number`와 그 2~3단계 변형
- 표: 행/열 추가, 셀 텍스트와 중첩 내용, 병합, 너비, 행 높이, 세로 정렬, 표 스타일과 정렬
- 이미지: 본문, 표 셀, 머리글/바닥글의 인라인 그림
- 페이지와 구역: 페이지/줄 나누기, 새 구역, 용지 크기와 방향, 여백
- 머리글과 바닥글: 텍스트, 이미지, 표. 첫 페이지 다르게. 홀수/짝수 페이지 다르게. 이전 구역과 연결/해제
- 메모(1.2.0): run에 메모 추가, 기존 메모 읽기
- 읽기: 문단과 표를 순서대로 순회(`iter_inner_content`), 하이퍼링크 읽기, 렌더링된 페이지 나눔, XML 직접 접근

## 제한 사항 — 미리 사용자에게 알린다

요청에 아래 기능이 필요하면 조용히 빼지 말고 todo list에 그 사실을 적고 우회 방법을 제안한다:

| 제한 | 대응 |
|------|------|
| 하이퍼링크, 페이지 번호, 목차, 기타 필드 | API가 없다. 헬퍼를 쓴다. 목차와 필드 값은 Word에서 필드를 업데이트한 뒤에만 나타난다. |
| 찾아 바꾸기 | API가 없다. `replace_text`를 쓰고 돌려준 횟수를 확인한다. |
| 각주/미주, 변경 내용 추적, 수식, 텍스트 상자 | 지원하지 않는다. 각주 대신 "출처"나 "주" 절을 쓰고, 나머지는 사용자에게 Word에서 추가해 달라고 요청한다. |
| 떠 있는(텍스트 감싸기) 이미지와 도형 | 인라인 그림만 만들 수 있다. 기존의 떠 있는 개체는 보존된다. |
| 번호 목록 다시 시작, 다단계 번호 제어 | 직접 지원하지 않는다. 번호를 다시 시작해야 하면 "1.", "2."를 텍스트로 쓴 문단을 쓴다. |
| 다단(여러 열) | API가 없고 구역 XML에 `w:cols`가 필요하다. 하기 전에 사용자에게 묻는다. |
| 구형 `.doc`, `.dotx` 템플릿 | `.doc`은 지원하지 않으므로 사용자에게 `.docx`로 저장해 달라고 요청한다. `.dotx`는 `.docx`로 변환해야 python-docx로 열 수 있다. |
| PDF나 이미지로 렌더링, 페이지 수 | Word나 LibreOffice 없이는 불가능하다. 파일을 다시 읽어 검증한다. |
