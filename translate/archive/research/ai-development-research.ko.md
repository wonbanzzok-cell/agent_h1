# 자료 조사 정리: AI의 발전 (2026년 10월 기준)

이 문서는 AI 발전의 현황에 관한 자료를 수집·정리한 것입니다. 최종 보고서(`AI_발전_보고서.docx`)의 입력 자료로 사용됩니다.

> 출처 관련 참고: 아래 일부 수치는 1차 보고서를 요약한 2차 자료(블로그, 뉴스)에서 가져왔습니다. 1차 출처(예: 스탠퍼드 AI Index, Gartner, FDA)가 있는 경우 함께 표기했습니다. 2차 자료에만 근거한 수치는 참고용으로 보십시오.

---

## 1. 모델 성능

### 1.1 성능 향상의 가속
- 스탠퍼드 AI Index 2026: SWE-bench(코딩) 점수가 1년 만에 약 60%에서 거의 100%로 상승했습니다.
- 최첨단 모델은 이제 박사 수준 과학 문제, 멀티모달 추론, 경시대회 수학에서 인간 수준과 같거나 이를 넘어섭니다.
- **"들쭉날쭉한 최전선(jagged frontier)"**: 국제수학올림피아드에서 금메달을 따는 모델이 아날로그 시계는 50.1%만 정확히 읽습니다. 성능은 고르지 않습니다.
- 2025년 주요 최첨단 모델의 90% 이상을 산업계가 만들었습니다.

### 1.2 최첨단 모델 경쟁
- 2026년 상반기 OpenAI, Google DeepMind, Anthropic이 잇달아 최첨단 모델을 출시했으며, 선두 연구소 간 격차는 한 자릿수 퍼센트포인트에 불과합니다.
- 언급된 사례: OpenAI GPT-5.4(2026년 3월, GDPval 83% — 다수의 지식 노동 과제에서 전문가 수준 이상), Gemini 3.1 Pro, Claude Opus 4.6/4.7.
- 경쟁의 초점이 순수 성능에서 속도, 장문맥 추론, 에이전트형 도구 사용으로 옮겨갔습니다.

### 1.3 미국–중국
- 미국과 중국 최상위 모델 간 성능 격차는 사실상 사라졌으며, 2025년 초 이후 선두가 여러 차례 바뀌었습니다.
- 중국은 논문 수, 인용 수, 특허 수에서 앞서고, 미국은 영향력 높은 특허와 최상위 모델 수에서 우위를 유지합니다.

## 2. 챗봇에서 에이전트로
- 2026년의 핵심 흐름은 *실제로 행동하는* 소프트웨어입니다. 회의 예약, CRM 갱신, 풀 리퀘스트 제출, 티켓 등록 등을 점점 적은 인간 감독으로 수행합니다.
- 추론 우선 모델(다단계 계획에 더 많은 연산을 투입)이 주류가 되었고, 통합 도구 사용은 새로운 기능이 아니라 기본 기대치가 되었습니다.
- 에이전트 성능의 상한은 최첨단 모델이 정합니다. 이들은 50개 이상의 도구와 매우 긴 문맥을 안정적으로 다룹니다.

## 3. 경제와 도입

### 3.1 도입
- 조직의 AI 도입률이 88%에 도달했습니다(AI Index 2026).
- 생성형 AI는 인구의 53%에 보급되었으며, 이는 PC나 인터넷보다 빠른 속도입니다.

### 3.2 투자
- 전 세계 민간 AI 투자는 약 2,520억 달러로 보고되었습니다(AI Index 2026의 2차 요약). 생성형 AI 투자는 200% 이상 증가해 민간 AI 투자의 거의 절반을 차지했습니다.
- 신규 투자 유치 AI 기업 수는 71% 증가했고, 10억 달러 이상 투자 건수는 거의 두 배가 되었습니다.
- 상위 5개 하이퍼스케일러의 2026년 데이터센터·AI 인프라 설비투자 전망: 약 6,020억 달러(2025년 약 4,000억 달러).

### 3.3 비용
- LLM 추론 비용은 매년 약 10배씩 하락했습니다. 2022년 말 100만 토큰당 20달러였던 GPT-4 수준 성능이 현재 약 0.40달러입니다.
- 추론 지출이 처음으로 학습 지출을 넘어섰습니다.

## 4. 인프라와 에너지
- Gartner(2026년 6월): 2026년 전 세계 데이터센터 전력 수요는 약 26~27% 증가해 약 132GW(2025년 104GW)에 이를 전망입니다.
- AI 최적화 서버는 2026년 데이터센터 전력 사용량의 31%를 차지할 것으로 추정되며, 2027년에는 일반 서버를 넘어설 전망입니다.
- IEA: 2025년 데이터센터 전력 소비는 17% 증가해 전 세계 전력 수요 증가율 3%를 크게 웃돌았습니다. 2030년 데이터센터 소비량은 약 945TWh로 2024년(415TWh)의 약 두 배가 될 전망입니다.

## 5. 노동 시장
- Gallup(2026년 2월, 미국 근로자 23,717명): 전체 근로자의 18%(AI 도입 조직은 23%)가 5년 내 AI로 일자리가 없어질 가능성이 있다고 답했습니다. AI 도입 조직 근로자의 65%는 AI가 생산성을 높였다고 답했습니다.
- S&P Global(2026): AI의 전 세계 순고용 효과가 소폭 부정적으로 돌아섰지만, 기업들은 인력 감축(24%)보다 프로세스 효율(64%)과 생산성(59%)을 우선시합니다.
- 세계경제포럼: 2030년까지 1억 7,000만 개 일자리가 생기고 9,200만 개가 대체되어 순증 7,800만 개가 예상됩니다.

## 6. 과학과 의료
- FDA 목록: 미국에서 승인된 AI 기반 의료기기는 1,451개이며, 그중 1,104개가 영상의학 분야입니다. 2026년 8월 FDA는 생성형 AI 의료기기에 대한 위험 비례 규제 방안 논의 문서를 발표했습니다.
- 173개 이상의 AI 설계 신약 후보가 임상 개발 중이며, 1상 성공률은 과거 평균 약 52% 대비 80~90%로 보고됩니다.
- 2026년 7월 기준, AI로 발견된 신약 중 FDA 최종 승인을 받은 것은 없습니다. 가장 앞선 사례인 Insilico Medicine의 렌토서팁(특발성 폐섬유증)은 2026년 7월 7일 3상에 진입했습니다.
- 재료과학: Google DeepMind의 GNoME는 안정적인 결정 구조 240만 개를 예측했고, 에이전트형 시스템이 로봇 실험실을 운영하고 있습니다.

## 7. 안전, 신뢰, 규제
- AI Index 2026: 기록된 AI 사고는 2024년 233건에서 2025년 362건으로 증가했습니다. 성능과 도입 속도가 평가·감독 체계를 앞지르고 있습니다.
- **EU AI Act**: 2025년 2월 2일부터 첫 조항 적용, 2027년까지 단계적 시행.
- **한국 AI 기본법**(인공지능 발전과 신뢰 기반 조성 등에 관한 기본법): 2024년 12월 26일 국회 통과, 2026년 1월 22일 시행 — 아시아 최초의 포괄적 AI 법률입니다. 생성형 AI와 "고영향 AI"(생명·안전·기본권에 중대한 영향)를 대상으로 하며, 투명성 의무와 역외 적용을 규정합니다.

## 8. 한국의 위치
- 2025년 말 APEC에서 NVIDIA는 한국 정부, 삼성, SK그룹, 현대, 네이버가 소버린 AI, 로보틱스, 제조를 위해 약 26만 개의 Blackwell GPU를 도입한다고 발표했습니다.
- 내역: 정부 소버린 AI 인프라(국가 AI 컴퓨팅 센터, 국내 클라우드 사업자)용 5만 개 이상, 삼성 AI 팩토리용 5만 개 이상, SK AI 팩토리·산업용 AI 클라우드용 5만 개 이상 등.
- 한국 정부 관계자들은 소버린 AI 역량 확보를 위해 GPU, 데이터, 인재에 대한 지속적 투자를 강조합니다.

## 9. 보고서용 핵심 정리
1. 성능은 빠르게, 그러나 고르지 않게 향상되고 있습니다("들쭉날쭉한 최전선").
2. 중심축이 대화형에서 자율 에이전트로 이동하고 있습니다.
3. 지능 단위당 비용은 급락하는 반면, 총 투자와 에너지 사용은 급증하고 있습니다.
4. 노동 효과는 혼재되어 있습니다. 당장은 생산성이 오르지만 대체 위험도 커지고 있습니다.
5. 과학과 의료에서 실질적이지만 초기 단계의 성과가 나타나고 있습니다.
6. 거버넌스가 성능을 따라가지 못하고 있으며, 2026년은 첫 주요 규제 준수의 해입니다(EU, 한국).
7. 한국은 컴퓨팅 자원(GPU)과 선도적 법제도로 입지를 다지고 있습니다.

---

## 출처
- Stanford HAI, AI Index Report 2026 — Economy chapter: https://hai.stanford.edu/ai-index/2026-ai-index-report/economy
- Burges Salmon, "AI in 2026: what does Stanford's AI Index tell us": https://www.burges-salmon.com/articles/102mpq6/ai-in-2026-what-does-stanfords-ai-index-tell-us/
- Lumenova, Stanford 2026 AI Index findings: https://www.lumenova.ai/blog/stanford-2026-ai-index-report-findings/
- The Deep View, "AI's surge is widening gaps in trust and policy": https://www.thedeepview.com/articles/ai-s-surge-is-widening-gaps-in-trust-and-policy
- Daily AI World, AI Index 2026 summary: https://dailyaiworld.com/blogs/stanford-hai-2026-ai-index-252b-investment-88-adoption-773
- Carly, State of AI 2026: https://www.usecarly.com/blog/state-of-ai-2026/
- Valentin Zacharias, "Frontier AI in 2026 – Agents with agency": https://valentinzacharias.de/blog/2026-01-agentswithagency
- Gartner, data center electricity demand 2026: https://www.gartner.com/en/newsroom/press-releases/2026-06-10-gartner-says-data-center-electricity-demand-to-grow-26-percent-in-2026
- Petromindo (IEA), data centre power demand: https://www.petromindo.com/news/article/data-centre-power-demand-surges-on-ai-growth-iea-says
- TTMS, AI data center energy 2024–2026: https://ttms.com/growing-energy-demand-of-ai-data-centers-2024-2026/
- S&P Global, The AI and Labor Landscape 2026: https://www.spglobal.com/content/dam/spglobal/global-assets/en/special-reports/The%20AI%20and%20Labor%20Landscape%202026.pdf
- Project DisCo, AI and workers research: https://project-disco.org/innovation/new-research-shows-ai-can-complement-workers-boost-wages-and-expand-opportunity/
- Gloat, AI labor market impact 2026: https://gloat.com/blog/ai-labor-market/
- IntuitionLabs, AI drug discovery and FDA approvals: https://intuitionlabs.ai/pdfs/ai-drug-discovery-fda-approvals.pdf
- Chambers, Healthcare AI 2026 (USA): https://practiceguides.chambers.com/practice-guides/healthcare-ai-2026/usa
- Cooley, South Korea's AI Basic Act overview: https://www.cooley.com/news/insight/2026/2026-01-27-south-koreas-ai-basic-act-overview-and-key-takeaways
- AI-Regulation.com, global AI regulation shifts: https://ai-regulation.com/global-ai-regulation-south-korea-ai-act-trump-eu-ai-act/
- NVIDIA press release, South Korea AI infrastructure: https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-South-Korea-Government-and-Industrial-Giants-Build-AI-Infrastructure-and-Ecosystem-to-Fuel-Korea-Innovation-Industries-and-Jobs/
- Korea Herald, sovereign AI investment: https://www.koreaherald.com/article/10759782
