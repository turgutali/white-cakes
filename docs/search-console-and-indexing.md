# Search Console, Bing, and indexing

## Automatic discovery for participating search engines

On each push to `main` that changes HTML pages, GitHub Actions submits their canonical URLs to IndexNow. The public key file is hosted at the site root so participating engines can verify it. IndexNow notifications can speed discovery, but do not guarantee crawling, indexing, or ranking. Google does not use IndexNow.

The workflow runs `python3 scripts/submit_indexnow.py <before-sha> <after-sha>`. To send all indexable HTML pages manually, run `python3 scripts/submit_indexnow.py` from a checkout of the target commit.

## Google Search Console

The sitemap is published at <https://www.thewhitecakes.com/sitemap.xml>. Submit it in Search Console, then use URL Inspection for the homepage and highest-priority service pages when access is available. A sitemap and a crawl request help Google discover URLs; neither guarantees indexing or rankings. Google says a new site may simply be too new and crawling can take days or weeks.

Use the `info@thewhitecakes.com` Google account for White Cakes properties. That account currently reports that it does not have access to `https://www.thewhitecakes.com/`. A property owner needs to add it as a full user or owner before URL Inspection and the performance reports are available there.

## Bing Webmaster Tools

The sitemap can also be submitted in Bing Webmaster Tools. IndexNow notifications are automatic; use Bing Webmaster Tools to inspect its IndexNow activity and indexing status.

## Business listings

Keep business name, phone, service areas, website, and service-area business details consistent across public listings. The business has a Google Business Profile awaiting video verification; do not create a duplicate listing.
