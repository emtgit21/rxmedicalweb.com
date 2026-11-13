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

1. Push to `main` on GitHub.
2. In cPanel → Git Version Control → rxmedicalweb.com → Manage → Pull or Deploy: click **Update from Remote**, then **Deploy HEAD Commit**.
3. `.cpanel.yml` copies the site into `/home/itjfn6oc46op/public_html/rxmedicalweb.com`.

A new top-level folder or file must be added to the copy task in `.cpanel.yml`. `./deploy.sh` is the alternative: it uploads every tracked file through the cPanel API. `src/` is harmless on the server but does not need to be there.

## Contact form

The site has no server-side code. The contact form opens the visitor's e-mail app with the details filled in. To collect submissions directly, point the form at a form handler or a CRM endpoint in `build_contact()`.
