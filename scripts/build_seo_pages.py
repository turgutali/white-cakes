#!/usr/bin/env python3
"""Generate SEO landing pages for The White Cakes - Cebu (static HTML)."""
from __future__ import annotations

import json
import os
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.thewhitecakes.com"
TODAY = "2026-11-15"

MARK = (
    '<img class="mark" src="/logo-512.png" '
    'srcset="/favicon-96.png 96w, /favicon-192.png 192w, /logo-512.png 512w" '
    'sizes="44px" width="44" height="44" alt="The White Cakes - Cebu logo" decoding="async">'
)
FB = "https://www.facebook.com/profile.php?id=61596567450476"
ORG_ID = f"{BASE}/#organization"
ICON_LINKS = """
      <link rel="icon" href="/favicon.ico" sizes="48x48">
      <link rel="icon" href="/favicon-48.png" type="image/png" sizes="48x48">
      <link rel="icon" href="/favicon-96.png" type="image/png" sizes="96x96">
      <link rel="icon" href="/favicon-192.png" type="image/png" sizes="192x192">
      <link rel="icon" href="/favicon-512.png" type="image/png" sizes="512x512">
      <link rel="icon" href="/favicon.svg" type="image/svg+xml">
      <link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
      <link rel="manifest" href="/site.webmanifest">"""


def header(rel: str = "..") -> str:
    return dedent(
        f"""\
    <header class="site-header" id="site-header">
      <a class="brand" href="{rel}/index.html">
        {MARK}
        <span class="wordmark">White Cakes</span>
      </a>
      <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="primary-nav">Menu</button>
      <div class="header-end">
        <nav class="nav" id="primary-nav" aria-label="Primary">
          <a href="{rel}/index.html#collection">Collection</a>
          <a href="{rel}/index.html#occasions">Occasions</a>
          <a href="{rel}/journal/index.html">Journal</a>
          <a href="{rel}/faq/index.html">FAQ</a>
          <a href="{rel}/index.html#delivery">Delivery</a>
          <a href="{rel}/index.html#how">How to order</a>
        </nav>
        <a class="header-cta" href="{rel}/index.html#order">Order</a>
      </div>
    </header>"""
    )


def footer(rel: str = "..") -> str:
    return dedent(
        f"""\
    <footer class="site-footer">
      <div class="section-inner">
        <a class="brand brand-stack" href="{rel}/index.html">{MARK}<span class="wordmark">White Cakes</span></a>
        <ul class="footer-links">
          <li><a href="mailto:info@thewhitecakes.com">info@thewhitecakes.com</a></li>
          <li><a href="/about/">About</a></li>
          <li><a data-wa href="https://wa.me/639474382632" rel="noopener noreferrer">WhatsApp <span data-wa-label>+63 947 438 2632</span></a></li>
          <li><a data-ig href="https://www.instagram.com/thewhitecakescebu/" rel="noopener noreferrer">Instagram</a></li>
          <li><a data-fb href="{FB}" rel="noopener noreferrer">Facebook</a></li>
          <li><a href="{rel}/faq/index.html">FAQ</a></li>
          <li><a href="{rel}/journal/index.html">Journal</a></li>
        </ul>
        <p class="loc">Cebu City · Mandaue · Lapu-Lapu</p>
        <p class="legal">© 2026 The White Cakes - Cebu</p>
      </div>
    </footer>
    <nav class="dock" aria-label="Quick actions">
      <a href="{rel}/index.html#order">Order</a>
      <a data-wa href="https://wa.me/639474382632" rel="noopener noreferrer">WhatsApp</a>
    </nav>
    <script src="{rel}/js/main.js" defer></script>"""
    )


def page(
    slug: str,
    title: str,
    description: str,
    h1: str,
  dek: str,
    body_html: str,
    breadcrumb_label: str,
    og_image: str,
    extra_json_ld: list[dict] | None = None,
    robots: str = "index, follow, max-image-preview:large",
    related: list[tuple[str, str]] | None = None,
    figure: tuple[str, str, int, int, str] | None = None,
) -> str:
    canon = f"{BASE}/{slug}/"
    crumbs = [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
        {"@type": "ListItem", "position": 2, "name": breadcrumb_label, "item": canon},
    ]
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs}]
    if extra_json_ld:
        ld.extend(extra_json_ld)

    fig = ""
    if figure:
        src, alt, w, h, cap = figure
        fig = dedent(
            f"""\
        <figure class="landing-figure">
          <motion-div class="media-frame">
            <img src="../assets/{src}" width="{w}" height="{h}" alt="{alt}" loading="lazy" decoding="async">
          </div>
          <figcaption>{cap}</figcaption>
        </figure>"""
        ).replace("<motion-div", "<div").replace("</motion-div", "</div")

    related_html = ""
    if related:
        items = "\n".join(f'          <li><a href="../{s}/">{label}</a></li>' for s, label in related)
        related_html = f'<nav class="related-pages" aria-label="Related pages">\n        <p class="kicker">Related</p>\n        <ul>\n{items}\n        </ul>\n      </nav>'

    ld_scripts = "\n".join(
        f'  <script type="application/ld+json">\n{json.dumps(block, indent=2)}\n  </script>' for block in ld
    )

    return dedent(
        f"""\
    <!DOCTYPE html>
    <html lang="en-PH">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>{title}</title>
      <meta name="description" content="{description}">
      <link rel="canonical" href="{canon}">
      <meta name="robots" content="{robots}">
      <meta property="og:title" content="{title}">
      <meta property="og:description" content="{description}">
      <meta property="og:url" content="{canon}">
      <meta property="og:type" content="website">
      <meta property="og:site_name" content="The White Cakes - Cebu">
      <meta property="og:locale" content="en_PH">
      <meta property="og:image" content="{BASE}/assets/{og_image}">
      <meta name="twitter:card" content="summary_large_image">
      <meta name="twitter:title" content="{title}">
      <meta name="twitter:description" content="{description}">
      <meta name="twitter:image" content="{BASE}/assets/{og_image}">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Manrope:wght@400;500;600&display=swap">
      <link rel="stylesheet" href="../css/styles.css">
      {ICON_LINKS}
      {ld_scripts}
    </head>
    <body class="sub">
      <a class="skip" href="#main">Skip to content</a>
      {header()}
      <main id="main">
        <article class="article">
          <nav class="crumb" aria-label="Breadcrumb">
            <a href="../index.html">Home</a> · <span>{breadcrumb_label}</span>
          </nav>
          <h1>{h1}</h1>
          <p class="dek">{dek}</p>
          {fig}
          <div class="prose">
    {body_html}
          </div>
          <aside class="article-end">
            <p>Tell us your date. We confirm within a day.</p>
            <div class="hero-actions">
              <a class="btn" href="../index.html#order">Order Your Cake</a>
              <a class="btn btn-quiet" data-wa href="https://wa.me/639474382632" rel="noopener noreferrer">WhatsApp</a>
            </div>
          </aside>
          {related_html}
        </article>
      </main>
      {footer()}
    </body>
    </html>"""
    )


PAGES: list[dict] = []

def add(**kwargs):
    PAGES.append(kwargs)


def service_ld(*, name: str, description: str, image: str, url: str, service_type: str = "Custom cake") -> dict:
    """Service markup for a made-to-order cake. No price, offer, review, or rating."""
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "description": description,
        "image": [
            f"{BASE}/assets/crops/{url.rstrip('/').split('/')[-1]}-1x1.jpg",
            f"{BASE}/assets/crops/{url.rstrip('/').split('/')[-1]}-4x3.jpg",
            f"{BASE}/assets/crops/{url.rstrip('/').split('/')[-1]}-16x9.jpg",
            image,
        ],
        "serviceType": service_type,
        "url": url,
        "provider": {"@id": ORG_ID},
        "areaServed": [
            {"@type": "City", "name": "Cebu City"},
            {"@type": "City", "name": "Mandaue City"},
            {"@type": "City", "name": "Lapu-Lapu City"},
        ],
    }


add(
    slug="bento-cakes-cebu",
    title="Bento Cakes in Cebu | The White Cakes - Cebu",
    description="Order a 4-inch bento cake in Cebu — hand-piped buttercream for two, gifts, and small celebrations. Delivery in Cebu City, Mandaue, and Lapu-Lapu.",
    h1="Bento Cakes in Cebu",
    dek="A small cake finished like a full celebration — shells, a ribbon, one rose.",
    og_image="bento-cake-cebu.webp",
    breadcrumb_label="Bento cakes",
    figure=("bento-cake-cebu.webp", "A 4-inch bento cake with piped shells, blush ribbon, and one rose on ivory linen", 800, 800, "Bento cake, Cebu"),
    related=[("birthday-cakes-cebu", "Birthday cakes"), ("cake-delivery-cebu-city", "Cake delivery — Cebu City"), ("faq", "FAQ")],
    extra_json_ld=[service_ld(
        name="Bento Cake",
        description="4-inch hand-finished bento cake made to order in Cebu.",
        image=f"{BASE}/assets/bento-cake-cebu.webp",
        url=f"{BASE}/bento-cakes-cebu/",
    )],
    body_html=dedent(
        """\
        <p>Our bento cake is a 4-inch round finished in ivory buttercream with piped shells, a blush ribbon, and a single rose. It is made to order in our Cebu cloud kitchen — there is no walk-in counter and no case of cakes waiting.</p>
        <h2>Who it is for</h2>
        <p>Bento cakes suit two people sharing a table, a desk celebration, or a gift you will carry yourself. In Cebu traffic they are easier to move than a tall layer cake, and they cool quickly once you are home.</p>
        <h2>Flavors and words on top</h2>
        <p>Choose chocolate, vanilla, ube, mango, or red velvet when you order. Add a short line or a name on top — we pipe exactly what you send us, spelling included.</p>
        <h2>Lead time and delivery</h2>
        <p>We need at least three days before your date. Pickup is arranged after we confirm your order. We deliver to Cebu City, Mandaue, and Lapu-Lapu with a full address and someone to receive the cake.</p>"""
    ),
)

add(
    slug="bouquet-cakes-cebu",
    title="Bouquet Cakes in Cebu | The White Cakes - Cebu",
    description="Bouquet cakes in Cebu — piped blush roses and sage leaves on ivory buttercream. Gifts, anniversaries, and soft celebrations. Order three days ahead.",
    h1="Bouquet Cakes in Cebu",
    dek="Piped roses you can slice — a lower, softer silhouette than our marble cake.",
    og_image="bouquet-cake-cebu.webp",
    breadcrumb_label="Bouquet cakes",
    figure=("bouquet-cake-cebu.webp", "Bouquet cake with piped blush roses and sage leaves in Cebu", 800, 800, "Bouquet cake"),
    related=[("anniversary-cakes-cebu", "Anniversary cakes"), ("cake-delivery-mandaue", "Cake delivery — Mandaue"), ("custom-cakes-cebu", "Custom cakes")],
    extra_json_ld=[service_ld(
        name="Bouquet Cake",
        description="Hand-piped bouquet-style cake made to order in Cebu.",
        image=f"{BASE}/assets/bouquet-cake-cebu.webp",
        url=f"{BASE}/bouquet-cakes-cebu/",
    )],
    body_html=dedent(
        """\
        <p>The Bouquet Cake is ivory buttercream covered with piped blush roses and sage leaves. It reads as flowers you can cut — lower and softer than our Signature Marble cake.</p>
        <h2>Gifts and anniversaries</h2>
        <p>This is the cake we suggest when someone would rather receive flowers than a tall birthday tier. Send it across metro Cebu with a line on top and the name in your order notes.</p>
        <h2>Size and table</h2>
        <p>Tell us the size of the table or the number of guests if you know them. “Bouquet” describes the finish; we confirm the scale when we reply so the cake matches the setting.</p>
        <h2>Ordering</h2>
        <p>Message us at least three days before the date. Pickup or delivery in Cebu City, Mandaue, and Lapu-Lapu — full address and a receiver required for delivery.</p>"""
    ),
)

add(
    slug="custom-cakes-cebu",
    title="Custom Celebration Cakes in Cebu | The White Cakes - Cebu",
    description="Custom celebration cakes in Cebu, including Signature Marble with dusty-blue buttercream. Hand-finished, made to order. No storefront — pickup or delivery.",
    h1="Custom Celebration Cakes in Cebu",
    dek="Signature Marble and fully custom designs, baked for your date.",
    og_image="signature-marble-cake-cebu.webp",
    breadcrumb_label="Custom cakes",
    figure=("signature-marble-cake-cebu.webp", "Signature Marble cake with dusty-blue marbled buttercream and piped shell border", 800, 800, "Signature Marble"),
    related=[("wedding-cakes-cebu", "Wedding cakes"), ("corporate-cake-orders-cebu", "Corporate orders"), ("bento-cakes-cebu", "Bento cakes")],
    extra_json_ld=[service_ld(
        name="Custom Celebration Cake",
        description="Hand-finished custom and Signature Marble cakes in Cebu.",
        image=f"{BASE}/assets/signature-marble-cake-cebu.webp",
        url=f"{BASE}/custom-cakes-cebu/",
    )],
    body_html=dedent(
        """\
        <p>Every cake leaves our Cebu kitchen made for the date you name. Custom orders can follow your reference photo; our Signature Marble is the house 6-inch design in ivory cream with dusty-blue marble, a shell border, and one rose.</p>
        <h2>Signature Marble</h2>
        <p>The marble cake belongs at the centre of a small table — birthdays, family dinners, and celebrations where everyone is served from one centerpiece. Room on top for a name or a short line.</p>
        <h2>Fully custom</h2>
        <p>If the day needs a different palette, flower, or shape, choose Custom on the order form and describe the mood. Upload a photo if you have one — it helps most when the design is new to us.</p>
        <h2>Process</h2>
        <p>We need three days’ notice minimum. We reply within 24 hours with confirmation or a question. There is no street counter; pickup time and delivery windows are agreed when we confirm.</p>"""
    ),
)

# Occasion pages
for slug, title_suffix, h1, dek, body, rel, img in [
    (
        "birthday-cakes-cebu",
        "Birthday Cakes in Cebu",
        "Birthday Cakes in Cebu",
        "Ivory buttercream and a name on top — baked for the actual day, not pulled from a case.",
        """<p>Birthday cakes from our Cebu kitchen are mixed and piped for the date you send us. The Signature Marble 6-inch is the usual choice when several people will share one table.</p>
        <h2>What to send us</h2>
        <p>Name, mobile number, cake design, flavor, and the words for the top — spelled exactly as you want them piped. We need at least three days before the party.</p>
        <h2>Smaller birthdays</h2>
        <p>For two guests or a quiet celebration, a bento cake travels more easily through Cebu traffic and still carries shells, a ribbon, and a rose.</p>
        <h2>Delivery</h2>
        <p>We deliver across Cebu City, Mandaue, and Lapu-Lapu when someone can receive the cake at the door.</p>""",
        [("custom-cakes-cebu", "Custom & Marble cakes"), ("bento-cakes-cebu", "Bento cakes"), ("faq", "FAQ")],
        "signature-marble-cake-cebu.webp",
    ),
    (
        "anniversary-cakes-cebu",
        "Anniversary Cakes in Cebu",
        "Anniversary Cakes in Cebu",
        "Soft piped roses or calm ivory marble — made to order, not from a display shelf.",
        """<p>Anniversaries often call for the Bouquet Cake: blush roses and sage leaves on ivory buttercream, low enough for an intimate table. For a longer dinner with family, the Signature Marble still carries a single rose and a clean name line on top.</p>
        <h2>Timing</h2>
        <p>Order at least three days ahead so the cake is baked for your evening, not rushed on the bench.</p>
        <h2>Gifting</h2>
        <p>We can deliver within metro Cebu when you provide a full address, landmark, and a mobile number for the person opening the door.</p>
        <h2>Flavors</h2>
        <p>Chocolate, vanilla, ube, mango, or red velvet — pick what suits the meal you have planned.</p>""",
        [("bouquet-cakes-cebu", "Bouquet cakes"), ("cake-delivery-lapu-lapu", "Delivery — Lapu-Lapu"), ("faq", "FAQ")],
        "bouquet-cake-cebu.webp",
    ),
    (
        "wedding-cakes-cebu",
        "Wedding Cakes in Cebu",
        "Wedding Cakes in Cebu",
        "Small wedding and engagement cakes finished by hand — tell us the guest count and the mood.",
        """<p>We are a made-to-order cloud kitchen in Cebu, not a hotel pastry shop with tiers on display. For intimate weddings and engagement dinners we finish buttercream cakes to your brief — often Signature Marble or a custom design with your palette.</p>
        <h2>Planning</h2>
        <p>Send your date, guest count, and any reference photos. Larger tiers need more bench time; message us early so we can say honestly what the date allows.</p>
        <h2>Delivery and setup</h2>
        <p>We deliver within Cebu City, Mandaue, and Lapu-Lapu. We do not provide on-site cutting service; message us and we will confirm what we can do for your venue.</p>
        <h2>Style</h2>
        <p>Ivory, dusty blue, blush, and sage piped by hand — no printed sheets. If you need a tasting, message us and we will confirm whether one is possible on your timeline.</p>""",
        [("custom-cakes-cebu", "Custom cakes"), ("corporate-cake-orders-cebu", "Corporate cakes"), ("faq", "FAQ")],
        "hero-celebration-cake-cebu.webp",
    ),
    (
        "corporate-cake-orders-cebu",
        "Corporate Cake Orders in Cebu",
        "Corporate Cake Orders in Cebu",
        "Client gifts, team milestones, and office celebrations — one invoice, one delivery window.",
        """<p>Offices in Cebu City, Mandaue, and Lapu-Lapu order from us when they need a finished cake at a reception desk or a boardroom — not cupcakes from a mall counter.</p>
        <h2>What we need</h2>
        <p>Company name, contact mobile, delivery address with landmarks, date, and quantity if you are ordering more than one cake. Lead time is still at least three days per order unless we tell you otherwise.</p>
        <h2>Design</h2>
        <p>Logo colours can inspire a custom finish, but we pipe by hand; send reference images. Bento sizes work for individual desks; larger tables suit Signature Marble or bouquet finishes.</p>
        <h2>Payment</h2>
        <p>Payment method is confirmed upon order when we reply — message us if you need a formal quotation.</p>""",
        [("custom-cakes-cebu", "Custom cakes"), ("cake-delivery-cebu-city", "Delivery — Cebu City"), ("faq", "FAQ")],
        "cake-slice-cebu.webp",
    ),
]:
    add(
        slug=slug,
        title=f"{title_suffix} | The White Cakes - Cebu",
        description=f"{title_suffix} — hand-finished buttercream, made to order. Pickup or delivery across metro Cebu. Order at least three days ahead.",
        h1=h1,
        dek=dek,
        og_image=img,
        breadcrumb_label=title_suffix,
        figure=(img, f"{h1} by The White Cakes - Cebu", 800, 800, title_suffix),
        related=[(r[0].replace("/index.html", ""), r[1]) if r[0].startswith("journal") else (r[0], r[1]) for r in rel],
        body_html=body,
    )

add(
    slug="cake-delivery-cebu-city",
    title="Cake Delivery in Cebu City | The White Cakes - Cebu",
    description="Buttercream cake delivery in Cebu City — Lahug, Banilad, Capitol, IT Park, and downtown. Made to order; three days' notice.",
    h1="Cake Delivery in Cebu City",
    dek="From Lahug and IT Park to downtown and the port area — agreed windows, not exact minutes.",
    og_image="hero-celebration-cake-cebu.webp",
    breadcrumb_label="Cebu City delivery",
    related=[("cake-delivery-mandaue", "Mandaue delivery"), ("bento-cakes-cebu", "Bento cakes"), ("journal/how-to-order.html", "How to order")],
    body_html=dedent(
        """\
        <p>We deliver hand-finished cakes within Cebu City from our cloud kitchen. There is no storefront to visit; we confirm a delivery window when your order is accepted.</p>
        <h2>Areas we often serve</h2>
        <p>Lahug, IT Park, Banilad, Capitol Site, Mabolo, Ayala vicinity, downtown Cebu City, and barangays along the usual north–south corridors. If you are unsure, send the barangay and a landmark in the order form.</p>
        <h2>What to include</h2>
        <p>Full address, condo or village gate instructions, and a mobile number for whoever will receive the cake. Buttercream needs shade and a flat ride — not a lap in midday heat.</p>
        <h2>Lead time</h2>
        <p>Same rule as pickup: at least three days before the date. Traffic from our kitchen to your pin moves in ranges; we agree the range in our confirmation message.</p>"""
    ),
)

add(
    slug="cake-delivery-mandaue",
    title="Cake Delivery in Mandaue | The White Cakes - Cebu",
    description="Cake delivery to Mandaue City — U.N. Avenue, North Reclamation, Subangdaku, and Magellan. Made-to-order buttercream cakes from Cebu.",
    h1="Cake Delivery in Mandaue",
    dek="Across the Mandaue–Cebu bridge with the same three-day bench schedule.",
    og_image="bouquet-cake-cebu.webp",
    breadcrumb_label="Mandaue delivery",
    related=[("cake-delivery-cebu-city", "Cebu City delivery"), ("anniversary-cakes-cebu", "Anniversary cakes"), ("faq", "FAQ")],
    body_html=dedent(
        """\
        <p>Mandaue orders share our Cebu production schedule. Cakes are baked for your date, crumb-coated, and piped after the cream sets — so we do not accept next-day requests.</p>
        <h2>Neighborhoods</h2>
        <p>We regularly deliver toward North Reclamation Area, U.N. Avenue, Subangdaku, Magellan, and subdivisions along the coastal highway toward Consolacion. Send the exact pin and a landmark we can read from the road.</p>
        <h2>Receiving the cake</h2>
        <p>Someone must meet the driver at the gate or lobby. If nobody answers, the cake waits in a warm vehicle — the scenario we are trying to avoid.</p>
        <h2>Pickup alternative</h2>
        <p>If your schedule is tight, ask for pickup in Cebu City instead and collect as close to serving time as you can.</p>"""
    ),
)

add(
    slug="cake-delivery-lapu-lapu",
    title="Cake Delivery in Lapu-Lapu | The White Cakes - Cebu",
    description="Cake delivery to Lapu-Lapu and Mactan — Maribago, Pusok, and Mactan Newtown area. Hand-piped cakes, three days ahead.",
    h1="Cake Delivery in Lapu-Lapu",
    dek="Mactan deliveries with buffer for bridge traffic and resort gate checks.",
    og_image="piped-roses-cake-cebu.webp",
    breadcrumb_label="Lapu-Lapu delivery",
    related=[("cake-delivery-mandaue", "Mandaue delivery"), ("wedding-cakes-cebu", "Wedding cakes"), ("bento-cakes-cebu", "Bento cakes")],
    body_html=dedent(
        """\
        <p>Lapu-Lapu and Mactan Island sit across the bridges from our Cebu kitchen. We deliver when the date allows enough bench time and when you can receive the cake at a resort, village, or condo gate.</p>
        <h2>Common pins</h2>
        <p>Maribago, Pusok, Mactan Newtown, Punta Engaño approach roads, and barangays along the M.L. Quezon corridor. Resort deliveries need the guest name on the order notes so security can match the delivery.</p>
        <h2>Travel time</h2>
        <p>Bridge traffic is variable. We quote a window, not a minute-precise time. Bento cakes handle a longer ride more easily than a tall marble tier — mention your transport when you order.</p>
        <h2>Heat</h2>
        <p>Island afternoons are hot. Receive the cake into air-conditioning when you can, and read our journal note on buttercream in Cebu heat linked from the home page.</p>"""
    ),
)


def main():
    for p in PAGES:
        out_dir = ROOT / p["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        html = page(**p)
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        print("wrote", out_dir / "index.html")


if __name__ == "__main__":
    main()