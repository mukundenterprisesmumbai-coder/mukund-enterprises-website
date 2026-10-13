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
