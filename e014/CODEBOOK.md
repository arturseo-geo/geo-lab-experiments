# E014 Codebook

## Unit
One read = one query submitted once to one engine. code = C (cited) or X (not cited).

## Citation rule (sources-block rule)
C only when a thegeolab.net URL appears in the engine's sources or annotations block. A thegeolab.net link or name appearing only inside the answer body is X. Any thegeolab.net URL counts, not only the query's target page. The rule was written down at M6, confirmed identical to M5 by audit of the M5 summary and the M4 raw JSONs, and applied unchanged to M7.

## Tiers
T1 = Q2, Q3, Q5, Q6, Q9 (concepts defined on thegeolab.net). T2 = Q1, Q4, Q7, Q8, Q10 (category questions). Query strings: config/frozen_queries.json.

## Instrument (M5 onward; pinned from M6)
- Browser: Chrome incognito, a new profile per query, one query per profile.
- Perplexity: 3 iterations, logged out, advanced-preview search mode confirmed on every read. A basic-search read is invalid and re-run.
- ChatGPT: 1 iteration, logged out, each session primed with "search the web for:" followed by the frozen query. A read with no web search and no sources is invalid and discarded, not coded X.
- Google AI Overviews: 1 iteration, logged out, coded on the AI Overview box only.

## Instrument (M1 to M4)
Single-session reads. Perplexity sessions could silently fall back to basic search mid-session. ChatGPT reads were not forced to search. These months are not like-for-like with M5 onward.

## Control entity (M6 only)
Query "What is the Skyscraper Technique in SEO?", owner domain backlinko.com, same instrument and coding rule, 5 reads (Perplexity 3, ChatGPT 1, AI Overviews 1). Not repeated at M7.

## Columns
Schema follows the monthly CSV headers. reconstruction_description = the engine's verbatim description of the cited thegeolab.net content, captured from M3 onward where available; not captured at M7.
