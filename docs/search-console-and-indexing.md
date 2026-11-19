# Search Console, Bing, and indexing

## Current verified state (2026-11-19)

- The live sitemap contains 99 unique canonical URLs, including 81 Journal articles (excluding the `/journal/` index).
- A Googlebot-user-agent crawl of all 99 sitemap URLs returned HTTP 200, with matching canonicals and no `noindex` directives. This establishes fetchability, not that Google has crawled or indexed each URL.
- The public robots file permits Googlebot, Bingbot, OAI-SearchBot, GPTBot, ClaudeBot, and PerplexityBot. `llms.txt` lists the current service areas, prices, key pages, and Journal articles.
- On 2026-11-19, after the journal content work was live, IndexNow accepted seven updated article URLs in one request (HTTP 200). The follow-up Cebuano pricing update changed `/journal/asa-magpa-order-cake-cebu.html` and `/journal/`; IndexNow accepted both in one request (HTTP 200). After the order-wizard image description update, IndexNow accepted `/order/` (HTTP 200). These notifications inform IndexNow-participating engines; they are not Google indexing requests or guarantees.
- A Google search snapshot for `cake delivery Cebu City` localized to Cebu did not show The White Cakes in the visible local or organic results. In a separate signed-out Google session whose displayed location was Singapore, `site:https://www.thewhitecakes.com/` returned no results. This is an indexing warning, not an index count: Google says `site:` results are incomplete and URL Inspection is more reliable ([Google Search operator documentation](https://developers.google.com/search/docs/monitor-debug/search-operators/all-search-site)).

## Google Search Console

The property is signed in under `info@thewhitecakes.com`. On 2026-11-19, the current 99-URL sitemap was successfully resubmitted. Search Console still showed 68 discovered URLs at the time of checking; this is stale processing data, not confirmation that all 99 were discovered.

The Page indexing report was still processing. The latest three-month Performance report showed 14 impressions, 0 clicks, 0% CTR, and average position 14.8, with data only through 2026-11-16. This sample is too small to support a broad demand forecast.

URL Inspection results on 2026-11-19:

- `/journal/paghahatid-cake-cebu.html` (Tagalog delivery guide) is indexed.
- `/journal/unsa-ang-bento-cake-cebu.html` (Cebuano Bento guide) passed a live URL test and its indexing request was accepted; Search Console showed it queued for priority crawling.
- `/journal/ano-ang-bento-cake-cebu.html` (Tagalog Bento guide) was previously unknown to Google. Its live URL test passed and showed it can be indexed, but the individual indexing request failed because the daily quota had been exceeded. Retry after the quota resets; the sitemap is also submitted as a discovery path.

Individual recrawl requests are quota-limited and do not guarantee inclusion. Use the sitemap for the full page set and URL Inspection for a small number of priority pages.

The 950 multilingual candidate manuscripts are in the `cebubu/content-batch-next` draft branch; they are not live URLs. The live-site count remains 99 until reviewed material is merged into canonical pages or approved as a distinct page.

Do not claim Google indexing solely because a URL is in the sitemap, appears in a `site:` query, or was sent through IndexNow. Google Search Console is the source for URL-level index status and site performance.

## Bing and IndexNow

On 2026-11-18, Bing Webmaster Tools recorded a 59-URL sitemap submission as Processing; its previous read showed 58 URLs. IndexNow accepted the 59-URL set. On 2026-11-19, after the current page batch was complete, IndexNow accepted `/cake-delivery-cebu-city/` and `/about/` together. Recheck Bing Webmaster Tools for sitemap processing, search queries, and AI Performance after reports refresh.

Keep notifications batch-based: finish the related copy, internal links, canonical metadata, and sitemap updates first; then send the changed canonical URL set once. Do not use IndexNow as a substitute for Google Search Console.

## Business listings

The Google Business Profile already exists and is awaiting video verification. Do not create a duplicate. The owner must complete Google's video step. Keep the public business name, phone, website, service areas, and service-area business details consistent across listings. The existing owner-verified MyCebu record is linked from the About page and from the site's Organization `sameAs` data.
