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
```

Hugo version is pinned to **0.139.0 extended** (Cloudflare Pages env `HUGO_VERSION=0.139.0`, same version in `.github/workflows/deploy-pages.yml.example`). Use that version when reproducing build issues locally.

After a fresh clone, theme submodule must be initialized: `git submodule update --init --recursive`. Without it, `hugo` fails because `themes/PaperMod/` is empty.

## Architecture

**Content layout — two parallel trees, one per language.** `hugo.toml` declares `[languages.nl]` with `contentDir = "content/nl"` and `[languages.en]` with `contentDir = "content/en"`. NL is default and rendered at the site root (`defaultContentLanguageInSubdir = false`); EN lives under `/en/`. Each language has its own `_index.md`, top-level pages (`about.md`, `diensten.md` vs `services.md`), and `posts/` directory. Menus are defined per-language in `hugo.toml` — adding a new top-level section means editing both `[[languages.nl.menu.main]]` and `[[languages.en.menu.main]]` blocks, plus creating the matching content file in each tree.

**Theme is a git submodule, not vendored.** `themes/PaperMod/` is pinned via `.gitmodules`. Do not edit files inside `themes/PaperMod/` — those changes get blown away on submodule updates. Customization goes in `layouts/` at the repo root (currently empty), which overrides theme templates by path. The `[params]` block in `hugo.toml` is the supported customization surface and is intentionally minimal.

**Archetype drives new-post frontmatter.** `archetypes/posts.md` is the template used by `hugo new content/...`. Posts are `draft: true` by default; flip to `false` to publish.

**Static assets and platform config live in `static/`.** Cloudflare Pages reads `_headers` and `_redirects` directly from the built output, so those files are copied verbatim from `static/`. Security headers (X-Frame-Options, etc.) are set there, not in Hugo config.

**Deployment.** Primary path is Cloudflare Pages connected to the GitHub repo; build is `hugo --gc --minify`, output is `public/`. `.github/workflows/deploy-pages.yml.example` is a parked GitHub-Pages fallback — rename to `.yml` if hosting flips. Cloudflare builds happen automatically on push to `main`; there is no local CI to run.

## Things to know before editing

- **Owner-owned project.** Per the user's global rules, this project must maintain a `CHANGELOG.md` with dated entries for every session that changes behavior. There isn't one yet — create it on first substantive change.
- **README is the source of truth for setup/hosting.** Keep it in sync with any change to build commands, Hugo version, or hosting topology in the same commit.
- **NL is the default locale.** When adding content, NL is mandatory; EN is optional but the menu structure assumes parity. A missing EN counterpart shows up as a broken language switcher entry.
- **`enableGitInfo = true`** in `hugo.toml` — Hugo reads commit timestamps for `lastmod`. Shallow clones (`fetch-depth: 1`) break this; the example workflow uses `fetch-depth: 0` deliberately.
- **`unsafe = true`** under `[markup.goldmark.renderer]` means raw HTML in Markdown is rendered. Treat post content as trusted (owner-authored only).
