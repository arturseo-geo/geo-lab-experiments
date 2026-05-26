# E042 Determinism Matrix — Cross-Platform Citation Outcomes
Session date: 2026-05-18
Pages tested: /geo-stack/, /extractability/, /retrieval-probability/
Platforms: Perplexity, ChatGPT, Gemini
Cell format: CITED (Y/N) | correct_page_retrieved (Y/N)

---

## Perplexity

| Page                    | 2–4 word         | 6–8 word         | 10–12 word        |
|-------------------------|------------------|------------------|-------------------|
| /geo-stack/             | Y \| Y (rank 5)  | Y \| Y (rank 5)  | N \| N (wrong page)¹ |
| /extractability/        | Y \| Y (rank 2)  | Y \| Y (rank 6)  | N \| N (absent)²  |
| /retrieval-probability/ | Y \| Y (rank 1)  | Y \| Y (rank 1)  | N \| N (absent)³  |

**Perplexity citation rate: 6/9 (67%)**

¹ /generative-engine-optimisation-guide/ retrieved at rank 10, not /geo-stack/. Cited=No.
² "Perplexity" modifier routes entire retrieval set to Perplexity-SEO cluster.
³ Dropped GEO context shifts retrieval to general AI/ML literature.

---

## ChatGPT

| Page                    | 2–4 word          | 6–8 word           | 10–12 word        |
|-------------------------|-------------------|--------------------|-------------------|
| /geo-stack/             | N \| N (GIS noise⁴)| Y \| N (wrong pages⁵)| Y \| N (homepage only⁶)|
| /extractability/        | Y \| Y (rank 2)   | Y \| Y (rank 3)    | N \| N (absent)²  |
| /retrieval-probability/ | Y \| N (homepage⁷)| N \| N (absent⁸)   | N \| N (absent)³  |

**ChatGPT citation rate: 5/9 (56%)**

⁴ 79% GIS noise — 11/14 sources geospatial software. No GEO/AI sources retrieved.
⁵ 8× citations, 12/17 links thegeolab.net, but /geo-stack/ slug specifically absent. Synthesised from 8 other slugs.
⁶ 4× citations but only homepage retrieved, no sub-slugs.
⁷ Direct quote used despite /retrieval-probability/ absent; homepage + /extractability/ surfaced instead.
⁸ Severe source quality collapse — 8 sources, 3 completely off-topic ResearchGate papers.

---

## Gemini

| Page                    | 2–4 word             | 6–8 word            | 10–12 word          |
|-------------------------|----------------------|---------------------|---------------------|
| /geo-stack/             | N \| N (no grounding)| N \| N (no grounding)| N \| N (ThatWare r1⁹)|
| /extractability/        | N \| N (no grounding)| N \| N (no grounding)| N \| N (absent)²   |
| /retrieval-probability/ | N \| N (GIS misfire¹⁰)| N \| N (absent)    | N \| N (absent)³   |

**Gemini citation rate: 0/9 (0%)**

⁹ ThatWare rank 1, cited 5×, Gemini adopted ThatWare's 5-layer framing entirely. Most severe competitive displacement in dataset.
¹⁰ Full GIS misfire — entire response about geostationary satellites, geo-localization, location privacy math. No grounding.

---

## Cross-Platform Agreement Matrix

| Query                   | Perplexity | ChatGPT | Gemini | Platforms citing |
|-------------------------|:----------:|:-------:|:------:|:----------------:|
| geo-stack-q1-2w         | Y          | N       | N      | 1                |
| geo-stack-q2-6w         | Y          | Y       | N      | 2                |
| geo-stack-q3-10w        | N          | Y       | N      | 1                |
| extractability-q1-2w    | Y          | Y       | N      | 2                |
| extractability-q2-6w    | Y          | Y       | N      | 2                |
| extractability-q3-10w   | **N**      | **N**   | **N**  | **0 — 3-platform failure** |
| retrieval-prob-q1-2w    | Y          | Y       | N      | 2                |
| retrieval-prob-q2-6w    | Y          | N       | N      | 1                |
| retrieval-prob-q3-10w   | **N**      | **N**   | **N**  | **0 — 3-platform failure** |

### Agreement summary
- **3-platform citation (all cite):** 0/9 queries
- **2-platform citation:** 4/9 — Q2 (geo-stack 6-8w), Q4 (extractability 2-4w), Q5 (extractability 6-8w), Q7 (retrieval-prob 2-4w)
- **1-platform citation:** 3/9 — Q1 (PPX only), Q3 (CGT only), Q8 (PPX only)
- **3-platform failure (none cite):** 2/9 — Q6 (extractability 10-12w), Q9 (retrieval-prob 10-12w)

### Critical findings
1. **Gemini is a zero-citation platform** for all 9 queries. Not a page-specific failure — structural absence from thegeolab.net's citation graph on Gemini across all targets and all tiers.
2. **3-platform failure modes confirmed:** Q6 ("Perplexity" modifier) and Q9 (dropped GEO context) fail on all three platforms. These are query construction failure modes, not site failures.
3. **2-4w tier is the highest-risk tier for GIS namespace collision.** Perplexity Q1 (56% GIS noise), ChatGPT Q1 (79% GIS noise), Gemini Q7 (full GIS misfire on "retrieval probability GEO"). Short queries without sufficient context trigger geospatial disambiguation on all platforms.
4. **Perplexity is the most reliable citation platform** for these pages: 6/9 citations, correct page retrieved on 4/6 cited queries.
5. **ChatGPT cites from entity graph, not page retrieval.** Q2 (8× citations, 12/17 links thegeolab.net, /geo-stack/ absent) and Q7 (direct quote used, /retrieval-probability/ absent) both demonstrate citation without target-page retrieval.
6. **ThatWare competitive displacement on Gemini Q3** is the most actionable finding: rank 1, cited 5×, Gemini's answer framing replaced by ThatWare's. Flag for E044.
