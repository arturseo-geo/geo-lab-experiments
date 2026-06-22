"""
E025 M2 — Second post-intervention citation rate measurement
Date: 2026-06-19
Parameters matched to M1 (2026-05-22): same queries, same platforms, same endpoints,
same iteration count, same citation detection logic.

10 queries × 5 iterations × 3 platforms = 150 API calls.
"""

import json
import os
import sys
import time
import csv
from base64 import b64encode
from datetime import datetime, timezone
from pathlib import Path

import requests

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
RAW_DIR = SCRIPT_DIR / "m2_raw"
RAW_DIR.mkdir(exist_ok=True)

TARGET_DOMAIN = "thegeolab.net"

# ── Credentials (from ~/.mcp.json, same method as E014 M2 runner) ────────────
def load_dfs_creds():
    mcp_path = Path.home() / ".mcp.json"
    with open(mcp_path) as f:
        cfg = json.load(f)
    env = cfg["mcpServers"]["dataforseo"]["env"]
    return env["DATAFORSEO_LOGIN"], env["DATAFORSEO_PASSWORD"]

DFS_LOGIN, DFS_PASS = load_dfs_creds()
DFS_AUTH = b64encode(f"{DFS_LOGIN}:{DFS_PASS}".encode()).decode()
DFS_HEADERS = {
    "Authorization": f"Basic {DFS_AUTH}",
    "Content-Type": "application/json",
}

# ── Query set (verbatim from M1 protocol) ─────────────────────────────────────
QUERIES = [
    {"id": "T1-Q1", "tier": "T1", "text": "GEO Stack framework"},
    {"id": "T1-Q2", "tier": "T1", "text": "retrievability in GEO"},
    {"id": "T1-Q3", "tier": "T1", "text": "GEO citation rate measurement"},
    {"id": "T1-Q4", "tier": "T1", "text": "extractability score GEO"},
    {"id": "T1-Q5", "tier": "T1", "text": "Artur Ferreira GEO Lab"},
    {"id": "T2-Q1", "tier": "T2", "text": "what is generative engine optimisation"},
    {"id": "T2-Q2", "tier": "T2", "text": "how to optimise for AI search"},
    {"id": "T2-Q3", "tier": "T2", "text": "AI citation rate factors"},
    {"id": "T2-Q4", "tier": "T2", "text": "how does Perplexity choose sources"},
    {"id": "T2-Q5", "tier": "T2", "text": "GEO vs SEO differences"},
]

DELAY = 2  # seconds between calls


def ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def save_raw(name, data):
    path = RAW_DIR / f"{name}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def extract_slug(url):
    url = url.replace("https://", "").replace("http://", "")
    parts = [p for p in url.split("/") if p]
    return parts[1] if len(parts) > 1 else parts[0] if parts else url


# ── Platform callers (matched to M1/E014 M2 runner) ──────────────────────────

def call_perplexity(query, iteration, query_id):
    """Endpoint: /v3/ai_optimization/perplexity/llm_responses/live (NOT /advanced)"""
    payload = [{
        "user_prompt": query,
        "model_name": "sonar-pro",
        "web_search": True,
    }]
    r = requests.post(
        "https://api.dataforseo.com/v3/ai_optimization/perplexity/llm_responses/live",
        headers=DFS_HEADERS,
        json=payload,
        timeout=60,
    )
    r.raise_for_status()
    raw = r.json()
    save_raw(f"ppx_{query_id}_iter{iteration}", raw)

    try:
        task = raw["tasks"][0]
        task_id = task.get("id", "")
        results = task.get("result") or []
        result = results[0] if results else {}
        items = result.get("items") or []

        annotations = []
        for item in items:
            for section in (item.get("sections") or []):
                for ann in (section.get("annotations") or []):
                    url = ann.get("url", "") if isinstance(ann, dict) else ""
                    if url and url not in annotations:
                        annotations.append(url)
    except (KeyError, IndexError, TypeError) as e:
        print(f"  WARN parse error: {e}")
        task_id = ""
        annotations = []

    cited_domain = [u for u in annotations if TARGET_DOMAIN in u]
    return {
        "task_id": task_id,
        "cited": bool(cited_domain),
        "annotations": annotations,
        "cited_urls": cited_domain,
        "timestamp": ts(),
    }


def call_chatgpt(query, iteration, query_id):
    """Endpoint: /v3/ai_optimization/chat_gpt/llm_scraper/live/advanced"""
    payload = [{
        "keyword": query,
        "location_name": "United Kingdom",
        "language_code": "en",
        "force_web_search": True,
    }]
    r = requests.post(
        "https://api.dataforseo.com/v3/ai_optimization/chat_gpt/llm_scraper/live/advanced",
        headers=DFS_HEADERS,
        json=payload,
        timeout=90,
    )
    r.raise_for_status()
    raw = r.json()
    save_raw(f"gpt_{query_id}_iter{iteration}", raw)

    try:
        task = raw["tasks"][0]
        task_id = task.get("id", "")
        results = task.get("result") or []
        result = results[0] if results else {}
        items = result.get("items") or []

        annotations = []
        for item in items:
            for src in (item.get("sources") or []):
                url = (src.get("url", "") if isinstance(src, dict) else "")
                if url and url not in annotations:
                    annotations.append(url)
            itype = item.get("type", "")
            if "source" in itype or itype == "chat_gpt_source":
                url = item.get("url", "")
                if url and url not in annotations:
                    annotations.append(url)
            for ann in (item.get("annotations") or []):
                url = (ann.get("url", "") if isinstance(ann, dict) else "")
                if url and url not in annotations:
                    annotations.append(url)
    except (KeyError, IndexError, TypeError) as e:
        print(f"  WARN parse error: {e}")
        task_id = ""
        annotations = []

    cited_domain = [u for u in annotations if TARGET_DOMAIN in u]
    return {
        "task_id": task_id,
        "cited": bool(cited_domain),
        "annotations": annotations,
        "cited_urls": cited_domain,
        "timestamp": ts(),
    }


def call_aio(query, iteration, query_id):
    """Google SERP — check ai_overview items for target domain."""
    payload = [{
        "keyword": query,
        "location_name": "United Kingdom",
        "language_code": "en",
        "depth": 10,
    }]
    r = requests.post(
        "https://api.dataforseo.com/v3/serp/google/organic/live/advanced",
        headers=DFS_HEADERS,
        json=payload,
        timeout=60,
    )
    r.raise_for_status()
    raw = r.json()
    save_raw(f"aio_{query_id}_iter{iteration}", raw)

    annotations = []
    aio_present = False
    try:
        task = raw["tasks"][0]
        task_id = task.get("id", "")
        results = task.get("result") or []
        result = results[0] if results else {}
        items = result.get("items") or []

        for item in (items or []):
            itype = item.get("type", "")
            if itype in ("ai_overview", "answer_box", "featured_snippet"):
                aio_present = True
                for ref in (item.get("references") or []):
                    url = ref.get("url", "") if isinstance(ref, dict) else ""
                    if url and url not in annotations:
                        annotations.append(url)
                for sub in (item.get("items") or []):
                    for ref in (sub.get("references") or []):
                        url = ref.get("url", "") if isinstance(ref, dict) else ""
                        if url and url not in annotations:
                            annotations.append(url)
    except (KeyError, IndexError, TypeError) as e:
        print(f"  WARN parse error: {e}")
        task_id = ""

    cited_domain = [u for u in annotations if TARGET_DOMAIN in u]
    return {
        "task_id": task_id,
        "cited": bool(cited_domain),
        "annotations": annotations,
        "cited_urls": cited_domain,
        "aio_present": aio_present,
        "timestamp": ts(),
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{'='*60}")
    print(f"E025 M2 — Citation Rate Measurement — {ts()}")
    print(f"{'='*60}\n")

    rows = []  # CSV output rows

    # ── Perplexity ────────────────────────────────────────────────────────────
    print("── PERPLEXITY (sonar-pro, 5 iters × 10 queries = 50 calls) ──")
    for iteration in range(1, 6):
        print(f"\n  Iteration {iteration}:")
        for q in QUERIES:
            qid = q["id"]
            print(f"    {qid} ({q['tier']}) {q['text'][:50]}...", end=" ", flush=True)
            try:
                res = call_perplexity(q["text"], iteration, qid)
                cited_flag = "Y" if res["cited"] else "N"
                rank = ""
                set_size = len(res["annotations"])
                notes = ""
                if res["cited"]:
                    try:
                        rank = next(i+1 for i, u in enumerate(res["annotations"]) if TARGET_DOMAIN in u)
                    except StopIteration:
                        rank = ""
                    slugs = [extract_slug(u) for u in res["cited_urls"]]
                    notes = f"slug={'|'.join(f'/{s}/' for s in slugs)}"
                rows.append({
                    "query_id": qid, "tier": q["tier"],
                    "platform": "perplexity-sonar-pro",
                    "iteration": iteration, "cited": cited_flag,
                    "thegeolab_rank": rank, "retrieval_set_size": set_size,
                    "notes": notes,
                })
                print(f"[{cited_flag}] size={set_size} {notes}")
            except Exception as e:
                print(f"[ERR] {e}")
                rows.append({
                    "query_id": qid, "tier": q["tier"],
                    "platform": "perplexity-sonar-pro",
                    "iteration": iteration, "cited": "ERR",
                    "thegeolab_rank": "", "retrieval_set_size": 0,
                    "notes": f"error:{e}",
                })
            time.sleep(DELAY)

    # ── ChatGPT ───────────────────────────────────────────────────────────────
    print("\n── CHATGPT (scraper, 5 iters × 10 queries = 50 calls) ──")
    for iteration in range(1, 6):
        print(f"\n  Iteration {iteration}:")
        for q in QUERIES:
            qid = q["id"]
            print(f"    {qid} ({q['tier']}) {q['text'][:50]}...", end=" ", flush=True)
            try:
                res = call_chatgpt(q["text"], iteration, qid)
                cited_flag = "Y" if res["cited"] else "N"
                rank = ""
                set_size = len(res["annotations"])
                notes = ""
                if not res["annotations"]:
                    notes = "no-annotations"
                elif res["cited"]:
                    try:
                        rank = next(i+1 for i, u in enumerate(res["annotations"]) if TARGET_DOMAIN in u)
                    except StopIteration:
                        rank = ""
                    slugs = [extract_slug(u) for u in res["cited_urls"]]
                    notes = f"slug={'|'.join(f'/{s}/' for s in slugs)}"
                rows.append({
                    "query_id": qid, "tier": q["tier"],
                    "platform": "chatgpt-gpt4o-mini",
                    "iteration": iteration, "cited": cited_flag,
                    "thegeolab_rank": rank, "retrieval_set_size": set_size,
                    "notes": notes,
                })
                print(f"[{cited_flag}] size={set_size} {notes}")
            except Exception as e:
                print(f"[ERR] {e}")
                rows.append({
                    "query_id": qid, "tier": q["tier"],
                    "platform": "chatgpt-gpt4o-mini",
                    "iteration": iteration, "cited": "ERR",
                    "thegeolab_rank": "", "retrieval_set_size": 0,
                    "notes": f"error:{e}",
                })
            time.sleep(DELAY)

    # ── Google AIO ────────────────────────────────────────────────────────────
    print("\n── GOOGLE AIO (5 iters × 10 queries = 50 calls) ──")
    for iteration in range(1, 6):
        print(f"\n  Iteration {iteration}:")
        for q in QUERIES:
            qid = q["id"]
            print(f"    {qid} ({q['tier']}) {q['text'][:50]}...", end=" ", flush=True)
            try:
                res = call_aio(q["text"], iteration, qid)
                cited_flag = "Y" if res["cited"] else "N"
                rank = ""
                set_size = len(res["annotations"])
                aio_tag = "type=ai_overview" if res["aio_present"] else "no-aio"
                notes = aio_tag
                if res["cited"]:
                    try:
                        rank = next(i+1 for i, u in enumerate(res["annotations"]) if TARGET_DOMAIN in u)
                    except StopIteration:
                        rank = ""
                    slugs = [extract_slug(u) for u in res["cited_urls"]]
                    notes = f"{aio_tag},slug={'|'.join(f'/{s}/' for s in slugs)}"
                rows.append({
                    "query_id": qid, "tier": q["tier"],
                    "platform": "google-aio",
                    "iteration": iteration, "cited": cited_flag,
                    "thegeolab_rank": rank, "retrieval_set_size": set_size,
                    "notes": notes,
                })
                print(f"[{cited_flag}] {aio_tag} size={set_size}")
            except Exception as e:
                print(f"[ERR] {e}")
                rows.append({
                    "query_id": qid, "tier": q["tier"],
                    "platform": "google-aio",
                    "iteration": iteration, "cited": "ERR",
                    "thegeolab_rank": "", "retrieval_set_size": 0,
                    "notes": f"error:{e}",
                })
            time.sleep(DELAY)

    # ── Write CSV ─────────────────────────────────────────────────────────────
    csv_path = SCRIPT_DIR / "e025_m2_results.csv"
    fieldnames = ["query_id", "tier", "platform", "iteration", "cited",
                   "thegeolab_rank", "retrieval_set_size", "notes"]
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {csv_path} ({len(rows)} rows)")

    # ── Write Summary ─────────────────────────────────────────────────────────
    write_summary(rows)

    print(f"\nM2 run complete at {ts()}")


def write_summary(rows):
    summary_path = SCRIPT_DIR / "e025_m2_summary.txt"

    # Count citations by platform × tier
    def count(platform, tier):
        matching = [r for r in rows if r["platform"] == platform and r["tier"] == tier and r["cited"] == "Y"]
        total = [r for r in rows if r["platform"] == platform and r["tier"] == tier and r["cited"] != "ERR"]
        return len(matching), len(total)

    ppx_t1_c, ppx_t1_t = count("perplexity-sonar-pro", "T1")
    ppx_t2_c, ppx_t2_t = count("perplexity-sonar-pro", "T2")
    gpt_t1_c, gpt_t1_t = count("chatgpt-gpt4o-mini", "T1")
    gpt_t2_c, gpt_t2_t = count("chatgpt-gpt4o-mini", "T2")
    aio_t1_c, aio_t1_t = count("google-aio", "T1")
    aio_t2_c, aio_t2_t = count("google-aio", "T2")

    ppx_t1_pct = ppx_t1_c / ppx_t1_t * 100 if ppx_t1_t else 0
    ppx_t2_pct = ppx_t2_c / ppx_t2_t * 100 if ppx_t2_t else 0
    gpt_t1_pct = gpt_t1_c / gpt_t1_t * 100 if gpt_t1_t else 0
    gpt_t2_pct = gpt_t2_c / gpt_t2_t * 100 if gpt_t2_t else 0
    aio_t1_pct = aio_t1_c / aio_t1_t * 100 if aio_t1_t else 0
    aio_t2_pct = aio_t2_c / aio_t2_t * 100 if aio_t2_t else 0

    # Combined T2
    combined_t2_c = ppx_t2_c + gpt_t2_c + aio_t2_c
    combined_t2_t = ppx_t2_t + gpt_t2_t + aio_t2_t
    combined_t2_pct = combined_t2_c / combined_t2_t * 100 if combined_t2_t else 0

    # Per-query Perplexity breakdown
    ppx_rows = [r for r in rows if r["platform"] == "perplexity-sonar-pro"]
    query_ids_ordered = [q["id"] for q in QUERIES]

    per_query_ppx = {}
    for qid in query_ids_ordered:
        qrows = [r for r in ppx_rows if r["query_id"] == qid and r["cited"] != "ERR"]
        cited_count = sum(1 for r in qrows if r["cited"] == "Y")
        total_count = len(qrows)
        # Get cited slugs
        slugs = set()
        for r in qrows:
            if r["cited"] == "Y" and "slug=" in r.get("notes", ""):
                s = r["notes"].split("slug=")[1]
                slugs.add(s)
        per_query_ppx[qid] = (cited_count, total_count, slugs)

    # Decision tree
    ppx_t1_overall = ppx_t1_c / ppx_t1_t * 100 if ppx_t1_t else 0
    if ppx_t1_overall < 80:
        decision = "CONFOUND ALERT — T1 dropped below 80%, investigate before interpreting T2"
    elif ppx_t2_pct == 0 and combined_t2_pct == 0:
        decision = "STRONG NULL — authority gate holds"
    elif combined_t2_pct > 0 and combined_t2_pct < 22:
        decision = f"NULL WITH LIFT — sub-threshold ({combined_t2_pct:.1f}pp < 22pp), do not claim positive"
    elif combined_t2_pct >= 22:
        decision = f"POSITIVE RESULT — trigger E026 decomposition ({combined_t2_pct:.1f}pp >= 22pp)"
    else:
        decision = "INCONCLUSIVE"

    lines = []
    lines.append("E025 M2 — Citation Rate Summary")
    lines.append(f"Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}  |  57 days post Wave-1 deployment")
    lines.append("=" * 60)
    lines.append("")
    lines.append("Perplexity")
    lines.append(f"  T1: {ppx_t1_c}/{ppx_t1_t} ({ppx_t1_pct:.1f}%)  |  T2: {ppx_t2_c}/{ppx_t2_t} ({ppx_t2_pct:.1f}%)")
    lines.append("ChatGPT")
    lines.append(f"  T1: {gpt_t1_c}/{gpt_t1_t} ({gpt_t1_pct:.1f}%)  |  T2: {gpt_t2_c}/{gpt_t2_t} ({gpt_t2_pct:.1f}%)")
    lines.append("Google AIO")
    lines.append(f"  T1: {aio_t1_c}/{aio_t1_t} ({aio_t1_pct:.1f}%)  |  T2: {aio_t2_c}/{aio_t2_t} ({aio_t2_pct:.1f}%)")
    lines.append("")
    lines.append(f"Combined T2 (all platforms): {combined_t2_c}/{combined_t2_t} ({combined_t2_pct:.1f}%)")
    lines.append("")
    lines.append("M0 Baseline (E016, 2026-04-13):")
    lines.append("  T1 Perplexity M0: 80%")
    lines.append("  T2 Perplexity M0: 0%")
    lines.append("")
    lines.append("M1 Baseline (2026-05-22):")
    lines.append("  T1 Perplexity M1: 80.0% (20/25)")
    lines.append("  T2 Perplexity M1: 0.0% (0/25)")
    lines.append("  Combined T2 M1: 0.0% (0/75)")
    lines.append("")
    lines.append("DECISION TREE OUTCOME:")
    lines.append(f"  {decision}")
    lines.append("")
    lines.append("DETAILED: Perplexity T1 citations by query")
    for qid in query_ids_ordered:
        if qid.startswith("T1"):
            c, t, slugs = per_query_ppx[qid]
            q_text = next(q["text"] for q in QUERIES if q["id"] == qid)
            slug_str = f" slugs={list(slugs)}" if slugs else ""
            lines.append(f"  {qid} ({q_text}): {c}/{t}{slug_str}")
    lines.append("")
    lines.append("DETAILED: Perplexity T2 citations by query")
    for qid in query_ids_ordered:
        if qid.startswith("T2"):
            c, t, slugs = per_query_ppx[qid]
            q_text = next(q["text"] for q in QUERIES if q["id"] == qid)
            slug_str = f" slugs={list(slugs)}" if slugs else ""
            lines.append(f"  {qid} ({q_text}): {c}/{t}{slug_str}")
    lines.append("")

    summary_text = "\n".join(lines)
    with open(summary_path, "w") as f:
        f.write(summary_text)
    print(f"\nWrote {summary_path}")
    print("\n" + summary_text)


if __name__ == "__main__":
    main()
