# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Personal site / blog at `westerweel.work`. Static site built with **Hugo** + the **PaperMod** theme. No Node, no build pipeline beyond `hugo`. Bilingual (NL default, EN secondary). Hosted on Cloudflare Pages; output is plain static HTML so a self-hosted Caddy fallback is also viable. Owner explicitly values "boring and auditable" — see the comment in `hugo.toml` near `[params]`.

## Commands

```bash
# Local dev server (drafts included)
hugo server -D                       # → http://localhost:1313

# Production build
hugo --gc --minify                   # output in public/

# New post (NL and EN are separate files, same date prefix)
hugo new content/nl/posts/YYYY-MM-DD-titel.md
hugo new content/en/posts/YYYY-MM-DD-title.md

# Update the PaperMod theme submodule
git submodule update --remote themes/PaperMod

# Smoke test (run after any layout or content-frontmatter change)
bash scripts/test-site.sh
```

Hugo version is pinned to **0.146.0 extended** (Cloudflare Pages env `HUGO_VERSION=0.146.0`, same version in `.github/workflows/deploy-pages.yml.example`). PaperMod requires ≥ 0.146.0 (uses Hugo's new `_partials/` layout lookup). Older Hugo versions fail with `partial "head.html" not found`.

After a fresh clone, theme submodule must be initialized: `git submodule update --init --recursive`. Without it, `hugo` fails because `themes/PaperMod/` is empty.

## Architecture

**Content layout — two parallel trees, one per language.** `hugo.toml` declares `[languages.nl]` with `contentDir = "content/nl"` and `[languages.en]` with `contentDir = "content/en"`. NL is default and rendered at the site root (`defaultContentLanguageInSubdir = false`); EN lives under `/en/`. Each language has its own `_index.md`, top-level pages (`about.md`, `diensten.md` vs `services.md`), and `posts/` directory. Menus are defined per-language in `hugo.toml` — adding a new top-level section means editing both `[[languages.nl.menu.main]]` and `[[languages.en.menu.main]]` blocks, plus creating the matching content file in each tree.

**Theme is a git submodule, not vendored.** `themes/PaperMod/` is pinned via `.gitmodules`. Do not edit files inside `themes/PaperMod/` — those changes get blown away on submodule updates. Customization goes in `layouts/` at the repo root, which overrides theme templates by path. The `[params]` block in `hugo.toml` is the supported customization surface and is intentionally minimal.

**Partial overrides go in `layouts/_partials/`, not `layouts/partials/`.** PaperMod 0.146+ uses Hugo's new `_partials/` lookup. Files in the old `partials/` location are silently ignored by the theme — this is the bear-trap that hid the cookie banner after the theme bump. Current overrides:

- `layouts/_partials/extend_footer.html` — adds the cookie-banner easter egg (extension point provided by PaperMod, not a fork).
- `layouts/_partials/extend_head.html` — Person JSON-LD on home + about pages, with `sameAs` to GitHub/LinkedIn. SEO entity-recognition signal. Extension point provided by PaperMod, not a fork.
- `layouts/_partials/header.html` — full copy of the theme header with one block patched so the language toggle links to the current page's translation (`.Translations`) instead of the language home (`site.Home.Translations`). Re-sync when bumping the theme submodule.

**Archetype drives new-post frontmatter.** `archetypes/posts.md` is the template used by `hugo new content/...`. Posts are `draft: true` by default; flip to `false` to publish.

**Static assets and platform config live in `static/`.** Cloudflare Pages reads `_headers` and `_redirects` directly from the built output, so those files are copied verbatim from `static/`. Security headers (X-Frame-Options, etc.) are set there, not in Hugo config.

**Deployment.** Primary path is Cloudflare Pages connected to the GitHub repo; build is `hugo --gc --minify`, output is `public/`. `.github/workflows/deploy-pages.yml.example` is a parked GitHub-Pages fallback — rename to `.yml` if hosting flips. Cloudflare builds happen automatically on push to `main`; there is no local CI to run.

## Things to know before editing

- **Owner-owned project.** Per the user's global rules, this project must maintain a `CHANGELOG.md` with dated entries for every session that changes behavior. There isn't one yet — create it on first substantive change.
- **README is the source of truth for setup/hosting.** Keep it in sync with any change to build commands, Hugo version, or hosting topology in the same commit.
- **Every content file needs a translation.** NL ↔ EN parity is enforced by the smoke test: each `content/**/*.md` must declare a non-empty `translationKey`, and the set of keys in `content/nl` must equal the set in `content/en`. Adding a post in one language without the other fails CI-like checks.
- **Never set `url:` in frontmatter on both languages of the same logical page.** Because NL renders at root (`defaultContentLanguageInSubdir = false`) and EN at `/en/`, an `url: "/foo/"` in both files makes them collide at `/foo/` — Hugo silently keeps one and drops the other, so `/en/foo/` 404s. Either omit the override entirely (let Hugo derive paths from filenames) or set `url:` only on the NL file.
- **Pair translations with `translationKey:` in frontmatter.** Because NL/EN file basenames differ (`diensten.md` vs `services.md`), Hugo can't auto-pair them. Without a shared `translationKey`, the header lang toggle, the per-page `Vertalingen:` link, and the SEO `<link rel=alternate hreflang>` all silently default to the language home.
- **`enableGitInfo = true`** in `hugo.toml` — Hugo reads commit timestamps for `lastmod`. Shallow clones (`fetch-depth: 1`) break this; the example workflow uses `fetch-depth: 0` deliberately.
- **`unsafe = true`** under `[markup.goldmark.renderer]` means raw HTML in Markdown is rendered. Treat post content as trusted (owner-authored only).
