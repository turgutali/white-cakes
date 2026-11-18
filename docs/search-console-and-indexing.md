# Search Console, Bing, and indexing

## Automatic discovery for participating search engines

Automatic push notifications remain disabled. The content set contains 41 journal posts and 59 canonical, indexable sitemap URLs. On 2026-11-18, the manual IndexNow workflow accepted all 59 canonical URLs (HTTP 200); the generated URL list exactly matched the published `sitemap.xml`. The public key file is hosted at the site root. IndexNow can speed discovery for participating engines, but does not guarantee crawling, indexing, or ranking. Google does not use IndexNow.

## Google Search Console

The `https://www.thewhitecakes.com/` property is available in Search Console under `info@thewhitecakes.com`. After the 59-URL content batch was published, `/sitemap.xml` was submitted on 2026-11-18 and Search Console confirmed successful receipt. The sitemap row then showed 59 discovered pages. The Page indexing report still says its data is processing and to check again in a few days. URL Inspection for `/journal/vintage-cake-cebu.html` said Google did not yet know the URL; the request was accepted and queued as a priority crawl. A sitemap and crawl request help discovery, but do not guarantee indexing or ranking.

Keep `/sitemap.xml` limited to canonical HTML pages intended for Google Search. Do not add `/llms.txt` there; it remains available to AI crawlers at its own URL. When changing the sitemap generator, include every current indexable static page (including `/christmas-cakes-cebu/` and `/ordering/`) and every journal post, then compare the generated URL set against the published sitemap before deployment.

## Bing Webmaster Tools

The `thewhitecakes.com` site property is available in Bing Webmaster Tools under the Google sign-in `info@thewhitecakes.com`. The latest 59-URL `/sitemap.xml` was submitted on 2026-11-18; Bing shows it as **Processing**, with 58 URLs from the previous read. Bing Search Performance says to check back in 48 hours. AI Performance reports 0 citations and 0 cited pages for 2026-08-18 through 2026-11-17. URL Inspection now knows `/journal/vintage-cake-cebu.html` and reports “Discovered but not crawled”; its indexing request was accepted. IndexNow accepted all 59 canonical URLs (HTTP 200). Recheck sitemap crawl, URL discovery, search queries and AI citations after the reports update.

## Business listings

Keep business name, phone, service areas, website, and service-area business details consistent across public listings. The business has a Google Business Profile awaiting video verification; do not create a duplicate listing.
