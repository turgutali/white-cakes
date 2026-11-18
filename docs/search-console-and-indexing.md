# Search Console, Bing, and indexing

## Automatic discovery for participating search engines

Automatic push notifications are disabled while the SEO content package is still being completed. The previous batch was accepted on 2026-11-18 (52 URLs, HTTP 200). When the package is final, run the workflow manually with its default empty `before` value to submit the site's current canonical, indexable HTML URLs in one batch. The public key file is hosted at the site root. IndexNow can speed discovery for participating engines, but does not guarantee crawling, indexing, or ranking. Google does not use IndexNow.

## Google Search Console

The `https://www.thewhitecakes.com/` property is available in Search Console under `info@thewhitecakes.com`. `/sitemap.xml` is already submitted; on 2026-11-18 it showed “Successful,” last read 18 November, with 51 discovered pages. The Page indexing and Performance reports were still processing. URL Inspection confirmed the homepage is indexed. The new Christmas landing page was initially unknown to Google; its live test passed and the indexing request was accepted on 18 November. Google reports it as queued, not indexed. A sitemap and crawl request help discovery, but do not guarantee indexing or ranking.

Keep `/sitemap.xml` limited to canonical HTML pages intended for Google Search. Do not add `/llms.txt` there; it remains available to AI crawlers at its own URL. When changing the sitemap generator, include every current indexable static page (including `/christmas-cakes-cebu/` and `/ordering/`) and every journal post, then compare the generated URL set against the published sitemap before deployment.

## Bing Webmaster Tools

The sitemap can also be submitted in Bing Webmaster Tools. Use Bing Webmaster Tools to inspect IndexNow activity and indexing status.

## Business listings

Keep business name, phone, service areas, website, and service-area business details consistent across public listings. The business has a Google Business Profile awaiting video verification; do not create a duplicate listing.
