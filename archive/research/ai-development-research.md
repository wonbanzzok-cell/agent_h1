# Research Notes: The Development of AI (as of October 2026)

These notes collect and organize sources on the current state of AI development. They are the input for the final report (`AI_발전_보고서.docx`).

> Note on sources: several figures below come from secondary summaries (blogs, news) of primary reports. Where a primary source exists (e.g., Stanford AI Index, Gartner, FDA), it is listed. Treat secondary-only figures as indicative.

---

## 1. Model capability

### 1.1 Capability is accelerating
- Stanford AI Index 2026: SWE-bench (coding) scores rose from about 60% to nearly 100% in a single year.
- Frontier models now match or exceed human-level performance on PhD-level science questions, multimodal reasoning, and competition mathematics.
- **"Jagged frontier"**: models that win gold at the International Mathematical Olympiad read analog clocks correctly only 50.1% of the time. Capability is uneven, not uniform.
- Industry produced over 90% of notable frontier models in 2025.

### 1.2 Frontier competition
- In the first half of 2026, OpenAI, Google DeepMind, and Anthropic released frontier models in rapid succession; the gap between leading labs is in single-digit percentage points.
- Examples cited: OpenAI GPT-5.4 (March 2026, 83% on GDPval — at or above expert level on many knowledge-work tasks), Gemini 3.1 Pro, Claude Opus 4.6/4.7.
- Competition has shifted from raw capability to speed, long-context reasoning, and agentic tool use.

### 1.3 US–China
- The performance gap between top US and Chinese models has effectively closed; the lead has changed hands several times since early 2025.
- China leads in publication volume, citations, and patent count; the US keeps more high-impact patents and more top-tier models.

## 2. From chatbots to agents
- The defining story of 2026 is software that *acts*: booking meetings, updating CRMs, shipping pull requests, filing tickets — with less human supervision.
- Reasoning-first models (spending more compute on multi-step planning) became mainstream; integrated tool use became an expectation rather than a novelty.
- Frontier models set the ceiling for agents: they reliably handle 50+ tools and very long contexts.

## 3. Economy and adoption

### 3.1 Adoption
- Organizational AI adoption reached 88% (AI Index 2026).
- Generative AI reached 53% of the population — faster than the PC or the internet did.

### 3.2 Investment
- Global private AI investment reported at about $252 billion (secondary summary of AI Index 2026); generative AI grew more than 200% and took nearly half of private AI funding.
- Newly funded AI companies rose 71%; billion-dollar funding rounds nearly doubled.
- Top five hyperscalers' projected 2026 capex on data centers and AI infrastructure: about $602 billion (vs. about $400 billion in 2025).

### 3.3 Cost
- LLM inference cost has dropped roughly 10x per year. GPT-4-level performance that cost $20 per million tokens in late 2022 costs about $0.40 now.
- Inference spending has overtaken training spending for the first time.

## 4. Infrastructure and energy
- Gartner (June 2026): worldwide data center electricity demand to grow about 26–27% in 2026, reaching about 132 GW (from 104 GW in 2025).
- AI-optimized servers are estimated at 31% of data center power use in 2026 and expected to exceed conventional servers by 2027.
- IEA: data center consumption grew 17% in 2025 vs. 3% growth in global electricity demand; data centers projected at about 945 TWh by 2030, roughly double 2024 (415 TWh).

## 5. Labor market
- Gallup (Feb 2026, 23,717 US employees): 18% of all employees (23% in AI-adopting organizations) think their job is likely to be eliminated by AI within five years; 65% of workers in AI-adopting organizations say AI improved their productivity.
- S&P Global (2026): AI's net employment impact turned modestly negative globally, but companies prioritize process efficiency (64%) and productivity (59%) over headcount reduction (24%).
- World Economic Forum: by 2030, 170 million jobs created and 92 million displaced — a net gain of 78 million.

## 6. Science and healthcare
- FDA list: 1,451 AI-enabled medical devices authorized in the US, 1,104 of them in radiology. In August 2026 the FDA released a discussion paper on risk-proportionate regulation of generative-AI medical devices.
- Over 173 AI-designed drug candidates are in clinical development; reported Phase I success rates of 80–90% vs. a historical ~52%.
- As of July 2026, no AI-discovered drug has full FDA approval. The most advanced, Insilico Medicine's rentosertib (idiopathic pulmonary fibrosis), entered Phase III on July 7, 2026.
- Materials science: Google DeepMind's GNoME predicted 2.4 million stable crystal structures; agentic systems now drive robotic labs.

## 7. Safety, trust, and regulation
- AI Index 2026: documented AI incidents rose to 362 in 2025 from 233 in 2024. Capability and adoption are outpacing evaluation and oversight.
- **EU AI Act**: first provisions applied from February 2, 2025; phased rollout through 2027.
- **Korea AI Basic Act** (Act on the Development of AI and Establishment of Trust): passed December 26, 2024; in force January 22, 2026 — the first comprehensive AI law in Asia. Covers generative AI and "high-impact AI" (significant effect on life, safety, or fundamental rights), with transparency duties and extraterritorial reach.

## 8. Korea's position
- At APEC (late 2025), NVIDIA announced the Korean government, Samsung, SK Group, Hyundai, and NAVER will deploy about 260,000 Blackwell GPUs for sovereign AI, robotics, and manufacturing.
- Breakdown includes 50,000+ GPUs for government sovereign AI infrastructure (National AI Computing Center, domestic cloud providers), 50,000+ for a Samsung AI factory, and 50,000+ for an SK AI factory / industrial AI cloud.
- Korean officials stress continued investment in GPUs, data, and talent to secure sovereign AI capability.

## 9. Key takeaways for the report
1. Capability keeps climbing fast, but unevenly ("jagged frontier").
2. The center of gravity is moving from chat to autonomous agents.
3. Costs per unit of intelligence are collapsing while total investment and energy use soar.
4. Labor effects are mixed: productivity gains now, displacement risk rising.
5. Science and medicine show real but early results.
6. Governance lags capability; 2026 is the first major compliance year (EU, Korea).
7. Korea is positioning through compute (GPUs) plus a first-mover legal framework.

---

## Sources
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
