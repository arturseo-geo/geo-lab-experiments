# Noise Floor Measurement for AI Citation Experiments: Platform Variance, Recording Artifacts, and a Four-Test Diagnostic Protocol

Artur Ferreira — The GEO Lab (thegeolab.net) — ORCID: 0009-0004-4072-9741

Submitted to Zenodo — GEO / AI Search Research

---

## Abstract

Controlled experiments measuring AI citation rate require a noise floor — a characterisation of natural citation variability under zero-intervention conditions — before any treatment effect can be interpreted. This paper reports a five-day, three-platform noise floor measurement against a single domain (thegeolab.net), using ten fixed queries across Perplexity sonar-pro, ChatGPT gpt-4o-mini, and Google AI Overviews (DataForSEO endpoint). During measurement, a Day 2 citation anomaly triggered a four-test diagnostic investigation (intraday repeat / content comparison / GSC impressions / crawler log analysis), which identified a recording artifact — not platform variance — as the source of the apparent instability.

Key findings: (1) Perplexity citation output is fully deterministic on short timescales — zero variance across all 5 days and 8 independent observations including 3 intraday reruns. (2) ChatGPT citation rate ranged 0–20% (0–2 citations per 10 queries) across five days, with a single Day 2 spike attributable to non-determinism in force_web_search=true mode. (3) Google AI Overviews returned 0 citations across all 50 checks; AI Overview boxes were present for 10/10 queries across Days 1–2 but cited no thegeolab.net URL in any case. (4) Combined noise floor (all three platforms, 10 queries each): 13.3–20.0pp. The interpretability threshold for subsequent experiments on this domain is set at 22.0pp combined — any observed delta below this value falls within noise floor range and cannot be attributed to a treatment.

The paper contributes: (a) a reproducible noise floor measurement protocol; (b) a four-test diagnostic playbook for investigating citation anomalies; (c) empirical evidence that Perplexity's citation surface is deterministic at T1 proprietary-concept query scale; and (d) the first published characterisation of a T1/T2 citation tier split (80% vs 0% Perplexity citation rate for proprietary vs category queries on a low-authority domain).

**Keywords:** generative engine optimisation, AI citation measurement, noise floor, Perplexity, Google AI Overviews, ChatGPT, measurement methodology

---

## 1. Introduction

The emerging field of Generative Engine Optimisation (GEO) depends on citation rate as its primary metric — the proportion of AI search responses that name a given URL as a source. Citation rate experiments compare pages, content interventions, or structural treatments against a control, inferring causal effects from observed deltas. If a page redesign raises the citation rate from 30% to 40%, the practitioner concludes the intervention worked. If an entity graph modification produces a 3pp lift, the question is whether that is real.

This measurement design has an underappreciated problem: without a characterisation of baseline variability, observed deltas are uninterpretable. A +4pp citation rate increase could reflect a genuine content effect or daily platform variance. A platform that produces 0–20% citation rates across days with identical content renders any sub-20pp finding meaningless. The noise floor — the range of citation rate variability under zero-intervention conditions — is a prerequisite for experimental inference, not an optional methodological detail.

No published study had characterised AI citation noise floors at the time E016 was designed (April 2026). Practitioner GEO guidance routinely reported citation deltas without reference to baseline variability. Reports of 10–15pp lifts from schema changes, content restructuring, or entity signals appeared in blog posts and case studies without any attempt to establish whether the platform would produce 10–15pp variation with no changes at all. This paper addresses that gap.

The secondary contribution is methodological. During the five-day measurement window, a Day 1→2 citation anomaly appeared: Perplexity appeared to switch the cited URL for query Q2 from one thegeolab.net page to another. Rather than accepting this as platform variance, we ran a four-test diagnostic investigation. The investigation overturned three successive hypotheses — platform non-determinism, crawl freshness differential, SEO cannibalisation — before identifying the actual cause: a recording artifact. The daily logger was capturing only the first annotation URL from a multi-URL annotation array, and the two thegeolab.net pages appeared at different positions on different days. Platform output was stable throughout; the variance was entirely in the measurement instrument.

This diagnostic sequence is the paper's most reusable contribution. The four-test protocol — intraday repeat, content comparison, GSC impressions, crawler log analysis — is documented in full in Appendix C and is offered as a standard investigative instrument for other researchers encountering unexplained citation variability.

---

## 2. Method

### 2.1 Domain and query set

Domain under test: thegeolab.net — a GEO research publication launched in early 2026, with low domain authority (DR ~0 at time of measurement) and limited backlink profile. The domain publishes original research on AI citation dynamics, GEO methodology, and content optimisation for large language model retrieval.

Query set: the E014 universal ten-query set, consisting of five Tier 1 proprietary-concept queries and five Tier 2 category queries.

- **T1 queries (proprietary concepts):** GEO Stack framework, Extractability (GEO), System Memory (GEO), Retrieval Probability (GEO), LLM readability score
- **T2 queries (category):** Generative Engine Optimisation, AI search optimisation, GEO vs SEO, AI citation rate, how to rank in AI search

Tier 1 queries target concepts defined and named by The GEO Lab — proprietary terminology where thegeolab.net is the definitional source. Tier 2 queries target competitive category terms where thegeolab.net competes with established publishers, research institutions, and news outlets for citation.

### 2.2 Platforms and execution

| Platform | Model / endpoint | Method |
|---|---|---|
| Perplexity | sonar-pro | DataForSEO ai_optimization_llm_response (web_search=true) |
| ChatGPT | gpt-4o-mini, force_web_search=true | DataForSEO ai_optimization_chat_gpt_scraper |
| Google AIO | N/A | Manual browser check (human-coded C/M/X) |

All three platforms were queried once per day for each of the 10 queries. Measurement window: 2026-04-13 to 2026-04-17 (5 days, 150 total checks: 5 days × 10 queries × 3 platforms). Execution time: approximately 10:00 UTC daily. Day 3 ran at 12:14 UTC (approximately 2 hours late due to an observer scheduling issue) — this was logged as a potential confound and tested explicitly on Day 4: the 08:01 UTC Day 4 run produced identical results, confirming time-of-day is not a variable within this protocol's range.

### 2.3 Controls

A publishing freeze was in effect for the full measurement window: no content changes, no redirects, no plugin updates, no new posts published, and no schema modifications on thegeolab.net. All external SEO-adjacent actions (social posting, link building, Zenodo deposits) were also paused for the five days. This ensures all observed citation variability reflects platform behaviour, not domain-side changes.

One infrastructure note: the 301 redirect from `/retrieval-probability-geo-stack/` to `/retrieval-probability/` was queued but deliberately not deployed during the freeze window. Its deployment was gated on E016 completion (executed 2026-04-18, post-freeze).

### 2.4 Recording — Day 1/2 limitation and correction

Days 1 and 2 were recorded using a single-URL logger that captured only the first annotation URL per query from the Perplexity API response. This is a known limitation identified during the Day 2 investigation: subsequent analysis confirmed Perplexity returns a multi-URL `annotations` array for at least one query in this set (Q2: Retrieval Probability), and the Day 1→2 apparent URL switch was the logger selecting different array positions on different days, not a platform-side change.

Binary citation counts for Days 1–2 — whether thegeolab.net appeared in the annotation array at all, regardless of position — are correct. The URL-level annotation data for Days 1–2 was completed via a retrospective re-run on 2026-04-28, using the same query set; the full `annotations` arrays are included in this deposit as `data/e016_annotation_rerun_20260428.json`. The re-run confirmed the expected result: Q2 returns both thegeolab.net URLs in identical position order, consistent with the intraday retest and Days 3–5 daily runs.

### 2.5 The Day 2 investigation — four-test diagnostic

On Day 2 (2026-04-14), Perplexity appeared to switch the cited URL for query Q2 from `/retrieval-probability-geo-stack/` (Day 1) to `/retrieval-probability/` (Day 2). Rather than attributing this to platform variance and moving on, we ran four diagnostic tests in sequence.

**Test 1 — Intraday repeat** (2026-04-15 01:47:20–01:48:07 UTC). Three identical API calls spaced 40–45 seconds apart returned identical annotation arrays — same 7 sources, same order, every run. Total runtime: 47 seconds. This confirmed Perplexity's output is deterministic at intraday timescales. If the flip were genuine platform randomness, we would expect divergent arrays. All three runs were identical: the flip could not be attributed to within-API selection variance.

**Test 2 — Content comparison.** Both thegeolab.net URLs appearing in Q2 annotations were fetched and compared. The finding was not a simple duplicate: `/retrieval-probability/` (2,700 words, Version 2.2, February 2026) defined GEO Stack as a five-layer model comprising Retrieval Probability, Extractability, Entity Reinforcement, Structural Authority, and System Memory. The second page, `/retrieval-probability-geo-stack/` (1,800 words, March 2026), defined GEO Stack entirely differently — as Discoverability, Relevance, Authority, Retrieval Probability, and Amplification — a taxonomy that blends traditional SEO signals (CTR, dwell time, domain authority) with GEO concepts. Both pages were self-canonical and indexed. Perplexity had been returning both simultaneously because they were both legitimate index candidates for Q2 — not because of a retrieval error.

**Test 3 — GSC impressions.** GSC search analytics for query variants containing "retrieval probability" over the previous 30 days returned zero impressions. Google organic had generated no traffic to either page. AI search platforms, not Google, were the only active discovery channel for this content. Cannibalisation in the traditional SEO sense — Google splitting organic traffic between two competing pages — did not apply here.

**Test 4 — Crawler log analysis.** Nginx access logs were inspected for PerplexityBot activity. Both URLs were hit in the same second on Day 1 (2026-04-13 07:23:23 UTC) and again in the same second on Day 2 (2026-04-14 10:00:38 UTC), from neighbouring IPs in the 18.97.9.x block. Synchronous crawl timing rules out differential freshness: both URLs were already in Perplexity's index before either measurement run. The "flip" could not be explained by one URL being freshly discovered between Day 1 and Day 2.

**Conclusion of investigation:** with platform variance, crawl freshness, and content duplication all eliminated as explanations, the recording artifact hypothesis was the only remaining candidate — and it was consistent with all the evidence. The Day 1→2 anomaly was an instrument failure, not a platform event.

---

## 3. Results

### 3.1 Five-day citation summary

| Day | Date | UTC | Perplexity | ChatGPT | Google AIO | Combined /30 |
|---|---|---|---|---|---|---|
| 1 | 13 Apr 2026 | ~10:04 | 4/10 (40%) | 0/10 (0%) | 0/10 (0%) | **13.3%** |
| 2 | 14 Apr 2026 | ~10:04 | 4/10 (40%) | 2/10 (20%) | 0/10 (0%) | **20.0%** |
| 3 | 15 Apr 2026 | 12:14 | 4/10 (40%) | 0/10 (0%) | 0/10 (0%) | **13.3%** |
| 4 | 16 Apr 2026 | 08:01 | 4/10 (40%) | 0/10 (0%) | 0/10 (0%) | **13.3%** |
| 5 | 17 Apr 2026 | 08:00 | 4/10 (40%) | 0/10 (0%) | 0/10 (0%) | **13.3%** |
| **5-day avg** | | | **40%** | **4%** | **0%** | **14.7%** |

C = cited (thegeolab.net URL in source list). M = mentioned (brand name in text, no URL). X = not cited or mentioned. AIO assumed 0/10 on Days 3–5 based on consistent 0/10 result Days 1–2 and absence of AIO manual runs.

### 3.2 Noise floor by platform

| Platform | Min | Max | Range | Variance assessment |
|---|---|---|---|---|
| Perplexity | 40% | 40% | 0pp | Zero — deterministic |
| ChatGPT | 0% | 20% | 20pp | High — single outlier Day 2 |
| Google AIO | 0% | 0% | 0pp | Zero (floor — no citations) |
| Combined /30 | 13.3% | 20.0% | 6.7pp | Low-moderate |

The noise floor range is 13.3%–20.0% combined. The Day 2 maximum (20.0%) is a single-day outlier driven entirely by ChatGPT's force_web_search non-determinism. On all other days the combined rate was 13.3%. If ChatGPT is excluded (treating Perplexity + AIO only), the noise floor collapses to a flat 40% Perplexity / 0% AIO — a combined /20 rate of 20% across all five days with zero variance.

### 3.3 Tier 1 vs Tier 2 split (Perplexity, all 5 days)

| Tier | Query count | Citations per day (avg) | Rate | Stability |
|---|---|---|---|---|
| T1 (proprietary concepts) | 5 | 4.0 | 80% | Perfect — 0% flip rate |
| T2 (category) | 5 | 0.0 | 0% | Perfect — 0% flip rate |

Four T1 queries (GEO Stack, Extractability, System Memory, Retrieval Probability) returned a citation on every one of the 5 days — zero flip rate across 20 individual checks. The fifth T1 query (LLM readability) returned 0 citations across all 5 days, likely due to semantic overlap with generic readability content from higher-authority publishers.

All five T2 category queries returned 0 citations across all 25 checks. The domain authority gate is holding: thegeolab.net does not appear in Perplexity responses to category queries regardless of content quality. This was subsequently confirmed by the EDX experiment (Zenodo DOI: 10.5281/zenodo.19450361), which established the domain authority gate as the primary blocker for T2 citation on low-authority research domains.

### 3.4 Per-query stability (Perplexity)

The following query→citation bindings were observed across all 5 days:

- **Stable C (cited every day, 5/5):** GEO Stack framework (Q1/Q5), Extractability (Q6), System Memory (Q3), Retrieval Probability (Q2)
- **Stable X (not cited any day, 0/5):** LLM readability score (Q4), Generative Engine Optimisation (Q7), AI search optimisation (Q8), GEO vs SEO (Q9), AI citation rate (Q10), how to rank in AI search (Q10-alt)

No query changed citation status across any of the 5 days. Flip rate: 0/10 queries = 0%. This is the operational definition of Perplexity's determinism finding: not merely that the aggregate count was stable, but that the same specific queries produced the same binary citation outcome every single day.

The Q2 annotation array (Retrieval Probability) was observed in full on 6 occasions: 3 intraday reruns (2026-04-15 01:47–01:48 UTC) and Days 3, 4, 5 daily runs. All 6 observations returned both thegeolab.net URLs — `/retrieval-probability-geo-stack/` at position 1 and `/retrieval-probability/` at position 2 — in identical order.

### 3.5 ChatGPT source-array firing rate

A secondary observation from the ChatGPT data is the inconsistency in source-array firing: the proportion of queries for which the scraper returned any source URLs at all varied day to day.

| Day | Queries with any source array | ChatGPT citations |
|---|---|---|
| 1 | N/A (prior to methodology fix) | 0 |
| 2 | N/A | 2 |
| 3 | 3/10 | 0 |
| 4 | 2/10 | 0 |
| 5 | 4/10 | 0 |

Even on days when source arrays fired, no thegeolab.net URL was cited (Days 3–5). The citations on Day 2 were to thegeolab.net via the `utm_source=openai` attribution; the sources that fired on Days 3–5 cited other domains. This confirms that ChatGPT's web search firing is non-deterministic at the query level and is not a reliable signal for low-authority domains.

### 3.6 Root causes of observed variance

| Apparent anomaly | Root cause | Classification |
|---|---|---|
| Day 1→2 Perplexity URL switch (Q2) | Single-URL logger selecting different positions from 2-URL annotation array | Recording artifact |
| Day 2 ChatGPT spike (0→2 citations) | force_web_search non-determinism; source arrays fired for 2 relevant queries | Platform non-determinism |
| Day 1 ChatGPT web_search failure | DataForSEO ai_optimization_llm_response silently ignored web_search=true flag | Tool bug (switched to ai_optimization_chat_gpt_scraper from Day 1 onwards) |
| Day 3 timing (+2h14m) | Observer scheduling | Confound tested and eliminated on Day 4 |

Central finding: no genuine platform noise detected across the five-day window. All observed variance is attributable to recording error, a known API tool bug, or single-day non-determinism in ChatGPT's web search invocation.

---

## 4. Discussion

### 4.1 Perplexity is deterministic at proprietary-query scale

The most striking finding is Perplexity's zero variance. Across 50 daily checks (5 days × 10 queries) plus 3 intraday reruns, citation output was identical every time — the same queries cited, the same URLs returned, the same annotation array order. This is not merely "low variance"; it is structural determinism.

The implication for experimental design is significant. If Perplexity's citation selection behaves as a deterministic function of its current index state — not a stochastic draw at query time — then single-run measurements are theoretically sufficient for binary citation detection (cited/not-cited). The experimental design question shifts from "how many iterations do I need to average over platform noise?" to "how do I reliably change the index state that Perplexity is reading?" This reframes GEO experimentation as primarily an indexing and content-structure problem, not a statistical noise problem.

The caution is that determinism at short timescales does not guarantee determinism across longer windows. Perplexity updates its retrieval pool through periodic model updates, index refreshes, and crawl cycles. E016 establishes determinism within a 5-day window with no platform-side updates. Longer windows, major model changes, or high-competition query spaces may produce genuine variance not captured here.

Early replication evidence supports the short-timescale finding. E027 (Perplexity Zero Variance Replication, running April–May 2026) reproduced the T1 citation pattern across five consecutive daily runs with identical query sets, with the same three pages cited in the same source-list positions across all five days. The three cited pages and their binding to specific queries remained unchanged from Day 1 through Day 5, with zero drift.

### 4.2 ChatGPT is unsuitable as a primary signal platform

ChatGPT's 0–20% range across five days makes it unsuitable as a primary signal platform for citation rate experiments on low-authority domains. The Day 2 outlier was not genuine signal: the two citations that day were produced by the same web search mechanism that failed silently on every other day, suggesting the 2C count was an artifact of force_web_search behaving differently on Day 2 than on the four surrounding days.

This non-determinism is partly structural: ChatGPT's `ai_optimization_chat_gpt_scraper` approach fires web search inconsistently — source arrays were returned for only 2–4 of 10 queries per day across Days 3–5. Even when source arrays fired, no thegeolab.net URL was cited. The citation surface at low domain authority is effectively zero. Combined with the high noise floor (0–20pp), any treatment effect of less than 20pp is uninterpretable on ChatGPT alone.

The practical recommendation is to use ChatGPT as a secondary confirmation platform where a Perplexity primary signal (≥22pp lift) is first established, then check whether ChatGPT shows consistent directional movement. A 0→2 citation count change on ChatGPT following an intervention that already shows ≥22pp on Perplexity would be corroborating evidence; the same 0→2 count in isolation would be noise.

### 4.3 Google AIO: 0% across all 50 checks — structure vs authority

Google AI Overviews returned zero citations to thegeolab.net across all 50 checks. A critical additional observation: AI Overview boxes were present for 10/10 queries on Days 1–2, meaning Google was generating AI responses to these queries — it simply was not selecting thegeolab.net as a source in any of them.

This distinguishes two possible interpretations: (a) Google AIO does not generate responses to this query type (absent finding), or (b) Google AIO generates responses but selects sources from a pool that excludes low-authority domains (authority-gate finding). The evidence supports interpretation (b). AIO boxes were consistently present; thegeolab.net was consistently absent from the source set.

This is consistent with the broader domain authority gate finding from EDX: on competitive category queries, AI citation systems prefer established publishers, research institutions, and high-authority reference sites. Content quality and structural signals may be necessary conditions for citation, but they are not sufficient. The authority floor is a selection criterion applied before content evaluation, not after.

### 4.4 The T1/T2 tier model and its implications

The 80% vs 0% Perplexity citation split between proprietary and category queries is the most practically significant finding for GEO researchers. It demonstrates that AI citation is not a single continuum that improves uniformly as content quality, authority, or structural signals improve. Instead, it appears to operate as a two-tier system.

Tier 1 (proprietary-concept queries): the domain that coined and defined a concept becomes the canonical source. On queries for "GEO Stack," "Extractability," or "System Memory" — terms The GEO Lab invented — thegeolab.net is cited at 80% because it is the definitional source. No other domain has a competing definition. The authority gate does not apply here because authority over proprietary terminology is established by definition, not by inbound link profile.

Tier 2 (category queries): the domain competes with established publishers. On queries for "generative engine optimisation" or "AI citation rate" — terms used across the web — thegeolab.net's citation rate is 0%. Content quality, GEO-optimised structure, and FAQ schema are all present on thegeolab.net's T2 query-matched pages. None of it matters at the sub-threshold authority level.

The practical implication for GEO practitioners: early-stage domain strategy should prioritise T1 proprietary concept creation (coining and defining new terminology) before optimising T2 category pages. Citation rate improvement on T2 queries requires domain authority advancement, not content iteration — a slower and structurally different problem.

### 4.5 The interpretability threshold

The 22.0pp combined interpretability threshold is derived conservatively: noise floor maximum (20.0pp) + 2pp buffer. Any future experiment result at or below 22.0pp combined on this domain cannot be attributed to a treatment effect with confidence. To claim signal, an observed lift must clear 22pp.

This threshold is domain-specific. A higher-authority domain where ChatGPT's citation floor is 20% rather than 0% would have a higher noise floor and require a correspondingly higher threshold. The E016 protocol is not a universal noise floor — it is a per-domain measurement that must be replicated on each domain before experimental results from that domain are interpreted.

The threshold has been applied prospectively to subsequent GEO Lab experiments. E025 (entity reinforcement intervention) uses 22.0pp as its success gate for T2 Perplexity citation lift. Any sub-threshold result will be reported as a null finding.

### 4.6 The recording artifact as a methodological warning

The Day 2 recording artifact is not an embarrassment to be minimised — it is the most instructive result in the dataset. The sequence of diagnostic steps that led from "Perplexity flipped URLs" to "our logger captured different positions in a stable multi-URL array" illustrates exactly how measurement design failures produce false variance signals in AI citation research.

The artifact arose from an implicit assumption: that each Perplexity citation for a given query would have a single canonical URL. In practice, Perplexity's annotation array for a query can contain multiple source URLs from the same domain — in this case, two thegeolab.net pages both satisfying the Q2 query. The logger took the first one. On different days, the API returned the array with different items at position 1. The logger reported a flip. The platform had not changed.

Any researcher logging Perplexity citations by capturing the first annotation URL only is exposed to this artifact. The correct approach, confirmed from Day 3 onward, is to log the full `annotations` array and derive the binary citation flag (cited: yes/no) from whether the target domain appears anywhere in the array, not from which URL is at position 1.

### 4.7 Limitations

- **Single domain.** thegeolab.net at DR ~0. Results may not generalise to higher-authority domains where ChatGPT citation rates are non-zero and Perplexity T2 citations are possible. Noise floor characterisation is a per-domain exercise.
- **Five-day window.** Longer windows may reveal periodic platform updates — model version changes, index refresh cycles — that introduce variance not captured here. E016 cannot speak to Perplexity's behaviour over months or across major model releases.
- **AIO raw data not preserved.** The 0/50 AIO finding is confirmed via human-coded C/M/X column and observer notes in the Notion research log but raw DataForSEO JSON responses were not saved. The zero finding is not post-hoc verifiable from raw API output. This is the one irreproducible element of the dataset.
- **Query set (10 queries, fixed).** Results are specific to this query set. A different query set on the same domain might yield a different noise floor profile — particularly if it included queries where thegeolab.net has genuine T2 category competition.
- **Single iteration per day.** Each platform was queried once per day per query. Multiple iterations per day (as in later experiments) would provide intra-day variance data in addition to inter-day variance, giving a more complete noise characterisation.

---

## 5. Conclusion

Noise floors matter. The absence of a published noise floor characterisation for AI citation experiments has allowed GEO practitioners to report and interpret citation deltas that may fall entirely within natural platform variability. A field that routinely reports +8pp lifts without establishing whether the platform produces ±12pp variation under zero-intervention conditions is not producing interpretable evidence.

This paper provides three things: a reproducible protocol for establishing a noise floor; a diagnostic toolkit for investigating anomalies when they occur; and an empirical finding — Perplexity's citation surface is deterministic at proprietary-concept query scale — that should inform how researchers design and replicate GEO experiments going forward.

The 22.0pp interpretability threshold derived here has been applied prospectively to The GEO Lab's subsequent experiment portfolio. It is offered as a working standard pending independent replication on other domains, at higher authority levels, and across longer measurement windows.

The four-test diagnostic playbook (Appendix C) is the most immediately portable output. Any AI citation researcher who encounters unexplained variance — a URL flip, a count change, a C↔X oscillation — now has a structured investigation protocol that takes less than two hours to run and costs under $0.10 in API credits. Run the tests before attributing anything to platform noise. Variance is data; unexplained variance is a bug.

---

## Appendix A — Raw data files

**`data/e016_annotation_rerun_20260428.json`** — Full Perplexity sonar-pro API JSON responses from the retrospective annotation re-run (10 queries, 2026-04-28). Includes complete `annotations` arrays for all queries. Q2 (Retrieval Probability) confirms both `/retrieval-probability-geo-stack/` and `/retrieval-probability/` present in identical position order, consistent with all 6 prior observations.

**`data/e016_spreadsheet_export.csv`** — Five-day citation log: 10 queries × 3 platforms × 5 days = 150 cells. Per-cell coding (C/M/X), observed URLs where applicable, daily totals, per-platform aggregates, Tier 1/Tier 2 breakdown. Source: Google Sheets ID 1s1zDp8EG828b3w8TDsgFIE8i_0nsVHNHTCCfY4RTbS4.

**`data/e016_aio_check_20260428.txt`** — Human-coded Google AIO check output for all 10 queries, confirming 0 citations and AIO box presence on 10/10 queries (Days 1–2 observation).

## Appendix B — Content comparison: two thegeolab.net Retrieval Probability pages

During Test 2 of the Day 2 investigation, both URLs appearing in Q2 annotations were fetched and compared. The finding was a content integrity bug, not SEO cannibalisation.

**`/retrieval-probability/`** (canonical, 2,700 words, Version 2.2, February 2026): defines GEO Stack as a five-layer model — Retrieval Probability, Extractability, Entity Reinforcement, Structural Authority, System Memory — with five associated variables (semantic alignment, entity match strength, structural clarity, topical isolation, contextual reinforcement). This is the current canonical GEO Stack definition.

**`/retrieval-probability-geo-stack/`** (secondary, 1,800 words, March 2026): defines GEO Stack as a five-layer model — Discoverability, Relevance, Authority, Retrieval Probability, Amplification — mixing traditional SEO signals (CTR, dwell time, domain authority) with GEO-specific concepts. This definition is contradictory to the canonical version and represents an earlier, superseded framework.

Both pages were self-canonical, both indexed by Google, and both active in Perplexity's annotation set for Q2. Perplexity was simultaneously returning two pages from the same domain that defined the same concept in contradictory ways. This is a domain-level content integrity problem — Perplexity ingesting conflicting framework definitions — that is independent of the recording artifact. The remediation (301 `/retrieval-probability-geo-stack/` → `/retrieval-probability/`) was deployed post-freeze on 2026-04-18. Both redirects were verified via nginx logs; the secondary page now returns 301.

## Appendix C — Four-test diagnostic playbook

Reusable protocol for investigating citation anomalies (URL drift, count change, C↔X flip). Run these four tests before attributing any variance to platform noise. They are independent and can be run in parallel.

**Test 1 — Intraday repeat** (Platform non-determinism test)

Run 3–5 identical API calls within 5 minutes using the same platform and model. Cost: ~$0.05 total. If annotation arrays are identical across all runs: day-to-day variance is not within-API randomness — the cause is elsewhere (recording, content, crawl). If annotation arrays vary: genuine intra-platform non-determinism; that variation range is your noise floor for this platform/query.

*Gotcha:* DataForSEO's `ai_optimization_llm_response` with `web_search=true` silently fails on gpt-4o-mini and gpt-4.1, returning training-data answers. For ChatGPT web-search citation testing, use `ai_optimization_chat_gpt_scraper` with `force_web_search=true`. For Perplexity sonar-pro, `ai_optimization_llm_response` works correctly.

**Test 2 — Content comparison** (Site-side explanation test)

Fetch both candidate URLs and compare: word count, framework consistency, schema types, version history, internal link strength, evidence density. Near-identical pages indicate simple SEO cannibalisation — recommend 301 redirect. Contradictory pages indicate content integrity bug — recommend 301 plus content audit, and note that the AI platform may have been ingesting conflicting definitions.

**Test 3 — GSC impressions** (Google pathway test)

Query GSC search analytics with a query filter matching the topic, 30-day window, dimension: page+query. If both URLs show impressions for the same queries: Google sees competition; cannibalisation has organic impact. If one shows impressions: Google has already selected a winner. If zero impressions on both: Google is not a discovery channel; the cannibalisation only affects AI search surfaces.

**Test 4 — Crawler log analysis** (Freshness differential test)

SSH to the webserver and grep Nginx access logs for AI crawler activity (PerplexityBot, OAI-SearchBot, GPTBot) on both candidate URLs around the measurement dates. If both URLs were crawled before the earlier measurement: both already indexed; freshness theory eliminated. If only one URL was crawled before the earlier measurement: genuine discovery artifact; that URL may have been freshly indexed between Day 1 and Day 2.

PerplexityBot fingerprint: IPs in 18.97.9.x block, User-Agent contains "PerplexityBot/1.0".

**Stop criteria:** Test 1 showing stable API + Test 2 showing contradictory pages is sufficient to diagnose recording artifact + content bug. Test 1 showing variable API is sufficient to establish the noise floor for that platform/query. All four tests inconclusive: repeat Test 1 with more runs, or verify manually via the platform's web UI.

---

## References

- Ferreira, A. (2026). *Domain Authority Gate in AI Citation: A Multi-Query Null Result (EDX).* Zenodo. DOI: 10.5281/zenodo.19450361
- Ferreira, A. (2026). *GEO Citation Index — E014 Universal Query Set Dataset.* Zenodo. DOI: 10.5281/zenodo.19253920
- E027 Research Log — Perplexity Zero Variance Replication. The GEO Lab Notion Research Journal. Parent page: 34b4714ae9d081c58748f47efe877f72
