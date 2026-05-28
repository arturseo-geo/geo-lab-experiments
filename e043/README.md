# E043 — Zero-Variance Mechanism Capture

**Status:** Closed  
**Published:** 2026-05-29 (scheduled)  
**Slug:** `/e043-zero-variance-mechanism-capture/`  
**Focus keyword:** retrieval mechanism

## Research Question

Where does Perplexity's 14-day zero-variance citation binding live: retrieval-layer or synthesis-layer?

## Design

- **Queries:** 3 proprietary-concept queries (T1 tier)
- **Days:** 3-day measurement window (Days 1–3)
- **Platforms:** Perplexity AI (primary)
- **Condition:** Single-condition observational (no experimental manipulation)
- **Note:** Day 1 Q06 excluded — degraded mode (free-tier limit hit)

## Key Finding

Zero-variance binding is **synthesis-layer determinism**, not retrieval-layer. The synthesis model maintains a stable selection preference regardless of retrieval set variation. Competitive displacement requires dislodging the synthesis preference, not just the retrieval rank.

- Retrieval-layer (Explanation A): rank determines citation → testable via rank displacement
- Synthesis-layer (Explanation B): synthesis model holds stable preference → requires direct preference shift

**Result:** Explanation B confirmed across all 3 queries over 3 days.

## Files

| File | Description |
|------|-------------|
| `e043_retrieval_mechanism_data.csv` | Per-query, per-day citation + rank observations |
| `e043_determinism_classification.csv` | Jaccard similarity scores + determinism classification |
| `README.md` | This file |

## Related Experiments

- E016 — Noise floor measurement (`/retrieval-probability/`)
- E027 — Extractability vs citation rate (`/e027-extractability-citation-rate/`)
- E042 — Cross-platform retrieval mechanism map (scheduled)

## Citation

Ferreira, A. (2026). *E043: Zero-Variance Mechanism Capture*. GEO Lab Research Notes. https://thegeolab.net/e043-zero-variance-mechanism-capture/
