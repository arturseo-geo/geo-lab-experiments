#!/usr/bin/env python3
"""E044 W8 single pull — captures raw responses with model_name, appends to CSV.
Does NOT modify e044_session_runner.py. Saves raw JSON for model_name audit."""
import csv, json, time, os, sys, hashlib
from datetime import datetime, timezone
from urllib.parse import urlparse
from pathlib import Path

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
    "hashmeta": ["hashmeta.com"],
}

today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
raw_dir = Path(f"/opt/e044/data/raw_{today.replace('-','')}")
raw_dir.mkdir(parents=True, exist_ok=True)

csv_path = "/opt/e044/data/e044_competitor_rank_log.csv"

results = []
model_names = []

for qid, query, target in QUERIES:
    print(f"[E044-W8] {qid}: {query}", flush=True)
    resp = requests.post(API, auth=(login, pwd),
        json=[{"user_prompt": query, "model_name": "sonar-pro", "web_search": True}],
        timeout=120)
    resp.raise_for_status()
    body = resp.json()

    # Save raw
    raw_bytes = json.dumps(body, indent=2).encode()
    sha = hashlib.sha256(raw_bytes).hexdigest()
    (raw_dir / f"{qid}.json").write_bytes(raw_bytes)

    # Extract model_name
    task = body.get("tasks", [{}])[0]
    result = (task.get("result") or [{}])[0]
    actual_model = result.get("model_name") or result.get("model") or "unknown"
    model_names.append(actual_model)

    # Extract citations
    all_urls = []
    for item in result.get("items", []):
        for sec in item.get("sections", []):
            for ann in sec.get("annotations", []):
                url = ann.get("url", "")
                if url:
                    all_urls.append(url)
    seen = set()
    ranked_urls = []
    for u in all_urls:
        if u not in seen:
            seen.add(u)
            ranked_urls.append(u)

    # Ranks
    thegeolab_rank = 0
    thegeolab_cited = "N"
    for i, u in enumerate(ranked_urls, 1):
        if TARGET_DOMAIN in u:
            thegeolab_rank = i
            thegeolab_cited = "Y"
            break

    def find_comp_rank(domains):
        for i, u in enumerate(ranked_urls, 1):
            for d in domains:
                if d in u:
                    return i
        return 0

    thatware_rank = find_comp_rank(COMPETITORS["thatware"])
    hashmeta_rank = find_comp_rank(COMPETITORS["hashmeta"])

    # Other competitors in top 8
    other_new = []
    other_new_urls = []
    for i, u in enumerate(ranked_urls[:8], 1):
        d = urlparse(u).netloc.lower()
        if d.startswith("www."):
            d = d[4:]
        if d == TARGET_DOMAIN:
            continue
        skip = False
        for comp_domains in COMPETITORS.values():
            for cd in comp_domains:
                if cd in d:
                    skip = True
        if not skip:
            other_new.append(d + "@" + str(i))
            other_new_urls.append(u + "@" + str(i))

    results.append({
        "qid": qid, "query": query,
        "thegeolab_rank": thegeolab_rank,
        "thatware_rank": thatware_rank,
        "hashmeta_rank": hashmeta_rank,
        "thegeolab_cited": thegeolab_cited,
        "other_new": ",".join(other_new[:6]),
        "other_new_urls": "|".join(other_new_urls[:6]),
        "model_name": actual_model,
        "set_size": len(ranked_urls),
    })

    print(f"  model={actual_model} thegeolab={thegeolab_rank} thatware={thatware_rank} hashmeta={hashmeta_rank} cited={thegeolab_cited} set_size={len(ranked_urls)}")
    time.sleep(2)

# Determine surface tag
distinct_models = sorted(set(model_names))
surface = "API-" + distinct_models[0] if len(distinct_models) == 1 else "API-mixed:" + "+".join(distinct_models)
is_new_surface = distinct_models != ["sonar-pro"]

print(f"\nModel names returned: {distinct_models}")
print(f"Surface tag: {surface}")
if is_new_surface:
    print("*** NEW SURFACE DETECTED — rows tagged as non-comparable to prior API-sonar-pro data ***")

# Append to CSV
with open(csv_path, "a", newline="") as f:
    w = csv.writer(f)
    for r in results:
        if is_new_surface:
            notes = f"source:{surface} pull:P1-postretire NEW_SURFACE:not-comparable-to-API-sonar-pro"
        else:
            notes = f"source:{surface} pull:P1 model_verified:{r['model_name']}"
        w.writerow([
            today, r["qid"], r["query"],
            r["thegeolab_rank"], r["thatware_rank"], r["hashmeta_rank"],
            r["thegeolab_cited"], r["other_new"],
            "", "", notes, r["other_new_urls"],
        ])

print(f"\nAppended {len(results)} rows to {csv_path}")
print(f"Raw responses saved to {raw_dir}/")

# Manifest
manifest = raw_dir / "sha256_manifest.txt"
with manifest.open("w") as mf:
    for fp in sorted(raw_dir.glob("*.json")):
        sha = hashlib.sha256(fp.read_bytes()).hexdigest()
        mf.write(f"{sha}  {fp.name}\n")
print(f"Manifest: {manifest}")
