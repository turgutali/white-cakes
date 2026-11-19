#!/usr/bin/env python3
"""Favicons, logos, and brand structured data for The White Cakes - Cebu.

Generates the square icon set from the owner's supplied logo and patches every
HTML page so Google can crawl a stable favicon, one Organization+Bakery entity,
and service images. Cake requests are quote-and-date based, so this script strips
Product markup that could incorrectly imply a single-SKU online checkout.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from html import escape, unescape
from pathlib import Path
from typing import TYPE_CHECKING
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape as xml_escape

if TYPE_CHECKING:
    from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.thewhitecakes.com"
ORG_ID = f"{BASE}/#organization"
SITE_ID = f"{BASE}/#website"
TODAY = date.today().isoformat()
NAVY = (0x1B, 0x23, 0x40, 255)
IVORY = (0xF8, 0xF4, 0xEC, 255)
FB = "https://www.facebook.com/profile.php?id=61596567450476"
IG = "https://www.instagram.com/thewhitecakescebu/"
MYCEBU = "https://mycebu.directory/business/the-white-cakes-cebu"
EMAIL = "info@thewhitecakes.com"
OLD_FB = "https://www.facebook.com/thewhitecakes/"

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FONT_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"

LOGO_IMG = (
    '<img class="mark" src="/logo-512.png" '
    'srcset="/favicon-48.png 48w, /favicon-96.png 96w, /favicon-192.png 192w, /logo-512.png 512w" '
    'sizes="44px" width="44" height="44" alt="The White Cakes - Cebu logo" decoding="async">'
)

ICON_LINKS = """  <link rel="icon" href="/favicon-96.png" type="image/png" sizes="96x96">
  <link rel="icon" href="/favicon-48.png" type="image/png" sizes="48x48">
  <link rel="icon" href="/favicon-192.png" type="image/png" sizes="192x192">
  <link rel="icon" href="/favicon-512.png" type="image/png" sizes="512x512">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
  <link rel="manifest" href="/site.webmanifest">"""

AREAS = [
    {"@type": "City", "name": "Cebu City"},
    {"@type": "City", "name": "Mandaue City"},
    {"@type": "City", "name": "Lapu-Lapu City"},
]

# Service pages: name, serviceType, and real cake photos already in assets/.
SERVICES: dict[str, dict] = {
    "bento-cakes-cebu/index.html": {
        "name": "Bento Cake",
        "serviceType": "Bento cake",
        "sources": ["bento-cake-cebu.webp", "bento.webp"],
    },
    "bouquet-cakes-cebu/index.html": {
        "name": "Bouquet Cake",
        "serviceType": "Bouquet cake",
        "sources": [
            "bouquet-cake-cebu.webp",
            "bouquet-cake-pink-wrapper-cebu.webp",
            "bouquet-cake-studio-cebu.webp",
            "piped-roses-cake-cebu.webp",
        ],
    },
    "custom-cakes-cebu/index.html": {
        "name": "Custom Celebration Cake",
        "serviceType": "Custom celebration cake",
        "sources": ["signature-marble-cake-cebu.webp", "hero-celebration-cake-cebu.webp", "cake-slice-cebu.webp", "marble.webp"],
    },
    "birthday-cakes-cebu/index.html": {
        "name": "Birthday Cake",
        "serviceType": "Birthday cake",
        "sources": ["signature-marble-cake-cebu.webp", "hero-celebration-cake-cebu.webp", "bento-cake-cebu.webp", "cake-slice-cebu.webp"],
    },
    "anniversary-cakes-cebu/index.html": {
        "name": "Anniversary Cake",
        "serviceType": "Anniversary cake",
        "sources": ["bouquet-cake-cebu.webp", "bouquet-cake-studio-cebu.webp", "signature-marble-cake-cebu.webp", "piped-roses-cake-cebu.webp"],
    },
    "wedding-cakes-cebu/index.html": {
        "name": "Wedding Cake",
        "serviceType": "Wedding cake",
        "sources": ["hero-celebration-cake-cebu.webp", "signature-marble-cake-cebu.webp", "piped-roses-cake-cebu.webp", "cake-slice-cebu.webp"],
    },
    "corporate-cake-orders-cebu/index.html": {
        "name": "Corporate Cake Order",
        "serviceType": "Corporate cake order",
        "sources": ["cake-slice-cebu.webp", "bento-cake-cebu.webp", "bouquet-cake-cebu.webp", "signature-marble-cake-cebu.webp"],
    },
    "cake-delivery-cebu-city/index.html": {
        "name": "Cake Delivery in Cebu City",
        "serviceType": "Cake delivery",
        "sources": ["hero-celebration-cake-cebu.webp", "signature-marble-cake-cebu.webp", "cake-slice-cebu.webp"],
    },
    "cake-delivery-mandaue/index.html": {
        "name": "Cake Delivery in Mandaue City",
        "serviceType": "Cake delivery",
        "sources": ["bouquet-cake-cebu.webp", "bouquet-cake-pink-wrapper-cebu.webp", "bouquet-cake-studio-cebu.webp"],
    },
    "cake-delivery-lapu-lapu/index.html": {
        "name": "Cake Delivery in Lapu-Lapu City",
        "serviceType": "Cake delivery",
        "sources": ["piped-roses-cake-cebu.webp", "hero-celebration-cake-cebu.webp", "bouquet-cake-cebu.webp"],
    },
}

COLLECTION = [
    ("Signature Marble", f"{BASE}/custom-cakes-cebu/"),
    ("Bouquet Cake", f"{BASE}/bouquet-cakes-cebu/"),
    ("Bento Cake", f"{BASE}/bento-cakes-cebu/"),
    ("Birthday Cake", f"{BASE}/birthday-cakes-cebu/"),
    ("Anniversary Cake", f"{BASE}/anniversary-cakes-cebu/"),
    ("Wedding Cake", f"{BASE}/wedding-cakes-cebu/"),
    ("Corporate Cake Order", f"{BASE}/corporate-cake-orders-cebu/"),
    ("Cake Delivery in Cebu City", f"{BASE}/cake-delivery-cebu-city/"),
    ("Cake Delivery in Mandaue City", f"{BASE}/cake-delivery-mandaue/"),
    ("Cake Delivery in Lapu-Lapu City", f"{BASE}/cake-delivery-lapu-lapu/"),
]

SITEMAP_PAGES = [
    ("/", "weekly", "1.0"),
    ("/bento-cakes-cebu/", "monthly", "0.9"),
    ("/bouquet-cakes-cebu/", "monthly", "0.9"),
    ("/custom-cakes-cebu/", "monthly", "0.9"),
    ("/birthday-cakes-cebu/", "monthly", "0.85"),
    ("/anniversary-cakes-cebu/", "monthly", "0.85"),
    ("/wedding-cakes-cebu/", "monthly", "0.85"),
    ("/corporate-cake-orders-cebu/", "monthly", "0.85"),
    ("/cake-delivery-cebu-city/", "monthly", "0.85"),
    ("/cake-delivery-mandaue/", "monthly", "0.85"),
    ("/cake-delivery-lapu-lapu/", "monthly", "0.85"),
    ("/christmas-cakes-cebu/", "weekly", "0.9"),
    ("/order/", "monthly", "0.95"),
    ("/about/", "monthly", "0.8"),
    ("/ordering/", "monthly", "0.8"),
    ("/faq/", "monthly", "0.8"),
    ("/journal/", "weekly", "0.8"),
    ("/privacy/", "yearly", "0.2"),
]


def glyph_group(font_path: str, char: str, font_px: float, x: float, baseline: float) -> tuple[str, float]:
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.ttLib import TTFont

    font = TTFont(font_path)
    glyphs = font.getGlyphSet()
    name = font.getBestCmap()[ord(char)]
    glyph = glyphs[name]
    pen = SVGPathPen(glyphs)
    glyph.draw(pen)
    scale = font_px / font["head"].unitsPerEm
    path = pen.getCommands()
    group = (
        f'<g transform="translate({x:.2f} {baseline:.2f}) scale({scale:.6f} {-scale:.6f})">'
        f'<path d="{path}" fill="#F8F4EC"/></g>'
    )
    return group, glyph.width * scale


def build_logo_svg() -> str:
    """Legacy vector generator; published raster assets use the owner's supplied logo."""
    w_group, w_adv = glyph_group(FONT_BOLD, "W", 82, 16, 124)
    c_group, _ = glyph_group(FONT_ITALIC, "C", 76, 16 + w_adv - 6, 120)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180" width="180" height="180" role="img" aria-label="The White Cakes - Cebu logo">
  <rect width="180" height="180" rx="34" fill="#1B2340"/>
  {w_group}
  {c_group}
  <g fill="none" stroke="#F8F4EC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M48 92c.8-16 .2-30-1-48"/>
    <path d="M46.5 42c-3.8-7.5 3.2-14.5 8.5-8 2.6 3.8.8 7.8-3.5 8.5"/>
  </g>
</svg>
"""


def render_master(svg: str) -> Image.Image:
    import cairosvg
    from io import BytesIO
    from PIL import Image

    png = cairosvg.svg2png(bytestring=svg.encode("utf-8"), output_width=1024, output_height=1024)
    return Image.open(BytesIO(png)).convert("RGBA")


def save_png(im: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, format="PNG", optimize=True)


def generate_brand_icons() -> Image.Image:
    from PIL import Image

    master = Image.open(ROOT / "assets" / "white-cakes-logo.png").convert("RGBA")

    def sized(px: int) -> Image.Image:
        return master.resize((px, px), Image.Resampling.LANCZOS)

    icons = {px: sized(px) for px in (16, 32, 48, 96, 180, 192, 512)}
    save_png(icons[48], ROOT / "favicon-48.png")
    save_png(icons[96], ROOT / "favicon-96.png")
    save_png(icons[192], ROOT / "favicon-192.png")
    save_png(icons[512], ROOT / "favicon-512.png")
    save_png(icons[512], ROOT / "logo-512.png")
    save_png(icons[180], ROOT / "apple-touch-icon.png")
    save_png(icons[192], ROOT / "assets" / "icon-192.png")
    save_png(icons[512], ROOT / "assets" / "icon-512.png")
    save_png(icons[512], ROOT / "assets" / "logo-512.png")
    save_png(icons[180], ROOT / "assets" / "apple-touch-icon.png")
    save_png(icons[32], ROOT / "assets" / "favicon-32.png")

    # Multi-resolution ICO. Pillow stores every size passed in `sizes`.
    icons[48].save(
        ROOT / "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
        append_images=[icons[16], icons[32]],
    )
    (ROOT / "assets" / "favicon.ico").write_bytes((ROOT / "favicon.ico").read_bytes())

    # Legacy JPEG logo on white, so the old URL still shows the mark.
    jpg = Image.new("RGB", (512, 512), (255, 255, 255))
    jpg.paste(icons[512], (0, 0), icons[512])
    jpg.save(ROOT / "assets" / "logo.jpg", format="JPEG", quality=92, optimize=True)
    return master


def write_manifest() -> None:
    manifest = {
        "name": "The White Cakes - Cebu",
        "short_name": "White Cakes",
        "description": "Made-to-order cakes from a cloud kitchen in Lahug, Cebu. Delivery in Cebu City, Mandaue City, and Lapu-Lapu City.",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#F8F4EC",
        "theme_color": "#F8F4EC",
        "lang": "en-PH",
        "icons": [
            {"src": "/favicon-48.png", "sizes": "48x48", "type": "image/png", "purpose": "any"},
            {"src": "/favicon-96.png", "sizes": "96x96", "type": "image/png", "purpose": "any"},
            {"src": "/favicon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/favicon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        ],
    }
    (ROOT / "site.webmanifest").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def open_rgb(path: Path) -> Image.Image:
    from PIL import Image

    im = Image.open(path)
    if im.mode in ("RGBA", "LA"):
        base = Image.new("RGB", im.size, IVORY[:3])
        base.paste(im, mask=im.split()[-1])
        return base
    return im.convert("RGB")


def crop_aspect(im: Image.Image, aw: int, ah: int, max_edge: int = 1600) -> Image.Image:
    from PIL import Image

    w, h = im.size
    target = aw / ah
    if w / h > target:
        new_w = int(round(h * target))
        left = (w - new_w) // 2
        box = (left, 0, left + new_w, h)
    else:
        new_h = int(round(w / target))
        top = max(0, (h - new_h) // 2)
        box = (0, top, w, top + new_h)
    cropped = im.crop(box)
    cw, ch = cropped.size
    scale = min(1.0, max_edge / max(cw, ch))
    if scale < 1:
        cropped = cropped.resize((int(cw * scale), int(ch * scale)), Image.Resampling.LANCZOS)
    return cropped


def save_jpeg(im: Image.Image, path: Path) -> tuple[int, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, format="JPEG", quality=86, optimize=True, progressive=True)
    return im.size


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate_crops() -> dict[str, list[dict]]:
    """Return service-relative path -> list of ImageObject dicts."""
    from PIL import Image

    crops_dir = ROOT / "assets" / "crops"
    crops_dir.mkdir(parents=True, exist_ok=True)
    out: dict[str, list[dict]] = {}

    def add_original(objects: list[dict], filename: str) -> None:
        path = ROOT / "assets" / filename
        if not path.exists():
            return
        with Image.open(path) as im:
            w, h = im.size
        objects.append(image_object(f"{BASE}/assets/{filename}", w, h))

    for rel, spec in SERVICES.items():
        slug = rel.split("/")[0]
        sources = [name for name in spec["sources"] if (ROOT / "assets" / name).exists()]
        if not sources:
            raise SystemExit(f"no photos for {rel}")
        primary = open_rgb(ROOT / "assets" / sources[0])
        objects: list[dict] = []
        for label, aw, ah in (("1x1", 1, 1), ("4x3", 4, 3), ("16x9", 16, 9)):
            cropped = crop_aspect(primary, aw, ah)
            w, h = save_jpeg(cropped, crops_dir / f"{slug}-{label}.jpg")
            if w * h < 50000:
                print(f"warning: {slug}-{label} is {w}x{h} ({w * h} px)")
            objects.append(image_object(f"{BASE}/assets/crops/{slug}-{label}.jpg", w, h))
        local_seen = set()
        for name in sources:
            digest = file_hash(ROOT / "assets" / name)
            if digest in local_seen:
                continue
            local_seen.add(digest)
            add_original(objects, name)
        out[rel] = objects

    # Brand crops used on the homepage Bakery image (1x1, 4x3, 16x9).
    brand_sources = {
        "1x1": "signature-marble-cake-cebu.webp",
        "4x3": "cake-slice-cebu.webp",
        "16x9": "hero-celebration-cake-cebu.webp",
    }
    brand_images = [
        image_object(f"{BASE}/assets/white-cakes-logo.png", 1024, 1024),
    ]
    for label, (aw, ah) in (("1x1", (1, 1)), ("4x3", (4, 3)), ("16x9", (16, 9))):
        cropped = crop_aspect(open_rgb(ROOT / "assets" / brand_sources[label]), aw, ah)
        w, h = save_jpeg(cropped, crops_dir / f"brand-{label}.jpg")
        brand_images.append(image_object(f"{BASE}/assets/crops/brand-{label}.jpg", w, h))
    with Image.open(ROOT / "assets" / "og.webp") as og:
        brand_images.append(image_object(f"{BASE}/assets/og.webp", og.size[0], og.size[1]))
    out["__brand__"] = brand_images
    return out


def image_object(url: str, width: int, height: int) -> dict:
    return {
        "@type": "ImageObject",
        "url": url,
        "contentUrl": url,
        "width": width,
        "height": height,
    }


def logo_object() -> dict:
    return {
        "@type": "ImageObject",
        "@id": f"{BASE}/#logo",
        "url": f"{BASE}/assets/white-cakes-logo.png",
        "contentUrl": f"{BASE}/assets/white-cakes-logo.png",
        "width": 1024,
        "height": 1024,
        "caption": "The White Cakes - Cebu logo",
    }


def organization_entity(images: list[dict]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": ["Organization", "Bakery"],
        "@id": ORG_ID,
        "name": "The White Cakes - Cebu",
        "legalName": "THE WHTE CAKES SHOP",
        "identifier": {
            "@type": "PropertyValue",
            "propertyID": "DTI Business Name Number",
            "value": "8628157",
        },
        "alternateName": ["White Cakes", "The White Cakes", "thewhitecakes.com"],
        "url": f"{BASE}/",
        "logo": logo_object(),
        "image": images,
        "description": (
            "The White Cakes - Cebu is a DTI-registered business name and made-to-order cloud kitchen in Lahug, Cebu. "
            "There is no storefront and no walk-in counter, and the street address is not published. "
            "Signature Marble, bouquet, bento, and custom buttercream cakes are baked for a named date, "
            "with at least three days' notice, for pickup by arrangement or delivery in Cebu City, Mandaue City, and Lapu-Lapu City."
        ),
        "email": EMAIL,
        "telephone": "+63-947-438-2632",
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "customer service",
            "email": EMAIL,
            "telephone": "+63-947-438-2632",
            "areaServed": "PH",
            "availableLanguage": "English",
        },
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Cebu City",
            "addressRegion": "Cebu",
            "postalCode": "6000",
            "addressCountry": "PH",
        },
        "areaServed": AREAS,
        "sameAs": [FB, IG, MYCEBU],
    }


def website_entity() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": SITE_ID,
        "name": "The White Cakes - Cebu",
        "alternateName": ["White Cakes", "The White Cakes", "thewhitecakes.com"],
        "url": f"{BASE}/",
        "inLanguage": "en-PH",
        "publisher": {"@id": ORG_ID},
    }


def collection_itemlist() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "The White Cakes collection",
        "description": "Made-to-order cakes and delivery across Cebu City, Mandaue City, and Lapu-Lapu City.",
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "numberOfItems": len(COLLECTION),
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": name, "url": url, "item": url}
            for i, (name, url) in enumerate(COLLECTION, start=1)
        ],
    }


def types_of(node) -> set[str]:
    found: set[str] = set()

    def walk(value) -> None:
        if isinstance(value, dict):
            t = value.get("@type")
            if isinstance(t, str):
                found.add(t)
            elif isinstance(t, list):
                found.update(x for x in t if isinstance(x, str))
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(node)
    return found


def is_our_org(node: dict) -> bool:
    t = node.get("@type")
    types = t if isinstance(t, list) else [t]
    name = str(node.get("name") or "")
    return bool(set(types) & {"Organization", "Bakery", "LocalBusiness"}) or "White Cakes" in name or node.get("@id") == ORG_ID


def clean_node(node):
    if isinstance(node, list):
        cleaned = []
        for item in node:
            item = clean_node(item)
            if item is not None:
                cleaned.append(item)
        return cleaned
    if not isinstance(node, dict):
        return node
    t = node.get("@type")
    types = set(t if isinstance(t, list) else [t])
    # Custom, date-based cake orders are confirmed after a quote, not bought
    # through a single-SKU online checkout. Keep service and article markup.
    if "Product" in types:
        return None
    if types & {"AggregateOffer", "AggregateRating", "Review", "Rating"}:
        raise SystemExit(f"refusing disallowed type {types}")
    for bad in ("lowPrice", "highPrice", "priceRange", "aggregateRating", "review", "reviewRating"):
        node.pop(bad, None)
    for key in ("publisher", "author", "provider"):
        val = node.get(key)
        if isinstance(val, dict) and (is_our_org(val) or val.get("@id") == ORG_ID):
            node[key] = {"@id": ORG_ID}
        elif isinstance(val, (dict, list)):
            node[key] = clean_node(val)
    for key, val in list(node.items()):
        if key in ("publisher", "author", "provider"):
            continue
        if isinstance(val, (dict, list)):
            node[key] = clean_node(val)
    if "@graph" in node and not node["@graph"]:
        return None
    node_type = node.get("@type")
    if node_type in ("FAQPage", "Blog", "BlogPosting", "Service", "AboutPage", "WebPage") and "publisher" not in node:
        node["publisher"] = {"@id": ORG_ID}
    if node_type == "BlogPosting" and "author" not in node:
        node["author"] = {"@id": ORG_ID}
    return node


def apply_service(node, spec: dict, images: list[dict], canon: str, description: str):
    if isinstance(node, list):
        for item in node:
            apply_service(item, spec, images, canon, description)
        return
    if not isinstance(node, dict):
        return
    t = node.get("@type")
    types = t if isinstance(t, list) else [t]
    if "Service" in types:
        node["name"] = spec["name"]
        node["description"] = description
        node["serviceType"] = spec["serviceType"]
        node["url"] = canon
        node["image"] = images
        node["provider"] = {"@id": ORG_ID}
        node["areaServed"] = AREAS
        node.pop("offers", None)
    for val in node.values():
        if isinstance(val, (dict, list)):
            apply_service(val, spec, images, canon, description)


def json_script(data: dict) -> str:
    body = json.dumps(data, indent=2, ensure_ascii=False)
    return f'  <script type="application/ld+json">\n{body}\n  </script>'


def strip_jsonld(html: str) -> str:
    return re.sub(r"\s*<script type=\"application/ld\+json\">.*?</script>", "", html, flags=re.S)


def replace_jsonld(html: str, mutator) -> str:
    def repl(match: re.Match) -> str:
        data = json.loads(match.group(2))
        data = mutator(data)
        if data is None:
            return ""
        body = json.dumps(data, indent=2, ensure_ascii=False)
        return f"{match.group(1)}\n{body}\n  {match.group(3)}"

    return re.sub(
        r'(<script type="application/ld\+json">)(.*?)(</script>)',
        repl,
        html,
        flags=re.S,
    )


def ensure_icon_links(html: str) -> str:
    html = re.sub(
        r'\s*<link\b[^>]*\brel="(?:shortcut icon|icon|apple-touch-icon|apple-touch-icon-precomposed|manifest)"[^>]*>',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(r'\s*<link\b[^>]*\bhref="data:image/[^"]*"[^>]*>', "", html)
    return html.replace("</head>", ICON_LINKS + "\n</head>", 1)


def ensure_logos(html: str) -> str:
    html = re.sub(r"<svg class=\"mark\"[\s\S]*?</svg>", LOGO_IMG, html)

    def brand_repl(match: re.Match) -> str:
        block = match.group(0)
        if 'class="mark"' in block:
            return block
        return block.replace(">", ">" + LOGO_IMG, 1)

    html = re.sub(r'<a class="brand[^"]*"[^>]*>[\s\S]*?</a>', brand_repl, html)
    return html


def meta_content(html: str, attr: str, key: str) -> str | None:
    patterns = [
        rf'<meta\s+{attr}="{re.escape(key)}"\s+content="([^"]*)"',
        rf'<meta\s+content="([^"]*)"\s+{attr}="{re.escape(key)}"',
    ]
    for pat in patterns:
        found = re.search(pat, html)
        if found:
            return found.group(1)
    return None


def plain(value: str) -> str:
    """Decode nested HTML entities so a value is escaped exactly once on write."""
    previous = None
    current = value
    while current != previous:
        previous = current
        current = unescape(current)
    return current


def set_meta(html: str, attr: str, key: str, value: str) -> str:
    value = escape(plain(value), quote=True)
    patterns = [
        rf'(<meta\s+{attr}="{re.escape(key)}"\s+content=")[^"]*(")',
        rf'(<meta\s+content=")[^"]*("\s+{attr}="{re.escape(key)}")',
    ]
    for pat in patterns:
        if re.search(pat, html):
            return re.sub(pat, lambda match: match.group(1) + value + match.group(2), html, count=1)
    tag = f'  <meta {attr}="{key}" content="{value}">\n'
    return html.replace("</head>", tag + "</head>", 1)


def title_text(html: str) -> str:
    found = re.search(r"<title>(.*?)</title>", html, flags=re.S)
    raw = re.sub(r"\s+", " ", found.group(1)).strip() if found else "The White Cakes - Cebu"
    return unescape(raw)


def ensure_social(html: str, rel: str, service_images: dict[str, list[dict]]) -> str:
    from PIL import Image

    title = title_text(html)
    if "The White Cakes - Cebu" not in title and "The White Cakes" not in title:
        title = f"{title} | The White Cakes - Cebu"
        html = re.sub(
            r"<title>.*?</title>",
            lambda _match: f"<title>{escape(title)}</title>",
            html,
            count=1,
            flags=re.S,
        )
    description = unescape(meta_content(html, "name", "description") or "Made-to-order cakes from The White Cakes - Cebu.")
    canon = meta_content(html, "rel", "canonical")
    if canon is None:
        href = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html)
        canon = href.group(1) if href else f"{BASE}/"
    html = set_meta(html, "property", "og:site_name", "The White Cakes - Cebu")
    html = set_meta(html, "property", "og:locale", "en_PH")
    if meta_content(html, "property", "og:title") is None:
        html = set_meta(html, "property", "og:title", title)
    if meta_content(html, "property", "og:description") is None:
        html = set_meta(html, "property", "og:description", description)
    if meta_content(html, "property", "og:url") is None:
        html = set_meta(html, "property", "og:url", canon)
    if meta_content(html, "property", "og:type") is None:
        kind = "article" if rel.startswith("journal/") and rel != "journal/index.html" else "website"
        html = set_meta(html, "property", "og:type", kind)

    if rel in service_images:
        wide = next(img for img in service_images[rel] if img["url"].endswith("-16x9.jpg"))
        image = wide["url"]
        width, height = str(wide["width"]), str(wide["height"])
        alt = meta_content(html, "property", "og:image:alt") or f"{SERVICES[rel]['name']} by The White Cakes - Cebu"
    elif meta_content(html, "property", "og:image"):
        image = meta_content(html, "property", "og:image") or f"{BASE}/assets/og.webp"
        width = meta_content(html, "property", "og:image:width")
        height = meta_content(html, "property", "og:image:height")
        local = image.removeprefix(BASE)
        file_path = ROOT / local.lstrip("/")
        if file_path.exists():
            with Image.open(file_path) as im:
                width, height = str(im.size[0]), str(im.size[1])
        alt = meta_content(html, "property", "og:image:alt") or "A cake by The White Cakes - Cebu"
    else:
        image = f"{BASE}/assets/og.webp"
        width, height = "1200", "630"
        alt = "An ivory marble cake by The White Cakes - Cebu"

    html = set_meta(html, "property", "og:image", image)
    html = set_meta(html, "property", "og:image:width", width or "1200")
    html = set_meta(html, "property", "og:image:height", height or "630")
    html = set_meta(html, "property", "og:image:alt", alt)
    html = set_meta(html, "name", "twitter:card", "summary_large_image")
    html = set_meta(html, "name", "twitter:title", meta_content(html, "property", "og:title") or title)
    html = set_meta(html, "name", "twitter:description", meta_content(html, "property", "og:description") or description)
    html = set_meta(html, "name", "twitter:image", image)
    html = set_meta(html, "name", "twitter:image:alt", alt)
    return html


def ensure_about_link(html: str) -> str:
    if 'href="/about/"' in html or "about/index.html" in html:
        return html
    email = '<li><a href="mailto:info@thewhitecakes.com">info@thewhitecakes.com</a></li>'
    if email in html:
        return html.replace(email, email + '\n        <li><a href="/about/">About</a></li>', 1)
    return html


def ensure_footer(html: str) -> str:
    if 'class="site-footer"' in html:
        return html
    footer = f"""  <footer class="site-footer">
    <div class="section-inner">
      <a class="brand brand-stack" href="/">{LOGO_IMG}<span class="wordmark">White Cakes</span></a>
      <ul class="footer-links">
        <li><a href="mailto:info@thewhitecakes.com">info@thewhitecakes.com</a></li>
        <li><a href="/about/">About</a></li>
        <li><a href="/faq/">FAQ</a></li>
      </ul>
      <p class="loc">Cebu City · Mandaue City · Lapu-Lapu City</p>
      <p class="legal">© 2026 The White Cakes - Cebu</p>
    </div>
  </footer>
"""
    return html.replace("</main>", "</main>\n" + footer, 1)


def service_block(rel: str, images: list[dict], description: str, canon: str) -> dict:
    spec = SERVICES[rel]
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": spec["name"],
        "description": description,
        "serviceType": spec["serviceType"],
        "url": canon,
        "image": images,
        "provider": {"@id": ORG_ID},
        "areaServed": AREAS,
    }


def breadcrumb(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": name, "item": url}
            for i, (name, url) in enumerate(items, start=1)
        ],
    }


def page_url(rel: str) -> str:
    if rel == "index.html":
        return f"{BASE}/"
    if rel.endswith("/index.html"):
        return f"{BASE}/{rel[: -len('index.html')]}"
    return f"{BASE}/{rel}"


def crumb_for(rel: str, html: str) -> dict | None:
    if rel in ("index.html", "404.html"):
        return None
    label = title_text(html).split("|")[0].strip()
    url = page_url(rel)
    if rel.startswith("journal/") and rel != "journal/index.html":
        return breadcrumb([("Home", f"{BASE}/"), ("Journal", f"{BASE}/journal/"), (label, url)])
    if rel == "journal/index.html":
        return breadcrumb([("Home", f"{BASE}/"), ("Journal", url)])
    return breadcrumb([("Home", f"{BASE}/"), (label, url)])


def patch_html(service_images: dict[str, list[dict]]) -> None:
    brand_images = service_images["__brand__"]
    for path in sorted(ROOT.rglob("*.html")):
        if "scripts" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        html = path.read_text(encoding="utf-8")
        html = html.replace(OLD_FB, FB).replace("https://www.facebook.com/thewhitecakes\"", FB + "\"")
        html = ensure_footer(html)
        html = ensure_logos(html)
        html = ensure_about_link(html)
        html = ensure_icon_links(html)
        html = ensure_social(html, rel, service_images)
        description = plain(meta_content(html, "name", "description") or "")
        canon = page_url(rel)

        if rel == "index.html":
            html = strip_jsonld(html)
            block = "\n".join(
                [
                    json_script(organization_entity(brand_images)),
                    json_script(website_entity()),
                    json_script(collection_itemlist()),
                ]
            )
            html = html.replace("</head>", block + "\n</head>", 1)
            if 'href="/about/"' not in html.split("<footer", 1)[0]:
                html = html.replace(
                    "we confirm pickup time and meeting details when we reply.</p>",
                    'we confirm pickup time and meeting details when we reply. <a href="/about/">Facts about the kitchen</a>.</p>',
                    1,
                )
        else:
            def mutate(data, rel=rel, description=description, canon=canon):
                data = clean_node(data)
                if rel in SERVICES:
                    apply_service(data, SERVICES[rel], service_images[rel], canon, description)
                return data

            html = replace_jsonld(html, mutate)
            found: set[str] = set()
            for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, flags=re.S):
                found |= types_of(json.loads(match.group(1)))
            extra = []
            if rel in SERVICES and "Service" not in found:
                extra.append(service_block(rel, service_images[rel], description, canon))
            if "BreadcrumbList" not in found:
                crumb = crumb_for(rel, html)
                if crumb:
                    extra.append(crumb)
            if rel == "about/index.html" and "AboutPage" not in found:
                extra.append(
                    {
                        "@context": "https://schema.org",
                        "@type": "AboutPage",
                        "@id": f"{BASE}/about/#webpage",
                        "url": f"{BASE}/about/",
                        "name": "About The White Cakes - Cebu",
                        "description": description,
                        "isPartOf": {"@id": SITE_ID},
                        "about": {"@id": ORG_ID},
                        "publisher": {"@id": ORG_ID},
                        "inLanguage": "en-PH",
                    }
                )
            if ORG_ID not in html and not any(ORG_ID in json.dumps(item) for item in extra):
                extra.append(
                    {
                        "@context": "https://schema.org",
                        "@type": "WebPage",
                        "url": canon,
                        "name": unescape(title_text(html).split("|")[0].strip()),
                        "isPartOf": {"@id": SITE_ID},
                        "publisher": {"@id": ORG_ID},
                        "inLanguage": "en-PH",
                    }
                )
            if extra:
                html = html.replace("</head>", "\n".join(json_script(item) for item in extra) + "\n</head>", 1)
        path.write_text(html, encoding="utf-8")
        print("patched", rel)


def write_about() -> None:
    description = (
        "The White Cakes - Cebu is a made-to-order cloud kitchen in Lahug, Cebu. "
        "No storefront or walk-ins. Delivery in Cebu City, Mandaue City, and Lapu-Lapu City."
    )
    page = f"""<!DOCTYPE html>
<html lang="en-PH">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>About | The White Cakes - Cebu</title>
  <meta name="description" content="{escape(description, quote=True)}">
  <link rel="canonical" href="{BASE}/about/">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Manrope:wght@400;500;600&display=swap">
  <link rel="stylesheet" href="/css/styles.css">
</head>
<body class="sub">
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header" id="site-header">
    <a class="brand" href="/">{LOGO_IMG}<span class="wordmark">White Cakes</span></a>
    <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="primary-nav">Menu</button>
    <div class="header-end">
      <nav class="nav" id="primary-nav" aria-label="Primary">
        <a href="/#collection">Collection</a>
        <a href="/#occasions">Occasions</a>
        <a href="/journal/">Journal</a>
        <a href="/faq/">FAQ</a>
        <a href="/about/" aria-current="page">About</a>
      </nav>
      <a class="header-cta" href="/order/">Order</a>
    </div>
  </header>
  <main id="main">
    <article class="article">
      <nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a> · <span>About</span></nav>
      <h1>About The White Cakes - Cebu</h1>
      <p class="dek">A made-to-order cloud kitchen in Lahug. No storefront, no walk-ins, no published street address.</p>
      <figure class="landing-figure">
        <div class="media-frame">
          <img src="/assets/white-cakes-logo.png" width="1024" height="1024" alt="The White Cakes - Cebu logo">
        </div>
        <figcaption>The White Cakes - Cebu</figcaption>
      </figure>
      <div class="prose">
        <p>The White Cakes - Cebu, also called White Cakes and The White Cakes, bakes buttercream cakes for a date you name. The kitchen is in Lahug, Cebu. Orders are confirmed before anyone collects a cake, and delivery runs to Cebu City, Mandaue City, and Lapu-Lapu City.</p>
        <h2 id="facts-title">Facts</h2>
        <dl class="cake-meta facts">
          <div><dt>Name</dt><dd>The White Cakes - Cebu</dd></div>
          <div><dt>Also known as</dt><dd>White Cakes; The White Cakes</dd></div>
          <div><dt>What we are</dt><dd>A made-to-order cloud kitchen. There is no storefront and no walk-in counter.</dd></div>
          <div><dt>Where</dt><dd>Lahug, Cebu City. The street address is not published. Pickup is arranged after the order is confirmed.</dd></div>
          <div><dt>Delivery</dt><dd>Cebu City, Mandaue City, and Lapu-Lapu City, including Mactan when the date and the gate allow it.</dd></div>
          <div><dt>Cakes</dt><dd>Signature Marble (6-inch), Bouquet Cake, Bento Cake (4-inch), and custom celebration cakes for birthdays, anniversaries, intimate weddings, and offices.</dd></div>
          <div><dt>Flavours</dt><dd>Chocolate, vanilla, ube, mango, and red velvet.</dd></div>
          <div><dt>Lead time</dt><dd>At least three days before the date. We reply within 24 hours.</dd></div>
          <div><dt>Email</dt><dd><a href="mailto:info@thewhitecakes.com">info@thewhitecakes.com</a></dd></div>
          <div><dt>WhatsApp</dt><dd><a data-wa href="https://wa.me/639474382632" rel="noopener noreferrer">+63 947 438 2632</a></dd></div>
          <div><dt>Instagram</dt><dd><a data-ig href="{IG}" rel="noopener noreferrer">@thewhitecakescebu</a></dd></div>
          <div><dt>Facebook</dt><dd><a data-fb href="{FB}" rel="noopener noreferrer">The White Cakes - Cebu</a></dd></div>
        </dl>
        <h2>How to order</h2>
        <p>Use the <a href="/order/">order form</a> or message us on WhatsApp. Send the design, the flavour, the date, the words for the top, and whether you want arranged pickup or delivery. For delivery, include a full address, a landmark, and the name of the person who will meet the cake. Launch price — until January 15, 2027. The struck-through amount on the menu is the regular price from January 16, 2027. Bouquet cakes are price on request. A 50% deposit confirms the order.</p>
        <p>Read the <a href="/faq/">FAQ</a> for lead time, flavours, and delivery, or start from the <a href="/#collection">collection</a>.</p>
      </div>
    </article>
  </main>
  <footer class="site-footer">
    <div class="section-inner">
      <a class="brand brand-stack" href="/">{LOGO_IMG}<span class="wordmark">White Cakes</span></a>
      <ul class="footer-links">
        <li><a href="mailto:info@thewhitecakes.com">info@thewhitecakes.com</a></li>
        <li><a href="/about/">About</a></li>
        <li><a data-ig href="{IG}" rel="noopener noreferrer">Instagram</a></li>
        <li><a data-fb href="{FB}" rel="noopener noreferrer">Facebook</a></li>
        <li><a href="/faq/">FAQ</a></li>
        <li><a href="/journal/">Journal</a></li>
      </ul>
      <p class="loc">Cebu City · Mandaue City · Lapu-Lapu City</p>
      <p class="legal">© 2026 The White Cakes - Cebu</p>
    </div>
  </footer>
  <nav class="dock" aria-label="Quick actions">
    <a href="/order/">Order</a>
    <a data-wa href="https://wa.me/639474382632" rel="noopener noreferrer">WhatsApp</a>
  </nav>
  <script src="/js/main.js" defer></script>
</body>
</html>
"""
    dest = ROOT / "about" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page, encoding="utf-8")


def write_robots() -> None:
    (ROOT / "robots.txt").write_text(
        """# Favicon, apple touch icon, logo, and manifest must stay crawlable.
# Googlebot and Googlebot-Image need the homepage and /assets/white-cakes-logo.png.

User-agent: *
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Googlebot-Image
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Bingbot
Allow: /

Sitemap: https://www.thewhitecakes.com/sitemap.xml
""",
        encoding="utf-8",
    )


def page_images(rel_url: str) -> list[tuple[str, str]]:
    if rel_url == "/llms.txt":
        return []
    if rel_url == "/":
        path = ROOT / "index.html"
    elif rel_url.endswith("/"):
        path = ROOT / rel_url.strip("/") / "index.html"
    else:
        path = ROOT / rel_url.lstrip("/")
    if not path.exists():
        return []
    html = path.read_text(encoding="utf-8")
    found: list[tuple[str, str]] = []
    seen: set[str] = set()

    def add(url: str, title: str) -> None:
        if not url or url.startswith("data:"):
            return
        if url.startswith("/"):
            url = BASE + url
        if not url.startswith(BASE):
            return
        if any(token in url for token in ("favicon", "apple-touch-icon", "/css/", "/js/")):
            return
        if url in seen:
            return
        seen.add(url)
        found.append((url, title))

    og = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html)
    og_alt = re.search(r'<meta\s+property="og:image:alt"\s+content="([^"]*)"', html)
    if og:
        add(og.group(1), plain(og_alt.group(1)) if og_alt else "")
    for tag in re.findall(r"<img\b[^>]*>", html):
        src = re.search(r'\bsrc="([^"]+)"', tag)
        alt = re.search(r'\balt="([^"]*)"', tag)
        if src:
            add(src.group(1), plain(alt.group(1)) if alt else "")
    for url in re.findall(r"https://www\.thewhitecakes\.com/[^\"\s]+\.(?:jpg|jpeg|png|webp)", html):
        add(url, "")
    if rel_url == "/":
        add(f"{BASE}/assets/white-cakes-logo.png", "The White Cakes - Cebu logo")
    return found[:1000]


def write_sitemap() -> None:
    journal = sorted((ROOT / "journal").glob("*.html"))
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]
    entries = list(SITEMAP_PAGES)
    for path in journal:
        if path.name == "index.html":
            continue
        entries.append((f"/journal/{path.name}", "monthly", "0.7"))
    for loc, freq, pri in entries:
        images = page_images(loc)
        lines.append("  <url>")
        lines.append(f"    <loc>{xml_escape(BASE + loc)}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{pri}</priority>")
        for url, title in images:
            lines.append("    <image:image>")
            lines.append(f"      <image:loc>{xml_escape(url)}</image:loc>")
            if title:
                lines.append(f"      <image:title>{xml_escape(title)}</image:title>")
            lines.append("    </image:image>")
        lines.append("  </url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_llms() -> None:
    journal_lines = []
    index = (ROOT / "journal" / "index.html").read_text(encoding="utf-8")
    entries = re.findall(
        r'<li>\s*<a href="(/journal/[^"#]+\.html)">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</a>\s*</li>',
        index,
        flags=re.S,
    )
    for href, title, summary in entries:
        title_text_value = unescape(re.sub(r"<.*?>", "", title)).strip()
        summary_text = unescape(re.sub(r"<.*?>", "", summary)).strip()
        if not summary_text:
            page = ROOT / href.lstrip("/")
            page_html = page.read_text(encoding="utf-8") if page.exists() else ""
            description = re.search(
                r'<meta\s+name="description"\s+content="([^"]*)"', page_html, flags=re.I
            )
            summary_text = unescape(description.group(1)).strip() if description else ""
        suffix = f" — {summary_text}" if summary_text else ""
        journal_lines.append(f"- [{title_text_value}]({BASE}{href}){suffix}")
    if not journal_lines:
        for path in sorted((ROOT / "journal").glob("*.html")):
            if path.name == "index.html":
                continue
            page_html = path.read_text(encoding="utf-8")
            title = title_text(page_html).split("|")[0].strip()
            description = re.search(
                r'<meta\s+name="description"\s+content="([^"]*)"', page_html, flags=re.I
            )
            summary = unescape(description.group(1)).strip() if description else ""
            suffix = f" — {summary}" if summary else ""
            journal_lines.append(f"- [{title}]({BASE}/journal/{path.name}){suffix}")
    body = f"""# The White Cakes - Cebu

> The White Cakes - Cebu (also called White Cakes and The White Cakes) is a made-to-order cloud kitchen in Lahug, Cebu. There is no storefront, no walk-in counter, and no street address is published. Pickup is arranged after an order is confirmed. Delivery covers Cebu City, Mandaue City, and Lapu-Lapu City.

## Brand

- Name: The White Cakes - Cebu
- DTI-registered business name: THE WHTE CAKES SHOP (National scope), Business Name No. 8628157; valid November 19, 2026 through November 19, 2031. This is a business name registration, not a license to operate.
- Alternate names: White Cakes; The White Cakes
- Website: {BASE}/
- Email: {EMAIL}
- WhatsApp: +63 947 438 2632
- Instagram: {IG}
- Facebook: {FB}
- Logo: {BASE}/assets/white-cakes-logo.png
- Cebu directory profile: {MYCEBU}

## Services

Hand-finished buttercream cakes, baked for a named date. Signature designs are Signature Marble (6-inch), Bouquet Cake, and Bento Cake (4-inch). Also custom celebration cakes, birthday cakes, anniversary and gift cakes, intimate wedding and engagement cakes, and corporate or office orders. Flavours are chocolate, vanilla, ube, mango, and red velvet.

Launch prices in PHP are published until January 15, 2027 inclusive. The regular price is charged after that date. Custom designs are starting prices. Bouquet cakes are price on request. A 50% deposit confirms the order. This site does not list reviews or ratings.

## Launch prices (PHP)

Valid through January 15, 2027. Custom cake prices are starting prices; the final amount depends on the design.

- Bento cake (4 inch): regular ₱599; launch ₱449
- 6-inch custom cake: regular ₱1,799; starting at ₱1,399
- 8-inch custom cake: regular ₱2,599; starting at ₱1,999
- 2-tier custom cake: regular ₱4,299; starting at ₱3,399
- Christmas vintage cake (6 inch): regular ₱1,650; Christmas special ₱650 through December 25, 2026
- Bouquet cake: price on request

## How to order

Orders need at least three days' notice. Tell us the design, flavour, date, words for the top, and whether you want arranged pickup in Cebu City or delivery. For delivery, send a full address, a landmark, and a person who will receive the cake. We reply within 24 hours.

- Order form: {BASE}/order/
- WhatsApp: https://wa.me/639474382632

## Delivery areas

- Cebu City: {BASE}/cake-delivery-cebu-city/
- Mandaue City: {BASE}/cake-delivery-mandaue/
- Lapu-Lapu City, including Mactan: {BASE}/cake-delivery-lapu-lapu/

## Key pages

- [Home]({BASE}/) — Signature Marble, Bouquet, and Bento, plus how to order.
- [About]({BASE}/about/) — Facts: name, kitchen, delivery areas, and contact.
- [Order]({BASE}/order/) — Design a cake and send the order.
- [Bento cakes]({BASE}/bento-cakes-cebu/) — 4-inch bento cakes.
- [Bouquet cakes]({BASE}/bouquet-cakes-cebu/) — Piped bouquet-style buttercream cakes.
- [Custom cakes]({BASE}/custom-cakes-cebu/) — Signature Marble and custom celebration cakes.
- [Birthday cakes]({BASE}/birthday-cakes-cebu/) — Birthday cakes made to order.
- [Anniversary cakes]({BASE}/anniversary-cakes-cebu/) — Anniversary and gift cakes.
- [Wedding cakes]({BASE}/wedding-cakes-cebu/) — Intimate wedding and engagement cakes.
- [Corporate orders]({BASE}/corporate-cake-orders-cebu/) — Office and corporate cake orders.
- [Christmas cakes]({BASE}/christmas-cakes-cebu/) — 2026 Christmas cake designs, the seasonal cake offer, ordering timeline, and Metro Cebu delivery.
- [FAQ]({BASE}/faq/) — Lead time, delivery, flavours, and ordering.
- [Journal]({BASE}/journal/) — Guides for ordering and celebrating in Cebu.

## Journal guides

{chr(10).join(journal_lines)}
"""
    (ROOT / "llms.txt").write_text(body, encoding="utf-8")


def validate() -> None:
    from PIL import Image

    ico = Image.open(ROOT / "favicon.ico")
    sizes = set(ico.ico.sizes())
    print("favicon.ico sizes", sorted(sizes))
    if sizes != {(16, 16), (32, 32), (48, 48)}:
        raise SystemExit(f"favicon.ico sizes are {sizes}")
    logo = Image.open(ROOT / "assets" / "white-cakes-logo.png")
    if logo.size[0] < 112 or logo.size[1] < 112 or logo.size[0] != logo.size[1]:
        raise SystemExit(f"logo is {logo.size}, need a square of at least 112")
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if re.search(r"(?i)disallow:\s*/(?:favicon|apple-touch|logo-512|site\.webmanifest)", robots):
        raise SystemExit("robots.txt blocks an icon")
    problems = []
    for path in sorted(ROOT.rglob("*.html")):
        if "scripts" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        if 'href="/assets/white-cakes-logo.png"' not in text:
            problems.append(f"{rel}: missing official logo asset")
        if 'rel="apple-touch-icon" href="/apple-touch-icon.png"' not in text:
            problems.append(f"{rel}: missing apple touch icon")
        if 'alt="The White Cakes - Cebu logo"' not in text:
            problems.append(f"{rel}: missing logo alt")
        if "data:image" in text and "rel=\"icon\"" in text.split("data:image", 1)[0][-80:]:
            problems.append(f"{rel}: data-uri icon")
        if 'property="og:site_name" content="The White Cakes - Cebu"' not in text:
            problems.append(f"{rel}: og:site_name")
        if 'property="og:image"' not in text or 'name="twitter:card"' not in text:
            problems.append(f"{rel}: missing social image")
        for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', text, flags=re.S):
            try:
                data = json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                problems.append(f"{rel}: JSON {exc}")
                continue
            blob = json.dumps(data)
            for banned in ('"@type": "Product"', '"AggregateOffer"', '"AggregateRating"', '"priceRange"', '"review"'):
                if banned in blob:
                    problems.append(f"{rel}: found {banned}")
            if '"@type": "Review"' in blob or '"Review"' in blob:
                problems.append(f"{rel}: Review type")
        if rel != "index.html" and "application/ld+json" in text and ORG_ID not in text and rel != "404.html":
            problems.append(f"{rel}: does not reference organization @id")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    if home.count(ORG_ID) < 2:
        problems.append("home: organization @id missing")
    if '"Organization"' not in home or '"Bakery"' not in home:
        problems.append("home: combined Organization+Bakery type missing")
    if '"WebSite"' not in home or '"alternateName"' not in home:
        problems.append("home: WebSite alternateName missing")
    if '"ItemList"' not in home:
        problems.append("home: ItemList missing")
    faq = (ROOT / "faq" / "index.html").read_text(encoding="utf-8")
    if '"FAQPage"' not in faq:
        problems.append("faq: FAQPage missing")
    sitemap_path = ROOT / "sitemap.xml"
    sitemap_text = sitemap_path.read_text(encoding="utf-8")
    if "image:image" not in sitemap_text:
        problems.append("sitemap: no image entries")
    try:
        sitemap_root = ET.parse(sitemap_path).getroot()
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        submitted = {
            loc.text.strip()
            for url in sitemap_root.findall(f"{namespace}url")
            if (loc := url.find(f"{namespace}loc")) is not None and loc.text
        }
        expected = set()
        for path in ROOT.rglob("*.html"):
            rel = path.relative_to(ROOT).as_posix()
            if rel == "404.html":
                continue
            text = path.read_text(encoding="utf-8")
            noindex = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex', text, re.I)
            if noindex:
                continue
            canonical = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', text, re.I)
            if canonical is None:
                problems.append(f"{rel}: missing canonical while checking sitemap")
            else:
                expected.add(canonical.group(1))
        if submitted != expected:
            missing_urls = sorted(expected - submitted)
            extra_urls = sorted(submitted - expected)
            if missing_urls:
                problems.append("sitemap missing indexable pages: " + ", ".join(missing_urls))
            if extra_urls:
                problems.append("sitemap includes non-page or non-canonical URLs: " + ", ".join(extra_urls))
    except ET.ParseError as exc:
        problems.append(f"sitemap: invalid XML {exc}")
    if problems:
        raise SystemExit("validation failed:\n" + "\n".join(problems))
    print("validation ok")


def main() -> None:
    generate_brand_icons()
    images = generate_crops()
    write_manifest()
    write_about()
    patch_html(images)
    write_robots()
    write_llms()
    write_sitemap()
    validate()


if __name__ == "__main__":
    main()
