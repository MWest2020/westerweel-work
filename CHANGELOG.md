# Changelog

All notable changes to this site. Dates are `YYYY-MM-DD`.

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
