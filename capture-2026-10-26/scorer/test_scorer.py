"""Tests on SYNTHETIC fixtures only. No capture or pre-check data is used.
Fixture shapes copy the key tree of the real responses (values invented)."""
import json, math, os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scorer as S

A100 = S.ARMS["e100"]["A"]; B100 = S.ARMS["e100"]["B"]
A097 = S.ARMS["e097"]["A"]; B097 = S.ARMS["e097"]["B"]
OTHER = "https://example.org/paywalls"


def gpt_raw(sources, cites, status="completed"):
    return {"status": status, "output": [
        {"type": "reasoning", "summary": [], "content": []},
        {"type": "web_search_call", "status": "completed",
         "action": {"type": "search", "query": "q", "sources": [{"type": "url", "url": u} for u in sources]}},
        {"type": "message", "content": [{"type": "output_text", "text": "answer",
                                          "annotations": [{"type": "url_citation", "url": u, "start_index": 0, "end_index": 1, "title": "t"} for u in cites]}]}]}


def gpt_raw_nosearch():
    return {"status": "completed", "output": [
        {"type": "message", "content": [{"type": "output_text", "text": "from memory", "annotations": []}]}]}


def pplx_raw(results, text, status="completed"):
    return {"status": status, "output": [
        {"type": "search_results", "queries": ["q"],
         "results": [{"id": i, "url": u, "title": "t", "snippet": "s", "source": "web", "last_updated": "2026-10-01"} for i, u in results]},
        {"type": "message", "content": [{"type": "output_text", "text": text, "annotations": []}]}]}


class UrlRule(unittest.TestCase):
    def test_query_string_and_slash(self):
        arms = S.ARMS["e100"]
        self.assertEqual(S.arm_of(A100 + "?utm_source=openai", arms), "A")
        self.assertEqual(S.arm_of(A100.rstrip("/"), arms), "A")
        self.assertEqual(S.arm_of(B100 + "#section", arms), "B")
        self.assertEqual(S.arm_of(B100.rstrip("/") + "?x=1#y", arms), "B")

    def test_scheme_host_as_returned(self):
        arms = S.ARMS["e100"]
        self.assertIsNone(S.arm_of(A100.replace("https://", "http://"), arms))
        self.assertIsNone(S.arm_of(A100.replace("thegeolab.net", "www.thegeolab.net"), arms))
        self.assertIsNone(S.arm_of(A100.replace("thegeolab.net", "TheGeoLab.net"), arms))  # no case folding
        self.assertIsNone(S.arm_of(OTHER, arms))
        self.assertIsNone(S.arm_of(A100 + "extra/", arms))  # different path
        self.assertIsNone(S.arm_of(None, arms))


class ChatGPT(unittest.TestCase):
    arms = S.ARMS["e100"]

    def test_cited_and_surfaced(self):
        r = S.chatgpt_call(gpt_raw([A100, B100 + "?utm_source=openai", OTHER], [A100 + "?utm_source=openai"]), self.arms)
        self.assertTrue(r["browsed_raw"]); self.assertTrue(r["A_cited"]); self.assertFalse(r["B_cited"])
        self.assertTrue(r["A_surfaced"]); self.assertTrue(r["B_surfaced"])
        self.assertEqual(r["A_cited_urls_verbatim"], [A100 + "?utm_source=openai"])

    def test_not_browsed(self):
        r = S.chatgpt_call(gpt_raw_nosearch(), self.arms)
        self.assertFalse(r["browsed_raw"])

    def test_empty_sources_is_not_browsed(self):
        self.assertFalse(S.chatgpt_call(gpt_raw([], []), self.arms)["browsed_raw"])

    def test_citation_type_other_than_url_citation_ignored(self):
        raw = gpt_raw([A100], [])
        raw["output"][2]["content"][0]["annotations"].append({"type": "file_citation", "url": A100})
        self.assertFalse(S.chatgpt_call(raw, self.arms)["A_cited"])


class Perplexity(unittest.TestCase):
    arms = S.ARMS["e097"]

    def test_markers(self):
        raw = pplx_raw([(1, OTHER), (2, A097 + "?ref=x"), (3, B097)], "Text [2] and more [1][9].")
        r = S.perplexity_call(raw, self.arms)
        self.assertTrue(r["A_cited"]); self.assertFalse(r["B_cited"])
        self.assertTrue(r["B_surfaced"]); self.assertEqual(r["invalid_markers"], [9])

    def test_nonconforming_bracket_not_counted(self):
        r = S.perplexity_call(pplx_raw([(1, A097), (2, B097)], "Both [1,2]."), self.arms)
        self.assertFalse(r["A_cited"]); self.assertFalse(r["B_cited"])
        self.assertEqual(r["nonconforming_brackets"], ["[1,2]"])

    def test_both_cited(self):
        r = S.perplexity_call(pplx_raw([(1, A097), (2, B097)], "x[1] y[2]"), self.arms)
        self.assertTrue(r["A_cited"] and r["B_cited"])

    def test_no_results_not_browsed(self):
        r = S.perplexity_call(pplx_raw([], "no search"), self.arms)
        self.assertFalse(r["browsed_raw"])


class Stats(unittest.TestCase):
    def test_wald_known(self):
        d, (lo, hi) = S.diff_ci(40, 20, 80, "wald")
        self.assertAlmostEqual(d, 0.25)
        se = math.sqrt(0.5 * 0.5 / 80 + 0.25 * 0.75 / 80)
        self.assertAlmostEqual(lo, 0.25 - S.Z * se); self.assertAlmostEqual(hi, 0.25 + S.Z * se)

    def test_newcombe_reference(self):
        # Newcombe (1998) example 1: 56/70 vs 48/80 -> 0.2000, CI 0.0524 to 0.3339
        pa, pb = 56 / 70, 48 / 80
        la, ua = S.wilson(56, 70); lb, ub = S.wilson(48, 80)
        lo = (pa - pb) - math.sqrt((pa - la) ** 2 + (ub - pb) ** 2)
        hi = (pa - pb) + math.sqrt((ua - pa) ** 2 + (pb - lb) ** 2)
        self.assertAlmostEqual(lo, 0.0524, places=3); self.assertAlmostEqual(hi, 0.3339, places=3)

    def test_floor(self):
        self.assertEqual(S.floor_check(18, 80)["floor"], 18); self.assertTrue(S.floor_check(18, 80)["met"])
        self.assertFalse(S.floor_check(17, 80)["met"])
        self.assertEqual(S.floor_check(0, 81)["floor"], 18)

    def test_null_rule(self):
        t = S.ab_test(30, 20, 80, "wald")
        self.assertTrue(t["null_literal_reading"])  # 12.5 points < 22


class PairedNewcombe(unittest.TestCase):
    """Synthetic only. First two cases are the co-author's own check values (29 Oct 2026)."""
    def pts(self, cells):
        d, (lo, hi) = S.newcombe_paired(*cells)
        return round(d * 100, 1), round(lo * 100, 1), round(hi * 100, 1)

    def test_coauthor_example_1(self):
        self.assertEqual(self.pts((4, 30, 6, 40)), (30.0, 16.2, 42.4))

    def test_coauthor_example_2(self):
        self.assertEqual(self.pts((10, 20, 5, 45)), (18.8, 6.7, 30.2))

    def test_swap_arms_negates_interval(self):
        d, (lo, hi) = S.newcombe_paired(10, 20, 5, 45)
        d2, (lo2, hi2) = S.newcombe_paired(10, 5, 20, 45)
        self.assertAlmostEqual(d2, -d); self.assertAlmostEqual(lo2, -hi); self.assertAlmostEqual(hi2, -lo)

    def test_phi_zero_equals_independent(self):
        # a=b=c=d: ad - bc = 0 so phi = 0 and the paired formula reduces to the independent one
        n = 20
        d, (lo, hi) = S.newcombe_paired(5, 5, 5, 5)
        d2, (lo2, hi2) = S.diff_ci(10, 10, n, "newcombe_independent")
        self.assertAlmostEqual(lo, lo2); self.assertAlmostEqual(hi, hi2)

    def test_zero_denominator_phi_zero(self):
        d, (lo, hi) = S.newcombe_paired(0, 0, 0, 80)       # nobody cited
        self.assertEqual(d, 0.0); self.assertLess(lo, 0.0); self.assertGreater(hi, 0.0)
        d, (lo, hi) = S.newcombe_paired(80, 0, 0, 0)       # everybody cited both
        self.assertEqual(d, 0.0)

    def test_symmetric_when_b_equals_c(self):
        d, (lo, hi) = S.newcombe_paired(10, 7, 7, 56)
        self.assertAlmostEqual(d, 0.0); self.assertAlmostEqual(lo, -hi)

    def test_positive_correlation_narrows_vs_independent(self):
        d, (lo, hi) = S.newcombe_paired(40, 5, 5, 30)
        d2, (lo2, hi2) = S.diff_ci(45, 45, 80, "newcombe_independent")
        self.assertLess(hi - lo, hi2 - lo2)

    def test_n_zero_is_nan(self):
        d, (lo, hi) = S.newcombe_paired(0, 0, 0, 0)
        self.assertTrue(math.isnan(d) and math.isnan(lo) and math.isnan(hi))

    def test_needs_consistent_cells(self):
        with self.assertRaises(ValueError): S.diff_ci(34, 10, 80, "newcombe_paired")
        with self.assertRaises(ValueError): S.diff_ci(34, 10, 80, "newcombe_paired", cells=(4, 30, 6, 41))
        with self.assertRaises(ValueError): S.diff_ci(34, 10, 80, "newcombe_paired", cells=(5, 30, 6, 39))
        self.assertEqual(S.diff_ci(34, 10, 80, "newcombe_paired", cells=(4, 30, 6, 40))[0], 0.3)

    def test_paired_cells_helper(self):
        self.assertEqual(S.paired_cells([(1, 1), (1, 0), (0, 1), (0, 0), (0, 0)]), (1, 1, 1, 2))

    def test_old_name_rejected(self):
        with self.assertRaises(SystemExit):
            S.main(["--experiment", "e100", "--raw", "x", "--ci", "newcombe", "--out", "y"])

    def test_unchanged_wald_and_independent(self):
        d, (lo, hi) = S.diff_ci(40, 20, 80, "wald")
        self.assertAlmostEqual(d, 0.25)
        d, (lo, hi) = S.diff_ci(56, 48, 70, "newcombe_independent")  # smoke: same code path as before the rename
        self.assertAlmostEqual(d, 56 / 70 - 48 / 70)


def row(a_c, b_c, a_s=None, b_s=None):
    return {"A_cited": a_c, "B_cited": b_c, "A_surfaced": a_c if a_s is None else a_s, "B_surfaced": b_c if b_s is None else b_s}


class E097Branches(unittest.TestCase):
    def test_neither_heavy(self):
        rows = [row(False, False)] * 70 + [row(True, False)] * 10
        self.assertTrue(S.e097_branch(rows, "wald")["reading"].startswith("neither-heavy"))

    def test_branch1(self):
        rows = [row(True, True)] * 10 + [row(True, False)] * 20 + [row(False, True)] * 10 + [row(False, False)] * 40
        self.assertTrue(S.e097_branch(rows, "wald")["reading"].startswith("Branch 1"))

    def test_branch2(self):
        rows = [row(True, True)] * 1 + [row(True, False)] * 25 + [row(False, True)] * 2 + [row(False, False)] * 52
        out = S.e097_branch(rows, "wald")
        self.assertEqual(out["reading"], "Branch 2 (consolidation): engine keeps arm A")

    def test_branch2_guard(self):
        rows = ([row(True, False, True, True)] * 25 + [row(True, True)] * 1 + [row(False, True)] * 2 + [row(False, False)] * 52)
        self.assertTrue(S.e097_branch(rows, "wald")["reading"].startswith("both seen, one preferred"))

    def test_neither_branch(self):
        rows = [row(True, True)] * 1 + [row(True, False)] * 12 + [row(False, True)] * 10 + [row(False, False)] * 57
        self.assertTrue(S.e097_branch(rows, "wald")["reading"].startswith("neither branch"))


class EndToEnd(unittest.TestCase):
    def _write(self, rows):
        d = tempfile.mkdtemp(); p = os.path.join(d, "raw_calls.jsonl")
        with open(p, "w") as f:
            for r in rows: f.write(json.dumps(r) + "\n")
        return d, p

    def test_e100_drops_unbrowsed_and_incomplete(self):
        rows = [{"call_id": f"c{i}", "engine": "chatgpt", "query_index": "q1", "browsed": True, "error": None,
                 "raw": gpt_raw([A100, B100], [A100] if i % 2 else [])} for i in range(6)]
        rows.append({"call_id": "nb", "engine": "chatgpt", "query_index": "q2", "browsed": False, "error": None, "raw": gpt_raw_nosearch()})
        rows.append({"call_id": "inc", "engine": "chatgpt", "query_index": "q2", "browsed": True, "error": None, "raw": gpt_raw([A100], [A100], status="incomplete")})
        d, p = self._write(rows)
        out = os.path.join(d, "out")
        S.main(["--experiment", "e100", "--raw", p, "--ci", "wald", "--out", out])
        s = json.load(open(os.path.join(out, "e100_summary.json")))
        self.assertEqual(s["chatgpt"]["observations"], 6)
        self.assertEqual(s["chatgpt"]["all"]["primary_cited"]["A"], 3)
        self.assertEqual(s["chatgpt"]["browse_flag_agreement_with_harness"], "8/8")

    def test_e097_chatgpt_sensitivity_first_80(self):
        rows = [{"call_id": f"c{i}", "engine": "chatgpt", "query_index": "q1", "browsed": True, "error": None,
                 "raw": gpt_raw([A097], [A097])} for i in range(81)]
        d, p = self._write(rows)
        out = os.path.join(d, "out")
        S.main(["--experiment", "e097", "--raw", p, "--ci", "newcombe_paired", "--out", out])
        s = json.load(open(os.path.join(out, "e097_summary.json")))
        self.assertEqual(s["chatgpt"]["primary_all"]["n"], 81)
        self.assertEqual(s["chatgpt"]["sensitivity_first_80"]["n"], 80)

    def test_e097_per_query_cited_table(self):
        rows = []
        for i in range(10):
            qi = "q1" if i < 6 else "q2"
            a = i % 2 == 0; b = i % 3 == 0
            rows.append({"call_id": f"c{i}", "engine": "chatgpt", "query_index": qi, "browsed": True, "error": None,
                         "raw": gpt_raw([A097, B097], [u for u, f in ((A097, a), (B097, b)) if f])})
        d, p = self._write(rows)
        out = os.path.join(d, "out")
        S.main(["--experiment", "e097", "--raw", p, "--ci", "newcombe_paired", "--out", out])
        with open(os.path.join(out, "e097_summary.json")) as f:
            s = json.load(f)
        pq = s["chatgpt"]["primary_all"]["per_query_cited"]
        self.assertEqual(sorted(pq), ["q1", "q2"])
        self.assertEqual(sum(v["n"] for v in pq.values()), 10)
        self.assertEqual(sum(v["both"] + v["A_only"] + v["B_only"] + v["neither"] for v in pq.values()), 10)
        self.assertEqual(pq["q1"], {"n": 6, "both": 1, "A_only": 2, "B_only": 1, "neither": 2})

    def test_ci_required(self):
        with self.assertRaises(SystemExit):
            S.main(["--experiment", "e100", "--raw", "x", "--out", "y"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
