---
name: mk-xls
description: 이 프로젝트에서 openpyxl로 Excel(.xlsx) 통합 문서를 만들거나 수정한다. 사용자가 스프레드시트, Excel 파일, 내려받을 데이터 표, 엑셀 / 스프레드시트 / 표 정리를 요청하거나, 자료조사 수치나 보고서 데이터를 통합 문서로 만들고 싶어 하거나, 이 프로젝트에 있는 기존 .xlsx 파일을 읽거나 수정하거나 확인하려 할 때는 "openpyxl"이라고 말하지 않더라도 항상 이 스킬을 사용한다.
---

# mk-xls

openpyxl을 쓰는 Python 빌드 스크립트를 작성하고 실행한 뒤, 결과 파일을 다시 읽어 확인하는 방식으로 이 프로젝트의 `.xlsx` 파일을 만들고 수정한다.

## 환경

- 이 사용자 계정에 Python 3.13과 openpyxl 3.1.5가 전역으로 설치되어 있다.
- 오래된 셸에서는 `python`이 PATH에 없을 수 있다. `python --version`이 실패하면 전체 경로를 쓴다:
  - PowerShell: `& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"`
  - Bash: `"$LOCALAPPDATA/Programs/Python/Python313/python.exe"`
- Windows 콘솔 코드 페이지 때문에 `print()` 출력의 한글이 깨진다(파일 자체는 정상이다). 출력을 읽어야 하는 스크립트를 실행할 때는 `PYTHONIOENCODING=utf-8`을 설정한다.
- 헬퍼를 import해도 스킬 폴더에 `__pycache__/`가 남지 않도록 Python을 `-B` 옵션으로 실행한다.
- 헬퍼 함수는 `.claude/skills/mk-xls/scripts/xlsx_helpers.py`에 있다. 빌드 스크립트마다 코드를 복사하지 말고, 그 폴더를 `sys.path`에 추가해 import한다(아래 템플릿 참고).

## 파일 위치

| 무엇 | 위치 | 이름 |
|------|------|------|
| 빌드 스크립트 | `scripts/` | `build_<주제>_xlsx.py` (영어, snake_case) |
| 결과 통합 문서 | `sheets/` | 한국어 제목, 예: `AI_투자_현황.xlsx` |

- 기존 통합 문서를 덮어쓰지 않는다. 바꾸려면 빌드 스크립트를 수정하고 새 이름으로 저장한 뒤(`_2026-10-15` 같은 날짜를 붙이거나, `next_available_path()`가 `_2`, `_3`, ...을 붙이게 한다) 사용자에게 새 이름을 알린다. 이전 통합 문서는 사용자가 동의할 때만 `archive/sheets/`로 옮긴다.
- 사용자가 따로 요청하지 않으면 시트 이름, 머리글, 레이블은 한국어로 쓴다.
- 데이터를 `research/`의 자료조사 노트에서 가져올 때는 수치를 노트에 있는 그대로 쓴다. 통합 문서는 노트 없이 따로 돌아다니므로, 출처와 2차 자료 수치의 "참고치" 표시를 `출처` 열이나 메모 시트에 넣는다.

## 작업 흐름

1. **통합 문서 구성 계획.** 시트 목록(시트 이름, 열, 대략적인 행 수, 수식, 차트)을 작성해 사용자에게 보고하는 todo list에 넣는다. 그래야 사용자가 빌드 전에 구성을 승인할 수 있다.
2. **빌드 스크립트 작성.** 아래 템플릿으로 `scripts/`에 작성한다. 시트마다 함수를 하나씩 두면 나중에 고치기 쉽다.
3. **실행**하고 오류를 고친다.
4. **통합 문서를 다시 읽어 검증한다.** openpyxl로 시트 이름, 머리글 행, 행 수, 일부 값, 표시 형식, 표, 그리고 모든 수식이 제자리에 있는지(`list_formulas`) 확인한다. 무엇을 확인했는지 보고한다. 수식 결과는 여기서 확인할 수 없고(제한 사항 참고) 렌더링된 시트도 볼 수 없으므로, 그 사실을 말하고 사용자에게 Excel에서 파일을 열어 보라고 권한다.

## 빌드 스크립트 템플릿

```python
"""Build sheets/<workbook>.xlsx. Run: python -B scripts/build_<topic>_xlsx.py"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "mk-xls" / "scripts"))

from openpyxl import Workbook
from xlsx_helpers import write_table, autofit_columns, apply_font, next_available_path

OUT = next_available_path(ROOT / "sheets" / "<통합문서_이름>.xlsx")

def build_summary(wb):
    ws = wb.active
    ws.title = "요약"
    headers = ["항목", "금액", "비율"]
    rows = [["가", 1200, 0.4], ["나", 1800, 0.6]]
    write_table(ws, headers, rows, number_formats={"금액": "#,##0", "비율": "0.0%"},
                as_table="SummaryTable")
    ws["A5"], ws["B5"] = "합계", "=SUM(B2:B3)"

def main():
    wb = Workbook()
    build_summary(wb)
    apply_font(wb)                    # after all cells are written
    for ws in wb.worksheets:
        autofit_columns(ws)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    print(f"saved {OUT}")

if __name__ == "__main__":
    main()
```

## 헬퍼 (`scripts/xlsx_helpers.py`)

| 함수 | 존재 이유 |
|------|-----------|
| `write_table(ws, headers, rows, start_row=1, start_col=1, number_formats=None, header_fill="1F4E79", as_table=None, freeze=True, borders=True)` | 서식 있는 머리글, 데이터, 테두리, 열별 표시 형식, 머리글 틀 고정, 그리고 엑셀 표(`as_table="Name"`) 또는 일반 자동 필터 중 하나를 적용한다. `"A1:C4"` 같은 범위를 돌려준다. |
| `add_excel_table(ws, ref, name, style="TableStyleMedium2")` | 기존 범위에 엑셀 표를 만든다. 머리글 셀은 서로 다른 문자열이어야 하고, 이름은 통합 문서 안에서 고유하고 공백이 없어야 한다. |
| `autofit_columns(ws, min_width=8, max_width=60)` | openpyxl에는 자동 맞춤이 없다. 한글을 2칸으로 세어 열 너비를 추정한다. |
| `apply_font(wb, name="맑은 고딕")` | 비어 있지 않은 모든 셀에 글꼴을 지정하고 크기, 굵기, 색은 유지한다. 데이터를 다 쓴 뒤 호출한다. |
| `list_formulas(ws)` | `(좌표, 수식)` 목록을 돌려준다. openpyxl은 수식을 계산하지 않으므로 이것으로 수식을 검증한다. |
| `next_available_path(path)` | 비어 있는 파일 이름을 돌려줘 기존 결과물을 덮어쓰지 않게 한다. |

같은 범위에 시트 자동 필터와 엑셀 표를 함께 두지 않는다. 그러면 Excel이 파일이 손상되었다고 보고하기 때문에 `write_table`은 둘 중 하나만 적용한다.

## openpyxl로 할 수 있는 작업

시트에 아래 기능이 필요하면 `references/openpyxl-api.md`에서 코드 예제를 읽는다:

- 통합 문서: 새로 만들기/열기/저장, 템플릿, 속성, 이름 정의, 통합 문서 보호
- 시트: 만들기/복사/삭제/이름 변경/순서 변경, 차트 시트, 탭 색상, 숨기기, 틀 고정, 확대/축소, 눈금선, 시트 보호
- 셀: 값(숫자, 텍스트, 날짜, 불리언), `append`, 범위 순회, 행/열 삽입·삭제, 범위 이동, 병합, 너비/높이, 숨기기/그룹화
- 수식: 수식 문자열, 배열 수식, `data_only=True`로 저장된 결과 읽기
- 서식: 글꼴, 채우기, 테두리, 맞춤, 표시 형식, 셀 보호, 이름 있는 스타일
- 조건부 서식: 셀 값/수식 규칙, 색조, 데이터 막대, 아이콘 집합
- 데이터 도구: 데이터 유효성 검사(드롭다운, 범위), 자동 필터, 엑셀 표
- 차트: 막대/세로 막대, 선, 원, 도넛, 영역, 분산형, 거품형, 방사형, 주식형, 표면형. 축, 제목, 범례, 레이블, 보조 축, 결합 차트
- 이미지, 메모, 하이퍼링크
- 인쇄 설정: 용지, 방향, 여백, 인쇄 영역, 인쇄 제목, 머리글/바닥글, 페이지 나누기, 한 페이지에 맞추기
- 대용량 파일: 읽기는 `read_only=True`, 쓰기는 `write_only=True`

## 제한 사항 — 미리 사용자에게 알린다

요청에 아래 기능이 필요하면 조용히 빼지 말고 todo list에 그 사실을 적고 우회 방법을 제안한다:

| 제한 | 대응 |
|------|------|
| 수식이 계산되지 않음 | Excel이나 LibreOffice에서 열어 저장하기 전까지 파일에는 결과 없이 수식만 있다. 값을 지금 알아야 한다면(보고하거나 다른 곳에 쓰려면) Python으로 계산해 숫자를 쓰거나, 수식과 함께 Python으로 계산한 검증값을 메모 열에 쓴다. |
| 기존 파일을 다시 저장하면 차트, 이미지, 도형, 슬라이서, 스파크라인이 사라질 수 있음 | 사용자의 통합 문서를 직접 수정하지 않는다. 불러온 뒤 결과를 새 파일로 저장하고, 사라질 수 있는 항목을 사용자에게 알린다. 필요하면 차트를 코드로 다시 만든다. |
| 구형 `.xls` | 지원하지 않는다. 사용자에게 `.xlsx`로 저장해 달라고 요청한다. |
| 피벗 테이블 | 불러오고 저장할 때 보존되지만 만들거나 편집할 수 없다. 대신 Python으로 요약 표를 만든다. |
| 매크로(VBA) | `.xlsm`을 `keep_vba=True`로 열면 보존되지만 실행하거나 편집할 수 없다. |
| 필터와 정렬 | `auto_filter`는 필터·정렬 설정만 기록하고 행을 숨기거나 순서를 바꾸지 않는다. 쓰기 전에 Python으로 행을 정렬한다. |
| PDF나 이미지로 렌더링 | Excel이나 LibreOffice 없이는 불가능하다. 파일을 다시 읽어 검증한다. |
