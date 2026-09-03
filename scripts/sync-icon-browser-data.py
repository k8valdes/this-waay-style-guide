#!/usr/bin/env python3
"""
sync-icon-browser-data.py — regenerates the embedded ICON_DATA snapshot inside
product-design-studio/index.html from the source of truth,
product-design-studio/assets/icons/icon-manifest.json.

The icon-library live preview embeds a compact copy of the manifest directly in
the page (not fetched at runtime, so it works over file://, a local server, or
GitHub Pages alike). Run this whenever icon-manifest.json changes so the two
never drift — the same class of staleness the guide's own :root snapshot once
had (see CHANGELOG.md, 2026-08 spec correction).

    python3 scripts/sync-icon-browser-data.py
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / "product-design-studio" / "assets" / "icons" / "icon-manifest.json"
GUIDE = REPO / "product-design-studio" / "index.html"


def main():
    manifest = json.loads(MANIFEST.read_text())
    compact = [[e["file"], e["concept"], e["category"], e["aliases"]] for e in manifest["icons"]]
    data_literal = json.dumps(compact, separators=(",", ":"))

    html = GUIDE.read_text(encoding="utf-8")
    pattern = re.compile(r"var ICON_DATA = \[.*?\];", re.DOTALL)
    if not pattern.search(html):
        sys.exit("error: 'var ICON_DATA = [...]' not found in index.html — has the browser been removed?")

    new_html = pattern.sub(f"var ICON_DATA = {data_literal};", html, count=1)
    if new_html == html:
        print(f"already in sync — {len(compact)} icons, no change written")
    else:
        GUIDE.write_text(new_html, encoding="utf-8")
        print(f"synced — {len(compact)} icons written into index.html's embedded ICON_DATA")


if __name__ == "__main__":
    main()
