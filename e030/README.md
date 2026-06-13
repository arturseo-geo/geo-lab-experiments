# E030 — Fan-Out Query Length and Citation Rate: Replication Package

## Files

- `e030_queries.csv` — 45 frozen queries (1 header + 45 rows). Columns: query_id, page, length_tier, word_count, query. Three length tiers (2–4 words, 6–8 words, 10–12 words), 3 target pages, 5 queries per cell.
- `e030_measurements.csv` — 225 measurements (1 header + 225 rows). 45 queries × 5 days. Columns: query_id, query_text, length_tier, target_page, day, date, cited, query_rewrite, query_rewrite_text, correct_page_retrieved, wrong_page_retrieved, gis_noise_count, thatware_rank, hashmeta_rank, notes.
- `e030_statistical_summary.md` — Full statistical summary including citation rates by tier, Wilson CIs, Cochran–Armitage trend test, and per-page breakdowns.
- `data/` — Raw DataForSEO API JSON responses, one per day (5 files, 2026-05-19 to 2026-05-23).

## Primary Result

Citation rate inverts monotonically with query length on Perplexity sonar-pro over five days:

| Tier | Rate | 95% CI (Wilson) |
|------|------|-----------------|
| 2–4 words | 61.3% | [50.0%–71.5%] |
| 6–8 words | 36.0% | [26.1%–47.3%] |
| 10–12 words | 16.0% | [9.4%–25.9%] |

**Target pages (3):** /geo-stack/, /extractability/, /retrieval-probability/

**Measurement window:** 19–23 May 2026 (5 days). Platform: Perplexity sonar-pro via DataForSEO AI Optimization API.

## Related records

- Working paper: https://doi.org/10.5281/zenodo.20601081
- Results post: https://thegeolab.net/e030-fan-out-length-citation-rate-results/
- Pre-registration post: https://thegeolab.net/e030-fan-out-length-citation-rate/
- E016 noise floor: https://doi.org/10.5281/zenodo.19869156
