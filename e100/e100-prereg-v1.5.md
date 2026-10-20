# Pre-registration: E100

**Does clearing non-body content from the post-H1 snippet window change whether ChatGPT cites a page, when the page body is held constant?**

Version 1.5 (E100-only). Correction version of v1.4, deposited before any capture call was run under any version. It supersedes v1.4 (10.5281/zenodo.22879130) and v1.3 (10.5281/zenodo.22849119); all versions sit under concept DOI 10.5281/zenodo.22849118. The changes are listed in the changelog. This document is the frozen record. Any change made during capture or analysis is reported as a deviation, not folded into the method.

**Creators**
Artur Ferreira, The GEO Lab, ORCID 0009-0004-4072-9741 (pages, manipulation, frozen query set, this pre-registration, analysis)
Marwa Saleh, LeapOne, ORCID 0009-0008-8525-2747 (capture pipeline, browse pre-check, all calls, per-call model log)

**Licence** CC BY 4.0. **Venue** Zenodo. **Freeze tag** `e100-prereg-v1.5`. T0 is the deposit date of this document and replaces the v1.4 T0. No capture runs before T0.

---

## Changelog

**v1.5 (before capture; no scored call has been run under any version):** Corrections and additions that follow the co-author's characterisation of the capture path (review of 30 Sep and 1 Oct 2026, updates of 14 and 16 Oct 2026). The field semantics in item 1 were checked against OpenAI's published Responses API documentation. The query-string behaviour in item 2 is the co-author's observation; the rule is harmless if it never occurs.
  1. **Outcome measure corrected (2.4).** v1.4 scored the sources array as the primary outcome and called it cited. That field lists the pages the search consulted, in one typical call on gpt-5.6-luna, about 28 consulted and about 6 cited; about 2 cited per call on gpt-6-luna, so v1.4's primary would have measured surfacing and labelled it citation. The primary is now the url_citation annotations. The consulted list is the secondary outcome and the request must ask for it explicitly. The search_results field named in v1.4 does not exist on this path and is removed.
  2. **URL matching widened (2.4).** Cited URLs can come back with a query string appended. The rule now removes the query string and fragment as well as normalising the trailing slash.
  3. **Browse rate corrected (2.1, 2.6).** v1.4 said the browse rate was expected to be near-universal. The co-author measured 17 of 24 probe calls browsing on gpt-5.6-luna (71%), and on gpt-6-luna the probes browsed 24 of 24 and the twins of frozen queries 1 and 2 browsed 3 of 3.
  4. **Model pin changed (2.2)** from gpt-5.6-luna to gpt-6-luna, with a retirement clause. Reasoning effort (medium) and the output limit (4000 tokens) are pinned, and a call cut off by the limit is a failed call that is re-run, never scored as not cited.
  5. **Browse pre-check and reserve query list added (2.1, 3a)**, so that a query that never triggers search is handled by a registered rule and not by a decision made during capture.
  6. **Citation floor added (2.4)**, ceil(0.22 x n), replacing any informal floor.
  7. **Phase 0 figures corrected (2.3).** The 728 offset and two snippet md5 values in v1.3 and v1.4 are withdrawn; see erratum commit da21809.
  8. **Shared-body md5 clarified (2.3):** the live-database value is now the canonical check, with a reproduction script.
  9. **One capture window, and the sibling timing limitation removed (2.1, 5):** E100 and E097 are captured in the same session.
  10. **Transparency standard extended (2.7).**
  11. **Analysis plan and sequence brought into line (2.5, 2.6, 4, 6).** The analysis plan now names the primary and secondary outcomes and the citation floor, and the sequence now includes the browse pre-check and the shared capture window. No change to the design, the arms, the query set or the 22-point threshold.
  12. **API-error rule added (2.2).** Tool retirement clause extended to `web_search_preview` (2.2). Changelog item 3 probe numbers updated to gpt-6-luna (24 of 24 probes, 3 of 3 twins).

**v1.4 (before capture):** registered the URL-matching rule. Comparison of a returned URL against a registered arm address ignores a trailing slash on the path, and the returned URL is logged verbatim per call (2.4). Aligned the 2.3 arm addresses to the live canonical, which carries a trailing slash. No capture had run at the time of this revision, so the registered protocol still equals the executed protocol. Same rule folded into E097 before its tag.

**v1.3 (E100-only):** this experiment was designed and reviewed as one half of a joint E097/E100 pre-registration (v1.2.1). E097 (URL slug) and E100 (post-H1 snippet window) shared a methods block and were to deposit together.

Both experiments' pages went live on 11 September 2026 at 08:00 UTC. On the two-path index check, **E097 failed its Google index gate**: its two arms carry byte-identical bodies, and although both are self-canonical, indexable, return 200, and were confirmed so by direct request, Google Search Console reports arm B as "Duplicate, Google chose different canonical than user", with arm A selected as canonical. The decision held across checks on 14 and 16 September, and arm B was not re-crawled after 11 September. E097's registered pre-T0 gate requires both arms indexed on separate paths; arm B does not meet it. E097 is therefore **withdrawn before deposit** and re-registered separately on a reduced engine set with its own outcome rules. It carries no deposit and no ORCID until that record is complete.

E100 passed both gates cleanly (see section 2.5) and is deposited here on its own, unchanged in substance from the reviewed joint version. The Google folding of the E097 pair is recorded as a finding in its own right: two byte-identical pages with correct self-canonicals were merged by Google regardless.

---

## 1. Hypothesis and prior

**Hypothesis (as registered):** the mechanism reported for ChatGPT (RESONEO/Abondance, Jul 2026) is that the model selects on the title plus a stored snippet of roughly 200 characters anchored on the H1. Clearing non-body elements from between the H1 and the first substantive sentence raises the share of on-topic text in that window and should therefore raise citation. This is the mechanism under test, not an established description of the system.

**What is measured (scope):** capture is the ChatGPT API with `web_search_preview` enabled (the pins in 2.2), not the consumer instant-mode UI. The snippet-window mechanism above is the origin hypothesis; this experiment tests whether clearing the post-H1 window shifts citation on the API path we can actually observe and log. Any claim is scoped to that path, not to instant-mode UI behaviour we do not measure.

**Prediction (before data):** directional, arm A (clean window) above arm B (clutter retained) on citation rate, within-site. Held loosely: the snippet mechanism was reported in July 2026 and flagged by its authors as likely temporary.

The prior is that the title carries the lexical weight and the post-H1 window carries a smaller, second-order effect. A null is interpretable: it would price the snippet-composition advice currently circulating.

## 2. Design

### 2.1 Structure
- Two arms, matched pair on thegeolab.net, one topic (paywalled and gated content in AI search).
- Frozen query set Q = 8 (section 3). Renders R = 10 per query. Capture unit = 1 query x 1 render on the ChatGPT API (`web_search_preview`).
- Both arms live simultaneously and compete inside the same answer, so one call yields one observation per arm.
- Target = 80 browsed observations per arm (a browsed call returned a search-results list; see 2.6). Q and R are rigor floors, not budget dials.
- Stopping rule: capture continues until 80 browsed observations per arm are reached, hard cap 160 calls. The stopping criterion (count of browsed calls) is outcome-blind. The browse rate is not assumed to be near-universal. The co-author measured 17 of 24 probe calls browsing on gpt-5.6-luna (71%) and 24 of 24 on gpt-6-luna with the same probes. At 71%, about 113 calls would be needed to reach 80 browsed observations; at the rate measured on gpt-6-luna, about 80. If the cap is reached before 80 browsed observations per arm, capture stops and the achieved N is reported as the registered N. At the measured rates the cap does not bind. Same rule as E097.
- Top-up allocation: any renders beyond the initial 10 per query, needed if a non-browsing call leaves an arm short of 80 browsed observations, are added by cycling the frozen query order (query 1, 2 ... 8, then 1, 2 ... again). Allocation is fixed in advance, not decided mid-capture.
- Single capture window: capture runs as one session on one harness. The start and end timestamps (UTC) of the session are recorded and deposited with the results. The same session captures E097 (section 5).
- Browse pre-check (registered before capture, run after this document is deposited and before the first scored call): the co-author runs it on her harness with the pinned model and settings (2.2). Each frozen query is asked twice. If neither call browses, it is asked twice more, and the query is declared dead only if all four calls fail to browse. A dead query is replaced by the next unused query in the reserve list (section 3a), in the listed order, and each substitution is recorded in the deposit before capture starts, so the frozen set of eight is still fixed before any scored call. The pre-check reads the browse flag only. No arm is scored, no citation outcome is read, and the raw responses are deposited unscored. Pre-check calls do not count toward the 80 browsed observations or the 160-call cap. The rule exists because a query shape that rarely triggers search adds no observations to either arm, and a single unlucky pair of non-browsing calls would otherwise discard a live query too often.
- Power rationale (approximate, not a guarantee): roughly 80 observations per arm is the minimum to detect the 22 percentage-point re-ask noise floor documented in the anchor study (same top answer on 7 of 24 ChatGPT re-asks). Differences below 22 points are read as null.

### 2.2 Engine and model pin
Exact identifier, no alias. Returned model logged on every call, log deposited with results.
- **ChatGPT** model `gpt-6-luna`, `web_search_preview` enabled, and the `include` parameter set to return `web_search_call.action.sources` on every call (2.4). OpenAI's model page lists this single identifier and no dated snapshot, so the pin is the requested identifier together with the returned model string logged on every call.
- **Reasoning effort:** `medium`, sent explicitly on every call, and the effort the API reports back is logged next to the model name. This is the API default for gpt-6-luna when no effort is set (co-author's check, 16 Oct 2026), and it is the setting her probe measurements ran at.
- **Output limit:** `max_output_tokens` 4000. Reasoning tokens count toward the limit on this API. In the co-author's probes the longest answer used 1,300 tokens, and two re-runs of the longest-answer query at medium used 1,473 and 1,736, about half of it reasoning, so the limit is set well above the longest observed use.
- **Incomplete calls:** a call whose response status is `incomplete` (cut off by the output limit) is a failed call, not an observation. It is never scored as "arm not cited". It does not count toward the 80 browsed observations, it is re-run for the same query, and every attempt counts toward the 160-call cap. The status field does not depend on which arm was cited. The number of incomplete calls is reported per query. API errors with no response, such as a timeout or a rate limit, are logged, re-run, never scored, and counted toward the 160-call cap.

Retirement clause: if the pinned model is retired, or the model or the reasoning effort the API returns changes from the one recorded in the browse pre-check, before the first scored call, capture does not run. If the `web_search_preview` tool is refused or retired before capture, capture does not run. A re-pin is a new version of this document, with its own deposit and T0.

Mid-capture rule: if the returned model or reasoning effort changes within a capture window, that window is flagged at capture time and kept, split or voided from the log under this rule, not after seeing results.

### 2.3 Arms
Title and H1 identical. Body identical from the first substantive sentence down.

Shared-body check. The canonical check is the live database value: `post_content` from the first `<p>AI search engines can only cite` to the end, md5 `1be194c58fb711f01a1eabc91d9920af`, 5856 bytes, identical on both arms. The same span in the committed page-source export carries one trailing newline and has md5 `a85274885b18741417d647b569d62fa5`, the value quoted in v1.3 and v1.4. The two differ by that one newline byte and nothing else. Reproduction script: `e100/verify/shared_body_md5.py`.

Page state. The four experiment pages were published live on 11 September 2026 at 08:00 UTC. Their page-source files last changed in commit `55ac913` (10 September), and the freeze manifests are at tag `e097-e100-pages-frozen` (commit `baa06e9`). Full `post_content` md5 for the E100 arms: arm A `c397e1b02f90e27b8d9d44217842373a`, arm B `5b9713919af7d157c040dcb07b1eb025`. `post_modified_gmt` is 2026-09-11 08:00:45 on both. Re-checked unchanged on 16 Oct 2026.

- **A, clean window:** nothing between the H1 and the opening sentence. The opening sentence is at offset 0 after the H1.
- **B, clutter retained:** five elements between the H1 and the opening sentence, in this order: a category label, a publish date, a table of contents, an image with alt text, and a widget. The opening sentence is at offset 520 after the H1. These elements may appear elsewhere on the page in arm A; only the post-H1 window differs.

Phase 0 correction. v1.3 and v1.4 stated that arm B's opening sentence begins at character 728, and the Zenodo record description carries two snippet md5 values. Those figures came from an unsaved one-off calculation on 16 Sep 2026 and cannot be reproduced. One documented extraction method (`e100/phase0/snippet_offset.py`, md5 `6ac84b1f9aef6873d2a317fe4abd8c06`) was run on the preserved 16 Sep captures and on the live pages. It gives offset 0 for arm A and offset 520 for arm B, identical on saved and live copies and for browser and Googlebot user agents. Other extraction methods placed arm B between 520 and 757, and arm A at 0 under every method. The finding is unchanged: arm A starts the post-H1 window with body text, and arm B's opening sentence sits outside the first 200 characters. Withdrawn: the 728 figure and the two md5 values. Erratum: `e100/ERRATUM-2026-09-29-phase0.md`, commit `da21809`, tag `e100-erratum-phase0`.

Slugs are not a variable in E100. The two arm addresses, as served live (canonical carries a trailing slash):
- Arm A: `https://thegeolab.net/guides/paywalls-and-ai-search-a/`
- Arm B: `https://thegeolab.net/guides/paywalls-and-ai-search-b/`

Same folder, identical topic tokens, single-character disambiguator. Which physical suffix carries the clean window was assigned by a coin flip before build (result: `a` = clean) and recorded in the freeze manifest.

### 2.4 Outcome measure
**Primary (cited):** the arm's URL appears among the url_citation annotations of the ChatGPT response for that call.

**Secondary (surfaced but not cited):** the arm's URL appears in the list of pages the search consulted, returned in `web_search_call.action.sources`. The request sets the `include` parameter to return this list; without it the list comes back null. In the co-author's characterisation every cited page is also in the consulted list (about 2 cited per call on gpt-6-luna), so the primary outcome is the stricter of the two.

One arm is one URL. No click, CTR or traffic metric enters the analysis.

**URL matching rule (registered before capture):** a returned URL is matched to a registered arm address (2.3) after removing any query string and fragment and normalising a trailing slash on the path, so `.../paywalls-and-ai-search-a`, `.../paywalls-and-ai-search-a/` and `.../paywalls-and-ai-search-a/?utm_source=openai` are treated as the same address. Cited URLs can come back with a tracking query string appended, and without this rule such a citation would be scored as a miss. Scheme and host are compared as returned. The raw returned URL is logged verbatim on every call (2.7), so any match can be re-derived either way from the deposited log. No other normalisation is applied.

**Citation floor (registered before capture):** let n be the number of valid observations per arm, that is browsed calls (2.6). The registered detectable difference is 22 percentage points (2.1). The largest possible difference between the arms, counted in calls, equals the number of calls that cite either arm, so a 22 point difference cannot be shown unless at least ceil(0.22 x n) browsed calls cite one or both arms. At n = 80 the floor is 18. If fewer calls than the floor cite either arm, the primary outcome is declared uninformative, no difference between arms is claimed, and the surfaced outcome is reported as its own finding (pages the search retrieved but did not cite). The floor is fixed here, before any result exists.

### 2.5 Gates (passed before the v1.4 deposit; carried forward unchanged and re-checked on the morning capture opens)
- **Two-path index check, both arms:** Google Search Console coverage plus a verified crawler hit in server logs. Both arms indexed on both paths, no folding, confirmed on two separate reads (14 and 16 September). This is the check E097 failed and E100 passed.
- **Phase 0 served-snippet read:** the served snippet for each arm read directly and confirmed query-independent, with arm A's window visibly cleaner than arm B's. What the server delivers is byte-identical between a normal browser and Googlebot on both arms, so the manipulation is server-side and not cloaked. Passed. The Phase 0 figures quoted in v1.3 and v1.4 are corrected in 2.3 (erratum commit da21809); the gate itself is unchanged.
- **Abort condition (stays in force through capture):** if either arm drops from the index during the capture window, every call in that window is voided. A page that is not indexed cannot be cited, and its absence is not a finding.

### 2.6 Denominator rule
Calls are the ChatGPT API with `web_search_preview` enabled. The browse rate is not assumed to be near-universal (2.1). If any call returns no search results at all (the model answered without searching), it is dropped from the denominator, not counted as a zero for both arms, and does not count toward the 80 browsed observations in the stopping rule (2.1). Same logic as the cross-engine no-browse rule.

### 2.7 Transparency standard
Deposited with results: raw API responses for all calls unedited; the per-call model log (requested and returned model, requested and returned reasoning effort, response status); the per-call browse flag (browsed / did not browse); which response fields were present on each call; the exact request specification, including the `include` parameter; every script used to produce every figure; the resolved URL match per call; and the start and end timestamps (UTC) of the capture session. The browse pre-check responses are deposited unscored, with the substitution record if any query was replaced.

## 3. Frozen queries (ChatGPT only, no paraphrase)
1. can AI search engines read paywalled articles
2. do AI assistants cite content behind a paywall
3. how do AI search engines handle gated content
4. is paywalled content indexed by AI search
5. can AI answer engines see content behind a login
6. do AI search engines cite subscription-only articles
7. how to make paywalled content visible to AI search without giving it away
8. does a paywall stop a page being cited in AI answers

### 3a. Reserve queries

They went through the same collision and Goldilocks gates as the frozen eight (collision grep on the site database, content-word overlap against the frozen sets, a check that the arm page body contains the query's key terms, and a search-results saturation read on 16 October 2026, before any capture call). They are listed in the fixed substitution order. A frozen query that fails the browse pre-check (2.1) is replaced by the first unused reserve, and so on down the list. The list is deposited unscored.

1. what do AI crawlers see on a metered paywall
2. is a client-side paywall visible to AI search engines
3. does paywall structured data matter for AI search

A fourth candidate, "do publisher licensing deals let AI cite paywalled articles", was tested and rejected before registration (67% content-word overlap with frozen query 1, and the results page was already saturated with direct answers). If all three reserves are used and a frozen query is still dead, that query is dropped, the arm keeps the remaining queries, and the drop is reported.

## 4. Analysis plan
Per-arm citation rate = cited observations (primary outcome, 2.4) / valid observations after the denominator rule (2.6). Report the point difference A minus B with a 95% two-proportion confidence interval. A difference whose interval includes zero, or whose point estimate is below 22 points, is reported as null. If the citation floor (2.4) is not met, the primary outcome is declared uninformative and no difference is claimed. Secondary: surfaced-but-not-cited rate per arm (the arm's URL in the consulted list and not among the citation annotations), with the same interval, reported as retrieval and not as citation. Full per-query breakdown; no query dropped after the fact except by the registered substitution rule (2.1, 3a), with every substitution and drop reported. Voided and dropped calls reported with counts and reasons. Anything added or re-weighted after T0 is labelled exploratory.

## 5. Sibling note (descriptive)
E100's sibling experiment E097 (URL slug, same folder family, separate topic) is registered separately (concept DOI 10.5281/zenodo.22899396). Both experiments are captured in the same session, on one harness, with one pinned ChatGPT model and a shared browse pre-check, so timing is controlled between them. Any comparison between the two remains descriptive only, because the topics differ (as always intended). It is kept as context, not as a claim.

## 6. Sequence
E100 pages are already live, indexed on both paths, and past the Phase 0 snippet read. Remaining: (1) co-author reads this file; (2) deposit as v1.5, which sets T0; (3) browse pre-check on the co-author's harness (2.1), with the raw responses deposited unscored and any substitution recorded before the first scored call; (4) capture week named with several days' notice, as one session shared with E097 (2.1, 5); (5) capture to the stopping rule; (6) analysis and write-up.
