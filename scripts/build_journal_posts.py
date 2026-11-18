#!/usr/bin/env python3
"""Build journal HTML from blog-publish-prompt.md (posts 01–04 this run)."""
from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
PROMPT = Path(__file__).resolve().parent / "blog-publish-prompt.md"
PUBLISH_IDS = {"19"}

LIVE_JOURNAL = {
    "how-to-order.html",
    "choosing-a-flavor.html",
    "which-cake.html",
    "buttercream-in-cebu-heat.html",
    "christmas-cake-delivery-cebu.html",
    "what-is-a-bento-cake.html",
    "how-to-choose-wedding-cake-cebu.html",
    "cake-delivery-cebu.html",
    "how-far-ahead-to-order-a-cake-cebu.html",
    "bouquet-cake-gift-cebu.html",
    "corporate-office-cakes-cebu.html",
    "debut-cake-cebu.html",
    "first-birthday-sinulog-cake-cebu.html",
    "how-to-brief-a-custom-cake-cebu.html",
    "christening-cake-cebu.html",
    "valentines-bouquet-cake-cebu.html",
    "graduation-cakes-cebu.html",
    "cake-prices-cebu.html",
    "ube-cake-cebu.html",
    "baby-shower-cakes-cebu.html",
    "send-cake-to-cebu-from-abroad.html",
    "mothers-day-cakes-cebu.html",
    "anniversary-cake-message-ideas-cebu.html",
}

POSTS_META = []  # filled after build for index/sitemap


def parse_frontmatter(chunk: str) -> tuple[dict, str]:
    if not chunk.lstrip().startswith("---"):
        raise ValueError("missing front matter")
    parts = chunk.split("---\n", 2)
    meta = yaml.safe_load(parts[1])
    rest = parts[2]
    return meta, rest


def extract_jsonld(chunk: str) -> str:
    m = re.search(
        r"<script type=\"application/ld\+json\">\s*(\{.*?\})\s*</script>",
        chunk,
        re.DOTALL,
    )
    if not m:
        raise ValueError("JSON-LD not found")
    data = json.loads(m.group(1))
    return json.dumps(data, indent=2, ensure_ascii=False)


def photo_to_comment(text: str) -> str:
    def repl(m: re.Match) -> str:
        block = m.group(0)
        alt_m = re.search(r'Suggested alt text:\s*"([^"]+)"', block)
        alt = alt_m.group(1) if alt_m else ""
        desc = re.sub(r"^>\s*\*\*Photo placeholder[^:]*:\*\*\s*", "", block)
        desc = desc.split("Suggested alt text")[0].strip().rstrip(".")
        return f'<!-- PHOTO TODO: {desc} | alt="{alt}" -->'

    return re.sub(
        r">\s*\*\*Photo placeholder \(real photo only\):\*\*.*?(?:\n\n|\n(?=#))",
        repl,
        text,
        flags=re.DOTALL,
    )


def preprocess_links(md: str) -> str:
    def link(m: re.Match) -> str:
        label, dest = m.group(1), m.group(2)
        if dest.startswith("/journal/"):
            slug = dest.rstrip("/").split("/")[-1]
            if not slug.endswith(".html"):
                slug += ".html"
            if slug not in LIVE_JOURNAL:
                return f"{label}<!-- LINK WHEN LIVE: {dest} -->"
        return f'<a href="{dest}">{label}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, md)


def split_cta(md: str) -> tuple[str, str | None]:
    m = re.search(r"^## (?:Order|Start your).*$", md, re.MULTILINE | re.IGNORECASE)
    if not m:
        return md, None
    return md[: m.start()].rstrip(), md[m.start() :].strip()


def md_to_html(md: str) -> str:
    md = md.strip()
    md = re.sub(r"^# .+\n", "", md, count=1)
    md = photo_to_comment(md)
    md = preprocess_links(md)
    html_out = markdown.markdown(
        md,
        extensions=["extra", "smarty"],
        output_format="html5",
    )
    html_out = re.sub(
        r"<p><strong>Quick answer:</strong>\s*(.*?)</p>",
        r'<p class="quick-answer"><strong>Quick answer:</strong> \1</p>',
        html_out,
        count=1,
        flags=re.DOTALL,
    )
    return html_out


def format_publish_date(iso) -> tuple[str, str]:
    if not isinstance(iso, str):
        iso = iso.isoformat()
    d = datetime.strptime(iso, "%Y-%m-%d")
    human = f"Published {d.day} {d.strftime('%B %Y')}"
    return iso, human


def wa_from_cta(cta: str | None, default: str) -> str:
    if not cta:
        return default
    m = re.search(r"\((https://wa\.me/[^)]+)\)", cta)
    return m.group(1) if m else default


def render_page(meta: dict, body_html: str, jsonld: str, wa_url: str) -> str:
    title = html.escape(meta["title"])
    desc = html.escape(meta["meta_description"])
    url = meta["url"]
    h1 = html.escape(meta["h1"])
    og_alt = html.escape(meta.get("og_image_alt", "White Cakes Cebu"))
    pub_iso, pub_human = format_publish_date(meta["publish_date"])

    return f"""<!DOCTYPE html>
<html lang="en-PH">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta property="og:image" content="https://www.thewhitecakes.com/assets/og.webp">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{og_alt}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="https://www.thewhitecakes.com/assets/og.webp">
  <meta property="og:title" content="{h1}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="The White Cakes - Cebu">
  <meta property="og:locale" content="en_PH">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Manrope:wght@400;500;600&display=swap">
  <link rel="stylesheet" href="../css/styles.css">
  <link rel="icon" href="/favicon-96.png" type="image/png" sizes="96x96">
  <link rel="icon" href="/favicon-48.png" type="image/png" sizes="48x48">
  <link rel="icon" href="/favicon-192.png" type="image/png" sizes="192x192">
  <link rel="icon" href="/favicon-512.png" type="image/png" sizes="512x512">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
  <link rel="manifest" href="/site.webmanifest">
  <script type="application/ld+json">
{jsonld}
  </script>
</head>
<body class="sub">
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header" id="site-header">
    <a class="brand" href="/">
      <img class="mark" src="/logo-512.png" srcset="/favicon-48.png 48w, /favicon-96.png 96w, /favicon-192.png 192w, /logo-512.png 512w" sizes="44px" width="44" height="44" alt="The White Cakes - Cebu logo" decoding="async">
      <span class="wordmark">White Cakes</span>
    </a>
    <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="primary-nav">Menu</button>
    <div class="header-end">
      <nav class="nav" id="primary-nav" aria-label="Primary">
        <a href="/#collection">Collection</a>
        <a href="/#occasions">Occasions</a>
        <a href="/journal/">Journal</a>
        <a href="/#delivery">Delivery</a>
        <a href="/#how">How to order</a>
      </nav>
      <a class="header-cta" href="/order/">Order</a>
    </div>
  </header>
  <main id="main">
    <article class="article">
      <p class="crumb"><a href="/journal/">Journal</a></p>
      <h1>{h1}</h1>
      <p class="article-byline">By White Cakes · Lahug, Cebu City · <time datetime="{pub_iso}">{pub_human}</time></p>
      <div class="prose">
{body_html}
      </div>
      <aside class="article-end">
        <p>Tell us your date. We confirm within a day.</p>
        <div class="hero-actions">
          <a class="btn" href="/order/">Order Your Cake</a>
          <a class="btn btn-quiet" data-wa href="{html.escape(wa_url, quote=True)}" rel="noopener noreferrer">WhatsApp</a>
          <a class="btn btn-quiet" href="https://m.me/thewhitecakes" rel="noopener noreferrer">Messenger</a>
        </div>
      </aside>
    </article>
  </main>
  <footer class="site-footer">
    <div class="section-inner">
      <a class="brand" href="/"><img class="mark" src="/logo-512.png" srcset="/favicon-48.png 48w, /favicon-96.png 96w, /favicon-192.png 192w, /logo-512.png 512w" sizes="44px" width="44" height="44" alt="The White Cakes - Cebu logo" decoding="async"><span class="wordmark">White Cakes</span></a>
      <ul class="footer-links">
        <li><a href="mailto:info@thewhitecakes.com">info@thewhitecakes.com</a></li>
        <li><a data-wa href="https://wa.me/639474382632" rel="noopener noreferrer">WhatsApp <span data-wa-label>+63 947 438 2632</span></a></li>
        <li><a href="/journal/">Journal</a></li>
      </ul>
      <p class="loc">Cebu, Philippines</p>
      <p class="legal">© 2026 White Cakes</p>
    </div>
  </footer>
  <nav class="dock" aria-label="Quick actions">
    <a href="/order/">Order</a>
    <a data-wa href="https://wa.me/639474382632" rel="noopener noreferrer">WhatsApp</a>
  </nav>
  <script src="../js/main.js" defer></script>
</body>
</html>
"""


def slug_from_meta(meta: dict) -> str:
    url = meta["url"]
    return url.rsplit("/", 1)[-1]


def build_posts():
    text = PROMPT.read_text(encoding="utf-8")
    segments = re.findall(
        r"<!-- ===== FILE: (\d+)-.+?\.md ===== -->\s*(.*?)(?=<!-- ===== FILE:|\Z)",
        text,
        flags=re.DOTALL,
    )
    for num, chunk in segments:
        if num not in PUBLISH_IDS:
            continue
        meta, rest = parse_frontmatter(chunk)
        jsonld_part = rest.split("<!-- JSONLD -->", 1)[1]
        md_part = rest.split("<!-- JSONLD -->", 1)[0]
        jsonld = extract_jsonld(jsonld_part)
        main_md, cta_md = split_cta(md_part)
        body_html = md_to_html(main_md)
        wa = wa_from_cta(
            cta_md, "https://wa.me/639474382632?text=Hi%20White%20Cakes%2C%20I%27d%20like%20to%20order%20a%20cake"
        )
        page = render_page(meta, body_html, jsonld, wa)
        fname = slug_from_meta(meta)
        out = ROOT / "journal" / fname
        out.write_text(page, encoding="utf-8")
        LIVE_JOURNAL.add(fname)
        POSTS_META.append(
            {
                "file": fname,
                "h1": meta["h1"],
                "title": meta["title"],
                "meta_description": meta["meta_description"],
                "url": meta["url"],
                "publish_date": meta["publish_date"].isoformat()
                if hasattr(meta["publish_date"], "isoformat")
                else meta["publish_date"],
            }
        )
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    build_posts()
