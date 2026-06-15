---
title: "Gecureerde, deelbare skillsets voor AI-agents"
date: 2026-06-15
draft: true
tags: ["ai", "claude-code", "skills", "provenance", "devops"]
translationKey: "curated-skillsets"
summary: "Een skill voor een AI-agent is een markdown-bestand. Dat is precies het probleem: iedereen kan er een dumpen, niemand weet of-ie deugt. Hier is hoe ik er een gecureerde, ondertekende, deelbare bibliotheek van maak — en waarom de kern niet de skills zijn, maar de curatie."
---

Laatst kwam ik een GitHub-repo tegen met één skill erin:
[`owasp-security`](https://github.com/agamm/claude-code-owasp) — OWASP
Top 10:2025, ASVS 5.0, de LLM Top 10, netjes als checklist voor een
AI-agent. 233 sterren, MIT-licentie, ziet er goed uit. De verleiding
is om 'm te kopiëren naar `~/.claude/skills/` en klaar.

Dat deed ik niet. In plaats daarvan haalde ik 'm door een pipeline,
en juist dáár zit het verhaal.

### Een skill is maar een bestand — dat is het probleem

Voor Claude Code (en de meeste agents) is een
[skill](https://github.com/anthropics/skills) een `SKILL.md`: wat
frontmatter, een "wanneer te gebruiken", en een lap instructies.
Laagdrempelig, en dat is de charme. Maar het betekent ook: geen
kwaliteitsdrempel, geen herkomst, geen idee of de inhoud nog klopt.
Je verzamelt er een handvol, ze rotten stilletjes, en je agent gedraagt
zich naar de slechtste die toevallig afvuurt.

Bij code lossen we dat al jaren op — review, versies, herkomst,
ondertekening. Bij skills doen de meeste mensen nog niets. Dus bouwde
ik een klein CLI-gereedschap, `skill-forge`, dat skills behandelt als
wat ze zijn: artefacten die curatie verdienen.

### De curatie-lus

Skills komen binnen als **draft**, niet als waarheid. Daarna:

| Stap | Wat er gebeurt |
|---|---|
| `import` | binnenhalen, herkomst vastleggen (origin + bron-URL's) |
| `judge` | een LLM scoort tegen een vaste rubric (helderheid, bruikbaarheid, dekking, herkomst) |
| `promote` | alleen als de score de drempel haalt (totaal ≥ 0,75, elke as ≥ 0,50) |
| `refine` | verbeter over genummerde iteraties, met een diff en een audit-spoor |

Terug naar `owasp-security`. De judge gaf 'm een 0,87 — sterk op
bruikbaarheid en dekking. Maar één as bleef hangen op 0,60:
**herkomst**. De `## Source`-sectie verwees alleen naar de GitHub-repo,
niet naar de OWASP- en ASVS-standaarden waar de skill feitelijk op
leunt. Een terechte bevinding. Eén `refine` later — de gezaghebbende
bronnen toegevoegd, de rest onaangeraakt — stond-ie op 0,88 met die
as op 0,85. Pas toen promote.

Het punt is niet de score. Het punt is dat er een *oordeel* tussen zit,
met een spoor dat een ander kan nalopen. Geen losse map met prompts,
maar een bibliotheek met provenance — elke skill ondertekend met een
Ed25519-stempel, zodat geknoei zichtbaar is.

### De kern: skillsets die je kunt delen

Hier zit het bestaansrecht. Een gecureerde skill is leuk; een
gecureerde *set* die je kunt delen is het hele punt.

Skills krijgen **tags**, en een *skillset* is simpelweg een query:
"alle live skills met tag `security`". Geen apart bestand, geen
registry — een tag en een vraag. Daarmee mount je een gevet subset in
plaats van je hele bibliotheek:

```bash
forge ls --tag security          # wat zit er in de set
forge sync claude-code --tag security   # mount alleen die set
```

Een review-container krijgt de `security`-set. Een examen-container
de `examenstof`-set. Geen van beide krijgt de rest, en geen van beide
hoeft te vertrouwen op een gedeelde schijf.

### Het toekomstplan: skillsets over de lijn

Dat laatste — "geen gedeelde schijf" — is waar het heen gaat.
`sync` werkt via symlinks: prima op één machine, nutteloos voor een
gecontaineriseerde agent. Dus draait er nu een kleine, **read-only**
MCP-server bovenop:

```bash
forge serve mcp    # tools: list_skills, get_skill, get_skillset
```

Een container start dit, vraagt `get_skillset("security")`, en krijgt
de gevette set over het protocol — inclusief herkomst, zonder ooit bij
de rest van de bibliotheek te kunnen. Read-only is een harde grens:
de server serveert de gecureerde uitvoer, nooit de curatie zelf.
Importeren, scoren, promoten — dat blijft lokaal en bewust.

### Waarom dit, en niet meer

De rode draad is dezelfde die ik bij infrastructuur aanhoud: saai en
naloopbaar. Geen federatie, geen marktplaats, geen slim distributie-web
— die laag werd er expres weer uitgesloopt toen-ie niet bleek te
verdienen. Wat overblijft is de kleinst mogelijke kern die het werk
doet: cureren, ondertekenen, groeperen, en read-only doorgeven.

Een AI-agent is zo goed als de instructies die-ie mag inladen. Die
instructies verdienen dezelfde discipline als je code: een drempel om
binnen te komen, een herkomst om op terug te vallen, en een manier om
precies de juiste set te delen — niet meer, niet minder.
