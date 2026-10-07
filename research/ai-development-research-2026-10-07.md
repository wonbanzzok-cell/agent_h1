# Research Notes: The Development of AI (research date: 2026-10-07)

These notes collect sources on the current state of AI development. They are the input for the report `report/AI_발전_보고서.docx`.

> Source note: many figures come from secondary summaries (news, blogs) of primary reports. Primary sources are named where known (Stanford AI Index, IEA, Epoch AI, company earnings). Treat secondary-only figures as indicative, not exact.

---

## 1. Technical capability

### 1.1 Capability is accelerating, not plateauing
- Stanford AI Index 2026 (published April 13, 2026; 400+ pages): SWE-bench coding scores rose from about 60% to nearly 100% in one year.
- Frontier models meet or exceed human-level performance on PhD-level science questions, multimodal reasoning, and competition mathematics. Google's Gemini Deep Think won a gold medal at the International Mathematical Olympiad.

### 1.2 The "jagged frontier"
- The same models that win IMO gold read analog clocks correctly only 50.1% of the time. Capability is uneven: superhuman in some tasks, unreliable in others.

### 1.3 US–China competition
- The performance gap between the top US and Chinese models has effectively closed; the lead has changed hands several times since early 2025.
- China leads in publication volume, citations, and patents; the US keeps more high-impact patents and more top-tier models.

### 1.4 Cost of intelligence is collapsing
- Epoch AI: the price of reaching a fixed performance level falls between 9x and 900x per year depending on the benchmark; GPT-4-level performance on PhD-level science questions fell about 40x per year.
- Other estimates put the decline at 5–10x per year for frontier models; a fixed level of performance fell roughly 1,000x in three years (GPT-3-quality output: $60 per million tokens in late 2021 → $0.06 by late 2024).
- Drivers: smaller models, cheaper hardware, and algorithmic efficiency (about 3x per year).

## 2. From chatbots to agents
- 2026 is described as the inflection point for AI agents: software that plans and executes multi-step work, not only answers questions.
- Market: AI agents market projected at $10.9B in 2026 and $50.3B by 2030 (CAGR ~46%).
- Adoption: about 51% of enterprises report agents in production, another 23% scaling; 62% at least experimenting. 40% of enterprise applications are expected to include task-specific agents by end of 2026 (vs. under 5% in 2025).
- Risks: over 40% of agentic AI projects are projected to be canceled by end of 2027 (cost, unclear value, weak risk controls). Only 44% of organizations using agents have security policies for them; 80% report agents taking unintended actions (e.g., accessing unauthorized systems).

## 3. Economy and investment
- Organizational AI adoption: 88%. Generative AI reached 53% of the population, faster than the PC or the internet (AI Index 2026).
- Big Tech capex: Alphabet, Amazon, Microsoft, and Meta plan about $725B of capital spending in 2026, up 77% from about $410B in 2025 (Amazon ~$200B, Microsoft ~$190B, Alphabet $175–185B, Meta $115–135B). Analysts project over $1T in 2027.
- Most of this spending goes to GPU clusters, custom chips, and data center construction.

## 4. Infrastructure and energy
- IEA: data center electricity demand grew 17% in 2025, more than five times global demand growth (3%).
- IEA projection: data center demand more than doubles to about 945 TWh by 2030 (more than Japan's current consumption); AI-specific demand triples.
- Constraints: shortages of gas turbines, transformers, and advanced semiconductors; slow grid connections and permits.
- Tech companies signed about 40% of all corporate renewable power purchase agreements in 2025 and are driving interest in nuclear and advanced geothermal.

## 5. Labor market
- Stanford "Canaries in the Coal Mine?" (August 2026 update, ADP payroll data): employment of workers aged 22–25 in the most AI-exposed occupations is now 19% below less-exposed peers (13% a year earlier).
- Since 2022, employment of 22–25-year-olds in the 40% most AI-exposed occupations fell about 11%, while it rose 10% in the 60% least exposed. The cause is mainly weaker hiring, not layoffs.
- Survey of ~1,000 US business leaders: 21% have frozen entry-level hiring because of AI; 36% expect to by end of 2026.
- Long-term risk: fewer entry-level roles today may leave a gap in experienced talent in the 2030s.

## 6. Science and healthcare
- ASCO 2026 analysis: 117 AI-enabled therapeutic assets from 63 companies have entered human trials; 60 (51.3%) completed Phase 1, only 8 (6.8%) completed Phase 2.
- Insilico Medicine's rentosertib (TNIK inhibitor for idiopathic pulmonary fibrosis) entered a 320-patient Phase III trial on July 7, 2026, after a Phase IIa result in Nature Medicine (+98.4 mL FVC at 12 weeks, highest dose).
- As of July 2026, no AI-discovered drug has full FDA approval.

## 7. Safety and governance
- Documented AI incidents rose from 233 to 362 year over year (AI Index 2026).
- Only half of US middle and high schools have AI policies; experts and the public differ by 50 points on whether AI will help people do their jobs.
- EU AI Act: the Digital Omnibus (Parliament June 16, Council June 29, 2026) delayed high-risk obligations — Annex III stand-alone systems from Aug 2, 2026 to Dec 2, 2027; Annex I embedded systems from Aug 2, 2027 to Aug 2, 2028. Article 50 transparency duties and general-purpose AI enforcement stayed on Aug 2, 2026. Reason: harmonized standards were not ready.

## 8. Korea
- AI Basic Act ("Framework Act on AI Development and Establishment of Trust"): passed December 2024, fully in force from January 22, 2026 — described as the first comprehensive AI law in full force. Core elements: risk management for high-impact AI and labeling duties for generative AI output.
- Government plan (December 2025 work plan of the Ministry of Science and ICT): develop a sovereign AI model in the global top 10, secure 260,000 GPUs in phases (including via a partnership with NVIDIA), and fund a KRW 1 trillion general-purpose AI project.
- July 2026: plan to spend about KRW 5 trillion of excess tax revenue on a Korean frontier model, concentrating about 10,000 NVIDIA Vera Rubin GPUs on one leading team ("selection and concentration").

## 9. Key takeaways for the report
1. Capability keeps rising fast, but unevenly ("jagged frontier").
2. The center of gravity moved from chatbots to agents; value is real but governance and security lag.
3. Investment and energy are the new bottlenecks: ~$725B capex in 2026, data center power doubling by 2030.
4. Falling inference cost spreads AI widely and quickly.
5. Labor impact is visible first in entry-level hiring.
6. Science/healthcare shows the first late-stage clinical evidence, but no approved AI-discovered drug yet.
7. Regulation is arriving but slowing at the edges (EU delay); Korea chose early, framework-style regulation plus heavy public investment.

## Sources
- Stanford AI Index 2026 summaries: [Stark Insider](https://starkinsider.com/2026/04/stanford-2026-ai-index-report.html), [Burges Salmon](https://www.burges-salmon.com/articles/102mpq6/ai-in-2026-what-does-stanfords-ai-index-tell-us/), [Lumenova](https://www.lumenova.ai/blog/stanford-2026-ai-index-report-findings/)
- Epoch AI: [LLM inference price trends](https://epoch.ai/data-insights/ai-inference-price-trends), [How has the cost of LLM inference changed](https://epoch.ai/blog/how-has-the-cost-of-llm-inference-changed); [The Price of Progress (arXiv)](https://arxiv.org/html/2511.23455v1)
- AI agents: [G2 Enterprise AI Agents Report](https://learn.g2.com/enterprise-ai-agents-report), [CMARIX](https://www.cmarix.com/blog/ai-agents-statistics-trends/), [Ringly](https://www.ringly.io/blog/ai-agent-statistics-2026)
- Capex: [Yahoo Finance](https://finance.yahoo.com/sectors/technology/articles/hyperscalers-hit-700-billion-2026-111243744.html), [AI Weekly](https://aiweekly.co/alerts/amazon-microsoft-alphabet-meta-plan-725b-ai-capex-in-2026), [The Next Web](https://thenextweb.com/news/alphabet-amazon-meta-q1-2026-earnings-ai-cloud)
- Energy (IEA): [W.Media](https://w.media/data-center-power-demand-will-double-by-2030-iea/), [Enlit](https://www.enlit.world/library/ai-and-data-centre-electricity-use-continue-to-surge-iea-finds)
- Labor: [Computing](https://www.computing.co.uk/news/2026/ai/ai-is-closing-the-door-on-entry-level-jobs-study-finds), [AI Weekly – Brynjolfsson](https://aiweekly.co/alerts/stanfords-brynjolfsson-study-entry-level-employment-in-ai-exposed-jobs-now-19), [Business Journal Daily](https://businessjournaldaily.com/ai-driving-decline-in-entry-level-hiring-survey-finds/)
- Drug discovery: [IntuitionLabs](https://intuitionlabs.ai/articles/ai-discovered-drugs-clinical-trials-2026), [Quartz](https://qz.com/pharma-ai-research-progress-lilly-insilico)
- EU AI Act: [Sidley Data Matters](https://datamatters.sidley.com/2026/06/22/eu-lawmakers-reach-provisional-agreement-to-delay-key-eu-ai-act-obligations/), [Process Excellence Network](https://www.processexcellencenetwork.com/ai/articles/eu-ai-act-2026-what-actually-changed-and-what-deployers-still-must-do)
- Korea: [law.asia](https://law.asia/ko/?p=673939), [eopla](https://eopla.net/magazines/37907), [Newsis](https://www.newsis.com/view/NISX20251212_0003438800), [Daum (GPU 260k)](https://v.daum.net/v/20251031185346138), [WikiDocs (sovereign AI, July 2026)](https://wikidocs.net/blog/@openwiki/21646/)
