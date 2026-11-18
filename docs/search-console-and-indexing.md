# Search Console, Bing, and indexing

## Automatic discovery for participating search engines

During the current SEO cleanup, the workflow is manual-only so intermediate site edits are not announced as final. After the content and technical changes are complete, run the workflow once with `workflow_dispatch`; an empty `before` value makes the script submit every tracked, indexable HTML URL. Then restore the push trigger for future site releases. The public key file is hosted at the site root. IndexNow notifications can speed discovery for participating engines, but do not guarantee crawling, indexing, or ranking. Google does not use IndexNow.

## Google Search Console

The `https://www.thewhitecakes.com/` property is available in Search Console under `info@thewhitecakes.com`. The `/sitemap.xml` report is successful. As of 2026-11-18, the page-indexing and performance reports were still processing; URL Inspection showed the Red Velvet guide as indexed with a valid breadcrumb. Wait until the SEO edits are complete, then submit the sitemap once and request priority crawling for the homepage and key commercial pages. A sitemap and crawl request help discovery, but do not guarantee indexing or ranking.

## Bing Webmaster Tools

The sitemap can also be submitted in Bing Webmaster Tools. Once the SEO cleanup is complete, run the manual IndexNow workflow and use Bing Webmaster Tools to inspect its activity and indexing status.

## Business listings

Keep business name, phone, service areas, website, and service-area business details consistent across public listings. The business has a Google Business Profile awaiting video verification; do not create a duplicate listing.
