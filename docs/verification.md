# Recreation verification — 15 October 2026

Source: https://www.zairadafni.gr/

- Imported all 11 sitemap pages, plus `/` as the homepage alias, into 86 files.
- `npm run check` passed: 12 HTML documents and 289 local references.
- `npm run build` passed: static output created in `dist/`.
- Browser traversal passed for all 11 linked pages: no broken images, no local HTTP errors, and no JavaScript page errors during that traversal.
- Homepage slideshow Next changed from the first photograph to the second. Clicking the image opened the Fancybox lightbox; Escape dismissed it.
- The contact map embed loaded Google Maps controls at the original coordinates. It is the one external content dependency.
- Desktop checked at 1440px; mobile checked at 390px. The original desktop-width layout remains; the mobile document width measured 988px. This recreation does not add a responsive redesign.
- Compared the local homepage with a live-site screenshot. Original colors, placements, text, imagery, and tight heading line spacing remain. Gallery image and analytics counter can differ: the gallery rotates, and analytics are removed locally.

The import manifest records unavailable source assets (including unused builder/legacy IE graphics and a missing vintage footer). CSS references to these already-missing images were removed. No replacement images were invented.

The local copy is separate from the existing hosting. This task does not change domain, DNS, live hosting, or deploy a replacement site. Older browser libraries are kept for fidelity and should be reviewed before a future production rebuild.
