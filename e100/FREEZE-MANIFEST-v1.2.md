# E100 Freeze Manifest v1.2

**Protocol:** e097-e100-prereg-v1.2
**Frozen:** 2026-09-10
**Joint study with:** E097

## Coin flip

```
Command: python3 -c "import secrets; print(secrets.choice(['a','b']))"
Output:  a
```

**Mapping:** suffix `a` = CLEAN window, suffix `b` = clutter set.

## URL scheme

| Arm | Condition | Slug | Full URL | WP ID |
|-----|-----------|------|----------|-------|
| A | CLEAN | paywalls-and-ai-search-a | https://thegeolab.net/guides/paywalls-and-ai-search-a/ | 2213 |
| B | CLUTTER | paywalls-and-ai-search-b | https://thegeolab.net/guides/paywalls-and-ai-search-b/ | 2214 |
| Parent | — | guides | https://thegeolab.net/guides/ | 2210 |

## Title / H1 (identical on both arms)

Can AI search engines read paywalled content?

## RankMath meta (identical on both arms)

- **SEO title:** Can AI search engines read paywalled content? %sep% %sitename%
- **Meta description:** How paywalls affect AI search visibility. Hard, metered and client-side paywalls behave differently for AI crawlers.
- **Focus keyword:** paywalled content ai search
- **Robots:** index
- **Canonical:** self

## E100 arm construction

**CLEAN arm (A):** H1, then immediately the first paragraph ("AI search engines can only cite the content their crawlers can access. ..."). Nothing rendered between the H1 and that paragraph.

**CLUTTER arm (B):** Between the H1 and that same first paragraph, in this order:
1. Category label ("Technical Guides") — rendered above the H1
2. Publish date (10 September 2026)
3. Table of contents (9 entries)
4. Image with alt text (paywalls-ai-search-hero.webp, 800x450, "Diagram showing how different paywall types affect AI search engine access to content")
5. Widget (Related link to /what-is-generative-engine-optimisation/)

From the first paragraph down: byte-identical to the clean arm.

## Body md5 checksums

| Check | md5 |
|-------|-----|
| E100-A full post_content (WP DB) | c397e1b02f90e27b8d9d44217842373a |
| E100-B full post_content (WP DB) | 5b9713919af7d157c040dcb07b1eb025 |
| E100 shared body from first ¶ (WP DB) | 1be194c58fb711f01a1eabc91d9920af |
| E100 shared body from first ¶ (exported file) | a85274885b18741417d647b569d62fa5 |
| **Shared body byte-identical** | **YES** |

## Inbound links

| Source post | ID | Link target |
|-------------|-----|-------------|
| The ChatGPT Pre-Retrieval Gate | 1872 | /guides/paywalls-and-ai-search-a/ |
| The Difference Between Being Retrieved and Being Cited in AI Search | 1865 | /guides/paywalls-and-ai-search-b/ |

## Retired slugs (removed — verified absent)

- /guides/paywalled-content-ai-search/ — not found in WP or nginx
- /notes/paywalled-content-ai-search/ — not found in WP or nginx

## Draft URLs (WP preview)

- E100-A (CLEAN): https://thegeolab.net/?page_id=2213
- E100-B (CLUTTER): https://thegeolab.net/?page_id=2214

## Status

Draft. Publish waits on Phase 2 clearance from AJ.
