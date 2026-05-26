# E042 — Cross-Platform Retrieval Mechanism Comparison

**Status:** Active — analysis and write-up pending  
**Platforms:** Perplexity, ChatGPT, Gemini  
**Date:** 2026-05-18  
**Research journal:** https://www.notion.so/3634714ae9d08155bbdbf384d6d82f1c

## Overview

Systematic comparison of retrieval mechanisms across Perplexity, ChatGPT, and Gemini on the same 9 queries (3 length tiers × 3 target pages). Documents sub-query width, query rewrite behaviour, deep crawl activation, and retrieval set composition per platform.

## Top-line results

| Platform | Cited / 9 queries |
|----------|-------------------|
| Perplexity | 6/9 (67%) |
| ChatGPT | 5/9 (56%) |
| Gemini | 0/9 (0%) |

## Data files

| File | Description |
|------|-------------|
| `e042_cross_platform_mechanism_map.csv` | 27-row mechanism map (9 queries × 3 platforms) |
| `e042_robots_txt_audit.csv` | Infrastructure accessibility audit for retrieved domains |
| `e042_competitor_rank_log.csv` | Competitor domain ranks per query per platform |

## Target pages

- `/geo-stack/` — thegeolab.net/geo-stack/
- `/extractability/` — thegeolab.net/extractability/
- `/retrieval-probability/` — thegeolab.net/retrieval-probability/

## Related experiments

E030 (Perplexity length × citation rate), E041 (URL_NAVIGATE triggers), E035 (Gemini T1.5 mention vs citation)
