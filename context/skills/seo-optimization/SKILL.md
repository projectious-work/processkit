---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-seo-optimization
  name: seo-optimization
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "SEO — on-page, technical, structured data, Core Web Vitals, and mobile-first indexing."
  category: meta
  layer: null
  when_to_use: "Use when optimizing a website for search engines, adding meta tags or structured data, fixing Core Web Vitals, or auditing technical SEO."
---

# SEO Optimization

## Level 1 — Intro

SEO is two jobs: make the page understandable to crawlers (titles,
headings, structured data, sitemap, canonicals) and make it fast and
usable for humans (Core Web Vitals, mobile, HTTPS). Both feed the
same ranking signals.

## Level 2 — Overview

### On-page SEO

- **Title tags:** unique per page, 50–60 characters, primary
  keyword near the start.
- **Meta descriptions:** 120–160 characters, with a call to action,
  unique per page.
- **Headings:** one `<h1>` per page matching the topic; logical
  `<h2>`–`<h6>` hierarchy without skipping levels.
- **Alt text:** descriptive, concise (≤125 chars), keywords used
  naturally. Decorative images use `alt=""`.
- **Internal links:** descriptive anchor text — never "click here".
- **URLs:** short, lowercase, hyphen-separated, include the
  primary keyword.
- **Content:** answer the user's query comprehensively; use
  related terms naturally rather than keyword-stuffing.

### Crawling and indexing

- **robots.txt** at the site root: allow important paths, block
  admin and staging.
- **XML sitemap** lists all indexable pages, excludes `noindex`
  pages, submitted to Search Console.
- **Canonicals** on every page (`<link rel="canonical">`) to
  prevent duplicate content.
- **Hreflang** for multilingual sites
  (`<link rel="alternate" hreflang="en">` per language) with a
  self-referencing entry and `x-default`.
- **HTTP status codes:** 200 for live, 301 for permanent redirects,
  404 for gone. No soft 404s.
- **Redirect chains:** at most one hop. Fix chains to point
  directly to the final URL.
- **Index control:** `<meta name="robots" content="noindex">` on
  pages that should not rank.

### Structured data (JSON-LD)

- Use JSON-LD in `<script type="application/ld+json">` in the
  `<head>`. Prefer it over Microdata or RDFa.
- Common types: `Article`, `Product`, `FAQPage`, `BreadcrumbList`,
  `Organization`, `LocalBusiness`.
- `@context: "https://schema.org"` and the most specific `@type`
  available.
- Match structured data to visible page content — never add data
  that is not shown on the page.
- Validate with Google Rich Results Test before deploying.
- Add `BreadcrumbList` for hierarchical navigation.

### Core Web Vitals

- **LCP (Largest Contentful Paint):** target < 2.5s. Preload the
  LCP image, use responsive `srcset`, inline critical CSS, defer
  non-critical stylesheets.
- **INP (Interaction to Next Paint):** target < 200ms. Break up
  long tasks (>50ms) with `requestIdleCallback` or
  `scheduler.yield()`. Minimize main-thread work in interaction
  handlers. Debounce rapid input events.
- **CLS (Cumulative Layout Shift):** target < 0.1. Set explicit
  `width` and `height` on images and video. Reserve space for ads
  and embeds. Avoid inserting content above the fold after initial
  render. Use `font-display: swap` with preloaded fonts.

### Page speed

- Inline critical CSS and defer non-critical JS.
- Compress images with WebP/AVIF and provide fallbacks; lazy-load
  below-fold images.
- Enable HTTP/2 or HTTP/3 for multiplexed requests.
- Serve static assets from a CDN to reduce TTFB.
- Minify HTML/CSS/JS and enable Brotli or gzip.
- Audit with Lighthouse: `npx lighthouse <url> --output=json`.

### Mobile-first indexing

- Google indexes the mobile version, so ensure content parity with
  desktop.
- Responsive design preferred: same URL, same HTML, CSS adapts.
- Viewport tag:
  `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- Base font size at least 16px so text is readable without zooming.
- No horizontal scrolling at any viewport width.
- Touch targets ≥ 48×48 CSS pixels with 8px spacing.
- Verify with Chrome DevTools device emulation and Google's
  Mobile-Friendly Test.

## Level 3 — Full reference

### Internal linking

- Link from high-authority pages to important pages that need
  ranking signals.
- Create content hubs: a pillar page links to cluster pages and
  back.
- Limit links per page to a reasonable number (under ~100).
- Fix orphan pages — every indexable page should be reachable via
  internal links.
- Use breadcrumbs for hierarchical navigation and search engine
  context.

### Security and trust

- Serve every page over HTTPS.
- Set HSTS:
  `Strict-Transport-Security: max-age=31536000; includeSubDomains`.
- No mixed content (HTTP resources on HTTPS pages).
- Set `X-Content-Type-Options: nosniff` and `X-Frame-Options`.
- Configure a Content Security Policy.
- Surface E-E-A-T signals: author bios, about pages, contact info,
  reviews and certifications where relevant.

### Technical SEO checklist

A condensed actionable checklist (full version in
`references/technical-seo-checklist.md`):

**Crawling and indexing**

- [ ] `robots.txt` exists; allows important paths, blocks admin
- [ ] XML sitemap lists indexable pages and is submitted to
  Search Console and Bing Webmaster Tools
- [ ] No orphan pages
- [ ] Redirect chains resolved (max 1 hop), no loops
- [ ] 404s return real 404 status (not soft 404)
- [ ] Removed pages return 410 or redirect to relevant content

**Canonicals and duplicates**

- [ ] Every page has a self-referencing or preferred canonical
- [ ] Pagination uses sensible canonical strategy (not all to
  page 1)
- [ ] WWW vs non-WWW redirects configured to one canonical
- [ ] Trailing-slash behavior consistent
- [ ] HTTP redirects to HTTPS

**Performance**

- [ ] LCP < 2.5s, INP < 200ms, CLS < 0.1
- [ ] Images have explicit `width`/`height`
- [ ] Above-fold images preloaded; below-fold use `loading="lazy"`
- [ ] Fonts preloaded with `font-display: swap`
- [ ] Critical CSS inlined; non-critical CSS deferred
- [ ] JavaScript deferred or async where possible
- [ ] Brotli/gzip enabled, static assets from CDN

**Structured data**

- [ ] JSON-LD format
- [ ] `@context` is `https://schema.org`
- [ ] Most specific `@type` used
- [ ] Fields match visible content
- [ ] Validates clean in Google Rich Results Test
- [ ] `BreadcrumbList` on hierarchical pages

### JSON-LD examples

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": { "@type": "Person", "name": "Author Name" },
  "datePublished": "2025-01-15",
  "image": "https://example.com/image.jpg"
}
```

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "image": "https://example.com/product.jpg",
  "description": "Product description",
  "offers": {
    "@type": "Offer",
    "price": "29.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  }
}
```

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is the return policy?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "You can return items within 30 days."
    }
  }]
}
```

### Anti-patterns

- Stuffing keywords into titles, alt text, or body copy
- Adding structured data that does not match visible content
- Using "click here" or bare URLs as anchor text
- Letting redirect chains accumulate over time
- Lazy-loading the LCP image (defeats the preload)
- Treating mobile as an afterthought when Google indexes mobile
  first
- Blocking CSS or JS in `robots.txt` — Googlebot needs them to
  render

### References

- `references/technical-seo-checklist.md` — full checklist by
  category
- [Google Search Central](https://developers.google.com/search)
- [web.dev Core Web Vitals](https://web.dev/vitals/)
