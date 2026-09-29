# E100 Erratum: Phase 0 offset and md5 values (29 Sep 2026)

Filed before capture results exist. This erratum will be carried into the results deposit.

## What the registered record says

The e100-prereg-v1.4 section 2.3 reads:

> Verified at build: the opening sentence begins at character 728, after the label, date and contents block.

The Zenodo record description also carries Phase 0 md5s:

- Arm A: 80c2783a376bed47037ebf778c14cc7e
- Arm B: 3eaf4fa976276888144a01cadd099f9b

## What happened

These values were computed on 16 September 2026 with an in-session method that was never saved. The saved artefacts from that session (four full-page HTML files, two UAs per arm) survive on the VPS and are preserved in this repository at e100/phase0/artefacts-2026-09-16/.

The values cannot be reproduced from those artefacts. Eight tag-strip variants and over 800 html2text/markdownify parameter combinations were tested. Arm B offsets ranged from 520 to 757 depending on the extraction method. None reproduced 728 or the registered md5s.

Arm A reached the opening sentence at offset 0 under every method tested.

## What the Phase 0 claim actually depends on

The substantive Phase 0 claim is that arm B's opening sentence falls outside the approximately 200-character post-H1 snippet window, while arm A's is at the start. This holds under every method tested: arm A offset = 0, arm B offset > 500 in all variants. No method placed arm B's opening sentence inside the 200-character window.

## Pinned method (reproducible reference)

A deterministic extraction script is committed at e100/phase0/snippet_offset.py. Method:

1. Extract the entry-content element from the served page.
2. Tag-strip using Python's html.parser (HTMLParser), skipping script and style content.
3. Decode HTML entities via html.unescape().
4. Collapse all whitespace runs to a single space, strip.
5. Report the character offset of "AI search engines can only cite" and the md5 of the first 200 characters.

### Pinned-method values (29 Sep 2026)

| Source | Arm | UA | Offset | md5 (first 200 chars) |
|--------|-----|----|--------|-----------------------|
| Saved 16 Sep | A | browser | 0 | c47fa4ff85245f843430d9ee52ca8e54 |
| Saved 16 Sep | A | Googlebot | 0 | c47fa4ff85245f843430d9ee52ca8e54 |
| Saved 16 Sep | B | browser | 520 | 6ca4854d0a323ec84dbe1259ff2cf052 |
| Saved 16 Sep | B | Googlebot | 520 | 6ca4854d0a323ec84dbe1259ff2cf052 |
| Live 29 Sep | A | browser | 0 | c47fa4ff85245f843430d9ee52ca8e54 |
| Live 29 Sep | A | Googlebot | 0 | c47fa4ff85245f843430d9ee52ca8e54 |
| Live 29 Sep | B | browser | 520 | 6ca4854d0a323ec84dbe1259ff2cf052 |
| Live 29 Sep | B | Googlebot | 520 | 6ca4854d0a323ec84dbe1259ff2cf052 |

All eight reads are identical. Saved and live match. Browser and Googlebot match (not cloaked). Arm A offset = 0, arm B offset = 520.

### T0 artefact md5s

| File | md5 |
|------|-----|
| e100_a_browser.html | 1f6c5ecdd36c0627493caa47585d6680 |
| e100_a_gbot.html | 1f6c5ecdd36c0627493caa47585d6680 |
| e100_b_browser.html | 50f49ae6cadf0209145204f12c185655 |
| e100_b_gbot.html | 50f49ae6cadf0209145204f12c185655 |

Browser and Googlebot served identical content on both arms (md5 match per arm).

## Index status at capture start (29 Sep 2026)

Phase 0 is a pre-T0 gate (section 2.5: "Gates (all passed before this deposit)"). The registered capture-time abort condition covers index status only (section 2.5: "if either arm drops from the index during the capture window, every call in that window is voided").

Both arms passed the index check on 29 Sep 2026:

- Arm A: GSC "Submitted and indexed", userCanonical = googleCanonical = own URL, INDEXING_ALLOWED, pageFetchState SUCCESSFUL.
- Arm B: GSC "Submitted and indexed", userCanonical = googleCanonical = own URL, INDEXING_ALLOWED, pageFetchState SUCCESSFUL.
- No fold on either arm.

Post_content md5s are unchanged since the 11 Sep freeze:

- ID 2213 (arm A): c397e1b02f90e27b8d9d44217842373a, post_modified_gmt 2026-09-11 08:00:45
- ID 2214 (arm B): 5b9713919af7d157c040dcb07b1eb025, post_modified_gmt 2026-09-11 08:00:45
