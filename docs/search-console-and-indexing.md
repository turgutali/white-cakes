# Search Console, Bing, and indexing

## Current verified state (2026-11-19)

- The live sitemap contains 68 canonical URLs, including 50 Journal articles.
- A public crawl returned HTTP 200 for all 68 sitemap URLs and all 75 unique internal-link destinations found on those pages.
- The public robots file permits Googlebot, Bingbot, OAI-SearchBot, GPTBot, ClaudeBot, and PerplexityBot. `llms.txt` lists the current service areas, prices, key pages, and Journal articles.
- The latest completed website batch changed `/cake-delivery-cebu-city/` and `/about/`. IndexNow accepted both URLs in one request (HTTP 200). This informs IndexNow-participating engines; it is not a Google indexing request or guarantee.
- A Google search snapshot for `cake delivery Cebu City` localized to Cebu did not show The White Cakes in the visible local or organic results. This is a spot check, not a rank report.

## Google Search Console

The property was previously accessed under `info@thewhitecakes.com`. On 2026-11-18, the recorded sitemap submission contained 59 URLs and Search Console showed 59 discovered pages while the indexing report was processing. That is historical state; the sitemap has since grown to 68 URLs.

The current browser session has `info@thewhitecakes.com` selected but is waiting at Google's password step. Do not treat the historical 59-URL report as the current status. After the account owner finishes sign-in:

1. Check the Sitemaps report for `https://www.thewhitecakes.com/sitemap.xml`, last read, discovered URL count, and errors. Resubmit the sitemap if the latest 68-URL version is not processed.
2. Review Page indexing for excluded, blocked, duplicate, and crawled-but-not-indexed pages.
3. Review the last 28 days and 3 months of Performance data. Export queries and pages with impressions, clicks, CTR, and average position; prioritize pages with real impressions and weak CTR or relevance.
4. Use URL Inspection for a small number of fixed, high-value pages. For many URLs Google recommends a sitemap; a sitemap is a discovery hint and does not guarantee indexing. Individual recrawl requests are quota-limited and also do not guarantee inclusion.

Do not claim Google indexing solely because a URL is in the sitemap, appears in a `site:` query, or was sent through IndexNow. Google Search Console is the source for URL-level index status and site performance.

## Bing and IndexNow

On 2026-11-18, Bing Webmaster Tools recorded a 59-URL sitemap submission as Processing; its previous read showed 58 URLs. IndexNow accepted the 59-URL set. On 2026-11-19, after the current page batch was complete, IndexNow accepted `/cake-delivery-cebu-city/` and `/about/` together. Recheck Bing Webmaster Tools for sitemap processing, search queries, and AI Performance after reports refresh.

Keep notifications batch-based: finish the related copy, internal links, canonical metadata, and sitemap updates first; then send the changed canonical URL set once. Do not use IndexNow as a substitute for Google Search Console.

## Business listings

The Google Business Profile already exists and is awaiting video verification. Do not create a duplicate. The owner must complete Google's video step. Keep the public business name, phone, website, service areas, and service-area business details consistent across listings. The existing owner-verified MyCebu record is linked from the About page and from the site's Organization `sameAs` data.
