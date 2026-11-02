import sys, json, requests, os
from urllib.parse import urlparse
from dotenv import dotenv_values

cfg = dotenv_values("/opt/geolab-auto-measure/.env")
login = cfg.get("DATAFORSEO_LOGIN", "")
pwd = cfg.get("DATAFORSEO_PASS", "")
API = "https://api.dataforseo.com/v3/ai_optimization/perplexity/llm_responses/live"

query = sys.argv[1]
resp = requests.post(API, auth=(login, pwd),
    json=[{"user_prompt": query, "model_name": "sonar-pro", "web_search": True}],
    timeout=180)
resp.raise_for_status()
body = resp.json()
task = body.get("tasks", [{}])[0]
result = (task.get("result") or [{}])[0]

all_urls = []
for item in result.get("items", []):
    for sec in item.get("sections", []):
        for ann in sec.get("annotations", []):
            url = ann.get("url", "")
            if url:
                all_urls.append(url)

seen = set()
ranked = []
for u in all_urls:
    if u not in seen:
        seen.add(u)
        ranked.append(u)

print(json.dumps({"ranked_urls": ranked, "set_size": len(ranked)}, indent=2))
