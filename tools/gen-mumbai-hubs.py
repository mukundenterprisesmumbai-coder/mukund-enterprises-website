"""Rebuild the Mumbai-region hub pages around 2-day printed delivery, plus the
2-day delivery pillar page. Run from the website repo root."""
import json, re, html

ROOT = "."
tpl = open(f"{ROOT}/locations/thane.html", encoding="utf-8").read()
HEADER = tpl[tpl.index("<body>"):tpl.index('<section class="hero')]
FOOTER = tpl[tpl.index("<footer>"):]
HEAD_ASSETS = tpl[tpl.index('<link rel="icon"'):tpl.index('<script type="application/ld+json">')]

PH = "+91 91378 78456"
PRICES = [
    ("Printed 10x10 ft pop-up canopy", "from ₹4,950 · from 1 pc", "../products/pop-up-canopy-10x10.html"),
    ("Printed gazebo tent", "from ₹5,220 · from 1 pc", "../products/gazebo-tent.html"),
    ("Big umbrella for stall &amp; shop", "from ₹1,799 · from 1 pc", "../products/vendor-umbrella.html"),
    ("Logo-printed garden umbrella", "from ₹584 (6 ft) · min. 12 pcs", "../products/garden-umbrella-with-stand.html"),
    ("Logo-printed umbrellas", "from ₹269 · min. 300 pcs", "../promotional-umbrellas.html"),
    ("Printed promotional table", "from ₹2,961 · from 1 pc", "../products/promotional-advertising-table.html"),
]

HUBS = [
 dict(slug="mumbai", name="Mumbai", short="Mumbai",
  title="Printed Canopy, Gazebo &amp; Umbrellas Mumbai – 2-Day Delivery",
  desc="Logo-printed canopy tents, gazebos and umbrellas delivered in 2 days across Mumbai. Own factory, GST invoice. WhatsApp for a quote in 15 minutes.",
  h1="Printed Canopy Tents, Gazebos &amp; Umbrellas in <em>Mumbai</em>, in 2 Days",
  areas="South Mumbai, Kalbadevi, Dadar, Lower Parel, BKC, Andheri, Goregaon, Malad, Borivali, Kurla, Chembur, Ghatkopar and Mulund",
  route="Our booking office is in Kalbadevi and our factory is in Bhiwandi, about 1.5 to 2 hours from most of Mumbai by road. We deliver across the city and suburbs in our own tempo or by local transport.",
  buyers=["Brands and agencies with stalls at Jio World Convention Centre (BKC), Bombay Exhibition Centre (NESCO, Goregaon) and hotel ballrooms",
          "Shops and hawkers in Crawford Market, Dadar, Lokhandwala and Linking Road who need a big stall umbrella",
          "Banks, insurers and FMCG brands running activation stalls at railway stations, malls and housing societies",
          "Ganeshotsav and Navratri mandals, housing societies and marathon organisers"],
  why="Most Mumbai event requests reach us late: a stall is confirmed on Monday for a Thursday event. Because printing, stitching and framing all happen in our own Bhiwandi factory, we do not wait on an outside printer, so a printed canopy or gazebo can reach a Mumbai venue 2 days after you approve the mock-up.",
  occasions="Exhibition season (November to March), Mumbai Marathon (January), Gudi Padwa and wedding season, Ganeshotsav and Navratri, and pre-monsoon umbrella gifting (April to June).",
  pickup="Collect from our Bhiwandi factory outlet, or book an appointment at the Kalbadevi office.",
  faq_extra=("Can you deliver a printed canopy to a Mumbai exhibition venue?", "Yes. Share the venue, stall number and the setup time. We deliver to Jio World Convention Centre, Bombay Exhibition Centre (NESCO) and hotel venues, and can time delivery for the setup window."),
 ),
 dict(slug="thane", name="Thane", short="Thane",
  title="Printed Canopy Tent &amp; Umbrellas in Thane – 2-Day Delivery",
  desc="Logo-printed canopy tents, gazebos and stall umbrellas delivered in 2 days in Thane, Ghodbunder Road and Wagle Estate. Factory 30 minutes away in Bhiwandi.",
  h1="Printed Canopy Tents &amp; Umbrellas in <em>Thane</em>, in 2 Days",
  areas="Thane West, Ghodbunder Road, Majiwada, Kolshet, Wagle Estate, Naupada, Kalwa, Mumbra and Mira-Bhayandar",
  route="Thane is about 30 to 45 minutes from our Bhiwandi factory, so most Thane orders reach you the day after printing. Our Dombivli West shop is also close for collection.",
  buyers=["Real-estate developers on Ghodbunder Road and Kolshet who need site-launch gazebos and printed canopies",
          "Corporate offices and IT parks in Wagle Estate and Hiranandani Estate",
          "Navratri and Ganeshotsav organisers, including the large Thane garba venues",
          "Malls, retailers and shop owners at Thane station, Gokhale Road and Majiwada"],
  why="Thane is the closest big city to our factory, so it gets the fastest turnaround: a printed 10x10 canopy or gazebo is usually ready in a day and delivered the next.",
  occasions="Builder site launches and property exhibitions, Navratri garba and Ganeshotsav, school and society events, and pre-monsoon umbrella gifting.",
  pickup="Collect from our Bhiwandi factory outlet or Dombivli West shop (by appointment).",
  faq_extra=("Do you deliver to sites on Ghodbunder Road?", "Yes. We deliver to project sites, sales offices and show flats along Ghodbunder Road, Kolshet and Majiwada. Share the site address and contact person with your order."),
 ),
 dict(slug="navi-mumbai", name="Navi Mumbai", short="Navi Mumbai",
  title="Printed Canopy &amp; Gazebo Navi Mumbai – 2-Day Delivery",
  desc="Printed canopy tents, gazebos and stall umbrellas delivered in 2 days in Vashi, APMC, Nerul, Kharghar and Ulwe. Own factory near Mumbai, GST invoice.",
  h1="Printed Canopies, Gazebos &amp; Umbrellas in <em>Navi Mumbai</em>, in 2 Days",
  areas="Vashi, Turbhe, APMC market, Mahape, Airoli, Ghansoli, Nerul, Seawoods, Belapur, Kharghar, Ulwe and the new airport area",
  route="Navi Mumbai is about 1 to 1.5 hours from our Bhiwandi factory by road, so printed canopies and gazebos reach you 2 days after you approve the mock-up.",
  buyers=["Exhibitors at CIDCO Exhibition Centre, Vashi, and events at DY Patil Stadium, Nerul",
          "Traders in the Vashi and Turbhe APMC markets who need big stall umbrellas and shop canopies",
          "Companies in the TTC (Mahape) and Airoli industrial belt for safety weeks and dealer meets",
          "Developers in Kharghar, Ulwe and around Navi Mumbai International Airport for site launches"],
  why="Exhibition and stall bookings at Vashi are often confirmed only days before the show. Our in-house printing means you do not lose a week waiting for an outside printer.",
  occasions="Exhibitions at CIDCO Vashi, cricket and concert events at DY Patil, property expos, and the monsoon gifting season.",
  pickup="Collect from our Bhiwandi factory outlet (by appointment).",
  faq_extra=("Do you supply big umbrellas for APMC market stalls?", "Yes. Our big stall umbrellas (from ₹1,799) and 10x10 canopies can be printed with your shop name and delivered to the Vashi and Turbhe APMC markets in 2 days."),
 ),
 dict(slug="kalyan-dombivli", name="Kalyan &amp; Dombivli", short="Kalyan-Dombivli",
  title="Printed Canopy &amp; Umbrellas Kalyan Dombivli – 2-Day Delivery",
  desc="Printed canopy tents, gazebos and stall umbrellas in Kalyan, Dombivli, Ulhasnagar, Ambernath and Badlapur. Our own shop in Dombivli West. 2-day delivery.",
  h1="Printed Canopies &amp; Umbrellas in <em>Kalyan &amp; Dombivli</em>, in 2 Days",
  areas="Kalyan, Dombivli East and West, Ulhasnagar, Ambernath, Badlapur, Titwala, Shahad and Palava",
  route="Our own shop is in Dombivli West and our factory is in Bhiwandi, about 40 minutes away. Kalyan-Dombivli orders are usually ready the day after you approve the mock-up.",
  buyers=["Wholesalers and shop owners in Ulhasnagar and Kalyan markets",
          "Developers in Palava, Kalyan West and Badlapur for site launches",
          "Companies in Dombivli and Ambernath MIDC",
          "Ganeshotsav and Navratri mandals and Shobha Yatra organisers"],
  why="This is our home ground: walk into our Dombivli West shop (by appointment) to see canopy and umbrella samples, approve your print, and collect the order.",
  occasions="Gudi Padwa Shobha Yatras, Ganeshotsav, Navratri, builder launches and the monsoon season.",
  pickup="Collect from our Dombivli West shop on Ghanshyam Gupte Road or the Bhiwandi factory outlet (by appointment).",
  faq_extra=("Can I see samples at your Dombivli shop?", "Yes. Our Dombivli West shop on Ghanshyam Gupte Road has umbrella and canopy samples. Please book an appointment on WhatsApp before visiting."),
 ),
 dict(slug="bhiwandi", name="Bhiwandi", short="Bhiwandi",
  title="Printed Canopy, Gazebo &amp; Umbrellas in Bhiwandi – Factory",
  desc="Our factory is in Bhiwandi. Printed canopy tents, gazebos and umbrellas, often ready next day, for warehouses, traders and events. Factory pricing.",
  h1="Printed Canopies &amp; Umbrellas from our <em>Bhiwandi</em> Factory",
  areas="Bhiwandi, Dapoda, Mankoli, Vadpe, Kalher, Padgha, Shahapur and the warehousing belt",
  route="Our factory is on Dapoda Road, Bhiwandi. Orders here can usually be collected the day after you approve the mock-up, and we deliver to warehouses and offices across the Bhiwandi belt.",
  buyers=["Warehouses and logistics parks that need shade canopies for loading bays and security posts",
          "Textile and powerloom traders",
          "FMCG and e-commerce distributors running dealer and staff events",
          "Local shops, political offices and event organisers"],
  why="Buying in Bhiwandi means buying straight from the factory: no middleman, factory pricing and the shortest turnaround we offer.",
  occasions="Peak season (after Diwali through August, when the factory runs 24/7), dealer meets, safety weeks, Ganeshotsav and elections.",
  pickup="Collect from our factory outlet: C-14, Gala No. 104, Parashnath Complex, Dapoda Road (by appointment).",
  faq_extra=("Can I visit the factory?", "Yes, by appointment. After Diwali through August the Bhiwandi factory runs 24/7 and you can see samples and production."),
 ),
 dict(slug="vasai-virar-palghar", name="Vasai-Virar &amp; Palghar", short="Vasai-Virar",
  title="Printed Canopy &amp; Umbrellas Vasai-Virar – 2-Day Delivery",
  desc="Printed canopy tents, gazebos, stall and beach umbrellas delivered in 2 days in Vasai, Virar, Nalasopara, Mira Road, Palghar and Boisar.",
  h1="Printed Canopies &amp; Umbrellas in <em>Vasai-Virar &amp; Palghar</em>, in 2 Days",
  areas="Mira Road, Bhayandar, Vasai, Nalasopara, Virar, Palghar, Boisar, Tarapur MIDC and Dahanu",
  route="Vasai-Virar is about 1 to 1.5 hours from our Bhiwandi factory, and Palghar and Boisar about 2 hours. Printed orders reach you 2 days after mock-up approval.",
  buyers=["Shops and market vendors in Vasai, Nalasopara and Virar who need big stall umbrellas",
          "Industrial units in Vasai, Tarapur and Boisar MIDC for safety weeks and staff events",
          "Beach resorts at Arnala, Kelva and Dahanu that need beach and garden umbrellas",
          "Developers in Virar and Mira Road for site launches"],
  why="This area is growing fast and is short of local canopy printers. We print in-house and deliver by road, so Vasai-Virar and Palghar buyers get the same 2-day turnaround as Mumbai.",
  occasions="Resort season (October to May), builder launches, Christmas and church feasts in Vasai, Ganeshotsav and the monsoon season.",
  pickup="Collect from our Bhiwandi factory outlet (by appointment).",
  faq_extra=("Do you supply beach umbrellas for resorts in Palghar?", "Yes. Large beach and garden umbrellas, printed with your resort's name, delivered to Arnala, Kelva and Dahanu. Garden umbrellas start at 12 pieces for printing."),
 ),
 dict(slug="panvel", name="Panvel &amp; Raigad", short="Panvel",
  title="Printed Canopy &amp; Umbrellas Panvel, Raigad – 2-Day Delivery",
  desc="Printed canopy tents, gazebos and stall umbrellas delivered in 2 days in Panvel, Kamothe, Kalamboli, Taloja, Uran and Khopoli. GST invoice.",
  h1="Printed Canopies &amp; Umbrellas in <em>Panvel &amp; Raigad</em>, in 2 Days",
  areas="Panvel, New Panvel, Kamothe, Kalamboli, Kharghar, Taloja MIDC, Uran, JNPT, Pen, Khopoli and Karjat",
  route="Panvel is about 1.5 hours from our Bhiwandi factory. Printed orders reach Panvel, Taloja and Uran 2 days after mock-up approval.",
  buyers=["Companies in Taloja MIDC and the Kalamboli steel market",
          "Logistics and port companies around JNPT and Uran",
          "Developers around Navi Mumbai International Airport, Ulwe and New Panvel",
          "Shops, mandals and event organisers in Panvel and Pen"],
  why="The new airport has brought a wave of projects and events to Panvel. Our in-house printing lets you order a printed canopy for a launch on short notice.",
  occasions="Property expos and site launches, Ganeshotsav (Pen is famous for Ganesh idols), safety weeks and the monsoon season.",
  pickup="Collect from our Bhiwandi factory outlet (by appointment).",
  faq_extra=("Do you deliver to Taloja MIDC and JNPT?", "Yes. Share the company address and gate pass details with your order, and we deliver to Taloja, Kalamboli, Uran and JNPT."),
 ),
 dict(slug="pune", name="Pune", short="Pune",
  title="Printed Canopy Tent &amp; Umbrellas in Pune – 2-Day Delivery",
  desc="Logo-printed canopy tents, gazebos and umbrellas from our factory near Mumbai, delivered to Pune and Pimpri-Chinchwad in 2 days. GST invoice.",
  h1="Printed Canopy Tents &amp; Umbrellas in <em>Pune</em>, in 2 Days",
  areas="Pune city, Pimpri-Chinchwad, Hinjewadi, Wakad, Baner, Kharadi, Magarpatta, Hadapsar, Chakan, Talegaon and Moshi",
  route="Pune is about 3 to 4 hours from our Bhiwandi factory by the Expressway. We print the order and send it by road the next day, so it reaches Pune 2 days after mock-up approval.",
  buyers=["Exhibitors at the Auto Cluster Exhibition Centre (Chinchwad) and the exhibition centre at Moshi",
          "Automotive and manufacturing companies in Chakan, Talegaon and Pimpri-Chinchwad for dealer meets and safety weeks",
          "IT companies in Hinjewadi and Kharadi for employee gifting",
          "Colleges, Ganeshotsav mandals and event agencies"],
  why="Pune has the biggest demand outside Mumbai, but most printed canopies sold there come from Mumbai or Delhi anyway. Ordering straight from our factory skips the middleman and gets your print to Pune in 2 days.",
  occasions="Ganeshotsav (Pune's biggest season), auto expos and dealer launches, college fests, marathons, and pre-monsoon umbrella gifting.",
  pickup="Delivery by road to your office, site or venue in Pune.",
  faq_extra=("How is delivery to Pune charged?", "Delivery is added to your quote based on the order size. Send your Pune pin code with the enquiry and we include it."),
 ),
 dict(slug="nashik", name="Nashik", short="Nashik",
  title="Printed Canopy &amp; Umbrellas Nashik Kumbh – 2-Day Delivery",
  desc="Printed canopy tents, gazebos and stall umbrellas for Nashik and the Simhastha Kumbh 2027, delivered in 2 days from our factory near Mumbai.",
  h1="Printed Canopies &amp; Umbrellas in <em>Nashik</em>, in 2 Days",
  areas="Nashik city, Panchavati, Satpur and Ambad MIDC, Trimbakeshwar, Sinnar, Igatpuri, Niphad and Lasalgaon",
  route="Nashik is about 3 to 4 hours from our Bhiwandi factory by road. We print the order and dispatch it the next day, so it reaches Nashik 2 days after mock-up approval.",
  buyers=["Sponsors, NGOs, banks and stall-holders at the Nashik-Trimbakeshwar Simhastha Kumbh",
          "Wineries and resorts that need branded garden umbrellas",
          "Agri-input, seed and fertiliser companies running farmer meets around Niphad and Lasalgaon",
          "Companies in Satpur, Ambad and Sinnar MIDC"],
  why="The Simhastha Kumbh is the biggest event Nashik will see for 12 years. Help desks, food stalls, sponsor booths and pilgrim shade will all need printed canopies, gazebos and umbrellas, often at short notice. Our 2-day delivery lets you add or replace stalls during the mela.",
  occasions="The Simhastha Kumbh (flag hoisting was scheduled for 31 Oct 2026; Amrit Snan dates reported as 2 Aug, 31 Aug and 11 Sep 2027), the grape harvest and wine festivals, farmer meets, and the monsoon season.",
  pickup="Delivery by road to your site, stall or office in Nashik.",
  faq_extra=("Can you supply canopies and umbrellas for the Nashik Kumbh?", "Yes. We make printed 10x10 canopies, gazebos, stall umbrellas and logo umbrellas for sponsors, NGOs and stall-holders. Book early for the Amrit Snan dates; repeat and top-up orders reach Nashik in 2 days."),
 ),
 dict(slug="lonavala-alibaug", name="Lonavala &amp; Alibaug", short="Lonavala-Alibaug",
  title="Garden Umbrella &amp; Gazebo Lonavala Alibaug – 2-Day Delivery",
  desc="Printed garden umbrellas, gazebos and beach umbrellas for resorts, villas and cafes in Lonavala, Khandala, Karjat and Alibaug. 2-day delivery.",
  h1="Garden Umbrellas &amp; Gazebos in <em>Lonavala &amp; Alibaug</em>, in 2 Days",
  areas="Lonavala, Khandala, Kamshet, Karjat, Matheran foothills, Alibaug, Kihim, Nagaon, Kashid and Murud",
  route="Lonavala and Karjat are about 2.5 to 3 hours from our Bhiwandi factory, and Alibaug about 3 hours. Printed orders reach you 2 days after mock-up approval.",
  buyers=["Resorts, villas and homestays that need garden umbrellas and gazebos for lawns and pools",
          "Beach shacks and cafes in Alibaug, Nagaon and Kashid",
          "Wedding and event planners using resort venues",
          "Corporate offsite organisers"],
  why="Resorts often need replacements just before a long weekend or wedding. With in-house printing, we can brand and deliver new garden umbrellas or a gazebo in 2 days.",
  occasions="Weekend and holiday season (October to May), weddings, corporate offsites, and pre-monsoon replacement.",
  pickup="Delivery by road to your resort, villa or venue.",
  faq_extra=("Can garden umbrellas be printed with our resort's name?", "Yes. Our 6, 7 and 8 ft garden umbrellas can be printed with your resort's name or logo from 12 pieces, and come with a stand if you need one."),
 ),
 dict(slug="surat-vapi", name="Surat, Vapi &amp; South Gujarat", short="Surat-Vapi",
  title="Printed Canopy &amp; Umbrellas Surat, Vapi – 2-Day Delivery",
  desc="Logo-printed canopy tents, gazebos and umbrellas delivered in 2 days to Surat, Vapi, Valsad, Daman and Silvassa from our factory near Mumbai.",
  h1="Printed Canopies &amp; Umbrellas in <em>Surat, Vapi &amp; South Gujarat</em>, in 2 Days",
  areas="Surat, Navsari, Valsad, Vapi GIDC, Umbergaon, Daman and Silvassa",
  route="Vapi is about 3 hours and Surat about 5 to 6 hours from our Bhiwandi factory by road. Printed orders reach South Gujarat 2 days after mock-up approval.",
  buyers=["Textile and diamond traders in Surat for dealer meets and exhibitions",
          "Chemical and pharma units in Vapi GIDC, Daman and Silvassa",
          "Exhibitors at the Surat International Exhibition and Convention Centre",
          "Retailers and distributors across South Gujarat"],
  why="South Gujarat is closer to our factory than most of Maharashtra. Ordering direct gets you factory pricing and a 2-day delivery.",
  occasions="Navratri, the exhibition season, Diwali dealer meets, and the monsoon season.",
  pickup="Delivery by road to your office, factory or venue.",
  faq_extra=("Do you give a GST invoice for Gujarat orders?", "Yes. Every order comes with a GST invoice (IGST for deliveries outside Maharashtra)."),
 ),
]

def faq_list(h):
    return [
        (f"Can you deliver printed canopies and umbrellas in {h['short']} in 2 days?",
         f"Yes. For standard sizes and regular quantities, your printed canopy, gazebo or umbrella reaches {h['short']} within 2 days of mock-up approval and advance payment. For large bulk orders we confirm the date in the quote."),
        h["faq_extra"],
        ("What is the minimum order?",
         "Canopy tents, gazebos, stall umbrellas and promotional tables: from 1 piece. Printed garden umbrellas: 12 pieces. Logo-printed umbrellas: 300 pieces."),
        ("How do I get a price?",
         f"WhatsApp {PH} with the product, quantity, your {h['short']} location, the event date and your logo. We usually reply within 15 minutes."),
    ]

def hub_card_list(current):
    return "".join(f'<li><a href="../locations/{h["slug"]}.html">{h["name"]}</a></li>' for h in HUBS if h["slug"] != current) + '<li><a href="../2-day-delivery.html">2-day printed delivery</a></li><li><a href="../locations/goa.html">Goa</a></li>'

def esc_json(s):
    return html.unescape(s)

def page(h):
    url = f"https://shadowumbrellas.in/locations/{h['slug']}.html"
    nm = esc_json(h["name"])
    faqs = faq_list(h)
    ld = [
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://shadowumbrellas.in/"},
        {"@type": "ListItem", "position": 2, "name": "Areas we serve", "item": "https://shadowumbrellas.in/areas-we-serve.html"},
        {"@type": "ListItem", "position": 3, "name": nm, "item": url}]},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": esc_json(q), "acceptedAnswer": {"@type": "Answer", "text": esc_json(a)}} for q, a in faqs]},
      {"@context": "https://schema.org", "@type": "Service", "name": f"Printed canopy tents, gazebos and umbrellas in {nm} with 2-day delivery",
       "serviceType": "Promotional canopy tent, gazebo and umbrella printing",
       "provider": {"@type": "LocalBusiness", "name": "Mukund Enterprises", "url": "https://shadowumbrellas.in/", "telephone": "+919137878456",
         "address": {"@type": "PostalAddress", "streetAddress": "C-14, Gala No. 104, Parashnath Complex, Dapoda Road", "addressLocality": "Bhiwandi", "postalCode": "421302", "addressRegion": "MH", "addressCountry": "IN"}},
       "areaServed": [{"@type": "Place", "name": a.strip()} for a in esc_json(h["areas"]).replace(" and ", ", ").split(",")]},
    ]
    ldh = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    wa = f"Hi, I am in {nm} and need printed canopies / umbrellas delivered in 2 days."
    q = f"../contact.html?topic=Bulk%20or%20B2B%20order&amp;product=Order%20for%20{h['short'].replace(' ', '%20')}"
    buyers = "".join(f"<li>{b}</li>" for b in h["buyers"])
    prices = "".join(f'<tr><th><a href="{u}">{n}</a></th><td>{p}</td></tr>' for n, p, u in PRICES)
    faqh = "".join(f"<details><summary>{q_}</summary><p>{a}</p></details>" for q_, a in faqs)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{h['title']}</title>
<meta name="description" content="{h['desc']}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{h['title']}">
<meta property="og:description" content="{h['desc']}">
<meta property="og:image" content="https://shadowumbrellas.in/assets/products/pop-up-canopy-10x10.jpg">
<meta property="og:url" content="{url}">
{HEAD_ASSETS}{ldh}</head>
{HEADER}<section class="hero small lp-hero">
  <div class="wrap">
    <p class="crumbs"><a href="../index.html">Home</a> / <a href="../areas-we-serve.html">Areas we serve</a> / {h['name']}</p>
    <p class="eyebrow">2-day printed delivery · {h['name']}</p>
    <h1>{h['h1']}</h1>
    <p class="lead">Logo-printed canopy tents, gazebos, stall umbrellas and promotional umbrellas for {h['areas']}. Printed in our own Bhiwandi factory and delivered within 2 days of your mock-up approval.</p>
    <div class="btns">
      <a class="btn" href="{q}">Get a quote</a>
      <a class="btn ghost" data-wa="{wa}">WhatsApp us</a>
    </div>
  </div>
</section>
<section>
  <div class="wrap two">
    <div><p class="eyebrow">Why 2 days</p><h2>Printed in-house, delivered to <em>{h['name']}</em></h2></div>
    <div><p>{h['why']}</p><p style="margin-top:12px">{h['route']}</p><ul class="ticks" style="margin-top:18px"><li>Day 0: you approve the PDF mock-up and pay the 50% advance</li><li>Day 1: we print, stitch and fit the frame in our Bhiwandi factory</li><li>Day 2: delivered to your office, shop, site or venue</li></ul><p style="margin-top:12px"><small>2-day delivery applies to standard sizes and regular quantities. For large bulk orders, we confirm the delivery date in the quote. <a href="../2-day-delivery.html">How 2-day delivery works</a>.</small></p></div>
  </div>
</section>
<section class="alt">
  <div class="wrap two">
    <div><p class="eyebrow">Who we supply</p><h2>Built for <em>{h['name']}</em> buyers</h2></div>
    <div><ul class="ticks">{buyers}</ul><p style="margin-top:12px"><b>Busy seasons:</b> {h['occasions']}</p></div>
  </div>
</section>
<section>
  <div class="wrap two">
    <div><p class="eyebrow">Price</p><h2>Starting prices for <em>{h['name']}</em></h2></div>
    <div><table class="spec">{prices}</table><p style="margin-top:12px"><small>Starting prices incl. 5% GST, delivery extra depending on the order size. GST invoice with every order. {h['pickup']}</small></p></div>
  </div>
</section>
<section class="alt">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">What we make</p><h2>Products for <em>{h['name']}</em></h2></div>
    <div class="grid g5"><a class="card" href="../canopy-tent-printing.html"><p class="label">2-day delivery</p><h3>Printed canopy tents</h3><p>6x6 to 10x20 ft · from 1 piece</p></a><a class="card" href="../gazebo-tents.html"><p class="label">2-day delivery</p><h3>Gazebo tents</h3><p>Pop-up gazebos · from 1 piece</p></a><a class="card" href="../products/vendor-umbrella.html"><p class="label">2-day delivery</p><h3>Big stall umbrellas</h3><p>For shops and stalls · from 1 piece</p></a><a class="card" href="../promotional-garden-umbrellas.html"><p class="label">2-day delivery</p><h3>Promotional garden umbrellas</h3><p>6, 7 &amp; 8 ft · from 12 pieces</p></a><a class="card" href="../promotional-umbrellas.html"><p class="label">Bulk</p><h3>Promotional umbrellas</h3><p>Logo printed · from 300 pieces</p></a></div>
  </div>
</section>
<section>
  <div class="wrap two">
    <div><p class="eyebrow">FAQ</p><h2>Common <em>questions</em></h2><p class="lead">More answers on our <a href="../faq.html">FAQ page</a>.</p></div>
    <div class="faq">{faqh}</div>
  </div>
</section>
<section class="alt">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Nearby</p><h2>Other 2-day delivery areas</h2></div>
    <ul class="related">{hub_card_list(h['slug'])}</ul>
  </div>
</section>
<section class="band dark">
  <div class="wrap">
    <p class="eyebrow">Need it in 2 days?</p>
    <h2>Send your {h['short']} requirement today</h2>
    <p class="lead">Product, quantity, location, event date and your logo. We usually reply on WhatsApp within 15 minutes.</p>
    <div class="btns"><a class="btn" href="{q}">Send a requirement</a><a class="btn ghost" data-wa="{wa}">WhatsApp us</a></div>
  </div>
</section>
{FOOTER}"""

for h in HUBS:
    t = re.sub("<[^>]+>", "", html.unescape(h["title"]))
    assert len(t) <= 66, (t, len(t))
    assert len(html.unescape(h["desc"])) <= 160, (h["slug"], len(h["desc"]))
    open(f"{ROOT}/locations/{h['slug']}.html", "w", encoding="utf-8").write(page(h))
    print(h["slug"], len(t), len(html.unescape(h["desc"])))

# ---------- pillar page ----------
P_TITLE = "Printed Canopy, Gazebo &amp; Umbrellas in 2 Days | Mumbai"
P_DESC = "Logo-printed canopy tents, gazebos and umbrellas delivered in 2 days across Mumbai, Thane, Navi Mumbai, Pune, Nashik and Surat. Printed in our own factory."
hub_rows = "".join(f'<tr><th><a href="locations/{h["slug"]}.html">{h["name"]}</a></th><td>{h["areas"]}</td></tr>' for h in HUBS)
pfaq = [
 ("Can you really print and deliver a canopy in 2 days?", "Yes. Printing, stitching and framing all happen in our own factory in Bhiwandi, which runs 24/7 from Diwali through August. For standard sizes and regular quantities, your order reaches Mumbai, Thane, Navi Mumbai, Pune, Nashik or South Gujarat within 2 days of mock-up approval and advance payment."),
 ("When does the 2 days start?", "From the time you approve the PDF mock-up and pay the 50% advance. Send your logo (CDR or PDF) with the enquiry so the mock-up is ready quickly."),
 ("Which products can be delivered in 2 days?", "Printed 10x10 pop-up canopies, gazebo tents, canopy tents with side walls, big stall umbrellas, printed garden umbrellas and promotional tables. Logo-printed umbrellas in bulk (300+ pieces) depend on quantity; we confirm the date in the quote."),
 ("Is there an extra charge for 2-day delivery?", "No rush fee. Delivery is charged by city and order size and added to your quote."),
 ("Which areas get 2-day delivery?", "Mumbai, Thane, Navi Mumbai, Kalyan-Dombivli, Bhiwandi, Vasai-Virar and Palghar, Panvel and Raigad, Pune, Nashik, Lonavala and Alibaug, and Surat, Vapi and South Gujarat. We deliver to the rest of India by transport or courier."),
]
pfaqh = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in pfaq)
pld = [
 {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://shadowumbrellas.in/"},
   {"@type": "ListItem", "position": 2, "name": "2-day printed delivery", "item": "https://shadowumbrellas.in/2-day-delivery.html"}]},
 {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pfaq]},
 {"@context": "https://schema.org", "@type": "Service", "name": "2-day printed canopy, gazebo and umbrella delivery", "serviceType": "Promotional canopy tent, gazebo and umbrella printing",
  "provider": {"@type": "LocalBusiness", "name": "Mukund Enterprises", "url": "https://shadowumbrellas.in/", "telephone": "+919137878456"},
  "areaServed": [{"@type": "Place", "name": html.unescape(h["name"])} for h in HUBS]},
]
pldh = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in pld)
root_head = HEAD_ASSETS.replace('href="../', 'href="')
root_header = HEADER.replace('href="../', 'href="')
root_footer = FOOTER.replace('href="../', 'href="').replace('src="../', 'src="')
wa = "Hi, I need printed canopies / umbrellas delivered in 2 days."
qq = "contact.html?topic=Bulk%20or%20B2B%20order&amp;product=2-day%20printed%20delivery"
pillar = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{P_TITLE}</title>
<meta name="description" content="{P_DESC}">
<link rel="canonical" href="https://shadowumbrellas.in/2-day-delivery.html">
<meta property="og:type" content="website">
<meta property="og:title" content="{P_TITLE}">
<meta property="og:description" content="{P_DESC}">
<meta property="og:image" content="https://shadowumbrellas.in/assets/products/pop-up-canopy-10x10.jpg">
<meta property="og:url" content="https://shadowumbrellas.in/2-day-delivery.html">
{root_head}{pldh}</head>
{root_header}<section class="hero small lp-hero">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> / 2-day printed delivery</p>
    <p class="eyebrow">Event in a hurry?</p>
    <h1>Printed Canopies, Gazebos &amp; Umbrellas <em>in 2 Days</em></h1>
    <p class="lead">Your logo on a canopy tent, gazebo, stall umbrella or garden umbrella, printed in our own Bhiwandi factory and delivered across Mumbai, Thane, Navi Mumbai, Pune, Nashik and South Gujarat within 2 days of mock-up approval.</p>
    <div class="btns"><a class="btn" href="{qq}">Get a quote</a><a class="btn ghost" data-wa="{wa}">WhatsApp us</a></div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">How it works</p><h2>From your logo to your venue in <em>2 days</em></h2></div>
    <div class="grid g4 steps"><div class="card step"><p class="label">Day 0</p><h3>Send your logo</h3><p>WhatsApp {PH} with the product, quantity, location, event date and your logo. We send the price and a PDF mock-up, usually the same day.</p></div><div class="card step"><p class="label">Day 0</p><h3>Approve and pay the advance</h3><p>The 2 days start when you approve the mock-up and pay the 50% advance. GST invoice with every order.</p></div><div class="card step"><p class="label">Day 1</p><h3>Printed in-house</h3><p>We print, stitch and fit the frame under one roof in Bhiwandi. No outside printer, so no waiting in someone else's queue.</p></div><div class="card step"><p class="label">Day 2</p><h3>Delivered</h3><p>Delivered to your office, shop, site or event venue, once the balance is paid. Or collect it from our factory outlet.</p></div></div>
  </div>
</section>
<section class="alt">
  <div class="wrap two">
    <div><p class="eyebrow">Why we can</p><h2>Our own <em>factory</em></h2></div>
    <div><p>Most canopy and umbrella sellers buy the frame from one supplier and send the fabric to another printer, which takes a week or more. We do screen and digital printing, stitching and framing in our own factory in Bhiwandi, near Mumbai, which runs 24/7 from Diwali through August.</p><ul class="ticks" style="margin-top:18px"><li>Over a decade in business; founder with about 35 years in umbrellas</li><li>Screen printing for 1 to 3 colour logos, digital printing for any colour</li><li>No rush fee: delivery is charged by city and order size</li></ul><p style="margin-top:12px"><small>2-day delivery applies to standard sizes and regular quantities. For large bulk orders, such as thousands of logo umbrellas, we confirm the date in the quote.</small></p></div>
  </div>
</section>
<section>
  <div class="wrap two">
    <div><p class="eyebrow">Areas</p><h2>Where we deliver in <em>2 days</em></h2></div>
    <div><table class="spec">{hub_rows}</table><p style="margin-top:12px"><small>Rest of India: dispatched by transport or courier, see <a href="areas-we-serve.html">areas we serve</a>.</small></p></div>
  </div>
</section>
<section class="alt">
  <div class="wrap two">
    <div><p class="eyebrow">Price</p><h2>Starting <em>prices</em></h2></div>
    <div><table class="spec">{"".join(f'<tr><th><a href="{u[3:]}">{n}</a></th><td>{p}</td></tr>' for n, p, u in PRICES)}</table><p style="margin-top:12px"><small>Starting prices incl. 5% GST, delivery extra.</small></p></div>
  </div>
</section>
<section>
  <div class="wrap two">
    <div><p class="eyebrow">FAQ</p><h2>2-day delivery <em>questions</em></h2></div>
    <div class="faq">{pfaqh}</div>
  </div>
</section>
<section class="band dark">
  <div class="wrap">
    <p class="eyebrow">Need it this week?</p>
    <h2>Send your requirement now</h2>
    <p class="lead">Product, quantity, location, event date and your logo. We usually reply on WhatsApp within 15 minutes.</p>
    <div class="btns"><a class="btn" href="{qq}">Send a requirement</a><a class="btn ghost" data-wa="{wa}">WhatsApp us</a></div>
  </div>
</section>
{root_footer}"""
open(f"{ROOT}/2-day-delivery.html", "w", encoding="utf-8").write(pillar)
print("pillar", len(html.unescape(P_TITLE)), len(P_DESC))
