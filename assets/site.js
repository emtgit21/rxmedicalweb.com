// Rx Medical Web — small progressive enhancements. The site works without this file.
(function () {
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  if (header && toggle) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.textContent = open ? 'Close' : 'Menu';
      document.documentElement.classList.toggle('nav-lock', open);
    });
  }

  // A soft highlight slides between the main links as the pointer moves across them.
  var nav = document.querySelector('.nav');
  var hl = document.querySelector('.nav-hl');
  if (nav && hl && window.matchMedia('(hover: hover)').matches) {
    var items = nav.querySelectorAll(':scope > a, .nav-services > button');
    items.forEach(function (it) {
      it.addEventListener('pointerenter', function () {
        var w = header.querySelector('.wrap').getBoundingClientRect(), r = it.getBoundingClientRect();
        hl.style.width = r.width + 'px';
        hl.style.transform = 'translateX(' + (r.left - w.left) + 'px)';
        hl.style.opacity = '1';
      });
    });
    nav.addEventListener('pointerleave', function () { hl.style.opacity = '0'; });
  }

  // Services menu: the preview on the right follows the link under the pointer or focus.
  var preview = document.querySelector('.menu-preview');
  if (preview) {
    var pImg = preview.querySelector('img'), pName = preview.querySelector('b'), pText = preview.querySelector('p'), current = '';
    var show = function (a) {
      if (current === a.href) return;
      current = a.href;
      pName.textContent = a.textContent; pText.textContent = a.getAttribute('data-blurb');
      var src = '/assets/img/' + a.getAttribute('data-img') + '.webp';
      if (pImg.getAttribute('src') !== src) {
        pImg.classList.add('out');
        var next = new Image();
        next.onload = function () { pImg.src = src; pImg.classList.remove('out'); };
        next.src = src;
      }
    };
    document.querySelectorAll('.menu-cols a').forEach(function (a) {
      a.addEventListener('pointerenter', function () { show(a); });
      a.addEventListener('focus', function () { show(a); });
    });
  }
  // On phones each service group opens on its own.
  document.querySelectorAll('.menu .mh button').forEach(function (b) {
    b.addEventListener('click', function (e) {
      e.stopPropagation();
      var col = b.closest('div'), open = col.classList.toggle('open');
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  var services = document.querySelector('.nav-services');
  if (services) {
    var button = services.querySelector('button');
    var close = function () {
      services.classList.remove('open');
      button.setAttribute('aria-expanded', 'false');
    };
    button.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = services.classList.toggle('open');
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function (e) {
      if (!services.contains(e.target)) close();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        close();
        if (services.contains(document.activeElement)) document.activeElement.blur();
      }
    });
  }

  var calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Header condenses once the page scrolls.
  if (header) {
    var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 24); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // The prescription pad leans toward the pointer, eased so it feels like paper, not a cursor.
  var pad = document.querySelector('.pad');
  var hero = document.querySelector('.hero');
  if (pad && hero && !calm && window.matchMedia('(hover: hover) and (min-width: 901px)').matches) {
    var tx = 0, ty = 0, cx = 0, cy = 0, raf = null;
    var tick = function () {
      cx += (tx - cx) * 0.08; cy += (ty - cy) * 0.08;
      pad.style.transform = 'rotate(' + (2.2 + cx * 1.2).toFixed(3) + 'deg) rotateY(' + (cx * 9).toFixed(3) + 'deg) rotateX(' + (-cy * 7).toFixed(3) + 'deg) translate3d(' + (cx * 10).toFixed(2) + 'px,' + (cy * 8).toFixed(2) + 'px,0)';
      raf = (Math.abs(tx - cx) > 0.001 || Math.abs(ty - cy) > 0.001) ? requestAnimationFrame(tick) : null;
    };
    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      tx = (e.clientX - r.left) / r.width * 2 - 1; ty = (e.clientY - r.top) / r.height * 2 - 1;
      pad.style.transition = 'none';
      if (!raf) raf = requestAnimationFrame(tick);
    });
    hero.addEventListener('pointerleave', function () { tx = 0; ty = 0; if (!raf) raf = requestAnimationFrame(tick); });
  }

  // Patient story: on wide screens the graphics move into a pinned stage and cross-fade as each step is read.
  var stage = document.querySelector('.story-stage');
  var steps = document.querySelectorAll('.story-step');
  if (stage && steps.length && 'IntersectionObserver' in window && window.matchMedia('(min-width: 900px)').matches) {
    var panels = [];
    steps.forEach(function (st) {
      var fig = st.querySelector('.anim');
      fig.setAttribute('data-manual', '');
      stage.appendChild(fig);
      panels.push(fig);
    });
    var activate = function (i) {
      steps.forEach(function (st, n) { st.classList.toggle('active', n === i); });
      panels.forEach(function (p, n) { p.classList.toggle('active', n === i); p.classList.toggle('in', n === i); });
    };
    activate(0);
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) activate(Array.prototype.indexOf.call(steps, en.target));
      });
    }, { rootMargin: '-45% 0px -45% 0px' });
    steps.forEach(function (st) { so.observe(st); });
  }

  // 90-day plan: the graphic stays pinned and advances with the scroll (scrollytelling).
  var plan = document.querySelector('.sp-plan');
  var sc = plan && plan.querySelector('.sc');
  if (sc && !calm && window.CSS && CSS.supports('position', 'sticky') && CSS.supports('width', 'clamp(0px, 1px, 2px)')) {
    var pSteps = sc.querySelectorAll('ol > li');
    var scenes = sc.querySelectorAll('.sc-scene');
    var marks = sc.querySelectorAll('.sc-rail span');
    var dayEl = sc.querySelector('.sc-day b');
    var days = [1, 14, 30, 75, 90];
    if (pSteps.length === 4 && scenes.length === 4) {
      plan.classList.add('sc-live');
      var pRaf = 0, lastDay = 0;
      var draw = function () {
        pRaf = 0;
        var narrow = window.innerWidth <= 900;
        var focal = window.innerHeight * (narrow ? 0.84 : 0.6), span = narrow ? 0.55 : 0.8;
        var act = 0, prog = 0;
        pSteps.forEach(function (li, i) {
          var r = li.getBoundingClientRect();
          if (focal >= r.top) { act = i; prog = Math.min(1, Math.max(0, (focal - r.top) / (r.height * span))); }
        });
        sc.style.setProperty('--t', ((act + prog) / 4).toFixed(4));
        var d = Math.round(days[act] + (days[act + 1] - days[act]) * prog);
        if (d !== lastDay) { dayEl.textContent = d; lastDay = d; }
        for (var i = 0; i < 4; i++) {
          pSteps[i].classList.toggle('on', i === act); pSteps[i].classList.toggle('past', i < act);
          scenes[i].classList.toggle('on', i === act); scenes[i].classList.toggle('past', i < act);
          marks[i].classList.toggle('on', i <= act); marks[i].classList.toggle('cur', i === act);
          scenes[i].style.setProperty('--p', i < act ? 1 : i > act ? 0 : prog.toFixed(4));
        }
      };
      var ask = function () { if (!pRaf) pRaf = requestAnimationFrame(draw); };
      window.addEventListener('scroll', ask, { passive: true });
      window.addEventListener('resize', ask);
      draw();
    }
  }

  // Living-photo clips play only while visible.
  // Phones show the hero as a still image, so the hero clip is never downloaded there.
  var heroClip = document.querySelector('.hero-bg');
  if (heroClip && window.matchMedia('(max-width: 700px)').matches) heroClip.removeAttribute('loop');   // hidden on phones: never observed, never downloaded
  var clips = document.querySelectorAll('video[loop]');
  if ('IntersectionObserver' in window) {
    var vo = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && !calm) { var p = en.target.play(); if (p && p.catch) p.catch(function () {}); }
        else en.target.pause();
      });
    }, { threshold: 0.1 });
    if (!calm) clips.forEach(function (v) { vo.observe(v); });
  }

  // Start each animated graphic when it scrolls into view, and pause it when it leaves.
  var graphics = document.querySelectorAll('.anim:not([data-manual]), .reveal, .reveal-mask');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.target.classList.contains('reveal') || en.target.classList.contains('reveal-mask')) {
          if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
        } else {
          en.target.classList.toggle('in', en.isIntersecting);
        }
      });
    }, { threshold: 0.25 });
    graphics.forEach(function (g) { io.observe(g); });
  } else {
    graphics.forEach(function (g) { g.classList.add('in'); });
  }

  // Contact form: this static site has no server-side handler, so the form
  // composes an email in the visitor's own mail app, addressed to support@.
  var form = document.querySelector('form[data-mailto]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var lines = [
        'Name: ' + (d.get('name') || ''),
        'Practice: ' + (d.get('practice') || ''),
        'Phone: ' + (d.get('phone') || ''),
        'Email: ' + (d.get('email') || ''),
        'Website: ' + (d.get('website') || ''),
        'Interested in: ' + (d.get('topic') || ''),
        '',
        d.get('message') || ''
      ];
      var subject = (d.get('topic') || 'Website inquiry') + ' - ' + (d.get('practice') || d.get('name') || '');
      window.location.href = 'mailto:' + form.getAttribute('data-mailto') +
        '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
    });
  }
})();
