# E014: System Memory Longitudinal Citation Study (Feb to Sep 2026)

Author: Artur Ferreira, The GEO Lab (thegeolab.net). ORCID 0009-0004-4072-9741.

## Status of this deposit

E014 was NOT pre-registered. This is an observational longitudinal dataset deposited after the series closed on 28 September 2026, together with its full deviation log. It is not a confirmatory study and supports no causal claim.

## What was measured

Whether Perplexity, ChatGPT and Google AI Overviews cite thegeolab.net for ten frozen queries, measured monthly from 28 February to 28 September 2026. Five Tier 1 queries ask about concepts defined on thegeolab.net (Retrieval Probability, LLM readability, the GEO Stack, Extractability, System Memory). Five Tier 2 queries are category questions. The hypothesis under test: citation of the site accumulates over time with consistent publishing (System Memory, Layer 5 of the GEO Stack).

Standard month: 50 reads = 10 queries x (Perplexity 3 iterations + ChatGPT 1 + Google AI Overviews 1). M2 used a 70-read denominator.

## Results summary

| Month | Date | Combined | Tier 1 | Tier 2 |
|---|---|---|---|---|
| Baseline | 28 Feb | 3% | not split | 0% |
| M1 | 28 Mar | 6.7% | not split | 0% |
| M2 | 24 Apr | 12.9% (9/70) | not split | 0% |
| M3 | 28 May | 12.0% (6/50) | 24% | 0% |
| M4 | 28 Jun | 6.0% (3/50) | 12% | 0% |
| M5 | 2 Aug | 48% (24/50) | 92% | excluded (see DEVIATIONS.md) |
| M6 | 9 Sep | 46% (23/50) | 92% | 0% |
| M7 | 28 Sep | 48% (24/50) | 96% | 0% |

Tier 1 citation held at 92% to 96% for three consecutive months (M5 to M7) on a fixed instrument. Tier 2 stayed at 0% at every clean measurement. The M4 to M5 jump coincided with an instrument change (see DEVIATIONS.md), so it cannot be attributed to accumulation. System Memory accumulation remains the leading hypothesis, not an established result.

## Contents

- data/: monthly coded CSVs (M3 to M7), summary files, M6 control-entity CSV. M2 data is in raw/m2/.
- raw/: M2 run directory (includes the M2 coded data), 52 M4 raw API responses (50 main reads + 2 exploratory probes), M7 raw capture text.
- config/frozen_queries.json: the 10 frozen query strings, tiers and target pages.
- docs/: this README, CODEBOOK.md, DEVIATIONS.md.
- MANIFEST.sha256: checksums for every file.

## Data availability

Row-level data: M2 to M7. Baseline and M1 row-level data are not recoverable; those figures come from the contemporaneous write-up only.

## Related

Month 1 write-up: https://thegeolab.net/e014-month-1-citation-rate-baseline/
