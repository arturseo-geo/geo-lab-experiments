#!/usr/bin/env python3
"""
E044 Weekly Delta Report
Reads e044_competitor_rank_log.csv and produces a structured diff
comparing the two most recent session dates.

Usage:
    python3 e044_delta_report.py --csv /path/to/e044_competitor_rank_log.csv --date 2026-05-20
"""

import csv
import argparse
import sys
import os
from datetime import datetime
from collections import defaultdict

REPORTS_DIR = "/opt/e044/reports"

QUERY_LABELS = {}  # populated from CSV


def load_csv(path):
    """Returns list of dicts from CSV, sorted by session_date asc."""
    if not os.path.exists(path):
        print(f"ERROR: CSV not found at {path}", file=sys.stderr)
        sys.exit(1)
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    rows.sort(key=lambda r: r["session_date"])
    return rows


def get_two_most_recent_dates(rows):
    dates = sorted(set(r["session_date"] for r in rows), reverse=True)
    if len(dates) < 2:
        return dates[0], None
    return dates[0], dates[1]


def rows_for_date(rows, date):
    return {r["query_id"]: r for r in rows if r["session_date"] == date}


def safe_int(val):
    """Convert rank string to int; 0 or empty = absent."""
    try:
        v = int(val)
        return v if v > 0 else 0
    except (ValueError, TypeError):
        return 0


def rank_delta(old, new):
    if old == 0 and new == 0:
        return "absent → absent (STABLE)"
    if old == 0 and new > 0:
        return f"absent → rank {new} (APPEARED ✨)"
    if old > 0 and new == 0:
        return f"rank {old} → absent (DROPPED OUT ❌)"
    diff = old - new  # positive = moved up (lower number)
    if diff == 0:
        return f"rank {old} → {new} (STABLE)"
    if diff > 0:
        return f"rank {old} → {new} (UP {diff} ⬆️{'🏆' if new == 1 else ''})"
    return f"rank {old} → {new} (DOWN {abs(diff)} ⬇️)"


def cited_delta(old_str, new_str):
    old = old_str.strip().upper() if old_str else "N"
    new = new_str.strip().upper() if new_str else "N"
    old_yn = "YES" if old in ("Y", "YES", "1", "TRUE") else "NO"
    new_yn = "YES" if new in ("Y", "YES", "1", "TRUE") else "NO"
    if old_yn == new_yn:
        return f"{old_yn} → {new_yn} (stable)"
    return f"{old_yn} → {new_yn} ({'GAINED ✅' if new_yn == 'YES' else 'LOST 🚨'})"


def parse_competitors(field):
    """Parse other_new_competitors field — expects 'domain@rank' pairs, comma-separated."""
    if not field or not field.strip():
        return {}
    result = {}
    for item in field.split(","):
        item = item.strip()
        if "@" in item:
            parts = item.rsplit("@", 1)
            domain = parts[0].strip()
            try:
                rank = int(parts[1].strip())
            except ValueError:
                rank = 0
            result[domain] = rank
        elif item:
            result[item] = 0
    return result


def get_all_queries(rows):
    """Return ordered list of (query_id, query_text)."""
    seen = {}
    for r in rows:
        qid = r["query_id"]
        if qid not in seen:
            seen[qid] = r.get("query_text", qid)
    return list(seen.items())


def build_rank_history(rows, query_id, field):
    """All sessions sorted asc for a given query + field."""
    dates = sorted(set(r["session_date"] for r in rows))
    history = []
    by_date = defaultdict(dict)
    for r in rows:
        by_date[r["session_date"]][r["query_id"]] = r
    for d in dates:
        row = by_date[d].get(query_id)
        history.append(safe_int(row[field]) if row else 0)
    return history, dates


def trend_label(history):
    if len(history) < 2:
        return "insufficient data"
    non_zero = [x for x in history if x > 0]
    if not non_zero:
        return "absent all sessions"
    if history[-1] == 0:
        return "dropped out ❌"
    if history[0] == 0:
        return "recently appeared"
    diffs = [history[i] - history[i + 1] for i in range(len(history) - 1)]  # positive = rank improved
    ups = sum(1 for d in diffs if d > 0)
    downs = sum(1 for d in diffs if d < 0)
    if ups > downs:
        return "improving ⬆️"
    if downs > ups:
        return "declining ⬇️"
    return "stable"


def check_escalations(this_week, prev_week, all_queries, rows):
    triggers = []

    for qid, qtext in all_queries:
        curr = this_week.get(qid)
        prev = prev_week.get(qid) if prev_week else None

        if curr is None:
            continue

        # T1: thatware or hashmeta rank 1-3
        for comp, label in [("thatware_rank", "ThatWare"), ("hashmeta_rank", "Hashmeta")]:
            r = safe_int(curr.get(comp, 0))
            if 1 <= r <= 3:
                triggers.append(f"🚨 T1 FIRED: {qtext} — {label} at rank {r}")

        # T2: thegeolab_rank = 0
        if safe_int(curr.get("thegeolab_rank", 0)) == 0:
            triggers.append(f"🚨 T2 FIRED: thegeolab.net absent on '{qtext}'")

        # T4: new domain in top 5 not seen before
        curr_comps = parse_competitors(curr.get("other_new_competitors", ""))
        all_prev_comps = set()
        for r in rows:
            if r["session_date"] < curr["session_date"] and r["query_id"] == qid:
                all_prev_comps.update(parse_competitors(r.get("other_new_competitors", "")).keys())
        for domain, rank in curr_comps.items():
            if domain not in all_prev_comps and rank > 0 and rank <= 5:
                triggers.append(f"⚠️  T4: New competitor '{domain}' at rank {rank} on '{qtext}'")

    # T3: thegeolab_cited = 0 for 2+ consecutive sessions
    by_date = defaultdict(dict)
    for r in rows:
        by_date[r["session_date"]][r["query_id"]] = r
    dates_sorted = sorted(by_date.keys())
    for qid, qtext in all_queries:
        consecutive = 0
        max_consec = 0
        for d in dates_sorted:
            row = by_date[d].get(qid)
            if row:
                cited = row.get("thegeolab_cited", "N").strip().upper()
                if cited not in ("Y", "YES", "1", "TRUE"):
                    consecutive += 1
                    max_consec = max(max_consec, consecutive)
                else:
                    consecutive = 0
        if max_consec >= 2:
            triggers.append(f"🚨 T3 FIRED: thegeolab.net uncited for 2+ consecutive sessions on '{qtext}'")

    return triggers


def generate_report(csv_path, report_date_str):
    rows = load_csv(csv_path)
    all_queries = get_all_queries(rows)

    this_date, prev_date = get_two_most_recent_dates(rows)
    this_week = rows_for_date(rows, this_date)
    prev_week = rows_for_date(rows, prev_date) if prev_date else {}

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = []

    lines.append("=" * 60)
    lines.append(f"E044 WEEKLY DELTA REPORT — {report_date_str}")
    lines.append(f"Generated: {now}")
    if prev_date:
        lines.append(f"Comparing: {this_date} vs {prev_date} (prior session)")
    else:
        lines.append(f"Single session only: {this_date} — no comparison available")
    lines.append("=" * 60)

    # ── ESCALATION STATUS ──
    lines.append("\nESCALATION STATUS")
    lines.append("-" * 40)
    triggers = check_escalations(this_week, prev_week if prev_week else None, all_queries, rows)
    if triggers:
        for t in triggers:
            lines.append(f"  {t}")
    else:
        lines.append("  ✅  No escalation triggers fired")

    if not prev_date:
        lines.append("\n[No prior session — delta sections skipped]")
        return "\n".join(lines)

    # ── RANK CHANGES — thegeolab.net ──
    lines.append("\nRANK CHANGES — thegeolab.net")
    lines.append("-" * 40)
    for qid, qtext in all_queries:
        curr = this_week.get(qid, {})
        prev = prev_week.get(qid, {})
        tgl_curr = safe_int(curr.get("thegeolab_rank", 0))
        tgl_prev = safe_int(prev.get("thegeolab_rank", 0))
        cited_curr = curr.get("thegeolab_cited", "N")
        cited_prev = prev.get("thegeolab_cited", "N")
        lines.append(f"\n{qid} ({qtext}):")
        lines.append(f"  thegeolab: {rank_delta(tgl_prev, tgl_curr)}")
        lines.append(f"  cited:     {cited_delta(cited_prev, cited_curr)}")

    # ── COMPETITOR MOVEMENTS ──
    lines.append("\nCOMPETITOR MOVEMENTS")
    lines.append("-" * 40)
    for comp_field, comp_label in [("thatware_rank", "ThatWare"), ("hashmeta_rank", "Hashmeta")]:
        lines.append(f"\n{comp_label}:")
        any_present = False
        for qid, qtext in all_queries:
            curr = this_week.get(qid, {})
            prev = prev_week.get(qid, {})
            r_curr = safe_int(curr.get(comp_field, 0))
            r_prev = safe_int(prev.get(comp_field, 0))
            if r_curr == 0 and r_prev == 0:
                continue
            any_present = True
            lines.append(f"  {qid}: {rank_delta(r_prev, r_curr)}")
        if not any_present:
            lines.append("  All queries: absent → absent (stable)")

    # ── NEW ENTRANTS ──
    lines.append("\nNEW ENTRANTS THIS WEEK")
    lines.append("-" * 40)
    new_entrants = []
    for qid, qtext in all_queries:
        curr = this_week.get(qid, {})
        prev = prev_week.get(qid, {})
        curr_comps = parse_competitors(curr.get("other_new_competitors", ""))
        prev_comps = parse_competitors(prev.get("other_new_competitors", ""))
        # Also collect domains seen in any earlier session
        all_prev_domains = set(prev_comps.keys())
        for r in rows:
            if r["session_date"] < this_date and r["query_id"] == qid:
                all_prev_domains.update(parse_competitors(r.get("other_new_competitors", "")).keys())
        for domain, rank in curr_comps.items():
            if domain not in all_prev_domains:
                rank_str = f"rank {rank}" if rank > 0 else "rank unknown"
                new_entrants.append(f"  {domain}: {qid} {rank_str} (NEW — substitution risk)")
    if new_entrants:
        for e in new_entrants:
            lines.append(e)
    else:
        lines.append("  None")

    # ── DROPPED OUT ──
    lines.append("\nDOMAINS THAT DROPPED OUT")
    lines.append("-" * 40)
    dropped = []
    for qid, qtext in all_queries:
        curr = this_week.get(qid, {})
        prev = prev_week.get(qid, {})
        curr_comps = parse_competitors(curr.get("other_new_competitors", ""))
        prev_comps = parse_competitors(prev.get("other_new_competitors", ""))
        for domain, rank in prev_comps.items():
            if domain not in curr_comps:
                rank_str = f"rank {rank}" if rank > 0 else "rank unknown"
                dropped.append(f"  {domain}: {qid} was {rank_str} → absent")
    if dropped:
        for d in dropped:
            lines.append(d)
    else:
        lines.append("  None")

    # ── TREND SUMMARY ──
    lines.append("\nTREND SUMMARY (all sessions to date)")
    lines.append("-" * 40)
    all_dates = sorted(set(r["session_date"] for r in rows))
    lines.append(f"Sessions: {len(all_dates)} ({', '.join(all_dates)})")
    lines.append("")

    for qid, qtext in all_queries:
        tgl_hist, _ = build_rank_history(rows, qid, "thegeolab_rank")
        lines.append(f"thegeolab {qid} rank history: {tgl_hist} — {trend_label(tgl_hist)}")
    lines.append("")
    for comp_field, comp_label in [("thatware_rank", "ThatWare"), ("hashmeta_rank", "Hashmeta")]:
        for qid, qtext in all_queries:
            hist, _ = build_rank_history(rows, qid, comp_field)
            if any(x > 0 for x in hist):
                lines.append(f"{comp_label} {qid} rank history: {hist} — {trend_label(hist)}")

    # ── SNIPPET COMPARISON ──
    lines.append("\nSNIPPET COMPARISON")
    lines.append("-" * 40)
    sample = rows[0] if rows else {}
    has_snippets = "thegeolab_snippet" in sample and "rank1_snippet" in sample
    if has_snippets:
        any_snippets = any(
            (this_week.get(qid, {}).get("thegeolab_snippet", "").strip() or
             this_week.get(qid, {}).get("rank1_snippet", "").strip())
            for qid, _ in all_queries
        )
        if any_snippets:
            for qid, qtext in all_queries:
                curr = this_week.get(qid, {})
                tgl_snip = curr.get("thegeolab_snippet", "").strip()
                r1_snip = curr.get("rank1_snippet", "").strip()
                r1_domain = curr.get("rank1_domain", "unknown").strip()
                if r1_snip or tgl_snip:
                    lines.append(f"\n{qid}: rank 1 ({r1_domain}) extracted:")
                    lines.append(f'  "{r1_snip}"')
                    lines.append(f"thegeolab.net extracted:")
                    lines.append(f'  "{tgl_snip}"')
        else:
            lines.append("  snippet columns not yet populated — add after Week 3 session")
    else:
        lines.append("  snippet columns not yet in CSV — add after Week 3 session")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="E044 Weekly Delta Report")
    parser.add_argument("--csv", required=True, help="Path to e044_competitor_rank_log.csv")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="Report date (YYYY-MM-DD)")
    args = parser.parse_args()

    report = generate_report(args.csv, args.date)
    print(report)

    os.makedirs(REPORTS_DIR, exist_ok=True)
    out_path = os.path.join(REPORTS_DIR, f"e044_delta_{args.date}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nReport saved to: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
