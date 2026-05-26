# E027 — Deterministic Citation-Identity in Perplexity: Dataset

## Files

- `data/e027_14day_citations.csv` — 14-day citation log, 140 rows (14 days × 10 queries). Columns: day, date, query_id, tier, query_text, result_code, cited_url, platform, data_source. Days 1 and 3-14 from automated cron runs; Day 2 reconstructed from session notes (data_source=reconstructed_from_notes).
- `data/e027_q09_annotation_urls.txt` — Full Q09 annotation [1] source log across all 14 days with provenance notes. Documents four-way disambiguation conflict: GeoSCADA, GeoServer, Dell RAM, /geo-stack/.
- `data/day-01-raw/` — Raw DataForSEO API JSON responses for Day 1 (2026-04-24). Format: tasks[0].result[0].items[0].sections[0].annotations[]. 10 files, one per query.

## Provenance notes

- Days 3-14: live VPS cron data from /opt/e027/data/e027/
- Day 1: raw JSON from PC repo (geo-citation-index/data/e027/day-01/raw/), format-verified identical to VPS Days 3-14
- Day 2: outcome codes from session notes only — raw API response not preserved (session compaction). data_source=reconstructed_from_notes in CSV.

## Related paper

Ferreira, A. (2026). Deterministic Citation-Identity in Perplexity: A 14-Day Zero-Variance Replication of AI Citation Behaviour on Proprietary-Concept Queries. Zenodo. [DOI to be assigned on publication]

## Related records

- E016 noise floor paper: https://doi.org/10.5281/zenodo.19869156
- EDX null result: https://doi.org/10.5281/zenodo.19450361
