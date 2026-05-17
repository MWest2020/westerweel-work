# Changelog

All notable changes to this site. Dates are `YYYY-MM-DD`.

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
