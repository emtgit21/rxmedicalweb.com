#!/usr/bin/env python3
"""Static site generator for rxmedicalweb.com.

    python3 src/build.py

Reads the content in src/pages.py and writes every page as <path>/index.html at the
repo root, plus sitemap.xml. No dependencies beyond the standard library.
"""
import datetime
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages import *  # noqa: E402,F401,F403

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://rxmedicalweb.com"
YEAR = datetime.date.today().year
UP = "/wp-content/uploads/"
BUILT = []
UNLISTED = {"/book-a-call/"}   # live but not linked or in the sitemap until booking notices are set up
PAGE_CSS = []          # stylesheets for the custom animated graphics used on the page being built
ANIM_DIR = os.path.join(ROOT, "src", "anims")
# custom animated graphic for each service (falls back to the generic one in pages.py if the file is missing)
CUSTOM_ANIM = {
    "local-seo": "map", "online-booking": "booking", "e-mail-marketing": "inbox", "ai-chat-messaging": "agents",
    "ai-search-optimization": "answer", "pay-per-click": "adslot", "search-engine-marketing": "socialads",
    "social-media": "calendar", "short-form-video": "reel", "physician-content-marketing": "doc",
    "video-testimonials": "camera", "patient-crm-automation": "pipeline", "new-service-launch": "launch",
    "marketing-strategy": "roadmap", "medical-graphic-design": "brand", "printing": "press",
    "medical-practice-kit": "kit", "analytics-call-tracking": "dashboard", "medical-e-commerce": "cart",
    "emr-patient-portals": "portal", "website-accessibility-compliance": "a11y", "website-maintenance": "uptime",
    "landing-pages-funnels": "abtest", "integrations": "hub", "mobile-apps": "apps", "medical-spa-website-design": "devices",
}
try:
    import json
    FAQS = json.load(open(os.path.join(ROOT, "src", "faqs.json"), encoding="utf-8"))
except FileNotFoundError:
    FAQS = {}
try:
    EXPLAIN = json.load(open(os.path.join(ROOT, "src", "explain.json"), encoding="utf-8"))
except FileNotFoundError:
    EXPLAIN = {}


import hashlib
import re as _re


def ver(rel):
    """Short content hash, so browsers can cache assets for a long time."""
    return hashlib.md5(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()[:8]


def _minify(css):
    css = _re.sub(r"/\*.*?\*/", "", css, flags=_re.S)
    return _re.sub(r"\s+", " ", css).strip()


FONT_CSS = _minify(open(os.path.join(ROOT, "assets", "fonts", "fonts.css"), encoding="utf-8").read())


def anim_css():
    """Inline the CSS of the custom graphics used on this page: one request less per graphic."""
    keys = list(dict.fromkeys(PAGE_CSS))
    if not keys:
        return ""
    return "<style>" + " ".join(_minify(open(os.path.join(ROOT, "assets", "anim", k + ".css"), encoding="utf-8").read()) for k in keys) + "</style>\n"


def has_anim(key):
    return bool(key) and os.path.exists(os.path.join(ANIM_DIR, key + ".html"))


def has_video(name):
    return os.path.exists(os.path.join(ROOT, "assets", "video", name + ".mp4"))


def words(text):
    """Wrap each word so the hero headline can rise in word by word."""
    return " ".join(f'<span class="w"><span style="--i:{i}">{e(w)}</span></span>' for i, w in enumerate(text.split()))


def media(name, alt, cls, w=1248, h=832, lazy=True):
    """A living-photo clip when one exists, otherwise the still."""
    if has_video(name):
        return (f'<video class="{cls}" muted loop playsinline preload="none" poster="/assets/img/{name}.webp" '
                f'width="{w}" height="{h}" aria-label="{e(alt)}"><source src="/assets/video/{name}.mp4?v={ver("assets/video/" + name + ".mp4")}" type="video/mp4"></video>')
    return f'<img class="{cls}" src="/assets/img/{name}.webp" width="{w}" height="{h}" alt="{e(alt)}"{" loading=lazy" if lazy else ""}>'


def e(s):
    return html.escape(s, quote=True)


SPECS = json.load(open(os.path.join(ROOT, "src", "specialties.json"), encoding="utf-8"))
RESOURCES = json.load(open(os.path.join(ROOT, "src", "resources.json"), encoding="utf-8"))
GUIDE = "/assets/guides/medical-marketing-checklist-2026.pdf"
RES_DATE = "November 13, 2026"
RES_ISO = "2026-11-13"


def svc_url(s):
    return f"/service/{s['slug']}/"


# ---------------------------------------------------------------- shared chrome
def menu():
    cols = []
    for gi, (gname, _) in enumerate(GROUPS):
        links = "".join(f'<a href="{svc_url(s)}" data-img="{s["img"]}" data-blurb="{e(s["blurb"])}">{e(s["name"])}</a>'
                        for s in SERVICES if s["group"] == gi)
        cols.append(f'<div><p class="mh"><button type="button" aria-expanded="false">{e(gname)}</button></p>{links}</div>')
    first = SERVICES[0]
    return f"""<div class="menu-cols">{"".join(cols)}</div>
<aside class="menu-preview" aria-hidden="true">
  <div class="menu-preview-img"><img src="/assets/img/{first["img"]}.webp" alt="{e(first["alt"])}" loading="lazy"></div>
  <b>{e(first["name"])}</b><p>{e(first["blurb"])}</p>
</aside>
<div class="menu-foot"><span>Not sure where to start? We will look at your website and tell you.</span><a class="btn btn-ink" href="/contact-us/#analysis">Request a free analysis</a></div>"""


def header(path):
    def cur(p):
        return ' aria-current="page"' if path == p else ""
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Rx Medical Web, home"><img src="{UP}mainlogo.png" width="400" height="83" alt="Rx Medical Web. Physicians Rx for Success"></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main">
      <span class="nav-hl" aria-hidden="true"></span>
      <div class="nav-services">
        <button aria-expanded="false" aria-controls="services-menu">Services</button>
        <div class="menu" id="services-menu">{menu()}</div>
      </div>
      <a href="/specialties/"{cur('/specialties/')}>Specialties</a>
      <a href="/portfolio/"{cur('/portfolio/')}>Our work</a>
      <a href="/resources/"{cur('/resources/')}>Resources</a>
      <a href="/about/"{cur('/about/')}>About</a>
      <a href="/contact-us/"{cur('/contact-us/')}>Contact</a>
    </nav>
    <div class="header-cta">
      <a class="header-phone" href="{PHONE_HREF}">{PHONE}</a>
      <a class="btn btn-primary" href="/contact-us/#analysis">Free website analysis</a>
    </div>
  </div>
</header>"""


def closing(title="Ready to get started?", text="Tell us about your practice. We reply within 24 business hours with packages and pricing."):
    return f"""<section class="closing">
  <div class="wrap">
    <div>
      <h2>{title}</h2>
      <p>{text}</p>
    </div>
    <div class="closing-contact">
      <a class="big" href="{PHONE_HREF}">{PHONE}</a>
      <a class="big" href="mailto:{EMAIL}">{EMAIL}</a>
      <a class="btn btn-primary" href="/contact-us/#analysis">Request a free website analysis</a>
    </div>
  </div>
</section>"""


def footer():
    cols = []
    for gi, (gname, _) in enumerate(GROUPS):
        links = "".join(f'<li><a href="{svc_url(s)}">{e(s["name"])}</a></li>' for s in SERVICES if s["group"] == gi)
        cols.append(f'<div><p class="fh">{e(gname)}</p><ul>{links}</ul></div>')
    sp = "".join(f'<li><a href="/specialties/{k}/">{e(v["name"])}</a></li>' for k, v in SPECS.items())
    cols.append(f'<div><p class="fh">Specialties</p><ul>{sp}</ul></div>')
    rs = "".join(f'<li><a href="/resources/{a["slug"]}/">{e(a["title"])}</a></li>' for a in RESOURCES[:6])
    cols.append(f'<div class="wide"><p class="fh">Resources</p><ul>{rs}<li><a href="/resources/">All resources</a></li></ul></div>')
    return f"""<footer class="site-footer">
  <div class="wrap">
    <p class="footer-sign" aria-hidden="true">Physicians Rx for Success</p>
    <div class="footer-top">
      <div class="footer-brand">
        <img src="{UP}mainlogo.png" width="400" height="83" alt="Rx Medical Web" loading="lazy">
        <address>2720 E. Oakland Park Blvd, Suite 103<br>Fort Lauderdale, FL 33306<br>Monday to Friday, 9 am to 6 pm</address>
      </div>
      <div><p class="fh">Contact</p><ul>
        <li><a href="{PHONE_HREF}">{PHONE}</a></li>
        <li><a href="{LOCAL_PHONE_HREF}">{LOCAL_PHONE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="/contact-us/">Contact us</a></li>
      </ul></div>
      <div><p class="fh">Company</p><ul>
        <li><a href="/about/">About us</a></li>
        <li><a href="/about/why-choose-us/">Why choose us</a></li>
        <li><a href="/about/testimonials/">Testimonials</a></li>
        <li><a href="/portfolio/">Our work</a></li>
        <li><a href="/specialties/">Specialties</a></li>
        <li><a href="/resources/">Resources</a></li>
      </ul></div>
      <div><p class="fh">Strategic partner</p><ul>
        <li><a href="https://www.empiremedicaltraining.com/" rel="noopener">Empire Medical Training</a></li>
      </ul><p class="fh gap">Follow us</p><ul>
        <li><a href="https://www.linkedin.com/company/rx-medical-web" rel="noopener">LinkedIn</a></li>
        <li><a href="https://www.facebook.com/rxmedicalweb/" rel="noopener">Facebook</a></li>
      </ul></div>
    </div>
    <div class="footer-grid">{''.join(cols)}</div>
    <div class="footer-legal"><span>© {YEAR} Rx Medical Web. All rights reserved. <a href="/privacy-policy/">Privacy policy</a></span><span>Medical presence and marketing, Fort Lauderdale, Florida</span></div>
  </div>
</footer>"""


SEO = json.load(open(os.path.join(ROOT, "src", "seo.json"), encoding="utf-8"))
ORG_ID, WEB_ID = SITE + "/#organization", SITE + "/#website"
CRUMB_PARENTS = {"about": ("About us", "/about/"), "resources": ("Resources", "/resources/"), "specialties": ("Specialties", "/specialties/")}
PAGE_TYPES = {"/about/": "AboutPage", "/contact-us/": "ContactPage", "/resources/": "CollectionPage", "/specialties/": "CollectionPage", "/portfolio/": "CollectionPage"}
LASTMOD = {}


def fit_title(t):
    """Search results cut titles at about 60 characters: drop the brand suffix before a title gets cut."""
    suffix = " | Rx Medical Web"
    return t[:-len(suffix)] if len(t) > 60 and t.endswith(suffix) else t


def fit_desc(d):
    """Keep whole sentences up to 160 characters."""
    d = " ".join(d.split())
    if len(d) <= 160:
        return d
    out = ""
    for sent in _re.split(r"(?<=[.!?])\s+", d):
        if len(out) + len(sent) + 1 > 160:
            break
        out = (out + " " + sent).strip()
    return out if len(out) >= 90 else d[:157].rsplit(" ", 1)[0] + "…"


def page(path, title, desc, body, extra_head="", og_img="/assets/img/hero-clinic.jpg", og_type="website"):
    """path like '/' or '/about/'."""
    name = title.split(" | ")[0]
    o = SEO.get(path, {})
    title, desc = o.get("title") or fit_title(title), o.get("desc") or fit_desc(desc)
    noindex = "noindex" in extra_head or path in UNLISTED
    if path in UNLISTED and "noindex" not in extra_head:
        extra_head += '<meta name="robots" content="noindex">\n'
    if not noindex:
        extra_head = '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">\n' + extra_head
        if path != "/" and '"BreadcrumbList"' not in extra_head:
            seg = path.strip("/").split("/")
            trail = [("Home", "/")] + ([CRUMB_PARENTS[seg[0]]] if len(seg) > 1 and seg[0] in CRUMB_PARENTS else []) + [(name, path)]
            extra_head += ld({"@context": "https://schema.org", "@graph": [
                {"@type": PAGE_TYPES.get(path, "WebPage"), "@id": SITE + path + "#webpage", "url": SITE + path, "name": name, "description": desc,
                 "inLanguage": "en-US", "isPartOf": {"@id": WEB_ID}, "about": {"@id": ORG_ID}},
                {"@type": "BreadcrumbList", "itemListElement": [
                    {"@type": "ListItem", "position": n + 1, "name": t, "item": SITE + u} for n, (t, u) in enumerate(trail)]}]})
        LASTMOD[path] = hashlib.sha1((title + desc + body).encode("utf-8")).hexdigest()[:16]
    canonical = "" if path == "/404/" else f'<link rel="canonical" href="{SITE}{path}">\n'
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{canonical}<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="Rx Medical Web">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}{og_img}">
<meta name="theme-color" content="#0b2f38">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}{og_img}">
<link rel="preload" href="/assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>{FONT_CSS}</style>
<link rel="stylesheet" href="/assets/site.css?v={ver("assets/site.css")}">
{anim_css()}<script>document.documentElement.className='js'</script>
<!-- Google tag (Analytics property "Rx Medical Web") -->
<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-TP682R68"></script>
<script>window.dataLayer = window.dataLayer || [];function gtag(){{dataLayer.push(arguments);}}gtag('js', new Date());</script>
{extra_head}</head>
<body>
{header(path)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/site.js?v={ver("assets/site.js")}" defer></script>
<script src="/assets/chat.js?v={ver("assets/chat.js")}" defer></script>
</body>
</html>
"""
    out = os.path.join(ROOT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    PAGE_CSS.clear()
    if not path.startswith("/dev/") and path not in UNLISTED:
        BUILT.append(path)


# ---------------------------------------------------------------- animated graphics
def anim(spec, caption=""):
    kind = spec[0]
    if kind == "x":
        key = spec[1]
        inner = open(os.path.join(ANIM_DIR, key + ".html"), encoding="utf-8").read()
        label = open(os.path.join(ANIM_DIR, key + ".txt"), encoding="utf-8").read().strip()
        PAGE_CSS.append(key)
        cap = f"<figcaption>{caption}</figcaption>" if caption else ""
        return f'<figure class="anim anim-x anim-{key}" role="img" aria-label="{e(label)}">{inner}{cap}</figure>'
    if kind == "flow":
        steps = spec[1]
        items = "".join(f'<li style="--i:{i}"><span>{e(t)}</span></li>' for i, t in enumerate(steps))
        inner = f'<ol class="flow" style="--n:{len(steps)}">{items}</ol>'
        label = "Diagram of the steps: " + ", then ".join(steps)
    elif kind == "serp":
        inner = """<div class="serp" aria-hidden="true">
  <div class="serp-bar"><i></i><span>botox near me</span></div>
  <div class="serp-rows">
    <div class="serp-row r1"><b></b><u></u></div>
    <div class="serp-row r2"><b></b><u></u></div>
    <div class="serp-row r3"><b></b><u></u></div>
    <div class="serp-row you"><b>Your practice</b><u></u><em>★★★★★</em></div>
  </div>
</div>"""
        label = "Animation: your practice climbs from fourth place to first in a list of search results."
    elif kind == "chat":
        bubbles = "".join(f'<p class="{who_}" style="--i:{i}">{e(t)}</p>' for i, (who_, t) in enumerate(spec[1]))
        inner = f'<div class="chat" style="--n:{len(spec[1])}" aria-hidden="true">{bubbles}</div>'
        label = "Example conversation: " + " / ".join(t for _, t in spec[1])
    elif kind == "chart":
        bars = "".join(f'<i style="--h:{h}%;--i:{i}"></i>' for i, h in enumerate([22, 30, 27, 41, 52, 60, 74, 88]))
        inner = f"""<div class="chart" aria-hidden="true">
  <div class="chart-legend"><span class="k1">Calls and bookings</span><span class="k2">Cost per inquiry</span></div>
  <div class="chart-plot"><div class="chart-bars">{bars}</div>
  <svg viewBox="0 0 400 160" preserveAspectRatio="none"><path d="M5,30 C60,36 90,58 140,66 S230,92 280,112 S360,134 395,140" pathLength="1"/></svg></div>
</div>"""
        label = "Illustration, not client data: calls and bookings rise month over month while cost per inquiry falls."
    elif kind == "stars":
        stars = "".join(f'<i style="--i:{i}">★</i>' for i in range(5))
        inner = f"""<div class="stars" aria-hidden="true">
  <div class="stars-row">{stars}</div>
  <div class="stars-cards">
    <div style="--i:0"><b>★★★★★</b><u></u><u class="s"></u></div>
    <div style="--i:1"><b>★★★★★</b><u></u><u class="s"></u></div>
    <div style="--i:2"><b>★★★★★</b><u></u><u class="s"></u></div>
  </div>
</div>"""
        label = "Animation: new five star reviews arriving one after another."
    else:  # build
        inner = """<div class="build" aria-hidden="true">
  <div class="build-top"><i></i><i></i><i></i></div>
  <div class="build-page">
    <div class="b b-nav" style="--i:0"></div>
    <div class="b b-hero" style="--i:1"><span></span><span class="s"></span><em>Book now</em></div>
    <div class="b b-img" style="--i:2"></div>
    <div class="b b-card" style="--i:3"></div><div class="b b-card" style="--i:4"></div><div class="b b-card" style="--i:5"></div>
  </div>
</div>"""
        label = "Animation: a web page assembling block by block, ending with a Book now button."
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure class="anim anim-{kind}" role="img" aria-label="{e(label)}">{inner}{cap}</figure>'


# ---------------------------------------------------------------- pieces
def who(t):
    return (f'<div class="who"><img src="/assets/img/t-{t["img"].rsplit(".", 1)[0].lower()}.webp" width="76" height="76" alt="{e(t["name"])}" loading="lazy">'
            f'<div><b>{e(t["name"])}</b><span>{e(t["role"])}</span></div></div>')


def testimonials_block(full=False):
    lead = TESTIMONIALS[0]
    rest = "".join(f'<figure><blockquote>“{e(t["quote"])}”</blockquote><figcaption>{who(t)}</figcaption></figure>'
                   for t in TESTIMONIALS[1:])
    more = "" if full else '<a class="btn btn-line" href="/about/testimonials/">Read all testimonials</a>'
    return f"""<div class="quote-lead">
  <figure><blockquote>“{e(lead["quote"])}”</blockquote><figcaption>{who(lead)}</figcaption></figure>
  <div class="quote-aside">
    <h2 class="quote-h">Good words from good people</h2>
    <p>Many of our clients first met us through Empire Medical Training, then asked us to build the website and marketing for the services they had just learned.</p>
    {more}
  </div>
</div>
<div class="quotes">{rest}</div>"""


def work_cards(tag="h3", only=None):
    return "".join(
        f'<a href="{w["url"]}" rel="noopener"><div class="shot"><img src="/assets/img/{w["shot"]}.webp" width="1400" height="801" alt="Screenshot of the {e(w["name"])} website" loading="lazy"></div>'
        f'<{tag}>{e(w["name"])}</{tag}><p>{e(w["note"])}</p></a>' for w in WORK if not only or w["shot"] in only)


def page_head(crumbs, h1, lead, img=None, alt=""):
    trail = '<a href="/">Home</a>' + "".join(
        f'<span>/</span><a href="{u}">{e(t)}</a>' if u else f'<span>/</span>{e(t)}' for t, u in crumbs)
    pic = media(img, alt, "page-head-img", lazy=False) if img else ""
    cls = "page-head has-img" if img else "page-head"
    return f"""<section class="{cls}">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb">{trail}</nav>
    <div class="page-head-grid">
      <div><h1>{h1}</h1><p class="lead">{lead}</p></div>
      {pic}
    </div>
  </div>
</section>"""


def slip(title, text, related=None, related_title="Related services"):
    more = ""
    if related:
        links = "".join(f'<li><a href="{u}">{e(t)}</a></li>' for t, u in related)
        more = f'<div class="slip-more"><h3>{related_title}</h3><ul>{links}</ul></div>'
    return f"""<aside class="slip">
  <div class="slip-card">
    <h2>{title}</h2>
    <p>{text}</p>
    <a class="big" href="{PHONE_HREF}">{PHONE}</a>
    <a class="big" href="mailto:{EMAIL}">{EMAIL}</a>
    <a class="btn btn-ink" href="/contact-us/#analysis">Request a free analysis</a>
  </div>
  {more}
</aside>"""


# ---------------------------------------------------------------- home pieces
SPECIALTIES = ["Aesthetics", "Dermatology", "Plastic surgery", "Med spas", "Dentistry", "Cosmetic dentistry", "Gynecology",
               "Pain management", "Cardiology", "Chiropractic", "Family practice", "Weight loss", "Anti-aging medicine"]


def marquee():
    run = "".join(f"<span>{e(x)}</span>" for x in SPECIALTIES)
    return (f'<div class="marquee"><p class="vh">We work with practices in: {e(", ".join(SPECIALTIES))}.</p>'
            f'<div class="marquee-track" aria-hidden="true">{run}{run}</div></div>')


def pick(custom, fallback):
    return ("x", custom) if has_anim(custom) else fallback


def story():
    def links(*slugs):
        by = {s["slug"]: s for s in SERVICES}
        return '<div class="story-links">' + "".join(f'<a href="{svc_url(by[x])}">{e(by[x]["name"])}</a>' for x in slugs) + "</div>"
    steps = [
        ("They search, or ask an AI.", "Most patients start on Google, on a map or with an AI assistant. We work on all three, so your practice is the one they find.",
         pick("answer", ("serp",)), links("search-engine-optimization", "local-seo", "ai-search-optimization", "pay-per-click")),
        ("They land on a site built for them.", "A custom website and a landing page for each treatment answer the question that brought them, and make the next step obvious.",
         pick("devices", ("build",)), links("medical-website-design", "landing-pages-funnels", "medical-spa-website-design")),
        ("Someone answers right away.", "AI agents reply by chat, text and phone at any hour, and every lead is logged and followed until it books.",
         pick("agents", ("chat", AGENT_CHAT)), links("ai-chat-messaging", "patient-crm-automation")),
        ("They book from their phone.", "Online booking, intake forms and reminders by text. No phone tag, and fewer empty slots.",
         pick("booking", ("flow", ["Picks a time", "Fills in intake", "Gets a reminder"])), links("online-booking", "sms-marketing")),
        ("They tell other people.", "A review request after every visit and content worth sharing build the reputation new patients look for.",
         ("stars",), links("reputation-management", "social-media", "short-form-video")),
        ("They come back.", "Newsletters, reminders and reactivation campaigns bring patients back for the next treatment, and you see exactly what it produced.",
         pick("inbox", ("chart",)), links("e-mail-marketing", "analytics-call-tracking")),
    ]
    items = "".join(f'<li class="story-step"><h3>{e(t)}</h3><p>{e(d)}</p>{l}{anim(a)}</li>' for t, d, a, l in steps)
    return f"""<section class="section story">
  <div class="wrap">
    <div class="section-head reveal">
      <h2>How a patient reaches you, and how we help at every step.</h2>
      <p>Every service we offer supports one step of this path. We measure the whole thing by the calls and bookings at the end.</p>
    </div>
    <div class="story-grid">
      <div class="story-stage" aria-hidden="true"></div>
      <ol class="story-steps">{items}</ol>
    </div>
  </div>
</section>"""


def partner():
    return """<section class="section partner">
  <div class="wrap">
    <div class="partner-mark reveal"><div><b>Rx Medical Web</b><i>strategic partner of</i><b>Empire Medical Training</b></div></div>
    <div>
      <h2>Trained at Empire? We already know your next service.</h2>
      <p class="lead">We have marketed Empire Medical Training's courses for more than fifteen years. When you bring a new procedure back to your practice, we know the questions patients ask about it and what it takes to fill your first month.</p>
      <div class="actions">
        <a class="btn btn-ink" href="/service/new-service-launch/">Launch a new service</a>
        <a class="btn btn-line" href="/about/">About the partnership</a>
      </div>
    </div>
  </div>
</section>"""


def faq_block(slug):
    qs = FAQS.get(slug) or []
    if not qs:
        return "", ""
    items = "".join(f'<details><summary>{e(q["q"])}</summary><p>{e(q["a"])}</p></details>' for q in qs)
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in qs]}
    return (f'<div class="faq"><h2>Questions we hear</h2>{items}</div>',
            '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>\n")


# ---------------------------------------------------------------- home
def build_home():
    groups = []
    for gi, (gname, gdesc) in enumerate(GROUPS):
        rows = "".join(
            f'<li><a href="{svc_url(s)}"><b>{e(s["name"])}</b><span>{e(s["blurb"])}</span></a></li>'
            for s in SERVICES if s["group"] == gi)
        groups.append(f'<div class="formulary-group"><h3>{e(gname)}<small>{e(gdesc)}</small></h3><ul class="formulary-list">{rows}</ul></div>')

    body = f"""<section class="hero hero-video">
  <video class="hero-bg" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1">
    <source src="/assets/video/hero.mp4?v={ver("assets/video/hero.mp4")}" type="video/mp4">
  </video>
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <h1 aria-label="The marketing prescription for your medical practice.">{words("The marketing prescription for your medical practice.")}</h1>
        <p class="lead">Rx Medical Web is the agency dedicated to medical presence and marketing. Websites, mobile apps, SEO, advertising, social media and AI agents, built by an in-house team with the latest AI technology and reviewed by physicians.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="/contact-us/#analysis">Request a free website analysis</a>
          <a class="btn btn-ghost" href="{PHONE_HREF}">Call {PHONE}</a>
        </div>
      </div>
      <div class="pad-wrap"><div class="pad" role="img" aria-label="A prescription from Rx Medical Web for your practice: a custom website; SEO, ads and AI search; AI agents around the clock; social, email and SMS. Refills monthly.">
        <div class="pad-sheet" aria-hidden="true">
          <div class="pad-head">
            <div><strong>Rx Medical Web</strong><span>Physicians Rx for Success</span></div>
            <div class="pad-tel"><span>Fort Lauderdale, FL</span><br><span>{PHONE}</span></div>
          </div>
          <div class="pad-fields">
            <div class="pad-field">For <span class="hand write">Your practice</span></div>
            <div class="pad-field">Refills <span class="hand write">monthly</span></div>
          </div>
          <div class="pad-body">
            <div class="pad-rx">℞</div>
            <ul class="pad-lines">
              <li class="write">A custom website<small>built from scratch, no templates</small></li>
              <li class="write">SEO, ads + AI search<small>so patients find you first</small></li>
              <li class="write">AI agents, 24/7<small>chat, text and phone answered</small></li>
              <li class="write">Social, email + SMS<small>content reviewed by physicians</small></li>
            </ul>
          </div>
          <div class="pad-foot">
            <div>Take with a free website analysis</div>
            <div class="pad-sign"><span class="hand write">Rx Medical Web</span>Your marketing team</div>
          </div>
        </div>
      </div></div>
    </div>
    <dl class="facts">
      <div class="fact"><dt>Established</dt><dd>2008</dd></div>
      <div class="fact"><dt>Practices served</dt><dd>400+ physicians and dentists</dd></div>
      <div class="fact"><dt>Team</dt><dd>In house, Fort Lauderdale</dd></div>
      <div class="fact"><dt>Strategic partner</dt><dd>Empire Medical Training</dd></div>
    </dl>
  </div>
</section>

{marquee()}
{spec_tiles_section()}

<section class="section" id="services">
  <div class="wrap">
    <div class="section-head reveal">
      <h2>Everything your practice needs to be found, chosen and booked.</h2>
      <p>One team for the whole job, from your first website to advanced campaigns. Pick a single service or let us run all of it.</p>
    </div>
    <div class="formulary">{''.join(groups)}</div>
  </div>
</section>

<section class="section ai-band">
  <div class="wrap">
    <div class="section-head reveal">
      <h2>The latest AI, working for your practice around the clock.</h2>
      <p>Patients search differently in 2026, and they expect an answer right away. We put current AI to work on both, with physicians checking the medicine.</p>
    </div>
    <div class="ai-grid">
      <a class="ai-card" href="/service/search-engine-optimization/">
        {anim(("serp",))}
        <h3>Found first</h3>
        <p>SEO, local search and AI search optimization, so your practice shows up on Google, on the map and in AI answers.</p>
      </a>
      <a class="ai-card" href="/service/ai-chat-messaging/">
        {anim(pick("agents", ("chat", AGENT_CHAT)))}
        <h3>Answered right away</h3>
        <p>AI agents reply by chat, text and phone at any hour, take the booking request and hand off to your staff.</p>
      </a>
      <a class="ai-card" href="/service/reputation-management/">
        {anim(("stars",))}
        <h3>Chosen with confidence</h3>
        <p>Review requests after every visit and thoughtful replies build the reputation new patients look for.</p>
      </a>
    </div>
  </div>
</section>

{story()}

<section class="section">
  <div class="wrap split">
    {media("hero-team", "A marketing team and a physician advisor reviewing website designs", "split-img reveal-mask", 1280, 720)}
    <div>
      <h2>Experts in medical marketing.</h2>
      <p class="lead">We are a physician owned, family owned agency. Designers, programmers, marketers, MBAs and a physician advisory board work together in Fort Lauderdale. We do not outsource.</p>
      <div class="cols-2 split-cols">
        <div><h3>Strategic partner of Empire Medical Training</h3><p>We have marketed Empire's courses for more than fifteen years. When you add a procedure you learned there, we already know how to launch it.</p></div>
        <div><h3>Results you can count</h3><p>Our results and phone tracking system shows the calls and bookings your marketing produces, not just clicks.</p></div>
      </div>
      <p class="split-cta"><a class="btn btn-line" href="/about/why-choose-us/">Why practices choose us</a></p>
    </div>
  </div>
</section>

{partner()}
{res_teaser()}

<section class="section on-dark integrate">
  <div class="wrap xp-two even">
    <div>
      <h2>Keep the tools you already use.</h2>
      <p class="lead">You do not have to replace your EMR, your scheduler or your CRM to work with us. Our websites, apps, AI agents and campaigns connect to your current systems whenever they offer an API or webhooks.</p>
      <ul class="chips"><li>EMR</li><li>Scheduling</li><li>CRM</li><li>Phones</li><li>Text and e-mail</li><li>Payments</li><li>Reviews</li></ul>
      <p class="split-cta"><a class="btn btn-primary" href="/service/integrations/">How integrations work</a></p>
    </div>
    {anim(pick("hub", ("flow", ["Your current tools", "API or webhook", "Our systems", "One view of every patient"])))}
  </div>
</section>

<section class="copy-sheet">
  <div class="wrap">
    <div>
      <h2>Free website analysis</h2>
      <p>We check your website for on-page and off-page SEO, domain authority, social engagement, speed and how AI assistants describe your practice. We also analyze your competition, then walk you through what we found.</p>
    </div>
    <div class="actions">
      <a class="btn btn-ink" href="/contact-us/#analysis">Request your analysis</a>
      <a class="btn btn-line" href="/portfolio/">See our work</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <h2>Recent work</h2>
      <p>Some of our most recent website launches.</p>
    </div>
    <div class="work-3">{work_cards(only=("work-emt", "work-app", "work-eod"))}</div>
    <p class="more-work"><a class="btn btn-line" href="/portfolio/">See all our work</a></p>
  </div>
</section>

<section class="section section-mint">
  <div class="wrap">{testimonials_block()}</div>
</section>

{closing()}"""
    ld_home = ld({"@context": "https://schema.org", "@graph": [
        {"@type": "ProfessionalService", "@id": ORG_ID, "name": "Rx Medical Web", "url": "https://rxmedicalweb.com/", "logo": {"@type": "ImageObject", "url": "https://rxmedicalweb.com/wp-content/uploads/mainlogo.png", "width": 400, "height": 83}, "image": "https://rxmedicalweb.com/assets/img/hero-clinic.jpg", "description": "Marketing agency dedicated to medical presence and marketing: websites, SEO, advertising, social media and AI agents for medical practices.", "telephone": "+1-888-599-4548", "email": "support@rxmedicalweb.com", "foundingDate": "2008", "address": {"@type": "PostalAddress", "streetAddress": "2720 E. Oakland Park Blvd, Suite 103", "addressLocality": "Fort Lauderdale", "addressRegion": "FL", "postalCode": "33306", "addressCountry": "US"}, "openingHours": "Mo-Fr 09:00-18:00", "sameAs": ["https://www.linkedin.com/company/rx-medical-web", "https://www.facebook.com/rxmedicalweb/"], "areaServed": {"@type": "Country", "name": "United States"}, "knowsAbout": ["Medical website design", "Search engine optimization for medical practices", "Local SEO", "Pay-per-click advertising", "Social media marketing", "AI agents for medical practices", "Reputation management"]},
        {"@type": "WebSite", "@id": WEB_ID, "url": SITE + "/", "name": "Rx Medical Web", "inLanguage": "en-US", "publisher": {"@id": ORG_ID}}]})
    page("/", "Rx Medical Web | Medical website design and marketing agency",
         "The marketing agency for medical practices: websites, SEO, ads, social media and AI agents. Strategic partner of Empire Medical Training.",
         body, extra_head=ld_home + '<link rel="preload" as="image" href="/assets/img/hero-clinic.webp" fetchpriority="high" media="(min-width: 701px)"><link rel="preload" as="image" href="/assets/img/hero-clinic-m.webp" fetchpriority="high" media="(max-width: 700px)">\n')


# ---------------------------------------------------------------- services
def crumbs_html(crumbs):
    return '<a href="/">Home</a>' + "".join(
        f'<span>/</span><a href="{u}">{e(t)}</a>' if u else f'<span>/</span>{e(t)}' for t, u in crumbs)


def sec_title(h2, p=""):
    return f'<div class="sec-title reveal"><h2>{h2}</h2>{f"<p>{p}</p>" if p else ""}</div>'


def x_fit(x):
    items = "".join(f"<li>{e(t[0].upper() + t[1:])}</li>" for t in x.get("fit", []))
    return f'<div class="fit"><h2 class="fit-h">This is a good fit if</h2><ul>{items}</ul></div>' if items else ""


def x_deliverables(x, variant):
    d = x.get("deliverables", [])
    cells = "".join(f'<div><h3>{e(i["t"])}</h3><p>{e(i["d"])}</p></div>' for i in d)
    if variant == "sheet":
        return f'<div class="dl-sheet"><div class="dl-sheet-in"><h2 class="dl-sheet-h">What you get <span>℞</span></h2>{cells}</div></div>'
    return f'<div class="dl-{variant}">{cells}</div>'


def x_steps(x, variant):
    return f'<ol class="st-{variant}">' + "".join(f'<li><h3>{e(i["t"])}</h3><p>{e(i["d"])}</p></li>' for i in x.get("steps", [])) + "</ol>"


def x_tools(x, light=False):
    return f'<div class="tl-grid{" light" if light else ""}">' + "".join(
        f'<div><h3>{e(i["t"])}</h3><p>{e(i["d"])}</p></div>' for i in x.get("tools", [])) + "</div>"


def x_glossary(x):
    return '<dl class="gl">' + "".join(f'<div><dt>{e(i["t"])}</dt><dd>{e(i["d"])}</dd></div>' for i in x.get("glossary", [])) + "</dl>"


def build_services():
    for i, s in enumerate(SERVICES):
        g = s["group"]
        group = GROUPS[g][0]
        related = [(o["name"], svc_url(o)) for o in SERVICES if o["group"] == g and o is not s]
        nxt = SERVICES[(i + 1) % len(SERVICES)]
        spec = pick(CUSTOM_ANIM.get(s["slug"], ""), s["anim"])
        caption = "Illustration, not client data" if spec[0] == "chart" or spec[-1] == "dashboard" else ""
        faq_html, faq_ld = faq_block(s["slug"])
        x = EXPLAIN.get(s["slug"])
        crumbs = crumbs_html([("Services", "/#services"), (group, None)])
        h1, lead = e(s["h1"]), e(s["lead"])
        side = slip("Talk to us about this service", "We reply within 24 business hours with packages and pricing.", related, "More in " + e(group.lower()))
        details = f'<section class="section"><div class="wrap layout"><div class="prose"><p class="xp-kicker">The details</p>{s["body"]}</div>{side}</div></section>'
        faq_sec = f'<section class="section tight faq-sec on-mint"><div class="wrap narrow">{faq_html}</div></section>' if faq_html else ""
        graphic = anim(spec, caption)

        if not x:   # explanation not written yet: simple layout
            body = f"""{page_head([("Services", "/#services"), (group, None)], h1, lead, s["img"], s["alt"])}
<section class="section"><div class="wrap layout"><div class="prose">{graphic}{s["body"]}{faq_html}</div>{side}</div></section>"""
        elif g == 0:   # dark head with clip; grid of deliverables
            body = f"""{page_head([("Services", "/#services"), (group, None)], h1, lead, s["img"], s["alt"])}
<section class="section"><div class="wrap xp-two even"><div><p class="xp-kicker">In plain words</p><p class="xp-big">{e(x["plain"])}</p></div>{graphic}</div></section>
<section class="section on-mint"><div class="wrap">{sec_title("What you get", "The concrete pieces we deliver, in plain language.")}{x_deliverables(x, "grid")}</div></section>
<section class="section"><div class="wrap">{sec_title("How it works", "From the first conversation to ongoing results.")}{x_steps(x, "h")}</div></section>
<section class="section on-dark"><div class="wrap">{sec_title("The tools involved, explained", "What each one is, and how we use it for your practice.")}{x_tools(x)}</div></section>
{details}
<section class="section tight flush-top"><div class="wrap xp-two"><div>{sec_title("Words you will hear")}{x_glossary(x)}</div>{x_fit(x)}</div></section>
{faq_sec}"""
        elif g == 1:   # light head, the graphic is the hero; rows; vertical steps
            body = f"""<section class="page-head head-light"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav>
  <div class="page-head-grid"><div><h1>{h1}</h1><p class="lead">{lead}</p></div>{graphic}</div></div></section>
<section class="section"><div class="wrap xp-two"><div><p class="xp-kicker">In plain words</p><p class="xp-big">{e(x["plain"])}</p></div>{x_fit(x)}</div></section>
<section class="section flush-top"><div class="wrap">{sec_title("What you get", "The concrete pieces we deliver, in plain language.")}{x_deliverables(x, "rows")}</div></section>
<section class="section on-dark"><div class="wrap xp-two even"><div>{sec_title("How it works")}{x_steps(x, "v")}</div>{media(s["img"], s["alt"], "split-img reveal-mask")}</div></section>
<section class="section"><div class="wrap">{sec_title("The tools involved, explained", "What each one is, and how we use it for your practice.")}{x_tools(x, light=True)}</div></section>
<section class="section on-mint tight"><div class="wrap">{sec_title("Words you will hear")}{x_glossary(x)}</div></section>
{details}
{faq_sec}"""
        elif g == 2:   # cinematic head; rail of cards
            vid = media(s["img"], s["alt"], "cine-bg", lazy=False)
            body = f"""<section class="page-head head-cine"><div class="wrap">{vid}<nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav>
  <div><h1>{h1}</h1><p class="lead">{lead}</p></div></div></section>
<section class="section on-dark"><div class="wrap xp-two even">{graphic}<div><p class="xp-kicker">In plain words</p><p class="xp-big">{e(x["plain"])}</p></div></div></section>
<section class="section"><div class="wrap">{sec_title("What you get", "Swipe through the pieces we deliver.")}{x_deliverables(x, "rail")}</div></section>
<section class="section on-mint"><div class="wrap">{sec_title("How it works", "From the first conversation to ongoing results.")}{x_steps(x, "h")}</div></section>
<section class="section on-dark"><div class="wrap">{sec_title("The tools involved, explained", "What each one is, and how we use it for your practice.")}{x_tools(x)}</div></section>
{details}
<section class="section tight flush-top"><div class="wrap xp-two"><div>{sec_title("Words you will hear")}{x_glossary(x)}</div>{x_fit(x)}</div></section>
{faq_sec}"""
        else:          # yellow head with a taped print; prescription sheet
            pic = media(s["img"], s["alt"], "page-head-img", lazy=False)
            body = f"""<section class="page-head head-yellow"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav>
  <div class="page-head-grid has-img-grid"><div><h1>{h1}</h1><p class="lead">{lead}</p></div><div class="print"><div class="print-in" data-note="{e(s["name"])}">{pic}</div></div></div></div></section>
<section class="section"><div class="wrap xp-two even"><div><p class="xp-kicker">In plain words</p><p class="xp-big">{e(x["plain"])}</p></div>{graphic}</div></section>
<section class="section on-mint"><div class="wrap xp-two even">{x_deliverables(x, "sheet")}<div>{x_fit(x)}</div></div></section>
<section class="section"><div class="wrap">{sec_title("How it works", "From the first conversation to ongoing results.")}{x_steps(x, "h")}</div></section>
<section class="section on-dark"><div class="wrap">{sec_title("The tools involved, explained", "What each one is, and how we use it for your practice.")}{x_tools(x)}</div></section>
{details}
<section class="section tight flush-top"><div class="wrap">{sec_title("Words you will hear")}{x_glossary(x)}</div></section>
{faq_sec}"""
        body += f"""
<nav class="next" aria-label="Next service"><div class="wrap"><a href="{svc_url(nxt)}"><span><small>Next service</small><b>{e(nxt["name"])}</b></span><i aria-hidden="true"></i></a></div></nav>
{closing()}"""
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "Service", "name": s["h1"], "description": s["lead"], "serviceType": s["name"], "url": SITE + svc_url(s),
             "areaServed": "US", "audience": {"@type": "Audience", "audienceType": "Medical practices"},
             "provider": {"@type": "ProfessionalService", "@id": ORG_ID, "name": "Rx Medical Web", "url": SITE + "/", "telephone": "+1-888-599-4548"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": group, "item": SITE + "/#services"},
                {"@type": "ListItem", "position": 3, "name": s["name"], "item": SITE + svc_url(s)}]}]}
        svc_ld = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>\n"
        page(svc_url(s), f'{s["h1"]} | Rx Medical Web', s["lead"], body, extra_head=faq_ld + svc_ld, og_img=f'/assets/img/{s["img"]}.jpg')


def build_gallery():
    """Local review page for every animated graphic. Not linked, not in the sitemap, not deployed."""
    keys = sorted(f[:-5] for f in os.listdir(ANIM_DIR) if f.endswith(".html")) if os.path.isdir(ANIM_DIR) else []
    cells = "".join(f'<div><h3>{k}</h3>{anim(("x", k))}</div>' for k in keys)
    body = f'<section class="section"><div class="wrap"><h1>Animated graphics</h1><div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:28px">{cells}</div></div></section>'
    page("/dev/gallery/", "Gallery", "Internal review page.", body, extra_head='<meta name="robots" content="noindex">\n')


# ---------------------------------------------------------------- other pages
def build_about():
    about_nav = [("Why choose us", "/about/why-choose-us/"), ("Testimonials", "/about/testimonials/"), ("Our work", "/portfolio/")]
    story = [("2008", "Company founded in Fort Lauderdale."),
             ("2010", "Became the main source of online marketing for Empire Medical Training."),
             ("2012", "Set our focus on the success of doctors and their private practices, and began serving Empire's vendors."),
             ("2016", "Joined forces with Empire Medical Training, after the success stories of so many of its attendees."),
             ("Today", "A strategic partner of Empire, combining an in-house team, a physician advisory board and the latest AI.")]
    tl = "".join(f"<li><b>{y}</b><p>{e(t)}</p></li>" for y, t in story)
    body = f"""{page_head([("About us", None)], "The agency dedicated to medical presence and marketing.", "Family owned, physician owned and in house since 2008. Strategic partner of Empire Medical Training.", "hero-team", "A marketing team and a physician advisor reviewing website designs")}
<section class="section"><div class="wrap xp-two">
  <div><p class="xp-kicker">Who we are</p><p class="xp-big">We do one thing: the online presence and marketing of medical practices. Designers, programmers, marketers, MBAs and physicians work under one roof in Fort Lauderdale, and we do not outsource.</p></div>
  <dl class="about-facts">
    <div><dt>Established</dt><dd>2008</dd></div>
    <div><dt>Practices served</dt><dd>400+ physicians and dentists</dd></div>
    <div><dt>Team</dt><dd>In house, Fort Lauderdale</dd></div>
    <div><dt>Advisors</dt><dd>Physician advisory board</dd></div>
  </dl>
</div></section>
<section class="section on-dark"><div class="wrap">
  {sec_title("The latest AI, checked by people", "AI lets a focused team do more for each practice, faster. Because this is medicine, nothing it produces is published until our staff and physician advisors have reviewed it.")}
  <div class="cols-3 about-ai">
    <div><h3>In our own work</h3><p>Research, design, content drafts, video editing, call analysis and reporting all move faster with current AI tools.</p></div>
    <div><h3>For your patients</h3><p>AI agents answer by chat, text and phone at any hour, using only the information you approve.</p></div>
    <div><h3>With physicians in the loop</h3><p>Our physician advisory board reviews medical content, so what carries your name is accurate.</p></div>
  </div>
</div></section>
{partner()}
{res_teaser()}
<section class="section on-mint"><div class="wrap">{sec_title("Our story")}<ol class="story-line">{tl}</ol></div></section>
<section class="section"><div class="wrap layout">
  <div class="prose"><p class="xp-kicker">The details</p>{ABOUT_BODY}</div>
  {slip("Talk to our team", "Tell us about your practice and your goals.", about_nav, "More about us")}
</div></section>
{closing()}"""
    page("/about/", "About us | Rx Medical Web",
         "Rx Medical Web is a family owned, physician owned medical marketing agency in Fort Lauderdale, serving more than 400 physicians and dentists since 2008.", body)

    why_nav = [("About us", "/about/"), ("Testimonials", "/about/testimonials/"), ("Our work", "/portfolio/")]
    body = f"""{page_head([("About us", "/about/"), ("Why choose us", None)], "Why choose us?", "We are experts in medical marketing: it is all we do, with fair pricing and a team that understands medicine.")}
<section class="section"><div class="wrap layout">
  <div class="prose">{WHY_BODY}</div>
  {slip("Ask us anything", "We are glad to explain how we work before you decide.", why_nav, "More about us")}
</div></section>
{closing()}"""
    page("/about/why-choose-us/", "Why choose us | Rx Medical Web",
         "Experts in medical marketing: fair pricing, results tracking and an in-house team of marketers, MBAs and physicians.", body)

    body = f"""{page_head([("About us", "/about/"), ("Testimonials", None)], "Testimonials", "Good words from good people: physicians and practice owners we have worked with.")}
<section class="section"><div class="wrap">{testimonials_block(full=True)}</div></section>
{closing()}"""
    page("/about/testimonials/", "Testimonials | Rx Medical Web",
         "What physicians and practice owners say about working with Rx Medical Web.", body)


def build_portfolio():
    cases = ""
    for w in WORK:
        tags = "".join(f"<li>{e(t)}</li>" for t in w.get("did", []))
        cases += f"""<article class="case reveal">
  <a class="shot" href="{w["url"]}" rel="noopener"><img src="/assets/img/{w["shot"]}.webp" width="1400" height="801" alt="Screenshot of the {e(w["name"])} website" loading="lazy"></a>
  <div><h2>{e(w["name"])}</h2><p>{e(w["note"])}</p>
    <p class="case-label">What we do for them</p><ul class="case-tags">{tags}</ul>
    <a class="btn btn-line" href="{w["url"]}" rel="noopener">Visit the site</a></div>
</article>"""
    body = f"""{page_head([("Our work", None)], "Our work", "Websites and marketing we build and run every day for our strategic partner, Empire Medical Training, and its family of brands.")}
<section class="section"><div class="wrap cases">{cases}</div></section>
{closing("Want this for your practice?", "Tell us what you have in mind and we will show you how we would build it.")}"""
    page("/portfolio/", "Our work | Rx Medical Web", "Websites and marketing built and run by Rx Medical Web.", body)


PRIVACY_UPDATED = "November 14, 2026"
PRIVACY_BODY = """
<p class="meta">Last updated: {updated}</p>
<p>This policy explains what information Rx Medical Web collects through this website, rxmedicalweb.com, how we use it and the choices you have. It covers this website only. Work we do for a client is governed by our agreement with that client.</p>

<h2>Who we are</h2>
<p>Rx Medical Web is a marketing agency for medical practices, located at 2720 E. Oakland Park Blvd, Suite 103, Fort Lauderdale, FL 33306. You can reach us at <a href="mailto:{email}">{email}</a> or <a href="{tel}">{phone}</a>.</p>

<h2>Information you give us</h2>
<ul>
  <li><strong>When you contact us.</strong> If you call, e-mail or use the request form, we receive what you choose to send: typically your name, practice name, phone number, e-mail address, website and your message. The form on this site does not store anything on our server. It opens your own e-mail application with the details filled in, and nothing is sent until you send that e-mail.</li>
  <li><strong>When you book a call.</strong> The booking page stores what you enter on our server: the time you picked, your name, phone number, e-mail address and, if you add them, your practice, website and a note. We use it to prepare for and make that call. You can cancel from the link shown after you book.</li>
  <li><strong>When you use the site assistant.</strong> The assistant in the corner of each page runs entirely in your browser. It looks up answers in the content of this website. What you type is not sent to us or to anyone else, and it is not stored.</li>
</ul>
<p>Please do not send us patient information or other protected health information through this website, the request form or the assistant.</p>

<h2>Information collected automatically</h2>
<ul>
  <li><strong>Analytics.</strong> We use Google Analytics to understand how visitors use the site: which pages are viewed, roughly where visitors are located, the kind of device and browser, and how visitors arrived. Google Analytics uses cookies or similar identifiers to do this. You can learn how Google handles this information at <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">policies.google.com/technologies/partner-sites</a>, and you can opt out with the browser add-on at <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener">tools.google.com/dlpage/gaoptout</a>.</li>
  <li><strong>Security and delivery.</strong> The site is delivered through Cloudflare, which processes your IP address and basic request details to deliver pages quickly and to protect the site from abuse. Cloudflare may set a cookie that is strictly necessary for security.</li>
  <li><strong>Server logs.</strong> Our web server keeps standard logs of requests, including IP address, date and time, the page requested and the browser used. We use them to keep the site running and secure.</li>
</ul>
<p>We do not use advertising pixels on this website, and the fonts, images and video are served from our own site.</p>

<h2>How we use information</h2>
<ul>
  <li>To answer your questions and prepare the analysis, plan or quote you asked for</li>
  <li>To follow up about our services when you have contacted us</li>
  <li>To understand how the site is used and improve it</li>
  <li>To keep the site secure and prevent abuse</li>
  <li>To comply with the law</li>
</ul>

<h2>How we share information</h2>
<p>We do not sell your personal information, and we do not share it with other companies for their own marketing. We share it only with service providers that help us run this website and our business, such as Google (analytics and e-mail), Cloudflare (delivery and security) and DigitalOcean (hosting), and when the law requires it.</p>

<h2>Text messages and e-mail</h2>
<p>If you give us your phone number or e-mail address, we may use it to reply to your request. We send marketing text messages only to people who have agreed to receive them, and every message explains how to stop. Mobile opt-in information is not shared with third parties for their marketing.</p>

<h2>How long we keep information</h2>
<p>We keep messages and contact details for as long as needed to respond to you and to maintain our business records. Analytics data is kept for the retention period set in our Google Analytics account. Server logs are kept for a limited time and then deleted.</p>

<h2>Your choices and rights</h2>
<p>You can ask us what personal information we hold about you, ask us to correct or delete it, or ask us to stop contacting you. Depending on where you live, the law may give you additional rights. To make a request, write to <a href="mailto:{email}">{email}</a>. We will not treat you differently for making a request.</p>
<p>Most browsers let you block or delete cookies. If you block them, the site will still work.</p>

<h2>Children</h2>
<p>This website is for medical professionals and practice staff. It is not directed to children, and we do not knowingly collect information from children under 13.</p>

<h2>Links to other websites</h2>
<p>This site links to other websites, including examples of our work. Their privacy practices are their own, and this policy does not cover them.</p>

<h2>Changes to this policy</h2>
<p>We may update this policy from time to time. The date at the top shows when it was last changed.</p>
"""


def build_privacy():
    body = f"""{page_head([("Privacy policy", None)], "Privacy policy", "What this website collects, how we use it and the choices you have.")}
<section class="section"><div class="wrap layout">
  <div class="prose">{PRIVACY_BODY.format(updated=PRIVACY_UPDATED, email=EMAIL, tel=PHONE_HREF, phone=PHONE)}</div>
  {slip("Questions about privacy?", "Write or call and we will answer.", [("Contact us", "/contact-us/"), ("About us", "/about/")], "More")}
</div></section>"""
    page("/privacy-policy/", "Privacy policy | Rx Medical Web",
         "How Rx Medical Web handles information collected through rxmedicalweb.com.", body)


# ---------------------------------------------------------------- specialties and resources
def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>\n"


def spec_tiles(tag="h3", skip=None):
    return "".join(
        f'<a class="sp-tile" href="/specialties/{k}/"><img src="/assets/img/{v["img"]}.webp" width="1248" height="832" alt="{e(v["alt"])}" loading="lazy">'
        f'<span><{tag}>{e(v["name"])}</{tag}><i>See the plan</i></span></a>' for k, v in SPECS.items() if k != skip)


def spec_tiles_section():
    return f"""<section class="section sp-home">
  <div class="wrap">
    <div class="section-head reveal">
      <h2>A plan written for your specialty.</h2>
      <p>A med spa and a pain clinic do not find patients the same way. Pick your field and see what we would do first.</p>
    </div>
    <div class="sp-tiles">{spec_tiles()}</div>
  </div>
</section>"""


def res_card(a, tag="h3"):
    return (f'<a class="res-card" href="/resources/{a["slug"]}/"><div class="res-card-img"><img src="/assets/img/{a["img"]}.webp" width="1248" height="832" alt="{e(a["alt"])}" loading="lazy"></div>'
            f'<p class="res-min">{a["min"]} min read</p><{tag}>{e(a["title"])}</{tag}><p>{e(a["dek"])}</p></a>')


def guide_band():
    return f"""<div class="guide-band reveal">
  <div class="guide-cover" aria-hidden="true"><b>40 points</b><span>for your practice's marketing in 2026</span><i>Rx Medical Web</i></div>
  <div>
    <h2>The 40-point marketing checklist for medical practices</h2>
    <p>Every key point from our guides on one printable list: AI search, Google profile, reviews, missed calls, video, privacy and more. Free, no form to fill in.</p>
    <a class="btn btn-ink" href="{GUIDE}" download>Download the checklist (PDF)</a>
  </div>
</div>"""


def res_teaser():
    return f"""<section class="section res-home">
  <div class="wrap">
    <div class="section-head reveal">
      <h2>Advice you can use this week.</h2>
      <p>Practical guides from our team for physicians and practice managers. <a href="/resources/">See all resources</a></p>
    </div>
    <div class="res-grid">{"".join(res_card(a) for a in RESOURCES[:3])}</div>
  </div>
</section>"""


# Pinned graphic of the 90-day plan. Decorative: site.js drives it from the scroll position.
PLAN_STAGE = '''<div class="sc-stage" aria-hidden="true"><div class="sc-card">
        <div class="sc-top"><div class="sc-day"><small>Day</small><b>1</b></div><div class="sc-rail"><i></i><span>Audit</span><span>Foundation</span><span>Launch</span><span>Review</span></div></div>
        <div class="sc-scenes">
          <div class="sc-scene s1"><div class="a-site"><i class="a-dots"></i><i class="a-hero"></i><i class="a-l"></i><i class="a-l"></i><i class="a-l s"></i><i class="a-scan"></i></div>
            <ul class="a-list"><li style="--at:.12">Website</li><li style="--at:.26">Google profile and listings</li><li style="--at:.4">Reviews</li><li style="--at:.54">Ads and phone handling</li></ul></div>
          <div class="sc-scene s2"><em>Where your calls come from</em>
            <ul class="b-bars"><li style="--at:.1;--w:86%">Search<i></i></li><li style="--at:.2;--w:64%">Maps<i></i></li><li style="--at:.3;--w:48%">Ads<i></i></li><li style="--at:.4;--w:30%">Referrals<i></i></li></ul>
            <ul class="b-tog"><li style="--at:.3">Listings corrected</li><li style="--at:.45">Call tracking</li><li style="--at:.6">Dashboard</li></ul></div>
          <div class="sc-scene s3"><div class="c-card c1" style="--at:.08"><u></u><i></i><i></i><i class="s"></i><span>Pages published</span></div>
            <div class="c-card c2" style="--at:.24"><u></u><i></i><i class="s"></i><span>Campaigns live</span></div>
            <div class="c-card c3" style="--at:.4"><p>Thanks for reaching out. Here are two times this week.</p><span>Follow-up on</span></div></div>
          <div class="sc-scene s4"><em>Your 90-day review</em>
            <svg viewBox="0 0 400 150"><defs><linearGradient id="scg" x1="0" x2="1"><stop offset="0" stop-color="#00c0d0"/><stop offset="1" stop-color="#00e060"/></linearGradient></defs><path class="d-grid" d="M0 37H400M0 75H400M0 112H400"/><path class="d-line" pathLength="1" d="M4 128C50 124 70 108 110 104S170 96 200 78 262 70 296 46 360 30 396 16"/></svg>
            <ul class="d-notes"><li style="--at:.3">What worked</li><li style="--at:.44">What we change</li><li style="--at:.58">Next 90 days</li></ul></div>
        </div>
      </div></div>'''


def build_specialties():
    by = {s["slug"]: s for s in SERVICES}
    for slug, sp in SPECS.items():
        asks = "".join(f'<span style="--i:{i}">{e(q)}</span>' for i, q in enumerate(sp["searches"]))
        chal = "".join(f'<li><b>{e(c["t"])}</b><p>{e(c["d"])}</p></li>' for c in sp["challenges"])
        used, pool = set(), [x["img"] for x in SERVICES]
        def pic(sl):
            im = by[sl]["img"]
            if im in used:
                im = next((x for x in pool if x not in used), im)
            used.add(im)
            return im
        plays = "".join(
            f'<a class="sp-play" href="{svc_url(by[pl["slug"]])}"><img src="/assets/img/{pic(pl["slug"])}.webp" width="1248" height="832" alt="" loading="lazy">'
            f'<div><h3>{e(pl["t"])}</h3><p>{e(pl["d"])}</p><i>{e(by[pl["slug"]]["name"])}</i></div></a>' for pl in sp["plays"] if pl["slug"] in by)
        whens = ["Weeks 1–2", "Month 1", "Months 2–3", "Day 90"]
        plan = "".join(f'<li data-when="{whens[i] if i < 4 else ""}"><b>{e(st["t"])}</b><p>{e(st["d"])}</p></li>' for i, st in enumerate(sp["plan"]))
        care = "".join(f"<li>{e(c)}</li>" for c in sp["care"])
        faqs = "".join(f'<details><summary>{e(q["q"])}</summary><p>{e(q["a"])}</p></details>' for q in sp["faqs"])
        url = f"/specialties/{slug}/"
        head = ld({"@context": "https://schema.org", "@type": "FAQPage",
                   "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in sp["faqs"]]})
        head += ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Specialties", "item": SITE + "/specialties/"},
            {"@type": "ListItem", "position": 3, "name": sp["name"], "item": SITE + url}]})
        body = f"""<section class="sp-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="/specialties/">Specialties</a><span>/</span>{e(sp["name"])}</nav>
    <div class="sp-hero-grid">
      <div>
        <p class="sp-kicker">Rx for {e(sp["name"].lower())}</p>
        <h1>{e(sp["h1"])}</h1>
        <p class="lead">{e(sp["lead"])}</p>
        <div class="actions">
          <a class="btn btn-primary" href="/contact-us/#analysis">Request a free analysis</a>
          <a class="btn btn-ghost" href="#plan">See the first 90 days</a>
        </div>
      </div>
      <div class="sp-visual">
        {media(sp["img"], sp["alt"], "sp-photo", lazy=False)}
        <div class="sp-ask" aria-hidden="true"><em>Patients are asking</em><div class="sp-ask-box"><svg viewBox="0 0 24 24" width="18" height="18"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M16.5 16.5 21 21" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg><div class="sp-ask-roll">{asks}</div></div></div>
        <p class="vh">Examples of what patients search for: {e("; ".join(sp["searches"]))}.</p>
      </div>
    </div>
  </div>
</section>
<section class="section sp-chal">
  <div class="wrap">
    <div class="section-head reveal"><h2>What makes this specialty different to market.</h2><p>We start from how your patients decide, not from a list of services.</p></div>
    <ol>{chal}</ol>
  </div>
</section>
<section class="section sp-plays-sec">
  <div class="wrap">
    <div class="section-head reveal"><h2>What we would put to work first.</h2><p>Six services, in the order we would usually start. Each one opens a full explanation.</p></div>
    <div class="sp-plays">{plays}</div>
  </div>
</section>
<section class="section sp-plan" id="plan">
  <div class="wrap">
    <div class="section-head reveal"><h2>Your first 90 days with us.</h2><p>You always know what we are working on and what it produced.</p></div>
    <div class="sc">
      {PLAN_STAGE}
      <ol>{plan}</ol>
    </div>
  </div>
</section>
<section class="section sp-care-sec">
  <div class="wrap sp-care-grid">
    <div class="sp-care reveal">
      <h2>Advertising with care</h2>
      <ul>{care}</ul>
      <p class="fine">General information, not legal advice.</p>
    </div>
    <div class="faq"><h2>Questions we hear from {e(sp["name"].lower())}</h2>{faqs}</div>
  </div>
</section>
<section class="section sp-more">
  <div class="wrap">
    <div class="section-head reveal"><h2>Other specialties we work with.</h2><p>We work only with medical practices. If yours is not listed, <a href="/contact-us/">ask us</a>.</p></div>
    <div class="sp-tiles small">{spec_tiles(skip=slug)}</div>
  </div>
</section>
{closing(f"Let us look at your practice.", "Send us your website. We will tell you what we would fix first, at no charge.")}"""
        page(url, f'{sp["h1"]} | Rx Medical Web', sp["lead"], body, head, og_img=f'/assets/img/{sp["img"]}.jpg')

    body = f"""{page_head([("Specialties", None)], "Marketing built around your specialty", "Each field of medicine finds its patients differently. Choose yours to see the challenges we plan for, the services we would start with and what the first 90 days look like.")}
<section class="section"><div class="wrap">
  <div class="sp-tiles big">{spec_tiles("h2")}</div>
  <p class="sp-also">We also work with practices in {e(", ".join(x.lower() for x in SPECIALTIES if x not in ("Aesthetics", "Dermatology", "Plastic surgery", "Med spas", "Dentistry", "Pain management", "Family practice", "Weight loss", "Anti-aging medicine")))} and other fields. <a href="/contact-us/">Tell us about yours</a>.</p>
</div></section>
{partner()}
{closing()}"""
    page("/specialties/", "Medical marketing by specialty | Rx Medical Web",
         "Marketing plans for med spas, dermatology, plastic surgery, dental, weight loss, pain management, hormone therapy and family practice.", body)


def build_resources():
    by = {s["slug"]: s for s in SERVICES}
    for i, a in enumerate(RESOURCES):
        url = f'/resources/{a["slug"]}/'
        rel = [(by[x]["name"], svc_url(by[x])) for x in a["rel"] if x in by]
        nxt = [RESOURCES[(i + n) % len(RESOURCES)] for n in (1, 2, 3)]
        take = "".join(f"<li>{e(t)}</li>" for t in a["takeaways"])
        head = ld({"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["dek"],
                   "image": f'{SITE}/assets/img/{a["img"]}.jpg', "datePublished": RES_ISO, "dateModified": RES_ISO,
                   "author": {"@type": "Organization", "name": "Rx Medical Web", "url": SITE + "/about/"},
                   "publisher": {"@type": "Organization", "@id": ORG_ID, "name": "Rx Medical Web", "logo": {"@type": "ImageObject", "url": f"{SITE}{UP}mainlogo.png"}},
                   "mainEntityOfPage": SITE + url})
        body = f"""<section class="res-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="/resources/">Resources</a></nav>
    <div class="res-hero-grid">
      <div><p class="res-min">Guide · {a["min"]} min read</p><h1>{e(a["title"])}</h1><p class="lead">{e(a["dek"])}</p><p class="res-by">By the Rx Medical Web team · {RES_DATE}</p></div>
      <img class="res-hero-img" src="/assets/img/{a["img"]}.webp" width="1248" height="832" alt="{e(a["alt"])}">
    </div>
  </div>
</section>
<section class="section"><div class="wrap layout">
  <article class="prose res-body">
    <div class="res-take"><h2>In short</h2><ul>{take}</ul></div>
    {a["html"]}
    <p class="fine">This article is general information for medical practices. It is not legal or medical advice.</p>
  </article>
  {slip("Want help with this?", "We will look at your practice and tell you what we would do first.", rel, "Services in this guide")}
</div></section>
<section class="section res-next"><div class="wrap">
  <div class="section-head"><h2>Keep reading</h2><p><a href="/resources/">All resources</a></p></div>
  <div class="res-grid">{"".join(res_card(x) for x in nxt)}</div>
  {guide_band()}
</div></section>
{closing()}"""
        page(url, f'{a["title"]} | Rx Medical Web', a["dek"], body, head, og_img=f'/assets/img/{a["img"]}.jpg', og_type="article")

    f0 = RESOURCES[0]
    body = f"""{page_head([("Resources", None)], "Resources for medical practices", "Practical guides on finding patients, answering them and keeping them, written by our team for physicians and practice managers.")}
<section class="section"><div class="wrap">
  <a class="res-feature reveal" href="/resources/{f0["slug"]}/">
    <div class="res-card-img"><img src="/assets/img/{f0["img"]}.webp" width="1248" height="832" alt="{e(f0["alt"])}"></div>
    <div><p class="res-min">Start here · {f0["min"]} min read</p><h2>{e(f0["title"])}</h2><p>{e(f0["dek"])}</p><span class="btn btn-ink">Read the guide</span></div>
  </a>
  <div class="res-grid">{"".join(res_card(a, "h2") for a in RESOURCES[1:])}</div>
  {guide_band()}
</div></section>
{closing("Have a question we have not covered?", "Ask us. We answer within 24 business hours.")}"""
    page("/resources/", "Resources for medical practices | Rx Medical Web",
         "Free guides for physicians and practice managers: AI search, Google Business Profile, reviews, missed calls, video, patient privacy and more.", body)


def build_booking():
    def field(name, label, typ="text", req=False, auto=""):
        ac = f' autocomplete="{auto}"' if auto else ""
        opt = "" if req else " <i>optional</i>"
        return f'<label class="bk-f"><span>{label}{opt}</span><input type="{typ}" name="{name}"{" required" if req else ""}{ac}></label>'
    body = f"""<section class="bk-hero">
  <div class="wrap bk-grid">
    <div class="bk-intro">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>Book a call</nav>
      <p class="sp-kicker">Thirty minutes, no charge</p>
      <h1>Pick a time. We will call you.</h1>
      <p class="lead">Tell us about your practice and what you want more of. You will talk with someone from our team who works only with medical practices.</p>
      <ol class="bk-what">
        <li><b>Before the call</b>We look at your website, your Google profile and your reviews.</li>
        <li><b>On the call</b>We tell you what we would fix first, and answer your questions.</li>
        <li><b>After the call</b>You get a written plan with packages and pricing. No obligation.</li>
      </ol>
      <p class="bk-alt">Rather call now? <a href="{PHONE_HREF}">{PHONE}</a>, Monday to Friday, 9 am to 6 pm Eastern.</p>
    </div>
    <div class="bk-card" data-booking>
      <div class="bk-pick">
        <h2><i>1</i>Pick a day</h2>
        <div class="bk-days" role="group" aria-label="Day"></div>
        <h2><i>2</i>Pick a time</h2>
        <div class="bk-times" role="group" aria-label="Time"></div>
        <p class="bk-tz"></p>
        <p class="bk-status" role="status">Loading open times…</p>
        <noscript><p>The calendar needs JavaScript. Please call us at {PHONE} or write to {EMAIL}.</p></noscript>
      </div>
      <form class="bk-form" novalidate>
        <h2><i>3</i>Where do we call you?</h2>
        <p class="bk-sel">Your call: <b class="bk-chosen">no time picked yet</b></p>
        <div class="bk-fields">
          {field("name", "Your name", req=True, auto="name")}
          {field("practice", "Practice", auto="organization")}
          {field("phone", "Phone", "tel", True, "tel")}
          {field("email", "E-mail", "email", True, "email")}
          {field("website", "Website", auto="url")}
          <label class="bk-f"><span>Topic</span><select name="topic"></select></label>
          <label class="bk-f bk-wide"><span>Anything we should know <i>optional</i></span><textarea name="notes" rows="2"></textarea></label>
          <label class="bk-hp" aria-hidden="true">Company URL<input type="text" name="company_url" tabindex="-1" autocomplete="off"></label>
        </div>
        <p class="bk-error" role="alert"></p>
        <button type="submit" class="btn btn-primary" disabled>Book the call</button>
        <p class="fine">Please do not include patient information. We use your details only to prepare for and make this call. See our <a href="/privacy-policy/">privacy policy</a>.</p>
      </form>
      <div class="bk-done" aria-live="polite">
        <svg viewBox="0 0 48 48" width="56" height="56" aria-hidden="true"><circle cx="24" cy="24" r="22" fill="#00e060"/><path d="M14 25l7 7 13-15" fill="none" stroke="#0b2f38" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <h2>Your call is booked</h2>
        <p class="bk-when"></p>
        <p>We will call you at <b class="bk-phone"></b>. If something changes, call us at {PHONE}.</p>
        <a class="btn btn-ink bk-ics" href="#">Add to my calendar</a>
        <p class="fine"><a class="bk-cancel" href="#">Cancel this call</a></p>
      </div>
    </div>
  </div>
</section>
<script src="/assets/booking.js?v={ver("assets/booking.js")}" defer></script>"""
    page("/book-a-call/", "Book a call | Rx Medical Web",
         "Pick a time for a free 30-minute call with Rx Medical Web. We look at your practice's website first and tell you what we would fix.", body)


def build_404():
    body = f"""<section class="page-head lost"><div class="wrap">
  <p class="lost-rx" aria-hidden="true">℞</p>
  <h1>This page is out of stock.</h1>
  <p class="lead">The address may have changed in our redesign. Here is where most people are headed.</p>
  <div class="hero-actions"><a class="btn btn-primary" href="/">Go to the home page</a><a class="btn btn-ghost" href="/#services">See all services</a><a class="btn btn-ghost" href="/contact-us/">Contact us</a></div>
</div></section>"""
    page("/404/", "Page not found | Rx Medical Web", "Page not found.", body, extra_head='<meta name="robots" content="noindex">\n')
    os.replace(os.path.join(ROOT, "404", "index.html"), os.path.join(ROOT, "404.html"))
    os.rmdir(os.path.join(ROOT, "404"))
    BUILT.remove("/404/")


def build_contact():
    topics = "".join(f"<option>{e(s['name'])}</option>" for s in SERVICES)
    body = f"""{page_head([("Contact us", None)], "Contact us and we will give you a solution.", "We appreciate your business and reply within 24 business hours, including our packages and pricing.")}
<section class="section"><div class="wrap contact-grid">
  <div>
    <dl class="contact-list">
      <div><dt>Toll free</dt><dd><a href="{PHONE_HREF}">{PHONE}</a></dd></div>
      <div><dt>Phone</dt><dd><a href="{LOCAL_PHONE_HREF}">{LOCAL_PHONE}</a></dd></div>
      <div><dt>E-mail</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
      <div><dt>Address</dt><dd>2720 E. Oakland Park Blvd, Suite 103<br>Fort Lauderdale, FL 33306<br><a href="https://maps.google.com/?q=2720+E+Oakland+Park+Blvd+Fort+Lauderdale+FL+33306" rel="noopener">See on the map</a></dd></div>
      <div><dt>Hours</dt><dd>Monday to Friday<br>9 am to 6 pm</dd></div>
    </dl>
  </div>
  <form class="form" id="analysis" data-mailto="{EMAIL}" action="mailto:{EMAIL}" method="post" enctype="text/plain">
    <h2>Request a free website analysis</h2>
    <div class="form-row">
      <label class="field"><span>Your name</span><input name="name" autocomplete="name" required></label>
      <label class="field"><span>Practice name</span><input name="practice" autocomplete="organization"></label>
    </div>
    <div class="form-row">
      <label class="field"><span>Phone</span><input name="phone" type="tel" autocomplete="tel"></label>
      <label class="field"><span>E-mail</span><input name="email" type="email" autocomplete="email" required></label>
    </div>
    <label class="field"><span>Current website, if you have one</span><input name="website" type="text" inputmode="url" placeholder="yourpractice.com"></label>
    <label class="field"><span>What are you interested in?</span><select name="topic"><option>Free website analysis</option>{topics}<option>Something else</option></select></label>
    <label class="field"><span>Tell us about your practice</span><textarea name="message"></textarea></label>
    <button class="btn btn-ink" type="submit">Send request by e-mail</button>
    <small>This opens your e-mail app with the details filled in. Please do not include patient information. You can also call us at {PHONE}. See our <a href="/privacy-policy/">privacy policy</a>.</small>
  </form>
</div></section>"""
    page("/contact-us/", "Contact us | Rx Medical Web",
         "Contact Rx Medical Web in Fort Lauderdale. Call 1-888-599-4548 or request a free website analysis. We reply within 24 business hours.", body)


def build_articles():
    for a in ARTICLES:
        others = [(o["title"], f'/{o["path"]}/') for o in ARTICLES if o is not a]
        body = f"""{page_head([("Articles", None)], e(a["title"]), e(a["lead"]), a["img"], a["alt"])}
<section class="section"><div class="wrap layout">
  <article class="prose"><p class="meta">Published {a["date"]}</p>{a["body"]}</article>
  {slip("Talk to our team", "We reply within 24 business hours.", others + [("Medical website design", "/service/medical-website-design/")], "Keep reading")}
</div></section>
{closing()}"""
        page(f'/{a["path"]}/', f'{a["title"]} | Rx Medical Web', a["lead"], body, og_img=f'/assets/img/{a["img"]}.jpg')


def build_chat_index():
    """Knowledge for the site assistant: every answer is text that already exists on the site."""
    docs = []
    for s in SERVICES:
        x = EXPLAIN.get(s["slug"], {})
        kw = " ".join([s["name"], s["h1"], s["blurb"], s["lead"]] + [d["t"] for d in x.get("deliverables", [])]
                      + [t["t"] for t in x.get("tools", [])] + [g["t"] for g in x.get("glossary", [])])
        docs.append({"t": s["name"], "u": svc_url(s), "k": kw, "a": x.get("plain") or s["lead"], "s": 1})
        for q in FAQS.get(s["slug"], []):
            docs.append({"t": s["name"], "u": svc_url(s), "q": q["q"], "a": q["a"]})
    groups = [{"g": g, "items": [{"t": s["name"], "u": svc_url(s)} for s in SERVICES if s["group"] == i]} for i, (g, _) in enumerate(GROUPS)]
    general = [
        {"t": "About Rx Medical Web", "u": "/about/", "q": "Who are you? What is Rx Medical Web? Tell me about your company agency team experience",
         "a": "Rx Medical Web is a family owned, physician owned marketing agency in Fort Lauderdale. Medical marketing is all we do: since 2008 we have worked with more than 400 physicians and dentists, with an in-house team and a physician advisory board."},
        {"t": "Empire Medical Training", "u": "/about/", "q": "Empire Medical Training partner partnership relationship courses trained",
         "a": "We are the strategic marketing partner of Empire Medical Training and have marketed its courses for more than fifteen years. If you trained there and are adding a new procedure, we already know how to launch it."},
        {"t": "How we use AI", "u": "/about/", "q": "Do you use AI artificial intelligence technology ChatGPT how",
         "a": "We use the latest AI technology across our work: research, design, content drafts, video, call analysis and the AI agents we set up for practices. Because this is medicine, our staff and physician advisors review what AI produces before it is published."},
        {"t": "Our work", "u": "/portfolio/", "q": "portfolio examples work clients sites you built case studies",
         "a": "Our portfolio shows what we build and run for Empire Medical Training and its family of brands: the main website, the member portal, the iPhone and Android app, Empire On-Demand, AAOPM, Empire Verified and the provider locator."},
        {"t": "Specialties", "u": "/", "q": "Which specialties do you work with? dentist dermatologist plastic surgeon med spa chiropractor aesthetics pain management",
         "a": "We work only with medical practices: aesthetics, dermatology, plastic surgery, med spas, dentistry, gynecology, pain management, cardiology, chiropractic, family practice, weight loss and anti-aging medicine, among others."},
    ]
    for k, sp in SPECS.items():
        general.append({"t": sp["name"], "u": f"/specialties/{k}/", "q": sp["name"] + " " + sp["h1"] + " " + " ".join(sp["searches"]), "a": sp["lead"] + " See our plan for this specialty."})
        for q in sp["faqs"]:
            general.append({"t": sp["name"], "u": f"/specialties/{k}/", "q": q["q"], "a": q["a"]})
    for a in RESOURCES:
        general.append({"t": a["title"], "u": f'/resources/{a["slug"]}/', "q": a["title"] + " " + a["dek"], "a": a["takeaways"][0] + " " + a["takeaways"][1]})
    data = {"docs": docs + general, "groups": groups, "phone": PHONE, "tel": PHONE_HREF, "email": EMAIL}
    with open(os.path.join(ROOT, "assets", "chat-index.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


def build_sitemap():
    """lastmod only changes when the page's own content changes (kept in src/lastmod.json)."""
    store_path = os.path.join(ROOT, "src", "lastmod.json")
    store = json.load(open(store_path, encoding="utf-8")) if os.path.exists(store_path) else {}
    today = datetime.date.today().isoformat()
    for p in BUILT:
        if store.get(p, {}).get("hash") != LASTMOD.get(p):
            store[p] = {"hash": LASTMOD.get(p), "date": today}
    store = {p: store[p] for p in BUILT}
    with open(store_path, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=1, sort_keys=True)
        f.write("\n")
    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{store[p]['date']}</lastmod></url>\n" for p in BUILT)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")


def build_llms():
    """llms.txt: a plain summary of the site for AI assistants."""
    L = ["# Rx Medical Web", "",
         "> Marketing agency dedicated to medical practices: websites, SEO, advertising, social media, AI agents, apps, e-mail and text marketing, and printing. Physician owned, based in Fort Lauderdale, Florida. Strategic partner of Empire Medical Training.", "",
         "Contact: 1-888-599-4548, support@rxmedicalweb.com, " + SITE + "/contact-us/", "", "## Services", ""]
    L += [f"- [{s['name']}]({SITE}{svc_url(s)}): {s['lead']}" for s in SERVICES]
    L += ["", "## Specialties", ""] + [f"- [{v['name']}]({SITE}/specialties/{k}/): {v['lead']}" for k, v in SPECS.items()]
    L += ["", "## Guides", ""] + [f"- [{a['title']}]({SITE}/resources/{a['slug']}/): {a['dek']}" for a in RESOURCES]
    L += ["", "## Company", "", f"- [About us]({SITE}/about/)", f"- [Why choose us]({SITE}/about/why-choose-us/)", f"- [Our work]({SITE}/portfolio/)", f"- [Privacy policy]({SITE}/privacy-policy/)"]
    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    build_home()
    build_services()
    build_about()
    build_portfolio()
    build_contact()
    build_articles()
    build_specialties()
    build_resources()
    build_privacy()
    build_booking()
    build_404()
    build_chat_index()
    build_sitemap()
    build_llms()
    build_gallery()
    print(f"built {len(BUILT)} pages")
