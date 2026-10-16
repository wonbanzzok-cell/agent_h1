---
name: mk-ppt
description: 이 프로젝트에서 python-pptx로 PowerPoint(.pptx) 덱을 만들거나 수정한다. 사용자가 슬라이드, PPT, 프레젠테이션, 덱, 발표 자료 / 슬라이드 / 피피티를 요청하거나, 자료조사 노트나 보고서를 슬라이드로 만들고 싶어 하거나, 이 프로젝트에 있는 기존 .pptx 파일을 수정·확인하거나 내용을 추출하려 할 때는 "python-pptx"라고 말하지 않더라도 항상 이 스킬을 사용한다.
---

# mk-ppt

python-pptx를 쓰는 Python 빌드 스크립트를 작성하고 실행한 뒤, 결과 파일을 다시 읽어 확인하는 방식으로 이 프로젝트의 `.pptx` 파일을 만들고 수정한다.

## 먼저 읽기: PPT 규칙이 우선한다

- `.pptx` 작업을 시작하기 전에 `.claude/rules/ppt-rule-v1/ppt-rule-v1.md`(자동으로 로드됨)를 적용한다. 이 스킬과 규칙 파일이 충돌하면 규칙 파일을 따른다.
- 우선순위: **규칙 파일 → 사용자의 디자인 파일(예: `references/ppt/slide-design-system.md`) → 이 스킬**. 디자인 파일이 규칙 파일의 최솟값(글자 크기, 여백, 간격)보다 낮출 수는 없다.
- 아래의 핑크 테마(`PINK_THEME`, `apply_pink_theme`)와 `Noto Sans KR` 글꼴은 대체 기본값이다. 사용자가 디자인 파일 없이 진행하라고 할 때만 쓴다.

## 환경

- 이 사용자 계정에 Python 3.13과 python-pptx 1.0.2가 전역으로 설치되어 있다.
- 오래된 셸에서는 `python`이 PATH에 없을 수 있다. `python --version`이 실패하면 전체 경로를 쓴다:
  - PowerShell: `& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"`
  - Bash: `"$LOCALAPPDATA/Programs/Python/Python313/python.exe"`
- Windows 콘솔 코드 페이지 때문에 `print()` 출력의 한글이 깨진다(파일 자체는 정상이다). 출력을 읽어야 하는 스크립트를 실행할 때는 `PYTHONIOENCODING=utf-8`을 설정한다(PowerShell은 `$env:PYTHONIOENCODING="utf-8"`, Bash는 명령 앞에 붙인다).
- 헬퍼 함수는 `.claude/skills/mk-ppt/scripts/pptx_helpers.py`에 있다. 빌드 스크립트마다 코드를 복사하지 말고, 그 폴더를 `sys.path`에 추가해 import한다(아래 템플릿 참고).

## 파일 위치

| 무엇 | 위치 | 이름 |
|------|------|------|
| 빌드 스크립트 | `scripts/` | `build_<주제>_pptx.py` (영어, snake_case) |
| 결과 덱 | `slides/` | 한국어 제목, 예: `AI_발전_발표.pptx` |

- 기존 덱을 덮어쓰지 않는다. 덱을 바꾸려면 빌드 스크립트를 수정하고 결과를 새 이름으로 저장한 뒤(`_2026-10-15` 같은 날짜를 붙이거나, 헬퍼의 `next_available_path()`가 `_2`, `_3`, ...을 붙이게 한다) 사용자에게 새 이름을 알린다. 이전 덱은 사용자가 동의할 때만 `archive/slides/`로 옮긴다.
- 사용자가 따로 요청하지 않으면 덱의 텍스트는 `report/`의 보고서처럼 한국어로 쓴다.
- 내용을 `research/`의 자료조사 노트에서 가져올 때는 수치를 노트에 있는 그대로 쓰고, 2차 자료 수치에 붙은 "참고치" 표시도 유지한다.

## 작업 흐름

1. **디자인 파일 확보.** 사용자가 준 디자인 `.md`를 읽는다. 받지 못했다면 요청하고, 사용자가 디자인 파일 없이 진행하라고 할 때만 대체 기본값을 쓴다.
2. **덱 구성 계획.** 사용자가 따로 요청하지 않으면 8장으로 만든다. 짧은 슬라이드 개요(슬라이드별 제목 + 핵심 내용)를 작성해 사용자에게 보고하는 todo list에 넣는다. 그래야 사용자가 빌드 전에 구성을 승인할 수 있다. 내용이 다 들어가지 않으면 그렇다고 말하고 슬라이드 분할이나 내용 축소를 제안한다.
3. **빌드 스크립트 작성.** 먼저 그리드 위에 각 요소의 위치를 정한 뒤, 아래 템플릿으로 `scripts/`에 작성한다. 슬라이드마다 함수를 하나씩 두면 나중에 고치기 쉽다.
4. **실행**하고 오류를 고친다.
5. **덱을 다시 읽어 검증한다.** python-pptx로 슬라이드 수, 각 슬라이드 제목, 계획한 자리에 표·차트·이미지가 있는지, 한글 텍스트에 한글 글꼴이 적용됐는지 확인한다. 규칙 파일의 검사도 함께 한다: 모든 도형이 슬라이드 안에 있는지, 의도하지 않은 겹침이 없는지, 상자를 넘칠 것 같은 텍스트가 없는지. 문제가 없어질 때까지 고치고 다시 검사한다.
6. **보고.** 무엇을 확인했는지, 어떤 디자인 규칙을 적용했는지, 어디서 왜 벗어났는지 보고한다. 렌더링된 슬라이드는 볼 수 없으므로 레이아웃이 괜찮다고 단정하지 말고 그 사실을 말한 뒤, 사용자에게 PowerPoint에서 파일을 열어 확인해 달라고 요청한다.

## 빌드 스크립트 템플릿

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

## 헬퍼 (`scripts/pptx_helpers.py`)

| 함수 | 존재 이유 |
|------|-----------|
| `new_presentation(template=None, widescreen=True)` | 새 덱 또는 템플릿 기반 덱. 기본값은 16:9다(python-pptx 기본값은 4:3). |
| `add_title_slide(prs, title, subtitle=None)` | 레이아웃 0으로 제목 슬라이드를 만든다. |
| `add_bullet_slide(prs, title, items)` | 글머리 기호 목록. 항목은 `"text"` 또는 `("text", level)`이다. |
| `set_font(font, name=None, size=None, bold=None, color=None)` | `font`는 `run.font` 또는 `paragraph.font`다. 영문 글꼴과 동아시아 글꼴을 모두 설정한다. `font.name`만으로는 한글 텍스트가 바뀌지 않는다. `color`는 `"1F4E79"` 같은 16진수다. |
| `apply_korean_font(prs, name="Noto Sans KR")` | 모든 도형, 그룹, 표의 모든 run에 한글 글꼴을 적용한다(차트 제외). |
| `PINK_THEME` | 분홍 팔레트 dict(16진수): `background`, `primary`(제목), `secondary`(막대), `accent`, `text`(본문). |
| `set_slide_background(slide, color)` | 16진수 색으로 배경을 단색으로 채운다. |
| `add_accent_bar(slide, prs, color=PINK_THEME["secondary"], top=..., height=...)` | 가로 전체 폭의 얇은 막대. 기본 위치는 제목 바로 아래다. |
| `apply_pink_theme(prs, theme=PINK_THEME, font="Noto Sans KR")` | 모든 슬라이드에 분홍 배경, 굵은 분홍 제목, 회색 본문, 테마 글꼴을 적용한다. 내용을 모두 추가한 뒤 호출한다. |
| `delete_slide(prs, slide)` | 공식 API가 없다. |
| `duplicate_slide(prs, slide)` | 공식 API가 없다. 도형, 배경, 이미지/링크 관계를 복사한다. 노트는 복사하지 않으며, 복사된 차트는 원본과 데이터를 공유하므로 차트는 새로 만든다. |
| `move_slide(prs, slide, new_index)` | 순서 변경용 공식 API가 없다. |
| `next_available_path(path)` | 비어 있는 파일 이름을 돌려줘 기존 결과물을 덮어쓰지 않게 한다. |

## python-pptx로 할 수 있는 작업

슬라이드에 아래 기능이 필요하면 `references/python-pptx-api.md`에서 코드 예제를 읽는다:

- 파일: 새로 만들기/열기/저장, 템플릿 기반 덱, 슬라이드 크기, 문서 속성
- 슬라이드: 레이아웃으로 추가, 마스터/레이아웃 목록, 단색 배경, 발표자 노트
- 텍스트: placeholder, 텍스트 상자, 문단/run 서식, 정렬, 간격, 수준, 자동 맞춤, 하이퍼링크
- 도형: 기본 도형, 연결선, 자유형, 채우기/선, 그룹, 클릭 동작
- 이미지와 미디어: 이미지 삽입/자르기, 동영상 삽입(실험적), 이미지 추출
- 표: 추가, 셀 텍스트/서식/채우기, 병합, 열 너비, 스타일 옵션
- 차트: 막대/세로 막대, 선, 원/도넛, 영역, 분산형(XY), 거품형, 방사형. 축, 범례, 레이블. 데이터 교체
- 읽기: 슬라이드/도형/텍스트 순회, 표와 차트 데이터 읽기, XML 직접 접근

## 제한 사항 — 미리 사용자에게 알린다

요청에 아래 기능이 필요하면 조용히 빼지 말고 todo list에 그 사실을 적고 우회 방법을 제안한다:

| 지원하지 않음 | 대응 |
|---------------|------|
| 슬라이드 삭제 / 복제 / 순서 변경 | 위의 헬퍼를 쓴다. |
| 애니메이션, 화면 전환 | 불가능하다. 사용자가 PowerPoint에서 추가한다. |
| PDF나 이미지로 렌더링, 미리보기 | PowerPoint나 LibreOffice 없이는 불가능하다. 파일을 다시 읽어 검증한다. |
| SmartArt, 구형 `.ppt` | 불가능하다. 도형과 연결선으로 다이어그램을 만들거나, 사용자에게 `.pptx`로 저장해 달라고 요청한다. |
| 그림 채우기, 3D 효과, 일부 고급 서식 | 제한적이다. 단색/그라데이션 채우기를 쓰거나 원하는 모양이 이미 들어 있는 템플릿을 쓴다. |
