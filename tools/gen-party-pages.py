#!/usr/bin/env python3
"""Builds the political-party pages (parties/*.html) and the hub
political-party-umbrellas.html. Re-run after editing PARTIES below; it
overwrites those files. Head, header and footer are copied from
elections/uttar-pradesh.html so they stay in sync with the rest of the site.

No party logos or artwork are used anywhere: party names and symbols are
named in text only, and every page says we are not affiliated with any party.
"""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://shadowumbrellas.in/"
TPL = (ROOT / "elections/uttar-pradesh.html").read_text(encoding="utf-8")
HEAD_LINKS = re.search(r'(<link rel="icon".*?<link rel="stylesheet" href="../style.css">)', TPL, re.S).group(1)
HEADER = re.search(r"(<header>.*?</header>)", TPL, re.S).group(1)
FOOTER = re.search(r"(<footer>.*?</html>)", TPL, re.S).group(1)

ELECTIONS = {
    "uttar-pradesh": ("Uttar Pradesh", "Assembly, expected Feb to Mar 2027"),
    "punjab": ("Punjab", "Assembly, expected Feb to Mar 2027"),
    "uttarakhand": ("Uttarakhand", "Assembly, expected Feb to Mar 2027"),
    "tamil-nadu": ("Tamil Nadu", "Urban local bodies, expected early 2027"),
    "gujarat": ("Gujarat", "Assembly, expected Dec 2027"),
    "himachal-pradesh": ("Himachal Pradesh", "Assembly, expected Nov 2027"),
}
MUMBAI_HUBS = [("mumbai", "Mumbai"), ("thane", "Thane"), ("navi-mumbai", "Navi Mumbai"),
               ("kalyan-dombivli", "Kalyan &amp; Dombivli"), ("pune", "Pune"), ("nashik", "Nashik")]

MR = "पक्षाचे रंग आणि चिन्ह छापलेल्या छत्र्या, कॅनोपी आणि गझेबो – घाऊक दरात, संपूर्ण महाराष्ट्रात डिलिव्हरी."
HI = "पार्टी के रंग और चुनाव चिह्न वाले छाते, कैनोपी और गज़ेबो टेंट – थोक में, पूरे भारत में डिलीवरी।"

# slug, short name (title/H1), full name, local-language search name, symbol,
# colours (None = not stated), where active, election page slugs,
# Maharashtra party?, a unique paragraph, a local-language line (lang, text)
PARTIES = [
    dict(slug="bjp", short="BJP", full="Bharatiya Janata Party (BJP)", local="भाजपा छाता",
         symbol="lotus (kamal)", colours="saffron and green",
         active="every state", elections=["uttar-pradesh", "uttarakhand", "gujarat", "himachal-pradesh", "punjab"], mh=True,
         para="BJP units are among the biggest bulk buyers of campaign umbrellas: mandal and booth committees order saffron-and-green umbrellas for karyakartas, and candidates order lotus-printed canopy tents for booth tables and nukkad sabhas. With assembly polls due in Uttar Pradesh, Uttarakhand, Punjab, Gujarat and Himachal Pradesh in 2027, orders for the same weeks pile up, so district units that book early get their dates.",
         line=("hi", "भाजपा के केसरिया-हरे रंग और कमल चिह्न वाले छाते, कैनोपी और गज़ेबो – थोक में, हर ज़िले में डिलीवरी।")),
    dict(slug="congress", short="Congress", full="Indian National Congress (INC)", local="कांग्रेस छाता",
         symbol="hand (haath / panja)", colours="the tricolour: saffron, white and green",
         active="every state", elections=["punjab", "uttar-pradesh", "uttarakhand", "himachal-pradesh", "gujarat"], mh=True,
         para="Congress committees usually want the tricolour in the right order on the panels, with the hand symbol and the candidate's photo on one or two panels. A 3-colour screen print keeps the cost low on large runs; digital printing is better when the candidate's photo goes on the umbrella. Punjab, Himachal Pradesh, Uttarakhand, Uttar Pradesh and Gujarat all vote in 2027.",
         line=("hi", "कांग्रेस के तिरंगे और हाथ (पंजा) चिह्न वाले छाते और कैनोपी – थोक में, पूरे भारत में डिलीवरी।")),
    dict(slug="aap", short="AAP", full="Aam Aadmi Party (AAP)", local="आम आदमी पार्टी छाता",
         symbol="broom (jhadu)", colours=None,
         active="Punjab, Delhi, Gujarat and Goa", elections=["punjab", "gujarat", "uttarakhand"], mh=False,
         para="AAP campaigns lean on volunteers going door to door, so the usual order is a large run of plain-colour umbrellas with the broom symbol and a one-line message, plus a few canopy tents for help desks. Punjab votes in early 2027 and Gujarat later in 2027; Goa, also expected in early 2027, is served from our Mumbai base.",
         line=("pa", "ਪਾਰਟੀ ਦੇ ਰੰਗ ਅਤੇ ਚੋਣ ਨਿਸ਼ਾਨ ਵਾਲੀਆਂ ਛਤਰੀਆਂ ਅਤੇ ਕੈਨੋਪੀ – ਥੋਕ ਵਿੱਚ, ਪੂਰੇ ਪੰਜਾਬ ਵਿੱਚ ਡਿਲੀਵਰੀ।")),
    dict(slug="samajwadi-party", short="Samajwadi Party", full="Samajwadi Party (SP)", local="समाजवादी पार्टी छाता",
         symbol="bicycle (cycle)", colours="red and green",
         active="Uttar Pradesh", elections=["uttar-pradesh"], mh=False,
         para="Samajwadi Party orders are almost all for Uttar Pradesh, where all 403 seats vote in early 2027. Red-and-green umbrellas with the cycle symbol work well for workers at rallies, and a 10x10 ft canopy printed on three sides makes a booth that people recognise from across the road. We deliver to district towns such as Azamgarh, Etawah, Mainpuri and Ballia, not just Lucknow.",
         line=("hi", "समाजवादी पार्टी के लाल-हरे रंग और साइकिल चिह्न वाले छाते और कैनोपी – थोक में, यूपी के हर ज़िले में डिलीवरी।")),
    dict(slug="bsp", short="BSP", full="Bahujan Samaj Party (BSP)", local="बसपा छाता",
         symbol="elephant (haathi)", colours="blue",
         active="Uttar Pradesh, Punjab and Uttarakhand", elections=["uttar-pradesh", "punjab", "uttarakhand"], mh=False,
         para="BSP's blue is a single solid colour, which keeps printing simple: a blue umbrella with a white elephant symbol and the candidate's name is a 1 or 2-colour screen print, among the cheapest per piece at 300 pieces and above. Uttar Pradesh, Punjab and Uttarakhand all vote in early 2027.",
         line=("hi", "बसपा के नीले रंग और हाथी चिह्न वाले छाते और कैनोपी – थोक में, यूपी, पंजाब और उत्तराखंड में डिलीवरी।")),
    dict(slug="shiv-sena", short="Shiv Sena", full="Shiv Sena and Shiv Sena (UBT)", local="शिवसेना छत्री",
         symbol="bow and arrow (Shiv Sena) or flaming torch, mashaal (Shiv Sena UBT)", colours="saffron",
         active="Mumbai, Thane and the rest of Maharashtra", elections=[], mh=True,
         para="We are a Mumbai manufacturer with a factory in Bhiwandi, so Shiv Sena shakhas and corporators in Mumbai, Thane, Kalyan-Dombivli and Navi Mumbai can get printed umbrellas and canopies within 2 days of approving the mock-up. Saffron umbrellas are ordered in the thousands before the monsoon, and canopies for shakha events and festival pandals. We print for both Shiv Sena and Shiv Sena (UBT) units, each with its own symbol.",
         line=("mr", MR)),
    dict(slug="ncp", short="NCP", full="Nationalist Congress Party (NCP) and NCP (Sharadchandra Pawar)", local="राष्ट्रवादी छत्री",
         symbol="clock (NCP) or a man blowing a turha (NCP-SP)", colours=None,
         active="Maharashtra, especially Pune, western Maharashtra and Mumbai", elections=[], mh=True,
         para="NCP units in Pune, Baramati, Satara, Nashik and Mumbai order printed umbrellas for workers and canopy tents for janata darbars and local events. Pune and Nashik are within our 2-day delivery area from Bhiwandi. We print for both NCP and NCP (SP) units, each with its own symbol and colours.",
         line=("mr", MR)),
    dict(slug="mns", short="MNS", full="Maharashtra Navnirman Sena (MNS)", local="मनसे छत्री",
         symbol="railway engine", colours="saffron",
         active="Mumbai, Thane, Nashik and Pune", elections=[], mh=True,
         para="MNS shakhas in Mumbai, Thane, Kalyan-Dombivli, Nashik and Pune order umbrellas and canopies for ward events, monsoon drives and help camps. Because we print in Bhiwandi, a Mumbai-region order is usually ready within 2 days of approving the mock-up, which helps when an event is announced at short notice.",
         line=("mr", MR)),
    dict(slug="tmc", short="TMC", full="All India Trinamool Congress (TMC)", local="তৃণমূল ছাতা",
         symbol="twin flowers and grass (jora ghas phool)", colours=None,
         active="West Bengal", elections=[], mh=False, kolkata=True,
         para="Trinamool units in Kolkata and across West Bengal order party umbrellas for workers and canopy tents for para events, Durga Puja season and the Kolkata Municipal Corporation election, which is due by December 2026. We dispatch by transport to Kolkata and district towns.",
         line=("bn", "দলের রঙ ও প্রতীক ছাপা ছাতা, ক্যানোপি ও গেজেবো – পাইকারি দামে, সারা পশ্চিমবঙ্গে ডেলিভারি।")),
    dict(slug="dmk", short="DMK", full="Dravida Munnetra Kazhagam (DMK)", local="திமுக குடை",
         symbol="rising sun", colours="black and red",
         active="Tamil Nadu and Puducherry", elections=["tamil-nadu"], mh=False,
         para="DMK's black-and-red is printed as alternating panels or as a red band on a black umbrella, with the rising sun symbol. Tamil Nadu's urban local body elections are expected in early 2027, which means ward-level candidates in many towns, each needing a few hundred umbrellas and a canopy or two.",
         line=("ta", "கட்சி வண்ணம் மற்றும் சின்னம் அச்சிட்ட குடைகள், கேனோபி – மொத்தமாக, தமிழ்நாடு முழுவதும் டெலிவரி.")),
    dict(slug="aiadmk", short="AIADMK", full="All India Anna Dravida Munnetra Kazhagam (AIADMK)", local="அதிமுக குடை",
         symbol="two leaves", colours="black, white and red",
         active="Tamil Nadu and Puducherry", elections=["tamil-nadu"], mh=False,
         para="AIADMK's black, white and red stripes need a 3-colour print or a digital print on each panel, with the two leaves symbol on one or two panels. With Tamil Nadu's urban local body elections expected in early 2027, ward candidates across the state need umbrellas and canopies at the same time, so early orders get the best dates.",
         line=("ta", "கட்சி வண்ணம் மற்றும் சின்னம் அச்சிட்ட குடைகள், கேனோபி – மொத்தமாக, தமிழ்நாடு முழுவதும் டெலிவரி.")),
    dict(slug="akali-dal", short="Akali Dal", full="Shiromani Akali Dal (SAD)", local="ਅਕਾਲੀ ਦਲ ਛਤਰੀ",
         symbol="scales (taraju)", colours=None,
         active="Punjab", elections=["punjab"], mh=False,
         para="Shiromani Akali Dal candidates in Punjab's 117 seats need umbrellas for workers and canopies for village meetings ahead of the early 2027 assembly election. We deliver to district towns such as Bathinda, Moga, Sangrur and Hoshiarpur, not just Ludhiana and Amritsar.",
         line=("pa", "ਪਾਰਟੀ ਦੇ ਰੰਗ ਅਤੇ ਚੋਣ ਨਿਸ਼ਾਨ ਵਾਲੀਆਂ ਛਤਰੀਆਂ ਅਤੇ ਕੈਨੋਪੀ – ਥੋਕ ਵਿੱਚ, ਪੂਰੇ ਪੰਜਾਬ ਵਿੱਚ ਡਿਲੀਵਰੀ।")),
]

PRODUCTS = [
    ("promotional-umbrellas.html", "Printed umbrellas", "For karyakartas, volunteers and rallies · from ₹269 · min. 300 pcs"),
    ("canopy-tent-printing.html", "Printed canopy tents", "Booths, nukkad sabhas, help desks · from ₹4,950 · from 1 pc"),
    ("gazebo-tents.html", "Gazebo tents", "Party offices and campaign desks · from ₹5,220"),
    ("promotional-garden-umbrellas.html", "Garden umbrellas", "Party office seating · from ₹584 (6 ft) · min. 12 pcs"),
]
PRICE_NOTE = "Starting prices incl. GST (5% on umbrellas, 18% on canopies and gazebos), delivery extra. Final price depends on quantity and printing."
DISCLAIMER = "Mukund Enterprises is an independent manufacturer and is not affiliated with or endorsed by any political party. Party names are used only to describe the printing we do for party units and candidates, who supply their own approved artwork."

e = html.escape


def head(title, desc, url, p, schemas):
    s = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in schemas)
    links = HEAD_LINKS if p == "../" else HEAD_LINKS.replace('"../', '"')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}assets/products/promotional-umbrella.jpg">
<meta property="og:url" content="{url}">
{links}
{s}
</head>
<body>
"""


def chrome(p):
    h = HEADER if p == "../" else HEADER.replace('"../', '"')
    f = FOOTER if p == "../" else FOOTER.replace('"../', '"')
    return h, f


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs]}


def faq_html(faqs):
    return "".join(f"<details><summary>{e(q)}</summary><p>{a}</p></details>" for q, a in faqs)


def crumbs_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def products_table(p):
    rows = "".join(f'<tr><th><a href="{p}{h}">{n}</a></th><td>{t}</td></tr>' for h, n, t in PRODUCTS)
    return f'<table class="spec">{rows}</table><p style="margin-top:12px"><small>{PRICE_NOTE}</small></p>'


def party_page(d):
    p = "../"
    url = f"{SITE}parties/{d['slug']}.html"
    s = d["short"]
    sp = s if "Party" in s else s + " Party"
    sym_short = "party" if " or " in d["symbol"] else d["symbol"].split(" (")[0]
    title = f"{s} Umbrellas & Canopy Tents, Printed in Bulk"
    if len(title) > 60:
        title = f"{s} Umbrellas & Canopies, Printed in Bulk"
    colour_txt = f" in {d['colours']}" if d["colours"] else " in the party colours"
    desc = f"{s} party umbrellas, canopy tents and gazebos printed{colour_txt} with the {sym_short} symbol and candidate name. Bulk, GST invoice, delivery across India."
    if len(desc) > 155:
        desc = f"{s} party umbrellas and canopy tents printed{colour_txt} with symbol and candidate name. Bulk orders, GST invoice, delivery across India."
    if len(desc) > 155:
        desc = f"{s} party umbrellas and canopy tents printed with symbol and candidate name. Bulk orders, GST invoice, delivery across India."
    wa = f"Hi, I need printed umbrellas / canopies for a {s} campaign (town: __, quantity: __)."
    quote = f"{p}contact.html?topic=Bulk%20or%20B2B%20order&amp;product=" + e(f"{s} umbrellas / canopies").replace(" ", "%20").replace("&amp;", "%26")
    faqs = [
        (f"Can you print the {s} symbol and colours on umbrellas?",
         f"Yes. We print the {d['symbol']} symbol{(', ' + d['colours']) if d['colours'] else ' and party colours'}, the candidate's name and photo, or a slogan, and send a PDF mock-up for approval before printing. Screen printing suits up to 3 colours; digital printing handles photos and any number of colours."),
        ("Who can order party-printed umbrellas?",
         "Party units, candidates and their campaign agencies. Please send the artwork approved by your party office; we print it for you but don't supply party artwork or sell symbol-printed stock to the public."),
        ("What is the minimum order?", "Printed umbrellas: 300 pieces. Printed garden umbrellas: 12 pieces. Canopy tents and gazebos: from 1 piece."),
        ("Can the umbrellas be given out to voters?",
         "Gifts to voters are not allowed while the model code of conduct is in force. During an election, use them for party workers, booths and rallies. Outside election periods, party units often order umbrellas for monsoon drives and public events."),
        ("Do you give a GST invoice for the election expense account?",
         "Yes. Every order comes with a GST invoice (GSTIN 27AGCPJ9001C1ZX), which candidates can use for their election expenditure records."),
    ]
    if d["mh"]:
        faqs.insert(3, ("How fast can you deliver in Mumbai and Maharashtra?",
                        f'Within 2 days of mock-up approval for standard sizes in Mumbai, Thane, Navi Mumbai, Kalyan-Dombivli, Pune and Nashik, because we print in our own Bhiwandi factory. See <a href="{p}2-day-delivery.html">2-day printed delivery</a>.'))
    where = []
    for el in d["elections"]:
        n, w = ELECTIONS[el]
        where.append(f'<a class="card" href="{p}elections/{el}.html"><p class="label">{w}</p><h3>{n}</h3><p>{s} campaign umbrellas and canopies, delivered to small towns as well as cities.</p></a>')
    if d["mh"]:
        for slug, n in MUMBAI_HUBS[:3 if d["elections"] else 6]:
            where.append(f'<a class="card" href="{p}locations/{slug}.html"><p class="label">2-day printed delivery</p><h3>{n}</h3><p>Printed in our Bhiwandi factory, delivered within 2 days of mock-up approval.</p></a>')
    if d.get("kolkata"):
        where.append(f'<a class="card" href="{p}locations/kolkata.html"><p class="label">Kolkata municipal election, due by Dec 2026</p><h3>Kolkata</h3><p>Party umbrellas and canopy tents for Kolkata and West Bengal.</p></a>')
    others = "".join(f'<li><a href="{x["slug"]}.html">{x["short"]}</a></li>' for x in PARTIES if x is not d)
    lang, line = d["line"]
    colours_li = f"<li>Colours: {d['colours']}</li>" if d["colours"] else "<li>Colours: matched to the shades your party office gives us</li>"
    h, f = chrome(p)
    schemas = [
        crumbs_schema([("Home", SITE), ("Election campaigns", SITE + "industries/election-campaigns.html"),
                       ("Political party umbrellas", SITE + "political-party-umbrellas.html"), (f"{s} umbrellas", url)]),
        faq_schema(faqs),
        {"@context": "https://schema.org", "@type": "Service", "name": f"{s} party umbrellas and canopy tents",
         "serviceType": "Printed political campaign umbrellas and canopy tents",
         "provider": {"@type": "LocalBusiness", "name": "Mukund Enterprises", "url": SITE, "telephone": "+919137878456"},
         "areaServed": {"@type": "Country", "name": "India"}},
    ]
    return head(title, desc, url, p, schemas) + h + f"""

<section class="hero small lp-hero">
  <div class="wrap">
    <p class="crumbs"><a href="{p}index.html">Home</a> / <a href="{p}industries/election-campaigns.html">Election campaigns</a> / <a href="{p}political-party-umbrellas.html">Party umbrellas</a> / {e(s)}</p>
    <p class="eyebrow">For {e(d['full'])} units and candidates</p>
    <h1>{e(sp)} <em>Umbrellas</em> &amp; Canopy Tents</h1>
    <p class="lead">Umbrellas, canopy tents and gazebos printed{e(colour_txt)} with the {e(d['symbol'])} symbol and your candidate's name – made in bulk in our own factory and delivered to {e(d['active'])}.</p><p lang="{lang}" style="margin-top:12px">{line}</p>
    <div class="btns">
      <a class="btn" href="{quote}">Get a quote</a>
      <a class="btn ghost" data-wa="{e(wa)}">WhatsApp us</a>
    </div>
  </div>
</section>
<section>
  <div class="wrap two">
    <div><p class="eyebrow">How we print it</p><h2>{e(s)} <em>campaign</em> umbrellas</h2></div>
    <div><p>{d['para']}</p>
    <ul class="ticks" style="margin-top:18px"><li>Symbol: {e(d['symbol'])}</li>{colours_li}<li>Candidate name, photo, slogan or ward number on any panel</li><li>PDF mock-up before printing; screen or digital print</li></ul>
    <p style="margin-top:12px"><small>Also searched as: {e(d['local'])}, {e(s)} chhata, {e(s)} printed umbrella.</small></p></div>
  </div>
</section>
<section class="alt">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Where we deliver</p><h2>{e(s)} orders <em>we supply</em></h2><p>We dispatch from Bhiwandi by transport or courier to every state, including small district towns.</p></div>
    <div class="grid g3">{''.join(where) if where else ''}<a class="card" href="{p}areas-we-serve.html"><p class="label">All India</p><h3>Other states and towns</h3><p>Send the town name with your enquiry; delivery is charged by town and order size.</p></a></div>
  </div>
</section>
<section>
  <div class="wrap two">
    <div><p class="eyebrow">What to order</p><h2>Campaign <em>material</em></h2></div>
    <div>{products_table(p)}</div>
  </div>
</section>
<section class="alt">
  <div class="wrap two">
    <div><p class="eyebrow">FAQ</p><h2>Common <em>questions</em></h2><p class="lead">More answers on our <a href="{p}faq.html">FAQ page</a>.</p></div>
    <div class="faq">{faq_html(faqs)}</div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Other parties</p><h2>We print for <em>every party</em></h2></div>
    <ul class="related">{others}<li><a href="{p}political-party-umbrellas.html">All party umbrellas</a></li><li><a href="{p}industries/election-campaigns.html">All election material</a></li></ul>
    <p style="margin-top:18px"><small>{DISCLAIMER}</small></p>
  </div>
</section>
<section class="band dark">
  <div class="wrap">
    <p class="eyebrow">Bulk orders</p>
    <h2>Planning a {e(s)} campaign?</h2>
    <p class="lead">Send the product, quantity, town and your approved artwork. We usually reply on WhatsApp within 15 minutes.</p>
    <div class="btns"><a class="btn" href="{quote}">Send a requirement</a><a class="btn ghost" data-wa="{e(wa)}">WhatsApp us</a></div>
  </div>
</section>

""" + f + "\n"


def hub_page():
    p = ""
    url = SITE + "political-party-umbrellas.html"
    title = "Political Party Umbrellas, Printed with Symbol"
    desc = "Party umbrellas, canopy tents and gazebos printed with party colours, symbol and candidate name for BJP, Congress, AAP, SP, Shiv Sena, DMK and more."
    faqs = [
        ("Which parties do you print umbrellas for?", "Any registered party, independent candidates and their campaign agencies. Regular orders come from BJP, Congress, AAP, Samajwadi Party, BSP, Shiv Sena, NCP, MNS, TMC, DMK, AIADMK and Akali Dal units."),
        ("Who can order party-printed umbrellas?", "Party units, candidates and their campaign agencies. Please send the artwork approved by your party office; we print it for you but don't supply party artwork or sell symbol-printed stock to the public."),
        ("What is the minimum order?", "Printed umbrellas: 300 pieces. Printed garden umbrellas: 12 pieces. Canopy tents and gazebos: from 1 piece."),
        ("How long does printing take?", 'Within 2 days of mock-up approval for standard sizes in the Mumbai region (see <a href="2-day-delivery.html">2-day printed delivery</a>). For other states, add transport time; the date is confirmed in the quote. Book early before polling, when many candidates order in the same weeks.'),
        ("Can the umbrellas be given out to voters?", "Gifts to voters are not allowed while the model code of conduct is in force. During an election, use them for party workers, booths and rallies."),
        ("Do you give a GST invoice?", "Yes, with every order (GSTIN 27AGCPJ9001C1ZX), for the candidate's election expenditure records."),
    ]
    cards = "".join(f'<a class="card" href="parties/{d["slug"]}.html"><p class="label">{e(d["active"])}</p><h3>{e(d["short"])} umbrellas</h3><p>Symbol: {e(d["symbol"].split(" (")[0])}{(" · " + e(d["colours"])) if d["colours"] else ""}</p></a>' for d in PARTIES)
    els = "".join(f'<li><a href="elections/{k}.html">{v[0]}</a></li>' for k, v in ELECTIONS.items())
    h, f = chrome(p)
    schemas = [
        crumbs_schema([("Home", SITE), ("Election campaigns", SITE + "industries/election-campaigns.html"), ("Political party umbrellas", url)]),
        faq_schema(faqs),
        {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": f"{d['short']} umbrellas", "url": f"{SITE}parties/{d['slug']}.html"} for i, d in enumerate(PARTIES)]},
    ]
    return head(title, desc, url, p, schemas) + h + f"""

<section class="hero small lp-hero">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a> / <a href="industries/election-campaigns.html">Election campaigns</a> / Political party umbrellas</p>
    <p class="eyebrow">For party units, candidates and campaign agencies</p>
    <h1>Political Party <em>Umbrellas</em> &amp; Canopy Tents</h1>
    <p class="lead">Umbrellas, canopy tents and gazebos printed in your party's colours, with the election symbol, candidate name and photo – made in bulk in our own Bhiwandi factory and delivered to any town in India.</p><p lang="hi" style="margin-top:12px">{HI}</p>
    <div class="btns">
      <a class="btn" href="contact.html?topic=Bulk%20or%20B2B%20order&amp;product=Political%20party%20umbrellas">Get a quote</a>
      <a class="btn ghost" data-wa="Hi, I need party-printed umbrellas / canopies (party: __, town: __, quantity: __).">WhatsApp us</a>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Choose your party</p><h2>Party umbrellas <em>we print</em></h2><p>Each page covers that party's colours and symbol, the elections coming up where it is active, and delivery.</p></div>
    <div class="grid g3">{cards}</div>
    <p style="margin-top:18px">Independent candidate or a party not listed? We print for any party – send your artwork with the enquiry.</p>
  </div>
</section>
<section class="alt">
  <div class="wrap two">
    <div><p class="eyebrow">How it works</p><h2>From artwork to <em>delivery</em></h2></div>
    <div><ul class="ticks"><li>Send the product, quantity, town and the artwork approved by your party office</li><li>Get a quote and a PDF mock-up showing the colours on each panel</li><li>Approve with a 50% advance; we print in our own factory</li><li>Dispatch by transport or courier, with a GST invoice for the expense account</li></ul>
    <p style="margin-top:12px">Screen printing is cheapest for 1 to 3 colours (party colour plus symbol). Digital printing suits the candidate's photo or many colours. Try the <a href="logo-preview.html">logo preview tool</a> to see a design on an umbrella.</p></div>
  </div>
</section>
<section>
  <div class="wrap two">
    <div><p class="eyebrow">What to order</p><h2>Campaign <em>material</em></h2></div>
    <div>{products_table(p)}</div>
  </div>
</section>
<section class="alt">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Upcoming elections</p><h2>States voting <em>next</em></h2><p>Town lists and timings for each state.</p></div>
    <ul class="related">{els}<li><a href="locations/kolkata.html">Kolkata</a></li><li><a href="2-day-delivery.html">Mumbai region (2-day delivery)</a></li></ul>
  </div>
</section>
<section>
  <div class="wrap two">
    <div><p class="eyebrow">FAQ</p><h2>Common <em>questions</em></h2><p class="lead">More answers on our <a href="faq.html">FAQ page</a>.</p></div>
    <div class="faq">{faq_html(faqs)}</div>
  </div>
</section>
<section class="band dark">
  <div class="wrap">
    <p class="eyebrow">Bulk orders</p>
    <h2>Planning your campaign?</h2>
    <p class="lead">Send the party, product, quantity and town. We usually reply on WhatsApp within 15 minutes.</p>
    <div class="btns"><a class="btn" href="contact.html?topic=Bulk%20or%20B2B%20order&amp;product=Political%20party%20umbrellas">Send a requirement</a><a class="btn ghost" data-wa="Hi, I need party-printed umbrellas / canopies (party: __, town: __, quantity: __).">WhatsApp us</a></div>
    <p style="margin-top:18px"><small>{DISCLAIMER}</small></p>
  </div>
</section>

""" + f + "\n"


if __name__ == "__main__":
    (ROOT / "parties").mkdir(exist_ok=True)
    for d in PARTIES:
        (ROOT / "parties" / f"{d['slug']}.html").write_text(party_page(d), encoding="utf-8")
    (ROOT / "political-party-umbrellas.html").write_text(hub_page(), encoding="utf-8")
    print(f"wrote {len(PARTIES)} party pages + hub")
