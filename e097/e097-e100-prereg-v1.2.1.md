# Pre-registration: E097 and E100 (joint)

**Does URL slug text, or the composition of the post-H1 snippet window, change whether an AI search engine cites a page when the page content is held constant?**

Version 1.2.1. Registered protocol for two matched-pair experiments run in a single capture window. This document is the frozen record. Any deviation during capture or analysis is reported as a deviation, not absorbed silently.

**Creators**
Artur Ferreira, The GEO Lab, ORCID 0009-0004-4072-9741 (controlled arm: pages, manipulations, frozen query sets, this pre-registration, analysis)
Marwa Saleh, LeapOne, ORCID 0009-0008-8525-2747 (capture pipeline, all 400 calls, per-call model log, observational anchor from the LeapOne Canadian AI Visibility Report 2026, optometry edition)

**Licence** CC BY 4.0. **Venue** Zenodo. **Freeze tag** `e097-e100-prereg-v1.2.1`. T0 is the deposit date of this document. No capture runs before T0.

---

## 1. Lineage and why two experiments

Both experiments trace to a single claim in circulation: that non-body strings near the top of a page (the URL slug, the text immediately after the H1) influence whether an AI answer engine selects and cites that page. E097 tests the slug. E100 tests the post-H1 window. They are siblings, measured on ChatGPT in the same run, but they sit on different topics with disjoint query sets so that their four pages cannot compete for the same citations.

The prior for both is a null on the retrieval mechanism. In ChatGPT instant mode the model selects on the title plus a short stored snippet; the URL is rendered at citation display but there is no evidence its tokens drive selection. Under lexical scoring the title and H1 are the short high-weight fields and the slug is a weak semantic signal riding alongside them. A shared null across E097 and E100 would be a stronger statement than either alone; it is registered as descriptive, not causal (section 6).

---

## 2. Shared design

### 2.1 Structure
- Two arms per experiment, matched pairs on thegeolab.net, one topic per experiment.
- Frozen query set Q = 8 per experiment. Renders R = 10 per query per engine (fresh re-asks, identical wording).
- Capture unit = 1 query x 1 engine x 1 render. Both arms are live simultaneously and compete inside the same answer, so one call yields one observation per arm.
- Observations per arm per engine = 80. Q and R are rigor floors, not budget dials.
- Power rationale (approximate, not a guarantee): a two-proportion comparison at roughly 80 observations per arm per engine is the minimum to detect the 22 percentage-point re-ask noise floor documented in the anchor study (same top answer on 7 of 24 ChatGPT re-asks). Differences below 22 points are read as null.

### 2.2 Call counts
| | Engines | Calls |
|---|---|---|
| E097 | ChatGPT, Gemini, Perplexity, Google AI Overview | 8 x 10 x 4 = 320 |
| E100 | ChatGPT only | 8 x 10 x 1 = 80 |
| **Joint** | | **400** |

Per engine: ChatGPT 160 (80 E097 + 80 E100), Gemini 80, Perplexity 80, AI Overview 80. All 400 run on the LeapOne pipeline, one harness, one code path, for every engine and both experiments. Nothing runs on The GEO Lab side. Engine cut order if any engine must be dropped: AI Overview first, then Gemini, then Perplexity; ChatGPT is never cut because the sibling read requires it.

### 2.3 Engine and model pins
Exact identifiers, no aliases. The returned model is logged on every call and the log is deposited with the results.

- **ChatGPT** model `gpt-5.6-luna`, `web_search_preview` enabled, `max_output_tokens` 3000. The default 700 truncates a reasoning model (reasoning tokens bill as output); measured on this model, a 700 cap returned one citation and a mid-word stop where 3000 returned the same question in full with six citations. Truncation would read as "arm not cited".
- **Gemini** model `gemini-3.7-flash`, `google_search` grounding via REST, `maxOutputTokens` 3500, `temperature` 0.0. Too small a budget spends the tokens thinking and grounding never fires.
- **Perplexity** model `perplexity/sonar`, no presets.
- **Google AI Overview** not a model: DataForSEO `/v3/serp/google/organic/live/advanced`, `device` desktop, `load_async_ai_overview` true, `location_name` United Kingdom, `language_code` en.

Mid-capture rule: if the returned model changes within a capture window, that window is flagged at capture time and the decision to keep, split or void it is taken from the log under this rule, not after seeing results.

### 2.4 Outcome measure
Primary outcome for both experiments: the arm's URL appears in the engine's citation list for that call. For ChatGPT this is `sources[]` only (strict); `search_results[]` is recorded as the secondary "surfaced but not cited" outcome. Equivalent citation lists are used for Gemini (grounding sources), Perplexity (citations) and AI Overview (AIO reference links). One arm is one URL. No click, CTR or traffic metric enters any analysis; those measure a user-facing trust cue, not selection.

### 2.5 Denominator rules
- A call where the engine did not search (Gemini returns no grounding sources) is dropped from the denominator, not counted as a zero for both arms.
- Both arms of both experiments must be indexed before T0 and stay indexed through capture. Verification is two-path per URL: Google Search Console coverage plus a verified crawler hit in server logs. If either arm of an experiment drops from the index during the capture window, every call in that engine-window is voided. A page that is not indexed cannot be cited, and its absence is not a finding.
- E097 is the primary canonicalisation risk (byte-identical bodies, slug-only separation). E100 is secondary (arms differ visibly above the fold).

### 2.6 Page conditions common to all four pages
Self-canonical. Indexable. Linked contextually and via sitemap, not sitewide navigation. Same folder (`/guides/`) for every page, so folder text never varies within or across experiments. Titles and H1s identical within each pair. JSON-LD is RankMath's standard output only (BreadcrumbList, WebSite, Organization); the site's entity-graph plugin does not fire on these pages, so there is no entity-level schema (no TechArticle, DefinedTerm or author reference). Identical across arms except the URL-derived @id fields in the BreadcrumbList node.

### 2.7 Transparency standard
Deposited with results: raw API responses for all 400 calls unedited, the per-call model log, every script used to produce every figure, and the resolved URL match per call. Same standard as the LeapOne optometry reconciliation pack.

---

## 3. E097: URL slug

**Hypothesis (as registered, v1.2.1):** a descriptive slug that contains the topic's own terms is cited at a different rate than an opaque ID-style slug with no lexical content, page content held identical. The treatment under test is the whole difference between a keyword-bearing descriptive slug and a contentless one. This experiment does not separate two sub-effects inside that difference: URL structure (hierarchical or readable versus flat or ID-style) and lexical overlap (slug tokens matching query tokens versus no tokens at all). Arm A (`/guides/hreflang-and-ai-search-explained`) carries both properties; arm B (`/guides/p48213`) carries neither. A difference between them is attributed to the combined treatment, not to structure alone.

**Prediction (before data):** null or sub-22-point difference across all four engines. The prior is that ChatGPT-instant and grounded engines select on title and stored snippet, and that the slug, whether or not it carries query terms, is a weak signal beside the high-weight title and H1 fields, which are identical across arms. If a difference does appear, the registered reading is that it reflects lexical overlap in the URL rather than readable structure as such, because lexical overlap is the component with a plausible retrieval pathway; this reading is stated in advance so it is not constructed after seeing the result.

A Gemini null is separately expected and interpretable: on discovery queries Gemini leans heavily on entity cards and may surface few organic URLs for a slug to act on. That is a reading, not a power failure.

**Scope and known confound (registered):** the two E097 slugs differ on structure and on keyword content at the same time. The opaque arm slug `p48213` was a deliberate, hand-set token-free choice, not a CMS default; the confound is therefore between that intended opaque token and the descriptive arm's keyword content, not an artefact of an unset slug. A clean separation would need a third arm, a readable but keyword-free slug (for example a descriptive slug in an unrelated vocabulary), or a fourth, an opaque slug seeded with the query terms. This run does not include those arms. It tests whether the everyday choice a publisher actually faces, a human-readable topic slug versus a CMS-style ID, moves AI citation; it does not test which half of that choice is responsible. The keyword-free-readable and keyword-bearing-opaque arms are named here as the registered follow-up.

**Topic:** hreflang and multilingual content in AI search. Discovery-weighted, outside The GEO Lab's existing content lines.

**Scope statement:** E097 does not implement hreflang. Each arm is a single English page whose subject is hreflang. There are no language variants; an arm is one URL. The topic is not the manipulation. Queries are English-only and generic informational; no local-intent queries are used.

**Arms (body byte-identical, title and H1 identical):**
- A, descriptive slug: `/guides/hreflang-and-ai-search-explained`
- B, opaque slug: `/guides/p48213`

Retired and not built: the v1.1 pair `/international-seo/hreflang-for-ai-search/` vs `/p/4k9x2/`, because folder and slug both varied.

**Frozen queries (identical strings to all four engines, no paraphrase):**
1. how do AI search engines handle hreflang
2. does hreflang affect which language version AI search cites
3. how do AI assistants choose between translated versions of a page
4. do you need hreflang for AI search visibility
5. how to optimise a multilingual website for AI search
6. can AI search engines cite the wrong language version of a page
7. does AI search treat translated pages as duplicate content
8. which URL do AI search engines cite when a page exists in several languages

**Engines:** ChatGPT, Gemini, Perplexity, Google AI Overview. 320 calls.

---

## 4. E100: post-H1 snippet window

**Hypothesis (as registered):** in ChatGPT instant mode the model selects on the title plus a stored snippet of roughly 200 characters anchored on the H1. Clearing non-body elements from between the H1 and the first substantive sentence raises the share of on-topic text in that window and therefore instant-mode citation. This is the mechanism under test, not an established description of the system.

**Prediction (before data):** directional, A above B on citation rate, within-site. Held loosely: the snippet mechanism was reported in July 2026 and flagged by its authors as likely temporary.

**Topic:** paywalled and gated content in AI search. Definitional, snippet-friendly, disjoint from E097's topic.

**Arms (body identical below the fold, title and H1 identical):**
- A, clean window: nothing between the H1 and the opening sentence.
- B, clutter retained: five elements between the H1 and the opening sentence, in this order: a category label, a publish date, a table of contents, an image with alt text, and a widget. These may appear elsewhere on the page in arm A; only the post-H1 window differs.

**Slugs (not the variable):** `/guides/paywalls-and-ai-search-a` and `/guides/paywalls-and-ai-search-b`. Same folder, identical topic tokens, single-character disambiguator. Retired and not built: the v1.1 pair `/guides/paywalled-content-ai-search/` vs `/notes/paywalled-content-ai-search/`, because the folder varied and E097 is the experiment that tests URL text.

**Slug assignment:** which physical URL (`-a` or `-b`) carries the clean window was assigned by a single coin flip before build and is recorded in the freeze manifest, so the suffix carries no consistent treatment meaning.

**Frozen queries (ChatGPT only, no paraphrase):**
1. can AI search engines read paywalled articles
2. do AI assistants cite content behind a paywall
3. how do AI search engines handle gated content
4. is paywalled content indexed by AI search
5. can AI answer engines see content behind a login
6. do AI search engines cite subscription-only articles
7. how to make paywalled content visible to AI search without giving it away
8. does a paywall stop a page being cited in AI answers

**Engine:** ChatGPT instant mode only. 80 calls.

**Phase 0 gate (E100 only, before T0):** the served snippet for each arm is read directly from the index and verified to be query-independent. If the served window for arm A is not visibly cleaner than arm B, the manipulation did not land and E100 does not run.

---

## 5. Observational anchor

The LeapOne optometry study (July 2026, verified at row level) found that on the discovery query "best optometrist in {city}", ChatGPT credited a clinic's own site in `sources[]` zero times out of 72 top-3 recommendations. That result is local-intent, entity-card-heavy discovery. E097's queries are generic informational. The anchor is therefore registered as observational context from an adjacent query class, not as the same construct. If the controlled result and the anchor point the same way, that is convergence across query classes; it is not equivalence.

---

## 6. Sibling comparison

E097 on ChatGPT and E100 are measured in the same run, so timing is controlled. Topic is not: the two experiments sit on different topics, so an E097 versus E100 difference could be topic rather than design. The sibling comparison is registered as **descriptive only**. Topic selection: the two topics were chosen to differ on purpose (E097 discovery-weighted, E100 definitional) and are matched only on lying outside The GEO Lab's existing content lines and on zero query overlap. They are not matched on difficulty or competitiveness.

---

## 7. Analysis plan

For each experiment and each engine: per-arm citation rate = cited observations / valid observations after the denominator rules in 2.5. Report the point difference A minus B with a 95% two-proportion confidence interval. A difference whose interval includes zero, or whose point estimate is below 22 points, is reported as null. Secondary for ChatGPT: surfaced-but-not-cited rate per arm. Per-query breakdown reported in full; no query is dropped after the fact. Voided windows and dropped calls are reported with counts and reasons. No analysis is added, removed or re-weighted after T0 without being labelled exploratory.

---

## 8. Contingency clauses (resolve before deposit)

**Perplexity.** The LeapOne harness currently runs ChatGPT, Gemini and AI Overview. Perplexity is being added on its Agent API, which has shown rate-limit failures. If an 80-call viability check fails before deposit, E097 runs on three engines (240 calls, joint 320) and the Perplexity absence is stated here and in the write-up. Either outcome is fixed at deposit; this clause is replaced by the decision.

---

## 9. Sequence

Build on the v1.2 URL scheme, publish, two-path index verification on all four pages, E100 Phase 0 snippet read, then deposit (sets T0), then capture week named with several days' notice, then capture, then analysis and joint write-up with each cut attributed to its producer.

---

## Changelog

v1.2.1 (12 September 2026): E097 hypothesis narrowed to the combined descriptive-plus-keyword treatment; the structure versus lexical-overlap confound and the two follow-up arms registered explicitly, after a collaborator observation. The live pages are unchanged from the v1.2 freeze (body md5s identical); this is a text amendment to the registered claim, not a change to the instrument. All other sections carry forward from v1.2 unchanged. The Perplexity contingency in section 8 remains open at the time of this amendment and is resolved at deposit.
