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
    hipaa: 'compliance', ada: 'accessibility', accessible: 'accessibility',
    // Spanish
    pagina: 'web', paginas: 'web', sitio: 'web', sitios: 'web', web: 'web', anuncio: 'ad', anuncios: 'ad', publicidad: 'ad', pauta: 'ad',
    redes: 'social', sociales: 'social', correo: 'email', correos: 'email', boletin: 'email', mensajes: 'sms', mensaje: 'sms', texto: 'sms',
    resena: 'review', resenas: 'review', opiniones: 'review', reputacion: 'review', aplicacion: 'app', aplicaciones: 'app', celular: 'app',
    cita: 'book', citas: 'book', agendar: 'book', reservas: 'book', reserva: 'book', agenda: 'book', impresion: 'print', imprimir: 'print',
    folleto: 'print', folletos: 'print', tarjetas: 'print', marca: 'brand', logotipo: 'brand', diseno: 'design', posicionamiento: 'seo',
    buscadores: 'seo', agente: 'agent', agentes: 'agent', inteligencia: 'ai', artificial: 'ai', ia: 'ai', integracion: 'integration',
    integraciones: 'integration', integrar: 'integration', conectar: 'integration', conectarse: 'integration', conexion: 'integration', sistemas: 'integration', sistema: 'integration', systems: 'integration', connect: 'integration', prospectos: 'lead',
    tienda: 'ecommerce', vender: 'ecommerce', portafolio: 'portfolio', estrategia: 'strategy', analitica: 'analytics', llamadas: 'call',
    contenido: 'content', articulos: 'content', mantenimiento: 'maintenance', accesibilidad: 'accessibility', lanzamiento: 'launch',
    lanzar: 'launch', mapa: 'local', mapas: 'local', cerca: 'local' };
  var ES_STOP = ('el la los las un una unos unas de del al y o que en con por para como es son esta estan hay mi mis su sus nos me se lo le ' +
    'les si no mas muy pero tambien hacen hace hacer tienen tiene pueden puede puedo quiero necesito ustedes usted ofrecen ofrece sobre ' +
    'algo esto eso ese esa aqui ayudar ayuda ayudan ayudarme servicio').split(' ');
  ES_STOP.forEach(function (w) { stop[w] = 1; });
  function fold(str) { return (str || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''); }
  function isSpanish(str) {
    return /[¿¡ñ]/.test(str.toLowerCase()) || /\b(hola|gracias|que|como|cuanto|cuanta|cuesta|donde|hacen|tienen|pueden|puedo|necesito|quiero|ustedes|para|pagina|paginas|pacientes|citas?|servicios|precio|costo|espanol|ayuda|redes|ofrecen|buenos|buenas)\b/.test(fold(str));
  }

  function tokens(str) {
    return fold(str).replace(/[^a-z0-9\- ]+/g, ' ').split(/\s+/).map(function (w) {
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

  var T = {
    en: {
      hello: 'Hello. I can answer basic questions about what Rx Medical Web does for medical practices. What would you like to know?',
      thanks: 'You are welcome. If you would like to talk to a person, our team replies within 24 business hours.',
      price1: 'Pricing depends on the practice and on what you need, so we do not publish a price list.',
      price2: 'We start with a free website analysis, then give you a plan and a quote. We reply within 24 business hours.',
      contact1: function () { return 'You can reach our team at ' + data.phone + ' or ' + data.email + ', Monday to Friday, 9 am to 6 pm Eastern.'; },
      contact2: 'We reply within 24 business hours.',
      where1: 'We are at 2720 E. Oakland Park Blvd, Suite 103, Fort Lauderdale, FL 33306.', where2: 'Our hours are Monday to Friday, 9 am to 6 pm.',
      services: 'We do one thing: the online presence and marketing of medical practices. These are the areas we cover:',
      medical: 'I can only answer questions about our marketing services, and I cannot give medical advice. For a health question, please contact your physician.',
      patients1: 'Bringing in new patients usually takes a combination: being found on Google and on the map, ads for the treatments you want to grow, good reviews, and a website that makes it easy to call or book.',
      patients2: 'These are the services that do that. A free website analysis will show where to start for your practice.',
      start1: 'It starts with a free website analysis: we review your website, your rankings and your competitors and walk you through what we found.',
      start2: 'Then we give you a plan and a quote. Once you approve it, our in-house team builds it and reports results to you every month.',
      spanish: 'Yes. Our team speaks Spanish and English.',
      maybe: 'This may be what you are looking for:',
      none1: 'I do not have a good answer for that. I can only answer basic questions about our services, using what is on this website.',
      none2: 'Our team will be glad to help directly.',
      call: 'Call ', free: 'Request a free analysis', contactPage: 'Contact page', more: 'Read more: ', all: 'See all services'
    },
    es: {
      hello: 'Hola. Puedo responder preguntas básicas sobre lo que Rx Medical Web hace por las consultas médicas. ¿Qué te gustaría saber?',
      thanks: 'Con gusto. Si prefieres hablar con una persona, nuestro equipo responde en un máximo de 24 horas hábiles.',
      price1: 'El precio depende de la consulta y de lo que necesite, por eso no publicamos una lista de precios.',
      price2: 'Empezamos con un análisis gratuito de tu sitio web y después te damos un plan y una cotización. Respondemos en 24 horas hábiles.',
      contact1: function () { return 'Puedes comunicarte con nuestro equipo al ' + data.phone + ' o a ' + data.email + ', de lunes a viernes, de 9 am a 6 pm (hora del Este).'; },
      contact2: 'Respondemos en un máximo de 24 horas hábiles.',
      where1: 'Estamos en 2720 E. Oakland Park Blvd, Suite 103, Fort Lauderdale, FL 33306.', where2: 'Atendemos de lunes a viernes, de 9 am a 6 pm.',
      services: 'Hacemos una sola cosa: la presencia en línea y el marketing de consultas médicas. Estas son las áreas que cubrimos (las páginas están en inglés):',
      medical: 'Solo puedo responder sobre nuestros servicios de marketing y no puedo dar consejo médico. Para una pregunta de salud, consulta a tu médico.',
      patients1: 'Atraer pacientes nuevos suele requerir una combinación: aparecer en Google y en el mapa, anuncios para los tratamientos que quieres crecer, buenas reseñas y un sitio web donde sea fácil llamar o reservar.',
      patients2: 'Estos son los servicios que lo hacen. Un análisis gratuito de tu sitio muestra por dónde empezar.',
      start1: 'Todo empieza con un análisis gratuito: revisamos tu sitio web, tu posicionamiento y tu competencia, y te explicamos lo que encontramos.',
      start2: 'Después te damos un plan y una cotización. Cuando lo apruebas, nuestro equipo lo construye y te reporta resultados cada mes.',
      spanish: 'Sí. Nuestro equipo habla español e inglés.',
      maybe: 'Esto puede ser lo que buscas (el detalle está en inglés):',
      none1: 'No tengo una buena respuesta para eso. Solo puedo responder preguntas básicas sobre nuestros servicios con lo que está en este sitio.',
      none2: 'Nuestro equipo te ayuda directamente con gusto.',
      call: 'Llamar al ', free: 'Pedir un análisis gratuito', contactPage: 'Página de contacto', more: 'Ver más: ', all: 'Ver todos los servicios'
    }
  };

  function svcLinks(urls) {
    var out = [];
    urls.forEach(function (u) { data.docs.some(function (d) { if (d.s && d.u === u) { out.push({ t: d.t, u: d.u }); return true; } return false; }); });
    return out;
  }

  function answer(q) {
    var es = isSpanish(q), L = es ? T.es : T.en;
    var s = fold(q).trim();
    var hits = search(q), top = hits[0];
    var contact = [{ t: L.call + data.phone, u: data.tel }, { t: L.free, u: '/contact-us/#analysis' }];
    var strong = top && top.score > 4.5;

    if (/(diagnos|sintoma|symptom|should i take|que debo tomar|medication for|medicamento para|dosage|dosis|side effect|efecto secundario|(chest|back|head|stomach) pain|dolor de|my pain|i have (a |an )?(pain|fever|rash|headache)|tengo (dolor|fiebre))/.test(s))
      return { text: [L.medical] };
    if (/^(hi|hello|hey|hola|buenas|buenos dias|good (morning|afternoon|evening))\b/.test(s) && s.split(' ').length <= 3)
      return { text: [L.hello], chips: true };
    if (/^(thanks|thank you|gracias|muchas gracias|great|perfect|perfecto|ok|okay|vale)\b/.test(s) && s.length < 40)
      return { text: [L.thanks], links: contact };
    if (/\b(spanish|espanol|habla[ns]? espanol|en espanol)\b/.test(s))
      return { text: [L.spanish], links: contact };
    if (/\b(price|prices|pricing|cost|costs|how much|fee|fees|rates?|budget|quote|precio|precios|costo|costos|cuesta|cuestan|cuanto|cotizacion|presupuesto|tarifas?)\b/.test(s)) {
      var pl = contact.slice();
      if (top && top.score > 7) pl.unshift({ t: top.doc.t, u: top.doc.u });
      return { text: [L.price1, L.price2], links: pl };
    }
    if (/\b(phone number|your phone|call you|contact|talk to|speak (to|with)|human|a person|someone|your email|reach you|meeting|appointment with you|schedule a call|telefono|contacto|contactar|llamar|llamada con|hablar con|persona|reunion|quiero una cita|agendar una (cita|llamada)|cita con ustedes)\b/.test(s))
      return { text: [L.contact1(), L.contact2], links: contact.concat([{ t: L.contactPage, u: '/contact-us/' }]) };
    if (/\b(where|address|located|location|office|hours|open|horario|direccion|donde|ubicacion|ubicados|oficina)\b/.test(s) && !strong)
      return { text: [L.where1, L.where2], links: [{ t: L.contactPage, u: '/contact-us/' }] };
    if (/^(who are you|who is rx|what is rx medical web|about (you|your company|the company|rx)|tell me about (you|your company|rx)|quienes son|quien es rx|que es rx)/.test(s)) {
      var about = data.docs.filter(function (d) { return d.t === 'About Rx Medical Web'; })[0];
      if (about) return { text: [about.a], links: [{ t: 'About us', u: '/about/' }, { t: 'Why choose us', u: '/about/why-choose-us/' }] };
    }
    if (/(more|new|mas|nuevos|atraer|conseguir|get|getting|grow|crecer|aumentar).{0,25}(patients|pacientes|clients|clientes)|(patients|pacientes).{0,15}(more|mas|nuevos)|grow my practice|crecer mi (consulta|practica|clinica)/.test(s))
      return { text: [L.patients1, L.patients2], links: svcLinks(['/service/search-engine-optimization/', '/service/local-seo/', '/service/pay-per-click/', '/service/reputation-management/', '/service/medical-website-design/']).concat([{ t: L.free, u: '/contact-us/#analysis' }]) };
    if (/(how does (it|this) work|how do (we|i) (start|get started|begin)|get started|where do (we|i) start|next steps?|how do you work|what is the process|como funciona|como empez|como (trabajan|es el proceso)|por donde empiez|siguiente paso|help (me|my practice|us)|ayud(a|en|ar)(me|nos)? (con )?(mi|a mi|nuestra) (consulta|practica|clinica))/.test(s))
      return { text: [L.start1, L.start2], links: contact.concat([{ t: L.all, u: '/#services' }]) };
    if (/(what (do you|services)|which services|all (your )?services|list of services|what can you do|what do you offer|servicios|que hacen|que ofrecen|a que se dedican)/.test(s) || /^(marketing|services?|help|ayuda|info|informacion)$/.test(s))
      return { text: [L.services], groups: true };

    if (/(redes sociales|social media|instagram|facebook|tiktok)/.test(s) && !/\b(ads?|advertis|anuncios?|publicidad|pauta)/.test(s)) {
      var sm = data.docs.filter(function (d) { return d.s && d.u === '/service/social-media/'; })[0];
      if (sm) return { text: (es ? [L.maybe] : []).concat([sm.a]), links: [{ t: L.more + sm.t, u: sm.u }].concat(svcLinks(['/service/short-form-video/', '/service/search-engine-marketing/'])) };
    }
    if (top && top.score > 2.2) {
      var seen = {}, more = [];
      seen[top.doc.u] = 1;
      hits.slice(1, 8).forEach(function (h) { if (h.score > 2 && !seen[h.doc.u] && more.length < 2) { seen[h.doc.u] = 1; more.push({ t: h.doc.t, u: h.doc.u }); } });
      var text = [top.doc.a];
      if (!strong || es) text.unshift(L.maybe);
      return { text: text, links: [{ t: L.more + top.doc.t, u: top.doc.u }].concat(more) };
    }
    return { text: [L.none1, L.none2], links: contact.concat([{ t: L.all, u: '/#services' }]), chips: true };
  }

  // ---------- interface ----------
  var CHIPS = ['What services do you offer?', 'How do we get more patients?', 'How does it work?', 'What are AI agents?', 'How much does it cost?'];
  var root = document.createElement('div');
  root.className = 'rxchat';
  root.innerHTML =
    '<button class="rxchat-open" type="button" aria-expanded="false" aria-controls="rxchat-panel"><span aria-hidden="true">℞</span> Ask a question</button>' +
    '<section class="rxchat-panel" id="rxchat-panel" role="dialog" aria-label="Rx Medical Web assistant" hidden>' +
    '<header><div><b>Ask Rx Medical Web</b><small>Automated answers from this website · English o español</small></div><button class="rxchat-close" type="button" aria-label="Close the assistant">×</button></header>' +
    '<div class="rxchat-log" role="log" aria-live="polite"></div>' +
    '<form class="rxchat-form"><label class="vh" for="rxchat-input">Your question</label><input id="rxchat-input" type="text" autocomplete="off" placeholder="Ask about our services / Pregunta aquí" maxlength="200"><button type="submit">Send</button></form>' +
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
