"""Build slides/AI_발전_발표.pptx from research/ai-development-research-2026-10-07.md.

Design: references/ppt/slide-design-system.md (Orange Business).
Rules:  .claude/rules/ppt-rule-v1/ppt-rule-v1.md (8 slides, no overflow/overlap).

Run: python scripts/build_ai_development_pptx.py
After saving, the script reads the deck back and runs the rule-file layout checks.

Shape names are "<group>:<label>". Shapes in the same group may overlap on purpose
(text on a shape, ring on its track); the group "bg" marks background decoration.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "mk-ppt" / "scripts"))

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt
from pptx_helpers import new_presentation, next_available_path

# `--out <path>` writes elsewhere (e.g. a scratch file while iterating on the layout).
OUT = (Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv
       else next_available_path(ROOT / "slides" / "AI_발전_발표.pptx"))

# -- design tokens (slide-design-system.md §2, §3) -------------------------
ORANGE, LIGHT_OR, PALE_OR, RED_OR = "F26522", "F7A27A", "FDE3D6", "E8432B"
BLACK, DARK, MID, LIGHT, WHITE = "1A1A1A", "444444", "9A9A9A", "EDEDED", "FFFFFF"
KO = "Malgun Gothic"          # Korean body font
EN = "Arial"                  # fallback for Montserrat (not installed)
EN_BLACK = "Arial Black"      # fallback for Montserrat Extra Bold (cover)

SLIDE_W, SLIDE_H = 13.333, 7.5
MARGIN = 0.5
TOTAL = 8
# 3-column grid (§4): column 3.8 in, gutter 0.4 in, centered in the content width
COL_W, GUTTER = 3.8, 0.4
COL_X = [MARGIN + (SLIDE_W - 2 * MARGIN - (3 * COL_W + 2 * GUTTER)) / 2 + i * (COL_W + GUTTER)
         for i in range(3)]
CAPTION_Y = 6.45              # source caption row, above the bottom orange line (7.0)


# -- low-level helpers -----------------------------------------------------

def rgb(hex_):
    return RGBColor.from_string(hex_)


def style_run(run, size, bold=False, italic=False, color=DARK, latin=KO, ea=KO):
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = rgb(color)
    rPr = run._r.get_or_add_rPr()
    for tag, name in (("a:latin", latin), ("a:ea", ea), ("a:cs", latin)):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set("typeface", name)


def fill_text(tf, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, margin=0.05):
    """paras: list of dicts with text, size and optional bold/italic/color/latin/ea/after."""
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Inches(margin))
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = p.get("align", align)
        if p.get("after"):
            para.space_after = Pt(p["after"])
        run = para.add_run()
        run.text = p["text"]
        style_run(run, p["size"], p.get("bold", False), p.get("italic", False),
                  p.get("color", DARK), p.get("latin", KO), p.get("ea", KO))


def P(text, size, **kw):
    return dict(text=text, size=size, **kw)


def textbox(slide, name, x, y, w, h, paras, **kw):
    s = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    s.name = name
    fill_text(s.text_frame, paras, **kw)
    return s


def shape(slide, name, kind, x, y, w, h, fill=None, line=None, line_w=0.75):
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    s.name = name
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = rgb(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(line_w)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def capsule(slide, name, x, y, w, h, fill, paras=None, **kw):
    s = shape(slide, name, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=fill)
    s.adjustments[0] = 0.5
    if paras:
        fill_text(s.text_frame, paras, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                  margin=kw.pop("margin", 0.02), **kw)
    return s


def circle(slide, name, x, y, d, fill, paras=None):
    s = shape(slide, name, MSO_SHAPE.OVAL, x, y, d, d, fill=fill)
    if paras:
        fill_text(s.text_frame, paras, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, margin=0)
    return s


def line(slide, name, x1, y1, x2, y2, color, width_pt):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1),
                                   Inches(x2), Inches(y2))
    c.name = name
    c.line.color.rgb = rgb(color)
    c.line.width = Pt(width_pt)
    return c


def set_geom(s, **vals):
    """Write preset-geometry adjust values (raw OOXML units) into <a:avLst>."""
    av = s._element.spPr.find(qn("a:prstGeom")).find(qn("a:avLst"))
    for gd in list(av):
        av.remove(gd)
    for k, v in vals.items():
        etree.SubElement(av, qn("a:gd"), name=k, fmla=f"val {int(v)}")


def _ang(deg):
    return int((deg % 360) * 60000)


def ring(slide, group, x, y, d, segments, track=LIGHT, thick=12000):
    """Ring chart from shapes. segments: [(fraction, color)], drawn clockwise from 12 o'clock."""
    t = shape(slide, f"{group}:track", MSO_SHAPE.DONUT, x, y, d, d, fill=track)
    set_geom(t, adj=thick)
    start = 0.0
    for i, (frac, color) in enumerate(segments):
        if frac <= 0:
            continue
        if frac >= 0.999:
            s = shape(slide, f"{group}:seg{i}", MSO_SHAPE.DONUT, x, y, d, d, fill=color)
            set_geom(s, adj=thick)
        else:
            s = shape(slide, f"{group}:seg{i}", MSO_SHAPE.BLOCK_ARC, x, y, d, d, fill=color)
            set_geom(s, adj1=_ang(270 + 360 * start), adj2=_ang(270 + 360 * (start + frac)),
                     adj3=thick)
        start += frac


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def header(slide, n, tab, title):
    """Common header (§5) and bottom orange line."""
    capsule(slide, "hdr_tab:tab", MARGIN, 0.45, 1.45, 0.4, ORANGE,
            [P(tab, 14, bold=True, color=WHITE, latin=EN)])
    textbox(slide, "hdr_title:title", 2.15, 0.4, 9.3, 0.55,
            [P(title, 26, bold=True, italic=True, color=BLACK, latin=EN)],
            anchor=MSO_ANCHOR.MIDDLE)
    capsule(slide, "hdr_pill:pill", SLIDE_W - MARGIN - 1.1, 0.5, 1.1, 0.32, BLACK,
            [P(f"{n:02d} / {TOTAL:02d}", 14, bold=True, color=WHITE, latin=EN)])
    line(slide, "hdr_line:line", 2.15, 1.15, SLIDE_W - MARGIN, 1.15, LIGHT, 0.75)
    line(slide, "ftr_line:line", MARGIN, 7.0, SLIDE_W - MARGIN, 7.0, ORANGE, 1)


def caption(slide, text):
    textbox(slide, "caption:src", MARGIN, CAPTION_Y, SLIDE_W - 2 * MARGIN, 0.35,
            [P(text, 14, color=MID)])


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


# -- slides ----------------------------------------------------------------

def slide_cover(prs):
    s = blank(prs)
    # background decoration: faint diagonal lines (top right) and concentric circles (bottom right)
    for i in range(3):
        line(s, f"bg:diag{i}", 10.2 + i * 0.6, 1.3, 11.0 + i * 0.6, 0.5, PALE_OR, 1)
    for i, d in enumerate((1.6, 1.15, 0.7)):
        off = (1.6 - d) / 2
        shape(s, f"bg:ring{i}", MSO_SHAPE.OVAL, 11.0 + off, 5.2 + off, d, d, line=LIGHT, line_w=0.75)
    # orange capsule with white headline (no photo available: solid orange instead)
    capsule(s, "cap:capsule", MARGIN, 0.9, 5.4, 5.0, ORANGE)
    textbox(s, "cap:headline", 0.9, 1.4, 4.6, 4.0, [
        P("AI DEVELOPMENT 2026", 16, bold=True, color=WHITE, latin=EN, after=12),
        P("더 빠르게,", 32, bold=True, color=WHITE),
        P("더 넓게,", 32, bold=True, color=WHITE),
        P("고르지 않게", 32, bold=True, color=WHITE),
    ], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, "title:title", 6.4, 1.6, 6.433, 1.9, [
        P("AI 발전 동향", 54, bold=True, italic=True, color=BLACK, latin=EN_BLACK),
        P("2026", 54, bold=True, italic=True, color=ORANGE, latin=EN_BLACK),
    ])
    textbox(s, "subtitle:sub", 6.4, 3.75, 6.433, 1.2, [
        P("기술 · 에이전트 · 투자 · 노동 · 규제로 본 AI의 현재", 18, color=MID, after=6),
        P("자료조사 노트(2026-10-07) 기반", 14, color=MID),
    ])
    capsule(s, "pill1:pill", MARGIN, 6.3, 1.6, 0.4, ORANGE,
            [P("2026.10", 14, bold=True, color=WHITE, latin=EN)])
    capsule(s, "pill2:pill", 2.3, 6.3, 2.4, 0.4, BLACK,
            [P("RESEARCH BRIEF", 14, bold=True, color=WHITE, latin=EN)])
    notes(s, "AI 발전 동향 2026. 출처: research/ai-development-research-2026-10-07.md")


def slide_agenda(prs):
    s = blank(prs)
    header(s, 2, "CONTENTS", "목차")
    items = [
        ("01", 1 / 3, "기술과 에이전트", "능력은 빠르게 오르지만 고르지 않다 · 챗봇에서 에이전트로"),
        ("02", 2 / 3, "투자와 에너지", "빅테크 설비투자 급증 · 데이터센터 전력 수요 2배"),
        ("03", 1.0, "사회와 제도", "신입 채용 감소 · AI 신약 임상 · 규제와 한국의 대응"),
    ]
    for i, (num, frac, label, desc) in enumerate(items):
        x = COL_X[i]
        g = f"c{i}"
        ring(s, g, x + 0.9, 1.6, 2.0, [(frac, ORANGE)], track=PALE_OR, thick=12000)
        textbox(s, f"{g}:num", x + 1.3, 2.25, 1.2, 0.7,
                [P(num, 32, bold=True, color=ORANGE, latin=EN)],
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, margin=0)
        tri = shape(s, f"t{i}:tri", MSO_SHAPE.ISOSCELES_TRIANGLE, x + 1.7, 3.85, 0.4, 0.25,
                    fill=ORANGE)
        tri.rotation = 180
        textbox(s, f"l{i}:label", x, 4.3, COL_W, 0.5,
                [P(label, 20, bold=True, color=BLACK)], align=PP_ALIGN.CENTER)
        textbox(s, f"d{i}:desc", x, 5.0, COL_W, 1.1,
                [P(desc, 15, color=DARK)], align=PP_ALIGN.CENTER)
    notes(s, "1부 기술과 에이전트(3–4쪽), 2부 투자와 에너지(5쪽), 3부 사회와 제도(6–7쪽), 마무리(8쪽).")


def slide_capability(prs):
    s = blank(prs)
    header(s, 3, "TECH", "기술 역량: 빠르지만 고르지 않다")
    items = [
        ("100%", 0.98, "코딩 능력 급상승",
         "SWE-bench 점수가 1년 만에 약 60%에서 100% 가까이로 상승"),
        ("50.1%", 0.501, "들쭉날쭉한 최전선",
         "IMO 금메달 수준 모델도 아날로그 시계는 50.1%만 정확히 읽음"),
        ("40×", 1.0, "지능 비용 급락",
         "박사급 과학 문제의 GPT-4 수준 성능 비용이 연 약 40배 하락"),
    ]
    for i, (num, frac, label, desc) in enumerate(items):
        x = COL_X[i]
        g = f"r{i}"
        ring(s, g, x + 0.95, 1.4, 1.9, [(frac, ORANGE)], track=LIGHT, thick=12000)
        textbox(s, f"{g}:num", x + 1.2, 1.95, 1.4, 0.8,
                [P(num, 30, bold=True, color=BLACK, latin=EN)],
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, margin=0)
        line(s, f"k{i}:link", x + COL_W / 2, 3.5, x + COL_W / 2, 3.75, MID, 0.75)
        textbox(s, f"l{i}:label", x, 3.95, COL_W, 0.45,
                [P(label, 18, bold=True, color=BLACK)], align=PP_ALIGN.CENTER)
        textbox(s, f"d{i}:desc", x, 4.6, COL_W, 0.85,
                [P(desc, 14, color=DARK)], align=PP_ALIGN.CENTER)
    shape(s, "note:box", MSO_SHAPE.ROUNDED_RECTANGLE, MARGIN, 5.65, SLIDE_W - 2 * MARGIN, 0.6,
          fill=LIGHT).adjustments[0] = 0.2
    capsule(s, "note:tag", 0.7, 5.75, 1.1, 0.4, ORANGE,
            [P("CHECK", 14, bold=True, color=WHITE, latin=EN)])
    textbox(s, "note:text", 2.0, 5.7, 10.6, 0.5,
            [P("미·중 최상위 모델의 성능 격차는 사실상 해소, 2025년 초 이후 선두가 여러 차례 바뀜", 15,
               color=DARK)], anchor=MSO_ANCHOR.MIDDLE)
    caption(s, "※ 2차 요약 자료(Stanford AI Index 2026, Epoch AI) 기반 수치로 추정치임")
    notes(s, "출처: Stanford AI Index 2026 요약(Stark Insider, Burges Salmon, Lumenova), "
             "Epoch AI 추론 가격 추세. 가격 하락 폭은 벤치마크에 따라 연 9배~900배.")


def slide_agents(prs):
    s = blank(prs)
    header(s, 4, "AGENTS", "챗봇에서 에이전트로")
    # featured card (left)
    shape(s, "card:bg", MSO_SHAPE.ROUNDED_RECTANGLE, MARGIN, 1.45, 3.3, 4.75,
          fill=ORANGE).adjustments[0] = 0.12
    textbox(s, "card:label", 0.75, 1.75, 2.8, 0.35,
            [P("KEY FIGURE", 14, bold=True, color=WHITE, latin=EN)])
    textbox(s, "card:num", 0.75, 2.25, 2.8, 0.8,
            [P("51%", 40, bold=True, color=WHITE, latin=EN)], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, "card:text", 0.75, 3.25, 2.8, 0.75,
            [P("에이전트를 실제 운영 중인 기업 비율", 16, bold=True, color=WHITE)])
    textbox(s, "card:sub", 0.75, 4.2, 2.8, 0.9, [
        P("추가 23%는 확대 중", 14, color=WHITE),
        P("62%는 최소 실험 단계", 14, color=WHITE),
    ])
    # three items (middle) with numbered orange circles
    items = [
        ("시장 규모", "2026년 109억 달러 → 2030년 503억 달러 (연평균 약 46%)"),
        ("확산 전망", "2026년 말 기업용 앱의 40%가 업무별 에이전트 탑재 (2025년 5% 미만)"),
        ("리스크", "2027년 말까지 40% 이상 프로젝트 중단 전망 · 보안 정책 보유 44%뿐"),
    ]
    for i, (label, text) in enumerate(items):
        t = 1.5 + i * 1.55
        textbox(s, f"il{i}:label", 4.2, t, 4.4, 0.4,
                [P(label, 18, bold=True, color=BLACK)])
        textbox(s, f"it{i}:text", 4.2, t + 0.6, 4.4, 0.75, [P(text, 14, color=DARK)])
        circle(s, f"ic{i}:icon", 8.8, t + 0.35, 0.6, ORANGE,
               [P(str(i + 1), 16, bold=True, color=WHITE, latin=EN)])
    # large circle (right) in place of a photo
    circle(s, "big:circle", 9.6, 2.2, 3.2, PALE_OR)
    textbox(s, "big:text", 10.0, 3.0, 2.4, 1.6, [
        P("CHATBOT → AGENT", 14, bold=True, color=ORANGE, latin=EN, after=6),
        P("질문에 답하는 AI에서 여러 단계 업무를 계획·실행하는 AI로", 14, color=DARK),
    ], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    caption(s, "※ 시장·도입 수치는 2차 자료(G2, CMARIX, Ringly) 기반 추정치임")
    notes(s, "에이전트 프로젝트의 80%가 의도치 않은 행동(무단 시스템 접근 등)을 보고. "
             "출처: G2 Enterprise AI Agents Report, CMARIX, Ringly.")


def slide_invest(prs):
    s = blank(prs)
    header(s, 5, "INVEST", "투자와 에너지, 새로운 병목")
    groups = [
        (1.45, "빅테크 4사 설비투자", ["2026년 전년 대비 +77%", "2027년 1조 달러 전망"],
         [("2025년 실적", 410, "$410B"), ("2026년 계획", 725, "$725B")]),
        (4.2, "데이터센터 전력", ["2025년 수요 증가율", "전 세계 평균의 5배 이상"],
         [("데이터센터", 17, "+17%"), ("전 세계 전체", 3, "+3%")]),
    ]
    for gi, (top, title, sub, rows) in enumerate(groups):
        textbox(s, f"gl{gi}:label", MARGIN, top, 2.6, 1.45,
                [P(title, 18, bold=True, color=BLACK, after=4)] + [P(t, 14, color=DARK) for t in sub])
        line(s, f"gb{gi}:bracket", 3.3, top + 0.05, 3.3, top + 1.4, ORANGE, 1)
        vmax = max(v for _, v, _ in rows)
        for ri, (lab, v, val) in enumerate(rows):
            y = top + 0.15 + ri * 0.7
            color = ORANGE if ri == 0 else RED_OR
            textbox(s, f"rl{gi}{ri}:label", 3.6, y, 2.4, 0.45,
                    [P(lab, 14, color=DARK)], anchor=MSO_ANCHOR.MIDDLE)
            shape(s, f"rb{gi}{ri}:bar", MSO_SHAPE.ROUNDED_RECTANGLE, 6.2, y + 0.05,
                  5.0 * v / vmax, 0.35, fill=color).adjustments[0] = 0.5
            textbox(s, f"rv{gi}{ri}:value", 11.4, y, 1.43, 0.45,
                    [P(val, 20, bold=True, color=BLACK, latin=EN)],
                    align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    circle(s, "chk:circle", MARGIN, 3.15, 0.85, BLACK,
           [P("CHECK", 14, bold=True, color=WHITE, latin=EN)])
    textbox(s, "chkt:text", 1.6, 3.25, 11.233, 0.65,
            [P("데이터센터 전력 수요는 2030년 약 945 TWh로 2배 이상 증가 전망 (일본의 현재 소비량 초과)",
               16, bold=True, color=BLACK)], anchor=MSO_ANCHOR.MIDDLE)
    caption(s, "※ 설비투자는 실적 발표의 2차 요약 기반 추정치 · 전력 수치는 IEA 전망")
    notes(s, "2026년 설비투자: Amazon 약 2,000억, Microsoft 약 1,900억, Alphabet 1,750–1,850억, "
             "Meta 1,150–1,350억 달러. 출처: Yahoo Finance, AI Weekly, The Next Web, IEA(W.Media, Enlit).")


def slide_society(prs):
    s = blank(prs)
    header(s, 6, "SOCIETY", "노동·과학·안전: 사회로 번지는 영향")
    items = [
        ("01", "−19%", [(0.19, ORANGE)], "노동: 신입 채용부터",
         "AI 노출이 큰 직종의 22–25세 고용, 덜 노출된 또래보다 19% 낮음 · 기업 21%가 신입 채용 동결"),
        ("02", "117", [(0.068, ORANGE), (0.445, LIGHT_OR)], "의료: 임상 후기 진입",
         "AI 신약 후보 117건 임상 진입 · 1상 완료 51.3%, 2상 완료 6.8% · FDA 승인 신약은 아직 없음"),
        ("03", "362", [(233 / 362, LIGHT_OR), (1 - 233 / 362, ORANGE)], "안전: 사고 증가와 규제",
         "AI 사고 233건 → 362건 · EU AI Act 고위험 의무는 2027년 12월로 연기"),
    ]
    for i, (badge, num, segs, label, desc) in enumerate(items):
        x = COL_X[i]
        g = f"d{i}"
        circle(s, f"b{i}:badge", x + (COL_W - 0.55) / 2, 1.4, 0.55, ORANGE,
               [P(badge, 14, bold=True, color=WHITE, latin=EN)])
        ring(s, g, x + 0.9, 2.15, 2.0, segs, track=PALE_OR, thick=13000)
        textbox(s, f"{g}:num", x + 1.25, 2.75, 1.3, 0.8,
                [P(num, 28, bold=True, color=BLACK, latin=EN)],
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, margin=0)
        textbox(s, f"l{i}:label", x, 4.35, COL_W, 0.45,
                [P(label, 18, bold=True, color=BLACK)], align=PP_ALIGN.CENTER)
        textbox(s, f"t{i}:desc", x, 5.0, COL_W, 1.2,
                [P(desc, 14, color=DARK)], align=PP_ALIGN.CENTER)
    caption(s, "※ 2차 요약 자료(Stanford·ADP, ASCO 2026, AI Index 2026, Sidley) 기반 추정치임")
    notes(s, "도넛: ① 고용 격차 19%, ② 117건 중 2상 완료 6.8%(진한 주황)·1상 완료 51.3%(연한 주황 포함), "
             "③ 사고 362건 중 전년 233건(연한 주황)과 증가분(진한 주황). "
             "Insilico의 rentosertib는 2026년 7월 320명 규모 3상 진입.")


def cell_borders(cell, bottom=None):
    """Hide all cell borders except an optional thin bottom divider."""
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        old = tcPr.find(qn(tag))
        if old is not None:
            tcPr.remove(old)
    for idx, tag in enumerate(("a:lnL", "a:lnR", "a:lnT", "a:lnB")):
        color = bottom if tag == "a:lnB" else None
        ln = etree.Element(qn(tag), w=str(9525 if color else 0))
        if color:
            sf = etree.SubElement(ln, qn("a:solidFill"))
            etree.SubElement(sf, qn("a:srgbClr"), val=color)
        else:
            etree.SubElement(ln, qn("a:noFill"))
        tcPr.insert(idx, ln)


def slide_korea(prs):
    s = blank(prs)
    header(s, 7, "KOREA", "한국: 기본법과 대규모 공공투자")
    rows = [
        ("구분", "내용", "시점"),
        ("AI 기본법", "고영향 AI 위험관리와 생성형 AI 결과물 표시 의무, 전면 시행된 첫 포괄적 AI 법", "2026.01 시행"),
        ("GPU 확보", "GPU 26만 장을 단계적으로 확보 (NVIDIA 협력 포함)", "2025.12 계획"),
        ("범용 AI 프로젝트", "1조 원 투입, 세계 10위권 소버린 AI 모델 개발", "2025.12 계획"),
        ("프런티어 모델", "초과 세수 약 5조 원, Vera Rubin GPU 약 1만 장을 선도 1팀에 집중", "2026.07 계획"),
    ]
    widths = [2.8, 7.333, 2.2]
    heights = [0.5] + [0.85] * 4
    gf = s.shapes.add_table(len(rows), 3, Inches(MARGIN), Inches(1.45),
                            Inches(sum(widths)), Inches(sum(heights)))
    gf.name = "table:table"
    tbl = gf.table
    tbl.first_row = False
    tbl.horz_banding = False
    for c, w in enumerate(widths):
        tbl.columns[c].width = Inches(w)
    for r, h in enumerate(heights):
        tbl.rows[r].height = Inches(h)
    for r, row in enumerate(rows):
        hi = r == 1                      # highlighted row
        for c, text in enumerate(row):
            cell = tbl.cell(r, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(ORANGE if hi else WHITE)
            cell_borders(cell, bottom=(BLACK if r == 0 else LIGHT))
            for side in ("left", "right"):
                setattr(cell, f"margin_{side}", Inches(0.15))
            cell.margin_top = cell.margin_bottom = Inches(0.05)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            if r == 0:
                p = P(text, 14, bold=True, color=BLACK)
            elif c == 0:
                p = P(text, 16, bold=True, color=WHITE if hi else BLACK)
            else:
                p = P(text, 15, color=WHITE if hi else DARK)
            tf = cell.text_frame
            tf.word_wrap = True
            para = tf.paragraphs[0]
            para.alignment = PP_ALIGN.CENTER if c == 2 else PP_ALIGN.LEFT
            run = para.add_run()
            run.text = p["text"]
            style_run(run, p["size"], p.get("bold", False), False, p["color"])
    capsule(s, "btn:pill", 9.8, 5.65, 3.033, 0.5, ORANGE,
            [P("선택과 집중 전략", 16, bold=True, color=WHITE)])
    caption(s, "※ 2차 자료(law.asia, 뉴시스, 다음, 위키독스) 기반 정리 · 계획 수치는 발표 당시 기준")
    notes(s, "AI 기본법(인공지능 발전과 신뢰 기반 조성 등에 관한 기본법): 2024년 12월 통과, 2026년 1월 22일 전면 시행. "
             "GPU·범용 AI 계획은 과기정통부 2025년 12월 업무계획, 프런티어 모델 계획은 2026년 7월 보도.")


def slide_closing(prs):
    s = blank(prs)
    capsule(s, "cap:capsule", MARGIN, 0.9, 4.8, 5.6, ORANGE)
    textbox(s, "cap:text", 0.9, 2.3, 4.0, 2.6, [
        P("THANK YOU", 36, bold=True, italic=True, color=WHITE, latin=EN_BLACK, after=6),
        P("감사합니다", 24, bold=True, color=WHITE, after=12),
        P("질문과 의견을 환영합니다", 16, color=WHITE),
    ], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, "kt:label", 5.8, 1.0, 7.033, 0.45,
            [P("KEY TAKEAWAYS", 18, bold=True, color=ORANGE, latin=EN)])
    textbox(s, "kt:title", 5.8, 1.6, 7.033, 0.65,
            [P("핵심 요약", 28, bold=True, italic=True, color=BLACK, latin=EN)])
    items = [
        "능력은 빠르게, 그러나 고르지 않게 성장",
        "챗봇에서 에이전트로, 보안·거버넌스는 뒤처짐",
        "투자와 전력이 새로운 병목",
        "노동 영향은 신입 채용에서 먼저 나타남",
        "규제는 도입 중, 한국은 기본법과 공공투자",
    ]
    for i, text in enumerate(items):
        y = 2.5 + i * 0.8
        circle(s, f"kn{i}:num", 5.8, y + 0.025, 0.5, ORANGE,
               [P(str(i + 1), 14, bold=True, color=WHITE, latin=EN)])
        textbox(s, f"kx{i}:text", 6.5, y, 6.333, 0.55,
                [P(text, 16, color=DARK)], anchor=MSO_ANCHOR.MIDDLE)
    line(s, "ftr_line:line", MARGIN, 7.0, SLIDE_W - MARGIN, 7.0, ORANGE, 1)
    notes(s, "핵심 요약 5가지. 상세 근거는 research/ai-development-research-2026-10-07.md 9절 참조.")


# -- verification (ppt-rule-v1 §3) -----------------------------------------

EMU_IN = 914400
CJK = lambda o: 0xAC00 <= o <= 0xD7A3 or 0x3130 <= o <= 0x318F or 0x4E00 <= o <= 0x9FFF


def text_width(text, size, bold, latin):
    """Rough rendered width in inches (conservative)."""
    em = 0.0
    for ch in text:
        if CJK(ord(ch)):
            w = 1.0
        elif ch == " ":
            w = 0.3
        elif ch.isupper() or ch.isdigit():
            w = 0.66
        elif ch.isascii():
            w = 0.56
        else:
            w = 0.9                      # symbols such as · → − ×
        if latin == EN_BLACK and not CJK(ord(ch)):
            w *= 1.25
        em += w
    return em * size / 72 * (1.06 if bold else 1.0)


def lines_needed(text, size, bold, latin, avail):
    words, lines, cur = text.split(" "), 1, 0.0
    space = text_width(" ", size, bold, latin)
    for w in words:
        ww = text_width(w, size, bold, latin)
        add = ww if cur == 0 else space + ww
        if cur + add <= avail:
            cur += add
        else:
            lines += 1 + int(ww // avail)
            cur = ww % avail
    return lines


def frame_height(tf, avail_w):
    total, info = 0.0, []
    for para in tf.paragraphs:
        runs = para.runs
        if not runs:
            continue
        r = runs[0]
        size = r.font.size.pt
        latin = r._r.rPr.find(qn("a:latin")).get("typeface")
        text = "".join(x.text for x in runs)
        n = lines_needed(text, size, bool(r.font.bold), latin, avail_w)
        total += n * size * 1.2 / 72 + (para.space_after.pt / 72 if para.space_after else 0)
        info.append((text[:20], n))
    return total, info


def verify(path):
    prs = Presentation(path)
    sw, sh = prs.slide_width / EMU_IN, prs.slide_height / EMU_IN
    problems, fonts_ok = [], True
    for si, slide in enumerate(prs.slides, 1):
        boxes = []
        for shp in slide.shapes:
            x, y = shp.left / EMU_IN, shp.top / EMU_IN
            w, h = shp.width / EMU_IN, shp.height / EMU_IN
            name = shp.name
            group = name.split(":")[0]
            # 1) inside the slide, with the 0.4 in edge margin
            if x < 0.4 - 1e-3 or y < 0.4 - 1e-3 or x + w > sw - 0.4 + 1e-3 or y + h > sh - 0.4 + 1e-3:
                problems.append(f"slide {si}: {name} outside margin ({x:.2f},{y:.2f},{w:.2f},{h:.2f})")
            # 2) fonts and text fit
            frames = []
            if shp.has_text_frame and shp.text_frame.text.strip():
                tf = shp.text_frame
                factor = 0.72 if shp.shape_type == 1 and "OVAL" in str(shp.auto_shape_type) else 1.0
                frames.append((tf, w * factor - (tf.margin_left + tf.margin_right) / EMU_IN,
                               h - (tf.margin_top + tf.margin_bottom) / EMU_IN, name))
            if shp.has_table:
                tbl = shp.table
                for r, row in enumerate(tbl.rows):
                    for c, cell in enumerate(row.cells):
                        cw = tbl.columns[c].width / EMU_IN
                        frames.append((cell.text_frame, cw - (cell.margin_left + cell.margin_right) / EMU_IN,
                                       row.height / EMU_IN - (cell.margin_top + cell.margin_bottom) / EMU_IN,
                                       f"{name}[{r},{c}]"))
            for tf, aw, ah, nm in frames:
                for para in tf.paragraphs:
                    for run in para.runs:
                        ea = run._r.rPr.find(qn("a:ea"))
                        if ea is None or ea.get("typeface") != KO:
                            fonts_ok = False
                            problems.append(f"slide {si}: {nm} Korean font missing")
                        if run.font.size.pt < 14:
                            problems.append(f"slide {si}: {nm} font {run.font.size.pt}pt < 14")
                need, info = frame_height(tf, aw)
                if need > ah + 0.01:
                    problems.append(f"slide {si}: {nm} text may overflow (need {need:.2f} in, have {ah:.2f}) {info}")
            boxes.append((name, group, x, y, x + w, y + h))
        # 3) overlaps and 0.2 in gaps
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if a[1] == "bg" or b[1] == "bg":
                    continue
                dx = max(b[2] - a[4], a[2] - b[4])
                dy = max(b[3] - a[5], a[3] - b[5])
                overlap = dx < -1e-3 and dy < -1e-3
                if overlap and a[1] != b[1]:
                    problems.append(f"slide {si}: overlap {a[0]} / {b[0]}")
                elif not overlap and a[1] != b[1] and max(dx, dy) < 0.2 - 1e-3:
                    problems.append(f"slide {si}: gap {max(dx, dy):.2f} in between {a[0]} / {b[0]}")
    return prs, problems, fonts_ok


def main():
    prs = new_presentation()          # 16:9, 13.333 x 7.5 in
    for build in (slide_cover, slide_agenda, slide_capability, slide_agents,
                  slide_invest, slide_society, slide_korea, slide_closing):
        build(prs)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"saved {OUT}")

    back, problems, fonts_ok = verify(OUT)
    print(f"slides: {len(back.slides)}")
    for i, slide in enumerate(back.slides, 1):
        titles = [s.text_frame.text.replace("\n", " ") for s in slide.shapes
                  if s.name.startswith(("hdr_title", "title", "kt:title")) and s.has_text_frame]
        print(f"  {i}: {titles[0] if titles else ''} ({len(slide.shapes)} shapes)")
    print(f"Korean font on every run: {fonts_ok}")
    print("layout problems:" if problems else "layout check: OK (bounds, overlaps, gaps, text fit)")
    for p in problems:
        print("  -", p)


if __name__ == "__main__":
    main()
