#!/usr/bin/env python3
"""E044 competitor rank monitoring. API sonar-pro surface."""
import argparse
import fcntl
import hashlib
import sys, json, time, csv, os, shutil
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

POLLUTION_MARKERS = [
    "geostack-ml", "geostack ml", "geostack-ai", "geostack ai",
    "geophysic", "remote sensing", "remote-sensing",
    "ensemble model", "ensemble learning", "stacking model",
    "satellite imagery", "raster", "lidar", "spectral band",
    "earth observation", "earth-observation",
    "worldscientificnews", "geological", "seismic",
    "vision-language", "visual grounding",
    "clip adapter", "catastrophic forgetting", "quasi-abelian",
    "2605.06477",
    "gis.stackexchange", "stats.stackexchange",
    "quantitativeimaginglaboratory",
    "pubs.geoscienceworld",
    "osgeo", "foss4g",
]


def is_pollution(url, title="", snippet=""):
    haystack = (url + " " + title + " " + snippet).lower()
    return any(m in haystack for m in POLLUTION_MARKERS)


CSV_HEADER = ["session_date", "query_id", "query_text", "thegeolab_rank",
              "thatware_rank", "hashmeta_rank", "thegeolab_cited",
              "other_new_competitors", "thegeolab_snippet", "rank1_snippet",
              "rank1_domain", "other_new_urls"]


def count_session_rows(csv_path, date):
    if not os.path.exists(csv_path):
        return 0
    with open(csv_path, newline="") as f:
        return sum(1 for row in csv.DictReader(f) if row.get("session_date") == date)


def write_rows(csv_path, pull1, pull2, today):
    write_header = not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0
    with open(csv_path, "a", newline="") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(CSV_HEADER)
        for pull_data in [pull1, pull2]:
            for r in pull_data:
                notes = "source:API-sonar-pro pull:" + r["pull"]
                w.writerow([
                    today, r["qid"], r["query"],
                    r["thegeolab_rank"], r["thatware_rank"], r["hashmeta_rank"],
                    r["thegeolab_cited"], r["other_new"],
                    "", "", notes, r.get("other_new_urls", ""),
                ])


def save_raw(raw_responses, pull_label, raw_dir):
    """Write raw API responses for one pull immediately."""
    os.makedirs(raw_dir, exist_ok=True)
    manifest_path = os.path.join(raw_dir, "sha256_manifest.txt")
    new_entries = {}
    for qid, body in raw_responses:
        fname = "%s_%s.json" % (qid, pull_label)
        fpath = os.path.join(raw_dir, fname)
        blob = json.dumps(body, indent=2)
        with open(fpath, "w") as f:
            f.write(blob)
        sha = hashlib.sha256(blob.encode()).hexdigest()
        new_entries[fname] = "%s  %s" % (sha, fname)
    # Replace existing lines for the same filenames, append new ones
    existing_lines = []
    if os.path.exists(manifest_path):
        with open(manifest_path) as f:
            existing_lines = [l.rstrip("\n") for l in f if l.strip()]
    kept = [l for l in existing_lines if l.split("  ", 1)[-1] not in new_entries]
    kept.extend(new_entries.values())
    with open(manifest_path, "w") as f:
        f.write("\n".join(kept) + "\n")
    print("  Raw %s saved to %s (%d files)" % (pull_label, raw_dir, len(raw_responses)))


QUERIES = [
    ("Q1", "what is the GEO Stack framework", "/geo-stack/"),
    ("Q2", "what is extractability in AI search", "/extractability/"),
    ("Q3", "retrieval probability in GEO Stack model", "/retrieval-probability/"),
]

COMPETITORS = {
    "thatware": ["thatware.co", "thatware.in"],
    "hashmeta": ["hashmeta.com"],
}

WEEK6_ENTRANTS = ["gotoclient", "lauralake", "nrlc.ai", "authoritytech.io"]


def url_domain(u):
    d = urlparse(u).netloc.lower()
    if d.startswith("www."):
        d = d[4:]
    return d


def run_pull(pull_label):
    results = []
    raw_responses = []
    for qid, query, target in QUERIES:
        print("  [%s] %s: %s" % (pull_label, qid, query), flush=True)
        resp = requests.post(API, auth=(login, pwd),
            json=[{"user_prompt": query, "model_name": "sonar-pro", "web_search": True}],
            timeout=120)
        resp.raise_for_status()
        body = resp.json()
        raw_responses.append((qid, body))
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
        ranked_urls = []
        for u in all_urls:
            if u not in seen:
                seen.add(u)
                ranked_urls.append(u)

        thegeolab_rank = 0
        thegeolab_cited = 0
        for i, u in enumerate(ranked_urls, 1):
            if url_domain(u) == TARGET_DOMAIN:
                thegeolab_rank = i
                thegeolab_cited = 1
                break

        def find_comp_rank(domains):
            for i, u in enumerate(ranked_urls, 1):
                for d in domains:
                    if d in url_domain(u):
                        return i
            return 0

        thatware_rank = find_comp_rank(COMPETITORS["thatware"])
        hashmeta_rank = find_comp_rank(COMPETITORS["hashmeta"])

        other_new = []
        for i, u in enumerate(ranked_urls[:8], 1):
            domain = url_domain(u)
            if domain == TARGET_DOMAIN:
                continue
            skip = False
            for comp_domains in COMPETITORS.values():
                for d in comp_domains:
                    if d in domain:
                        skip = True
            if not skip:
                tag = " [POLLUTION]" if is_pollution(u) else ""
                other_new.append(domain + "@" + str(i) + tag)

        # ADDITIVE (2026-06-23): full URLs with rank for source-set traceability
        other_new_urls = []
        for i, u in enumerate(ranked_urls[:8], 1):
            domain = url_domain(u)
            if domain == TARGET_DOMAIN:
                continue
            skip = False
            for comp_domains in COMPETITORS.values():
                for cd in comp_domains:
                    if cd in domain:
                        skip = True
            if not skip:
                other_new_urls.append(u + "@" + str(i))

        # Compute pollution-stripped thegeolab rank
        pollution_stripped_rank = 0
        clean_pos = 0
        for u in ranked_urls:
            if is_pollution(u):
                continue
            clean_pos += 1
            if url_domain(u) == TARGET_DOMAIN:
                pollution_stripped_rank = clean_pos
                break

        row = {
            "qid": qid, "query": query, "target": target,
            "thegeolab_rank": thegeolab_rank,
            "pollution_stripped_rank": pollution_stripped_rank,
            "thatware_rank": thatware_rank,
            "hashmeta_rank": hashmeta_rank,
            "thegeolab_cited": "Y" if thegeolab_cited else "N",
            "other_new": ",".join(other_new[:6]),
            "other_new_urls": "|".join(other_new_urls[:6]),
            "retrieval_set_size": len(ranked_urls),
            "pull": pull_label,
            "ranked_urls": ranked_urls,
        }
        results.append(row)
        status = "CITED" if thegeolab_cited else "ABSENT"
        print("    thegeolab=%d stripped=%d thatware=%d hashmeta=%d %s set_size=%d" % (
            thegeolab_rank, pollution_stripped_rank,
            thatware_rank, hashmeta_rank, status, len(ranked_urls)))
        time.sleep(2)
    return results, raw_responses


def main():
    ap = argparse.ArgumentParser(description="E044 competitor rank session runner")
    ap.add_argument("--force", action="store_true",
                    help="Back up and replace existing rows for today. "
                         "Requires a full dual-pull run (P1 + 13 min + P2).")
    ap.add_argument("--week", type=int, default=None,
                    help="Week number for banners (optional)")
    ap.add_argument("--csv", default="/opt/e044/data/e044_competitor_rank_log.csv")
    ap.add_argument("--json-dir", default="/opt/e044/data")
    ap.add_argument("--lock", default="/opt/e044/data/e044_runner.lock")
    args = ap.parse_args()

    csv_path = args.csv
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    week_tag = "WEEK %d" % args.week if args.week else today
    json_out = os.path.join(args.json_dir, "e044_week7_%s.json" % today)
    raw_dir = os.path.join(args.json_dir, "raw_%s" % today.replace("-", ""))

    # --- Exclusive lock: prevent concurrent runs ---
    lock_dir = os.path.dirname(args.lock)
    if lock_dir and not os.path.isdir(lock_dir):
        os.makedirs(lock_dir, exist_ok=True)
    lock_fd = open(args.lock, "w")
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("LOCKED: another runner holds %s. No session recorded." % args.lock)
        lock_fd.close()
        sys.exit(3)
    lock_fd.write("pid=%d started=%s\n" % (os.getpid(), datetime.now(timezone.utc).isoformat()))
    lock_fd.flush()

    # --- Pre-flight: check for existing rows BEFORE any API call ---
    existing = count_session_rows(csv_path, today)
    if existing > 0 and not args.force:
        print("SKIP: %s already has %d rows in %s. No session recorded." % (today, existing, csv_path))
        print("Pass --force to back up and replace.")
        lock_fd.close()
        sys.exit(3)
    if existing > 0 and args.force:
        print("--force: %d existing rows for %s will be replaced after pulls complete." % (existing, today))

    # --- Pull 1 ---
    print("=== E044 %s -- PULL 1 ===" % week_tag)
    pull1, raw1 = run_pull("P1")
    save_raw(raw1, "P1", raw_dir)

    print("\nWaiting 13 minutes for pull 2...")
    time.sleep(780)

    # --- Pull 2 ---
    print("\n=== E044 %s -- PULL 2 ===" % week_tag)
    pull2, raw2 = run_pull("P2")
    save_raw(raw2, "P2", raw_dir)

    # --- Force deletion: inside lock, after both pulls, before write ---
    if args.force:
        existing_now = count_session_rows(csv_path, today)
        if existing_now > 0:
            bak = csv_path + ".bak.force.%s" % today
            shutil.copy2(csv_path, bak)
            print("--force: backed up %s to %s" % (csv_path, bak))
            rows_keep = []
            with open(csv_path, newline="") as f:
                reader = csv.reader(f)
                header = next(reader)
                for row in reader:
                    if row[0] != today:
                        rows_keep.append(row)
            with open(csv_path, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(header)
                w.writerows(rows_keep)
            print("--force: removed %d existing rows for %s" % (existing_now, today))

    # --- Pre-write assertion (inside lock) ---
    pre_count = count_session_rows(csv_path, today)
    assert pre_count == 0, (
        "INTEGRITY FAIL before write: %s already has %d rows for %s" % (csv_path, pre_count, today))

    # --- Write CSV ---
    write_rows(csv_path, pull1, pull2, today)
    print("\nAppended 6 rows to %s" % csv_path)

    # --- Post-write assertion ---
    final = count_session_rows(csv_path, today)
    assert final == 6, "INTEGRITY FAIL after write: %s has %d rows, expected 6" % (csv_path, final)

    # Stability check
    print("\n=== INTRA-SESSION STABILITY ===")
    for i in range(3):
        p1, p2 = pull1[i], pull2[i]
        qid = p1["qid"]
        geo_stable = p1["thegeolab_rank"] == p2["thegeolab_rank"]
        tw_stable = p1["thatware_rank"] == p2["thatware_rank"]
        if geo_stable and tw_stable:
            print("  %s: STABLE (thegeolab=%d, thatware=%d)" % (
                qid, p1["thegeolab_rank"], p1["thatware_rank"]))
        else:
            parts = []
            if not geo_stable:
                parts.append("thegeolab %d->%d" % (p1["thegeolab_rank"], p2["thegeolab_rank"]))
            if not tw_stable:
                parts.append("thatware %d->%d" % (p1["thatware_rank"], p2["thatware_rank"]))
            print("  %s: FLICKER -- %s" % (qid, ", ".join(parts)))

    # Durability check
    print("\n=== WEEK 6 ENTRANT DURABILITY ===")
    all_pull_urls = []
    for pull_data in [pull1, pull2]:
        for r in pull_data:
            all_pull_urls.extend(r["ranked_urls"])
    all_urls_str = " ".join(all_pull_urls)

    for ent in WEEK6_ENTRANTS:
        found = ent in all_urls_str
        status = "CONFIRMED DURABLE" if found else "CHURNED"
        print("  %s: %s" % (ent, status))

    # Escalation check
    print("\n=== ESCALATION CHECK ===")
    prior_rows = []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            if row["session_date"] != today:
                prior_rows.append(row)

    prior_dates = sorted(set(r["session_date"] for r in prior_rows), reverse=True)
    if prior_dates:
        last_date = prior_dates[0]
        print("  Prior session: %s" % last_date)
        for qid_check in ["Q1", "Q2", "Q3"]:
            prior_q = [r for r in prior_rows if r["session_date"] == last_date and r["query_id"] == qid_check]
            curr_p1 = [r for r in [pull1[j] for j in range(3)] if r["qid"] == qid_check]
            if prior_q and curr_p1:
                pq = prior_q[0]
                cq = curr_p1[0]
                tw_curr = cq["thatware_rank"]
                tw_prev = int(pq.get("thatware_rank", 0) or 0)
                if 1 <= tw_curr <= 3 and 1 <= tw_prev <= 3:
                    print("  T1 FIRE: %s -- ThatWare rank %d (prior %d) -- 2 consecutive!" % (
                        qid_check, tw_curr, tw_prev))
                elif 1 <= tw_curr <= 3:
                    print("  T1 watch: %s -- ThatWare rank %d this week (prior %d)" % (
                        qid_check, tw_curr, tw_prev))
                geo_curr = cq["thegeolab_rank"]
                geo_prev = int(pq.get("thegeolab_rank", 0) or 0)
                if geo_curr == 0 and geo_prev == 0:
                    print("  T3 FIRE: %s -- thegeolab absent 2 consecutive sessions!" % qid_check)
                elif geo_curr == 0:
                    print("  T3 watch: %s -- thegeolab absent this week (prior rank %d)" % (
                        qid_check, geo_prev))
                cited_curr = cq["thegeolab_cited"]
                cited_prev = pq.get("thegeolab_cited", "")
                if cited_curr == "N" and cited_prev == "N":
                    print("  T5 FIRE: %s -- thegeolab not cited 2 consecutive!" % qid_check)
                elif cited_curr == "N":
                    print("  T5 watch: %s -- thegeolab not cited this week (prior: %s)" % (
                        qid_check, cited_prev))
    else:
        print("  No prior sessions found for comparison")

    # Save JSON
    with open(json_out, "w") as f:
        def clean(r):
            return {k: v for k, v in r.items()}
        json.dump({"date": today, "pull1": [clean(r) for r in pull1],
                   "pull2": [clean(r) for r in pull2]}, f, indent=2)
    print("\nJSON: %s" % json_out)
    print("\n=== COMPLETE ===")

    lock_fd.close()


if __name__ == "__main__":
    main()
