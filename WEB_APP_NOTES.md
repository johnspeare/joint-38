# Building the FD SOGs web app (offline, installable)

Handoff notes for building the "eventually: a web version (HTML site)" deliverable
mentioned in `handoff.md` §1. This describes the pattern to follow, based on a
working reference app already built the same way for a different department's
EMS protocols, plus how it adapts to this project's specific content.

## Reference implementation — read this first

`/Users/john/Dropbox/emt-dev/wa-protocols/` is a complete, shipped, working
example of this exact kind of app (Washington State EMS protocols, built from
a PDF, converted into an installable offline PWA). Read these files directly
before writing any code:
- `wa-protocols/index.html` — full structure, styles, data shape, logic in one file
- `wa-protocols/sw.js` — the service worker (offline caching strategy)
- `wa-protocols/manifest.json` — PWA manifest
- `wa-protocols/INSTALL.md` — end-user install instructions (per platform)

That app is a **quick-reference card deck**: short, independent protocol
entries, filtered/searched, opened one at a time in a modal. FD SOGs is a
**linear policy manual** (32 numbered sections read mostly in order, with
tables, an org-chart image, and fillable appendix forms) — so borrow the
mechanics (single file, PWA shell, service worker, responsive CSS) but adapt
the layout: a table-of-contents + collapsible sections + in-page search,
rather than a card grid with filter tabs. This matches what was actually
requested when the reference app's own project was kicked off ("Table of
contents with jump links, Collapsible protocol sections") — same brief,
just apply the TOC/collapsible half more literally here since the source
document is a manual, not a stack of independent protocols.

## Architecture: one file, no build step

Same rule as the reference app: don't add a framework, bundler, or SSG. One
`index.html` (structure + CSS + data + JS) plus three sidecar files
(`manifest.json`, `sw.js`, an icon). This has to work fully offline after
first load, so keep the file count small and the precache list explicit.

Do **not** touch `build_sog_pdf.py` or the PDF pipeline — the web app is a
new, separate deliverable built from the same source (`FD SOGs.md`), not a
replacement. Both consume the markdown; neither depends on the other.

## Step 1: turn `FD SOGs.md` into structured section data

`FD SOGs.md` is already clean, hierarchical markdown (1 H1, 32 H2, 86 H3, 41
H4 — see `handoff.md` §2 for the exact structure). Parse it into an ordered
array of section records embedded in `index.html`, mirroring the existing
heading hierarchy instead of inventing a new one:

```js
const SECTIONS = [
  {
    id: 'chain-of-command',           // slug from the heading, for jump links (#chain-of-command)
    level: 2,                          // 2/3/4, mirrors the source H2/H3/H4 — drives TOC indent + collapsible nesting
    title: 'Chain of Command',
    tags: 'chain of command org chart chief captain lieutenant', // plain string, substring-matched by search
    body: `<img src="assets/chain-of-command.svg" alt="Chain of Command organizational chart"> ...`,
  },
  // ... one record per H2/H3/H4, in document order
];
```

Notes specific to this content:
- Convert markdown → HTML with a real converter (`markdown` in Python, same
  library already used by `build_sog_pdf.py`, or any markdown-to-HTML pass)
  rather than hand-authoring HTML fragments like the reference app does —
  this source is long-form prose and tables, not short bulleted clinical
  entries, so a faithful mechanical conversion is the right call here
  (unlike the reference app, where hand-converting to compact styled HTML
  materially improved usability). Spot-check the converted output against
  `FD SOGs.md` for the GFM pipe tables in Appendix C and the mission
  statement table — these are the two places conversion is most likely to
  go wrong.
- `id` should be a stable slug derived from the heading text (kebab-case,
  same scheme `build_sog_pdf.py`'s TOC/anchor generation likely already
  uses — check its output so anchors match between the PDF and the web
  version where practical).
- Keep H2/H3/H4 as a `level` field rather than flattening — the UI needs it
  to render a nested, indented TOC and to nest `<details>` elements
  correctly (an H3 collapses inside its parent H2, not as a sibling).
- The org chart: use `FD-SOGs-assets/chain-of-command.svg`, not the `.png`.
  The PNG only exists because WeasyPrint (the PDF pipeline) can't render
  SVG reliably — see `handoff.md` §9. Browsers handle SVG natively, so the
  web app doesn't inherit that workaround; reference the SVG directly and
  ship it as a precached asset.
- Appendices C–E are fillable forms (medical questionnaire, fit-testing
  record, injury report). Render them as read-only reference in the app —
  don't build interactive form state/persistence unless specifically asked;
  that's a different feature, not part of "convert the manual to a PWA."

## Step 2: render as TOC + collapsible sections + search

- A persistent (or drawer-toggled on mobile) table of contents built from
  the `SECTIONS` array, indented by `level`, each entry an anchor link.
- Each section rendered as a `<details>`/`<summary>` (or an equivalent
  custom collapsible) so the whole manual can be scanned collapsed and
  expanded on demand — H3/H4 as nested `<details>` inside their parent H2.
- A single search input that filters by substring match against
  `title + tags` (or `title + body text`, given how long-form this content
  is) and, on match, auto-expands and scrolls to the matching section(s) —
  don't hide non-matching sections entirely the way the reference app's
  card filter does; a manual's context (which chapter a match lives under)
  matters more than in a flat protocol list.
- Deep links: read `location.hash` on load, expand and scroll to the
  matching section id. Same mechanism as the reference app's
  `openProto(id)` / `popstate` handling, just targeting scroll+expand
  instead of opening a modal.
- At this content size (2,949 source lines, ~110 headings) a single
  render-everything-up-front approach is fine — no virtualization needed.

## Step 3: responsive CSS

Reuse the reference app's approach directly:
- CSS custom properties for all colors in `:root`, overridden in a single
  `@media (prefers-color-scheme: dark)` block — free dark mode, no
  per-component duplication.
- For brand consistency with the existing PDF (`build_sog_pdf.py`), use its
  color palette as the light-mode tokens: heading/accent `#8B0000` (dark
  red — the "fire-dept convention" called out in `handoff.md` §6.11),
  Arial/Helvetica Neue/system-ui font stack, body text `#111`, secondary
  text `#555`/`#777`.
- Mobile-first layout, single column, widening only if a desktop TOC-sidebar
  layout is wanted at wider breakpoints (e.g. `min-width: 900px` moves the
  TOC from a drawer to a persistent left rail).
- `env(safe-area-inset-*)` padding for notch/home-indicator clearance when
  installed fullscreen on iOS.
- Inputs at `font-size: 16px` minimum to prevent iOS Safari auto-zoom on
  focus.
- Sticky header containing the search input and a TOC-toggle button.

## Step 4: PWA manifest + icon

No app icon exists yet in this project — one needs to be created (512×512
PNG, `purpose: "any maskable"`, real padding so it survives circular/squircle
masking). A fire-dept badge/shield motif in the `#8B0000` accent would match
the PDF branding; check with the department if they have an existing logo
before designing one from scratch.

```json
{
  "name": "Joint Fire Protection District 3 & 8 — SOGs",
  "short_name": "FD 3&8 SOGs",
  "description": "Standard Operating Guidelines — Joint Fire Protection District 3 & 8",
  "start_url": "./index.html",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#8B0000",
  "orientation": "portrait-primary",
  "categories": ["reference"],
  "icons": [
    { "src": "icon.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable" }
  ]
}
```

Plus the standard iOS meta tags in `<head>` (copy verbatim from
`wa-protocols/index.html`'s `<head>`): viewport, `theme-color`,
`apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style`,
`apple-mobile-web-app-title`, `<link rel="manifest">`, `<link
rel="apple-touch-icon">`.

## Step 5: service worker (offline)

Copy `wa-protocols/sw.js` near-verbatim; only the cache name and precache
list change:

```js
const CACHE = 'fd-sogs-v1';
const PRECACHE = ['./index.html', './manifest.json', './icon.png', './assets/chain-of-command.svg'];
```

Keep the same strategy — it's the correct one for this use case too:
- **Network-first for the HTML document** — always fetch fresh when online
  (so policy updates reach members immediately, no version-bump dance),
  fall back to cache when offline.
- **Cache-first for static assets** (icon, manifest, the org-chart image) —
  these change rarely.
- Precache on `install` with `self.skipWaiting()`; delete stale cache
  versions on `activate`; `self.clients.claim()`.
- Bump the `CACHE` version string only when the *set* of precached files
  changes, not for ordinary content edits to `FD SOGs.md`.

Register at the bottom of `index.html`:
```js
if ('serviceWorker' in navigator) navigator.serviceWorker.register('./sw.js').catch(()=>{});
```

## Step 6: deploy and hand end users install instructions

Deploy as static files to wherever the department can host (GitHub Pages,
same as the reference app, is the simplest zero-cost option if there's a
GitHub org/repo for the district; otherwise any static host works).

Write an `INSTALL.md` (or an in-app help panel) with these per-platform
steps — adapted from `wa-protocols/INSTALL.md`:

> ## Installing the FD 3&8 SOGs App
>
> Open **[deployed URL]** in your browser, then follow the steps for your device:
>
> | Platform | Browser | Steps |
> |----------|---------|-------|
> | iPhone / iPad | Safari | Tap the **Share** button (⬆ box with arrow) → scroll down → tap **Add to Home Screen** → tap **Add** |
> | Android | Chrome | Tap the **⋮** menu (top right) → tap **Add to Home screen** → tap **Add** |
> | Android | Firefox | Tap the **⋮** menu → tap **Install** |
> | Mac / Windows | Chrome or Edge | Click the **install icon** (⊕) in the address bar → click **Install** |
> | Mac / Windows | Firefox | No install prompt — bookmark the page; works offline as a regular tab |
>
> **The app works fully offline after the first visit.** Load it once with a
> normal internet connection (station wifi, cell signal) so it can cache the
> full manual — after that it opens and works with no connection at all,
> including on a rig with no signal.
>
> **Getting updates:** whenever the SOGs are revised and republished at the
> same URL, the app fetches the latest version automatically the next time
> you open it with a connection. No reinstall needed. If you're ever unsure
> you have the latest version, open the app once while online.

No further end-user *configuration* is needed for a single-department app —
there's no login, no settings, no per-user state. (The reference app has an
unused `DEPARTMENTS` config hook for restricting which entries show per
department — not applicable here since this app serves one department; skip
building anything like it unless a future requirement calls for
multi-department variants of the same manual.)

## Checklist

1. Convert `FD SOGs.md` → an ordered `SECTIONS` array (`id`, `level`, `title`,
   `tags`, `body` as converted HTML), in document order, matching the
   existing H2/H3/H4 hierarchy.
2. Spot-check conversion accuracy against the source, especially the GFM
   tables (mission statement, Appendix C questionnaire).
3. Build `index.html`: CSS custom properties + dark-mode override
   (`#8B0000` accent to match the PDF), responsive layout, sticky header
   with search + TOC toggle, nested collapsible sections, hash-based deep
   linking to a section.
4. Reference `FD-SOGs-assets/chain-of-command.svg` (not the PNG) inline.
5. Create a 512×512 maskable app icon; add `manifest.json` and iOS meta tags.
6. Add `sw.js` (network-first HTML, cache-first assets); register it.
7. Deploy to a static host.
8. Write `INSTALL.md` using the per-platform steps above with the real
   deployed URL filled in.
9. Test offline: load once online, enable airplane mode, confirm the full
   manual (including the org chart image) still renders and search still
   works.
10. Whenever `FD SOGs.md` is revised, re-run the extraction step (1–2) and
    redeploy — there's no automated sync between the markdown and the
    embedded `SECTIONS` array, same as the reference app's manual-update
    workflow.
