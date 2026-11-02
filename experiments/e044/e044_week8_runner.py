#!/usr/bin/env python3
"""E044 Week 8 — 2026-06-29. API sonar-pro. Decisive confirm-or-clear."""
import sys, json, time, csv, os
from datetime import datetime, timezone
from urllib.parse import urlparse

sys.path.insert(0, "/opt/geolab-auto-measure")
from dotenv import dotenv_values
import requests

cfg = dotenv_values("/opt/geolab-auto-measure/.env")
login = cfg.get("DATAFORSEO_LOGIN", "")
pwd = cfg.get("DATAFORSEO_PASS", "")
API = "https://api.dataforseo.com/v3/ai_optimization/perplexity/llm_responses/live"
TARGET_DOMAIN = "thegeolab.net"

QUERIES = [
    ("Q1", "what is the GEO Stack framework", "/geo-stack/"),
    ("Q2", "what is extractability in AI search", "/extractability/"),
    ("Q3", "retrieval probability in GEO Stack model", "/retrieval-probability/"),
]

COMPETITORS = {
    "thatware": ["thatware.co", "thatware.in"],
    "hashmeta": ["hashmeta.com", "hashmeta.ai"],
}

# Broadened pollution filter (28 Jun E072 tooling note)
POLLUTION_MARKERS = [
    "geostack-ml", "geostack ml", "geostack-ai", "geostack ai",
    "geophysic", "remote sensing", "remote-sensing",
    "ensemble model", "ensemble learning", "stacking model",
    "satellite imagery", "raster", "lidar", "spectral band",
    "earth observation", "earth-observation",
    "worldscientificnews", "geological", "seismic",
]

def is_pollution(url, title):
    """Flag but don't auto-strip — spot-check before reading stripped rank."""
    haystack = f"{url} {title}".lower()
    return any(m in haystack for m in POLLUTION_MARKERS)


def run_pull(pull_label):
    results = []
    for qid, query, target in QUERIES:
        print(f"  [{pull_label}] {qid}: {query}", flush=True)
        resp = requests.post(API, auth=(login, pwd),
            json=[{"user_prompt": query, "model_name": "sonar-pro", "web_search": True}],
            timeout=120)
        resp.raise_for_status()
        body = resp.json()
        task = body.get("tasks", [{}])[0]
        result = (task.get("result") or [{}])[0]

        all_urls = []
        all_titles = {}
        for item in result.get("items", []):
            for sec in item.get("sections", []):
                for ann in sec.get("annotations", []):
                    url = ann.get("url", "")
                    title = ann.get("title", "")
                    if url:
                        all_urls.append(url)
                        if url not in all_titles:
                            all_titles[url] = title

        seen = set()
        ranked_urls = []
        for u in all_urls:
            if u not in seen:
                seen.add(u)
                ranked_urls.append(u)

        thegeolab_rank = 0
        thegeolab_cited = 0
        thegeolab_url = ""
        for i, u in enumerate(ranked_urls, 1):
            if TARGET_DOMAIN in u:
                thegeolab_rank = i
                thegeolab_cited = 1
                thegeolab_url = u
                break

        def find_comp_rank(domains):
            for i, u in enumerate(ranked_urls, 1):
                for d in domains:
                    if d in u:
                        return i, u
            return 0, ""

        thatware_rank, thatware_url = find_comp_rank(COMPETITORS["thatware"])
        hashmeta_rank, hashmeta_url = find_comp_rank(COMPETITORS["hashmeta"])

        # Build other-new with full URLs
        other_new = []
        other_new_urls = []
        for i, u in enumerate(ranked_urls[:8], 1):
            domain = urlparse(u).netloc.lower()
            if domain.startswith("www."):
                domain = domain[4:]
            if TARGET_DOMAIN not in u and not any(d in u for ds in COMPETITORS.values() for d in ds):
                pollution_flag = " [POLLUTION]" if is_pollution(u, all_titles.get(u, "")) else ""
                other_new.append(f"{domain}@{i}{pollution_flag}")
                other_new_urls.append(u)

        status = "Y" if thegeolab_cited else "N"
        results.append({
            "pull": pull_label, "qid": qid, "query": query,
            "thegeolab_rank": thegeolab_rank, "thatware_rank": thatware_rank,
            "hashmeta_rank": hashmeta_rank, "thegeolab_cited": status,
            "thegeolab_url": thegeolab_url,
            "other_new": ",".join(other_new), "other_new_urls": "|".join(other_new_urls),
            "ranked_urls": ranked_urls, "all_titles": all_titles,
            "set_size": len(ranked_urls),
        })
        print(f"    thegeolab={thegeolab_rank} thatware={thatware_rank} hashmeta={hashmeta_rank} cited={status} set_size={len(ranked_urls)}")
        time.sleep(2)
    return results


TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
print(f"=== E044 WEEK 8 — {TODAY} — PULL 1 ===")
pull1 = run_pull("P1")

print("\nWaiting 13 minutes for pull 2...")
time.sleep(780)

print(f"\n=== E044 WEEK 8 — PULL 2 ===")
pull2 = run_pull("P2")

# Write to CSV
csv_path = "/opt/e044/data/e044_competitor_rank_log.csv"
with open(csv_path, "a", newline="") as f:
    w = csv.writer(f)
    for pull_data in [pull1, pull2]:
        for r in pull_data:
            notes = "source:API-sonar-pro pull:" + r["pull"]
            w.writerow([
                TODAY, r["qid"], r["query"],
                r["thegeolab_rank"], r["thatware_rank"], r["hashmeta_rank"],
                r["thegeolab_cited"], r["other_new"],
                "", "", notes, r["other_new_urls"],
            ])
print(f"\nAppended {len(pull1)+len(pull2)} rows to {csv_path}")

# Stability check
print("\n=== INTRA-SESSION STABILITY (pull 1 vs pull 2) ===")
for i in range(3):
    p1, p2 = pull1[i], pull2[i]
    qid = p1["qid"]
    geo_s = p1["thegeolab_rank"] == p2["thegeolab_rank"]
    tw_s = p1["thatware_rank"] == p2["thatware_rank"]
    hm_s = p1["hashmeta_rank"] == p2["hashmeta_rank"]
    cited_s = p1["thegeolab_cited"] == p2["thegeolab_cited"]
    if geo_s and tw_s and hm_s and cited_s:
        print(f"  {qid}: STABLE (thegeolab={p1['thegeolab_rank']} thatware={p1['thatware_rank']} cited={p1['thegeolab_cited']})")
    else:
        parts = []
        if not geo_s: parts.append(f"thegeolab {p1['thegeolab_rank']}->{p2['thegeolab_rank']}")
        if not tw_s: parts.append(f"thatware {p1['thatware_rank']}->{p2['thatware_rank']}")
        if not hm_s: parts.append(f"hashmeta {p1['hashmeta_rank']}->{p2['hashmeta_rank']}")
        if not cited_s: parts.append(f"cited {p1['thegeolab_cited']}->{p2['thegeolab_cited']}")
        print(f"  {qid}: FLICKER — {', '.join(parts)}")

# Week 7 baseline comparison (HARDCODED to avoid delta-report bug selecting wrong session)
print("\n=== WEEK 8 vs WEEK 7 DELTA (baseline: 2026-06-22, API-sonar-pro) ===")
W7 = {
    "Q1": {"thegeolab_rank": 1, "thatware_rank": 2, "hashmeta_rank": 0, "cited": "Y"},
    "Q2": {"thegeolab_rank": 0, "thatware_rank": 0, "hashmeta_rank": 0, "cited": "N"},
    "Q3": {"thegeolab_rank": 1, "thatware_rank": 0, "hashmeta_rank": 0, "cited": "Y"},
}
for i in range(3):
    p = pull1[i]  # Use pull 1 for delta (first observation)
    qid = p["qid"]
    w7 = W7[qid]
    geo_d = p["thegeolab_rank"] - w7["thegeolab_rank"]
    tw_d = p["thatware_rank"] - w7["thatware_rank"]
    print(f"  {qid}: thegeolab {w7['thegeolab_rank']}->{p['thegeolab_rank']} ({geo_d:+d}), "
          f"thatware {w7['thatware_rank']}->{p['thatware_rank']} ({tw_d:+d}), "
          f"cited {w7['cited']}->{p['thegeolab_cited']}")

# WATCH DECISIONS
print("\n=== WATCH DECISIONS (persistence amendment: 2 consecutive same-surface) ===")

# Watch 1: ThatWare Q1
tw_q1_w7 = W7["Q1"]["thatware_rank"]  # 2
tw_q1_w8 = pull1[0]["thatware_rank"]
tw_q1_w8_p2 = pull2[0]["thatware_rank"]
geo_q1_w8 = pull1[0]["thegeolab_rank"]

print(f"\n  WATCH 1 — ThatWare Q1 T1:")
print(f"    Week 7: ThatWare rank {tw_q1_w7}, thegeolab rank {W7['Q1']['thegeolab_rank']}")
print(f"    Week 8 P1: ThatWare rank {tw_q1_w8}, thegeolab rank {geo_q1_w8}")
print(f"    Week 8 P2: ThatWare rank {tw_q1_w8_p2}, thegeolab rank {pull2[0]['thegeolab_rank']}")

if 1 <= tw_q1_w8 <= 3:
    print(f"    → T1 FIRES: ThatWare rank {tw_q1_w8} (1-3) for 2 consecutive API sessions")
    if geo_q1_w8 == 1 and tw_q1_w8 > 1:
        print(f"    ⚠ FLAG: thegeolab holds rank 1; ThatWare is rank {tw_q1_w8} behind — 'competitor present', not displacement")
        print(f"    → Route: NOTE against E072 for AJ review. Do NOT auto-create experiment.")
    else:
        print(f"    → Route: escalate — displacement risk")
else:
    print(f"    → CLEARED: ThatWare rank {tw_q1_w8} (>3 or absent)")

# Watch 2: /extractability/ Q2
geo_q2_w7 = W7["Q2"]["thegeolab_rank"]  # 0
geo_q2_w8 = pull1[1]["thegeolab_rank"]
cited_q2_w8 = pull1[1]["thegeolab_cited"]
geo_q2_w8_p2 = pull2[1]["thegeolab_rank"]

print(f"\n  WATCH 2 — /extractability/ Q2 T3+T5:")
print(f"    Week 7: thegeolab rank {geo_q2_w7} (absent), cited={W7['Q2']['cited']}")
print(f"    Week 8 P1: thegeolab rank {geo_q2_w8}, cited={cited_q2_w8}")
print(f"    Week 8 P2: thegeolab rank {geo_q2_w8_p2}, cited={pull2[1]['thegeolab_cited']}")

if geo_q2_w8 == 0:
    print(f"    → T3+T5 FIRE: /extractability/ absent + uncited for 2 consecutive API sessions")
    print(f"    → Route: RETRIEVAL-LAYER diagnostic (NOT content rewrite)")
    print(f"      Action: check PerplexityBot crawl date + HTTP status for /extractability/ in nginx logs")
    print(f"      Context: page is canonical/top on 5/6 other engines — Perplexity-sonar ingestion gap")
    print(f"      Freeze note: page double-frozen under E025 T1 + E047 — do NOT propose rewrite")
else:
    print(f"    → CLEARED: /extractability/ returned at rank {geo_q2_w8}")

# Watch 3: Q3 control
geo_q3 = pull1[2]["thegeolab_rank"]
print(f"\n  Q3 CONTROL: thegeolab rank {geo_q3} (expected ~1)")

# E081 note
print(f"\n  E081 NOTE (29 Jun gate): Q2 /extractability/ {'ABSENT' if geo_q2_w8 == 0 else f'PRESENT rank {geo_q2_w8}'} on sonar — data point for cross-engine prediction")

# Pollution spot-check
print(f"\n=== POLLUTION FLAGS (spot-check, not auto-stripped) ===")
all_flagged = []
for pull_data in [pull1, pull2]:
    for r in pull_data:
        for i, u in enumerate(r["ranked_urls"][:10], 1):
            t = r["all_titles"].get(u, "")
            if is_pollution(u, t):
                entry = f"  {r['pull']} {r['qid']} rank {i}: {urlparse(u).netloc} — \"{t[:60]}\""
                if entry not in [e for e in all_flagged]:
                    all_flagged.append(entry)
                    print(entry)
if not all_flagged:
    print("  (none flagged)")

# Save JSON
json_out = f"/opt/e044/data/e044_week8_{TODAY}.json"
def clean(r):
    return {k: v for k, v in r.items() if k not in ["ranked_urls", "all_titles"]}
with open(json_out, "w") as f:
    json.dump({"date": TODAY, "week": 8, "surface": "API-sonar-pro",
               "pull1": [clean(r) for r in pull1],
               "pull2": [clean(r) for r in pull2]}, f, indent=2)
print(f"\nJSON: {json_out}")
print(f"\n=== WEEK 8 COMPLETE ===")
