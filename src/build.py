#!/usr/bin/env python3
"""Static site generator for rxmedicalweb.com.

    python3 src/build.py

Reads the content in src/pages.py and writes every page as <path>/index.html at the
repo root, plus sitemap.xml. No dependencies beyond the standard library.
"""
import datetime
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages import *  # noqa: E402,F401,F403

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://rxmedicalweb.com"
YEAR = datetime.date.today().year
UP = "/wp-content/uploads/"
BUILT = []


def e(s):
    return html.escape(s, quote=True)


def svc_url(s):
    return f"/service/{s['slug']}/"


# ---------------------------------------------------------------- shared chrome
def menu():
    cols = []
    for gi, (gname, _) in enumerate(GROUPS):
        links = "".join(f'<a href="{svc_url(s)}">{e(s["name"])}</a>' for s in SERVICES if s["group"] == gi)
        cols.append(f"<div><h4>{e(gname)}</h4>{links}</div>")
    return "".join(cols)


def header(path):
    def cur(p):
        return ' aria-current="page"' if path == p else ""
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Rx Medical Web, home"><img src="{UP}mainlogo.png" width="400" height="83" alt="Rx Medical Web. Physicians Rx for Success"></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main">
      <div class="nav-services">
        <button aria-expanded="false" aria-controls="services-menu">Services</button>
        <div class="menu" id="services-menu">{menu()}</div>
      </div>
      <a href="/about/"{cur('/about/')}>About</a>
      <a href="/portfolio/"{cur('/portfolio/')}>Our work</a>
      <a href="/about/testimonials/"{cur('/about/testimonials/')}>Testimonials</a>
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
        cols.append(f"<div><h4>{e(gname)}</h4><ul>{links}</ul></div>")
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <img src="{UP}mainlogo.png" width="400" height="83" alt="Rx Medical Web" loading="lazy">
        <address>2720 E. Oakland Park Blvd, Suite 103<br>Fort Lauderdale, FL 33306<br>Monday to Friday, 9 am to 6 pm</address>
      </div>
      <div><h4>Contact</h4><ul>
        <li><a href="{PHONE_HREF}">{PHONE}</a></li>
        <li><a href="{LOCAL_PHONE_HREF}">{LOCAL_PHONE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="/contact-us/">Contact us</a></li>
      </ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="/about/">About us</a></li>
        <li><a href="/about/why-choose-us/">Why choose us</a></li>
        <li><a href="/about/testimonials/">Testimonials</a></li>
        <li><a href="/portfolio/">Our work</a></li>
      </ul></div>
      <div><h4>Strategic partner</h4><ul>
        <li><a href="https://www.empiremedicaltraining.com/" rel="noopener">Empire Medical Training</a></li>
      </ul><h4 class="gap">Follow us</h4><ul>
        <li><a href="https://www.linkedin.com/company/rx-medical-web" rel="noopener">LinkedIn</a></li>
        <li><a href="https://www.facebook.com/rxmedicalweb/" rel="noopener">Facebook</a></li>
      </ul></div>
    </div>
    <div class="footer-grid">{''.join(cols)}</div>
    <div class="footer-legal"><span>© {YEAR} Rx Medical Web. All rights reserved.</span><span>Medical presence and marketing, Fort Lauderdale, Florida</span></div>
  </div>
</footer>"""


def page(path, title, desc, body, extra_head="", og_img="/assets/img/hero-clinic.jpg"):
    """path like '/' or '/about/'."""
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Rx Medical Web">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}{og_img}">
<meta name="theme-color" content="#0b2f38">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Caveat:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<script>document.documentElement.className='js'</script>
{extra_head}</head>
<body>
{header(path)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/site.js" defer></script>
</body>
</html>
"""
    out = os.path.join(ROOT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    BUILT.append(path)


# ---------------------------------------------------------------- animated graphics
def anim(spec, caption=""):
    kind = spec[0]
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
    return (f'<div class="who"><img src="{UP}{t["img"]}" width="76" height="76" alt="" loading="lazy">'
            f'<div><b>{e(t["name"])}</b><span>{e(t["role"])}</span></div></div>')


def testimonials_block(full=False):
    lead = TESTIMONIALS[0]
    rest = "".join(f'<figure><blockquote>“{e(t["quote"])}”</blockquote><figcaption>{who(t)}</figcaption></figure>'
                   for t in TESTIMONIALS[1:])
    more = "" if full else '<a class="btn btn-line" href="/about/testimonials/">Read all testimonials</a>'
    return f"""<div class="quote-lead">
  <figure><blockquote>“{e(lead["quote"])}”</blockquote><figcaption>{who(lead)}</figcaption></figure>
  <div class="quote-aside">
    <h3>Good words from good people</h3>
    <p>Many of our clients first met us through Empire Medical Training, then asked us to build the website and marketing for the services they had just learned.</p>
    {more}
  </div>
</div>
<div class="quotes">{rest}</div>"""


def work_cards(tag="h3"):
    return "".join(
        f'<a href="{w["url"]}" rel="noopener"><div class="shot"><img src="{UP}{w["img"]}" width="700" height="525" alt="Screenshot of the {e(w["name"])} website" loading="lazy"></div>'
        f'<{tag}>{e(w["name"])}</{tag}><p>{e(w["note"])}</p></a>' for w in WORK)


def page_head(crumbs, h1, lead, img=None, alt=""):
    trail = '<a href="/">Home</a>' + "".join(
        f'<span>/</span><a href="{u}">{e(t)}</a>' if u else f'<span>/</span>{e(t)}' for t, u in crumbs)
    pic = f'<img class="page-head-img" src="/assets/img/{img}.webp" width="1248" height="832" alt="{e(alt)}">' if img else ""
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


# ---------------------------------------------------------------- home
def build_home():
    groups = []
    for gi, (gname, gdesc) in enumerate(GROUPS):
        rows = "".join(
            f'<li><a href="{svc_url(s)}"><b>{e(s["name"])}</b><span>{e(s["blurb"])}</span></a></li>'
            for s in SERVICES if s["group"] == gi)
        groups.append(f'<div class="formulary-group"><h3>{e(gname)}<small>{e(gdesc)}</small></h3><ul class="formulary-list">{rows}</ul></div>')

    body = f"""<section class="hero hero-video">
  <video class="hero-bg" autoplay muted loop playsinline preload="metadata" poster="/assets/img/hero-clinic.jpg" aria-hidden="true" tabindex="-1">
    <source src="/assets/video/hero.mp4" type="video/mp4">
  </video>
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <h1>The marketing prescription for your medical practice.</h1>
        <p class="lead">Rx Medical Web is the agency dedicated to medical presence and marketing. Websites, SEO, advertising, social media and AI agents, built by an in-house team with the latest AI technology and reviewed by physicians.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="/contact-us/#analysis">Request a free website analysis</a>
          <a class="btn btn-ghost" href="{PHONE_HREF}">Call {PHONE}</a>
        </div>
      </div>
      <div class="pad" role="img" aria-label="A prescription from Rx Medical Web for your practice: a custom website; SEO, ads and AI search; AI agents around the clock; social, email and SMS. Refills monthly.">
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
      </div>
    </div>
    <dl class="facts">
      <div class="fact"><dt>Established</dt><dd>2008</dd></div>
      <div class="fact"><dt>Practices served</dt><dd>400+ physicians and dentists</dd></div>
      <div class="fact"><dt>Team</dt><dd>In house, Fort Lauderdale</dd></div>
      <div class="fact"><dt>Strategic partner</dt><dd>Empire Medical Training</dd></div>
    </dl>
  </div>
</section>

<section class="section" id="services">
  <div class="wrap">
    <div class="section-head">
      <h2>Everything your practice needs to be found, chosen and booked.</h2>
      <p>One team for the whole job, from your first website to advanced campaigns. Pick a single service or let us run all of it.</p>
    </div>
    <div class="formulary">{''.join(groups)}</div>
  </div>
</section>

<section class="section ai-band">
  <div class="wrap">
    <div class="section-head">
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
        {anim(("chat", AGENT_CHAT))}
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

<section class="section section-mint">
  <div class="wrap">
    <div class="section-head">
      <h2>How a patient reaches you.</h2>
      <p>Every service we offer supports one step of this path. We measure the whole thing by the calls and bookings at the end.</p>
    </div>
    {anim(("flow", ["Searches or asks AI", "Lands on your website", "Chats, calls or books", "Visits your practice", "Leaves a review", "Comes back"]))}
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <img class="split-img" src="/assets/img/hero-team.webp" width="1280" height="720" alt="A marketing team and a physician advisor reviewing website designs" loading="lazy">
    <div>
      <h2>Marketers who understand medicine.</h2>
      <p class="lead">We are a physician owned, family owned agency. Designers, programmers, marketers, MBAs and a physician advisory board work together in Fort Lauderdale. We do not outsource.</p>
      <div class="cols-2 split-cols">
        <div><h3>Strategic partner of Empire Medical Training</h3><p>We have marketed Empire's courses for more than fifteen years. When you add a procedure you learned there, we already know how to launch it.</p></div>
        <div><h3>Results you can count</h3><p>Our results and phone tracking system shows the calls and bookings your marketing produces, not just clicks.</p></div>
      </div>
      <p class="split-cta"><a class="btn btn-line" href="/about/why-choose-us/">Why practices choose us</a></p>
    </div>
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
    <div class="section-head">
      <h2>Recent work</h2>
      <p>Some of our most recent website launches.</p>
    </div>
    <div class="work-3">{work_cards()}</div>
  </div>
</section>

<section class="section section-mint">
  <div class="wrap">{testimonials_block()}</div>
</section>

{closing()}"""
    ld = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"ProfessionalService","name":"Rx Medical Web","url":"https://rxmedicalweb.com/","logo":"https://rxmedicalweb.com/wp-content/uploads/mainlogo.png","image":"https://rxmedicalweb.com/assets/img/hero-clinic.jpg","description":"Marketing agency dedicated to medical presence and marketing: websites, SEO, advertising, social media and AI agents for medical practices.","telephone":"+1-888-599-4548","email":"support@rxmedicalweb.com","foundingDate":"2008","address":{"@type":"PostalAddress","streetAddress":"2720 E. Oakland Park Blvd, Suite 103","addressLocality":"Fort Lauderdale","addressRegion":"FL","postalCode":"33306","addressCountry":"US"},"openingHours":"Mo-Fr 09:00-18:00","sameAs":["https://www.linkedin.com/company/rx-medical-web","https://www.facebook.com/rxmedicalweb/"]}</script>
"""
    page("/", "Rx Medical Web | Medical website design and marketing agency",
         "Rx Medical Web is the marketing agency dedicated to medical practices: websites, SEO, ads, social media, AI agents and more. Strategic partner of Empire Medical Training.",
         body, extra_head=ld)


# ---------------------------------------------------------------- services
def build_services():
    for s in SERVICES:
        group = GROUPS[s["group"]][0]
        related = [(o["name"], svc_url(o)) for o in SERVICES if o["group"] == s["group"] and o is not s]
        body = f"""{page_head([("Services", "/#services"), (group, None)], e(s["h1"]), e(s["lead"]), s["img"], s["alt"])}
<section class="section">
  <div class="wrap layout">
    <div class="prose">
      {anim(s["anim"], "Illustration, not client data" if s["anim"][0] == "chart" else "How it works")}
      {s["body"]}
    </div>
    {slip("Talk to us about this service", "We reply within 24 business hours with packages and pricing.", related, "More in " + e(group.lower()))}
  </div>
</section>
{closing()}"""
        page(svc_url(s), f'{s["h1"]} | Rx Medical Web', s["lead"], body, og_img=f'/assets/img/{s["img"]}.jpg')


# ---------------------------------------------------------------- other pages
def build_about():
    about_nav = [("Why choose us", "/about/why-choose-us/"), ("Testimonials", "/about/testimonials/"), ("Our work", "/portfolio/")]
    body = f"""{page_head([("About us", None)], "The agency dedicated to medical presence and marketing.", "Family owned, physician owned and in house since 2008. Strategic partner of Empire Medical Training.")}
<section class="section"><div class="wrap layout">
  <div class="prose">{ABOUT_BODY}</div>
  {slip("Talk to our team", "Tell us about your practice and your goals.", about_nav, "More about us")}
</div></section>
{closing()}"""
    page("/about/", "About us | Rx Medical Web",
         "Rx Medical Web is a family owned, physician owned medical marketing agency in Fort Lauderdale, serving more than 400 physicians and dentists since 2008.", body)

    why_nav = [("About us", "/about/"), ("Testimonials", "/about/testimonials/"), ("Our work", "/portfolio/")]
    body = f"""{page_head([("About us", "/about/"), ("Why choose us", None)], "Why choose us?", "A written guarantee, fair pricing and a team that understands medicine.")}
<section class="section"><div class="wrap layout">
  <div class="prose">{WHY_BODY}</div>
  {slip("Ask us anything", "We are glad to explain how we work before you decide.", why_nav, "More about us")}
</div></section>
{closing()}"""
    page("/about/why-choose-us/", "Why choose us | Rx Medical Web",
         "A written money back guarantee, fair pricing, results tracking and an in-house team of marketers, MBAs and physicians.", body)

    body = f"""{page_head([("About us", "/about/"), ("Testimonials", None)], "Testimonials", "Good words from good people: physicians and practice owners we have worked with.")}
<section class="section"><div class="wrap">{testimonials_block(full=True)}</div></section>
{closing()}"""
    page("/about/testimonials/", "Testimonials | Rx Medical Web",
         "What physicians and practice owners say about working with Rx Medical Web.", body)


def build_portfolio():
    body = f"""{page_head([("Our work", None)], "Our work", "Some of our most recent website launches.")}
<section class="section"><div class="wrap"><div class="work-3">{work_cards("h2")}</div></div></section>
{closing("Need more for your marketing?", "Have specific requirements? Send us the details.")}"""
    page("/portfolio/", "Our work | Rx Medical Web", "Recent website launches by Rx Medical Web.", body)


def build_contact():
    topics = "".join(f"<option>{e(s['name'])}</option>" for s in SERVICES)
    body = f"""{page_head([("Contact us", None)], "Contact us and we will give you a solution.", "We appreciate your business and guarantee a response within 24 business hours, including our packages and pricing.")}
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
    <small>This opens your e-mail app with the details filled in. Please do not include patient information. You can also call us at {PHONE}.</small>
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

    # Old WordPress attachment URL: send visitors and search engines to the service page.
    target = "/service/medical-website-design/"
    out = os.path.join(ROOT, "medical-website-design", "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Medical website design | Rx Medical Web</title>'
                f'<link rel="canonical" href="{SITE}{target}"><meta http-equiv="refresh" content="0; url={target}">'
                f'<meta name="robots" content="noindex"></head><body><p><a href="{target}">Medical website design</a></p></body></html>\n')


def build_sitemap():
    today = datetime.date.today().isoformat()
    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{today}</lastmod></url>\n" for p in BUILT)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")


if __name__ == "__main__":
    build_home()
    build_services()
    build_about()
    build_portfolio()
    build_contact()
    build_articles()
    build_sitemap()
    print(f"built {len(BUILT)} pages")
