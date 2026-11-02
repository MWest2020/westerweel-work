# westerweel.work

Persoonlijke site / blog. Hugo + PaperMod, statisch, NL/EN.

## Stack

- **Generator:** [Hugo](https://gohugo.io/) (Go, één binary, geen Node)
- **Theme:** [PaperMod](https://github.com/adityatelange/hugo-PaperMod) (git submodule)
- **Hosting:** Cloudflare Pages (primary), self-host op eigen node (optie)
- **DNS:** Cloudflare (`westerweel.work`)

## Eerste keer opzetten

```bash
# 1. Hugo installeren (Linux/macOS)
# AlmaLinux: hugo zit niet in default repos, download de binary:
curl -L https://github.com/gohugoio/hugo/releases/download/v0.146.0/hugo_extended_0.146.0_linux-amd64.tar.gz \
  | tar -xz -C /tmp hugo
sudo mv /tmp/hugo /usr/local/bin/

# 2. Repo klonen + theme als submodule binnenhalen
git clone https://github.com/MWest2020/westerweel-work
cd westerweel-work
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
git submodule update --init --recursive

# 3. Lokaal draaien
hugo server -D    # -D = include drafts
# → open http://localhost:1313
```

## Nieuwe blogpost

```bash
hugo new content/nl/posts/2026-05-20-titel.md
hugo new content/en/posts/2026-05-20-title.md
```

Frontmatter staat al goed via het archetype. Schrijf, zet `draft: false`,
commit, push. Cloudflare bouwt en deployt binnen 30 seconden.

## Build

```bash
hugo --gc --minify
# Output staat in public/
```

## Hosting — Cloudflare Pages (huidige setup)

1. Repo naar GitHub pushen.
2. Cloudflare Dashboard → Workers & Pages → Create → Pages → Connect to Git.
3. Build config:
   - Framework: **Hugo**
   - Build command: `hugo --gc --minify`
   - Build output: `public`
   - Environment variable: `HUGO_VERSION=0.146.0` (PaperMod requires ≥ 0.146.0)
4. Custom domain toevoegen: `westerweel.work` + `www.westerweel.work`.
5. Cloudflare maakt automatisch DNS CNAME-records aan (oranje wolk = aan).

Klaar. PR-previews krijg je gratis.

## Hosting — eigen node (later optioneel)

Hugo's output is pure statische HTML. Op je Proxmox-node:

```bash
# Op je build-machine (of in GH Actions):
hugo --gc --minify --baseURL "https://westerweel.work/"
rsync -avz --delete public/ node:/var/www/westerweel.work/

# Op de node — Caddy doet TLS automatisch:
# /etc/caddy/Caddyfile:
westerweel.work {
    root * /var/www/westerweel.work
    file_server
    encode gzip zstd
    header {
        Strict-Transport-Security "max-age=31536000"
        X-Content-Type-Options "nosniff"
        Referrer-Policy "strict-origin-when-cross-origin"
    }
}
```

DNS-record in Cloudflare: A-record naar je node-IP, oranje wolk aan.

### Failover van eigen node naar Cloudflare Pages

Twee opties.

**Optie A — Cloudflare Load Balancing (betaald, ~€5/maand).**
Pool met twee origins (jouw node primary, Pages fallback), health check
elke 60s, na 10x falen flippen. Volautomatisch met failback.

**Optie B — Gratis, via GitHub Action cronjob.**
Action draait elke 5 minuten, pingt je node-endpoint. Bij fail: patcht
het CNAME-record via Cloudflare API naar `westerweel-work.pages.dev`.
Bij herstel: patcht het terug. DNS-TTL op 60s zetten.

Voorbeeld-workflow staat klaar als je dit nodig hebt — vraag dan even
of zet hem zelf in elkaar; het is ~30 regels YAML.

## Structuur

```
content/
├── nl/                   # Nederlandse content (default)
│   ├── _index.md         # home
│   ├── about.md
│   ├── diensten.md
│   ├── workshops.md      # overzicht van slidedecks
│   └── posts/
│       └── *.md
└── en/                   # Engelse content
    ├── _index.md
    ├── about.md
    ├── services.md
    ├── workshops.md
    └── posts/
        └── *.md

archetypes/posts.md       # template voor nieuwe posts
hugo.toml                 # config
static/                   # favicon, _redirects, _headers, robots.txt
└── slides/<slug>/index.html   # self-contained presentaties, verbatim geserveerd
themes/PaperMod/          # submodule
```

## /nu/ — het gegenereerde overzicht

`/nu/` en `/en/now/` tonen waar ik aan werk: per project wat er in de maak is,
wat vastzit, wat er de afgelopen zeven dagen is opgeleverd en welke vragen op
mij wachten, elk met wat er gebeurt als ik niet antwoord. De pagina rendert
`data/status.json` met `layouts/_default/now.html`.

Dat bestand schrijft niemand met de hand. `orchestrator/status_site.py` in
[ratatoskr](https://github.com/MWest2020/ratatoskr) bouwt het elke twee uur uit
bouwstatus en GitHub, filtert geheimen, e-mailadressen en ids eruit, en pusht
naar `main` alleen als de inhoud veranderd is en hooguit eens per twee uur:
elke push is een Cloudflare Pages-build, en de gratis laag heeft een
maandbudget. Uitleg: `docs/how-to/status-site.md` in ratatoskr.

Een vraag op het overzicht zetten: een issue met label `waiting-on-mark`, de
vraag als titel en een regel `Default: …` in de body.

## Workshops / slidedecks

Een deck is een **self-contained HTML-bestand** op
`static/slides/<slug>/index.html`. Cloudflare Pages (en de Caddy-fallback)
serveren het byte-voor-byte op `/slides/<slug>/` — dus online identiek aan het
bestand lokaal openen. Geen Hugo-rendering, geen build-stap.

Een nieuw deck toevoegen:

1. Zet het HTML-bestand op `static/slides/<slug>/index.html`.
2. Voeg een regel toe aan **beide** overzichtspagina's
   (`content/nl/workshops.md` en `content/en/workshops.md`) die naar
   `/slides/<slug>/` linkt.

De overzichtspagina's zijn gewone Hugo-content en vallen onder de NL/EN-pariteit
(`translationKey: workshops`, op `/workshops/` en `/en/workshops/`). De decks
zelf staan in `static/` en vallen er buiten — een deck mag dus eentalig zijn.

## Boekenclub

`/boekenclub/` (en `/en/bookclub/`) is een gewone pagina van de site: per boek de score, voor wie, een link naar
de slides en een downloadknop voor de PDF. Elk boek heeft een eigen deck op `/boekenclub/<slug>/` en `/en/bookclub/<slug>/`. Slides zijn staand 1080×1350
(LinkedIn-carrousel), werken met pijltjes, spatie, vegen en tikken, en `#3` opent slide 3.
De stijl komt uit tree-presentations (Cormorant Garamond, sepia, een boom per slide).

**Een boek toevoegen = één bestand per taal:** kopieer `content/nl/boekenclub/becoming-sre.md` naar
`content/nl/boekenclub/<slug>.md` en `content/en/bookclub/becoming-sre.md` naar `content/en/bookclub/<slug>.md`
(zelfde `translationKey`), en vul de front matter in. De smoke test eist beide talen. Daarin staan titel, auteur,
uitgever en jaar, de cover-zin (`hook`), 3–5 inzichten (met optioneel `nugget` + `chapter` voor een concreet voorbeeld uit het boek, `doe` en
`emphasis`; een deck heeft 7–9 slides, de build faalt daarbuiten), de scores op de vaste rubriek, voor wie en niet voor wie, `further_reading`
en `question`, en optioneel `photo` (eigen foto op de cover) en `quote` (hooguit één, onder de 15 woorden). `weight` bepaalt de volgorde. De eindscore rekent het template uit:
het gemiddelde, afgerond op 0,5 (halven naar boven). Wat je nu leest, staat in
`content/nl/boekenclub/_index.md` (`reading_now`). Opmaak:
`layouts/boekenclub/{single,list}.html` en `static/boekenclub/assets/`. Licenties van
de bomen: `CREDITS.md`.

**PDF voor LinkedIn** (één pagina per slide, exact 1080×1350):

```bash
uv run --with playwright playwright install chromium     # eenmalig
uv run --with playwright --with pypdf scripts/boekenclub_pdf.py becoming-sre           # -> boekenclub-pdf/becoming-sre.pdf
uv run --with playwright --with pypdf scripts/boekenclub_pdf.py becoming-sre --shots   # + PNG per slide (1080 px, en een telefoon van 390 px)
uv run --with playwright --with pypdf scripts/boekenclub_pdf.py becoming-sre --lang en  # de Engelse versie
uv run --with playwright --with pypdf scripts/boekenclub_pdf.py becoming-sre --publish  # ook naar static/boekenclub/pdf/ (downloadknop); commit die PDF
```

`boekenclub-pdf/` staat in `.gitignore`. Met `--publish` komt de PDF ook in `static/boekenclub/pdf/`; die staat wel in git, want de site biedt hem aan als download. Maak hem opnieuw na elke tekstwijziging (de smoke test controleert dat hij er is, niet dat hij actueel is).
De smoke test faalt zolang er nog een `TODO` in een deck staat.

## Theme bijwerken

```bash
git submodule update --remote themes/PaperMod
git add themes/PaperMod
git commit -m "Update PaperMod theme"
```

## Domein

`westerweel.work` via Cloudflare. Geen MX-records nodig tenzij je
mail-routing wilt — voor `mark@westerweel.work` regel je mailbox
los (Migadu, Fastmail, of zelf op je node).
