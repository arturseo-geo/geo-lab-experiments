#!/usr/bin/env python3
"""
E097 body md5 verification.

Reproduces the canonical body md5 for posts 2211 (arm A, descriptive slug)
and 2212 (arm B, opaque slug).  Read-only — no writes, no page modifications.

Database access: ssh + wp-cli `wp db query` on the VPS (same method used
for the pre-tag integrity checks).  No credentials stored; wp-cli reads
wp-config.php on the server.

Run:  python3 -I e097/verify/body_md5.py
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
ARM_A_ID, ARM_B_ID = 2211, 2212
EXPECTED_CONTENT_MD5   = "56d4f3939b053548331def4c307f5e73"
EXPECTED_CONTENT_BYTES = 7503

# md5 of the exported HTML file (the full file, not the post_content column;
# the export includes the full page source as served, not just the DB field).
EXPECTED_EXPORT_MD5    = "b60dcb77d76576eb9120789892cce50c"

EXPORT_A = os.path.join(REPO_ROOT, "e097", "page-source-arm-a.html")
EXPORT_B = os.path.join(REPO_ROOT, "e097", "page-source-arm-b.html")

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


# ── Live database: post_content md5 and length ───────────────────────

print("=" * 70)
print("Live database: post_content md5 and length")
print("=" * 70)

sql = (
    f"SELECT ID, MD5(post_content), LENGTH(post_content) "
    f"FROM geo_posts WHERE ID IN ({ARM_A_ID},{ARM_B_ID}) ORDER BY ID"
)
rows = wp_query(sql).strip().split("\n")[1:]  # skip header

md5s = []
for row in rows:
    parts = row.split("\t")
    pid, md5_val, length = int(parts[0]), parts[1], int(parts[2])
    md5s.append(md5_val)
    label = "arm A" if pid == ARM_A_ID else "arm B"
    print(f"\nPost {pid} ({label}):")
    check(f"post_content md5", md5_val, EXPECTED_CONTENT_MD5)
    check(f"post_content length", length, EXPECTED_CONTENT_BYTES)

if md5s[0] == md5s[1]:
    print("\n  Arms A and B: post_content is IDENTICAL (md5 match)")
else:
    print("\n  MISMATCH: arms A and B differ in post_content")
    ok = False


# ── Committed export files ───────────────────────────────────────────

print()
print("=" * 70)
print("Committed export files (full file md5, not post_content column)")
print("=" * 70)

file_data = {}
for path, label in [(EXPORT_A, "arm A"), (EXPORT_B, "arm B")]:
    data = open(path, "rb").read()
    md5_val = hashlib.md5(data).hexdigest()
    file_data[label] = data
    print(f"\n{label} ({os.path.basename(path)}):")
    print(f"  file size: {len(data)}")
    check(f"export file md5", md5_val, EXPECTED_EXPORT_MD5)

if file_data["arm A"] == file_data["arm B"]:
    print("\n  Export files arm A and arm B: BYTE-IDENTICAL")
else:
    print("\n  MISMATCH: export files differ between arms")
    ok = False


# ── result ────────────────────────────────────────────────────────────

print()
if ok:
    print("ALL CHECKS PASSED")
    sys.exit(0)
else:
    print("SOME CHECKS FAILED")
    sys.exit(1)
