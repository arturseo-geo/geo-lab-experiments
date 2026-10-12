#!/usr/bin/env python3
"""
E100 Phase 0 snippet-window offset measurement (pinned method).

Method (deterministic, standard library only):
  1. Input is a full-page HTML file or a URL fetched with a specified UA.
  2. Extract the entry-content element: regex match on
     <div class="entry-content ..."> up to <div class="author-bio" or
     <div class="wp-block-group site-footer".
  3. Tag-strip using html.parser (HTMLParser subclass that skips <script>
     and <style> content, joins all handle_data output).
  4. Decode HTML entities via html.unescape().
  5. Collapse all runs of whitespace (spaces, tabs, newlines) to a
     single space, then strip leading/trailing whitespace.
  6. Report:
     - Character offset of the first occurrence of
       "AI search engines can only cite"
     - md5 of the first 200 characters of the resulting string.

Usage:
  python3 snippet_offset.py FILE [FILE ...]
  python3 snippet_offset.py --url URL --ua browser|googlebot
"""

import hashlib
import html
import re
import sys
import urllib.request
from html.parser import HTMLParser

NEEDLE = "AI search engines can only cite"

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/128.0.0.0 Safari/537.36"
)
GOOGLEBOT_UA = (
    "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/128.0.6613.137 Mobile Safari/537.36 "
    "(compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
)


class _TextExtractor(HTMLParser):
    """Extract visible text, skipping <script> and <style> content."""

    def __init__(self):
        super().__init__()
        self.pieces = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip_depth = max(0, self._skip_depth - 1)

    def handle_data(self, data):
        if self._skip_depth == 0:
            self.pieces.append(data)


def extract_entry_content(page_html):
    """Return the innerHTML of the entry-content div."""
    m = re.search(
        r'<div class="entry-content[^"]*">(.*)',
        page_html,
        re.DOTALL,
    )
    if not m:
        return page_html
    content = m.group(1)
    for marker in (
        '<div class="author-bio',
        '<div class="wp-block-group site-footer',
    ):
        idx = content.find(marker)
        if idx > 0:
            content = content[:idx]
            break
    return content


def measure(page_html):
    """Return (offset, md5_200, stripped_text_preview)."""
    ec = extract_entry_content(page_html)
    parser = _TextExtractor()
    parser.feed(ec)
    raw_text = "".join(parser.pieces)
    decoded = html.unescape(raw_text)
    collapsed = re.sub(r"\s+", " ", decoded).strip()
    offset = collapsed.find(NEEDLE)
    md5_200 = hashlib.md5(collapsed[:200].encode("utf-8")).hexdigest()
    return offset, md5_200, collapsed[:120]


def fetch_url(url, ua):
    """Fetch a URL with the given User-Agent string."""
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    if args[0] == "--url":
        url = args[1]
        ua_name = args[2] if len(args) > 2 else "browser"
        ua = GOOGLEBOT_UA if ua_name == "googlebot" else BROWSER_UA
        page = fetch_url(url, ua)
        offset, md5_200, preview = measure(page)
        print("url:     %s" % url)
        print("ua:      %s" % ua_name)
        print("offset:  %d" % offset)
        print("md5_200: %s" % md5_200)
        print("preview: %s" % preview)
    else:
        for path in args:
            with open(path, encoding="utf-8", errors="replace") as f:
                page = f.read()
            offset, md5_200, preview = measure(page)
            print("file:    %s" % path)
            print("offset:  %d" % offset)
            print("md5_200: %s" % md5_200)
            print("preview: %s" % preview)
            print()


if __name__ == "__main__":
    main()
