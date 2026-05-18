---
title: "Drie regels config tegen npm supply-chain attacks"
date: 2026-05-18
draft: false
tags: ["security", "supply-chain", "npm", "devops"]
translationKey: "npm-supply-chain-cooldown"
summary: "npm yankt malicious versies meestal binnen 24-48 uur. Een wachttijd van zeven dagen — drie regels config — laat dat venster voor je werken."
---

Het patroon van npm-supply-chain-aanvallen is inmiddels routineus.
Een maintainer-account wordt gecompromitteerd (phishing, token-leak,
social engineering). De aanvaller publiceert een nieuwe patch-versie
van een populair pakket met malicious code — typisch een post-install
script dat secrets exfiltreert of een dead-man's switch installeert.
Iedereen met `^x.y.z` of `~x.y.z` in zijn lockfile pakt de versie op
tijdens de volgende `npm install`. Binnen 24-48 uur detecteert
[npm](https://docs.npmjs.com/) de versie, yankt 'm, en publiceert
een advisory.

Het slechte nieuws: in dat venster van een dag of twee installeert
je CI-pipeline de malicious versie zonder vragen. Het goede nieuws:
diezelfde 24-48 uur is een handvat.

### Het mechanisme

Een cooldown weigert pakketversies te installeren als ze jonger zijn
dan N dagen. Drie pakketmanagers, drie config-keys, allemaal native
ondersteund — geen agent, geen daemon, geen extra dependency:

| Manager | File | Key | Eenheid | Min. versie |
|---|---|---|---|---|
| [npm](https://docs.npmjs.com/cli/v11/configuring-npm/npmrc) | `~/.npmrc` | `min-release-age` | dagen | 11.10+ |
| [pnpm](https://pnpm.io/settings) | `~/.npmrc` | `minimum-release-age` | minuten | 10.16+ |
| [bun](https://bun.sh/docs/runtime/bunfig) | `~/.bunfig.toml` | `[install] minimumReleaseAge` | seconden | 1.3+ |

Met een venster van zeven dagen kom je categorisch ná het detect-en-
yank-moment van npm. Een malicious versie haalt je lockfile pas als
dezelfde versie zeven dagen ongedetecteerd is gebleven — orde van
grootte zeldzamer dan het basis-scenario.

### Drie scopes: workstation, project, CI

`~/.npmrc` en `~/.bunfig.toml` zijn user-level. Dat is goed voor je
eigen interactieve gebruik, maar niet genoeg:

- Jouw workstation, jij ingelogd: actief.
- Andere user op dezelfde machine: niet actief.
- Docker build die als `node`-user draait: niet actief.
- CI-runner ([GitHub Actions](https://docs.github.com/en/actions),
  GitLab CI, etc.): niet actief.

CI is precies waar de aanvaller wil komen — daar draait je
production build. User-level dekt dat niet.

**Per-project.** Drop een `.npmrc` en `bunfig.toml` in elke repo
die je owned, met de cooldown-keys. Beide files bevatten geen secrets
en horen in version control. Een CI-runner die je project checkt-out
leest ze automatisch.

**CI-only.** Voor projecten waar je geen file mag committen (gedeelde
codebases waar het team de keuze niet deelt) zet je de cooldown
in environment variables:

```yaml
env:
  NPM_CONFIG_MIN_RELEASE_AGE: 7
  NPM_CONFIG_MINIMUM_RELEASE_AGE: 10080
```

Geen file-wijziging, geen PR-discussie, alleen een env-blok bij de
jobs die `npm install` draaien.

### Override voor urgente CVEs

Wat als er een echte security-patch valt binnen je 7-daagse venster?
Een CVE in `lodash` waarvan de fix gisteren is gepubliceerd, en jouw
cooldown houdt 'm tegen. Twee opties:

```bash
# Tijdelijke override, alleen voor dit install-commando:
NPM_CONFIG_MIN_RELEASE_AGE=0 npm install lodash@4.17.45
```

Of, als je de fix permanent wil opnemen, zet in de project-lokale
`.npmrc` de waarde op `0`, commit dat als hotfix, en revert wanneer
de cooldown het pakket toch zou hebben toegelaten. De commit zelf is
je audit-trail: bewijs dat de override bewust is.

### Wat het kost

Je loopt zeven dagen achter op patches. Daar moet je eerlijk over
zijn. Voor een dev-machine is dat triviaal. Voor productiebuilds
waar je dependency-updates al via een review-flow doet
([Renovate](https://docs.renovatebot.com/) of
[Dependabot](https://docs.github.com/en/code-security/dependabot)) is
het ook prima: hun bots wachten zelf vaak al langer voordat ze een
PR openen. Voor use-cases waar je écht binnen het uur op een
npm-publish moet kunnen handelen (CVE-response op productie) is de
override-flow er, of zet je dat specifieke project op een korter
venster.

### Wat het niet is

Geen zilveren kogel. Een aanval die zich verstopt achter een
8+ dagen oude package valt buiten dit venster. Idem voor compromise
van de npm-registry zelf, kwaadaardige IDE-extensies, of
npm-onafhankelijke ecosystemen — [PyPI](https://pypi.org/) heeft
geen equivalent van `min-release-age`, voor Docker pin je images op
SHA. Het is een tijds-filter, geen integriteits-check.

### Implementatie

In [`MWest2020/workstation-security`](https://github.com/MWest2020/workstation-security)
staat een installer-script dat alle drie de keys idempotent zet
([`common/install-pm-cooldown.sh`](https://github.com/MWest2020/workstation-security/blob/main/common/install-pm-cooldown.sh)),
plus templates voor per-project en CI. User-level, geen sudo,
behoudt bestaande inhoud en file-modus. Standalone uitleg met de
volledige tabel staat onder
[`docs/supply-chain-cooldown.md`](https://github.com/MWest2020/workstation-security/blob/main/docs/supply-chain-cooldown.md).

Drie regels config, twee dagen latency. Lijkt me de moeite waard.
