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
curl -L https://github.com/gohugoio/hugo/releases/download/v0.139.0/hugo_extended_0.139.0_linux-amd64.tar.gz \
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
   - Environment variable: `HUGO_VERSION=0.139.0`
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
│   └── posts/
│       └── *.md
└── en/                   # Engelse content
    ├── _index.md
    ├── about.md
    ├── services.md
    └── posts/
        └── *.md

archetypes/posts.md       # template voor nieuwe posts
hugo.toml                 # config
static/                   # favicon, _redirects, _headers, robots.txt
themes/PaperMod/          # submodule
```

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
