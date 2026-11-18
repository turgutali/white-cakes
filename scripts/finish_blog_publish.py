#!/usr/bin/env python3
"""Journal index, sitemap, cross-links, llms.txt after full blog publish."""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROMPT = Path(__file__).resolve().parent / "blog-publish-prompt.md"
LASTMOD_SITE = "2026-11-15"

LEGACY_POSTS = [
    {
        "file": "how-to-order.html",
        "h1": "How to order a custom cake in Cebu",
        "meta": "How to order a White Cakes cake in Cebu: what to tell us, the three-day minimum, and the difference between pickup and delivery.",
        "date": "2026-11-14",
    },
    {
        "file": "choosing-a-flavor.html",
        "h1": "Choosing a flavor",
        "meta": "Chocolate, vanilla, ube, mango, or red velvet — how to pick a White Cakes flavor for your Cebu celebration.",
        "date": "2026-11-14",
    },
    {
        "file": "which-cake.html",
        "h1": "Marble, bouquet, or bento",
        "meta": "Which White Cakes design fits a birthday, a gift, or a table for two in Cebu.",
        "date": "2026-11-14",
    },
    {
        "file": "buttercream-in-cebu-heat.html",
        "h1": "Buttercream in Cebu heat",
        "meta": "When to refrigerate, how to ride home with a cake, and what not to do in a parked car.",
        "date": "2026-11-14",
    },
]

CROSSLINKS = {
    "cake-delivery-cebu-city": [
        ("cake-delivery-cebu.html",),
        ("christmas-cake-delivery-cebu.html",),
        ("corporate-office-cakes-cebu.html",),
        ("first-birthday-sinulog-cake-cebu.html",),
    ],
    "cake-delivery-mandaue": [
        ("cake-delivery-cebu.html",),
        ("christmas-cake-delivery-cebu.html",),
        ("corporate-office-cakes-cebu.html",),
    ],
    "cake-delivery-lapu-lapu": [
        ("cake-delivery-cebu.html",),
        ("christmas-cake-delivery-cebu.html",),
        ("first-birthday-sinulog-cake-cebu.html",),
        ("valentines-bouquet-cake-cebu.html",),
    ],
    "birthday-cakes-cebu": [
        ("debut-cake-cebu.html",),
        ("first-birthday-sinulog-cake-cebu.html",),
        ("what-is-a-bento-cake.html",),
        ("how-far-ahead-to-order-a-cake-cebu.html",),
    ],
    "anniversary-cakes-cebu": [
        ("bouquet-cake-gift-cebu.html",),
        ("valentines-bouquet-cake-cebu.html",),
        ("what-is-a-bento-cake.html",),
    ],
    "wedding-cakes-cebu": [
        ("how-to-choose-wedding-cake-cebu.html",),
        ("how-to-brief-a-custom-cake-cebu.html",),
        ("how-far-ahead-to-order-a-cake-cebu.html",),
    ],
    "corporate-cake-orders-cebu": [
        ("corporate-office-cakes-cebu.html",),
        ("how-far-ahead-to-order-a-cake-cebu.html",),
        ("what-is-a-bento-cake.html",),
    ],
    "bento-cakes-cebu": [
        ("what-is-a-bento-cake.html",),
        ("corporate-office-cakes-cebu.html",),
        ("valentines-bouquet-cake-cebu.html",),
    ],
    "bouquet-cakes-cebu": [
        ("bouquet-cake-gift-cebu.html",),
        ("valentines-bouquet-cake-cebu.html",),
        ("christmas-cake-delivery-cebu.html",),
    ],
    "custom-cakes-cebu": [
        ("how-to-brief-a-custom-cake-cebu.html",),
        ("christening-cake-cebu.html",),
        ("debut-cake-cebu.html",),
        ("how-to-choose-wedding-cake-cebu.html",),
    ],
}

FAQ_GUIDES = [
    ("how-far-ahead-to-order-a-cake-cebu.html",),
    ("cake-delivery-cebu.html",),
    ("how-to-brief-a-custom-cake-cebu.html",),
]


def load_prompt_posts() -> list[dict]:
    text = PROMPT.read_text(encoding="utf-8")
    posts = []
    for chunk in re.findall(
        r"<!-- ===== FILE: \d+-.+?\.md ===== -->\s*(.*?)(?=<!-- ===== FILE:|\Z)",
        text,
        flags=re.DOTALL,
    ):
        if not chunk.lstrip().startswith("---"):
            continue
        parts = chunk.split("---\n", 2)
        meta = yaml.safe_load(parts[1])
        if not meta or "url" not in meta:
            continue
        fname = meta["url"].rsplit("/", 1)[-1]
        pub = meta["publish_date"]
        if hasattr(pub, "isoformat"):
            pub = pub.isoformat()
        posts.append(
            {
                "file": fname,
                "h1": meta["h1"],
                "meta": meta["meta_description"],
                "date": pub,
            }
        )
    return posts


def all_posts() -> list[dict]:
    combined = load_prompt_posts() + LEGACY_POSTS
    combined.sort(key=lambda p: p["date"], reverse=True)
    return combined


def h1_for_file(posts: list[dict], fname: str) -> str:
    for p in posts:
        if p["file"] == fname:
            return p["h1"]
    return fname


def journal_section_html(posts: list[dict]) -> str:
    items = "".join(
        f"""
        <li>
          <a href="/journal/{p['file']}">
            <h3>{p['h1']}</h3>
            <p>{p['meta']}</p>
          </a>
        </li>"""
        for p in posts
    )
    blog_posts = [
        {
            "@type": "BlogPosting",
            "headline": p["h1"],
            "url": f"https://www.thewhitecakes.com/journal/{p['file']}",
            "datePublished": p["date"],
        }
        for p in posts
    ]
    blog_ld = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "@id": "https://www.thewhitecakes.com/journal/",
        "name": "Journal — Notes from the bench",
        "description": "Practical notes on ordering, delivery and celebrating with cake in Cebu.",
        "publisher": {"@id": "https://www.thewhitecakes.com/#organization"},
        "blogPost": blog_posts,
    }
    crumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.thewhitecakes.com/"},
            {"@type": "ListItem", "position": 2, "name": "Journal", "item": "https://www.thewhitecakes.com/journal/"},
        ],
    }
    return f"""<!DOCTYPE html>
<html lang="en-PH">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Journal: Cake Guides for Cebu | The White Cakes - Cebu</title>
  <meta name="description" content="Journal from White Cakes Cebu: ordering, delivery, bento and wedding cakes, Christmas gifts, debut, christening, and buttercream in tropical heat.">
  <link rel="canonical" href="https://www.thewhitecakes.com/journal/">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta property="og:title" content="Journal: Cake Guides for Cebu | The White Cakes - Cebu">
  <meta property="og:description" content="Practical notes on ordering, delivery and celebrating with cake in Cebu.">
  <meta property="og:url" content="https://www.thewhitecakes.com/journal/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="The White Cakes - Cebu">
  <meta property="og:locale" content="en_PH">
  <meta property="og:image" content="https://www.thewhitecakes.com/assets/og.webp">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="An ivory marble cake by The White Cakes - Cebu">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Journal: Cake Guides for Cebu | The White Cakes - Cebu">
  <meta name="twitter:description" content="Practical notes on ordering, delivery and celebrating with cake in Cebu.">
  <meta name="twitter:image" content="https://www.thewhitecakes.com/assets/og.webp">
  <link rel="stylesheet" href="../css/styles.css">
  <link rel="icon" href="/favicon-96.png" type="image/png" sizes="96x96">
  <link rel="icon" href="/favicon-48.png" type="image/png" sizes="48x48">
  <link rel="icon" href="/favicon-192.png" type="image/png" sizes="192x192">
  <link rel="icon" href="/favicon-512.png" type="image/png" sizes="512x512">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
  <link rel="manifest" href="/site.webmanifest">
  <script type="application/ld+json">
{json.dumps(crumb, indent=2)}
  </script>
  <script type="application/ld+json">
{json.dumps(blog_ld, indent=2)}
  </script>
</head>
<body class="sub">
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header" id="site-header">
    <a class="brand" href="/"><img class="mark" src="/logo-512.png" srcset="/favicon-48.png 48w, /favicon-96.png 96w, /favicon-192.png 192w, /logo-512.png 512w" sizes="44px" width="44" height="44" alt="The White Cakes - Cebu logo" decoding="async"><span class="wordmark">White Cakes</span></a>
    <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="primary-nav">Menu</button>
    <div class="header-end">
      <nav class="nav" id="primary-nav" aria-label="Primary">
        <a href="/#collection">Collection</a>
        <a href="/#occasions">Occasions</a>
        <a href="/journal/">Journal</a>
        <a href="/#delivery">Delivery</a>
        <a href="/#order">Order</a>
      </nav>
      <a class="header-cta" href="/#order">Order</a>
    </div>
  </header>
  <main id="main" class="article">
    <h1>Notes from the bench</h1>
    <p class="dek">Practical notes on ordering, delivery and celebrating with cake in Cebu.</p>
    <div class="section-inner">
      <ol class="journal-list">
        {items}
      </ol>
      <p class="next-step"><a href="/#order">Order Your Cake</a></p>
    </div>
  </main>
  <footer class="site-footer">
    <div class="section-inner">
      <a class="brand brand-stack" href="/"><img class="mark" src="/logo-512.png" srcset="/favicon-48.png 48w, /favicon-96.png 96w, /favicon-192.png 192w, /logo-512.png 512w" sizes="44px" width="44" height="44" alt="The White Cakes - Cebu logo" decoding="async"><span class="wordmark">White Cakes</span></a>
      <ul class="footer-links">
        <li><a href="mailto:info@thewhitecakes.com">info@thewhitecakes.com</a></li>
        <li><a data-wa href="https://wa.me/639474382632" rel="noopener noreferrer">WhatsApp <span data-wa-label>+63 947 438 2632</span></a></li>
        <li><a href="https://www.instagram.com/thewhitecakescebu/" rel="noopener noreferrer">Instagram</a></li>
        <li><a href="https://www.facebook.com/profile.php?id=61596567450476" rel="noopener noreferrer">Facebook</a></li>
        <li><a href="/#order">Order</a></li>
      </ul>
      <p class="loc">Cebu, Philippines</p>
      <p class="legal">© 2026 White Cakes</p>
    </div>
  </footer>
  <script src="../js/main.js" defer></script>
</body>
</html>"""


def add_crosslinks(slug: str, files: list[tuple[str, ...]], posts: list[dict]):
    path = ROOT / slug / "index.html"
    if not path.exists():
        return
    t = path.read_text(encoding="utf-8")
    t = re.sub(r"\s*<nav class=\"journal-from-bench\".*?</nav>\s*", "\n          ", t, count=1, flags=re.DOTALL)
    lis = "".join(
        f'<li><a href="/journal/{f}">{h1_for_file(posts, f)}</a></li>' for (f,) in files
    )
    block = f"""<nav class="journal-from-bench" aria-label="From our journal">
            <p class="kicker">From our journal</p>
            <ul>
              {lis}
            </ul>
          </nav>
          <aside class="article-end">"""
    if "<aside class=\"article-end\">" not in t:
        return
    t = t.replace('<aside class="article-end">', block, 1)
    path.write_text(t, encoding="utf-8")


def faq_guides(posts: list[dict]):
    path = ROOT / "faq" / "index.html"
    t = path.read_text(encoding="utf-8")
    t = re.sub(r"\s*<nav class=\"related-guides\".*?</nav>\s*", "\n      ", t, count=1, flags=re.DOTALL)
    lis = "".join(
        f'<li><a href="/journal/{f}">{h1_for_file(posts, f)}</a></li>' for (f,) in FAQ_GUIDES
    )
    block = f"""<nav class="related-guides" aria-label="Related guides">
        <p class="kicker">Related guides</p>
        <ul>
          {lis}
        </ul>
      </nav>
    </main>"""
    t = t.replace("</main>", block, 1)
    path.write_text(t, encoding="utf-8")


def home_journal(posts: list[dict]):
    path = ROOT / "index.html"
    t = path.read_text(encoding="utf-8")
    items = "".join(
        f"""
          <li>
            <a href="journal/{p['file']}">
              <h3>{p['h1']}</h3>
              <p>{p['meta']}</p>
            </a>
          </li>"""
        for p in posts[:3]
    )
    t = re.sub(
        r'<ol class="journal-list">.*?</ol>',
        f'<ol class="journal-list">{items}\n        </ol>',
        t,
        count=1,
        flags=re.DOTALL,
    )
    # richer intro under journal section
    t = t.replace(
        "Short guides on ordering, flavor, and heat in Cebu.",
        "Guides on delivery, lead time, bento and wedding cakes, debut, christening, and celebrating in Cebu heat.",
    )
    path.write_text(t, encoding="utf-8")


def sitemap(posts: list[dict]):
    del posts
    from apply_brand_seo import write_sitemap

    write_sitemap()


def robots():
    from apply_brand_seo import write_robots

    write_robots()


def llms_txt(posts: list[dict]):
    del posts
    from apply_brand_seo import write_llms

    write_llms()


def main():
    posts = all_posts()
    (ROOT / "journal" / "index.html").write_text(journal_section_html(posts), encoding="utf-8")
    for slug, links in CROSSLINKS.items():
        add_crosslinks(slug, links, posts)
    faq_guides(posts)
    home_journal(posts)
    sitemap(posts)
    robots()
    llms_txt(posts)
    print(f"Updated index, sitemap ({len(posts)} posts), cross-links, llms.txt")


if __name__ == "__main__":
    main()
