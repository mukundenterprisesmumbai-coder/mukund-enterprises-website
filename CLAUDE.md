# Mukund Enterprises website

Static website (plain HTML/CSS/JS, no build step) for Mukund Enterprises — promotional umbrella, canopy tent and gazebo manufacturer & wholesaler, Kalbadevi (Mumbai) and Dombivli West.

Owner is non-technical: explain changes in plain language and show a preview after every change.

## Files
- `index.html`, `products.html`, `about.html`, `contact.html` — the four pages
- `style.css` — all styling; `script.js` — phone number, WhatsApp links, menu, product filter, contact-form prefill
- `products/*.html` — one SEO page per product; `faq.html` — FAQ
- Keyword landing pages: `promotional-umbrellas.html`, `promotional-garden-umbrellas.html`, `canopy-tent-printing.html`, `gazebo-tents.html`, `corporate-gift-umbrellas.html`; buyer pages in `industries/`; city pages in `locations/`; hub `areas-we-serve.html`. Linked from every footer ("For businesses") and listed in `sitemap.xml`.
- Analytics: fill `ga4` / `clarity` IDs in `SITE` at the top of `script.js` (blank = off). Events: whatsapp_click, price_request, call_click, quote_click, generate_lead.
- Deploys cost Netlify credits: batch changes and deploy only on the owner's go-ahead.
- `assets/umbrella.svg`, `assets/tent.svg` — fallback icons shown when a product photo is missing
- `assets/products/` — product photos

## Product photos
- Each product card in `products.html` loads `assets/products/<name>.jpg`; the expected names are listed in `assets/products/README-file-names.txt`.
- Names must match exactly: lowercase, hyphens, `.jpg`.
- Before adding a photo, check its real format (owner's photos are sometimes PNGs renamed to .jpg). Convert to a real JPEG, max 800×800, quality ~82, progressive — target under ~150 KB.
- After adding or replacing any photo in `assets/products`, `assets/branding`, `assets/factory` or `assets/hero`, run `python3 tools/make-avif.py` (needs Pillow with AVIF). It makes the smaller AVIF copies at the same pixel size. Pages show them through `<picture><source type="image/avif" ...>` around the `<img>`, with the JPG as fallback; new `<img>` tags for these photos should get the same wrapper.
- Browser caching is set in `_headers`: photos are cached for 30 days, so give a replaced photo a new file name.

## Speed
- Poppins is self-hosted in `assets/fonts/` (latin + latin-ext, weights 400-700); every page preloads the 4 latin files. Don't add Google Fonts links back.
- On `products.html` only the first card photo loads eagerly (`fetchpriority="high"`); the rest stay `loading="lazy"`.

## Lead pages and extras (31 Oct 2026)
- `bulk-government-orders.html` and `monsoon-umbrella-booking.html`: lead pages linked from every footer ("For businesses") and the sitemap. Built by a one-off script; edit the HTML directly.
- The floating WhatsApp button (`a.wa`) is pre-filled by `script.js` with the page's H1 and URL (home page keeps the generic text).
- Catalogue PDF is linked from Home, Products, Promotional umbrellas and the two lead pages; clicks are tracked as `catalogue_download`. Keep it near 3 MB (images recompressed with PyMuPDF `rewrite_images`, quality 62, 144 dpi).
- Home page has a "What our buyers say" block with 4 Google reviews (same texts as the review pop-up).
