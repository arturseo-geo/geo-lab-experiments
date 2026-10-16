#!/usr/bin/env python3
"""
E100 shared-body md5 verification.

Reproduces the canonical body md5 for posts 2213 (arm A, clean) and 2214
(arm B, clutter).  Read-only — no writes, no page modifications.

Database access: ssh + wp-cli `wp db query` on the VPS (same method used
for the pre-tag integrity checks).  No credentials stored; wp-cli reads
wp-config.php on the server.

Run:  python3 -I e100/verify/shared_body_md5.py
"""

import hashlib
import os
import shlex
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SSH_CMD = ["ssh", "-p", "2222", "-i", os.path.expanduser("~/.ssh/claude_vps"),
           "root@45.55.91.146"]

# --- expected values ---
ARM_A_ID, ARM_B_ID = 2213, 2214
BODY_MARKER = "<p>AI search engines can only cite"
EXPECTED_BODY_MD5_DB   = "1be194c58fb711f01a1eabc91d9920af"
EXPECTED_BODY_BYTES_DB = 5856
EXPECTED_BODY_MD5_FILE = "a85274885b18741417d647b569d62fa5"
EXPECTED_FULL_MD5_A    = "c397e1b02f90e27b8d9d44217842373a"
EXPECTED_FULL_MD5_B    = "5b9713919af7d157c040dcb07b1eb025"

EXPORT_A = os.path.join(REPO_ROOT, "e100", "page-source-arm-a-clean.html")
EXPORT_B = os.path.join(REPO_ROOT, "e100", "page-source-arm-b-clutter.html")

ok = True


def check(label, observed, expected):
    global ok
    match = observed == expected
    tag = "MATCH" if match else "MISMATCH"
    print(f"  {tag}: {label}")
    print(f"    observed: {observed}")
    print(f"    expected: {expected}")
    if not match:
        ok = False


def wp_query(sql):
    """Run a read-only SQL query via ssh + wp-cli and return stdout."""
    remote_cmd = "wp db query {} --path=/var/www/thegeolab --allow-root".format(
        shlex.quote(sql)
    )
    result = subprocess.run(
        SSH_CMD + [remote_cmd],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        print(f"ERROR: wp db query failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(2)
    return result.stdout


# ── Method 1: live database, shared body from marker ──────────────────

print("=" * 70)
print("Method 1 — live database: body from first occurrence of marker")
print("=" * 70)

sql = (
    "SELECT ID, "
    f"MD5(SUBSTRING(post_content FROM LOCATE('{BODY_MARKER}', post_content))), "
    f"LENGTH(SUBSTRING(post_content FROM LOCATE('{BODY_MARKER}', post_content))) "
    f"FROM geo_posts WHERE ID IN ({ARM_A_ID},{ARM_B_ID}) ORDER BY ID"
)
rows = wp_query(sql).strip().split("\n")[1:]  # skip header

for row in rows:
    parts = row.split("\t")
    pid, md5_val, length = int(parts[0]), parts[1], int(parts[2])
    label = "arm A" if pid == ARM_A_ID else "arm B"
    print(f"\nPost {pid} ({label}):")
    check(f"body md5 (from marker)", md5_val, EXPECTED_BODY_MD5_DB)
    check(f"body length", length, EXPECTED_BODY_BYTES_DB)

# confirm identical across arms
if rows[0].split("\t")[1] == rows[1].split("\t")[1]:
    print("\n  Arms A and B: body from marker is IDENTICAL (md5 match)")
else:
    print("\n  MISMATCH: arms A and B differ in body from marker")
    ok = False


# ── Method 2: committed export files, same span ──────────────────────

print()
print("=" * 70)
print("Method 2 — committed export files: body from first occurrence of marker")
print("=" * 70)

marker_bytes = BODY_MARKER.encode("utf-8")
spans = {}

for path, label in [(EXPORT_A, "arm A"), (EXPORT_B, "arm B")]:
    data = open(path, "rb").read()
    idx = data.find(marker_bytes)
    if idx == -1:
        print(f"  ERROR: marker not found in {path}")
        sys.exit(2)
    span = data[idx:]
    md5_val = hashlib.md5(span).hexdigest()
    spans[label] = span
    print(f"\nExport {label} ({os.path.basename(path)}):")
    print(f"  marker offset: {idx}")
    print(f"  span length:   {len(span)}")
    check(f"export body md5 (from marker)", md5_val, EXPECTED_BODY_MD5_FILE)

byte_diff = len(spans["arm A"]) - EXPECTED_BODY_BYTES_DB
print(f"\nByte difference (export span - DB span): {byte_diff}")
if byte_diff == 1:
    # Confirm trailing newline
    if spans["arm A"][-1:] == b"\n" and spans["arm A"][:-1] == spans["arm B"][:-1]:
        print("  Confirmed: exactly one trailing newline in export vs DB column")
    else:
        print("  WARNING: 1-byte difference but not a trailing newline")
        ok = False
else:
    print(f"  MISMATCH: expected 1-byte trailing-newline difference, got {byte_diff}")
    ok = False

if spans["arm A"] == spans["arm B"]:
    print("  Export spans arm A and arm B: IDENTICAL")
else:
    print("  MISMATCH: export spans differ between arms")
    ok = False


# ── Full post_content md5 per arm ────────────────────────────────────

print()
print("=" * 70)
print("Full post_content md5 per arm")
print("=" * 70)

sql_full = (
    f"SELECT ID, MD5(post_content) FROM geo_posts "
    f"WHERE ID IN ({ARM_A_ID},{ARM_B_ID}) ORDER BY ID"
)
rows_full = wp_query(sql_full).strip().split("\n")[1:]

for row in rows_full:
    parts = row.split("\t")
    pid, md5_val = int(parts[0]), parts[1]
    expected = EXPECTED_FULL_MD5_A if pid == ARM_A_ID else EXPECTED_FULL_MD5_B
    label = "arm A" if pid == ARM_A_ID else "arm B"
    print(f"\nPost {pid} ({label}):")
    check(f"full post_content md5", md5_val, expected)


# ── result ────────────────────────────────────────────────────────────

print()
if ok:
    print("ALL CHECKS PASSED")
    sys.exit(0)
else:
    print("SOME CHECKS FAILED")
    sys.exit(1)
