#!/usr/bin/env python3
"""Check the built site (public/) for broken internal links.

Catches the two classes of internal 404s that Hugo will happily emit:
  - relative links that resolve past the current page (e.g. a card on
    /courses/ linking to "courses/core/..." -> /courses/courses/...)
  - root-absolute links ("...href=/courses") that drop the baseURL
    sub-path on GitHub Pages project sites

External links are checked separately by lychee (check-links.yml).

Usage: python3 scripts/check_internal_links.py [public]
Exits non-zero and prints offenders if any broken link is found.
"""

import html
import os
import re
import sys
from urllib.parse import unquote, urlparse

BASE_PATH = urlparse(os.environ.get("HUGO_BASEURL", "")).path


def exists(path: str) -> bool:
    return os.path.isfile(path) or os.path.isdir(path)


def resolves(target: str, public_root: str, page_dir: str) -> bool:
    if target.startswith("/"):
        # Root-absolute URLs must carry the baseURL sub-path (if any),
        # otherwise GitHub Pages serves them from the domain root.
        if BASE_PATH and not (target + "/").startswith(BASE_PATH):
            return False
        target = target[len(BASE_PATH):] if BASE_PATH else target.lstrip("/")
        full = os.path.join(public_root, target.lstrip("/"))
    else:
        full = os.path.normpath(os.path.join(page_dir, target))
    return (
        exists(full)
        or exists(full + ".html")
        or exists(full + "/index.html")
    )


def main() -> int:
    public_root = sys.argv[1] if len(sys.argv) > 1 else "public"
    if not os.path.isdir(public_root):
        print(f"error: {public_root} not found — run hugo first", file=sys.stderr)
        return 2

    broken = {}
    page_count = 0
    for root, _dirs, files in os.walk(public_root):
        for name in files:
            if not name.endswith(".html"):
                continue
            page_count += 1
            path = os.path.join(root, name)
            with open(path, encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
            for match in re.finditer(r'(?:href|src)=("[^"]*"|[^\s>]+)', content):
                url = html.unescape(match.group(1).strip('"')).split("#")[0]
                if not url or url.startswith(("http", "mailto:", "tel:", "data:")):
                    continue
                if not resolves(unquote(url), public_root, os.path.dirname(path)):
                    broken.setdefault(url, path)

    if broken:
        print(f"❌ {len(broken)} broken internal link(s) across {page_count} pages:")
        for url, page in sorted(broken.items()):
            print(f"  {page} -> {url}")
        return 1

    print(f"✅ {page_count} pages, all internal links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
