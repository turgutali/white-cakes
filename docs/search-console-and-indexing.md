# Search Console, Bing, and indexing

## Current verified state (2026-11-19)

- The live sitemap contains 197 unique URLs, including 179 Journal articles (excluding the `/journal/` index). The newly added articles checked after deployment returned HTTP 200 and declared their own canonical URLs. This establishes fetchability for those checked URLs, not that Google has crawled or indexed them.
- The public robots file permits Googlebot, Bingbot, OAI-SearchBot, GPTBot, ClaudeBot, and PerplexityBot. `llms.txt` lists the current service areas, prices, key pages, and Journal articles.
- On 2026-11-19, after the journal content work was live, IndexNow accepted seven updated article URLs in one request (HTTP 200). The follow-up Cebuano pricing update changed `/journal/asa-magpa-order-cake-cebu.html` and `/journal/`; IndexNow accepted both in one request (HTTP 200). After the order-wizard image description update, IndexNow accepted `/order/` (HTTP 200). These notifications inform IndexNow-participating engines; they are not Google indexing requests or guarantees.
- After the 2026-11-19 trilingual content deployment, IndexNow accepted 175 changed canonical URLs in one request (HTTP 200). This is a notification only, not a crawl or indexing guarantee.
- After removing draft markers, fixing empty localized titles, and adding DTI business identity, IndexNow accepted 37 changed canonical URLs in one request (HTTP 200).
- A Google search snapshot for `cake delivery Cebu City` localized to Cebu did not show The White Cakes in the visible local or organic results. In a separate signed-out Google session whose displayed location was Singapore, `site:https://www.thewhitecakes.com/` returned no results. This is an indexing warning, not an index count: Google says `site:` results are incomplete and URL Inspection is more reliable ([Google Search operator documentation](https://developers.google.com/search/docs/monitor-debug/search-operators/all-search-site)).

## Google Search Console

The property is signed in under `info@thewhitecakes.com`. On 2026-11-19, the final 197-URL sitemap was successfully resubmitted from Brave. Search Console reports `Success` and 197 discovered pages. This confirms sitemap processing and discovery, not that every page is indexed or ranking.

The Page indexing report was still processing. The latest three-month Performance report showed 14 impressions, 0 clicks, 0% CTR, and average position 14.8, with data only through 2026-11-16. This sample is too small to support a broad demand forecast.

URL Inspection results on 2026-11-19:

- `/journal/paghahatid-cake-cebu.html` (Tagalog delivery guide) is indexed.
- `/journal/unsa-ang-bento-cake-cebu.html` (Cebuano Bento guide) passed a live URL test and its indexing request was accepted; Search Console showed it queued for priority crawling.
- `/journal/ano-ang-bento-cake-cebu.html` (Tagalog Bento guide) was previously unknown to Google. Its live URL test passed and showed it can be indexed, but the individual indexing request failed because the daily quota had been exceeded. Retry after the quota resets; the sitemap is also submitted as a discovery path.

Individual recrawl requests are quota-limited and do not guarantee inclusion. Use the sitemap for the full page set and URL Inspection for a small number of priority pages.

The 950 multilingual content items are integrated as reader questions and answers across the existing topic pages and localized companion pages; they were not published as 950 separate URLs. A source audit found 65 English, 57 Cebuano, and 57 Tagalog Journal articles. It also found recurring planning-question structures across many localized pages; localized copy still needs native editorial review, and repeated frameworks should be differentiated where they do not add topic-specific value. On 2026-11-19, the Cebuano and Tagalog flavour and price guides were expanded with menu-specific choice, quote, delivery, and deposit details and reciprocal internal links. The Tagalog birthday-cake message guide was rewritten to remove a truncated lead-in/meta description and add recipient-specific message examples and a text-fit checklist. A metadata audit found four localized descriptions under 80 characters and six identical, truncated snippets across baby shower, bridal shower and First Communion pages; all ten descriptions were rewritten to match each page. Editor-only translation marker paragraphs and empty localized page titles were removed or repaired on 2026-11-19. Do not treat the current 950 embedded questions as 950 standalone blog posts.

The About page and Organization entity now identify the DTI-registered business name `THE WHTE CAKES SHOP` (National scope), Business Name No. 8628157, valid November 19, 2026 through November 19, 2031. The certificate states that business-name registration is not a license to operate; the site does not imply otherwise.

Do not claim Google indexing solely because a URL is in the sitemap, appears in a `site:` query, or was sent through IndexNow. Google Search Console is the source for URL-level index status and site performance.

## Bing and IndexNow

On 2026-11-18, Bing Webmaster Tools recorded a 59-URL sitemap submission as Processing; its previous read showed 58 URLs. IndexNow accepted the 59-URL set. On 2026-11-19, after the current page batch was complete, IndexNow accepted `/cake-delivery-cebu-city/` and `/about/` together. Recheck Bing Webmaster Tools for sitemap processing, search queries, and AI Performance after reports refresh.

Keep notifications batch-based: finish the related copy, internal links, canonical metadata, and sitemap updates first; then send the changed canonical URL set once. Do not use IndexNow as a substitute for Google Search Console.

## Business listings

The Google Business Profile already exists and is awaiting video verification. Do not create a duplicate. The owner must complete Google's video step. Keep the public business name, phone, website, service areas, and service-area business details consistent across listings. The existing owner-verified MyCebu record is linked from the About page and from the site's Organization `sameAs` data.
