# E016 Reproducibility Package — v1.0

**Experiment:** E016 — Noise Floor Measurement for AI Citation Experiments  
**Domain:** thegeolab.net  
**Measurement window:** 2026-04-13 to 2026-04-17 (5 days)  
**Deposit date:** 2026-04-28  

---

## Files in this bundle

| File | Description |
|---|---|
| `paper.md` | Full paper draft — Markdown source |
| `data/e016_spreadsheet_export.csv` | Five-day citation log: 10 queries × 3 platforms × 5 days. Recording codes: C = Citation, M = Mention, X = No appearance |
| `data/e016_annotation_rerun_20260428.json` | Retrospective re-run of Days 1–2 with full annotation-array capture. Perplexity sonar-pro, 10 queries, DataForSEO task IDs preserved. Resolves the single-URL logger limitation for Days 1–2. |
| `data/e016_aio_check_20260428.txt` | AIO zero-finding confirmation. Human-coded across all 5 days. Raw DataForSEO JSON not preserved — see limitations in paper.md. |
| `MANIFEST.json` | SHA256 hashes of all files in this bundle |

---

## How to reproduce the five-day measurement

### Prerequisites
- DataForSEO account with Perplexity sonar-pro access
- DataForSEO account with Google AIO access (or manual browser check)
- A domain with at least one indexed page

### Step 1 — Define query set
Use a fixed set of queries covering both proprietary-concept and category terms. Do not modify queries between days. The E014 universal query set (10 queries) is used in this experiment — see `data/e016_spreadsheet_export.csv` column B for exact query text.

### Step 2 — Apply publishing freeze
No content changes, redirects, plugin updates or new posts on the test domain for the full 5-day window. Any change to the domain invalidates the noise floor for that day.

### Step 3 — Run daily measurements

**Perplexity sonar-pro via DataForSEO:**
```
POST https://api.dataforseo.com/v3/serp/perplexity/organic/live/advanced
{
  "language_code": "en",
  "location_code": 2826,
  "keyword": "<query>",
  "depth": 10
}
```
Record whether your domain URL appears in `items[].url` fields. Capture the full `items` array, not just the first URL.

**Google AIO via DataForSEO (or manual):**
```
POST https://api.dataforseo.com/v3/serp/google/organic/live/advanced
{
  "language_code": "en",
  "location_code": 2826,
  "keyword": "<query>",
  "calculate_rectangles": true
}
```
Check `items[].type == "answer_box"` or `"ai_overview"` for AIO presence. Record C/M/X per your domain.

### Step 4 — Record results
Use C/M/X codes immediately after each session. Record session completion time. Do not back-fill missed days — mark VOID and restart if 2+ days missed.

### Step 5 — Calculate noise floor
After 5 days: min and max combined citation rate (all platforms, queries ÷ total checks). Add 2pp buffer to the max for the interpretability threshold.

---

## Known limitations

1. **AIO raw data not preserved.** The zero-citation AIO finding rests on human-coded C/M/X entries and observer notes. Raw DataForSEO JSON responses were not saved.
2. **Days 1–2 single-URL logger.** The daily logger captured only the first annotation URL per query on Days 1–2. Binary citation counts (cited: yes/no) are correct. Full annotation arrays reconstructed in `e016_annotation_rerun_20260428.json`.
3. **Single domain, low authority.** Results are specific to thegeolab.net at DR ~0. Higher-authority domains should run their own noise floor characterisation.

---

## Citation

Ferreira, A. (2026). *Noise Floor Measurement for AI Citation Experiments: Platform Variance, Recording Artifacts, and a Four-Test Diagnostic Protocol.* Zenodo. DOI: [this deposit]

## Related deposits

- EDX null result (domain authority gate): DOI 10.5281/zenodo.19450361
