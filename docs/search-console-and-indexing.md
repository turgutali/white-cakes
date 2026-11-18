# Search Console, Bing, and indexing

## Automatic discovery for participating search engines

Automatic push notifications remain disabled. The content set contains 40 journal posts and 58 canonical, indexable sitemap URLs. On 2026-11-18, the manual IndexNow workflow accepted all 57 URLs (HTTP 200); the generated URL list exactly matched the then-current `sitemap.xml`. It later accepted the six changed HTML URLs in the minimalist-cake content batch (HTTP 200). Future content batches should be submitted once after publication using the workflow's default empty `before` value. The public key file is hosted at the site root. IndexNow can speed discovery for participating engines, but does not guarantee crawling, indexing, or ranking. Google does not use IndexNow.

## Google Search Console

The `https://www.thewhitecakes.com/` property is available in Search Console under `info@thewhitecakes.com`. After the 58-URL content batch was published, `/sitemap.xml` was submitted again on 2026-11-18 and Search Console confirmed successful receipt. The row still showed 57 discovered pages from its prior read; Google has not yet reflected the new URL. The Page indexing report says its data is processing and to check again in a few days. URL Inspection previously confirmed the homepage is indexed. The baby-shower article was reported as “Discovered – currently not indexed”; its indexing request had been accepted and queued. A sitemap and crawl request help discovery, but do not guarantee indexing or ranking.

Keep `/sitemap.xml` limited to canonical HTML pages intended for Google Search. Do not add `/llms.txt` there; it remains available to AI crawlers at its own URL. When changing the sitemap generator, include every current indexable static page (including `/christmas-cakes-cebu/` and `/ordering/`) and every journal post, then compare the generated URL set against the published sitemap before deployment.

## Bing Webmaster Tools

The `thewhitecakes.com` site property is available in Bing Webmaster Tools under the Google sign-in `info@thewhitecakes.com`. The 58-URL `/sitemap.xml` was submitted on 2026-11-18; Bing shows it as **Processing**, with its previous crawl on 2026-11-15 having discovered 30 URLs. Bing Search Performance says to check back in 48 hours. AI Performance reports 0 citations and 0 cited pages for 2026-08-18 through 2026-11-17. URL Inspection said the new `/journal/minimalist-cake-cebu.html` was not known to Bing; its indexing request was accepted. The IndexNow dashboard listed all 58 site URLs among its recent submissions. Recheck sitemap crawl, URL discovery, search queries and AI citations after the reports update.

## Business listings

Keep business name, phone, service areas, website, and service-area business details consistent across public listings. The business has a Google Business Profile awaiting video verification; do not create a duplicate listing.

## Pending content batch (do not request indexing until deployed)

The vintage cake guide and its internal links are being finalized with the current seasonal offer only: 6-inch Christmas vintage cake at ₱650 through December 25, 2026 (listed regular price ₱1,650). It explicitly says year-round vintage availability is not listed. After this content set is checked and published, submit the current sitemap once in Google Search Console and Bing Webmaster Tools; do not submit individual URLs repeatedly.
