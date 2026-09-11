# E097 Freeze Manifest v1.2

**Protocol:** e097-e100-prereg-v1.2
**Frozen:** 2026-09-10
**Joint study with:** E100

## URL scheme

| Arm | Slug | Full URL | WP ID |
|-----|------|----------|-------|
| A (descriptive) | hreflang-and-ai-search-explained | https://thegeolab.net/guides/hreflang-and-ai-search-explained/ | 2211 |
| B (opaque) | p48213 | https://thegeolab.net/guides/p48213/ | 2212 |
| Parent | guides | https://thegeolab.net/guides/ | 2210 |

## Title / H1 (identical on both arms)

Hreflang and AI search: which language version gets cited, and why

## RankMath meta (identical on both arms)

- **SEO title:** Hreflang and AI search: which language version gets cited %sep% %sitename%
- **Meta description:** How AI search engines handle hreflang, which language version gets cited, and practical steps for multilingual sites.
- **Focus keyword:** hreflang ai search
- **Robots:** index
- **Canonical:** self

## Body md5 checksums

| Check | md5 |
|-------|-----|
| E097-A post_content (WP DB) | 56d4f3939b053548331def4c307f5e73 |
| E097-B post_content (WP DB) | 56d4f3939b053548331def4c307f5e73 |
| E097-A exported HTML file | b60dcb77d76576eb9120789892cce50c |
| E097-B exported HTML file | b60dcb77d76576eb9120789892cce50c |
| **Byte-identical** | **YES** |

## Inbound links (APPLIED at publish)

**Source post:** 1875 — "What AI Search Engines Actually Do With Your Content"
**Anchor text (both arms):** Hreflang and AI search: which language version gets cited, and why
**Position:** Single `<li>` in Related section, arm A link then arm B link, separated by ` · `
**Applied:** 2026-09-11 08:00 UTC. Diff in `e097/inbound-link-diff.md`.

## Collision checks

- `/guides/p48213` does not collide with any WP rewrite rule, existing slug, or plugin route (verified 2026-09-10)
- `/guides/` parent page created (ID 2210, status: draft — set to draft in corrections pass)

## Retired slugs (removed — verified absent)

- /international-seo/hreflang-for-ai-search/ — not found in WP or nginx
- /p/4k9x2/ — not found in WP or nginx

## Live URLs

- E097-A: https://thegeolab.net/guides/hreflang-and-ai-search-explained/
- E097-B: https://thegeolab.net/guides/p48213/

## Publish timestamps (UTC)

| ID | Slug | post_date_gmt | post_modified_gmt |
|----|------|---------------|-------------------|
| 2210 | guides (parent) | 2026-09-10 21:09:51 | 2026-09-11 08:00:40 |
| 2211 | hreflang-and-ai-search-explained | 2026-09-11 08:00:41 | 2026-09-11 08:00:41 |
| 2212 | p48213 | 2026-09-11 08:00:41 | 2026-09-11 08:00:41 |

## Body md5 scope

All md5 checksums computed on `post_content` column only (body HTML). The H1 comes from `post_title` via the `wp:post-title` block in the page template and is NOT included in post_content. No theme wrapper, `<head>`, or full-page HTML is included.

## Parent page

| Field | Value |
|-------|-------|
| ID | 2210 |
| Slug | guides |
| URL | https://thegeolab.net/guides/ |
| Status | publish |
| Robots | noindex, follow |
| Body | Empty (heading only, no content) |
| Sitemap | Excluded (noindex) |

## Status

**Published.** 2026-09-11 08:00:41 UTC (both arms).

## Corrections (applied 2026-09-10, same session)

1. **Inbound links reverted and restaged.** Four asymmetric links (one per arm, different source posts, different anchor text) removed from posts 1875, 448, 1872, 1865. Replaced with symmetric pair diffs: one source post per experiment, both arms in one `<li>`, identical anchor text (page title). Diffs staged in `inbound-link-diff.md`, not applied to live posts. Links were never served (nginx cache empty, no access log hits during 30-min exposure window).
2. **`/guides/` parent page (ID 2210) set to draft.** Was published; now draft until Phase 2 clearance.
3. **Tag `e097-e100-prereg-v1.2` force-moved** to the corrections commit to include these fixes.

## Publish (2026-09-11)

1. All five pages published (parent 2210 + four experiment pages 2211-2214).
2. Parent page set to noindex,follow, empty body, excluded from sitemap.
3. Inbound links applied to source posts 1875 and 1872.
4. Timestamps aligned: arm B = arm A within each pair; post_modified = post_date on all four experiment pages.
5. JSON-LD: RankMath-only (BreadcrumbList, WebSite, Organization). No entity-graph injection, no FAQPage, no datePublished/dateModified in schema.
6. Sitemap: four experiment pages present in page-sitemap.xml, parent excluded.
