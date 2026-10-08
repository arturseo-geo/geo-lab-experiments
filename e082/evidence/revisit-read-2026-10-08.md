# ENTIA v1/revisit — Declared Live Read, 2026-10-08

Declared to Fernando Vilches by email before the request.

## Request

- **Pre-timestamp (UTC):** 2026-10-08T07:59:05.519Z
- **Post-timestamp (UTC):** 2026-10-08T07:59:06.150Z
- **Endpoint:** `https://entia.systems/lab/e082/api/v1/revisit`
- **HTTP status:** 200

## Response file

- **File:** `revisit_20261008.json`
- **SHA256:** `de025bdd391af3f9e83954a4a7d5eb124fc2a6c96d4f3e886bb5c1636788ecec`
- **Size:** 2,898,657 bytes

## Comparison to 16 Sep baseline

- **Baseline SHA256:** `5d461dbb50b2143fc8bc3b0fa184ba9c5d13212f82e99c9ab0b0283b91368b37`
- **Baseline size:** 1,275,302 bytes
- **Verdict:** DIFFERENT

## Step 3 — Frozen-window fields (from 8 Oct file)

| Field | Actual | Expected | Status |
|-------|--------|----------|--------|
| frozen_to | 2026-09-16 | 2026-09-16 | MATCH |
| window start | 2026-08-19 | 2026-08-19 | MATCH |
| window end | 2026-09-16 | 2026-09-16 | MATCH |
| day count | 29 | 29 | MATCH |
| mode | frozen | frozen | MATCH |
| complete | True | True | MATCH |
| computed_at | 2026-10-08T04:46:26+00:00 | 2026-09-16T07:15:59Z | NO MATCH |
| families | 16 | 16 | MATCH |
| total intervals | 181,721 | 81,418 | NO MATCH |

## Step 4 — Recomputed medians (continuous quantile, hours)

| Family | n | p10 (h) | p50 (h) | p90 (h) | n match | p50 match |
|--------|---|---------|---------|---------|---------|-----------|
| ChatGPT-User | 63 | 2.69 | 85.00 | 345.75 | NO MATCH (exp 51) | NO MATCH (exp 60.19) |
| OpenAI-SearchBot | 192 | 0.07 | 72.00 | 472.83 | NO MATCH (exp 78) | NO MATCH (exp 144.00) |
| Googlebot | 12,569 | 23.66 | 48.86 | 81.32 | NO MATCH (exp 6,892) | NO MATCH (exp 48.96) |

## Script

- **File:** `recompute_medians.py` (from 7 Oct evidence check, unchanged)
- **SHA256:** `ecd49d386135cdc80b0dbc28d01aaf459463c6542ebd608ee2ef9b2182dc6c31`
