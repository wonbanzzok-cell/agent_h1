# 자료조사 노트: AI의 발전 (조사일: 2026-10-07)

이 노트는 AI 발전의 현황에 관한 자료를 모아 정리한 것입니다. 보고서 `report/AI_발전_보고서.docx`의 기초 자료로 사용됩니다.

> 출처 관련 참고: 상당수 수치는 1차 보고서를 요약한 2차 자료(뉴스, 블로그)에서 가져왔습니다. 확인 가능한 경우 1차 출처(Stanford AI Index, IEA, Epoch AI, 기업 실적 발표)를 명시했습니다. 2차 자료로만 확인된 수치는 정확한 값이 아닌 참고치로 보십시오.

---

## 1. 기술 역량

### 1.1 역량은 정체가 아니라 가속 중
- Stanford AI Index 2026(2026년 4월 13일 발간, 400쪽 이상): SWE-bench 코딩 점수가 1년 만에 약 60%에서 100% 가까이 상승했습니다.
- 프런티어 모델은 박사 수준 과학 문제, 멀티모달 추론, 경시대회 수학에서 인간 수준에 도달하거나 이를 넘어섰습니다. Google의 Gemini Deep Think는 국제수학올림피아드(IMO)에서 금메달을 획득했습니다.

### 1.2 "들쭉날쭉한 프런티어(jagged frontier)"
- IMO 금메달을 딴 같은 모델이 아날로그 시계는 50.1%만 정확히 읽습니다. 역량은 고르지 않아, 어떤 과제에서는 인간을 뛰어넘고 다른 과제에서는 신뢰하기 어렵습니다.

### 1.3 미·중 경쟁
- 미국과 중국 최상위 모델 간 성능 격차는 사실상 사라졌으며, 2025년 초 이후 선두가 여러 차례 바뀌었습니다.
- 중국은 논문 수, 인용 수, 특허 수에서 앞서고, 미국은 고영향 특허와 최상위 모델 수에서 앞섭니다.

### 1.4 지능의 비용이 급락
- Epoch AI: 일정 성능 수준에 도달하는 가격은 벤치마크에 따라 연 9배~900배 하락하며, 박사 수준 과학 문제에서 GPT-4 수준 성능의 가격은 연 약 40배 하락했습니다.
- 다른 추정으로는 프런티어 모델 기준 연 5~10배 하락이며, 고정된 성능 수준의 가격은 3년 만에 약 1,000배 하락했습니다(GPT-3 수준 출력: 2021년 말 100만 토큰당 60달러 → 2024년 말 0.06달러).
- 요인: 모델 소형화, 하드웨어 가격 하락, 알고리즘 효율 향상(연 약 3배).

## 2. 챗봇에서 에이전트로
- 2026년은 AI 에이전트의 변곡점으로 평가됩니다. 질문에 답하는 것을 넘어 여러 단계의 작업을 계획하고 실행하는 소프트웨어입니다.
- 시장: AI 에이전트 시장은 2026년 109억 달러, 2030년 503억 달러로 전망됩니다(연평균 성장률 약 46%).
- 도입: 기업의 약 51%가 에이전트를 실제 운영 중이고, 23%는 확대 중이며, 62%는 최소한 실험 단계에 있습니다. 2026년 말까지 기업용 애플리케이션의 40%에 업무 특화 에이전트가 탑재될 전망입니다(2025년 5% 미만).
- 위험: 에이전트형 AI 프로젝트의 40% 이상이 2027년 말까지 중단될 전망입니다(비용, 불명확한 가치, 미흡한 위험 통제). 에이전트를 사용하는 조직 중 보안 정책을 갖춘 곳은 44%뿐이며, 80%가 에이전트의 의도치 않은 행동(예: 비인가 시스템 접근)을 경험했다고 보고했습니다.

## 3. 경제와 투자
- 조직의 AI 도입률 88%. 생성형 AI는 인구의 53%에 보급되어 PC나 인터넷보다 빠르게 확산되었습니다(AI Index 2026).
- 빅테크 설비투자: Alphabet, Amazon, Microsoft, Meta는 2026년 약 7,250억 달러의 설비투자를 계획하고 있으며, 이는 2025년 약 4,100억 달러 대비 77% 증가한 규모입니다(Amazon 약 2,000억, Microsoft 약 1,900억, Alphabet 1,750~1,850억, Meta 1,150~1,350억 달러). 애널리스트들은 2027년에 1조 달러를 넘을 것으로 전망합니다.
- 투자의 대부분은 GPU 클러스터, 자체 칩, 데이터센터 건설에 쓰입니다.

## 4. 인프라와 에너지
- IEA: 2025년 데이터센터 전력 수요는 17% 증가해, 전 세계 전력 수요 증가율(3%)의 5배를 넘었습니다.
- IEA 전망: 데이터센터 전력 수요는 2030년까지 두 배 이상 늘어 약 945TWh(현재 일본의 전력 소비량보다 많음)에 이르고, AI 관련 수요는 세 배로 증가합니다.
- 제약 요인: 가스터빈, 변압기, 첨단 반도체 부족, 느린 전력망 연결과 인허가.
- 테크 기업들은 2025년 전체 기업 재생에너지 전력구매계약(PPA)의 약 40%를 체결했으며, 원자력과 차세대 지열에 대한 관심을 이끌고 있습니다.

## 5. 노동 시장
- Stanford "탄광 속 카나리아?" 연구(2026년 8월 업데이트, ADP 급여 데이터): AI 노출도가 가장 높은 직종의 22~25세 고용은 노출도가 낮은 직종보다 19% 낮습니다(1년 전 13%).
- 2022년 이후 AI 노출 상위 40% 직종의 22~25세 고용은 약 11% 감소한 반면, 하위 60% 직종에서는 10% 증가했습니다. 원인은 해고보다는 주로 채용 감소입니다.
- 미국 기업 리더 약 1,000명 설문: 21%가 AI 때문에 신입 채용을 동결했고, 36%는 2026년 말까지 동결할 것이라고 답했습니다.
- 장기 위험: 오늘 신입 일자리가 줄면 2030년대에 숙련 인재 공백이 생길 수 있습니다.

## 6. 과학과 의료
- ASCO 2026 분석: 63개 기업의 AI 기반 치료제 후보 117개가 임상시험에 진입했으며, 60개(51.3%)가 1상을, 8개(6.8%)만이 2상을 완료했습니다.
- Insilico Medicine의 rentosertib(특발성 폐섬유증 치료용 TNIK 억제제)은 Nature Medicine에 게재된 2a상 결과(최고 용량군 12주차 FVC +98.4mL) 이후, 2026년 7월 7일 환자 320명 규모의 3상 시험에 진입했습니다.
- 2026년 7월 기준, AI가 발굴한 신약 중 FDA 정식 승인을 받은 것은 아직 없습니다.

## 7. 안전과 거버넌스
- 기록된 AI 사고는 전년 대비 233건에서 362건으로 증가했습니다(AI Index 2026).
- 미국 중·고등학교의 절반만 AI 정책을 갖추고 있으며, AI가 사람들의 업무에 도움이 될지에 대해 전문가와 일반 대중의 견해는 50%p 차이가 납니다.
- EU AI Act: 디지털 옴니버스(의회 6월 16일, 이사회 6월 29일, 2026년)로 고위험 의무가 연기되었습니다. 부속서 III 단독형 시스템은 2026년 8월 2일 → 2027년 12월 2일, 부속서 I 내장형 시스템은 2027년 8월 2일 → 2028년 8월 2일. 제50조 투명성 의무와 범용 AI 집행 권한은 2026년 8월 2일 그대로 유지되었습니다. 사유: 통합 표준이 준비되지 않았기 때문입니다.

## 8. 한국
- AI 기본법(「인공지능 발전과 신뢰 기반 조성 등에 관한 기본법」): 2024년 12월 국회 통과, 2026년 1월 22일 전면 시행. 전면 시행된 세계 최초의 포괄적 AI 법으로 평가됩니다. 핵심은 고영향 AI의 위험관리와 생성형 AI 결과물 표시 의무입니다.
- 정부 계획(과학기술정보통신부 2025년 12월 업무계획): 세계 10위권 독자 AI 모델 개발, GPU 26만 장 순차 확보(NVIDIA와의 협력 포함), 1조 원 규모 범용 AI 사업 추진.
- 2026년 7월: 초과세수 약 5조 원을 한국형 프런티어 모델 개발에 투입하고, NVIDIA 베라루빈 GPU 약 1만 개를 최정예 한 팀에 집중 지원하는 방안 추진("선택과 집중").

## 9. 보고서용 핵심 시사점
1. 역량은 빠르게 향상되지만 고르지 않습니다("들쭉날쭉한 프런티어").
2. 무게중심이 챗봇에서 에이전트로 이동했으며, 가치는 실재하지만 거버넌스와 보안이 뒤처져 있습니다.
3. 투자와 에너지가 새로운 병목입니다. 2026년 설비투자 약 7,250억 달러, 데이터센터 전력은 2030년까지 두 배.
4. 추론 비용 하락으로 AI가 넓고 빠르게 확산됩니다.
5. 노동 영향은 신입 채용에서 가장 먼저 나타납니다.
6. 과학·의료에서 첫 후기 임상 근거가 나왔지만, 승인된 AI 발굴 신약은 아직 없습니다.
7. 규제는 도입되고 있으나 일부는 지연(EU 연기)되고 있으며, 한국은 이른 기본법형 규제와 대규모 공공 투자를 택했습니다.

## 출처
- Stanford AI Index 2026 요약: [Stark Insider](https://starkinsider.com/2026/04/stanford-2026-ai-index-report.html), [Burges Salmon](https://www.burges-salmon.com/articles/102mpq6/ai-in-2026-what-does-stanfords-ai-index-tell-us/), [Lumenova](https://www.lumenova.ai/blog/stanford-2026-ai-index-report-findings/)
- Epoch AI: [LLM inference price trends](https://epoch.ai/data-insights/ai-inference-price-trends), [How has the cost of LLM inference changed](https://epoch.ai/blog/how-has-the-cost-of-llm-inference-changed); [The Price of Progress (arXiv)](https://arxiv.org/html/2511.23455v1)
- AI 에이전트: [G2 Enterprise AI Agents Report](https://learn.g2.com/enterprise-ai-agents-report), [CMARIX](https://www.cmarix.com/blog/ai-agents-statistics-trends/), [Ringly](https://www.ringly.io/blog/ai-agent-statistics-2026)
- 설비투자: [Yahoo Finance](https://finance.yahoo.com/sectors/technology/articles/hyperscalers-hit-700-billion-2026-111243744.html), [AI Weekly](https://aiweekly.co/alerts/amazon-microsoft-alphabet-meta-plan-725b-ai-capex-in-2026), [The Next Web](https://thenextweb.com/news/alphabet-amazon-meta-q1-2026-earnings-ai-cloud)
- 에너지(IEA): [W.Media](https://w.media/data-center-power-demand-will-double-by-2030-iea/), [Enlit](https://www.enlit.world/library/ai-and-data-centre-electricity-use-continue-to-surge-iea-finds)
- 노동: [Computing](https://www.computing.co.uk/news/2026/ai/ai-is-closing-the-door-on-entry-level-jobs-study-finds), [AI Weekly – Brynjolfsson](https://aiweekly.co/alerts/stanfords-brynjolfsson-study-entry-level-employment-in-ai-exposed-jobs-now-19), [Business Journal Daily](https://businessjournaldaily.com/ai-driving-decline-in-entry-level-hiring-survey-finds/)
- 신약 개발: [IntuitionLabs](https://intuitionlabs.ai/articles/ai-discovered-drugs-clinical-trials-2026), [Quartz](https://qz.com/pharma-ai-research-progress-lilly-insilico)
- EU AI Act: [Sidley Data Matters](https://datamatters.sidley.com/2026/06/22/eu-lawmakers-reach-provisional-agreement-to-delay-key-eu-ai-act-obligations/), [Process Excellence Network](https://www.processexcellencenetwork.com/ai/articles/eu-ai-act-2026-what-actually-changed-and-what-deployers-still-must-do)
- 한국: [law.asia](https://law.asia/ko/?p=673939), [eopla](https://eopla.net/magazines/37907), [뉴시스](https://www.newsis.com/view/NISX20251212_0003438800), [다음(GPU 26만 장)](https://v.daum.net/v/20251031185346138), [WikiDocs(소버린 AI, 2026년 7월)](https://wikidocs.net/blog/@openwiki/21646/)
