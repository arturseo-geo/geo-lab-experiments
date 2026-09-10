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
1. Category label ("Technical Guides") — renders as first element inside post_content (visually below the theme-generated H1; see render check note)
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

## Inbound links (staged — NOT applied to live posts)

**Source post:** 1872 — "The ChatGPT Pre-Retrieval Gate"
**Anchor text (both arms):** Can AI search engines read paywalled content?
**Position:** Single `<li>` in Related section, arm A link then arm B link, separated by ` · `
**Apply:** at publish time only. Diff in `e100/inbound-link-diff.md`.

## Retired slugs (removed — verified absent)

- /guides/paywalled-content-ai-search/ — not found in WP or nginx
- /notes/paywalled-content-ai-search/ — not found in WP or nginx

## Draft URLs (WP preview)

- E100-A (CLEAN): https://thegeolab.net/?page_id=2213
- E100-B (CLUTTER): https://thegeolab.net/?page_id=2214

## Body md5 scope

All md5 checksums computed on `post_content` column only (body HTML). The H1 comes from `post_title` via the `wp:post-title` block in the page template and is NOT included in post_content. No theme wrapper, `<head>`, or full-page HTML is included.

## Render check (E100-A clean arm)

Between the closing `</h1>` (theme-generated) and the opening `<p>AI search engines...` (first body paragraph):

**Result: EMPTY.** The rendered post_content starts immediately with `<p>AI search engines can only cite...`. The theme page template (`templates/page.html`) places `wp:post-title` directly before `wp:post-content` with no injected elements between them. No wrapper, breadcrumb, meta line, or empty div.

## Render check (E100-B clutter arm — category label position)

The category label `<div class="category-label">Technical Guides</div>` renders as the **first element inside post_content**, which the page template places **after** the theme-generated H1. In the HTML source order: `</h1>` → `<div class="category-label">...` → `<time>...` → `<nav class="toc">...` → `<figure>...` → `<div class="widget-box">...` → `<p>AI search engines...`.

The spec says "category label (rendered above the H1)". This would require the label to be outside post_content, which the current theme architecture does not support without a template override. For E100's purpose (testing the labrador snippet window), what matters is the HTML source order: the junk occupies the ~200 chars between the H1 token and the snippet payload paragraph. The visual position is secondary.

## Status

Draft. Publish waits on Phase 2 clearance from AJ.

## Corrections (applied 2026-09-10, same session)

1. **Inbound links reverted and restaged.** Four asymmetric links (one per arm, different source posts, different anchor text) removed from posts 1875, 448, 1872, 1865. Replaced with symmetric pair diffs: one source post per experiment, both arms in one `<li>`, identical anchor text (page title). Diffs staged in `inbound-link-diff.md`, not applied to live posts. Links were never served (nginx cache empty, no access log hits during 30-min exposure window).
2. **`/guides/` parent page (ID 2210) set to draft.** Was published; now draft until Phase 2 clearance.
3. **Category label position clarified.** Renders after H1 in HTML (inside post_content), not above it visually. Functionally correct for snippet-window testing.
4. **Tag `e097-e100-prereg-v1.2` force-moved** to the corrections commit to include these fixes.
