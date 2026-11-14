// Call booking: pick a day, pick a time, leave your details. Talks to /api/booking/ on the same site.
(function () {
  var root = document.querySelector('[data-booking]');
  if (!root) return;
  var API = '/api/booking/';
  var daysEl = root.querySelector('.bk-days'), timesEl = root.querySelector('.bk-times'), form = root.querySelector('form');
  var statusEl = root.querySelector('.bk-status'), chosenEl = root.querySelector('.bk-chosen'), tzEl = root.querySelector('.bk-tz');
  var errEl = root.querySelector('.bk-error'), doneEl = root.querySelector('.bk-done'), btn = form.querySelector('button[type=submit]');
  var tz = '';
  try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) {}
  var fmt = function (opts) { return new Intl.DateTimeFormat('en-US', opts); };
  var fDow = fmt({ weekday: 'short' }), fDay = fmt({ day: 'numeric' }), fMon = fmt({ month: 'short' });
  var fTime = fmt({ hour: 'numeric', minute: '2-digit' }), fLong = fmt({ weekday: 'long', month: 'long', day: 'numeric' });
  var fZone = fmt({ timeZoneName: 'short' });
  var groups = [], picked = null;

  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }
  function key(d) { return d.getFullYear() + '-' + d.getMonth() + '-' + d.getDate(); }

  function showTimes(i) {
    Array.prototype.forEach.call(daysEl.children, function (b, n) { b.setAttribute('aria-pressed', n === i ? 'true' : 'false'); });
    timesEl.textContent = '';
    groups[i].slots.forEach(function (s) {
      var b = el('button', 'bk-time', fTime.format(s.date));
      b.type = 'button';
      b.setAttribute('aria-pressed', picked && picked.id === s.id ? 'true' : 'false');
      b.addEventListener('click', function () { pick(s, b); });
      timesEl.appendChild(b);
    });
  }

  function pick(s, b) {
    picked = s;
    Array.prototype.forEach.call(timesEl.children, function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    chosenEl.textContent = fLong.format(s.date) + ' at ' + fTime.format(s.date);
    root.classList.add('has-time');
    errEl.textContent = '';
    btn.disabled = false;
    if (window.matchMedia('(max-width: 900px)').matches) form.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function load(keepDay) {
    return fetch(API + 'slots', { headers: { Accept: 'application/json' } }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (d) {
      groups = []; var map = {};
      d.days.forEach(function (day) { day.slots.forEach(function (s) {
        var date = new Date(s.utc), k = key(date);
        if (!map[k]) { map[k] = { date: date, slots: [] }; groups.push(map[k]); }
        map[k].slots.push({ id: s.id, date: date });
      }); });
      var sel = form.querySelector('select[name=topic]');
      if (!sel.options.length) d.topics.forEach(function (t) { sel.appendChild(new Option(t, t)); });
      daysEl.textContent = '';
      if (!groups.length) { statusEl.textContent = 'No times are open right now. Please call us at 1-888-599-4548.'; return; }
      statusEl.textContent = '';
      groups.forEach(function (g, i) {
        var b = el('button', 'bk-day'); b.type = 'button';
        b.appendChild(el('span', '', fDow.format(g.date))); b.appendChild(el('b', '', fDay.format(g.date))); b.appendChild(el('span', '', fMon.format(g.date)));
        b.setAttribute('aria-label', fLong.format(g.date) + ', ' + g.slots.length + ' times open');
        b.addEventListener('click', function () { showTimes(i); });
        daysEl.appendChild(b);
      });
      var zone = '';
      try { zone = fZone.formatToParts(groups[0].date).filter(function (p) { return p.type === 'timeZoneName'; })[0].value; } catch (e) {}
      tzEl.textContent = 'Times are shown in your time zone' + (zone ? ' (' + zone + ')' : '') + '. Calls last 30 minutes.';
      showTimes(Math.min(keepDay || 0, groups.length - 1));
      root.classList.add('ready');
    }).catch(function () {
      statusEl.textContent = 'We could not load the calendar. Please call us at 1-888-599-4548 or try again in a minute.';
    });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!picked) { errEl.textContent = 'Please pick a time first.'; return; }
    var d = new FormData(form), body = { slot: picked.id, tz: tz };
    ['name', 'practice', 'phone', 'email', 'website', 'topic', 'notes', 'company_url'].forEach(function (k) { body[k] = d.get(k) || ''; });
    btn.disabled = true; btn.textContent = 'Booking…'; errEl.textContent = '';
    fetch(API + 'book', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (res) {
        btn.textContent = 'Book the call';
        if (!res.ok) {
          errEl.textContent = res.j.error || 'Something went wrong. Please call us at 1-888-599-4548.';
          btn.disabled = false;
          if (res.j.field === 'slot') { picked = null; root.classList.remove('has-time'); btn.disabled = true; load(); }
          else if (res.j.field && form.elements[res.j.field]) form.elements[res.j.field].focus();
          return;
        }
        doneEl.querySelector('.bk-when').textContent = fLong.format(picked.date) + ' at ' + fTime.format(picked.date);
        doneEl.querySelector('.bk-phone').textContent = body.phone;
        doneEl.querySelector('.bk-ics').href = API + 'ics?t=' + encodeURIComponent(res.j.token);
        doneEl.querySelector('.bk-cancel').href = API + 'cancel?t=' + encodeURIComponent(res.j.token);
        root.classList.add('done');
        doneEl.setAttribute('tabindex', '-1'); doneEl.focus();
        doneEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        if (window.gtag) window.gtag('event', 'generate_lead', { method: 'call_booking', topic: body.topic });
      })
      .catch(function () { btn.disabled = false; btn.textContent = 'Book the call'; errEl.textContent = 'We could not reach the server. Please try again or call 1-888-599-4548.'; });
  });

  load();
})();
