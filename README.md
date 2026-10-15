# Zaira Dafni website

A local static recreation of [www.zairadafni.gr](https://www.zairadafni.gr/), captured on 15 October 2026. The Greek content, original URLs, layout, images, and nine-image slideshow are preserved.

- [Repository](https://github.com/gregorynikolaidis/zairadafni-gr)
- [Personal GitHub project](https://github.com/users/gregorynikolaidis/projects/7)

## Run locally

Requires Python 3.9 or newer. Node/npm is optional and only provides command shortcuts. No package installation is needed.

```sh
npm run dev
# Or:
python3 -m http.server 4173 --bind 127.0.0.1 --directory site
```

Open http://127.0.0.1:4173/. Serve `site/` as the web root; opening HTML files directly or serving under a URL subdirectory will not resolve the root-relative base URL correctly.

```sh
npm run check  # Validate pages, links, gallery assets, and CSS references
npm run build  # Copy the static website to dist/
```

The Python equivalents are `python3 scripts/check.py` and `python3 scripts/build.py`. The build does not deploy anything or change the live domain.

## Where to edit

| Directory | Contents |
| --- | --- |
| `site/index.html` | Root homepage |
| `site/Αρχική/index.html` | Homepage at its original Greek URL; keep both homepages in sync |
| `site/<page>/index.html` | The other ten pages |
| `site/css/common.css` | Shared text styles |
| `site/css/1.css` through `11.css` | Original page-specific layout and styles |
| `site/gallery_gen/` | Original page images and gallery photographs |
| `site/js/` | Original browser scripts and slideshow |
| `docs/import-manifest.json` | Source URLs, capture time, transformations, file hashes, and unavailable source assets |

This is an editable baseline of the published site, not a redesign or a copy of its hosting backend. The original desktop layout and older jQuery/Bootstrap/Fancybox code are preserved. Below 1024px, `site/css/responsive.css` switches to a fluid layout with readable text, grouped course cards, scaled images and maps, and a collapsible Greek navigation menu. `site/js/responsive.js` controls the menu; links stay visible when JavaScript is unavailable. Both homepage URLs share the same markup.

Google Analytics and StatCounter are removed so local work does not send visits to the live site's analytics. Public email links are decoded to ordinary `mailto:` links. Open Sans is stored locally; unused builder font declarations and CSS images that already return 404 on the source are removed. The legacy key-dependent Google Maps script is replaced with a Google Maps embed at the original coordinates; the map still requires an internet connection. There is no contact form backend to recreate.

## Working together

Track work as issues in this repository and add those issues to the linked personal project. Use the project's Status field to show progress.

1. Create a short issue describing the goal and what counts as done.
2. Create a branch such as `fix/contact-copy` or `feature/mobile-layout`.
3. Make the change and run the link check. Read affected pages in the browser.
4. Push the branch and open a pull request for the other person to review.
5. Merge after review; GitHub Actions publishes `main` to the shared GitHub Pages preview once Pages is enabled.

## Preview and production releases

- **Pull requests and branch pushes:** `Check website` validates the source and both the domain-root and preview builds.
- **Pushes to `main` (including merged PRs):** `Deploy preview to GitHub Pages` builds and publishes the shared preview. It can also be run manually from `main` in Actions.
- **Tags beginning with `v`, such as `v1.0.0`:** `Prepare production release (deployment TODO)` builds the tagged revision at the domain root and uploads a downloadable artifact. It does not deploy to production yet; the run shows a warning and summary explaining the missing setup.

To enable the preview, open repository **Settings → Pages → Build and deployment → Source** and choose **GitHub Actions**. Because this repository is private, the account needs a GitHub plan that supports Pages for private repositories. The preview is normally publicly accessible even though the repository is private.

The expected preview URL is https://gregorynikolaidis.github.io/zairadafni-gr/. Keep the production domain out of this repository's Pages custom-domain setting: Pages is the shared preview, while production will use a separate deployment destination. Configure the `github-pages` environment to allow deployments from `main` only.

The preview workflow reads its base path from GitHub Pages. To check the usual project path locally:

```sh
python3 scripts/build.py --base-path /zairadafni-gr/
python3 scripts/check.py --directory dist --base-path /zairadafni-gr/
```

Builds recreate `dist/` and adjust HTML and CSS paths there; source files under `site/` keep their domain-root paths. The default `npm run build` still produces a domain-root production build.

**Production TODO:** confirm the hosting provider, upload method (for example SFTP or a hosting API), destination directory, and required GitHub secrets. Then extend the tag workflow to deploy the artifact it already builds. Until that is configured, a successful tag run means the release files were prepared, not that production was updated.

Kostas's GitHub account is pending. After he creates it, invite the exact username through repository **Settings → Collaborators** and project **Settings → Manage access**. Repository and project permissions are separate. Give project Write access for managing tasks. He must accept the invitation before the private resources are available. Do not share account passwords or tokens.

## Refreshing the imported baseline

`python3 scripts/import_site.py` downloads the public site again and overwrites imported files. Run it only on a dedicated branch after committing your work; it can replace local edits. It is not part of normal development or the build. It discovers the 11 sitemap pages and their assets, applies the documented local transformations, and records the result in the import manifest.

Content and asset rights remain with their original owners. No new license is assigned to the imported material.
