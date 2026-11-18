#!/usr/bin/env python3
"""Notify IndexNow-participating search engines about changed HTML pages."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.thewhitecakes.com"
ENDPOINT = "https://api.indexnow.org/indexnow"
ROBOTS_META = re.compile(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)', re.I)
CANONICAL = re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', re.I)


def find_key() -> tuple[str, Path]:
    for path in ROOT.glob("*.txt"):
        value = path.read_text(encoding="utf-8").strip()
        if path.stem == value and re.fullmatch(r"[A-Za-z0-9-]{8,128}", value):
            return value, path
    raise SystemExit("IndexNow key file not found in the site root")


def changed_html(before: str, after: str) -> list[str]:
    if not before or set(before) == {"0"}:
        result = subprocess.run(
            ["git", "ls-files", "--", "*.html"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        paths = result.stdout.splitlines()
    else:
        result = subprocess.run(
            ["git", "diff", "--name-only", before, after, "--", "*.html"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        paths = result.stdout.splitlines()
    return sorted({path for path in paths if path.endswith(".html") and path != "404.html"})


def page_url(relative_path: str) -> str:
    path = Path(relative_path)
    if path.name == "index.html":
        suffix = path.parent.as_posix()
        return f"{BASE}/{suffix}/" if suffix != "." else f"{BASE}/"
    return f"{BASE}/{path.as_posix()}"


def indexable_url(relative_path: str) -> str | None:
    page = ROOT / relative_path
    if not page.exists():
        # A deleted page should also be removed from participating indexes.
        return page_url(relative_path)
    html = page.read_text(encoding="utf-8")
    robots = ROBOTS_META.search(html)
    if robots and "noindex" in robots.group(1).lower():
        return None
    canonical = CANONICAL.search(html)
    url = canonical.group(1).strip() if canonical else page_url(relative_path)
    return url if url.startswith(BASE + "/") else None


def main() -> int:
    before = sys.argv[1] if len(sys.argv) > 1 else ""
    after = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
    urls = sorted({url for path in changed_html(before, after) if (url := indexable_url(path))})
    if not urls:
        print("No indexable HTML URLs changed; nothing to submit.")
        return 0

    key, key_file = find_key()
    payload = json.dumps(
        {
            "host": "www.thewhitecakes.com",
            "key": key,
            "keyLocation": f"{BASE}/{key_file.name}",
            "urlList": urls,
        }
    ).encode("utf-8")
    request = Request(
        ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            print(f"IndexNow accepted {len(urls)} URL(s): HTTP {response.status}")
            return 0 if response.status in (200, 202) else 1
    except HTTPError as error:
        print(f"IndexNow rejected the submission: HTTP {error.code} {error.read().decode('utf-8', 'replace')}")
    except URLError as error:
        print(f"Could not reach IndexNow: {error.reason}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
