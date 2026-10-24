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
- Pages show fast WebP copies, not the .jpg: every `<img>` uses `<name>.webp` with a `srcset` of `<name>-sm.webp` (half width) and `<name>.webp`. After adding or replacing any .jpg in `assets/products|branding|factory|hero`, run `python3 tools/make-images.py` and commit the new .webp files, or the photo shows as the fallback icon. Keep the .jpg: Google Shopping feed, Merchant Center, structured data and og:image use it.
- New `<img>` tags: copy an existing one of the same kind (card, product main photo, gallery) so `srcset`, `sizes`, `width`/`height` and `loading="lazy"` stay right. Only the main product photo is eager with `fetchpriority="high"`.

## Speed & accessibility rules (Nov 2026 batch)
- Fonts: Poppins loads from the `<head>` of each page (preload + swap), never via `@import` in `style.css`. New pages must copy the four font lines from an existing page's `<head>`.
- Analytics (GA4, Clarity) download after the page `load` event — keep it that way.
- Text colours: use `--accent` / `--grey` (darkened for contrast); avoid lighter greys than #6B6B6B on light backgrounds.
- Footer column titles are `<h2 class="fh">` (not h4) so heading levels never skip.
