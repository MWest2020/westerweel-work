# Changelog

All notable changes to this site. Dates are `YYYY-MM-DD`.

## 2026-05-17 (fourth pass — first real post)

### Added
- `content/nl/posts/2026-05-17-claude-code-via-mobiel.md` (NL, draft).
  Three options for using Claude Code from a phone: Anthropic's
  `/remote-control` pairing, classic SSH + tmux on own iron, and
  third-party wrappers (Happy CLI). Written as draft pending owner
  verification of the option-1 specifics (`/remote-control` command,
  mobile app "Code tab" naming). EN translation deferred.

## 2026-05-17 (third pass — editorial)

### Changed
- `diensten.md` + `services.md`:
  - Dropped `(kubeadm, k3s, managed)` parenthetical from the Kubernetes
    bullet. It alienated non-tech clients and read as fluff to the ones
    who would have recognised it.
  - Added a WBSO bullet under funding work: "technische onderbouwing
    die de RVO-toets doorstaat". Renamed section heading from
    "subsidie-trajecten" → "subsidies" (NL) and "grant work" →
    "funding" (EN) to fit WBSO (a tax credit, not a grant).
  - Replaced the vague "Begin altijd met een gesprek — dan een spec,
    dan pas code." with "Ik denk, ik test, ik doe. Voor code:
    spec-driven development." (and the EN parallel). Describes how
    the work actually happens, not a sales-y intro.
- `about.md` (NL + EN):
  - Removed "Sinds 2026 onafhankelijk, als DevOps-consultant." /
    "Independent DevOps consultant since 2026." — redundant given
    the rest of the page.
  - "Open source, open standaarden, open haven." → "Open source."
    Same for EN. "Open haven" was meaningless; "open source" already
    implies more than a public GitHub repo.

### Deferred
- Tender / public-procurement bid work as a service line — left out
  pending confirmation that this is work the owner does. Easy to add
  as a separate bullet under the funding section.

## 2026-05-17 (second pass)

### Fixed
- `/en/about/` returned 404. Same root cause as the earlier services
  bug: `nl/about.md` AND `en/about.md` both carried `url: "/about/"`,
  causing a path collision that dropped the EN copy. Removed the EN
  override and added matching `translationKey: "about"` to both files.
- Header language toggle linked to `/en/` (language home) regardless of
  the current page. PaperMod's `_partials/header.html` hard-codes
  `site.Home.Translations`; overridden at `layouts/_partials/header.html`
  to prefer the current page's `.Translations`, with a fallback to the
  home for pages without a translation (tag pages, etc.). The override
  is a verbatim copy of the PaperMod file with one block patched —
  re-sync when bumping the PaperMod submodule.
- `layouts/partials/extend_footer.html` moved to
  `layouts/_partials/extend_footer.html`. PaperMod 0.146+ uses Hugo's
  new `_partials/` lookup; the old location was silently ignored, which
  is why the cookie banner disappeared after the previous theme bump.

### Changed
- Bumped the cookie-banner `localStorage` key from `cookieAck` to
  `cookieAck-v2` so previously-dismissed visitors (including the owner)
  see the typed banner again after the failed shell experiment.

### Added
- `scripts/test-site.sh` — bash smoke test. Builds the site, asserts
  expected pages render, that hreflang pairs are wired, that the
  header lang-menu points at translations (not the language home),
  and that the cookie banner partial is present on both home pages.
  Run with `bash scripts/test-site.sh`. Exits non-zero on first
  failure. Intended as a pre-push check.

## 2026-05-17

### Reverted
- The interactive "visitor shell" expansion of the cookie easter egg
  (commit `4efcfac`) caused the page to freeze in production. Reverted
  to the simple typed-out banner from `a338621`.

### Fixed
- Language switcher between `/diensten/` and `/services/` returned 404.
  Two problems: (1) the pages had no shared `translationKey`, so
  PaperMod couldn't pair them as translations; (2) `services.md`
  carried `url: "/services/"` which forced the EN page to render at
  root `/services/` instead of `/en/services/`, while the menu link
  resolved to `/en/services/`. Added matching `translationKey: "services"`
  to both files and dropped the URL override.

### Changed
- `content/nl/diensten.md`: tightened wording per editorial review.
  Kubernetes line now lists concrete distros, Compliance section drops
  ISO 27001 framing in favour of approach-based bullets, "stack"
  swapped for "praktijk" (audit audience).
- `content/en/services.md`: synced to mirror the new NL content.
- `hugo.toml`: moved `homeInfoParams` from global `[params]` into
  per-language `[languages.<lang>.params.homeInfoParams]` so the home
  intro flips with the language switcher.

## 2026-05-16

### Added
- `layouts/partials/extend_footer.html` — terminal-style "cookies" easter egg
  shown once per browser, dismissable via × or `Esc`, persisted in
  `localStorage` under `cookieAck`. NL/EN aware via `<html lang>`.
  Not a consent dialog — the site sets no tracking cookies and loads no
  third-party trackers; this is purely an easter egg that states that fact.
- `CLAUDE.md` — guidance for Claude Code working in this repo.

### Changed
- `.gitignore`: added defense-in-depth patterns for secrets (`.env`,
  `.env.*`, `*.pem`, `*.key`, `*_rsa`, `*.crt`). No such files exist
  today; this is preventative.
- Bumped pinned Hugo from `0.139.0` → `0.146.0` in `README.md` and
  `.github/workflows/deploy-pages.yml.example`. PaperMod (current submodule
  HEAD) now requires Hugo ≥ 0.146.0 because it migrated to Hugo's new
  `_partials/` layout lookup. Building with 0.139.0 fails with
  `partial "head.html" not found`.

### Action required (outside the repo)
- Update **Cloudflare Pages** project env var `HUGO_VERSION` from `0.139.0`
  to `0.146.0` (Dashboard → Pages → project → Settings → Environment
  variables). Without this the production build will fail / serve stale.
- Attach custom domains `westerweel.work` and `www.westerweel.work` to the
  Cloudflare Pages project (Dashboard → Pages → project → Custom domains).
  DNS records are created automatically.
