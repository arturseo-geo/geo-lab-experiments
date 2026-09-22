# Pre-registration: E097 (reworked)

**When two pages are byte-identical except for the URL slug, do ChatGPT and Perplexity cite them as distinct pages, and if so does the slug change which is cited?**

Version 1.3. Reworked from the joint E097/E100 pre-registration v1.2.1 after E097 failed its Google index gate before deposit. This document is the frozen record. Any change during capture or analysis is reported as a deviation, not folded into the method.

**Creators**
Artur Ferreira, The GEO Lab, ORCID 0009-0004-4072-9741 (pages, manipulation, frozen query set, this pre-registration, analysis)
Marwa Saleh, LeapOne, ORCID 0009-0008-8525-2747 (capture pipeline, all calls, per-call model log, Perplexity browse-rate characterisation)

**Licence** CC BY 4.0. **Venue** Zenodo. **Freeze tag** `e097-prereg-v1.3`. T0 is the deposit date of this document. No capture runs before T0.

---

## 1. What changed from v1.2.1, and why

E097 tests whether a descriptive URL slug lifts citation versus an opaque slug, content held identical. The two arms therefore carry byte-identical bodies and differ only in slug (`https://thegeolab.net/guides/hreflang-and-ai-search-explained/` vs `https://thegeolab.net/guides/p48213/`, same folder).

Both arms went live 11 September 2026, 08:00 UTC, both 200, both self-canonical, both indexable, all confirmed by direct request. But **Google merged them**: Search Console reports arm B as "Duplicate, Google chose different canonical than user", arm A chosen as canonical, held across 14 and 16 September, arm B not re-crawled after 11 September. That is a clean failure of E097's registered pre-T0 gate (both arms indexed on separate paths).

Two consequences follow, and both are registered here rather than worked around:

1. **Gemini and AI Overview are removed.** Both read from Google's index, which now holds only arm A as canonical. Neither can test a slug effect on a pair Google has already collapsed. This removal follows the co-author's 23 August point about index dependence, not budget. E097 runs on **ChatGPT and Perplexity only**.
2. **The question is reframed.** With the pair known to be a duplicate in at least one major index, the first thing worth measuring is whether the AI engines also consolidate identical bodies, which is itself unmeasured. So E097 no longer registers only as a slug-lift test; it registers a duplicate-handling outcome set (section 3) with the slug test live only on the branch where the engines treat the pages as distinct.

The Google folding itself, two byte-identical pages with correct self-canonicals merged regardless, is recorded as a standalone finding in the deposit and in the E100 record.

## 2. Design

### 2.1 Structure and engines
- Two arms, matched pair on thegeolab.net, one topic (hreflang and multilingual content in AI search). Body byte-identical (md5 `b60dcb77d76576eb9120789892cce50c` both arms); slug is the only intended difference.
- Engines: **ChatGPT** (`gpt-5.6-luna`, `web_search_preview` enabled, `max_output_tokens` 3000) and **Perplexity** (`perplexity/sonar`, no presets).
- Frozen query set Q = 8. Capture unit = 1 query x 1 render x 1 engine. Both arms compete inside the same answer, so one call yields one observation per arm.
- Returned model logged on every call; mid-capture model change flags the window, decided from the log.

### 2.2 Target N and stopping rule
The registered floor is **80 usable observations per arm per engine**, where usable = the call browsed (returned a search-results list). This is a stopping rule, not a fixed call count, because Perplexity browses on only some calls (section 2.3):

- Capture continues on each engine until 80 browsed observations per arm are reached.
- Hard cap **160 calls per engine**. If the cap is hit before 80 browsed observations, capture stops and the achieved usable N is reported as the registered N for that engine.
- The stopping criterion (count of browsed calls) is outcome-blind: it does not look at whether either arm was cited, only at whether the call searched.
- Top-up allocation: renders beyond the initial 10 per query, needed when non-browsing calls leave an engine short of 80 browsed observations, are added by cycling the frozen query order (query 1, 2 ... 8, then 1, 2 ... again). Allocation is fixed in advance, not decided mid-capture.

At the co-author's measured Perplexity browse rate (~6 in 10, from a 34-call pre-check: 34/34 completed, all `perplexity/sonar`, no rate limits, ~9s median latency, browsed on 20 of 34), 80 browsed observations are expected around 130–135 calls, inside the cap. ChatGPT with search enabled is expected to browse near-universally and reach 80 in ~80 calls. The rule is identical on both engines so it is not engine-specific.

### 2.3 Denominator rule (browse gate)
A call that did not browse (no search-results list) cannot cite either arm and is dropped from the denominator, not scored as a zero for both arms. This extends the cross-engine no-browse rule to Perplexity, where it bites hardest. The co-author confirmed the forced-tool parameter is accepted but inert (3/6 browsed with it vs 4/8 without), so it is not used; the browse rate is taken as the engine's own behaviour.

### 2.4 Outcome measure
Per call, each arm is scored cited / not cited: the arm's URL in `sources[]` for ChatGPT (strict; `search_results[]` recorded as secondary surfaced-not-cited) and in the citations list for Perplexity. This yields, per browsed call, exactly one of four joint outcomes: **both cited**, **A only**, **B only**, **neither**.

URL matching rule (registered before capture): a returned URL is matched to a registered arm address after normalising a trailing slash on the path, so `/guides/hreflang-and-ai-search-explained` and `/guides/hreflang-and-ai-search-explained/` are treated as the same address (and likewise for arm B). Scheme and host are compared as returned. This applies identically to the ChatGPT `sources[]` match and the Perplexity citations-list match. The raw returned URL is logged verbatim on every call, so any match can be re-derived either way from the deposited log. No other normalisation is applied.

## 3. Registered outcome set and decision rules

The joint-outcome distribution across browsed calls is the primary registered result. Its reading is fixed before capture:

**Branch 1, engines treat the pages as distinct.** If "both cited" occurs at a non-trivial rate (pre-registered threshold: both-cited on at least 15% of browsed calls where either arm is cited, per engine), the slug hypothesis is live. Test the original prediction: citation rate A minus B, per engine, with a 95% two-proportion CI, against the 22-point noise floor. Interval including zero or point estimate below 22 points = null. This is the mechanism-(a) slug test as originally registered.

**Branch 2, engines consolidate the pair.** If "both cited" is near zero and one arm carries essentially all citations, the engine is deduplicating identical bodies the way Google did. Register which arm it keeps and whether that matches Google's canonical choice (arm A). This is the duplicate-handling finding: how AI answer engines treat byte-identical pages, and whether they inherit Google's consolidation. Reported per engine; the two engines may differ.

**Neither-heavy outcome.** If "neither" dominates (the pages simply are not competitive for these queries on this engine), report as non-competitive and draw no slug or dedup conclusion. This protects against reading a coverage null as either finding.

**Escalation.** A crossover design (distinct bodies with matched structure, crossing slug with body) is the registered follow-up. It fires only from Branch 1, and only if A leads B by at least 22 points. It never fires from Branch 2 or the neither-heavy outcome. Registering it now prevents a post-hoc "the slug worked" read of what might be a dedup or coverage effect.

## 4. Frozen queries (identical strings to both engines, no paraphrase)
1. how do AI search engines handle hreflang
2. does hreflang affect which language version AI search cites
3. how do AI assistants choose between translated versions of a page
4. do you need hreflang for AI search visibility
5. how to optimise a multilingual website for AI search
6. can AI search engines cite the wrong language version of a page
7. does AI search treat translated pages as duplicate content
8. which URL do AI search engines cite when a page exists in several languages

Scope: E097 does not implement hreflang. Each arm is a single English page whose subject is hreflang; there are no language variants and an arm is one URL. The topic is not the manipulation. Queries are English-only and generic informational, no local intent.

## 5. Gates
- The pages are already live and byte-identical (built 11 September, freeze tag carried forward from the joint build, commit `d6a6249`).
- The Google index gate is known failed and is the reason for this rework; it is not re-run as a pass condition. The relevant live condition for ChatGPT and Perplexity is that both arms remain fetchable (200, indexable) through capture, which is verified by direct request, not via Google's index.
- Abort: if either arm returns non-200 or noindex during capture, that engine-window is voided.

## 6. Transparency standard
Deposited with results: raw API responses for all calls unedited, the per-call model log, the per-call browse flag (browsed / did not browse), every script used to produce every figure, and the resolved URL match per call.

## 7. Sibling note (descriptive, cross-run)
E097's sibling E100 (post-H1 snippet window) deposits separately and captures in a different window. Any E097/E100 comparison is descriptive only and carries two stated limitations: different topics (always intended) and non-simultaneous runs (timing no longer controlled). Kept as context, not a claim.

## 8. Sequence
Co-author confirms the stopping rule and the outcome set in this file, then deposit (sets T0), then capture week named with several days' notice, then capture, analysis and write-up. This record does not touch the shared September Gemini allowance (no Gemini), so it carries no September timing constraint.
