# space-studios-site

Source for [spacestudios.us](https://spacestudios.us). Static site, GitHub Pages.

## Stack
- Plain HTML + Tailwind CDN. No build step.
- Hosted on GitHub Pages.

## Local preview
Open `index.html` in a browser. That's it.

## Deploy
Push to `main`. GitHub Pages serves the root.

## Structure
- `index.html` — single-page landing (hero, services, approach, founder, book-a-call).
- `CNAME` — custom domain (activated at DNS cutover, not before).

## Placeholders to replace
- **Book-a-call CTA**: wired to `https://calendar.app.google/sbbST69RKQumuCvZ9` (Google Calendar appointment schedule).
- **LinkedIn URL** `https://www.linkedin.com/in/william-bransford` — best guess; LinkedIn API was day-capped when building, couldn't resolve the real vanity slug. Verify and update two lines in `index.html`.
- **Contact email** `william@spacestudios.us` — confirmed live (Workspace send-as verified 2026-04-20).
