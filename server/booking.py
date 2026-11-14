#!/usr/bin/env python3
"""Call booking service for rxmedicalweb.com. Standard library only.

Runs on the droplet behind nginx (location /api/booking/ -> 127.0.0.1:8791) as the
systemd unit rxbooking. Bookings live in SQLite outside the web root.

  GET  /api/booking/slots          open slots for the next weeks
  POST /api/booking/book           create a booking (JSON)
  GET  /api/booking/ics?t=<token>  calendar file for a booking
  GET  /api/booking/cancel?t=<token>  cancel a booking (link in the confirmation)
  POST /api/booking/contact        relay the contact form to the office by e-mail (nothing is stored)

Settings come from the environment (see /etc/rxbooking.env on the server):
  RXB_DB        path of the SQLite file            (default /var/lib/rxbooking/bookings.db)
  RXB_PORT      port to listen on, loopback only   (default 8791)
  RXB_NOTIFY    optional command run after each booking or cancellation; it receives
                the booking as JSON on standard input and "booked" or "cancelled" as argument
  MAILGUN_SENDING_KEY  sending key of the Mailgun domain; without it no e-mail is sent
  RXB_MAIL_DOMAIN      Mailgun sending domain          (default mg.rxmedicalweb.com)
  RXB_MAIL_TO          where notices and form requests go (default support@rxmedicalweb.com)

Staff commands:  python3 booking.py list | cancel <id> | block <YYYY-MM-DD> [note] | unblock <YYYY-MM-DD>
"""
import base64
import datetime as dt
import json
import os
import re
import secrets
import sqlite3
import subprocess
import sys
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/New_York")
DB = os.environ.get("RXB_DB", "/var/lib/rxbooking/bookings.db")
PORT = int(os.environ.get("RXB_PORT", "8791"))
NOTIFY = os.environ.get("RXB_NOTIFY", "")
MAIL_KEY = os.environ.get("MAILGUN_SENDING_KEY", "").strip()
MAIL_DOMAIN = os.environ.get("RXB_MAIL_DOMAIN", "mg.rxmedicalweb.com")
MAIL_TO = os.environ.get("RXB_MAIL_TO", "support@rxmedicalweb.com")

OPEN, CLOSE = dt.time(9, 0), dt.time(18, 0)   # office hours, Eastern time, Monday to Friday
SLOT_MIN = 30          # length of a call
STEP_MIN = 30          # distance between start times
LEAD_HOURS = 3         # earliest bookable time from now
DAYS_AHEAD = 21        # how far ahead visitors can book
LUNCH = (dt.time(12, 30), dt.time(13, 30))
TOPICS = ["Free website analysis", "A new website", "SEO and AI search", "Advertising", "Social media and video",
          "AI agents and lead follow-up", "E-mail and text campaigns", "Launching a new service", "Something else"]
LOCK = threading.Lock()
HITS = {}              # ip -> recent booking attempts


def db():
    con = sqlite3.connect(DB, timeout=10)
    con.row_factory = sqlite3.Row
    return con


def init():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    with db() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS booking (
          id INTEGER PRIMARY KEY, token TEXT UNIQUE NOT NULL, slot TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'booked',
          name TEXT, practice TEXT, phone TEXT, email TEXT, topic TEXT, notes TEXT, website TEXT, visitor_tz TEXT,
          ip TEXT, created TEXT NOT NULL, notified INTEGER NOT NULL DEFAULT 0);
        CREATE UNIQUE INDEX IF NOT EXISTS one_per_slot ON booking(slot) WHERE status = 'booked';
        CREATE TABLE IF NOT EXISTS closed (day TEXT PRIMARY KEY, note TEXT);
        """)
        if not con.execute("SELECT 1 FROM closed LIMIT 1").fetchone():
            con.executemany("INSERT OR IGNORE INTO closed VALUES (?, ?)", [
                ("2026-11-26", "Thanksgiving"), ("2026-11-27", "Day after Thanksgiving"), ("2026-12-24", "Christmas Eve"),
                ("2026-12-25", "Christmas"), ("2027-01-01", "New Year"), ("2027-05-31", "Memorial Day"),
                ("2027-07-05", "Independence Day observed"), ("2027-09-06", "Labor Day"), ("2027-11-25", "Thanksgiving"),
                ("2027-11-26", "Day after Thanksgiving"), ("2027-12-24", "Christmas Eve")])


def open_slots():
    now = dt.datetime.now(TZ)
    earliest = now + dt.timedelta(hours=LEAD_HOURS)
    with db() as con:
        taken = {r["slot"] for r in con.execute("SELECT slot FROM booking WHERE status = 'booked'")}
        closed = {r["day"] for r in con.execute("SELECT day FROM closed")}
    days = []
    for n in range(DAYS_AHEAD + 1):
        day = (now + dt.timedelta(days=n)).date()
        if day.weekday() > 4 or day.isoformat() in closed:
            continue
        t = dt.datetime.combine(day, OPEN, TZ)
        end = dt.datetime.combine(day, CLOSE, TZ)
        slots = []
        while t + dt.timedelta(minutes=SLOT_MIN) <= end:
            key = t.strftime("%Y-%m-%dT%H:%M")
            in_lunch = LUNCH[0] <= t.time() < LUNCH[1]
            if t >= earliest and key not in taken and not in_lunch:
                slots.append({"id": key, "utc": t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
            t += dt.timedelta(minutes=STEP_MIN)
        if slots:
            days.append({"day": day.isoformat(), "slots": slots})
    return days


def valid_slot(key):
    return any(key == s["id"] for d in open_slots() for s in d["slots"])


def clean(v, n):
    return re.sub(r"[\x00-\x1f\x7f]+", " ", str(v or "")).strip()[:n]


def slot_dt(key):
    return dt.datetime.strptime(key, "%Y-%m-%dT%H:%M").replace(tzinfo=TZ)


def describe(key):
    t = slot_dt(key)
    return t.strftime("%A, %B ") + str(t.day) + t.strftime(", %Y at ") + t.strftime("%I:%M %p").lstrip("0") + " Eastern"


def ics(row):
    start = slot_dt(row["slot"]).astimezone(dt.timezone.utc)
    end = start + dt.timedelta(minutes=SLOT_MIN)
    f = "%Y%m%dT%H%M%SZ"
    def esc(s):
        return str(s or "").replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Rx Medical Web//Call booking//EN", "METHOD:PUBLISH", "BEGIN:VEVENT",
             f"UID:{row['token']}@rxmedicalweb.com", f"DTSTAMP:{dt.datetime.now(dt.timezone.utc).strftime(f)}",
             f"DTSTART:{start.strftime(f)}", f"DTEND:{end.strftime(f)}",
             "SUMMARY:" + esc("Call with Rx Medical Web"),
             "DESCRIPTION:" + esc(f"We will call you at {row['phone']}.\nTopic: {row['topic']}\n"
                                  "Questions before the call: 1-888-599-4548 or support@rxmedicalweb.com"),
             "LOCATION:" + esc(f"Phone call to {row['phone']}"),
             "BEGIN:VALARM", "TRIGGER:-PT15M", "ACTION:DISPLAY", "DESCRIPTION:Call with Rx Medical Web", "END:VALARM",
             "END:VEVENT", "END:VCALENDAR"]
    return "\r\n".join(lines) + "\r\n"


def send_mail(subject, text, reply_to=""):
    """Send a plain-text message to the office through Mailgun. True when Mailgun accepted it."""
    if not MAIL_KEY:
        return False
    fields = {"from": f"Rx Medical Web website <website@{MAIL_DOMAIN}>", "to": MAIL_TO, "subject": subject[:200], "text": text}
    if reply_to:
        fields["h:Reply-To"] = reply_to
    req = urllib.request.Request(f"https://api.mailgun.net/v3/{MAIL_DOMAIN}/messages", data=urlencode(fields).encode())
    req.add_header("Authorization", "Basic " + base64.b64encode(("api:" + MAIL_KEY).encode()).decode())
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status == 200
    except Exception as ex:
        print("mail error:", getattr(ex, "code", ""), ex, flush=True)
        return False


def booking_text(row, event):
    lines = [("A call was booked on the website." if event == "booked" else "This call was CANCELLED by the visitor."), "",
             "When:     " + describe(row["slot"]), "Name:     " + row["name"], "Practice: " + (row["practice"] or "-"),
             "Phone:    " + row["phone"], "E-mail:   " + row["email"], "Website:  " + (row["website"] or "-"),
             "Topic:    " + row["topic"], "", "Note from the visitor:", row["notes"] or "-", "",
             "We call them at the number above; they are not expecting a meeting link."]
    return "\n".join(lines)


def notify(row, event):
    if not NOTIFY and not MAIL_KEY:
        return
    data = {k: row[k] for k in row.keys() if k not in ("ip",)}
    data["when"] = describe(row["slot"])
    def run():
        try:
            ok = False
            if MAIL_KEY:
                word = "New call booked" if event == "booked" else "Call cancelled"
                ok = send_mail(f"{word}: {row['name']}, {describe(row['slot'])}", booking_text(row, event), row["email"])
            if NOTIFY:
                r = subprocess.run(NOTIFY.split() + [event], input=json.dumps(data).encode(), timeout=60, capture_output=True)
                ok = ok or r.returncode == 0
                if r.returncode:
                    print("notify failed:", r.stderr.decode()[:300], flush=True)
            if ok and event == "booked":
                with db() as con:
                    con.execute("UPDATE booking SET notified = 1 WHERE id = ?", (row["id"],))
            elif not ok:
                print(f"notice not delivered for booking #{row['id']} ({event})", flush=True)
        except Exception as ex:  # a failed notice must never lose the booking
            print("notify error:", ex, flush=True)
    threading.Thread(target=run, daemon=True).start()


def too_many(ip):
    now = time.time()
    recent = [t for t in HITS.get(ip, []) if now - t < 3600]
    HITS[ip] = recent + [now]
    return len(recent) >= 6


SHELL = ("<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
         "<meta name='robots' content='noindex'><title>{title} | Rx Medical Web</title>"
         "<body style='font:18px/1.5 system-ui,sans-serif;max-width:34em;margin:12vh auto;padding:0 24px;color:#0b2f38'>{body}</body></html>")
CANCELLED = ("<h1>Your call is cancelled</h1><p>The call on {when} has been cancelled. "
             "<a href='/book-a-call/'>Pick another time</a> or call us at 1-888-599-4548.</p>")


class Handler(BaseHTTPRequestHandler):
    server_version = "rxbooking"

    def log_message(self, fmt, *args):
        print(self.headers.get("X-Real-IP", "-"), fmt % args, flush=True)

    def send(self, code, body, ctype="application/json", extra=None):
        raw = body if isinstance(body, bytes) else (json.dumps(body) if ctype == "application/json" else body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype + ("; charset=utf-8" if ctype.startswith("text/") or ctype == "application/json" else ""))
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Robots-Tag", "noindex")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(raw)

    def find(self, q):
        token = (q.get("t") or [""])[0]
        if not re.fullmatch(r"[A-Za-z0-9_-]{20,64}", token):
            return None
        with db() as con:
            return con.execute("SELECT * FROM booking WHERE token = ?", (token,)).fetchone()

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/api/booking/slots":
            return self.send(200, {"tz": "America/New_York", "minutes": SLOT_MIN, "topics": TOPICS, "days": open_slots()})
        if u.path == "/api/booking/ics":
            row = self.find(q)
            if not row or row["status"] != "booked":
                return self.send(404, {"error": "not found"})
            return self.send(200, ics(row), "text/calendar", {"Content-Disposition": 'attachment; filename="rx-medical-web-call.ics"'})
        if u.path == "/api/booking/cancel":
            row = self.find(q)
            if not row:
                return self.send(404, "<p>We could not find that booking.</p>", "text/html")
            # A link alone must not cancel anything (mail scanners open links), so this page only asks.
            if row["status"] == "booked":
                inner = (f"<h1>Cancel this call?</h1><p>Your call is on {describe(row['slot'])}.</p>"
                         "<form method='post'><button style='font:inherit;font-weight:700;padding:.7em 1.4em;border-radius:999px;border:0;"
                         "background:#0b2f38;color:#fff;cursor:pointer'>Yes, cancel the call</button></form>"
                         "<p><a href='/'>Keep the call</a></p>")
            else:
                inner = CANCELLED.format(when=describe(row["slot"]))
            return self.send(200, SHELL.format(title="Cancel your call", body=inner), "text/html")
        self.send(404, {"error": "not found"})

    def do_POST(self):
        u = urlparse(self.path)
        if u.path == "/api/booking/cancel":
            row = self.find(parse_qs(u.query))
            if not row:
                return self.send(404, "<p>We could not find that booking.</p>", "text/html")
            if row["status"] == "booked":
                with LOCK, db() as con:
                    con.execute("UPDATE booking SET status = 'cancelled' WHERE id = ?", (row["id"],))
                notify(row, "cancelled")
            return self.send(200, SHELL.format(title="Call cancelled", body=CANCELLED.format(when=describe(row["slot"]))), "text/html")
        if u.path not in ("/api/booking/book", "/api/booking/contact"):
            return self.send(404, {"error": "not found"})
        ip = self.headers.get("X-Real-IP", self.client_address[0])
        try:
            n = int(self.headers.get("Content-Length", "0"))
            if n <= 0 or n > 8000:
                return self.send(413, {"error": "The request is too large."})
            d = json.loads(self.rfile.read(n))
            assert isinstance(d, dict)
        except Exception:
            return self.send(400, {"error": "We could not read the request."})
        if clean(d.get("company_url"), 200):          # field hidden from people; only bots fill it in
            return self.send(200, {"ok": True, "when": "", "token": ""})
        if too_many(ip):
            return self.send(429, {"error": "Too many requests. Please call us at 1-888-599-4548."})
        if u.path == "/api/booking/contact":
            return self.contact(d)
        f = {"name": clean(d.get("name"), 80), "practice": clean(d.get("practice"), 120), "phone": clean(d.get("phone"), 40),
             "email": clean(d.get("email"), 120).lower(), "topic": clean(d.get("topic"), 60), "notes": clean(d.get("notes"), 1000),
             "website": clean(d.get("website"), 200), "visitor_tz": clean(d.get("tz"), 60)}
        slot = clean(d.get("slot"), 16)
        if len(f["name"]) < 2:
            return self.send(422, {"error": "Please enter your name.", "field": "name"})
        if len(re.sub(r"\D", "", f["phone"])) < 10:
            return self.send(422, {"error": "Please enter a phone number with area code.", "field": "phone"})
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", f["email"]):
            return self.send(422, {"error": "Please enter a valid e-mail address.", "field": "email"})
        if f["topic"] not in TOPICS:
            f["topic"] = TOPICS[-1]
        with LOCK:
            if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d", slot) or not valid_slot(slot):
                return self.send(409, {"error": "That time was just taken. Please pick another one.", "field": "slot"})
            token = secrets.token_urlsafe(24)
            try:
                with db() as con:
                    cur = con.execute(
                        "INSERT INTO booking (token, slot, name, practice, phone, email, topic, notes, website, visitor_tz, ip, created) "
                        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                        (token, slot, f["name"], f["practice"], f["phone"], f["email"], f["topic"], f["notes"], f["website"],
                         f["visitor_tz"], ip, dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")))
                    row = con.execute("SELECT * FROM booking WHERE id = ?", (cur.lastrowid,)).fetchone()
            except sqlite3.IntegrityError:
                return self.send(409, {"error": "That time was just taken. Please pick another one.", "field": "slot"})
        notify(row, "booked")
        self.send(200, {"ok": True, "token": token, "slot": slot, "when": describe(slot),
                        "utc": slot_dt(slot).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})


def contact(self, d):
    """Contact form: relayed to the office by e-mail and not stored here. 502 tells the page to fall back to the visitor's mail app."""
    f = {k: clean(d.get(k), n) for k, n in (("name", 80), ("practice", 120), ("phone", 40), ("email", 120), ("website", 200), ("topic", 60))}
    f["email"] = f["email"].lower()
    message = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]+", " ", str(d.get("message") or "")).strip()[:4000]
    if len(f["name"]) < 2:
        return self.send(422, {"error": "Please enter your name.", "field": "name"})
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", f["email"]):
        return self.send(422, {"error": "Please enter a valid e-mail address.", "field": "email"})
    text = "\n".join(["A request was sent from the contact form on rxmedicalweb.com.", "",
                      "Name:          " + f["name"], "Practice:      " + (f["practice"] or "-"), "Phone:         " + (f["phone"] or "-"),
                      "E-mail:        " + f["email"], "Website:       " + (f["website"] or "-"), "Interested in: " + (f["topic"] or "-"),
                      "", "Message:", message or "-", "", "Reply to this e-mail to answer them directly."])
    subject = f"{f['topic'] or 'Website inquiry'}: {f['practice'] or f['name']}"
    if not send_mail(subject, text, f["email"]):
        return self.send(502, {"error": "We could not send your request."})
    self.send(200, {"ok": True})


Handler.contact = contact


def cli(args):
    init()
    with db() as con:
        if args[0] == "list":
            rows = con.execute("SELECT * FROM booking WHERE status = 'booked' AND slot >= ? ORDER BY slot",
                               (dt.datetime.now(TZ).strftime("%Y-%m-%dT00:00"),)).fetchall()
            for r in rows:
                print(f"#{r['id']}  {describe(r['slot'])}  {r['name']} ({r['practice'] or 'no practice given'})  {r['phone']}  {r['email']}  [{r['topic']}]"
                      + (f"\n      {r['notes']}" if r["notes"] else ""))
            print(f"{len(rows)} upcoming call(s)")
        elif args[0] == "cancel" and len(args) > 1:
            print(con.execute("UPDATE booking SET status = 'cancelled' WHERE id = ?", (int(args[1]),)).rowcount, "cancelled")
        elif args[0] == "block" and len(args) > 1:
            con.execute("INSERT OR REPLACE INTO closed VALUES (?, ?)", (args[1], " ".join(args[2:])))
            print("closed", args[1])
        elif args[0] == "unblock" and len(args) > 1:
            print(con.execute("DELETE FROM closed WHERE day = ?", (args[1],)).rowcount, "reopened")
        else:
            print(__doc__)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli(sys.argv[1:])
    else:
        init()
        print(f"rxbooking listening on 127.0.0.1:{PORT}, database {DB}", flush=True)
        ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
