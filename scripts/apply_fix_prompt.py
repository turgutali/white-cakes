#!/usr/bin/env python3
"""Apply fix-prompt-2: unescape URLs, expand copy, meta, journal, 404."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WA_PREFILL = "https://wa.me/639474382632?text=Hi%20White%20Cakes%2C%20I%27d%20like%20to%20order%20a%20cake"

from landing_copy import COPY, META_OCCASION

LANDINGS = list(COPY.keys())

EXTENSIONS = {
    "bento-cakes-cebu": """<h2>Servings</h2><p>A 4-inch bento is sized for two generous slices, or three modest ones after a meal. It is not a centrepiece for a hall — if the guest list is a family table, see our <a href="../custom-cakes-cebu/">Signature Marble</a> or message us with the count.</p>
<h2>Compared with catalogue bentos</h2><p>Same-day mall and marketplace bentos are a different product: printed toppers, rush hours, and cases. We bake for your named date and pipe shells and a rose by hand. Shoppers who need a cake tonight should not start here; shoppers who need a finished small cake in three days should.</p>""",
    "bouquet-cakes-cebu": """<h2>Carrying and storage</h2><p>Keep the cake upright, out of sun, and cool until it is opened. If delivery lands hours before dinner, refrigerate when you can — especially in Cebu afternoons. The <a href="../journal/buttercream-in-cebu-heat.html">heat note</a> in our journal is written for exactly that gap.</p>
<h2>When to choose marble instead</h2><p>Pick Signature Marble when children expect a name on a tall tier and candles. Pick bouquet when the moment is softer: thank-yous, anniversaries, and gifts that should look like flowers on arrival.</p>""",
    "custom-cakes-cebu": """<h2>What to send for a custom brief</h2><p>Guest count, event time, indoor or outdoor venue, palette, and a photo if you have one. We pipe in buttercream — fondant figures, heavy toppers, and edible print sheets are not our bench. We will say no in reply rather than deliver something we cannot finish properly.</p>
<h2>Flavour pairings</h2><p>Ube and mango read Filipino and festive; chocolate and vanilla stay neutral for mixed tables; red velvet suits a bold palette. <a href="../journal/choosing-a-flavor.html">Choosing a flavor</a> is the longer guide if you are undecided.</p>""",
    "birthday-cakes-cebu": """<h2>Candles and inscriptions</h2><p>Say if you need space for candles or a long name on top. We pipe what you send — double-check spelling in the order form. For a milestone debut or 18th, tell us early if the reception is large; we may ask for more lead time.</p>
<h2>After-school and office birthdays</h2><p>Bento cakes suit office desks and classrooms where a tall cake is awkward. Signature Marble suits a home table where everyone is eating together. Either way, three days’ notice applies.</p>""",
    "anniversary-cakes-cebu": """<h2>Surprise deliveries</h2><p>If the recipient should not see the message before opening, put the line in the order notes and tell us who answers the door. We confirm the window by SMS to the contact you give — not to the recipient unless you ask.</p>
<h2>Photos for reference</h2><p>Pinterest and Instagram palettes are welcome. Buttercream cannot match every screen colour; we will adjust in reply if a requested blush or blue is outside what we can pipe on your date.</p>""",
    "wedding-cakes-cebu": """<h2>Tiers and servings</h2><p>Tell us realistic guest count and how the cake will be served — after dinner, during cocktails, or only for photos. We do not publish tier diagrams; we reply with what size and finish the bench can do for that date.</p>
<h2>Venue coordination</h2><p>Ask your venue about cake tables, power for AC near an outdoor setup, and whether they allow outside cakes. We deliver to the address you give; we do not negotiate corkage with the hotel — that stays between you and the venue.</p>""",
    "corporate-cake-orders-cebu": """<h2>Multiple cakes on one date</h2><p>Several bento boxes for a team need the same lead time as one marble cake — each one is piped separately. Send a list with names or flavours if each desk is different; we confirm what the bench can accept.</p>
<h2>Receiving at IT Park and BPO towers</h2><p>Lobby passes and floor access should be arranged before the driver arrives. Leave a named contact who can meet the delivery; guards cannot hold buttercream in a warm guardhouse.</p>""",
    "cake-delivery-cebu-city": """<h2>Traffic and windows</h2><p>Port area, flyovers, and school zones shift delivery windows without warning. We text inside the agreed range when the cake leaves the kitchen — not an hour before. Have someone reachable on the mobile number you gave.</p>
<h2>Same-day expectations</h2><p>We are not a same-day delivery catalogue. Services advertising free same-day city delivery operate on a different model. Our delivery page is for cakes ordered at least three days ahead, finished by hand.</p>""",
    "cake-delivery-mandaue": """<h2>Industrial and residential drops</h2><p>Factory gates, subdivisions with visitor slips, and coastal condos each need different notes. Write the name on the pass list if your village requires it; drivers cannot guess your phase and block.</p>
<h2>Combining with Cebu City pickup</h2><p>Some Mandaue customers collect in Cebu City when their day is tighter than ours. Say so in the order if you are flexible — we will reply with the option that protects the buttercream.</p>""",
    "cake-delivery-lapu-lapu": """<h2>Resorts and Airbnbs</h2><p>Short-term rentals and resorts need the guest name on the booking to match the delivery. Drivers are turned away at gates when the name on the cake order does not match the reservation — that detail is yours to align.</p>
<h2>Motorcycle and car transport</h2><p>If you collect yourself, a bento fits a top box more safely than a tall tier. Say how you will travel; we will suggest the cake shape that survives the ride.</p>""",
}


def unescape_urls(html: str) -> str:
    return html.replace("https:\\/\\/", "https://").replace("\\/", "/")


def replace_prose(html: str, body: str) -> str:
    return re.sub(
        r"(<div class=\"prose\">)\s*.*?\s*(</div>\s*<aside class=\"article-end\">)",
        rf"\1\n    {body}\n          \2",
        html,
        count=1,
        flags=re.DOTALL,
    )


def word_count_html(html: str) -> int:
    prose = re.search(r'<div class="prose">(.*?)</div>', html, re.DOTALL)
    if not prose:
        return 0
    text = re.sub(r"<[^>]+>", " ", prose.group(1))
    return len(text.split())


def patch_landings():
    counts = {}
    for slug in LANDINGS:
        path = ROOT / slug / "index.html"
        if not path.exists():
            continue
        html = unescape_urls(path.read_text(encoding="utf-8"))
        body = COPY[slug] + EXTENSIONS.get(slug, "")
        html = replace_prose(html, body)
        if slug in META_OCCASION:
            desc = META_OCCASION[slug]
            html = re.sub(
                r'<meta name="description" content="[^"]*">',
                f'<meta name="description" content="{desc}">',
                html,
                count=1,
            )
            html = re.sub(
                r'<meta property="og:description" content="[^"]*">',
                f'<meta property="og:description" content="{desc}">',
                html,
                count=1,
            )
            html = re.sub(
                r'<meta name="twitter:description" content="[^"]*">',
                f'<meta name="twitter:description" content="{desc}">',
                html,
                count=1,
            )
        path.write_text(html, encoding="utf-8")
        counts[slug] = word_count_html(html)
    return counts


def fix_wa_labels(root: Path):
    for f in root.rglob("*.html"):
        t = f.read_text(encoding="utf-8")
        n = t
        n = n.replace("+63 9XX XXX XXXX", "+63 947 438 2632")
        n = re.sub(
            r'(<a class="btn btn-quiet" data-wa href=")https://wa\.me/639474382632(")',
            rf"\1{WA_PREFILL}\2",
            n,
        )
        if n != t:
            f.write_text(n, encoding="utf-8")


def patch_home_meta():
    path = ROOT / "index.html"
    desc = "Luxury cakes to order in Cebu: Marble, Bouquet, and Bento. Delivery in Cebu City, Mandaue, and Lapu-Lapu. Order three days ahead."
    t = path.read_text(encoding="utf-8")
    assert len(desc) <= 155, len(desc)
    for pat in ("description", "og:description", "twitter:description"):
        if pat == "description":
            t = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', t, count=1)
        else:
            key = "property" if pat == "og:description" else "name"
            t = re.sub(
                rf'<meta {key}="{pat}" content="[^"]*">',
                f'<meta {key}="{pat}" content="{desc}">',
                t,
                count=1,
            )
    if '<link rel="icon" href="/favicon.ico"' not in t:
        t = t.replace(
            '<link rel="apple-touch-icon"',
            '<link rel="icon" href="/favicon.ico" sizes="any">\n  <link rel="icon" href="/assets/icon-192.png" type="image/png" sizes="192x192">\n  <link rel="apple-touch-icon"',
        )
    path.write_text(t, encoding="utf-8")


def patch_journal_index():
    path = ROOT / "journal/index.html"
    t = path.read_text(encoding="utf-8")
    t = unescape_urls(t)
    crumb = """
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.thewhitecakes.com/" },
      { "@type": "ListItem", "position": 2, "name": "Journal", "item": "https://www.thewhitecakes.com/journal/" }
    ]
  }
  </script>"""
    if "BreadcrumbList" not in t:
        t = t.replace("</head>", crumb + "\n</head>")
    t = re.sub(
        r'<p class="kicker" style="margin-top:var\(--space-lg\)">Coming soon</p>\s*<ol class="journal-list">.*?</ol>',
        '<p class="lede" style="margin-top:var(--space-lg)">Coming soon on the bench: how to choose a wedding cake in Cebu, and what is a bento cake — not linked until the pieces are written.</p>',
        t,
        flags=re.DOTALL,
    )
    path.write_text(t, encoding="utf-8")


def patch_404():
    path = ROOT / "404.html"
    t = """<!DOCTYPE html>
<html lang="en-PH">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page not found | The White Cakes - Cebu</title>
  <meta name="description" content="This page is not on The White Cakes - Cebu site. Return home or order a cake in Cebu City, Mandaue, or Lapu-Lapu.">
  <meta name="robots" content="noindex, follow">
  <link rel="stylesheet" href="/css/styles.css">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" sizes="180x180">
  <link rel="manifest" href="/site.webmanifest">
</head>
<body class="sub page-404">
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header" id="site-header">
    <a class="brand" href="/"><span class="wordmark">White Cakes</span></a>
  </header>
  <main id="main" class="article">
    <h1>This page isn’t on the bench</h1>
    <p class="dek">The link may be old, or the page moved when we added new cake and delivery guides.</p>
    <div class="hero-actions">
      <a class="btn" href="/">Back to home</a>
      <a class="btn btn-quiet" data-wa href=""" + json.dumps(WA_PREFILL) + """ rel="noopener noreferrer">WhatsApp</a>
    </div>
    <nav class="related-pages" aria-label="Helpful links">
      <p class="kicker">Try these</p>
      <ul>
        <li><a href="/bento-cakes-cebu/">Bento cakes</a></li>
        <li><a href="/faq/">FAQ</a></li>
        <li><a href="/journal/">Journal</a></li>
      </ul>
    </nav>
  </main>
  <script src="/js/main.js" defer></script>
</body>
</html>"""
    path.write_text(t, encoding="utf-8")


def generate_icons():
    from PIL import Image
    import cairosvg

    svg = ROOT / "assets/apple-touch-icon.svg"
    for size, name in [(192, "icon-192.png"), (512, "icon-512.png"), (32, "favicon-32.png")]:
        cairosvg.svg2png(url=str(svg), write_to=str(ROOT / "assets" / name), output_width=size, output_height=size)
    # favicon.ico from 32 and 16
    img32 = Image.open(ROOT / "assets/favicon-32.png")
    img16 = img32.resize((16, 16), Image.Resampling.LANCZOS)
    img32.save(ROOT / "favicon.ico", format="ICO", sizes=[(32, 32)])
    shutil.copy2(ROOT / "favicon.ico", ROOT / "assets/favicon.ico")
    # logo.jpg square 512 for manifest (overwrite og copy)
    cairosvg.svg2png(url=str(svg), write_to=str(ROOT / "assets/logo-512.png"), output_width=512, output_height=512)
    logo = Image.open(ROOT / "assets/logo-512.png").convert("RGB")
    logo.save(ROOT / "assets/logo.jpg", "JPEG", quality=90)

    manifest = {
        "name": "The White Cakes - Cebu",
        "short_name": "White Cakes",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#F8F4EC",
        "theme_color": "#F8F4EC",
        "lang": "en-PH",
        "icons": [
            {"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        ],
    }
    (ROOT / "site.webmanifest").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main():
    counts = patch_landings()
    fix_wa_labels(ROOT)
    patch_home_meta()
    patch_journal_index()
    patch_404()
    generate_icons()
    for slug, wc in sorted(counts.items()):
        print(f"{slug}: ~{wc} words")
    return counts


if __name__ == "__main__":
    main()