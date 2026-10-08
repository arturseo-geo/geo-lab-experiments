#!/usr/bin/env python3
"""Recompute revisit medians from revisit_20260916.json — ENTIA Phase 2 evidence check.
Method: continuous quantile (numpy percentile with interpolation='linear') on
gap values converted to hours, excluding gaps < 60 s (already excluded by the
file's min_gap_s=60 constraint — all gaps in the array are ≥ 60 s)."""

import json
import hashlib
import os
import numpy as np

FILE = "/home/ajdev/fernando-deposit-16sep/revisit_20260916.json"

# Step 1: Verify file integrity
size = os.path.getsize(FILE)
with open(FILE, "rb") as f:
    sha = hashlib.sha256(f.read()).hexdigest()

EXPECTED_SHA = "5d461dbb50b2143fc8bc3b0fa184ba9c5d13212f82e99c9ab0b0283b91368b37"
EXPECTED_SIZE = 1275302

print(f"File: {FILE}")
print(f"Size: {size} (expected {EXPECTED_SIZE}) — {'MATCH' if size == EXPECTED_SIZE else 'NO MATCH'}")
print(f"SHA256: {sha}")
print(f"Expected: {EXPECTED_SHA}")
print(f"Hash: {'MATCH' if sha == EXPECTED_SHA else 'NO MATCH — STOPPING'}")
if sha != EXPECTED_SHA:
    raise SystemExit("Hash mismatch. Aborting.")

# Step 2: Load and parse
with open(FILE) as f:
    d = json.load(f)

print(f"\n=== Metadata ===")
print(f"computed_at: {d['computed_at']}")
print(f"window from: {d['window']['from']}")
print(f"window to: {d['window']['to']}")
print(f"window days: {d['window']['days']}")
print(f"mode: {d['window']['mode']}")
print(f"frozen_to: {d['window']['frozen_to']}")
print(f"complete: {d['complete']}")
print(f"min_gap_s: {d['min_gap_s']}")
print(f"unit: {d['unit']}")
print(f"families_total: {d['families_total']}")

total_intervals = sum(len(fam['gaps']) for fam in d['families'])
print(f"total intervals (sum of all gaps arrays): {total_intervals}")

# Step 3: Recompute for the three target families
TARGETS = {
    "ChatGPT-User": {"expected_n": 51, "expected_p50": 60.19},
    "OpenAI-SearchBot": {"expected_n": 78, "expected_p50": 144.00},
    "Googlebot": {"expected_n": 6892, "expected_p50": 48.96},
}

print(f"\n=== Recomputed Medians (continuous quantile, gaps in hours) ===")
print(f"{'Family':<20} {'n':>6} {'p10 (h)':>10} {'p50 (h)':>10} {'p90 (h)':>10} {'n match':>8} {'p50 match':>10}")
print("-" * 80)

for fam in d['families']:
    name = fam['family']
    if name not in TARGETS:
        continue

    gaps_s = np.array(fam['gaps'], dtype=float)
    # Exclude gaps < 60 s (should already be excluded, but defensive)
    gaps_s = gaps_s[gaps_s >= 60]
    gaps_h = gaps_s / 3600.0

    n = len(gaps_h)
    p10 = float(np.percentile(gaps_h, 10, interpolation='linear'))
    p50 = float(np.percentile(gaps_h, 50, interpolation='linear'))
    p90 = float(np.percentile(gaps_h, 90, interpolation='linear'))

    exp = TARGETS[name]
    n_match = "MATCH" if n == exp["expected_n"] else f"NO MATCH (exp {exp['expected_n']})"
    p50_match = "MATCH" if abs(p50 - exp["expected_p50"]) < 0.005 else f"NO MATCH (exp {exp['expected_p50']:.2f}, got {p50:.2f}, diff {p50 - exp['expected_p50']:+.4f})"

    print(f"{name:<20} {n:>6} {p10:>10.2f} {p50:>10.2f} {p90:>10.2f} {n_match:>8} {p50_match}")
