#!/usr/bin/env python3
"""Inject GSC / Bing verification and optional GA4 from seo-config.json into all HTML."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "seo-config.json"
MARKER = "<!-- seo-verification-tags -->"


def load_config() -> dict:
    if not CONFIG.exists():
        return {}
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    return {k: (v or "").strip() for k, v in data.items()}


def build_snippet(cfg: dict) -> str:
    parts = [MARKER]
    g = cfg.get("google_site_verification", "")
    if g and "PASTE" not in g:
        parts.append(f'<meta name="google-site-verification" content="{g}">')
    b = cfg.get("bing_site_verification", "")
    if b and "PASTE" not in b:
        parts.append(f'<meta name="msvalidate.01" content="{b}">')
    ga = cfg.get("ga4_measurement_id", "")
    if ga and ga.startswith("G-"):
        parts.append(
            f'<script async src="https://www.googletagmanager.com/gtag/js?id={ga}"></script>'
        )
        parts.append(f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{ga}");</script>')
    parts.append("<!-- /seo-verification-tags -->")
    return "\n  ".join(parts)


def inject():
    cfg = load_config()
    snippet = build_snippet(cfg)
    has_real = any(
        x in snippet
        for x in ('name="google-site-verification"', "msvalidate.01", "googletagmanager.com")
    )
    if not has_real:
        print("seo-config.json missing or still placeholders — no tags injected")
        return
    for path in ROOT.rglob("*.html"):
        t = path.read_text(encoding="utf-8")
        t = re.sub(
            r"<!-- seo-verification-tags -->.*?<!-- /seo-verification-tags -->\s*",
            "",
            t,
            flags=re.DOTALL,
        )
        t = t.replace("</head>", f"  {snippet}\n</head>", 1)
        path.write_text(t, encoding="utf-8")
        print("seo tags", path.relative_to(ROOT))


if __name__ == "__main__":
    inject()