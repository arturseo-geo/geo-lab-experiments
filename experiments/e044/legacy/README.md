# E044 legacy rows: 2026-10-12 direct-API instrument

The 6 rows in e044_2026-10-12_direct_api_rows.csv are a direct Perplexity API
pull on 2026-10-12 (sonar-pro, no temperature set), ranked from the top-level
citations array, ThatWare matched on thatware.co only.

The weekly series in ../e044_competitor_rank_log.csv comes from the VPS runner
via DataForSEO, ranks from nested annotations deduplicated in order, matches
thatware.co or thatware.in, and runs P1 then P2 13 minutes apart.

The two instruments are not like-for-like. These rows must not feed the weekly
persistence rule or deltas, and no escalation applies to them. The rows carry
the tag source:API-sonar-pro; the forward tag for this instrument is
source:API-sonar-pro-direct.

Raw responses for this pull: ../raw/2026-10-12_Q1.json, ../raw/2026-10-12_Q2.json,
../raw/2026-10-12_Q3.json (one file per query, no P1/P2 split in the filenames;
the CSV records P1 and P2 rows but only three raw files exist).

Separated from the main CSV on 2026-11-02 (commit c6b1c43).
