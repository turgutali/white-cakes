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
<h2>Choose a flavour</h2><p>Chocolate, vanilla, ube, mango, and red velvet are listed flavours. The flavour name does not promise a separate filling or topping; describe any specific expectation and we will confirm what is available for your date. See our <a href="../journal/choosing-a-flavor.html">Cebu cake flavour guide</a> if you are still comparing.</p>""",
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

# Extra sections so each landing prose block clears 350 words. Same voice as EXTENSIONS.
# Keep published launch prices. City pages stay about different roads and gates.
MORE = {
    "bento-cakes-cebu": """<h2>What to write in the message</h2><p>Date, flavour, and the line for the top are enough to start. Add whether you will collect in Cebu City or need the cake taken to Mandaue or Lapu-Lapu, and a landmark if someone else opens the door. A long sentence will not fit a 4-inch top; we will say so rather than crowd the rose. We reply within 24 hours. The longer note is <a href="../journal/what-is-a-bento-cake.html">what a bento cake is</a>.</p>""",
    "bouquet-cakes-cebu": """<h2>A line among the flowers</h2><p>There is room for a short inscription if you want one. Send the spelling exactly, including a name. A long paragraph will not sit cleanly on a floral top; we will say so in the reply and keep the piping clear. Home dinners, hotel handovers, and office desks in Cebu City, Mandaue, and Lapu-Lapu are the usual drops. If the bouquet is a surprise, name who should receive the delivery window. <a href="../journal/bouquet-cake-gift-cebu.html">Bouquet cakes as a gift</a> walks through that handover.</p>""",
    "custom-cakes-cebu": """<h2>Occasions on the same bench</h2><p>Birthdays, christenings, debuts, and small weddings start the same way: a calendar date, a flavour, and a brief we can pipe by hand. Say which occasion it is. The words on the cake and the hour it is cut change how we schedule the finish. A folder of screenshots is less useful than one clear photo plus the guest count. Read <a href="../journal/how-to-brief-a-custom-cake-cebu.html">how to brief a custom cake</a> before you send the reference.</p>""",
    "birthday-cakes-cebu": """<h2>First birthdays and debuts</h2><p>A first birthday and an 18th debut are not the same order. Tell us the venue, whether the cake is photographed before it is cut, and how many people will actually eat. Sinulog week and December weekends fill the bench earlier than an ordinary Saturday, so message sooner when your date sits on a holiday. The notes on <a href="../journal/first-birthday-sinulog-cake-cebu.html">first birthdays around Sinulog</a> and <a href="../journal/debut-cake-cebu.html">debut cakes</a> cover those calendars.</p><h2>Choose a flavour the guests enjoy</h2><p>The menu lists chocolate, vanilla, ube, mango, and red velvet. Ask the celebrant or family which flavour they want, then include it in the order. Flavour names do not promise a separate filling or topping; request confirmation if those details matter. Read the <a href="/journal/choosing-a-flavor.html">Cebu cake flavour guide</a> for what to confirm.</p>""",
    "anniversary-cakes-cebu": """<h2>Dinner for two or a family table</h2><p>A bento is enough when the anniversary is two plates and a quiet evening. A bouquet is the cake to send when it should arrive looking like flowers. Signature Marble holds a longer dinner where relatives share slices. Tell us the evening as a calendar date. We do not guess from “our anniversary” alone.</p><h2>What to put in the order</h2><p>Date, design, flavour, the line on top, and whether we deliver to a home or you collect in Cebu City. If the cake is a surprise at a condo or a restaurant, name the person who will meet the driver and a landmark they will recognise. We confirm a window, not a minute, and we reply within 24 hours. How you will pay is settled in that confirmation, not on this page.</p>""",
    "wedding-cakes-cebu": """<h2>What we will and will not promise</h2><p>We finish a buttercream cake for an intimate wedding, an engagement dinner, or a rehearsal. We do not staff a cutting table, and we do not build a ballroom display from a catalogue. If the guest list is a hall, send the number early. We will say whether the bench can do that date, or whether a smaller cake for the couple’s table is the honest answer. The longer guide is <a href="../journal/how-to-choose-wedding-cake-cebu.html">how to choose a wedding cake in Cebu</a>.</p>""",
    "corporate-cake-orders-cebu": """<h2>Client gifts and team days</h2><p>A single bouquet or marble cake suits a client meeting and a shared pantry. A set of bento cakes suits named desks when each person should have their own box. Send the count, the date, and whether flavours differ. We confirm what one bench day can finish. We do not promise a same-morning reorder if the list grows after the cakes are already piped.</p><h2>What a quotation means here</h2><p>Bento cakes are ₱449 each until January 15, 2027 (regular price ₱599). Other launch prices are on the home menu. Bouquet cakes are price on request. If procurement needs a written quote, ask on WhatsApp with the company name, the date, and the cakes. A 50% deposit confirms the order. We do not invent billing terms or lead times we have not agreed in that reply. The practical note is <a href="../journal/corporate-office-cakes-cebu.html">corporate and office cakes in Cebu</a>.</p>""",
    "cake-delivery-cebu-city": """<h2>Pins we can place from the note</h2><p>A useful Cebu City note names the barangay, the building or village phase, and a landmark a driver can see from the street. IT Park and Cebu Business Park towers need the tower name and who will come to the lobby. Talamban and the uphill barangays take longer at school-out than a Lahug condo near the kitchen. Say which kind of drop it is so the window matches the road. This page is the city itself. Bridge crossings to Mandaue and the island ride to Mactan are written up on their own delivery pages, because those gates and queues are different.</p>""",
    "cake-delivery-mandaue": """<h2>Reclamation, highway, and subdivisions</h2><p>Mandaue is a short hop from the Cebu City kitchen and a different kind of address. North Reclamation warehouses, plants along the highway, and gated villages near Subangdaku and Magellan do not share one gate routine. A factory may need a visitor slip and a bay number. A subdivision may need the phase, the block, and the name already on the guard’s list. A condo on U.N. Avenue needs the tower and a person who can come down. Write the one that matches your pin.</p><h2>A Mandaue window</h2><p>We still quote a range. Late-afternoon queues on the Mandaue–Cebu corridors and around the port shift the drop, but the landmark we need is the gate you actually use, not the word “Mandaue” by itself. If the cake is for an office pantry, say whether reception can receive it or whether a named employee should meet it. Three days’ notice still applies before we mix. Resort gates and island bridges are not this page; those notes live with Lapu-Lapu delivery.</p>""",
    "cake-delivery-lapu-lapu": """<h2>Why the window is wider on Mactan</h2><p>The cake still leaves a Cebu City kitchen. It then crosses to the island, by the Mactan–Mandaue bridges or the Cebu–Cordova link, before a resort gate, a village in Pusok, or a house toward Punta Engaño. That crossing is why an island window is a range with slack, especially in the late afternoon, in December, and during Sinulog. Tell us if a ceremony starts at a fixed hour. We will say whether that hour is realistic before we accept the date.</p><h2>The name on the gate</h2><p>Resorts and short-stay houses turn drivers away when the cake order names a different guest from the reservation. Put the booking name in the notes, plus a landmark after the gate: lobby, pool, or unit. A home in Maribago or along M.L. Quezon still needs a pin, not only the barangay. If the timing cannot survive the crossing, collect in Cebu City and tell us you are riding back yourself. City condos and Mandaue factory slips are a different handover; use those delivery pages when the pin is not on the island.</p>""",
}


def unescape_urls(html: str) -> str:
    return html.replace("https:\\/\\/", "https://").replace("\\/", "/")


def replace_prose(html: str, body: str) -> str:
    # Stop at the prose div. Journal cross-links sit between it and the aside.
    return re.sub(
        r'(<div class="prose">).*?(</div>)',
        lambda m: m.group(1) + "\n    " + body + "\n          " + m.group(2),
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
        body = COPY[slug] + EXTENSIONS.get(slug, "") + MORE.get(slug, "")
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
    if 'href="/favicon-96.png"' not in t:
        t = t.replace(
            '<link rel="apple-touch-icon"',
            '<link rel="icon" href="/favicon-96.png" type="image/png" sizes="96x96">\n  '
            '<link rel="icon" href="/favicon-48.png" type="image/png" sizes="48x48">\n  '
            '<link rel="icon" href="/favicon-192.png" type="image/png" sizes="192x192">\n  '
            '<link rel="icon" href="/favicon-512.png" type="image/png" sizes="512x512">\n  '
            '<link rel="icon" href="/favicon.ico" sizes="any">\n  '
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">',
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
  <!-- Google Tag Manager -->
  <script async src="https://www.googletagmanager.com/gtm.js?id=GTM-T4NPB5VF"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
  </script>
  <!-- End Google Tag Manager -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page not found | The White Cakes - Cebu</title>
  <meta name="description" content="This page is not on The White Cakes - Cebu site. Return home or order a cake in Cebu City, Mandaue, or Lapu-Lapu.">
  <meta name="robots" content="noindex, follow">
  <link rel="stylesheet" href="/css/styles.css">
  <link rel="icon" href="/favicon-96.png" type="image/png" sizes="96x96">
  <link rel="icon" href="/favicon-48.png" type="image/png" sizes="48x48">
  <link rel="icon" href="/favicon-192.png" type="image/png" sizes="192x192">
  <link rel="icon" href="/favicon-512.png" type="image/png" sizes="512x512">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
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
    """Full square favicon set. See scripts/apply_brand_seo.py."""
    from apply_brand_seo import generate_brand_icons, write_manifest

    generate_brand_icons()
    write_manifest()


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
