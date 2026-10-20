# Pre-registration: E097 (reworked)

**When two pages are byte-identical except for the URL slug, do ChatGPT and Perplexity cite them as distinct pages, and if so does the slug change which is cited?**

Version 1.4. Correction version of v1.3, deposited before any capture call was run under any version. It supersedes v1.3 (10.5281/zenodo.22899397); all versions sit under concept DOI 10.5281/zenodo.22899396. The changes are listed in section 1. This document is the frozen record. Any change during capture or analysis is reported as a deviation, not folded into the method.

**Creators**
Artur Ferreira, The GEO Lab, ORCID 0009-0004-4072-9741 (pages, manipulation, frozen query set, this pre-registration, analysis)
Marwa Saleh, LeapOne, ORCID 0009-0008-8525-2747 (capture pipeline, browse pre-checks, all calls, per-call model log, Perplexity browse-rate characterisation)

**Licence** CC BY 4.0. **Venue** Zenodo. **Freeze tag** `e097-prereg-v1.4`. T0 is the deposit date of this document and replaces the v1.3 T0. No capture runs before T0.

---

## 1. What changed, and why

**v1.4** (pre-capture; no scored call has been run under any version). Corrections and additions that follow the co-author's characterisation of the capture path (reviews of 30 Sep, 1 Oct, 14 Oct and 16 Oct 2026). The field semantics in item 1 were checked against OpenAI's published Responses API documentation. The query-string behaviour in item 2 and the Perplexity behaviour in item 3 are the co-author's observations, not independently checked.
1. **ChatGPT outcome corrected (2.4).** v1.3 scored the sources array as the primary outcome and called it cited. That field lists the pages the search consulted, in one typical call on gpt-5.6-luna, about 28 consulted and about 6 cited; about 2 cited per call on gpt-6-luna, so the primary would have measured surfacing and labelled it citation. The primary is now the url_citation annotations. The consulted list is secondary and the request must ask for it explicitly. The search_results field named in v1.3 does not exist on this path and is removed.
2. **URL matching widened (2.4).** Cited ChatGPT URLs can come back with a query string appended. The rule now removes the query string and fragment as well as normalising the trailing slash.
3. **Perplexity outcome defined (2.4).** v1.3 said only "the citations list". By default Perplexity does not mark which of its results it used: there are no numbered markers, the annotations are empty and every answer carries 15 results, so the default signal is surfacing. The prompt now carries a citation instruction, identical for both arms, and the numbered markers in the answer are the cited outcome. The results list is the secondary outcome.
4. **Model pin changed (2.1)** for the ChatGPT arm from gpt-5.6-luna to gpt-6-luna, with a retirement clause. Reasoning effort (medium) and the output limit (4000 tokens) are pinned, and a call cut off by the limit is a failed call that is re-run, never scored as not cited.
5. **Browse rates corrected (2.2).** The expectation that ChatGPT browses near-universally is replaced by the measured rates.
6. **Browse pre-check and reserve query list added (2.2, 4a).**
7. **Citation floor added (2.4)**, per engine.
8. **Body md5 scope corrected (2.1).** The md5 quoted in v1.3 is the md5 of the whole exported page-source file, not the `post_content` column.
9. **One capture window, and the sibling timing limitation removed (2.1, 7).**
10. **Transparency standard extended (6).**
11. **Decision rules restated (3).** The branch rules now read the cited outcome, require the citation floor before any branch is read, and give Branch 2 a registered number where v1.3 said "near zero" and "essentially all". The 15% threshold for Branch 1 and the 22-point escalation threshold are unchanged. The "neither-heavy" outcome is now defined by the citation floor. The page-build reference in section 5 is corrected (commit d6a6249, which fixed the freeze text, is replaced by the page-source commit 55ac913 and the publish commit baa06e9), and the sequence in section 8 is updated.
12. **Perplexity cite-instruction string inserted (2.4).** The verbatim instruction text, its placement in the `instructions` field and the marker-reading rule were inserted from the co-author's 16 Oct message.
13. **Surfaced-list check before Branch 2 added, per engine (3).** Pre-check size clarified for E097 and E100 queries (2.2). API-error rule added to the cap (2.1). Tool retirement clause extended to `web_search_preview` (2.1).

**From v1.2.1 to v1.3 (text unchanged):**

E097 tests whether a descriptive URL slug lifts citation versus an opaque slug, content held identical. The two arms therefore carry byte-identical bodies and differ only in slug (`https://thegeolab.net/guides/hreflang-and-ai-search-explained/` vs `https://thegeolab.net/guides/p48213/`, same folder).

Both arms went live 11 September 2026, 08:00 UTC, both 200, both self-canonical, both indexable, all confirmed by direct request. But **Google merged them**: Search Console reports arm B as "Duplicate, Google chose different canonical than user", arm A chosen as canonical, held across 14 and 16 September, arm B not re-crawled after 11 September. That is a clean failure of E097's registered pre-T0 gate (both arms indexed on separate paths).

Two consequences follow, and both are registered here rather than worked around:

1. **Gemini and AI Overview are removed.** Both read from Google's index, which now holds only arm A as canonical. Neither can test a slug effect on a pair Google has already collapsed. This removal follows the co-author's 23 August point about index dependence, not budget. E097 runs on **ChatGPT and Perplexity only**.
2. **The question is reframed.** With the pair known to be a duplicate in at least one major index, the first thing worth measuring is whether the AI engines also consolidate identical bodies, which is itself unmeasured. So E097 no longer registers only as a slug-lift test; it registers a duplicate-handling outcome set (section 3) with the slug test live only on the branch where the engines treat the pages as distinct.

The Google folding itself, two byte-identical pages with correct self-canonicals merged regardless, is recorded as a standalone finding in the deposit and in the E100 record.

## 2. Design

### 2.1 Structure and engines
- Two arms, matched pair on thegeolab.net, one topic (hreflang and multilingual content in AI search). Body byte-identical on both arms; slug is the only intended difference.
- Body check. The live database `post_content` for both arms has md5 `56d4f3939b053548331def4c307f5e73`, 7503 bytes, identical on both arms, `post_modified_gmt` 2026-09-11 08:00:41, re-checked unchanged on 16 Oct 2026. The value `b60dcb77d76576eb9120789892cce50c` quoted in v1.3 is the md5 of the whole exported page-source file (`e097/page-source-arm-a.html` and `-b.html`, identical to each other), not of `post_content`. Reproduction script: `e097/verify/body_md5.py`.
- Engines: **ChatGPT** (`gpt-6-luna`, `web_search_preview` enabled, with the `include` parameter set to return `web_search_call.action.sources` on every call) and **Perplexity** (`perplexity/sonar`, no presets). ChatGPT reasoning effort is `medium`, sent explicitly on every call, with the effort the API reports back logged next to the model name; it is the API default for gpt-6-luna when none is set (co-author's check, 16 Oct 2026) and the setting her probes ran at. `max_output_tokens` is 4000 for the ChatGPT arm: reasoning tokens count toward the limit, and in her probes the longest answer used 1,300 tokens and two re-runs of the longest-answer query used 1,473 and 1,736. A ChatGPT call whose response status is `incomplete` (cut off by the limit) is a failed call, not an observation: it is never scored as "arm not cited", it does not count toward the 80 browsed observations, it is re-run for the same query, every attempt counts toward the 160-call cap, and the number of incomplete calls is reported per query. API errors with no response, such as a timeout or a rate limit, are logged, re-run, never scored, and counted toward the 160-call cap. OpenAI lists a single `gpt-6-luna` identifier and no dated snapshot, so the pin is the requested identifier together with the returned model string logged on every call.
- Perplexity scope: Perplexity API, Sonar model, accessed through the Agent API, not the consumer app. The earlier Sonar API was retired on 27 Sep 2026; `perplexity/sonar` continues to work on the Agent API (co-author's check, 1 Oct 2026). "No presets" is stated because presets can route a call to another vendor's model.
- Frozen query set Q = 8 (section 4). Capture unit = 1 query x 1 render x 1 engine. Both arms compete inside the same answer, so one call yields one observation per arm.
- Returned model logged on every call; a mid-capture change in the returned model (or, for ChatGPT, the returned reasoning effort) flags the window, decided from the log.
- Retirement clause: if a pinned model is retired, or the model (or, for ChatGPT, the reasoning effort) the API returns changes from the one recorded in the browse pre-check, before the first scored call, capture does not run for that engine. If the `web_search_preview` tool is refused or retired before capture, capture does not run. A re-pin is a new version of this document, with its own deposit and T0.
- Single capture window: both engines, and the E100 capture, run as one session. The start and end timestamps (UTC) are recorded and deposited with the results.

### 2.2 Target N, stopping rule and browse pre-check
The registered floor is **80 usable observations per arm per engine**, where usable = the call browsed (returned a search-results list). This is a stopping rule, not a fixed call count, because Perplexity browses on only some calls (section 2.3):

- Capture continues on each engine until 80 browsed observations per arm are reached.
- Hard cap **160 calls per engine**. If the cap is hit before 80 browsed observations, capture stops and the achieved usable N is reported as the registered N for that engine.
- The stopping criterion (count of browsed calls) is outcome-blind: it does not look at whether either arm was cited, only at whether the call searched.
- Top-up allocation: renders beyond the initial 10 per query, needed when non-browsing calls leave an engine short of 80 browsed observations, are added by cycling the frozen query order (query 1, 2 ... 8, then 1, 2 ... again). Allocation is fixed in advance, not decided mid-capture.

Measured browse rates (co-author's characterisation). Perplexity: about 6 in 10, from a 34-call pre-check (34/34 completed, all `perplexity/sonar`, no rate limits, about 9s median latency, browsed on 20 of 34), so 80 browsed observations are expected at around 130 to 135 calls and, at the low end of about 4 in 10, about 190 calls, which would reach the 160-call cap. ChatGPT: 17 of 24 probe calls browsed on gpt-5.6-luna (71%) and 24 of 24 on gpt-6-luna with the same probes, so about 80 calls on gpt-6-luna. Two query shapes (structural twins of frozen queries 1 and 2 in E100) browsed 0 of 3 on gpt-5.6-luna. These rates are the co-author's measurements, not independently reproduced. The rule is identical on both engines so it is not engine-specific.

Browse pre-check (registered before capture, run after this document is deposited and before the first scored call): the co-author runs it on her harness with the pinned models and settings, covering both engines and the E100 queries in the same session. For ChatGPT, each frozen query is asked twice; if neither call browses it is asked twice more, and the query is declared dead only if all four calls fail to browse. For Perplexity, because the browse rate is lower (about 6 in 10), the same rule runs to six calls: a query is declared dead only if all six fail to browse, which keeps the false-dead probability across eight queries to about 4% (0.41 to the sixth power is about 0.005 per query), against about 21% at four calls. A dead query is replaced by the next unused query in the reserve list (section 4a), in the listed order. Each substitution is recorded in the deposit before capture starts. The pre-check reads the browse flag only: no arm is scored, no citation outcome is read, and the raw responses are deposited unscored. Pre-check calls do not count toward the 80 browsed observations or the 160-call cap. Expected pre-check size for E097 queries: 32 to 80 calls across both engines. The E100 queries add 16 to 32 calls in the same session.

### 2.3 Denominator rule (browse gate)
A call that did not browse (no search-results list) cannot cite either arm and is dropped from the denominator, not scored as a zero for both arms. This extends the cross-engine no-browse rule to Perplexity, where it bites hardest. The co-author confirmed the forced-tool parameter is accepted but inert (3/6 browsed with it vs 4/8 without), so it is not used; the browse rate is taken as the engine's own behaviour.

### 2.4 Outcome measure
Per browsed call, each arm is scored cited / not cited, on the following definitions.

**ChatGPT.** Primary (cited): the arm's URL appears among the url_citation annotations of the response. Secondary (surfaced but not cited): the arm's URL appears in the list of pages the search consulted, `web_search_call.action.sources`, which is returned only when the request sets the `include` parameter for it. In the co-author's characterisation every cited page is also in the consulted list, so the primary is the stricter outcome.

**Perplexity.** Primary (cited): the arm's URL is among the results whose numbered marker appears in the answer text. Secondary (surfaced but not cited): the arm's URL appears in the results list (an `output[]` item of type `search_results`, with `results` entries carrying url, id, title, snippet, source, date and last_updated). The numbered markers are produced only when the prompt asks for them, so every Perplexity call carries the same citation instruction in the same position, identical for both arms and for every query, and the primary outcome is defined only for calls with that instruction. Instruction text, quoted verbatim from the string the co-author tested: `Cite your sources inline using bracketed markers, one source per bracket, like [1][2].` Placement: the string is sent in the instructions field of Perplexity's Agent API, and the question goes in input, word for word as for ChatGPT, so the question text is identical across engines and arms. The wording is Perplexity's own suggested wording from its web-search tool documentation (docs.perplexity.ai/docs/agent-api/tools/web-search). The documentation suggests appending it to the prompt; it is placed in instructions instead so the question itself is unchanged. Each [n] marker is read as the id of a result in search_results, as the documentation describes. A marker that points to no result is logged and not counted. The string was tested in September 2026 on 4 calls using questions outside the study; each answer marked 2 of its 15 results. Asymmetry stated: the ChatGPT primary is the engine's own citation annotation, whereas the Perplexity primary is produced under an instruction that Perplexity does not apply by default; the two primaries are comparable as "which sources the answer credits" but not identical as instruments. The instruction cannot favour one arm because it is identical across arms and refers to no URL.

This yields, per browsed call and per engine, on the primary definition, exactly one of four joint outcomes: **both cited**, **A only**, **B only**, **neither**. The same four-way outcome is also computed on the secondary (surfaced) definition and reported; the primary is the registered read.

**URL matching rule (registered before capture):** a returned URL is matched to a registered arm address after removing any query string and fragment and normalising a trailing slash on the path, so `/guides/hreflang-and-ai-search-explained`, `/guides/hreflang-and-ai-search-explained/` and `/guides/hreflang-and-ai-search-explained/?utm_source=openai` are treated as the same address (and likewise for arm B). Scheme and host are compared as returned. This applies identically to the ChatGPT annotation match, the ChatGPT consulted-list match and the Perplexity match. The raw returned URL is logged verbatim on every call, so any match can be re-derived either way from the deposited log. No other normalisation is applied.

**Citation floor (registered before capture), per engine:** let n be the number of usable observations per arm on that engine (browsed calls; the achieved N if the 160-call cap binds). The registered detectable difference is 22 percentage points. A 22 point difference between arms cannot be shown unless at least ceil(0.22 x n) browsed calls cite one or both arms; at n = 80 that is 18. If fewer calls than the floor cite either arm on an engine, the primary outcome for that engine is declared uninformative, no difference between arms is claimed for it, and the surfaced outcome is reported as its own finding (pages retrieved but not cited). The decision rules in section 3 operate on the primary outcome; when the floor is not met, section 3 sets out what is read instead.

## 3. Registered outcome set and decision rules

The joint-outcome distribution across browsed calls is the primary registered result, read on the cited outcome (2.4), per engine. Its reading is fixed before capture:

**Citation floor (checked first, per engine).** The branches below are read only on an engine where at least ceil(0.22 x n) browsed calls cite one or both arms (2.4; 18 at n = 80). An engine that does not meet the floor falls under the neither-heavy outcome below.

**Branch 1, engines treat the pages as distinct.** If "both cited" occurs at a non-trivial rate (pre-registered threshold: both-cited on at least 15% of browsed calls where either arm is cited, per engine), the slug hypothesis is live. Test the original prediction: citation rate A minus B, per engine, with a 95% two-proportion CI, against the 22-point noise floor. Interval including zero or point estimate below 22 points = null. This is the mechanism-(a) slug test as originally registered.

**Branch 2, engines consolidate the pair.** If "both cited" is below 15% of browsed calls where either arm is cited, and one arm accounts for at least 80% of the browsed calls in which exactly one arm is cited, the engine is deduplicating identical bodies the way Google did. Register which arm it keeps and whether that matches Google's canonical choice (arm A). This is the duplicate-handling finding: how AI answer engines treat byte-identical pages, and whether they inherit Google's consolidation. Reported per engine; the two engines may differ.

Before Branch 2 is read as a dedup result for an engine, that engine's surfaced lists are checked. If both arm pages are surfaced together (the arm's URL appears in `web_search_call.action.sources` for ChatGPT or in the `search_results` results list for Perplexity) on 15% or more of that engine's calls in which either arm page is surfaced, the result for that engine is reported as "both seen, one preferred". No dedup claim is made and there is no escalation.

**Neither branch.** If "both cited" is below 15% of browsed calls where either arm is cited and no arm reaches 80% of the single-arm calls, the four counts are reported and nothing is interpreted.

**Neither-heavy outcome.** If the citation floor is not met (the pages simply are not competitive for these queries on this engine), report as non-competitive and draw no slug or dedup conclusion. This protects against reading a coverage null as either finding. For that engine the same four-way table, with the 15% and 80% measures, is also reported on the surfaced outcome (2.4), labelled as retrieval, descriptively and without a slug or dedup conclusion about citation.

**Escalation.** A crossover design (distinct bodies with matched structure, crossing slug with body) is registered follow-up. It fires only from Branch 1 on the cited outcome, and only if A leads B by at least 22 points. It never fires from Branch 2, the neither branch, the neither-heavy outcome or a surfaced read. Registering it now prevents a post-hoc "the slug worked" read of what might be a dedup or coverage effect.

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

### 4a. Reserve queries

They went through the same collision and Goldilocks gates as the frozen eight (collision grep on the site database, content-word overlap against the frozen sets of both experiments, a check that the arm page body contains the query's key terms, and a search-results saturation read on 16 October 2026, before any capture call). They are listed in the fixed substitution order, chosen from the gate evidence and not from any capture result. A frozen query that fails the browse pre-check (2.2) on an engine is replaced, for that engine, by the first unused reserve, and so on down the list. The list is deposited unscored. The same query strings are used on ChatGPT and Perplexity.

1. does machine translation hurt citations in AI search
2. should multilingual sites let AI crawlers reach every language version
3. does a mixed-language page confuse AI search engines
4. do automatic language redirects hurt AI search visibility

None of the reserves contains the word hreflang, so a substitution lowers the share of queries that contain it (3 of 8 in the frozen set). Any substitution is reported with the resulting count.

A fifth candidate, "does hreflang help AI answer engines find the right page", was tested and rejected before registration (50% content-word overlap with frozen query 1, and the results page already holds a multi-engine hreflang test very close to this design). If all four reserves are used and a frozen query is still dead on an engine, that query is dropped for that engine, and the drop is reported.

## 5. Gates
- The pages are already live and byte-identical (page sources committed 10 September, commit `55ac913`; published live 11 September 2026, 08:00 UTC; freeze manifests at tag `e097-e100-pages-frozen`, commit `baa06e9`).
- The Google index gate is known failed and is the reason for this rework; it is not re-run as a pass condition. The relevant live condition for ChatGPT and Perplexity is that both arms remain fetchable (200, indexable) through capture, which is verified by direct request, not via Google's index.
- Abort: if either arm returns non-200 or noindex during capture, that engine-window is voided.

## 6. Transparency standard
Deposited with results: raw API responses for all calls unedited; the per-call model log (requested and returned model, and for ChatGPT requested and returned reasoning effort and response status); the per-call browse flag (browsed / did not browse); which response fields were present on each call; the exact request specification for each engine, including the `include` parameter and the full Perplexity prompt with its citation instruction; every script used to produce every figure; the resolved URL match per call; and the start and end timestamps (UTC) of the capture session. The browse pre-check responses are deposited unscored, with the substitution record if any query was replaced.

## 7. Sibling note (descriptive)
E097's sibling E100 (post-H1 snippet window; concept DOI 10.5281/zenodo.22849118) is registered separately. Both experiments are captured in the same session, on one harness, with the same pinned ChatGPT model and a shared browse pre-check, so timing is controlled between them. Any E097/E100 comparison remains descriptive only, because the topics differ (always intended). Kept as context, not a claim.

## 8. Sequence
(1) Co-author reads this file and confirms the stopping rule, the outcome set and the decision rules in this file; (2) deposit as v1.4, which sets T0; (3) browse pre-check on the co-author's harness for both engines (2.2), with the raw responses deposited unscored and any substitution recorded before the first scored call; (4) capture week named with several days' notice, as one session shared with E100 (2.1, 7); (5) capture to the stopping rule; (6) analysis and write-up. This record does not touch the shared September Gemini allowance (no Gemini), so it carries no September timing constraint.
