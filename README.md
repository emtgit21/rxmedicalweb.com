# rxmedicalweb.com

Website for Rx Medical Web: a static site, generated from `src/` and deployed to GoDaddy cPanel.

## Editing

- Text for every page lives in `src/pages.py` (services, testimonials, about, articles).
- Layout and shared header/footer live in `src/build.py`.
- Styles and behavior: `assets/site.css`, `assets/site.js`.
- Photos and the hero video: `assets/img/`, `assets/video/` (generated with xAI Grok Imagine; originals are archived outside the repo).
- Logo, testimonial photos and portfolio screenshots stay in `wp-content/uploads/` so their old URLs keep working.

After any change run:

    python3 src/build.py

It rewrites every `index.html` and `sitemap.xml`. Commit the generated files too: the host serves them as they are.

To preview locally: `python3 -m http.server 8765` and open http://127.0.0.1:8765/.

To add a service, add one entry to `SERVICES` in `src/pages.py`. It appears in the menu, the home page index, the footer, the contact form and the sitemap.

## Deployment

The site is served by nginx on the DigitalOcean droplet `rxmedicalweb` (134.209.164.194, NYC3).

Push to `main` and it is live within two minutes: a cron job on the droplet (`/etc/cron.d/rxmedicalweb-pull`) resets `/var/www/rxmedicalweb.com` to `origin/main`. Never edit files on the server; they are overwritten.

- nginx config: `/etc/nginx/sites-available/rxmedicalweb.com` (blocks `.git`, `src/`, `dev/`)
- HTTPS: Let's Encrypt through certbot, renewed by `certbot.timer`
- DNS: A record at GoDaddy points to the droplet

`.cpanel.yml` and `deploy.sh` belong to the old GoDaddy cPanel hosting and are no longer used.

## Contact form

The site has no server-side code. The contact form opens the visitor's e-mail app with the details filled in. To collect submissions directly, point the form at a form handler or a CRM endpoint in `build_contact()`.
