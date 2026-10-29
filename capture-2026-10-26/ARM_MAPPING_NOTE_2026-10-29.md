# E097 arm mapping note, 29 Oct 2026

Dated addendum. It preserves and does not change the scorer or any committed output.

What the committed output says: e097_summary.json in commit c651512 (sha256 9240ba181ca03e7845996e143e86a1c8539b9fdf03ff8b8cf69e3c9f5cba4900) lists, under AMBIGUITIES, that the E097 v1.4 text does not label hreflang-and-ai-search-explained as A and p48213 as B next to the URLs, and that the mapping was taken from the order in section 1, to be confirmed. That line was written into the scorer before this check.

```
"E097 v1.4 does not label hreflang-and-ai-search-explained as A and p48213 as B next to the URLs; mapping taken from the order in section 1, to be confirmed"
```

Where the scorer took the mapping from: the order in section 1 of the E097 v1.4 text.

```python
    # E097 v1.4 section 1 lists the pair as descriptive vs opaque slug, in this order.
    # The v1.4 text does not label them A and B explicitly next to the URLs: confirm
    # against the freeze manifest before the run (see AMBIGUITIES in the summary).
    "e097": {"A": "https://thegeolab.net/guides/hreflang-and-ai-search-explained/",
             "B": "https://thegeolab.net/guides/p48213/"},
```

Evidence that confirms it: the freeze zip `/home/ajdev/study-data/e100-e097-capture-2026-10-26/e100-e097-transparency-2026-10-27.zip` (sha256 8cff2893288bdffab6a137241a6fa40d46b1a9d36b01591e1bf05d1be2adf8f2) contains e097-v1.4/arm_gate_pre.json and e097-v1.4/arm_gate_post.json, both listed in MANIFEST-SHA256.txt.

Manifest lines:

```
eea68f73738c60356a8bdffc657eaecae471979e6fe39c77f0d2c6a6fa7300c4  e097-v1.4/arm_gate_pre.json
4d34a2b825a0d5ef687d32855eeb41484aa84f67996ee36f630e0ea385f2f394  e097-v1.4/arm_gate_post.json
```

Computed sha256 of each file extracted from the zip:

```
eea68f73738c60356a8bdffc657eaecae471979e6fe39c77f0d2c6a6fa7300c4  e097-v1.4/arm_gate_pre.json   — matches manifest
4d34a2b825a0d5ef687d32855eeb41484aa84f67996ee36f630e0ea385f2f394  e097-v1.4/arm_gate_post.json  — matches manifest
```

Both files assign label A to https://thegeolab.net/guides/hreflang-and-ai-search-explained/ and label B to https://thegeolab.net/guides/p48213/.

arm_gate_pre.json (checked_utc 2026-10-26T12:23:10.676251+00:00):

```json
"arms": [
  {
    "label": "A",
    "registered_url": "https://thegeolab.net/guides/hreflang-and-ai-search-explained/",
    "http_status": 200,
    "final_url": "https://thegeolab.net/guides/hreflang-and-ai-search-explained/",
    "redirected": false,
    "canonical": "https://thegeolab.net/guides/hreflang-and-ai-search-explained/",
    "self_canonical": true,
    "bytes": 84243,
    "ok": true
  },
  {
    "label": "B",
    "registered_url": "https://thegeolab.net/guides/p48213/",
    "http_status": 200,
    "final_url": "https://thegeolab.net/guides/p48213/",
    "redirected": false,
    "canonical": "https://thegeolab.net/guides/p48213/",
    "self_canonical": true,
    "bytes": 84139,
    "ok": true
  }
]
```

arm_gate_post.json (checked_utc 2026-10-26T12:37:39.062813+00:00):

```json
"arms": [
  {
    "label": "A",
    "registered_url": "https://thegeolab.net/guides/hreflang-and-ai-search-explained/",
    "http_status": 200,
    "final_url": "https://thegeolab.net/guides/hreflang-and-ai-search-explained/",
    "redirected": false,
    "canonical": "https://thegeolab.net/guides/hreflang-and-ai-search-explained/",
    "self_canonical": true,
    "bytes": 84243,
    "ok": true
  },
  {
    "label": "B",
    "registered_url": "https://thegeolab.net/guides/p48213/",
    "http_status": 200,
    "final_url": "https://thegeolab.net/guides/p48213/",
    "redirected": false,
    "canonical": "https://thegeolab.net/guides/p48213/",
    "self_canonical": true,
    "bytes": 84139,
    "ok": true
  }
]
```

MANIFEST-SHA256.txt itself holds only file names and hashes and does not state the mapping.

Result: the scorer, the committed output and both arm gate files agree. A = hreflang-and-ai-search-explained, B = p48213. No output, count or reading changes.

Limits: this checks the mapping only. It is the same freeze zip and the same Claude tooling as the earlier steps. The earlier method record line saying the mapping was confirmed from the freeze manifest is read as meaning the arm gate files covered by the manifest.
