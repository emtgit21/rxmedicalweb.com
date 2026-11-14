// Rx Medical Web site assistant.
// It answers basic questions about the services using only text that is already on this
// website (services, explanations and FAQs in /assets/chat-index.json). Nothing typed here
// leaves the visitor's browser: there is no server and no AI model behind it.
(function () {
  var STOP = ('a an and are as at be but by can do does for from have how i if in is it its me my of on or our so than that the ' +
    'their them then there these they this to was we what when where which who why will with would you your about any get got ' +
    'need want like tell know help please us am im i\'m also just really very much more most some').split(' ');
  var stop = {}; STOP.forEach(function (w) { stop[w] = 1; });
  var SYN = { website: 'web', websites: 'web', site: 'web', sites: 'web', webpage: 'web', ads: 'ad', advertising: 'ad', advertise: 'ad',
    adwords: 'ppc', 'pay-per-click': 'ppc', texting: 'sms', texts: 'sms', text: 'sms', emails: 'email', 'e-mail': 'email', newsletter: 'email',
    newsletters: 'email', chatbot: 'agent', chatbots: 'agent', bot: 'agent', bots: 'agent', agents: 'agent', assistant: 'agent', ai: 'ai',
    apps: 'app', application: 'app', iphone: 'app', android: 'app', ios: 'app', reviews: 'review', reputation: 'review', leads: 'lead',
    crm: 'crm', booking: 'book', bookings: 'book', appointment: 'book', appointments: 'book', schedule: 'book', scheduling: 'book',
    videos: 'video', reels: 'video', reel: 'video', tiktok: 'video', instagram: 'social', facebook: 'social', ranking: 'seo', rankings: 'seo',
    rank: 'seo', google: 'seo', search: 'seo', brochure: 'print', brochures: 'print', printing: 'print', printed: 'print', cards: 'print',
    logo: 'brand', branding: 'brand', integrate: 'integration', integrations: 'integration', api: 'integration', webhook: 'integration',
    webhooks: 'integration', emr: 'emr', ehr: 'emr', store: 'ecommerce', shop: 'ecommerce', 'e-commerce': 'ecommerce', sell: 'ecommerce',
    hipaa: 'compliance', ada: 'accessibility', accessible: 'accessibility' };

  function tokens(str) {
    return (str || '').toLowerCase().replace(/[^a-z0-9\- ]+/g, ' ').split(/\s+/).map(function (w) {
      if (!w || stop[w]) return '';
      if (SYN[w]) return SYN[w];
      if (w.length > 5 && /ing$/.test(w)) w = w.slice(0, -3);
      else if (w.length > 4 && /(es|ed)$/.test(w)) w = w.slice(0, -2);
      else if (w.length > 3 && /s$/.test(w)) w = w.slice(0, -1);
      return SYN[w] || w;
    }).filter(Boolean);
  }

  var data = null, idf = {}, loading = null;
  function load() {
    if (data) return Promise.resolve();
    if (loading) return loading;
    loading = fetch('/assets/chat-index.json').then(function (r) { return r.json(); }).then(function (d) {
      var df = {};
      d.docs.forEach(function (doc) {
        doc.tt = tokens(doc.t); doc.qt = tokens(doc.q); doc.kt = tokens(doc.k); doc.at = tokens(doc.a);
        var seen = {};
        doc.tt.concat(doc.qt, doc.kt, doc.at).forEach(function (w) { if (!seen[w]) { seen[w] = 1; df[w] = (df[w] || 0) + 1; } });
      });
      Object.keys(df).forEach(function (w) { idf[w] = Math.log(1 + d.docs.length / df[w]); });
      data = d;
    });
    return loading;
  }

  function search(q) {
    var qt = tokens(q), out = [];
    if (!qt.length) return out;
    data.docs.forEach(function (doc) {
      var score = 0;
      qt.forEach(function (w) {
        var wgt = idf[w] || 0;
        if (doc.tt.indexOf(w) > -1) score += wgt * 3;
        if (doc.qt.indexOf(w) > -1) score += wgt * 2.2;
        if (doc.kt.indexOf(w) > -1) score += wgt * 1.4;
        if (doc.at.indexOf(w) > -1) score += wgt * 0.6;
      });
      if (doc.s) score *= /^(what|tell|explain|describe)/i.test(q.trim()) ? 1.7 : 1.35;   // prefer the service summary over a single FAQ
      if (score > 0) out.push({ doc: doc, score: score / Math.sqrt(qt.length) });
    });
    out.sort(function (a, b) { return b.score - a.score; });
    return out;
  }

  function contactLinks() {
    return [{ t: 'Call ' + data.phone, u: data.tel }, { t: 'Request a free analysis', u: '/contact-us/#analysis' }];
  }

  function answer(q) {
    var s = q.toLowerCase().trim();
    var hits = search(q), top = hits[0];
    if (/^(hi|hello|hey|hola|good (morning|afternoon|evening))\b/.test(s) && s.length < 30)
      return { text: ['Hello. I can answer basic questions about what Rx Medical Web does for medical practices. What would you like to know?'], chips: true };
    if (/^(thanks|thank you|gracias|great|perfect|ok|okay)\b/.test(s) && s.length < 40)
      return { text: ['You are welcome. If you would like to talk to a person, our team replies within 24 business hours.'], links: contactLinks() };
    if (/(diagnos|symptom|should i take|what should i do about my|medication for|dosage|side effect|(chest|back|head|stomach) pain|my pain|i have (a |an )?(pain|fever|rash|headache))/.test(s))
      return { text: ['I can only answer questions about our marketing services, and I cannot give medical advice. For a health question, please contact your physician.'] };
    if (/\b(price|prices|pricing|cost|costs|how much|fee|fees|rates?|budget|quote|precio|costo|cuanto)\b/.test(s)) {
      var links = contactLinks();
      if (top && top.score > 4.5) links.unshift({ t: top.doc.t, u: top.doc.u });
      return { text: ['Pricing depends on the practice and on what you need, so we do not publish a price list.', 'We start with a free website analysis, then give you a plan and a quote. We reply within 24 business hours.'], links: links };
    }
    if (/\b(phone number|your phone|call you|contact|talk to|speak (to|with)|human|a person|someone|your email|reach you|telefono|contacto|llamar)\b/.test(s))
      return { text: ['You can reach our team at ' + data.phone + ' or ' + data.email + ', Monday to Friday, 9 am to 6 pm Eastern.', 'We reply within 24 business hours.'], links: contactLinks().concat([{ t: 'Contact page', u: '/contact-us/' }]) };
    if (/(where|address|located|location|office|hours|open|horario|direccion)/.test(s) && !(top && top.score > 4))
      return { text: ['We are at 2720 E. Oakland Park Blvd, Suite 103, Fort Lauderdale, FL 33306.', 'Our hours are Monday to Friday, 9 am to 6 pm.'], links: [{ t: 'Contact page', u: '/contact-us/' }] };
    if (/^(who are you|who is rx|what is rx medical web|about (you|your company|the company|rx)|tell me about (you|your company|rx))/.test(s)) {
      var about = data.docs.filter(function (d) { return d.t === 'About Rx Medical Web'; })[0];
      if (about) return { text: [about.a], links: [{ t: 'About us', u: '/about/' }, { t: 'Why choose us', u: '/about/why-choose-us/' }] };
    }
    if (/(what (do you|services)|which services|all (your )?services|list of services|what can you do|servicios|que hacen)/.test(s))
      return { text: ['We do one thing: the online presence and marketing of medical practices. These are the areas we cover:'], groups: true };
    if (top && top.score > 2.2) {
      var seen = {}, more = [];
      seen[top.doc.u] = 1;
      hits.slice(1, 8).forEach(function (h) { if (h.score > 2 && !seen[h.doc.u] && more.length < 2) { seen[h.doc.u] = 1; more.push({ t: h.doc.t, u: h.doc.u }); } });
      return { text: [top.doc.a], links: [{ t: 'Read more: ' + top.doc.t, u: top.doc.u }].concat(more) };
    }
    return { text: ['I do not have an answer for that. I can only answer basic questions about our services, using what is on this website.', 'Our team will be glad to help directly.'], links: contactLinks(), chips: true };
  }

  // ---------- interface ----------
  var CHIPS = ['What services do you offer?', 'Can you connect to our current systems?', 'What are AI agents?', 'How much does a website cost?'];
  var root = document.createElement('div');
  root.className = 'rxchat';
  root.innerHTML =
    '<button class="rxchat-open" type="button" aria-expanded="false" aria-controls="rxchat-panel"><span aria-hidden="true">℞</span> Ask a question</button>' +
    '<section class="rxchat-panel" id="rxchat-panel" role="dialog" aria-label="Rx Medical Web assistant" hidden>' +
    '<header><div><b>Ask Rx Medical Web</b><small>Automated answers from this website</small></div><button class="rxchat-close" type="button" aria-label="Close the assistant">×</button></header>' +
    '<div class="rxchat-log" role="log" aria-live="polite"></div>' +
    '<form class="rxchat-form"><label class="vh" for="rxchat-input">Your question</label><input id="rxchat-input" type="text" autocomplete="off" placeholder="Ask about our services" maxlength="200"><button type="submit">Send</button></form>' +
    '<p class="rxchat-note">This assistant cannot give medical advice. Please do not enter patient information.</p>' +
    '</section>';
  document.body.appendChild(root);
  var openBtn = root.querySelector('.rxchat-open'), panel = root.querySelector('.rxchat-panel'), log = root.querySelector('.rxchat-log');
  var form = root.querySelector('form'), input = root.querySelector('input'), started = false;

  function add(cls, build) {
    var el = document.createElement('div');
    el.className = 'rxchat-msg ' + cls;
    build(el);
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
    return el;
  }
  function p(parent, text) { var e = document.createElement('p'); e.textContent = text; parent.appendChild(e); }
  function linkRow(parent, links) {
    var row = document.createElement('div'); row.className = 'rxchat-links';
    links.forEach(function (l) { var a = document.createElement('a'); a.href = l.u; a.textContent = l.t; row.appendChild(a); });
    parent.appendChild(row);
  }
  function chipRow(parent) {
    var row = document.createElement('div'); row.className = 'rxchat-chips';
    CHIPS.forEach(function (c) {
      var b = document.createElement('button'); b.type = 'button'; b.textContent = c;
      b.addEventListener('click', function () { ask(c); });
      row.appendChild(b);
    });
    parent.appendChild(row);
  }
  function reply(res) {
    add('bot', function (el) {
      res.text.forEach(function (t) { p(el, t); });
      if (res.groups) data.groups.forEach(function (g) {
        var h = document.createElement('p'); h.className = 'rxchat-group'; h.textContent = g.g; el.appendChild(h);
        linkRow(el, g.items);
      });
      if (res.links) linkRow(el, res.links);
      if (res.chips) chipRow(el);
    });
  }
  function ask(q) {
    q = (q || '').trim();
    if (!q) return;
    add('me', function (el) { p(el, q); });
    input.value = '';
    load().then(function () { reply(answer(q)); }).catch(function () {
      add('bot', function (el) { p(el, 'I could not load my answers just now. Please call us at 1-888-599-4548 or use the contact page.'); linkRow(el, [{ t: 'Contact page', u: '/contact-us/' }]); });
    });
  }
  function setOpen(open) {
    panel.hidden = !open;
    root.classList.toggle('is-open', open);
    openBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) {
      load();
      if (!started) {
        started = true;
        add('bot', function (el) {
          p(el, 'Hello. I can answer basic questions about our services for medical practices. Pick one or type your own.');
          chipRow(el);
        });
      }
      input.focus();
    } else {
      openBtn.focus();
    }
  }
  openBtn.addEventListener('click', function () { setOpen(panel.hidden); });
  root.querySelector('.rxchat-close').addEventListener('click', function () { setOpen(false); });
  form.addEventListener('submit', function (e) { e.preventDefault(); ask(input.value); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) setOpen(false); });
})();
