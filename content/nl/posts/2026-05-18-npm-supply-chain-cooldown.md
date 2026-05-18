---
title: "Vijf regels config tegen supply-chain attacks (npm + PyPI)"
date: 2026-05-18
draft: false
tags: ["security", "supply-chain", "npm", "pypi", "devops"]
translationKey: "npm-supply-chain-cooldown"
summary: "npm haalt kwaadaardige versies binnen 24-48 uur offline; PyPI zet ze binnen uren in quarantaine. Een wachttijd van zeven dagen — vijf regels config — laat dat venster voor je werken."
---

Het patroon van supply-chain-aanvallen is inmiddels bekend, op
beide grote ecosystemen. Een maintainer-account wordt
gecompromitteerd (phishing, token-leak, social engineering). De
aanvaller publiceert een nieuwe patch-versie van een populair pakket
met kwaadaardige code — typisch een post-install / install-hook
script dat secrets exfiltreert of een dead-man's switch installeert.
Iedereen met `^x.y.z` of `~x.y.z` in zijn lockfile pakt de versie
op tijdens de volgende `npm install`; iedereen met een losse
`>=x.y.z` in `pyproject.toml` idem bij `pip install` of `uv sync`.
Binnen 24-48 uur detecteert [npm](https://docs.npmjs.com/) de
versie en haalt 'm offline; [PyPI](https://blog.pypi.org/) zet
nieuwe kwaadaardige uploads vaak binnen uren in quarantaine.

Het slechte nieuws: in dat detectie-venster installeert je
CI-pipeline de kwaadaardige versie zonder vragen. De [LiteLLM-aanval
op PyPI](https://blog.pypi.org/posts/2026-04-02-incident-report-litellm-telnyx-supply-chain-attack/)
in maart 2026 stond 2 uur 32 minuten live en haalde in die tijd
ruim 119.000 downloads op. Het goede nieuws: diezelfde paar uur
is een handvat.

### Het mechanisme

Een cooldown weigert pakketversies te installeren als ze jonger zijn
dan N dagen. Vijf pakketmanagers, vijf config-keys, allemaal native
ondersteund — geen agent, geen daemon, geen extra dependency:

| Manager | File | Key | Eenheid | Min. versie |
|---|---|---|---|---|
| [npm](https://docs.npmjs.com/cli/v11/configuring-npm/npmrc) | `~/.npmrc` | `min-release-age` | dagen | 11.10+ |
| [pnpm](https://pnpm.io/settings) | `~/.npmrc` | `minimum-release-age` | minuten | 10.16+ |
| [bun](https://bun.sh/docs/runtime/bunfig) | `~/.bunfig.toml` | `[install] minimumReleaseAge` | seconden | 1.3+ |
| [uv](https://docs.astral.sh/uv/reference/settings/) | `~/.config/uv/uv.toml` | `exclude-newer` | duration (`"7 days"`) | 0.9.17+ |
| [pip](https://pip.pypa.io/en/stable/cli/pip_install/) | `~/.config/pip/pip.conf` | `[install] uploaded-prior-to` | ISO 8601 (`P7D`) | 26.1+ |

Met een venster van zeven dagen kom je categorisch ná het detect-en-
yank/quarantine-moment van beide registries. Een kwaadaardige versie
haalt je lockfile pas als dezelfde versie zeven dagen ongedetecteerd
is gebleven — orde van grootte zeldzamer dan het basis-scenario.

### Drie scopes: workstation, project, CI

Alle vier de user-level files (`~/.npmrc`, `~/.bunfig.toml`,
`~/.config/uv/uv.toml`, `~/.config/pip/pip.conf`) dekken je eigen
interactieve gebruik. Niet genoeg voor de rest:

- Jouw workstation, jij ingelogd: actief.
- Andere user op dezelfde machine: niet actief.
- Docker build die als `node` / `python` user draait: niet actief.
- CI-runner ([GitHub Actions](https://docs.github.com/en/actions),
  GitLab CI, etc.): niet actief.

CI is precies waar de aanvaller wil komen — daar draait je
production build. User-level dekt dat niet.

**Per-project.** Drop config-files in elke repo die je owned. Voor
het Node-ecosysteem zijn dat `.npmrc` en `bunfig.toml` — auto-detect'd
door npm/pnpm/bun. Voor uv: een `[tool.uv]` blok in `pyproject.toml`
met `exclude-newer`. Pip is de uitzondering: pip leest géén
project-lokale `pip.conf` zonder hulp — je moet
`PIP_CONFIG_FILE=$PWD/pip.conf` zetten, of de env-var-route hieronder
gebruiken. Geen van de files bevat secrets; allemaal horen ze in
version control.

**CI-only.** Voor projecten waar je geen file mag committen (gedeelde
codebases waar het team de keuze niet deelt) zet je de cooldown
in environment variables:

```yaml
env:
  # Node ecosysteem (npm én pnpm honoreren NPM_CONFIG_*)
  NPM_CONFIG_MIN_RELEASE_AGE: 7
  NPM_CONFIG_MINIMUM_RELEASE_AGE: 10080

  # Python ecosysteem
  UV_EXCLUDE_NEWER: "7 days"
  PIP_UPLOADED_PRIOR_TO: P7D
```

Geen file-wijziging, geen PR-discussie, alleen een env-blok bij de
jobs die `npm install` / `pip install` / `uv sync` draaien. bun heeft
(vanaf 1.3) géén equivalent env-var — voor bun-projects is
`bunfig.toml` de enige weg.

### Override voor urgente CVEs

Wat als er een echte security-patch valt binnen je 7-daagse venster?
Een CVE in `lodash` of `pydantic` waarvan de fix gisteren is
gepubliceerd, en jouw cooldown houdt 'm tegen. Per-install override:

```bash
# Node
NPM_CONFIG_MIN_RELEASE_AGE=0 npm install lodash@4.17.45

# Python
pip install --uploaded-prior-to 2026-06-01T00:00:00Z pydantic==2.11.1
uv add --exclude-newer 'never' pydantic==2.11.1
```

Of, als je de fix permanent wil opnemen, zet in de project-lokale
config de waarde op `0` (of een datum vóór de fix), commit dat als
hotfix, en revert wanneer de cooldown het pakket toch zou hebben
toegelaten. De commit zelf is je audit-trail: bewijs dat de override
bewust is.

### Wat het kost

Je loopt zeven dagen achter op patches. Daar moet je eerlijk over
zijn. Voor een dev-machine is dat triviaal. Voor productiebuilds
waar je dependency-updates al via een review-flow doet
([Renovate](https://docs.renovatebot.com/) of
[Dependabot](https://docs.github.com/en/code-security/dependabot)) is
het ook prima: hun bots wachten zelf vaak al langer voordat ze een
PR openen. Voor use-cases waar je écht binnen het uur op een
registry-publish moet kunnen handelen (CVE-response op productie) is
de override-flow er, of zet je dat specifieke project op een korter
venster.

### Wat het niet is

Geen zilveren kogel. Een aanval die zich verstopt achter een
8+ dagen oude package valt buiten dit venster. Idem voor compromise
van de registries zelf, kwaadaardige IDE-extensies, of
package-managers die nog géén cooldown-feature hebben — `poetry` en
`pipenv` (Python) hebben per medio 2026 geen native equivalent;
voor Docker pin je images op SHA. Het is een tijds-filter, geen
integriteits-check.

### Implementatie

In [`MWest2020/workstation-security`](https://github.com/MWest2020/workstation-security)
staat een installer-script dat alle vijf de keys idempotent zet
([`common/install-pm-cooldown.sh`](https://github.com/MWest2020/workstation-security/blob/main/common/install-pm-cooldown.sh)),
plus templates voor per-project en CI. User-level, geen sudo,
behoudt bestaande inhoud en file-modus. Standalone uitleg met de
volledige tabel staat onder
[`docs/supply-chain-cooldown.md`](https://github.com/MWest2020/workstation-security/blob/main/docs/supply-chain-cooldown.md).

Vijf regels config, een week latency. Lijkt me de moeite waard.

### Feedback

Feedback op
[`workstation-security`](https://github.com/MWest2020/workstation-security)
is meer dan welkom — [open een
issue](https://github.com/MWest2020/workstation-security/issues/new/choose)
voor bugs, een ontbrekende distro, of een use-case die de tool nog
niet dekt. Mailen kan ook:
[mark@westerweel.work](mailto:mark@westerweel.work).
