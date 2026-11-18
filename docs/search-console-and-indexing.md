# Search Console, Bing, and indexing

## Automatic discovery for participating search engines

Automatic push notifications remain disabled. The completed content batch contains 39 journal posts and 57 canonical, indexable sitemap URLs. On 2026-11-18, the manual IndexNow workflow accepted all 57 URLs (HTTP 200); the generated URL list exactly matched `sitemap.xml`. Future content batches should be submitted once after publication using the workflow's default empty `before` value. The public key file is hosted at the site root. IndexNow can speed discovery for participating engines, but does not guarantee crawling, indexing, or ranking. Google does not use IndexNow.

## Google Search Console

The `https://www.thewhitecakes.com/` property is available in Search Console under `info@thewhitecakes.com`. The `/sitemap.xml` submission was refreshed on 2026-11-18 after publication of the 57-URL content batch; Search Console confirmed successful submission. Before the refresh, Google had discovered 56 pages. Allow the next report update to show the new count. The Page indexing, Performance, and Links reports were still processing. URL Inspection confirmed the homepage is indexed. The baby-shower article was reported as “Discovered – currently not indexed”; its indexing request had been accepted and was queued. A sitemap and crawl request help discovery, but do not guarantee indexing or ranking.

Keep `/sitemap.xml` limited to canonical HTML pages intended for Google Search. Do not add `/llms.txt` there; it remains available to AI crawlers at its own URL. When changing the sitemap generator, include every current indexable static page (including `/christmas-cakes-cebu/` and `/ordering/`) and every journal post, then compare the generated URL set against the published sitemap before deployment.

## Bing Webmaster Tools

The sitemap can also be submitted in Bing Webmaster Tools. Use Bing Webmaster Tools to inspect IndexNow activity and indexing status.

## Business listings

Keep business name, phone, service areas, website, and service-area business details consistent across public listings. The business has a Google Business Profile awaiting video verification; do not create a duplicate listing.
