# E100 Inbound Link — Symmetric Pair

**Source post:** 1872 — "The ChatGPT Pre-Retrieval Gate"
**Anchor text:** Can AI search engines read paywalled content?
**Position:** New item appended after the existing Related `</ul>`, before the closing `</div>` of `.meta-section`

## Diff (apply at publish time only)

**Find:**
```html
    <li><a href="https://thegeolab.net/failure-registry/">GEO Lab Failure Registry</a></li>
  </ul>

  <h2>Sources</h2>
```

**Replace with:**
```html
    <li><a href="https://thegeolab.net/failure-registry/">GEO Lab Failure Registry</a></li>
    <li><a href="https://thegeolab.net/guides/paywalls-and-ai-search-a/">Can AI search engines read paywalled content?</a> · <a href="https://thegeolab.net/guides/paywalls-and-ai-search-b/">Can AI search engines read paywalled content?</a></li>
  </ul>

  <h2>Sources</h2>
```

**Notes:**
- Both arms in the same `<li>`, separated by ` · `, arm A first then arm B
- Identical anchor text (page title) for both arms
- NOT applied to the live post — staged for publish-time deployment
