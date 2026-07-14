# Changelog

All notable changes to this site. Dates are `YYYY-MM-DD`.

## 2026-07-14 (twelfth pass — living-documentation post)

### Added
- Nieuwe post **"Documentatie die liegt is erger dan geen documentatie"** (NL)
  / **"Documentation that lies is worse than no documentation"** (EN),
  `translationKey: living-docs-gates`, gepubliceerd (`draft: false`). Essay over levende
  documentatie: docs-contract (owner + last_reviewed, docs in dezelfde PR),
  pre-push/CI-gates (contract-check, uitvoerbare doc-claims, freshness-gate,
  linkcheck, automatische drift-issues) en een read-only MCP-server die agents
  grondwaarheid mét herkomst geeft. Bewust geanonimiseerd: geen werkgever-,
  klant- of platformnamen. Gaat live bij de eerstvolgende push naar main.

## 2026-06-18 (eleventh pass — workshops / slidedecks)

### Added
- Nieuwe sectie **workshops** (NL + EN), `translationKey: workshops`.
  Tweetalige overzichtspagina (`/workshops/`, `/en/workshops/`) met
  menu-entries in beide talen (`hugo.toml`, `weight = 25`, tussen
  blog/diensten en about). (In dezelfde sessie eerst kort "presentaties"
  genoemd, daarna hernoemd naar "workshops".)
- Eerste deck: **Docker — van image naar registry**, een self-contained
  reveal-style HTML-presentatie (CRT/phosphor-stijl, keyboard- + tap-navigatie)
  op `static/slides/docker-101/index.html` → serveert verbatim op
  `/slides/docker-101/`. Decks staan bewust in `static/` (niet als Hugo-content):
  Cloudflare/Caddy serveren ze byte-voor-byte, dus online identiek aan lokaal
  openen. De overzichtspagina is de tweetalige content-laag; de decks zelf
  vallen daardoor buiten de NL/EN-pariteitscheck (deck-inhoud kan eentalig zijn).

### Notes
- Het Docker-deck laadt JetBrains Mono via de Google Fonts CDN — de enige
  externe afhankelijkheid. Valt netjes terug op `ui-monospace` als het CDN
  geblokkeerd/offline is. Kan op verzoek gevendord worden voor volledig
  zelfstandig + privacyvriendelijk ("boring & auditable").

## 2026-06-17 (tenth pass — post over output-veiligheid vs datavertrouwelijkheid)

### Added
- Nieuwe post (NL + EN, `translationKey: output-safety-vs-data`), **gepubliceerd**
  (`draft: false`): "Ricine breekt je model. Je data niet." / "Ricin breaks
  your model. Not your data." Kern: het misverstand dat een model dat ricine
  weigert (output-veiligheid / guardrails) ook je data beschermt
  (datavertrouwelijkheid) — twee losse mechanismen. Behandelt pretraining vs
  post-training, de twee-assen-framing (as 1 = belandt data in de *gewichten*,
  as 2 = verlaat data je *pand*), fine-tuning vs RAG vs in-context tegen die
  assen, inference ≠ training maar logging wél, tier/ZDR/DPA/DPIA, het
  Shadow-AI-risico van consumer-accounts, de Reddit-zaak (memorisatie), de
  NYT-retentie-uitspraak (Enterprise/ZDR/EU vielen erbuiten; bevel inmiddels
  grotendeels teruggedraaid), en lokale modellen als de echte ontsnapping.
- Bronlinks toegevoegd: Anthropic privacy + Constitutional Classifiers
  (paper + explainer), OpenAI enterprise-privacy + NYT-respons, secureprivacy.ai
  (feedbackknop-opt-out), bbycroft.net/llm + 3Blue1Brown.
- Gebaseerd op een geanonimiseerd klantgesprek (gereguleerde sector), met
  expliciete toestemming. Anonimisering aangescherpt in de herschrijving —
  geen herleidbare details.
- Begeleidende LinkedIn-post (kortere variant, links in eerste reactie)
  los aangeleverd buiten de repo.

### Verified
- `scripts/test-site.sh`: 45 passed, 0 failed (NL↔EN parity + hreflang).

## 2026-06-15 (ninth pass — post over gecureerde skillsets)

### Added
- Nieuwe post (NL + EN, `translationKey: curated-skillsets`):
  "Gecureerde, deelbare skillsets voor AI-agents" /
  "Curated, shareable skillsets for AI agents". Kern: een agent-skill is
  maar een markdown-bestand, dus het bestaansrecht zit in de curatie —
  draft → judge → promote → refine, ondertekend met provenance — en in
  deelbare skillsets (tags als query) met een read-only MCP-server als
  toekomstplan. Concreet voorbeeld: de `owasp-security`-skill door de
  pipeline gehaald (judge 0.87, herkomst-as gerefined naar 0.85).
- Gepubliceerd (`draft: false`) na review.

### Verified
- `scripts/test-site.sh`: 45 passed, 0 failed (NL↔EN parity + hreflang).
- `hugo -D` rendert beide posts; taaltoggle paart ze via `translationKey`.

## 2026-05-18 (eighth pass — uitbreiding cooldown-post naar Python)

### Changed
- Beide cooldown-posts uitgebreid van npm/pnpm/bun-only naar
  npm/pnpm/bun + uv + pip coverage. Aanleiding: uv 0.9.17 (dec 2025)
  voegde `[tool.uv].exclude-newer` toe; pip 26.1 (apr 2026)
  voegde `--uploaded-prior-to` toe. De claim "PyPI heeft geen
  equivalent van `min-release-age`" in de "Wat het niet is"-sectie
  was sinds eind 2025 niet meer correct — vervangen door de échte
  resterende gaps (poetry/pipenv, registry-compromise, IDE-extensies).
- Titel: "Drie regels config tegen npm supply-chain attacks" →
  "Vijf regels config tegen supply-chain attacks (npm + PyPI)".
  Tabel uitgebreid met uv en pip rijen + versie-vereisten. Intro
  noemt nu het LiteLLM PyPI-incident (maart 2026, 119k+ downloads
  in 2u32min) als concrete aanleiding voor de Python-kant. CI-env-vars
  uitgebreid met `UV_EXCLUDE_NEWER` en `PIP_UPLOADED_PRIOR_TO`.
  Override-flow + implementatie-link tellen nu 5 ipv 3 keys.
- Tags: `pypi` toegevoegd op beide posts.
- Geen wijzigingen aan slug of `translationKey` ("npm-supply-chain-cooldown")
  — pre-existing URL blijft werken, RSS-readers krijgen geen
  duplicate-entry.

### Tested
- `hugo --gc --minify` schoon, geen warnings.
- `bash scripts/test-site.sh` → 45/45 assertions pass, inclusief
  NL/EN translationKey parity-check.

### Fixed
- Taal-correctie in NL post: "routineus" (calque van Engels "routine"
  — in NL betekent het "uit gewoonte / mechanisch", niet "alledaags")
  → "bekend"; "malicious" → "kwaadaardig" in alle Nederlandse zinnen
  (4 voorkomens: summary, intro, CI-pipeline-zin, mechanisme-paragraaf).
  EN post ongewijzigd — "malicious" is daar het correcte Engelse woord.

## 2026-05-18 (seventh pass — npm supply-chain cooldown post)

### Added
- `content/nl/posts/2026-05-18-npm-supply-chain-cooldown.md` en
  `content/en/posts/2026-05-18-npm-supply-chain-cooldown.md` —
  parallelle NL/EN post over de 7-daagse package-manager cooldown
  als goedkope mitigatie voor npm supply-chain attacks. Shared
  `translationKey: "npm-supply-chain-cooldown"` zodat de language
  switcher ze pairt. Tags: `security`, `supply-chain`, `npm`,
  `devops`. Linkt naar de implementatie in
  [`MWest2020/workstation-security`](https://github.com/MWest2020/workstation-security)
  (`common/install-pm-cooldown.sh` + `docs/supply-chain-cooldown.md`),
  die op 2026-05-18 v1.0.0 hit.

### Tested
- `hugo --gc --minify` schoon (NL 31 pages, EN 29 pages,
  geen warnings).
- `bash scripts/test-site.sh` → 45/45 assertions pass, inclusief de
  NL/EN translationKey parity-check.

### Changed
- Beide cooldown-posts: `### Feedback`-sectie toegevoegd onderaan met
  link naar workstation-security issues + mailto. Eerste post met een
  expliciete CTA — sluit aan op de v1.0.0-release-flow.

## 2026-05-17 (sixth pass — translation parity + cleanup)

### Added
- `content/en/posts/2026-05-17-claude-code-from-your-phone.md` —
  English translation of the mobile-Claude-Code post. Same structure,
  same links, same `translationKey: "mobile-claude-code"` so the
  language switcher pairs them.
- `translationKey:` added to every existing content file that lacked
  one: `_index.md` (home), `posts/_index.md`, both `2026-05-14`
  posts, and the NL mobile post. Values picked to be stable and
  language-neutral (`home`, `posts`, `first-post`, `mobile-claude-code`).
- `archetypes/posts.md` now scaffolds an empty `translationKey: ""`
  in new posts, with a comment reminding the author to keep the
  value identical between NL and EN.

### Tested
- `scripts/test-site.sh` extended with two new content-parity checks
  (45 total assertions now):
  - every `content/**/*.md` declares a non-empty `translationKey`
  - the set of translationKey values in NL equals the set in EN
  Adding a post in one language without the other now fails the
  smoke test before commit.

### Removed
- `static/robots.txt`. Shadowed by Hugo's autogenerated robots.txt
  (because `enableRobotsTXT = true`); was dead code. Hugo emits an
  equivalent file at `/robots.txt` automatically.

## 2026-05-17 (fifth pass — SEO basics)

### Added
- `layouts/_partials/extend_head.html`: Person JSON-LD schema on the
  home page and both about pages. Includes `sameAs` to GitHub and
  LinkedIn so search engines can resolve "Mark Westerweel" → this
  site as the canonical identity. Skipped on service / post pages
  (those keep PaperMod's BlogPosting schema).
- `hugo.toml`: `Author = "Mark Westerweel"` in `[params]`. Fills the
  previously-empty `<meta name=author>` tag site-wide and lets
  PaperMod attach an author Person to BlogPosting schemas it
  generates.

### Tested
- `scripts/test-site.sh` extended: meta author non-empty site-wide,
  Person schema (with sameAs) present on home + about (NL+EN), Person
  schema NOT bleeding to service / post pages, sitemap index +
  per-language sub-sitemaps cover the key pages, robots.txt allows
  all and references the sitemap. 43 assertions total.

### Action required (outside the repo)
- Submit `https://westerweel.work/sitemap.xml` to **Google Search
  Console** (Property → Sitemaps) so initial indexing is faster than
  organic crawl. Same for Bing Webmaster Tools if you care.
- LinkedIn / GitHub profiles should ideally link back to
  `https://westerweel.work` somewhere visible (reciprocal `sameAs`).

### Known limitation
- `static/robots.txt` is currently shadowed by Hugo's autogenerated
  one (because `enableRobotsTXT = true`). Behaviour is correct but
  the static file is dead code — left in place rather than removed
  in this commit; clean up separately if desired.

## 2026-05-17 (fourth pass — first real post)

### Added
- `content/nl/posts/2026-05-17-claude-code-via-mobiel.md` (NL, draft).
  How the homelab option for using Claude Code from a phone is built:
  Proxmox LXC, Tailscale, tmux (multi-device shared sessions are the
  killer feature), per-device SSH keys, IaC for provisioning. No
  machine-specific paths, hostnames, IPs, or container IDs from the
  homelab repo leaked into the post — all generalised. EN translation
  deferred.

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
