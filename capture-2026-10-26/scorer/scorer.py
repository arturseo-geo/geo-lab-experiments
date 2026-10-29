#!/usr/bin/env python3
"""Independent scorer for E100 v1.5 and E097 v1.4 (The GEO Lab / LeapOne).

Written from the registered texts only (E100 v1.5 sections 2.1, 2.3, 2.4, 2.6, 4;
E097 v1.4 sections 2.1 to 2.4 and 3) and the handoff README. It reads ONLY the
"raw" API response of each row in raw_calls.jsonl, plus the row's call_id,
engine, query_index and the harness browse flag (the flag is used only to report
agreement with the browse state re-derived from raw). It never reads the
harness's extracted fields (cited_urls, surfaced_urls, text, invalid_markers).

Usage:
  python3 -I scorer.py --experiment e100 --raw PATH/raw_calls.jsonl --ci newcombe_paired --out OUTDIR
  python3 -I scorer.py --experiment e097 --raw PATH/raw_calls.jsonl --ci newcombe_paired --out OUTDIR
The CI method has no default on purpose: the registered texts say
"95% two-proportion confidence interval" without naming a method, so it must be
chosen explicitly and recorded before the run.
Choices: wald, newcombe_independent (Newcombe 1998a hybrid score, independent
samples), newcombe_paired (Newcombe 1998b, Stat Med 17:2635-2650, paired data,
as specified by the co-author on 29 Oct 2026). The earlier choice "newcombe"
was the independent-samples formula under an ambiguous name; it was removed.
"""
import argparse, csv, json, math, os, re, sys
from urllib.parse import urlsplit

# Arm addresses, verbatim from the registered texts.
ARMS = {
    # E100 v1.5 section 2.3
    "e100": {"A": "https://thegeolab.net/guides/paywalls-and-ai-search-a/",
             "B": "https://thegeolab.net/guides/paywalls-and-ai-search-b/"},
    # E097 v1.4 section 1 lists the pair as descriptive vs opaque slug, in this order.
    # The v1.4 text does not label them A and B explicitly next to the URLs: confirm
    # against the freeze manifest before the run (see AMBIGUITIES in the summary).
    "e097": {"A": "https://thegeolab.net/guides/hreflang-and-ai-search-explained/",
             "B": "https://thegeolab.net/guides/p48213/"},
}
FLOOR_SHARE = 0.22      # citation floor and detectable difference
BRANCH1_BOTH = 0.15     # E097 Branch 1 threshold
BRANCH2_DOM = 0.80      # E097 Branch 2 threshold
GUARD_BOTH_SURF = 0.15  # E097 surfaced both-together guard
Z = 1.959963984540054   # 95% two-sided

MARKER_RE = re.compile(r"\[(\d+)\]")                 # registered form: one source per bracket
NONCONFORM_RE = re.compile(r"\[(\d+(?:\s*[,\-–]\s*\d+)+)\]")  # e.g. [1,2] or [1-3]: logged, not counted


def norm(url):
    """Registered URL matching rule: drop query string and fragment, normalise a
    trailing slash on the path. Scheme and host compared as returned. Nothing else."""
    if not isinstance(url, str):
        return None
    p = urlsplit(url)
    path = p.path.rstrip("/")
    return (p.scheme, p.netloc, path)


def arm_of(url, arms):
    n = norm(url)
    if n is None:
        return None
    for label, addr in arms.items():
        if n == norm(addr):
            return label
    return None


def items(raw, typ):
    return [o for o in (raw.get("output") or []) if isinstance(o, dict) and o.get("type") == typ]


def chatgpt_call(raw, arms):
    """Return dict with browsed_raw, cited/surfaced per arm, matched URLs."""
    sources = []
    for ws in items(raw, "web_search_call"):
        act = ws.get("action") or {}
        for s in act.get("sources") or []:
            if isinstance(s, dict) and isinstance(s.get("url"), str):
                sources.append(s["url"])
    cites = []
    for msg in items(raw, "message"):
        for c in msg.get("content") or []:
            if isinstance(c, dict) and c.get("type") == "output_text":
                for a in c.get("annotations") or []:
                    if isinstance(a, dict) and a.get("type") == "url_citation" and isinstance(a.get("url"), str):
                        cites.append(a["url"])
    # A browsed call returned a search-results list (E100 2.1 and 2.6).
    browsed_raw = len(sources) > 0
    return score_lists(cites, sources, arms, browsed_raw, invalid=[], nonconform=[])


def perplexity_call(raw, arms):
    results = []
    for sr in items(raw, "search_results"):
        for r in sr.get("results") or []:
            if isinstance(r, dict):
                results.append(r)
    texts = []
    for msg in items(raw, "message"):
        for c in msg.get("content") or []:
            if isinstance(c, dict) and c.get("type") == "output_text" and isinstance(c.get("text"), str):
                texts.append(c["text"])
    text = "\n".join(texts)
    by_id = {}
    dup_ids = set()
    for r in results:
        rid = r.get("id")
        if rid in by_id:
            dup_ids.add(rid)
        by_id.setdefault(rid, r)
    cites, invalid = [], []
    for m in MARKER_RE.finditer(text):
        n = int(m.group(1))
        r = by_id.get(n)
        if r is None or not isinstance(r.get("url"), str):
            invalid.append(n)   # a marker that points to no result is logged, not counted
        else:
            cites.append(r["url"])
    nonconform = [m.group(0) for m in NONCONFORM_RE.finditer(text)]
    sources = [r["url"] for r in results if isinstance(r.get("url"), str)]
    browsed_raw = len(results) > 0  # no search-results list = did not browse (E097 2.3)
    out = score_lists(cites, sources, arms, browsed_raw, invalid=invalid, nonconform=nonconform)
    out["duplicate_result_ids"] = sorted(dup_ids)
    return out


def score_lists(cites, sources, arms, browsed_raw, invalid, nonconform):
    out = {"browsed_raw": browsed_raw, "invalid_markers": invalid, "nonconforming_brackets": nonconform}
    for label in arms:
        mc = [u for u in cites if arm_of(u, arms) == label]
        ms = [u for u in sources if arm_of(u, arms) == label]
        out[f"{label}_cited"] = bool(mc)
        out[f"{label}_surfaced"] = bool(ms)
        out[f"{label}_cited_urls_verbatim"] = mc
        out[f"{label}_surfaced_urls_verbatim"] = ms
    return out


# ---------- statistics ----------

def wilson(x, n):
    if n == 0:
        return (float("nan"), float("nan"))
    p = x / n
    d = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / d
    h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return (c - h, c + h)


def newcombe_paired(a, b, c, d):
    """Newcombe hybrid score interval for the difference of two paired
    proportions, as written out by the co-author (29 Oct 2026). Cells:
    a = both, b = A only, c = B only, d = neither; n = a+b+c+d.
    pA = (a+b)/n, pB = (a+c)/n. Wilson 95% intervals, no continuity correction
    on the Wilson intervals. phi = (ad-bc)/sqrt((a+b)(c+d)(a+c)(b+d)); if ad > bc
    the numerator is max(ad-bc-n/2, 0); phi = 0 if the denominator is 0.
    Returns (D, (lower, upper)) with D = pA - pB."""
    n = a + b + c + d
    if n == 0:
        nan = float("nan")
        return nan, (nan, nan)
    pa, pb = (a + b) / n, (a + c) / n
    dd = pa - pb
    la, ua = wilson(a + b, n)
    lb, ub = wilson(a + c, n)
    den = math.sqrt((a + b) * (c + d) * (a + c) * (b + d))
    if den == 0:
        phi = 0.0
    else:
        num = a * d - b * c
        if a * d > b * c:
            num = max(num - n / 2, 0.0)
        phi = num / den
    lo = dd - math.sqrt((pa - la) ** 2 - 2 * phi * (pa - la) * (ub - pb) + (ub - pb) ** 2)
    hi = dd + math.sqrt((ua - pa) ** 2 - 2 * phi * (ua - pa) * (pb - lb) + (pb - lb) ** 2)
    return dd, (lo, hi)


def diff_ci(xa, xb, n, method, cells=None):
    """95% CI for pA - pB. wald and newcombe_independent use independent-samples
    formulas with nA = nB = n. newcombe_paired needs the four paired cells
    (both, A only, B only, neither) and refuses to run without them."""
    pa, pb = xa / n, xb / n
    d = pa - pb
    if method == "wald":
        se = math.sqrt(pa * (1 - pa) / n + pb * (1 - pb) / n)
        return d, (d - Z * se, d + Z * se)
    if method == "newcombe_independent":  # Newcombe (1998a) hybrid score, independent samples
        la, ua = wilson(xa, n)
        lb, ub = wilson(xb, n)
        lo = d - math.sqrt((pa - la) ** 2 + (ub - pb) ** 2)
        hi = d + math.sqrt((ua - pa) ** 2 + (pb - lb) ** 2)
        return d, (lo, hi)
    if method == "newcombe_paired":
        if cells is None:
            raise ValueError("newcombe_paired needs the paired cells (both, A only, B only, neither)")
        a, b, c, dd = cells
        if min(cells) < 0 or a + b != xa or a + c != xb or a + b + c + dd != n:
            raise ValueError(f"paired cells {cells} inconsistent with xa={xa}, xb={xb}, n={n}")
        return newcombe_paired(a, b, c, dd)
    raise ValueError("ci method must be wald, newcombe_independent or newcombe_paired")


def paired_cells(pairs):
    """pairs: iterable of (A_flag, B_flag). Returns (both, A_only, B_only, neither)."""
    a = b = c = d = 0
    for x, y in pairs:
        if x and y: a += 1
        elif x: b += 1
        elif y: c += 1
        else: d += 1
    return (a, b, c, d)


def ab_test(xa, xb, n, method, cells=None):
    d, (lo, hi) = diff_ci(xa, xb, n, method, cells)
    includes_zero = lo <= 0 <= hi
    return {
        "n": n, "A": xa, "B": xb, "rate_A": xa / n, "rate_B": xb / n,
        "paired_cells_both_Aonly_Bonly_neither": list(cells) if cells is not None else None,
        "diff_A_minus_B": d, "ci95": [lo, hi], "ci_method": method,
        "ci_includes_zero": includes_zero,
        "point_below_22_signed": d < FLOOR_SHARE,       # literal reading: A minus B below 22 points
        "abs_point_below_22": abs(d) < FLOOR_SHARE,     # alternative reading, reported, not chosen
        "null_literal_reading": includes_zero or d < FLOOR_SHARE,
    }


def floor_check(either_cited, n):
    need = math.ceil(FLOOR_SHARE * n)
    return {"either_cited": either_cited, "floor": need, "met": either_cited >= need}


def four_way(rows, kind):
    c = {"both": 0, "A_only": 0, "B_only": 0, "neither": 0}
    for r in rows:
        a, b = r[f"A_{kind}"], r[f"B_{kind}"]
        c["both" if a and b else "A_only" if a else "B_only" if b else "neither"] += 1
    return c


def e097_branch(rows, method):
    n = len(rows)
    cited = four_way(rows, "cited")
    surf = four_way(rows, "surfaced")
    either = cited["both"] + cited["A_only"] + cited["B_only"]
    fl = floor_check(either, n)
    single = cited["A_only"] + cited["B_only"]
    both_share = cited["both"] / either if either else None
    dom_arm = "A" if cited["A_only"] >= cited["B_only"] else "B"
    dom_share = max(cited["A_only"], cited["B_only"]) / single if single else None
    s_either = surf["both"] + surf["A_only"] + surf["B_only"]
    s_both_share = surf["both"] / s_either if s_either else None
    s_single = surf["A_only"] + surf["B_only"]
    out = {"n": n, "cited_four_way": cited, "surfaced_four_way": surf, "floor": fl,
           "both_cited_share_of_either": both_share,
           "single_arm_calls": single, "dominant_arm": dom_arm if single else None,
           "dominant_share_of_single": dom_share,
           "surfaced_both_together_share_of_either": s_both_share,
           "surfaced_measures": {
               "both_share_of_either": s_both_share,
               "dominant_share_of_single": (max(surf["A_only"], surf["B_only"]) / s_single) if s_single else None}}
    if not fl["met"]:
        out["reading"] = "neither-heavy (floor not met): non-competitive, no slug or dedup conclusion; surfaced table reported as retrieval"
        return out
    if both_share >= BRANCH1_BOTH:
        t = ab_test(cited["both"] + cited["A_only"], cited["both"] + cited["B_only"], n, method,
                    cells=(cited["both"], cited["A_only"], cited["B_only"], cited["neither"]))
        out["branch1_test"] = t
        out["reading"] = "Branch 1 (pages treated as distinct): slug test as registered"
        out["escalation_condition_A_leads_by_22"] = t["diff_A_minus_B"] >= FLOOR_SHARE
        return out
    if dom_share is not None and dom_share >= BRANCH2_DOM:
        if s_both_share is not None and s_both_share >= GUARD_BOTH_SURF:
            out["reading"] = "both seen, one preferred (surfaced guard triggered): no dedup claim"
        else:
            out["reading"] = f"Branch 2 (consolidation): engine keeps arm {dom_arm}"
        return out
    out["reading"] = "neither branch: four counts reported, nothing interpreted"
    return out


# ---------- driver ----------

def load_rows(path, experiment):
    arms = ARMS[experiment]
    rows = []
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            d = json.loads(line)
            raw = d.get("raw") or {}
            eng = d.get("engine")
            if eng == "chatgpt":
                s = chatgpt_call(raw, arms)
            elif eng == "perplexity":
                s = perplexity_call(raw, arms)
            else:
                raise ValueError(f"line {line_no}: unknown engine {eng!r}")
            status = raw.get("status")
            s.update({"line": line_no, "call_id": d.get("call_id"), "engine": eng,
                      "query_index": d.get("query_index"), "status_raw": status,
                      "browsed_flag_harness": d.get("browsed"),
                      "error_row": d.get("error") not in (None, "", False)})
            # Failed calls are not observations (incomplete status, API errors).
            s["observation"] = bool(s["browsed_raw"]) and status == "completed" and not s["error_row"]
            rows.append(s)
    return rows


def summarise(rows, experiment, method):
    summ = {"experiment": experiment, "ci_method": method, "arms": ARMS[experiment],
            "rules": "registered texts E100 v1.5 / E097 v1.4; raw responses only",
            "AMBIGUITIES": [
                "CI method is not named in the registered texts; chosen at run time: " + method,
                "LIMITATION: the interval treats calls as independent; calls cluster within 8 queries, so the per-query table (E100) is the check on that. Not corrected for clustering.",
                "E100 section 4 null rule: 'point estimate below 22 points' read literally on A minus B; the absolute-value reading is also reported",
                "E097 v1.4 does not label hreflang-and-ai-search-explained as A and p48213 as B next to the URLs; mapping taken from the order in section 1, to be confirmed",
                "Perplexity brackets not of the form [n] (e.g. [1,2]) are logged as nonconforming and not counted",
            ]}
    by_engine = {}
    for r in rows:
        by_engine.setdefault(r["engine"], []).append(r)
    for eng, rs in by_engine.items():
        obs = [r for r in rs if r["observation"]]
        agree = sum(1 for r in rs if bool(r["browsed_raw"]) == bool(str(r["browsed_flag_harness"]).lower() in ("true", "1")))
        e = {"calls": len(rs), "observations": len(obs),
             "browse_flag_agreement_with_harness": f"{agree}/{len(rs)}",
             "invalid_markers_total": sum(len(r["invalid_markers"]) for r in rs),
             "nonconforming_brackets_total": sum(len(r["nonconforming_brackets"]) for r in rs)}
        sets = {"all": obs}
        if experiment == "e097" and eng == "chatgpt":
            sets = {"primary_all": obs, "sensitivity_first_80": obs[:80]}
        for name, sub in sets.items():
            if experiment == "e100":
                n = len(sub)
                xa = sum(r["A_cited"] for r in sub); xb = sum(r["B_cited"] for r in sub)
                either = sum(1 for r in sub if r["A_cited"] or r["B_cited"])
                sa = sum(1 for r in sub if r["A_surfaced"] and not r["A_cited"])
                sb = sum(1 for r in sub if r["B_surfaced"] and not r["B_cited"])
                res = {"floor": floor_check(either, n)}
                cc = paired_cells((r["A_cited"], r["B_cited"]) for r in sub)
                res["primary_cited"] = ab_test(xa, xb, n, method, cells=cc) if n else None
                res["primary_reading"] = ("uninformative (floor not met): no difference claimed; surfaced reported as its own finding"
                                          if not res["floor"]["met"] else
                                          ("null" if res["primary_cited"]["null_literal_reading"] else "difference"))
                sc = paired_cells((r["A_surfaced"] and not r["A_cited"], r["B_surfaced"] and not r["B_cited"]) for r in sub)
                res["secondary_surfaced_not_cited"] = ab_test(sa, sb, n, method, cells=sc) if n else None
                pq = {}
                for r in sub:
                    q = pq.setdefault(r["query_index"], {"n": 0, "A_cited": 0, "B_cited": 0, "A_surf_not_cited": 0, "B_surf_not_cited": 0})
                    q["n"] += 1; q["A_cited"] += r["A_cited"]; q["B_cited"] += r["B_cited"]
                    q["A_surf_not_cited"] += r["A_surfaced"] and not r["A_cited"]
                    q["B_surf_not_cited"] += r["B_surfaced"] and not r["B_cited"]
                res["per_query"] = dict(sorted(pq.items(), key=lambda kv: str(kv[0])))
                e[name] = res
            else:
                e[name] = e097_branch(sub, method) if sub else None
        summ[eng] = e
    return summ


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--experiment", required=True, choices=["e100", "e097"])
    ap.add_argument("--raw", required=True)
    ap.add_argument("--ci", required=True, choices=["wald", "newcombe_independent", "newcombe_paired"])
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    rows = load_rows(a.raw, a.experiment)
    os.makedirs(a.out, exist_ok=True)
    cols = ["line", "call_id", "engine", "query_index", "status_raw", "error_row", "browsed_flag_harness",
            "browsed_raw", "observation", "A_cited", "B_cited", "A_surfaced", "B_surfaced",
            "A_cited_urls_verbatim", "B_cited_urls_verbatim", "A_surfaced_urls_verbatim", "B_surfaced_urls_verbatim",
            "invalid_markers", "nonconforming_brackets"]
    with open(os.path.join(a.out, f"{a.experiment}_per_call.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow([json.dumps(r.get(c)) if isinstance(r.get(c), list) else r.get(c) for c in cols])
    with open(os.path.join(a.out, f"{a.experiment}_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summarise(rows, a.experiment, a.ci), f, indent=2, sort_keys=True)
    print("wrote", a.out)


if __name__ == "__main__":
    sys.exit(main())
