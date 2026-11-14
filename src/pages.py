"""Content for rxmedicalweb.com. Edit here, then run `python3 src/build.py`.

Each service: group, slug, name (menu), h1, lead, blurb (home index), img (assets/img/<img>.webp), alt,
anim (animated graphic: ("flow", [steps]) | ("serp",) | ("chat", [(who, text)]) | ("chart",) | ("stars",) | ("build",)),
body (HTML).
"""

PHONE = "1-888-599-4548"
PHONE_HREF = "tel:+18885994548"
LOCAL_PHONE = "(954) 358-2856"
LOCAL_PHONE_HREF = "tel:+19543582856"
EMAIL = "support@rxmedicalweb.com"

GROUPS = [
    ("Websites", "Sites built from scratch for medical practices, and everything that keeps them running."),
    ("Get found", "Show up where patients look: Google, maps, AI answers and review sites."),
    ("Stay in touch", "Content, conversations and AI agents that keep your practice in front of patients."),
    ("Brand and growth", "Strategy, launches, print and proof of what the marketing brings in."),
]

AGENT_CHAT = [
    ("them", "Hi, do you offer Botox? Any openings Thursday?"),
    ("us", "Yes, we do. Thursday has 2:30 or 4:00 open. Which works for you?"),
    ("them", "4:00 please."),
    ("us", "Done. Your request is in and a text confirmation is on its way."),
]
AI_SEARCH_CHAT = [
    ("them", "Who is a good doctor near me for laser hair removal?"),
    ("us", "Your practice is well reviewed for laser hair removal, with board certified physicians and online booking. Here is how to reach them."),
]

SERVICES = [
    # ------------------------------------------------------------------ Websites
    dict(group=0, slug="medical-website-design", name="Medical website design",
         h1="Medical website design",
         lead="Custom websites for medical, aesthetic and dental practices, designed and programmed in house and built to turn visitors into patient calls.",
         blurb="Custom sites for medical, aesthetic and dental practices. No templates.",
         img="studio", alt="Designers working on website layouts in a bright studio",
         anim=("build",),
         body="""
<p>Your website is where every campaign ends up, whether a patient finds you through search, maps, social media or an AI assistant. For a medical, aesthetic or dental practice, it is the most effective tool you have to reach new patients.</p>
<p>Our designers and programmers build each site from scratch. We learn your goals, your budget and your taste, then assign a designer who stays with your project from the first sketch to launch. We use the latest AI tools to speed up research, drafts and testing, and people review everything before it goes live.</p>

<h2>Why practices choose us</h2>
<ul>
  <li><strong>We specialize in medical marketing.</strong> As a physician owned company, we understand patient treatments and the dynamics of a medical practice.</li>
  <li><strong>We care about our clients.</strong> Public companies such as Aerolase, and other large private companies, trust us to create website and marketing programs for their own clients.</li>
  <li><strong>We show our results.</strong> Our results and phone tracking system lets you see the calls your website produces.</li>
  <li><strong>Design that has been tested.</strong> We use layouts and features that have been shown to generate results, not decoration for its own sake.</li>
</ul>

<h2>Our process</h2>
<ol class="steps">
  <li>Analysis</li>
  <li>Sketch</li>
  <li>Design and development</li>
  <li>Testing</li>
</ol>

<h2>Already have a website?</h2>
<p>We can review your current site for speed, mobile experience and how clearly it guides a patient to contact you, then recommend simple changes that suit your practice and your budget. The best way to judge a website is whether patients can find it and whether it brings in revenue.</p>

<h2>What every site includes</h2>
<ul class="two">
  <li>Mobile-first, fast-loading pages</li>
  <li>Clean structure and structured data for search engines and AI search</li>
  <li>Content management system you can edit</li>
  <li>Online patient forms</li>
  <li>Integrated blog</li>
  <li>Links to your social media profiles</li>
  <li>Bilingual options</li>
  <li>Phone support with our staff</li>
</ul>
"""),
    dict(group=0, slug="medical-spa-website-design", name="Medical spa website design",
         h1="Medical spa website design",
         lead="Websites and marketing for med spas, day spas and aesthetic practices, custom built to match the experience patients get when they walk in.",
         blurb="Sites for med spas and aesthetic practices that look like the experience you offer.",
         img="medspa-reception", alt="Reception area of a modern medical spa",
         anim=("flow", ["Sees you on Instagram", "Visits your site", "Books a consult", "Treatment", "Review and referral"]),
         body="""
<p>Whether you are a plastic surgeon, dermatologist or family practitioner adding aesthetics to your practice, or an established skin care and aesthetics center, our team can create a website and marketing campaign that fits your goals.</p>
<p>The most effective strategy available to aesthetic physicians is a distinctive website that loads fast on any phone, paired with strong search and social media marketing. Our designers, programmers and marketing specialists all work in house. We do not outsource and we do not use templates.</p>

<h2>Website and marketing together</h2>
<p>Your website is your practice online, and the image it shows must match your practice. A professional look is half of the job. The other half is making sure patients can find it.</p>
<p>After learning your goals, we design a strategy around what works now. Search engines change their algorithms constantly, and AI Overviews and AI assistants now answer many patient questions directly, so our staff keeps up with both.</p>

<h2>Every spa website includes</h2>
<ul class="two">
  <li>Mobile-first build with fast pages and structured data</li>
  <li>Physician staff to help write content</li>
  <li>Professional, custom appearance</li>
  <li>Website maintenance and support</li>
  <li>Phone support with our staff</li>
  <li>Bilingual websites</li>
</ul>

<h2>Services for medical spas</h2>
<ul>
  <li>Custom websites that match your practice</li>
  <li>Social media pages and campaigns, including Instagram, TikTok and short-form video</li>
  <li>Online booking for consultations and treatments</li>
  <li>Email marketing with automated newsletters written by our physician staff</li>
  <li>EMR integration</li>
  <li>Patient education resources reviewed by our physician staff</li>
</ul>
"""),
    dict(group=0, slug="landing-pages-funnels", name="Landing pages and funnels", new=True,
         h1="Landing pages and patient funnels",
         lead="One page, one treatment, one action. Landing pages built for a single campaign convert far better than sending ad traffic to your home page.",
         blurb="Single-purpose pages for each treatment and campaign, tested until they convert.",
         img="physician-laptop", alt="Physician reviewing a page on her laptop",
         anim=("build",),
         body="""
<p>When a patient clicks an ad for a specific treatment, they should land on a page about that treatment, with the answer to their question and an easy way to book. That is a landing page.</p>

<h2>What we build</h2>
<ul>
  <li>A page for each treatment, promotion or event</li>
  <li>Offers and forms designed around one clear action</li>
  <li>Before-and-after galleries, FAQs and physician credentials</li>
  <li>Instant follow-up by text and email when a patient submits</li>
  <li>A/B tests of headlines, offers and layouts</li>
  <li>Tracking from the first click to the booked consultation</li>
</ul>
<p>AI tools let us produce and test variations quickly. Our physician advisors review the medical claims on every page.</p>
"""),
    dict(group=0, slug="mobile-apps", name="Mobile apps for iPhone and Android", new=True,
         h1="Mobile apps for your practice",
         lead="Your own app in the App Store and on Google Play, with your name and your brand, so patients carry your practice in their pocket and you run it on the go.",
         blurb="Your own iPhone and Android app, for your patients and for running your practice on the go.",
         img="mobile-app", alt="A physician checking an app on a phone in a clinic hallway",
         anim=("flow", ["Plan the features", "Design your app", "Build for iPhone and Android", "Publish in the stores", "Updates and support"]),
         body="""
<p>Patients spend most of their phone time inside apps, not in a browser. An app with your practice's name on their home screen keeps you one tap away, and a notification from your app gets seen in a way an email often does not.</p>
<p>We design and build the app, publish it in the Apple App Store and on Google Play under your practice's name, and keep it updated. We have done this for Empire Medical Training, whose app is live in both stores.</p>

<h2>What patients can do in your app</h2>
<ul class="two">
  <li>Book and manage appointments</li>
  <li>Get reminders and offers as notifications</li>
  <li>Fill in forms before a visit</li>
  <li>See treatments, prices and before-and-after galleries</li>
  <li>Buy products and gift cards</li>
  <li>Earn and redeem loyalty rewards</li>
  <li>Message your front desk</li>
  <li>Find directions and call in one tap</li>
</ul>

<h2>What you can do on the go</h2>
<ul>
  <li>See today's schedule, new leads and messages from your phone</li>
  <li>Approve content, reviews and replies wherever you are</li>
  <li>Send a notification about an open slot or a promotion in a minute</li>
  <li>Check calls, bookings and campaign results without opening a laptop</li>
</ul>

<h2>How we build it</h2>
<p>One code base produces both the iPhone and the Android app, which keeps the cost and the timeline reasonable and means new features reach both at once. The app connects to your website, your booking system and your CRM, so nothing is entered twice. We handle the developer accounts, the store listings, the review process and every update after launch.</p>

<div class="note"><p>Anything in the app that touches patient information is built with HIPAA requirements in mind, and we work with your compliance contact on the details.</p></div>
"""),
    dict(group=0, slug="medical-e-commerce", name="Medical e-commerce",
         h1="Online medical stores and shopping carts",
         lead="Sell skincare, supplements and other products from your practice website. We set up the store, the payments and the products.",
         blurb="Online stores and shopping carts built into your practice website.",
         img="patient-phone", alt="Woman browsing on her phone at home",
         anim=("flow", ["Product page", "Cart", "Secure payment", "Shipped", "Reorder reminder"]),
         body="""
<p>If you are thinking about starting an online medical store, we can help. Medical e-commerce may seem complicated, but our programmers have years of experience building stores, shopping carts and custom options for physicians.</p>
<p>Our team sets up everything for you: the design of the store, the merchant account and all of your products.</p>

<h2>Custom shopping carts</h2>
<p>We build the shopping cart into your practice website so you can promote your products online. The store is designed for phones first, with fast pages and a short checkout. You choose how you accept payment, and every payment option we set up is secure for your patients.</p>
<ul>
  <li>Store design that matches your website</li>
  <li>Secure card payments and digital wallets</li>
  <li>Product pages with photos and descriptions</li>
  <li>Subscriptions and repeat orders for products patients reorder</li>
  <li>E-commerce hosting and maintenance</li>
</ul>
"""),
    dict(group=0, slug="emr-patient-portals", name="EMR and patient portals",
         h1="EMR integration and patient portals",
         lead="Connect your EMR's patient portal to your website, so patients find forms, appointments and refills in one place.",
         blurb="Your EMR's patient portal, connected to your website.",
         img="front-desk", alt="Front desk coordinator helping a caller",
         anim=("flow", ["Your website", "Patient portal", "Forms and records", "Appointment"]),
         body="""
<p>Your electronic medical record system already holds the tools patients expect to find online. We connect it to your website so they can reach those tools in one tap, from any device.</p>
<p>As part of an overall integration plan, our staff connects your EMR's online patient portal to your medical website. New patients see that booking, forms and records are easy to manage with your practice, and your office spends less time on phone calls and paperwork.</p>

<h2>What a patient portal gives you</h2>
<ul>
  <li>Convenience for patients, on mobile as well as desktop</li>
  <li>Improved record keeping</li>
  <li>Secure delivery of lab results, imaging studies and patient vital information</li>
  <li>Prescription refill requests</li>
  <li>Online patient forms completed before the visit</li>
  <li>Online appointment booking</li>
  <li>A foundation for patient communication and marketing, such as email and text message follow-up</li>
</ul>
<p>To speak with a representative about integrating your EMR or patient portal, call us at <a href="tel:+19543582856">954-358-2856</a>.</p>
"""),
    dict(group=0, slug="online-booking", name="Online booking and intake", new=True,
         h1="Online booking and patient intake",
         lead="Let patients book a visit and fill in their forms from their phone, at any hour, without calling the front desk.",
         blurb="Patients book and complete forms from their phone, any time of day.",
         img="patient-phone", alt="Woman booking an appointment from her phone",
         anim=("flow", ["Finds you at 9 pm", "Picks a time", "Fills in intake", "Gets a reminder", "Arrives ready"]),
         body="""
<p>Many patients decide where to go outside office hours. If the only way to book is a phone call tomorrow morning, some of them will book somewhere else tonight.</p>
<p>We add online booking and digital intake to your website and connect them to the scheduling system you already use, so your staff does not have to copy anything by hand.</p>

<h2>What we set up</h2>
<ul>
  <li>Book-now buttons on your website, Google Business Profile and social pages</li>
  <li>Appointment requests or real-time scheduling, depending on your system</li>
  <li>Digital intake and consent forms patients complete before they arrive</li>
  <li>Automatic confirmations and reminders by text and email</li>
  <li>Telehealth visit links for practices that offer virtual visits</li>
  <li>Tracking, so you know which campaigns produce bookings</li>
</ul>
<p>Forms that collect health information are set up with HIPAA requirements in mind, and we work with your compliance contact on the details.</p>
"""),
    dict(group=0, slug="website-accessibility-compliance", name="Accessibility and compliance", new=True,
         h1="Website accessibility and compliance",
         lead="A medical website has to work for every patient and handle their information carefully. We build and audit for both.",
         blurb="Sites every patient can use, with forms that handle health information carefully.",
         img="physician-laptop", alt="Physician reviewing her practice website on a laptop",
         anim=("flow", ["Audit", "Fix", "Test with assistive tech", "Publish statement", "Monitor"]),
         body="""
<p>Patients use your website with screen readers, with a keyboard, on small phones and with low vision. A site that works for them works better for everyone, and it lowers the risk of an accessibility complaint.</p>

<h2>Accessibility</h2>
<ul>
  <li>Audit of your current site against the WCAG guidelines</li>
  <li>Fixes for contrast, headings, forms, images and keyboard navigation</li>
  <li>Captions for video</li>
  <li>An accessibility statement and a way for patients to report problems</li>
</ul>

<h2>Privacy and patient information</h2>
<ul>
  <li>Contact and intake forms set up with HIPAA requirements in mind</li>
  <li>Review of tracking tags and pixels on pages where patients share health information</li>
  <li>Cookie consent and privacy policy pages</li>
  <li>SSL, backups and security updates</li>
</ul>
<p>We are a marketing agency, not a law firm. We work with your compliance officer or attorney and implement what they require.</p>
"""),
    dict(group=0, slug="website-maintenance", name="Website maintenance",
         h1="Website security and maintenance",
         lead="A designated team keeps your website current, secure and fast, and makes your changes within 24 to 48 hours.",
         blurb="Hosting, security, backups and changes made within 24 to 48 hours.",
         img="analytics-desk", alt="Analyst reviewing website performance charts",
         anim=("flow", ["You send a request", "Changed in 24 to 48 hours", "Backed up", "Security updated", "Monthly report"]),
         body="""
<p>A website that markets your practice well needs accurate information, regular updates and ongoing attention to speed, security and search visibility, both in Google and in AI search.</p>
<p>Our team understands how important this is and assigns people to maintain your website daily.</p>

<h2>What maintenance includes</h2>
<ul class="two">
  <li>Website hosting</li>
  <li>Onsite search engine optimization</li>
  <li>Marketing reports and analytics</li>
  <li>Website modifications</li>
  <li>Educational support</li>
  <li>Checks for broken links, images and pages</li>
  <li>Changes to your website within 24 to 48 hours</li>
  <li>Customer support</li>
  <li>Image updates</li>
  <li>Content additions</li>
  <li>Security updates</li>
  <li>Website backups</li>
  <li>E-commerce hosting</li>
  <li>E-commerce maintenance</li>
</ul>
"""),

    # ------------------------------------------------------------------ Get found
    dict(group=1, slug="search-engine-optimization", name="Search engine optimization",
         h1="Search engine optimization for doctors",
         lead="SEO gets your practice website to appear high in the results when patients search for the procedures you offer.",
         blurb="Ongoing work on content, code and authority so patients find your practice.",
         img="analytics-desk", alt="Analyst looking at search performance charts",
         anim=("serp",),
         body="""
<p>Search engine optimization helps patients find your website and your practice. When patients look for a doctor or a treatment, they turn to Google, map results and, increasingly, AI assistants. Being visible in those places is what brings them to your website.</p>
<p>A well built medical website combines an attractive design with clean, fast code that search engines can read easily. Visibility earned through SEO does not require paying for every click, which can make it more cost effective than advertising over time.</p>
<p>Optimizing a medical website is not a one-time setup. Our staff keeps working on your website on an ongoing basis.</p>

<h2>What is included</h2>
<ul class="two">
  <li>Keyword analysis and strategy</li>
  <li>Website architecture optimization</li>
  <li>Code optimization</li>
  <li>Content strategy and optimization</li>
  <li>Link building</li>
  <li>Infographic creation</li>
</ul>

<h2>Keywords and search intent</h2>
<p>Keywords are the words and questions a patient types or speaks into a search engine or an AI assistant. Our staff builds a list of the terms that matter for your practice and maps each one to the page that answers it best. That work starts with understanding your practice, which we take the time to learn, and a thorough analysis of your competition.</p>

<h2>Technical setup</h2>
<p>Before we begin designing, we set up your website with the code search engines read: title tags, descriptions, image alt text and structured data for every page. We plan for mobile screens first and for fast loading pages, because both affect how patients and search engines experience your website.</p>

<h2>Link building</h2>
<p>A link points to your website from another place. Search engines look at the quality and relevance of the websites that link to you, not the number of links. We use ethical, white hat strategies only.</p>

<h2>Content</h2>
<p>The quality of the information on your website is essential to how it performs in search. Search engines and AI search tools favor content that is accurate, helpful and written for patients. We have physicians on staff who write and review content for your website, your email campaigns and your social media.</p>
"""),
    dict(group=1, slug="local-seo", name="Local SEO",
         h1="Local search engine optimization",
         lead="Most patients choose a practice near them. Local SEO puts you on the map, with listings that are complete and correct.",
         blurb="Google Maps, directory listings and landing pages for the area you serve.",
         img="patient-phone", alt="Woman searching for a nearby doctor on her phone",
         anim=("flow", ["Clean up listings", "Google Business Profile", "Local pages", "Reviews", "Map results"]),
         body="""
<p>Most companies only push your information out to the major data directories. They do not look for the incomplete, duplicate or wrong listings of your practice that are already out there and that hurt your local visibility, both in Google and in the AI assistants that draw on the same data.</p>
<p>We find and fix those first, then build on a clean base.</p>

<h2>What is included</h2>
<ul>
  <li>Listing cleanup and consistent practice information across the major data directories</li>
  <li>Google Business Profile setup and upkeep</li>
  <li>Google Maps placement</li>
  <li>Medical directory listings</li>
  <li>Fast, mobile-first landing pages for each location and service</li>
  <li>Call-to-action buttons that let patients call or book in one tap</li>
  <li>Organic SEO for searches in your area</li>
</ul>
"""),
    dict(group=1, slug="ai-search-optimization", name="AI search optimization", new=True,
         h1="AI search optimization",
         lead="Patients now ask ChatGPT, Google's AI Overviews and other assistants which doctor to see. We work to make your practice part of the answer.",
         blurb="Be the practice AI assistants mention when patients ask who to see.",
         img="ai-assistant", alt="Hand holding a phone with a chat conversation in a clinic waiting room",
         anim=("chat", AI_SEARCH_CHAT),
         body="""
<p>Search has changed. A growing share of patient questions is answered by an AI summary before anyone clicks a link. Those answers are assembled from sources the AI trusts: clear, well structured pages, consistent listings, reviews and mentions on reputable sites.</p>
<p>AI search optimization, sometimes called answer engine optimization or generative engine optimization, is the work of making your practice easy for those systems to understand and safe for them to recommend.</p>

<h2>What we do</h2>
<ul>
  <li>Audit how AI assistants currently describe your practice and your competitors</li>
  <li>Structured data for your physicians, locations, procedures and reviews</li>
  <li>Question-and-answer content written the way patients ask, reviewed by physicians</li>
  <li>Consistent practice information across directories and profiles</li>
  <li>Author pages and credentials that show who stands behind your medical content</li>
  <li>Monitoring of your visibility in AI answers over time</li>
</ul>

<div class="note"><p>No one can guarantee a place in an AI answer, and you should be careful with anyone who does. What we can do is the groundwork these systems reward, on top of the SEO that still brings in most search traffic.</p></div>
"""),
    dict(group=1, slug="pay-per-click", name="Pay-per-click",
         h1="Pay-per-click marketing",
         lead="Paid search is the fastest way to the top of the results. Your ad appears when a patient searches for a service you offer.",
         blurb="Paid search campaigns, managed and measured by calls and bookings.",
         img="analytics-desk", alt="Analyst reviewing campaign charts on two monitors",
         anim=("chart",),
         body="""
<p>Pay-per-click ads appear above the organic search results. When patients search for terms related to your practice, the ads reach them at that moment and bring them to your website.</p>

<h2>How we manage a campaign</h2>
<ul class="two">
  <li>Account organization and structure</li>
  <li>Budget assignment</li>
  <li>Ad relevance and quality</li>
  <li>Coverage of the searches patients make</li>
  <li>Fast, mobile-first landing pages for each campaign</li>
  <li>Call and booking tracking</li>
</ul>

<h2>The result that counts</h2>
<p>No matter how much traffic your website gets, the end result should be a phone call or a booking from a patient interested in your services. Our results and phone tracking system lets you see exactly that.</p>
"""),
    dict(group=1, slug="search-engine-marketing", name="Search and social advertising",
         h1="Search engine marketing and social advertising",
         lead="In crowded markets, SEO alone may not be enough. Paid advertising on Google, Instagram, Facebook and TikTok fills the gap.",
         blurb="Advanced paid campaigns on Google, Meta and TikTok for competitive markets.",
         img="studio", alt="Marketing team working at their desks",
         anim=("chart",),
         body="""
<p>Sometimes a sound SEO plan needs a paid advertising strategy beside it. We can set it up and show you how to create ads, choose keywords and bidding, and maintain your own account, or we can manage it for you.</p>

<h2>The benefits</h2>
<ul class="two">
  <li>Prominent placement that brings more visibility and more traffic</li>
  <li>Cost control, with a budget you set</li>
  <li>Highly targeted traffic</li>
  <li>Ongoing marketing to potential patients</li>
  <li>Return on investment you can measure</li>
</ul>

<h2>Google Ads</h2>
<p>With paid search, your practice can appear at the top of the results page as soon as the campaign starts. When a patient searches a phrase such as “Botox Fort Lauderdale” on a phone, your ad is eligible to show right away, with a link to call or book. Each click uses part of your budget, which is paid to Google, so the setup matters. Think of a broker managing a portfolio: campaign management works the same way.</p>

<h2>Social advertising</h2>
<p>Paid campaigns on Instagram, Facebook and TikTok can also be very effective and often cost less per click than search. We build the audiences, produce the creative, including short-form video, and follow each platform's rules for health and aesthetic advertising.</p>

<h2>Advanced campaigns</h2>
<ul>
  <li>Retargeting for visitors who did not book</li>
  <li>Lookalike audiences built from your best patients, without sharing health information</li>
  <li>Seasonal promotions and event campaigns</li>
  <li>AI-assisted creative testing across many versions of an ad, with human review</li>
</ul>
"""),
    dict(group=1, slug="reputation-management", name="Reviews and reputation", new=True,
         h1="Reviews and reputation management",
         lead="Patients read reviews before they call. We help you collect more of them, answer them well and keep your profiles accurate.",
         blurb="More patient reviews, thoughtful replies and accurate profiles everywhere.",
         img="medspa-reception", alt="Receptionist greeting a patient",
         anim=("stars",),
         body="""
<p>Your star rating is often the first thing a new patient sees, and reviews are one of the signals search engines and AI assistants use when they decide which practice to show.</p>

<h2>What we do</h2>
<ul>
  <li>Review requests sent by text or email after a visit</li>
  <li>Monitoring of Google, Healthgrades, Yelp and other sites in one place</li>
  <li>Drafted replies for your approval, written so they never reveal patient information</li>
  <li>Google Business Profile management: photos, services, hours and posts</li>
  <li>Alerts when a new review needs attention</li>
  <li>Reviews displayed on your website</li>
</ul>
<p>We ask every patient the same way and do not filter who gets a request. That keeps your reviews honest and within the rules of the review sites.</p>
"""),

    # ------------------------------------------------------------------ Stay in touch
    dict(group=2, slug="ai-chat-messaging", name="AI agents: chat, text and voice", new=True,
         h1="AI agents for your practice",
         lead="Assistants on your website, your text line and your phone that answer patients at any hour, take booking requests and hand off to your staff.",
         blurb="AI agents that answer patients by chat, text and phone around the clock.",
         img="ai-assistant", alt="Phone showing a chat conversation in a clinic waiting room",
         anim=("chat", AGENT_CHAT),
         body="""
<p>A large share of calls to a practice arrive when nobody can pick up: at lunch, after hours, or while the front desk is with a patient. Every one of those is a patient who may call the next practice on the list.</p>
<p>We set up AI agents trained on your services, hours, locations and policies, so patients get an answer right away.</p>

<h2>What we set up</h2>
<ul>
  <li><strong>Website chat</strong> that answers questions about your services and takes booking requests</li>
  <li><strong>Text-back for missed calls</strong>, so a caller hears from you in seconds</li>
  <li><strong>Voice agent</strong> that answers the phone after hours, in English and Spanish</li>
  <li><strong>Reminders and follow-ups</strong> by text</li>
  <li><strong>Hand-off to your staff</strong>, with the conversation attached, whenever a person is needed</li>
  <li><strong>Answers limited to what you approve</strong>, and reports on what patients ask most</li>
</ul>

<h2>Agents for your team, too</h2>
<ul>
  <li>Call summaries, so your manager knows what every caller wanted</li>
  <li>Draft replies to reviews, emails and social messages for your approval</li>
  <li>A private assistant trained on your own policies and price list for new staff</li>
</ul>

<div class="note"><p>The agents do not give medical advice or diagnose. Clinical questions go to your team, and the setup is done with HIPAA requirements in mind.</p></div>
"""),
    dict(group=2, slug="social-media", name="Social media management",
         h1="Social media management",
         lead="A dedicated team creates and maintains your social media, so your practice stays in front of patients between visits.",
         blurb="Strategy, weekly posts, ads and community management for your practice.",
         img="social-reel", alt="Creator filming a doctor with a phone on a gimbal",
         anim=("flow", ["Plan", "Create", "Publish", "Engage", "Report"]),
         body="""
<p>Whatever your specialty, patients turn to social media for health information and to get a sense of a practice before they book. An effective physician marketing program includes social media, and you do not need to use it personally for it to work for your practice.</p>
<p>Our team of social media professionals focuses entirely on creating and maintaining your channels, including Instagram, TikTok and Facebook where they fit your audience. We develop content for your practice, with AI-assisted drafting and human and physician review, and build a connection with your audience.</p>

<h2>What each project includes</h2>
<ul class="two">
  <li>Strategy development</li>
  <li>Competitive and marketplace research</li>
  <li>Brand expansion</li>
  <li>Ad management</li>
  <li>Community management</li>
  <li>Events and promotions</li>
  <li>Content creation, including short-form video</li>
  <li>Conversion optimization</li>
</ul>

<h2>Benefits for your practice</h2>
<ul>
  <li><strong>Brand awareness.</strong> Photos and short-form video build your practice's image.</li>
  <li><strong>Feedback.</strong> Hear from current and potential patients in comments and messages, and improve your service.</li>
  <li><strong>Loyalty.</strong> Regular interaction builds confidence in your practice.</li>
  <li><strong>A base of potential patients.</strong> Followers can become patients over time.</li>
</ul>

<h2>Work process</h2>
<ol class="steps">
  <li>Research of the platforms your patients use</li>
  <li>Profile setup</li>
  <li>Launch</li>
  <li>Ongoing weekly posts</li>
</ol>
"""),
    dict(group=2, slug="short-form-video", name="Short-form video", new=True,
         h1="Short-form video and reels",
         lead="Short vertical videos are how many patients first meet a doctor. We plan, film, edit and publish them for you.",
         blurb="Reels and short videos of your physicians, planned, filmed and edited for you.",
         img="social-reel", alt="A doctor being filmed for a short video in a clinic hallway",
         anim=("flow", ["Plan the topics", "Film in one session", "Edit and caption", "Publish everywhere", "Measure"]),
         body="""
<p>A thirty second video of you answering a common question does more to build trust than a page of text. It also feeds Instagram, TikTok, YouTube Shorts and Facebook at the same time.</p>

<h2>What we do</h2>
<ul>
  <li>A monthly content plan built around the questions your patients ask</li>
  <li>Filming at your office in a single session that covers weeks of posts</li>
  <li>Editing, captions and cover images</li>
  <li>AI-assisted editing to produce more formats from the same footage</li>
  <li>Publishing on each network, with reporting on what performed</li>
  <li>Before-and-after and procedure content handled with patient consent</li>
</ul>
<p>Our physician advisory board reviews medical claims before anything is published.</p>
"""),
    dict(group=2, slug="e-mail-marketing", name="E-mail marketing management",
         h1="E-mail marketing management",
         lead="Stay in contact with your patients with newsletters written by physicians and sent on the schedule you choose.",
         blurb="Campaigns, newsletters and automations, written by physicians and managed for you.",
         img="content-physician", alt="A physician and a writer reviewing pages together",
         anim=("flow", ["Capture the email", "Send the free report", "Regular newsletter", "Timely offer", "Booking"]),
         body="""
<p>Email remains one of the most direct ways to stay in contact with your patients, and it is a channel your practice owns. We keep your patients' names and email addresses in a patient CRM, organized so that each message goes to the people it is relevant to.</p>

<h2>Managed for you</h2>
<ul>
  <li>List setup, clean-up and segmentation by treatment and interest</li>
  <li>Templates designed to match your brand and read well on a phone</li>
  <li>A monthly calendar of newsletters, promotions and event invitations</li>
  <li>Automations: welcome series, post-visit follow-up, birthdays and win-back</li>
  <li>Deliverability set up correctly, so your emails reach the inbox</li>
  <li>Reports on opens, clicks and the bookings each campaign produced</li>
</ul>
<p>This is the same email operation we run for Empire Medical Training, sized for a practice.</p>

<h2>Physician-written emails</h2>
<p>Our physicians write and review informative newsletters that are emailed to your list. You set the interval and can review or change the content before it goes out. These emails are not sales pitches. They are helpful information your patients will want to read, and that ongoing contact helps them remember who you are, what services you offer and how to reach you when they are ready for a procedure.</p>

<h2>Email sign-up and capture</h2>
<p>Our email capture system adds a visitor to your list when they request information from you, such as a short guide to healthy skin. The guides are written by our physicians and built into your website. Once the visitor enters an email address and agrees to hear from you, the guide is sent automatically, and you can keep in touch with newsletters they will be happy to receive.</p>
"""),
    dict(group=2, slug="sms-marketing", name="SMS campaign management", new=True,
         h1="SMS campaign management",
         lead="Text messages get read within minutes. We plan, write, send and track your text campaigns, and keep them within the carrier and consent rules.",
         blurb="Text promotions, reminders and two-way replies, planned and sent for you.",
         img="patient-phone", alt="Woman reading a text message on her phone",
         anim=("chat", [("us", "Hi Ana, it has been three months since your last treatment. Want us to hold a spot this week?"), ("them", "Yes, Friday morning?"), ("us", "Friday at 10:00 is yours. See you then.")]),
         body="""
<p>Email builds the relationship. Text gets the quick yes. A short message about an open appointment or a seasonal offer can fill a slow week in an afternoon.</p>

<h2>What we manage</h2>
<ul>
  <li>Registration of your business number with the carriers, so messages are delivered</li>
  <li>Opt-in forms, keywords and consent records</li>
  <li>Promotions, event invitations and last-minute openings</li>
  <li>Reminders for repeat treatments and follow-ups after a visit</li>
  <li>Two-way conversations routed to your front desk or to an AI agent</li>
  <li>Reports on replies, bookings and opt-outs</li>
</ul>

<div class="note"><p>We only text patients who agreed to receive messages, every message includes a way to opt out, and we keep health details out of the text itself.</p></div>
"""),
    dict(group=2, slug="physician-content-marketing", name="Physician content marketing",
         h1="Physician content marketing",
         lead="Website content, newsletters, articles and blogs written by physicians and internet writers. We do all the work.",
         blurb="Website copy, articles and newsletters written and reviewed by physicians.",
         img="content-physician", alt="A physician reviewing written content with a writer",
         anim=("flow", ["Research", "Draft with AI", "Physician review", "Publish", "Refresh"]),
         body="""
<p>Clear, accurate content on your website holds readers' attention and helps patients find your practice through search engines and AI assistants.</p>
<p>Our writers are physicians and digital marketing staff. A physician writes or reviews the medical content, then our digital staff makes sure it is clearly structured and easy for search engines and AI search tools to understand. Writing for the web is different from writing for journals or print, and with AI assistants now quoting websites directly, accuracy matters more than ever. We use AI tools to research and draft faster, and a physician checks the result.</p>

<h2>Website content</h2>
<p>Our physicians and writers prepare custom content along with the information you provide. As part of ongoing maintenance, we add new content regularly so the information on your site stays current and useful for readers.</p>

<h2>Email marketing and newsletters</h2>
<p>Your website is connected to a patient CRM that collects patient email addresses. Our physicians write articles and newsletters that we email to your patients. Patients are always at different stages of a decision, so regular contact means they know who you are, what you offer and how to find you when they are ready.</p>

<h2>Articles, press releases and blogs</h2>
<p>Publishing helpful, physician-reviewed articles, press releases and blog posts is an important part of being found in search and in AI answers. It is time consuming work that some agencies leave to the physician or the office staff. We do all the work, and we do not ask you to help write.</p>
"""),
    dict(group=2, slug="video-testimonials", name="Video testimonials",
         h1="Medical video testimonials",
         lead="Our videographers come to your office, interview your patients and deliver a finished video for your website.",
         blurb="On-site filming of patient testimonials, edited into a finished video.",
         img="video-shoot", alt="A video crew filming a patient testimonial in a clinic",
         anim=("flow", ["Plan", "Film at your office", "Interview patients", "Edit", "Deliver"]),
         body="""
<p>Video testimonials are one of the most effective ways to make a strong first impression on new visitors. They show what sets your practice apart, in your patients' own words.</p>
<p>Watching real patients talk about their experience creates comfort and trust in a way written reviews cannot. A prospective patient who has heard a satisfied patient describe their visit has a clearer reason to contact you.</p>

<h2>What the production package includes</h2>
<ul>
  <li><strong>On-site production.</strong> Our videographers travel to your office and spend half a day filming patient testimonials.</li>
  <li><strong>Patient interviewing and preparation.</strong> Our staff are experienced interviewers. They are friendly and make the experience comfortable and fun for your volunteers.</li>
  <li><strong>Post production.</strong> Our editors turn the footage of your office and patients into the finished video.</li>
  <li><strong>Final video.</strong> A professional video with authentic, believable testimonials. The video files and final product are yours to keep and reuse on your website, your Google Business Profile and your social channels.</li>
  <li><strong>One all-inclusive fee.</strong> No additional charges. Ask us for current package pricing.</li>
</ul>

<h2>What video does for your practice</h2>
<ul>
  <li>Creates trust and credibility with website visitors</li>
  <li>Makes your medical or aesthetics website stand out</li>
  <li>Adds emotion and personality to your practice</li>
  <li>Supports your visibility in search and AI search with original, first-hand content</li>
</ul>
"""),
    dict(group=2, slug="patient-crm-automation", name="Lead management and CRM", new=True,
         h1="Lead management and patient CRM",
         lead="Every inquiry captured, answered in minutes and followed until it becomes a booked patient. Past patients brought back automatically.",
         blurb="Every lead captured, answered fast and followed until it books.",
         img="front-desk", alt="Front desk coordinator on a headset",
         anim=("flow", ["New inquiry", "Instant reply", "Follow-up", "Consult booked", "Back in three months"]),
         body="""
<p>Most practices spend to attract an inquiry and then lose it because nobody followed up in time. A CRM keeps every lead and patient in one place and makes the follow-up happen on its own.</p>

<h2>Lead management</h2>
<ul>
  <li>Every form, call, text, chat and social message lands in one place</li>
  <li>Each lead is tagged with the campaign that produced it</li>
  <li>Scoring and routing, so your staff calls the hottest leads first</li>
  <li>We can manage the first response for you, by AI agent or by our team</li>
  <li>A weekly report: leads in, contacted, booked and lost, with the reasons</li>
</ul>
<p>We manage leads this way every day for Empire Medical Training, and we bring the same system to your practice.</p>

<h2>What we set up</h2>
<ul>
  <li>One inbox for web forms, calls, texts and chat</li>
  <li>Instant replies to new inquiries, then a sequence of follow-ups</li>
  <li>Reminders for patients who are due for a repeat treatment</li>
  <li>Reactivation campaigns for patients you have not seen in a while</li>
  <li>Birthday, promotion and event messages</li>
  <li>A pipeline view: inquiries, consultations booked, treatments done</li>
</ul>
<p>We connect the CRM to your website, your ads and your call tracking, so you can see which marketing produces patients and not just clicks.</p>
"""),

    # ------------------------------------------------------------------ Brand and growth
    dict(group=3, slug="new-service-launch", name="New service launch", new=True,
         h1="Launch a new service in your practice",
         lead="You trained in a new procedure. Now patients need to know you offer it. We take a new service from certificate to first bookings.",
         blurb="From your training certificate to your first bookings for a new procedure.",
         img="aesthetic-consult", alt="A physician consulting with a patient in a treatment room",
         anim=("flow", ["Train at Empire", "Service page and offer", "Tell your patients", "Ads and social", "First bookings"]),
         body="""
<p>Many of our clients come to us right after a course at Empire Medical Training. They have a new skill, such as aesthetics, weight loss, hormone therapy, regenerative medicine or pain management, and a practice whose patients do not know about it yet.</p>
<p>Because we are Empire's strategic marketing partner, we know these procedures, the questions patients ask about them and what it takes to fill the first month of appointments.</p>

<h2>What a launch includes</h2>
<ul>
  <li>A service page and a landing page for the new procedure, with physician-reviewed content</li>
  <li>An introductory offer and the booking form to go with it</li>
  <li>Announcement emails and texts to your current patients, who are your fastest first bookings</li>
  <li>Google and social campaigns aimed at your area</li>
  <li>Short videos of you explaining the treatment</li>
  <li>In-office materials: brochures, posters and a front desk script</li>
  <li>Consent forms and pre and post treatment instructions</li>
  <li>Tracking, so you see the return on the training you paid for</li>
</ul>
"""),
    dict(group=3, slug="marketing-strategy", name="Marketing strategy", new=True,
         h1="Marketing strategy and consulting",
         lead="A marketing plan for your practice, built by people who know medicine and business, with a review every month.",
         blurb="A plan and a monthly review with physicians, MBAs and marketers.",
         img="hero-team", alt="A team and a physician advisor reviewing plans at a table",
         anim=("flow", ["Audit", "Plan", "90-day roadmap", "Monthly review"]),
         body="""
<p>Our MBAs take the time to study your specialty and your competitors in order to build a marketing plan that is cost effective and aimed at results. Our physician advisory board adds what only physicians know about how patients choose.</p>

<h2>What you get</h2>
<ul>
  <li>An audit of your website, rankings, ads, reviews and competitors</li>
  <li>A plan that sets priorities and a budget for each channel</li>
  <li>A 90-day roadmap with clear owners and dates</li>
  <li>A monthly review of results and what to change</li>
  <li>Consultation with our physicians, business and marketing staff</li>
</ul>
<p>Whether you are new to the business of medicine or looking to reach the next level, we have helped hundreds of physicians one on one.</p>
"""),
    dict(group=3, slug="medical-graphic-design", name="Branding and graphic design",
         h1="Medical branding and graphic design",
         lead="Logos, brochures, postcards and print materials that give your practice one consistent, professional image.",
         blurb="Logos, brochures, postcards and stationery with one consistent look.",
         img="print-flatlay", alt="Brochures, business cards and a stethoscope on a desk",
         anim=("flow", ["Brief", "Concepts", "Revisions", "Final files", "Print"]),
         body="""
<p>Our graphic design team has the creativity and the experience to deliver work that stays within your budget and exceeds your expectations. Professionally designed brochures and print materials get your patients' attention and present a consistent image everywhere they see your practice.</p>

<h2>Logo and brand identity</h2>
<p>Our designers create an original logo that fits your practice's theme and overall look, along with the colors, type and templates that keep everything you publish looking like you.</p>

<h2>Medical practice brochures</h2>
<p>Patients expect clear information about your credentials, your practice and your services, and a practice brochure remains an essential marketing tool. Our staff writes the content about your background and services, then our design team creates a custom brochure with your logo and practice details.</p>

<h2>Patient information brochures</h2>
<p>These brochures explain an individual service your patient may be interested in. Our physician staff can write this material for you.</p>

<h2>Patient referral brochures</h2>
<p>Referrals are an important part of promoting your practice. We create customized referral brochures for your staff to give to patients, who pass them to friends and family. They detail your credentials, your services and any special promotions.</p>

<h2>Services postcards</h2>
<p>An attractive 6×9 postcard listing your services, practice information, address and phone number, along with any special promotions. It is larger than a business card and easy to keep as a quick reference.</p>

<h2>More print and display work</h2>
<ul class="two">
  <li>Posters for indoor and outdoor advertising</li>
  <li>Table top displays</li>
  <li>Seminar displays</li>
  <li>Invitations</li>
  <li>Stationery and business cards</li>
  <li>Graphics for social media and ads</li>
</ul>
"""),
    dict(group=3, slug="printing", name="Printing and fulfillment", new=True,
         h1="Printing and fulfillment",
         lead="We design it, print it and ship it to your office. The same print partner that produces Empire Medical Training's materials prints yours.",
         blurb="Brochures, cards, signs and more, printed and shipped to your office.",
         img="print-flatlay", alt="Printed brochures and business cards laid out on a desk",
         anim=("flow", ["Design", "Proof", "Print", "Shipped to your office"]),
         body="""
<p>Print still works in a medical office. A brochure goes home with the patient, a poster in the exam room starts a conversation and a referral card travels to a friend.</p>
<p>You approve a proof, and the finished pieces arrive at your door. One team handles the design and the printing, so colors and logos match your website.</p>

<h2>What we print</h2>
<ul class="two">
  <li>Practice and procedure brochures</li>
  <li>Business cards and appointment cards</li>
  <li>Referral cards and rack cards</li>
  <li>Postcards and direct mail</li>
  <li>Posters and window graphics</li>
  <li>Banners and event displays</li>
  <li>Letterhead, envelopes and folders</li>
  <li>Before and after care sheets</li>
  <li>Gift cards and loyalty cards</li>
  <li>Menus of services and price lists</li>
</ul>
<p>Need direct mail? We can print, address and mail a campaign to the neighborhoods around your practice.</p>
"""),
    dict(group=3, slug="medical-practice-kit", name="Medical practice kit",
         h1="The medical practice marketing kit",
         lead="Our most complete program: a custom website, email capture, print materials, staff training and consultation with physicians and business staff.",
         blurb="Our full program: website, print, staff training and consultation.",
         img="aesthetic-consult", alt="A physician consulting with a patient in a treatment room",
         anim=("flow", ["Custom website", "Print kit", "Staff training", "Compliance forms", "Consultation"]),
         body="""
<p>The Medical Practice Marketing Kit works as your entire marketing program. We create a custom website built for search visibility, so patients find you when they look for a service you offer, whether they use Google or an AI assistant. Many websites look attractive but are slow or poorly structured, which makes them hard to find.</p>
<p>The websites we develop are custom, not templates. Alongside designers, programmers and SEO staff, we keep videographers on staff, because video is one of the most effective ways to turn visitors into patients.</p>
<p>We develop websites for physicians and dentists of many specialties: aesthetics, plastic surgery, dentistry, gynecology, chiropractic, cosmetic dentistry, cardiology, pain management and others.</p>

<h2>What the website includes</h2>
<ul class="two">
  <li>Email capture with a patient CRM</li>
  <li>Physician-written patient guides</li>
  <li>Online patient forms</li>
  <li>Mobile-first, fast pages</li>
  <li>Integrated blog</li>
  <li>Social media integration, including Instagram and TikTok</li>
  <li>Content management system</li>
  <li>Room to expand as technology changes</li>
</ul>

<h2>Front office training</h2>
<p>After the website and marketing are working, the next step is to be ready for new patient calls. We developed an employee sales manual, Front Office Fundamentals, that helps your staff become outstanding sales consultants and customer service personnel. Your front office may be one of your best assets.</p>

<h2>Consent forms, treatment forms and compliance</h2>
<p>The kit includes consent forms for the procedures you perform, physician procedure notes, diagrams and pre and post treatment instructions. This documentation is often overlooked or incomplete, and it is an important part of maintaining proper compliance.</p>

<h2>Physician and business consultation</h2>
<p>The kit includes ongoing support and consultation with our staff of physicians, business and marketing personnel who are experienced in developing successful practices.</p>

<h2>Print materials for your office</h2>
<ul>
  <li><strong>Practice brochure.</strong> Your most important brochure, detailing your background and services.</li>
  <li><strong>Patient information brochures.</strong> More complete information about each procedure.</li>
  <li><strong>Patient referral brochures.</strong> For patients to share with friends and family.</li>
  <li><strong>Services postcard.</strong> A 6×9 card with your services, contact details and promotions.</li>
  <li><strong>Business cards.</strong> Matched to the rest of your print portfolio.</li>
</ul>
"""),
    dict(group=3, slug="analytics-call-tracking", name="Analytics and call tracking", new=True,
         h1="Analytics and call tracking",
         lead="See which campaigns make the phone ring. One dashboard for calls, forms, bookings and what each of them cost.",
         blurb="One dashboard showing which marketing produces calls and bookings.",
         img="analytics-desk", alt="Dashboards with charts and a map on two monitors",
         anim=("chart",),
         body="""
<p>No matter how much traffic your website gets, the end result should be a call or a booking from a patient. Since we started, we have tracked results that way, with our own results and phone tracking system.</p>

<h2>What we measure</h2>
<ul>
  <li>Calls from each campaign, with a tracking number for every source</li>
  <li>Form submissions, chat conversations and online bookings</li>
  <li>Search rankings and visibility in AI answers</li>
  <li>Cost per inquiry for each channel</li>
  <li>Website traffic and the pages patients read before contacting you</li>
</ul>

<h2>What you receive</h2>
<ul>
  <li>A live dashboard you can open at any time</li>
  <li>A monthly report in plain language</li>
  <li>AI-assisted summaries of call recordings, so you learn what patients ask for</li>
  <li>A review call with our team to decide what to change next</li>
</ul>
<p>Analytics on medical websites needs care. We configure tracking so that health information patients share with you is not passed to advertising platforms.</p>
"""),
]

TESTIMONIALS = [
    dict(name="Dr. Peter Khamvongsa", role="OB-GYN, Miami, Florida", img="Khamvongsa.png",
         quote="I’ve been using Rx Medical for several years now. I started attending their courses, and from there I expanded into using their web services and marketing. They have been very helpful in creating a website that is working for me, adding different services, expanding it, and using it to attract patients in my field. I’ve been very happy with them and I highly recommend them."),
    dict(name="Dr. Irina Vinarski", role="MD, Pittsburgh, Pennsylvania", img="vinarski.png",
         quote="Rx Medical Web has done my website, and we’ve been advertising weight loss, hair removal and lasers. I’m very happy with the product, and very happy with the advertisement. It attracted a lot of patients. We have been doing a lot of marketing through Facebook and email, which Rx Medical has been helping us with."),
    dict(name="Dr. Santillanes", role="MD", img="Michael.png",
         quote="We were able to do a website with Rx Medical Web and our website has been spectacular. We have gotten great reviews and we are very happy with the packages we received."),
    dict(name="Dr. Anup Aggwarl", role="MD", img="anup-aggwarl.png",
         quote="Rx Medical Web gave us huge improvements and results. Our office has been very busy since then."),
    dict(name="Dr. Bocian", role="DPM, GenesisPlus", img="bocian.png",
         quote="Rx Medical Web guided me through what seemed to be a complicated and overwhelming process."),
    dict(name="Ashli Holland", role="Gemini Medical Spa", img="Ashli.png",
         quote="Our relationship with Rx Medical Web has been fabulous."),
]

WORK = [
    dict(name="Empire Medical Training", url="https://www.empiremedicaltraining.com/", img="portfolio-emt-700x525.png", shot="work-emt",
         note="The main website of our strategic partner: continuing medical education for physicians, with hundreds of course pages and online registration.",
         did=["Website", "SEO", "E-mail and SMS campaigns", "Lead management", "Online registration"]),
    dict(name="Empire Member Portal", url="https://portal3.empiremedicaltraining.com/", img="portfolio-emt-700x525.png", shot="work-portal",
         note="The portal where Empire's members sign in with a one-time code to reach their courses, CME certificates and account.",
         did=["Web portal", "Passwordless sign-in", "Online payments", "CME certificates"]),
    dict(name="Empire Medical Training app", url="https://apps.apple.com/us/app/empire-medical-training-portal/id6786016946", img="portfolio-emt-700x525.png", shot="work-app",
         note="The member app for iPhone and Android: upcoming courses, certificates and the membership card, in the member's pocket.",
         did=["iPhone app", "Android app", "Course access", "Push notifications"]),
    dict(name="Empire On-Demand", url="https://www.empireondemand.com/", img="portfolio-eod-700x525.png", shot="work-eod",
         note="Empire's online education platform, with its own store, memberships and video library.",
         did=["Website", "Online store", "SEO", "Video platform"]),
    dict(name="American Academy of Procedural Medicine", url="https://www.aaopm.com/", img="portfolio-aaopm-700x525.png", shot="work-aaopm",
         note="CME training in aesthetics, pain management and functional medicine.",
         did=["Website", "SEO", "E-mail campaigns"]),
    dict(name="Empire Verified", url="https://empireverified.com/", img="portfolio-emt-700x525.png", shot="work-verified",
         note="A directory where patients find Empire-trained providers, compare treatments and contact the practice directly.",
         did=["Website", "Provider directory", "Patient reviews"]),
    dict(name="Find an Empire-Trained Provider", url="https://www.empiremedicaltraining.com/find-a-doctor/", img="portfolio-emt-700x525.png", shot="work-findadoctor",
         note="A map search that connects patients with the physicians Empire has trained.",
         did=["Provider locator", "Map search"]),
]

ABOUT_BODY = """
<p>Rx Medical Web is a family owned marketing agency dedicated to one thing: the online presence and marketing of medical practices. Since 2008 we have developed marketing and practice building strategies for more than 400 physicians and dentists of all specialties.</p>
<p>Our staff includes website designers and programmers, search engine optimization specialists, physicians and business personnel. All of our people work on site in Fort Lauderdale. We do not outsource.</p>
<p>Part of our success comes from understanding our clients. We understand medical marketing and the dynamics of a medical practice. In addition to our internet staff, we maintain a physician advisory board of specialists who help create and market our clients' websites. Our physician staff writes and reviews website content and marketing emails, and is available for support and consultation.</p>

<h2>What we do for you</h2>
<ul>
  <li>Make your website sell better</li>
  <li>Create and improve the marketing potential of your products and services</li>
  <li>Give you access to current technology, and the knowledge and experience to build a successful practice online</li>
  <li>Show you clear, measurable results and regular work on the growth of your practice</li>
</ul>

"""

WHY_BODY = """
<h2>Experts in medical marketing</h2>
<p>Medical marketing is all we do. We know how patients choose a physician, what they ask before a procedure and what a practice is allowed to say. That knowledge comes from working with physicians and dentists every day since 2008, with a physician advisory board beside our marketers.</p>
<p>A general agency has to learn your field at your expense. We already speak it, from aesthetics and pain management to dentistry and primary care, so your marketing is accurate from the first draft and gets to work sooner.</p>

<h2>Our pricing</h2>
<p>Our pricing is reasonable and in most cases more cost effective because of how efficiently we work. Be careful with agencies whose prices are unbelievably low and whose promises are unrealistic. The wrong choice costs more than money, because it cannot give back the time you lost. When you choose an agency, compare quality, staff and experience in medicine, and review their portfolio.</p>

<h2>How we measure results</h2>
<p>No matter how much traffic your website gets, the end result should always be a patient contacting your practice about your services, most often by phone. Our results and call tracking system lets you see that for yourself.</p>

<h2>Our team</h2>
<ul>
  <li><strong>Family owned.</strong> We are a family owned business, dedicated to the best results and service for our clients.</li>
  <li><strong>In house.</strong> We are a medium sized firm in Fort Lauderdale, Florida. All of our work is performed in house.</li>
  <li><strong>The digital team.</strong> Web designers, developers, graphic designers, videographers, and digital marketing and search specialists.</li>
  <li><strong>The business team.</strong> MBAs and marketing experts, plus a physician and legal advisory board for our medical websites.</li>
  <li><strong>AI at work.</strong> We use the latest AI tools to research, draft, test and report faster, with people reviewing the result.</li>
</ul>

<h2>What sets us apart</h2>
<p>We genuinely care about our clients and want you to be successful. We do more than build websites and campaigns. We focus on results you can notice in your practice.</p>
<p>Our MBAs take the time to study your specialty and your competitors, so your marketing plan is cost effective and aimed at results. Our physician advisory board is made up of physicians from different specialties who provide material for your website and marketing that is helpful to patients and medically accurate.</p>
<p>We give our clients personal service and attention, and we take direction only from you.</p>
"""

ARTICLES = [
    dict(path="dental-website-design", title="Dental websites are a must to stay in the game",
         date="October 23, 2016", img="dental-office", alt="A dentist talking with a patient in a modern operatory",
         lead="Being the best dentist does not mean you can ignore current marketing. Patients now search for practices online.",
         body="""
<p>Patients compare dentists online before they call. They read reviews, look at your Google Business Profile, ask AI assistants for recommendations and visit your website on their phones. A clear, attractive and informative website, supported by an active social media presence, gives them what they need to know about you, your practice and the technology you provide.</p>
<p>Dental internet marketing is the most cost-effective way to grow your practice and increase revenue, and working with a professional dental marketing company makes sure your site is as effective as it can be. It is also the easiest way to attract new patients and build loyalty with your current ones.</p>
<p>Rx Medical Web has a complete team of designers, programmers and internet specialists who work closely with dentists to make sure content is medically accurate. Each site is custom tailored for the practice, not a prefabricated template.</p>

<h2>Dental website features</h2>
<ul>
  <li>Exceptional dental website design that is mobile-first, fast and accessible</li>
  <li>Online dental education videos</li>
  <li>Helpful, dentist-reviewed content and structured data for visibility in search engines and AI search</li>
  <li>Simple navigation</li>
  <li>Optional video testimonials</li>
</ul>

<h2>Dental website and internet services</h2>
<ul>
  <li>Custom dental marketing website to match your practice</li>
  <li>Social media pages and marketing, including Instagram, TikTok and short-form video</li>
  <li>Email marketing campaigns and automation</li>
  <li>Full EMR integration</li>
  <li>Patient education resources</li>
</ul>
<p>For more information, call us today at <a href="tel:+19543582856">(954) 358-2856</a>.</p>
"""),
    dict(path="medical-internet-marketing", title="If you build it, will they come? The need for medical internet marketing",
         date="October 25, 2016", img="physician-laptop", alt="A physician working on a laptop",
         lead="Is your medical website one in a million, or one of a million? Creating a website does not mean anyone is looking at it.",
         body="""
<p>A medical website without a marketing plan behind it is rarely seen. Patients find practices through search results, maps, reviews and, increasingly, AI assistants, and a site that does not show up in those places sits unused.</p>
<p>Patients compare practices on their phones, often in a few minutes, before they ever call. A site that loads slowly, is hard to read on a small screen or does not answer their questions gets passed over. A clear design and a strategy built around how patients actually choose a practitioner give your practice a fair chance of being considered.</p>

<h2>Internet marketing options for medical practitioners</h2>
<ul class="two">
  <li>Search engine optimization</li>
  <li>Pay per click advertising</li>
  <li>Social media marketing</li>
  <li>Newsletters and email marketing</li>
  <li>Local advertising</li>
  <li>Medical directory placement</li>
  <li>Google Business Profile and online listings</li>
  <li>Display advertising</li>
  <li>Press releases</li>
  <li>Custom brochures for direct mail</li>
</ul>
<p>Rx Medical Web is a Fort Lauderdale, Florida based company that works only on medical websites. Our team works with practitioners to implement marketing plans designed for each practice. Whether you want a new website or want to improve an existing one, we will create a strategy to fit your needs.</p>

<h2>What medical internet marketing is designed to do</h2>
<ul>
  <li>Make your practice easier to find in Google search, maps and AI search results</li>
  <li>Bring more of the right visitors to your website</li>
  <li>Turn those visits into new patient inquiries and appointments</li>
  <li>Reach patients directly on the social platforms they use</li>
  <li>Keep your directory and listing information accurate and consistent wherever patients look</li>
</ul>
<p>Results depend on your specialty, your market and your starting point, so we set goals with each practice individually.</p>
<p>Feel free to contact us at <a href="tel:+19543582856">954-358-2856</a>.</p>
"""),
]
