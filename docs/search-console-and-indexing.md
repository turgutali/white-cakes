# Search Console, Bing, and indexing

## 1. Google Search Console

1. Open [Google Search Console](https://search.google.com/search-console).
2. Add property: **URL prefix** `https://www.thewhitecakes.com/`
3. Choose **HTML tag** verification. Copy the `content="..."` value only.
4. In the repo, copy `seo-config.example.json` to `seo-config.json` and set `"google_site_verification"` to that value.
5. Run: `python3 scripts/inject_seo_tags.py`, commit, push to `main`, wait ~2 minutes for GitHub Pages.
6. Click **Verify** in Search Console.
7. **Sitemaps** → Submit `https://www.thewhitecakes.com/sitemap.xml`
8. **URL inspection** → request indexing for:
   - `https://www.thewhitecakes.com/`
   - `https://www.thewhitecakes.com/bento-cakes-cebu/`
   - `https://www.thewhitecakes.com/journal/cake-delivery-cebu.html`
   - `https://www.thewhitecakes.com/journal/christmas-cake-delivery-cebu.html`

## 2. Bing Webmaster Tools

1. [Bing Webmaster](https://www.bing.com/webmasters) → add site → verify with meta tag.
2. Put the token in `seo-config.json` → `bing_site_verification`, run inject script, push, verify.
3. Submit the same sitemap URL.

## 3. Optional GA4

Set `"ga4_measurement_id": "G-XXXXXXXX"` in `seo-config.json` and re-run inject.

## 4. Social bios (manual)

- **Instagram** [@thewhitecakescebu](https://www.instagram.com/thewhitecakescebu/): Website = `https://www.thewhitecakes.com`
- **Facebook** [The White Cakes](https://www.facebook.com/thewhitecakes/): Website field = same URL

## 5. Google Business Profile (optional)

Service-area business: Cebu City, Mandaue, Lapu-Lapu. No public street address. Same website and WhatsApp as on the site.