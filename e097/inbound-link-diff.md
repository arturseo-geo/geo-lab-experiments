# E097 Inbound Link — Symmetric Pair

**Source post:** 1875 — "What AI Search Engines Actually Do With Your Content"
**Anchor text:** Hreflang and AI search: which language version gets cited, and why
**Position:** New paragraph appended after the existing Related `</ul>`, before the closing `</div>` of `.meta-section`

## Diff (apply at publish time only)

**Find:**
```html
    <li><a href="https://thegeolab.net/geo-glossary/">The GEO Glossary: 200+ AI Search Terms Defined</a></li>
  </ul>
</div>
```

**Replace with:**
```html
    <li><a href="https://thegeolab.net/geo-glossary/">The GEO Glossary: 200+ AI Search Terms Defined</a></li>
    <li><a href="https://thegeolab.net/guides/hreflang-and-ai-search-explained/">Hreflang and AI search: which language version gets cited, and why</a> · <a href="https://thegeolab.net/guides/p48213/">Hreflang and AI search: which language version gets cited, and why</a></li>
  </ul>
</div>
```

**Notes:**
- Both arms in the same `<li>`, separated by ` · `, arm A first then arm B
- Identical anchor text (page title) for both arms
- NOT applied to the live post — staged for publish-time deployment
