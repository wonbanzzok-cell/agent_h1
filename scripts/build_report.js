const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, LevelFormat, PageBreak, Footer, PageNumber, TableOfContents,
} = require('docx');

const FONT = 'Malgun Gothic';
const ACCENT = '1F4E79';

const p = (text, opts = {}) => new Paragraph({
  spacing: { after: 140, line: 360 },
  alignment: AlignmentType.JUSTIFIED,
  ...opts,
  children: [new TextRun({ text, font: FONT, size: 22 })],
});
const h1 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 }, children: [new TextRun({ text, font: FONT })] });
const h2 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 120 }, children: [new TextRun({ text, font: FONT })] });
const bullet = (text, boldLead) => new Paragraph({
  numbering: { reference: 'bullets', level: 0 },
  spacing: { after: 80, line: 340 },
  children: boldLead
    ? [new TextRun({ text: boldLead, bold: true, font: FONT, size: 22 }), new TextRun({ text, font: FONT, size: 22 })]
    : [new TextRun({ text, font: FONT, size: 22 })],
});
const numbered = (text, boldLead) => new Paragraph({
  numbering: { reference: 'numbers', level: 0 },
  spacing: { after: 80, line: 340 },
  children: [new TextRun({ text: boldLead, bold: true, font: FONT, size: 22 }), new TextRun({ text, font: FONT, size: 22 })],
});

// Key figures table
const border = { style: BorderStyle.SINGLE, size: 4, color: 'BFBFBF' };
const borders = { top: border, bottom: border, left: border, right: border };
const COLS = [2600, 3400, 3026];
const cell = (text, i, header) => new TableCell({
  borders,
  width: { size: COLS[i], type: WidthType.DXA },
  shading: header ? { fill: ACCENT, type: ShadingType.CLEAR, color: 'auto' } : undefined,
  margins: { top: 80, bottom: 80, left: 120, right: 120 },
  children: [new Paragraph({ children: [new TextRun({ text, font: FONT, size: 20, bold: header, color: header ? 'FFFFFF' : '000000' })] })],
});
const rows = [
  ['구분', '핵심 지표', '출처'],
  ['기술 역량', 'SWE-bench 코딩 점수 약 60% → 100% 근접 (1년)', 'Stanford AI Index 2026'],
  ['비용', '동일 성능 추론 가격 연 9~900배 하락', 'Epoch AI'],
  ['확산', '조직 도입률 88%, 생성형 AI 인구 보급률 53%', 'Stanford AI Index 2026'],
  ['투자', '빅테크 4사 2026년 설비투자 약 7,250억 달러 (+77%)', '각사 실적 발표 종합'],
  ['에너지', '데이터센터 전력 2030년 약 945TWh (2배 이상)', 'IEA'],
  ['노동', 'AI 고노출 직종 22~25세 고용 19% 낮음', 'Stanford 연구 (2026.8)'],
  ['안전', 'AI 사고 233건 → 362건', 'Stanford AI Index 2026'],
];
const table = new Table({
  width: { size: 9026, type: WidthType.DXA },
  columnWidths: COLS,
  rows: rows.map((r, ri) => new TableRow({ tableHeader: ri === 0, children: r.map((t, i) => cell(t, i, ri === 0)) })),
});
const caption = (text) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 100, after: 240 }, children: [new TextRun({ text, font: FONT, size: 18, italics: true, color: '595959' })] });

const sources = [
  'Stanford HAI, AI Index Report 2026 (2026.4.13) — Stark Insider, Burges Salmon, Lumenova 요약 참고',
  'Epoch AI, "LLM inference price trends"; "The Price of Progress" (arXiv:2511.23455)',
  'G2, Enterprise AI Agents Report; CMARIX, Ringly AI 에이전트 통계 (2026)',
  'Yahoo Finance, AI Weekly, The Next Web — 빅테크 2026년 설비투자 보도',
  'IEA, Energy and AI 관련 보도 (W.Media, Enlit)',
  'Brynjolfsson 외, "Canaries in the Coal Mine?" 2026년 8월 업데이트 (Computing, AI Weekly 보도)',
  'IntuitionLabs, "AI-Discovered Drugs in Clinical Trials 2026"; Quartz',
  'Sidley Austin Data Matters, EU AI Act 디지털 옴니버스 관련 (2026.6.22)',
  'law.asia, eopla — 한국 AI 기본법; 뉴시스(2025.12.12), 다음, WikiDocs — 한국 소버린 AI 정책',
];

const children = [
  // Cover
  new Paragraph({ spacing: { before: 3200 }, alignment: AlignmentType.CENTER, children: [new TextRun({ text: 'AI 발전 보고서', font: FONT, size: 56, bold: true, color: ACCENT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200, after: 600 }, children: [new TextRun({ text: '역량·확산·투자·사회적 영향과 대응 과제', font: FONT, size: 28, color: '404040' })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, border: { top: { style: BorderStyle.SINGLE, size: 8, color: ACCENT, space: 12 } }, spacing: { before: 400 }, children: [new TextRun({ text: '작성일: 2026년 10월 7일', font: FONT, size: 22 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: '기초 자료: research/ai-development-research-2026-10-07.md', font: FONT, size: 18, color: '7F7F7F' })] }),
  new Paragraph({ children: [new PageBreak()] }),


  // 서론
  h1('Ⅰ. 서론'),
  h2('1. 작성 배경'),
  p('인공지능(AI)은 2022년 말 생성형 AI의 대중화 이후 불과 몇 년 만에 일상과 산업 전반으로 확산되었다. 2026년 현재 AI는 단순히 질문에 답하는 도구를 넘어, 스스로 계획을 세우고 업무를 수행하는 "에이전트"로 진화하고 있다. 동시에 막대한 투자와 전력 수요, 일자리 변화, 안전과 규제 문제 등 기술 바깥의 영향도 빠르게 커지고 있다.'),
  p('Stanford AI Index 2026은 이러한 흐름을 "역량은 정체가 아니라 가속 중이며, 안전·정책·교육은 역량을 따라가지 못하고 있다"고 요약한다. 따라서 AI 발전을 기술 성능의 관점만이 아니라 경제, 에너지, 노동, 제도의 관점에서 함께 살펴볼 필요가 있다.'),
  h2('2. 목적 및 범위'),
  p('본 보고서는 2026년 10월 기준 공개 자료를 바탕으로 AI 발전의 현황을 정리하고, 그 의미와 대응 과제를 도출하는 것을 목적으로 한다. 다루는 범위는 다음과 같다.'),
  bullet('기술 역량과 비용 변화'),
  bullet('챗봇에서 AI 에이전트로의 전환'),
  bullet('투자, 인프라, 에너지'),
  bullet('노동 시장, 과학·의료에 미치는 영향'),
  bullet('안전·규제 동향과 한국의 대응'),
  p('수치 상당수는 1차 보고서를 요약한 2차 자료에서 인용하였으므로, 정확한 값보다는 추세를 보여주는 참고치로 이해해야 한다.'),

  // 본론
  new Paragraph({ children: [new PageBreak()] }),
  h1('Ⅱ. 본론'),
  h2('1. 기술 역량: 빠르지만 고르지 않은 발전'),
  p('AI의 성능은 여전히 빠르게 향상되고 있다. 소프트웨어 개발 능력을 측정하는 SWE-bench 점수는 1년 만에 약 60%에서 100% 가까이 상승했고, 프런티어 모델은 박사 수준 과학 문제와 경시대회 수학에서 인간 수준에 도달하거나 이를 넘어섰다. Google의 Gemini Deep Think는 국제수학올림피아드에서 금메달을 획득했다.'),
  p('그러나 역량은 고르지 않다. IMO 금메달 수준의 모델이 아날로그 시계는 50.1%만 정확히 읽는다. 이른바 "들쭉날쭉한 프런티어(jagged frontier)"로, 특정 과제에서의 뛰어난 성능이 모든 영역에서의 신뢰성을 의미하지 않는다는 점을 보여준다.'),
  p('국가 간 경쟁 구도도 바뀌었다. 미국과 중국 최상위 모델 간 성능 격차는 사실상 사라졌으며, 중국은 논문·인용·특허 수에서, 미국은 고영향 특허와 최상위 모델 수에서 앞서 있다.'),

  h2('2. 비용 하락과 대중적 확산'),
  p('AI 확산의 가장 큰 동력은 비용 하락이다. Epoch AI에 따르면 일정 성능을 얻는 데 드는 추론 가격은 벤치마크에 따라 연 9배에서 900배까지 하락했다. GPT-3 수준 출력의 가격은 2021년 말 100만 토큰당 60달러에서 2024년 말 0.06달러로 약 1,000배 낮아졌다. 모델 소형화, 하드웨어 가격 하락, 연 약 3배에 이르는 알고리즘 효율 향상이 이를 이끌었다.'),
  p('그 결과 조직의 AI 도입률은 88%에 이르렀고, 생성형 AI는 인구의 53%에 보급되어 PC나 인터넷보다 빠른 확산 속도를 보였다.'),

  h2('3. 챗봇에서 에이전트로'),
  p('2026년 AI 발전의 핵심 키워드는 "에이전트"다. 에이전트는 회의 예약, 고객 데이터 갱신, 코드 수정 등 여러 단계로 이루어진 업무를 사람의 감독을 줄인 채 직접 수행한다. 기업의 약 51%가 에이전트를 실제 운영 중이며, 2026년 말까지 기업용 애플리케이션의 40%에 업무 특화 에이전트가 탑재될 것으로 전망된다(2025년 5% 미만).'),
  p('하지만 위험도 함께 커지고 있다. 에이전트를 사용하는 조직 중 이를 관리하는 보안 정책을 갖춘 곳은 44%에 불과하고, 80%가 에이전트의 의도치 않은 행동을 경험했다. 또한 에이전트형 AI 프로젝트의 40% 이상이 비용과 불명확한 가치, 위험 통제 미흡으로 2027년 말까지 중단될 것으로 예상된다.'),

  h2('4. 투자와 에너지: 새로운 병목'),
  p('AI 경쟁은 인프라 경쟁으로 번지고 있다. Alphabet, Amazon, Microsoft, Meta 4개사의 2026년 설비투자 계획은 약 7,250억 달러로 전년(약 4,100억 달러) 대비 77% 증가했으며, 2027년에는 1조 달러를 넘을 것으로 전망된다. 투자의 대부분은 GPU 클러스터, 자체 칩, 데이터센터 건설에 쓰인다.'),
  p('이는 곧 전력 문제로 이어진다. IEA에 따르면 2025년 데이터센터 전력 수요는 17% 증가해 전체 전력 수요 증가율(3%)의 5배를 넘었고, 2030년에는 약 945TWh로 두 배 이상 늘어 현재 일본의 전력 소비량을 넘어설 전망이다. 가스터빈·변압기·첨단 반도체 부족과 전력망 연결 지연이 성장의 제약 요인으로 떠올랐으며, 테크 기업들은 재생에너지와 원자력 확보에 적극 나서고 있다.'),

  h2('5. 노동 시장: 신입 일자리에서 먼저 나타나는 변화'),
  p('AI의 노동 영향은 신입 채용에서 가장 먼저 드러나고 있다. Stanford 연구진이 미국 급여 데이터를 분석한 결과(2026년 8월), AI 노출도가 높은 직종의 22~25세 고용은 노출도가 낮은 직종보다 19% 낮았으며, 이 격차는 1년 전 13%에서 더 벌어졌다. 이는 해고보다는 채용 감소에 따른 것이다.'),
  p('미국 기업 리더 대상 설문에서도 21%가 AI 때문에 신입 채용을 동결했다고 답했다. 신입 일자리는 미래의 숙련 인재를 길러내는 통로이기 때문에, 단기 비용 절감이 2030년대의 인재 공백으로 이어질 수 있다는 우려가 제기된다.'),

  h2('6. 과학과 의료: 첫 후기 임상 근거'),
  p('AI는 신약 개발에서도 성과를 내기 시작했다. 2026년 ASCO 분석에 따르면 63개 기업의 AI 기반 치료제 후보 117개가 임상시험에 진입했다. Insilico Medicine의 특발성 폐섬유증 치료제 후보 rentosertib은 2026년 7월 환자 320명 규모의 3상 시험에 들어갔다. 다만 2상을 완료한 후보는 8개(6.8%)에 그치고, AI가 발굴한 신약 중 FDA 정식 승인을 받은 사례는 아직 없어, 기대와 실제 성과 사이의 간극도 분명하다.'),

  h2('7. 안전과 규제, 그리고 한국의 대응'),
  p('기록된 AI 사고는 1년 사이 233건에서 362건으로 늘었다. 규제는 도입되고 있으나 속도 조절도 나타난다. EU는 2026년 6월 디지털 옴니버스를 통해 AI Act의 고위험 AI 의무 시행을 2027년 12월(단독형) 및 2028년 8월(제품 내장형)로 연기했다. 통합 표준이 준비되지 않았기 때문이다. 다만 투명성 의무와 범용 AI 관련 집행은 2026년 8월부터 예정대로 적용되었다.'),
  p('한국은 2026년 1월 22일 「인공지능 발전과 신뢰 기반 조성 등에 관한 기본법」(AI 기본법)을 전면 시행하여, 고영향 AI의 위험관리와 생성형 AI 결과물 표시 의무를 도입했다. 동시에 GPU 26만 장의 순차 확보, 세계 10위권 독자 AI 모델 개발, 초과세수 약 5조 원을 활용한 한국형 프런티어 모델 집중 지원 등 대규모 공공 투자를 추진하고 있다.'),

  new Paragraph({ keepNext: true, spacing: { before: 200, after: 120 }, children: [new TextRun({ text: '[표 1] AI 발전 핵심 지표 요약', font: FONT, size: 22, bold: true })] }),
  table,
  caption('※ 수치는 2차 자료 요약 기준이며 추세 파악을 위한 참고치임'),

  // 결론
  new Paragraph({ children: [new PageBreak()] }),
  h1('Ⅲ. 결론'),
  h2('1. 요약'),
  p('2026년의 AI는 빠르게 똑똑해지고, 빠르게 싸지고, 빠르게 퍼지고 있다. 동시에 그 영향은 기술의 영역을 넘어 자본, 에너지, 일자리, 제도의 영역으로 확장되었다. 본 보고서의 주요 결론은 다음과 같다.'),
  numbered(' 성능은 가속 중이지만 고르지 않아, 신뢰성 검증이 여전히 중요하다.', '역량:'),
  numbered(' 무게중심이 챗봇에서 에이전트로 이동했으나, 보안과 거버넌스가 뒤처져 있다.', '활용:'),
  numbered(' 막대한 설비투자와 전력 수요가 AI 발전의 새로운 병목이 되었다.', '인프라:'),
  numbered(' 영향은 신입 채용 감소로 먼저 나타나며, 장기적 인재 공백이 우려된다.', '노동:'),
  numbered(' 규제는 자리 잡는 중이나 속도 조절이 병행되고 있으며, 한국은 이른 기본법 시행과 대규모 투자를 택했다.', '제도:'),
  h2('2. 대응 과제'),
  bullet(' 에이전트 도입 전 권한·접근 범위와 감사 체계를 먼저 설계하고, 결과물의 사람 검토 절차를 유지한다.', '기업:'),
  bullet(' 신입 채용을 줄이기보다 AI 활용 역량을 갖춘 신입을 육성하는 방식으로 인재 파이프라인을 지킨다.', '인재:'),
  bullet(' AI 기본법 하위 기준을 구체화하고, 전력망·데이터센터 등 인프라 계획을 AI 전략과 연계한다.', '정부:'),
  bullet(' AI 결과물을 비판적으로 검토하는 능력과, 도구를 업무에 결합하는 능력을 함께 기른다.', '개인:'),
  h2('3. 맺음말'),
  p('AI 발전은 더 이상 "얼마나 똑똑한가"만의 문제가 아니라, "얼마나 안전하고 지속 가능하게 사회에 통합할 것인가"의 문제가 되었다. 기술의 속도와 제도·인프라·사람의 적응 속도 사이의 간격을 줄이는 것이 앞으로의 핵심 과제이다.'),

  // 참고문헌
  h1('참고 자료'),
  ...sources.map((s) => bullet(s)),
];

const doc = new Document({
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 32, bold: true, color: ACCENT, font: FONT }, paragraph: { outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 26, bold: true, color: '2E75B6', font: FONT }, paragraph: { outlineLevel: 1 } },
    ],
  },
  numbering: {
    config: [
      { reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: 'numbers', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18 })] })] }) },
    children,
  }],
});

// Default output: report/AI_발전_보고서.docx (pass a path to write elsewhere)
const outPath = process.argv[2] || path.join(__dirname, '..', 'report', 'AI_발전_보고서.docx');
Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(outPath, buf);
  console.log('written', outPath);
});
