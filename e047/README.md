# E047 — Fan-out Sub-query Coverage × Citation Rate

- **Experiment:** E047 Fan-out Sub-query Coverage × Citation Rate (Perplexity-only)
- **Phase:** Phase 0 — Sub-query identification
- **Notion:** 3654714ae9d081808fbbf095f9e789a7
- **Queries:** 15 T1 primaries × 5 iterations = 75 API calls
- **Target pages:** /geo-stack/, /extractability/, /retrieval-probability/
- **Output files:**
  - `data/e047_phase0_raw.csv` — 75 rows, one per API call
  - `data/e047_phase0_stability.csv` — 15 rows, one per query
  - `data/e047_phase0_frozen_subqueries.csv` — unique sub-query register, M1 content targets
  - `data/debug_first_response.json` — raw first API response for field path verification
- **Noise floor:** 22.0pp (E016)
- **Protocol:** Freeze sub-query set after reviewing stability summary. No page edits until Research Journal entry logged.
- **Dependencies:** E030 content freeze lifted 2026-05-23 ✓
- **Model:** sonar-pro
- **Sleep:** 3s between calls (~7 min total runtime)

## Run

```bash
python3 /opt/e047/e047_phase0_runner.py
```

PERPLEXITY_API_KEY must be set in environment.

## Field path note

`search_queries` checked at three paths per response:
1. `response.search_queries`
2. `response.choices[0].delta.search_queries`
3. `response.choices[0].message.search_queries`

Verify via `data/debug_first_response.json` after first run.
