// Rx Medical Web — small progressive enhancements. The site works without this file.
(function () {
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  if (header && toggle) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.textContent = open ? 'Close' : 'Menu';
    });
  }

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

  // Start each animated graphic when it scrolls into view, and pause it when it leaves.
  var graphics = document.querySelectorAll('.anim, .reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.target.classList.contains('reveal')) {
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
