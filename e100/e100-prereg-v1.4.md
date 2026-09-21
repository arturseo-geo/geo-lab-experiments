# Pre-registration: E100

**Does clearing non-body content from the post-H1 snippet window change whether ChatGPT cites a page, when the page body is held constant?**

Version 1.4 (E100-only). Split from the joint E097/E100 pre-registration v1.2.1 after E097 failed its Google index gate before deposit (see changelog). This document is the frozen record. Any change made during capture or analysis is reported as a deviation, not folded into the method.

**Creators**
Artur Ferreira, The GEO Lab, ORCID 0009-0004-4072-9741 (pages, manipulation, frozen query set, this pre-registration, analysis)
Marwa Saleh, LeapOne, ORCID 0009-0008-8525-2747 (capture pipeline, all calls, per-call model log)

**Licence** CC BY 4.0. **Venue** Zenodo. **Freeze tag** `e100-prereg-v1.4`. T0 is the deposit date of this document. No capture runs before T0.

---

## Changelog

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
- Frozen query set Q = 8. Renders R = 10 per query. Capture unit = 1 query x 1 render on the ChatGPT API (`web_search_preview`).
- Both arms live simultaneously and compete inside the same answer, so one call yields one observation per arm.
- Target = 80 browsed observations per arm (a browsed call returned a search-results list; see 2.6). Q and R are rigor floors, not budget dials.
- Stopping rule: capture continues until 80 browsed observations per arm are reached, hard cap 160 calls. The stopping criterion (count of browsed calls) is outcome-blind. With `web_search_preview` the browse rate is expected to be near-universal, so this is expected to land at ~80 calls; the cap holds the floor by construction rather than by luck. Same rule as E097.
- Top-up allocation: any renders beyond the initial 10 per query, needed if a non-browsing call leaves an arm short of 80 browsed observations, are added by cycling the frozen query order (query 1, 2 ... 8, then 1, 2 ... again). Allocation is fixed in advance, not decided mid-capture.
- Power rationale (approximate, not a guarantee): roughly 80 observations per arm is the minimum to detect the 22 percentage-point re-ask noise floor documented in the anchor study (same top answer on 7 of 24 ChatGPT re-asks). Differences below 22 points are read as null.

### 2.2 Engine and model pin
Exact identifier, no alias. Returned model logged on every call, log deposited with results.
- **ChatGPT** model `gpt-5.6-luna`, `web_search_preview` enabled, `max_output_tokens` 3000. The default 700 truncates a reasoning model (reasoning tokens bill as output); measured on this model, a 700 cap returned one citation and a mid-word stop where 3000 returned the same question in full with six citations. Truncation would read as "arm not cited".

Mid-capture rule: if the returned model changes within a capture window, that window is flagged at capture time and kept, split or voided from the log under this rule, not after seeing results.

### 2.3 Arms
Title and H1 identical. Body identical from the first substantive sentence down (verified byte-identical, md5 `a85274885b18741417d647b569d62fa5` on both).
- **A, clean window:** nothing between the H1 and the opening sentence. Verified at build: rendered HTML reaches the opening sentence at character 0 after the H1.
- **B, clutter retained:** five elements between the H1 and the opening sentence, in this order: a category label, a publish date, a table of contents, an image with alt text, and a widget. Verified at build: the opening sentence begins at character 728, after the label, date and contents block. These elements may appear elsewhere on the page in arm A; only the post-H1 window differs.

Slugs are not a variable in E100. The two arm addresses, as served live (canonical carries a trailing slash):
- Arm A: `https://thegeolab.net/guides/paywalls-and-ai-search-a/`
- Arm B: `https://thegeolab.net/guides/paywalls-and-ai-search-b/`

Same folder, identical topic tokens, single-character disambiguator. Which physical suffix carries the clean window was assigned by a coin flip before build (result: `a` = clean) and recorded in the freeze manifest.

### 2.4 Outcome measure
Primary: the arm's URL appears in ChatGPT `sources[]` for that call (strict). `search_results[]` is recorded as the secondary "surfaced but not cited" outcome. One arm is one URL. No click, CTR or traffic metric enters the analysis.

**URL matching rule (registered before capture):** a returned URL is matched to a registered arm address (2.3) after normalising a trailing slash on the path, so `.../paywalls-and-ai-search-a` and `.../paywalls-and-ai-search-a/` are treated as the same address. Scheme and host are compared as returned. The raw returned URL is logged verbatim on every call (2.7), so any match can be re-derived either way from the deposited log. No other normalisation is applied.

### 2.5 Gates (all passed before this deposit)
- **Two-path index check, both arms:** Google Search Console coverage plus a verified crawler hit in server logs. Both arms indexed on both paths, no folding, confirmed on two separate reads (14 and 16 September). This is the check E097 failed and E100 passed.
- **Phase 0 served-snippet read:** the served snippet for each arm read directly and confirmed query-independent, with arm A's window visibly cleaner than arm B's. What the server delivers is byte-identical between a normal browser and Googlebot on both arms, so the manipulation is server-side and not cloaked. Passed.
- **Abort condition (stays in force through capture):** if either arm drops from the index during the capture window, every call in that window is voided. A page that is not indexed cannot be cited, and its absence is not a finding.

### 2.6 Denominator rule
Calls are the ChatGPT API with `web_search_preview` enabled; the expected browse rate is high. If any call returns no search results at all (the model answered without searching), it is dropped from the denominator, not counted as a zero for both arms, and does not count toward the 80 browsed observations in the stopping rule (2.1). Same logic as the cross-engine no-browse rule.

### 2.7 Transparency standard
Deposited with results: raw API responses for all calls unedited, the per-call model log, the per-call browse flag (browsed / did not browse), every script used to produce every figure, and the resolved URL match per call.

## 3. Frozen queries (ChatGPT only, no paraphrase)
1. can AI search engines read paywalled articles
2. do AI assistants cite content behind a paywall
3. how do AI search engines handle gated content
4. is paywalled content indexed by AI search
5. can AI answer engines see content behind a login
6. do AI search engines cite subscription-only articles
7. how to make paywalled content visible to AI search without giving it away
8. does a paywall stop a page being cited in AI answers

## 4. Analysis plan
Per-arm citation rate = cited observations / valid observations after the denominator rule. Report the point difference A minus B with a 95% two-proportion confidence interval. A difference whose interval includes zero, or whose point estimate is below 22 points, is reported as null. Secondary: surfaced-but-not-cited rate per arm. Full per-query breakdown; no query dropped after the fact. Voided and dropped calls reported with counts and reasons. Anything added or re-weighted after T0 is labelled exploratory.

## 5. Sibling note (descriptive, cross-run)
E100's sibling experiment E097 (URL slug, same pages' folder family, separate topic) is being re-registered separately and will capture in a different window. Any comparison between the two is descriptive only and now carries two stated limitations rather than one: the topics differ (as always intended), and the runs are no longer simultaneous, so timing is no longer controlled either. It is kept as context, not as a claim.

## 6. Sequence
E100 pages are already live, indexed on both paths, and past the Phase 0 snippet read. Remaining: co-author reads this file, deposit (sets T0), capture week named with several days' notice, capture, analysis and write-up.
