---
title: "Spreker"
summary: "Talks en dev-sessies over AI-agents in operations, context en SRE. Voor meetups en conferenties, in het Nederlands of het Engels."
translationKey: "speaker"
---

Ik praat over wat er gebeurt als je AI-agents in operations zet: welke
context ze nodig hebben, waar de grenzen moeten liggen, en hoe je bewijst dat
het werkt. Daarnaast geef ik dev-sessies over het vak zelf, zoals containers
en de plek van een check. Voor meetups en conferenties over SRE, DevOps en
cloud native, in het Nederlands of het Engels.

De decks staan bij [workshops](/workshops/) en draaien in je browser.

## Talks

### Agents, skills & tools

Wat ik leerde bij het bouwen van SREna, een lokale SRE-agent, verteld in
verhalen. De peuter en de koektrommel: een agent gebruikt alles wat binnen
bereik ligt, dus jij bepaalt wat er in de keuken staat. De golem: hoe ver laat
je een agent zelf lopen, van alleen monitoring tot volledig zelfsturend. David
tegen Goliath: een klein lokaal model tegen een cloud-baseline, en waar hij
nog verliest.

- **Vorm:** talk
- **Taal:** Engels
- **Deck:** [/slides/agents-skills-tools/](/slides/agents-skills-tools/) (concept)

### Context is alles

Een agent die gokt, mist meestal context, geen intelligentie. Deze talk loopt
van een MCP die agents naar de kennisbank stuurt naar SREna, een SRE-agent die
volledig lokaal draait. Met goud, zilver en brons als keurmerk op bronnen, en
wat een klein lokaal model je leert over je eigen context. De grootste les:
de kennisbank gaat hallucineren tegen, niet het model.

- **Vorm:** talk
- **Taal:** Nederlands of Engels
- **Deck:** [/slides/context-is-alles/](/slides/context-is-alles/), hoort bij
  [de blogpost](/posts/2026-11-04-context-is-alles/)

### AI zijn net mensen *(maar dan anders)*

Waarom AI-agents dezelfde fouten maken als mensen, en wat je eraan doet.
Aandacht (wat in het midden van de context staat, raakt zoek), een briefing
als voor een nieuwe collega, één vak per agent en een aparte reviewer. En waar
de vergelijking ophoudt: geen geheugen tussen sessies, niet moe, wel met veel
zelfvertrouwen fout. Eindigt met een checklist voor morgen.

- **Vorm:** talk of workshop
- **Taal:** Nederlands of Engels
- **Deck:** [/slides/ai-zijn-net-mensen/](/slides/ai-zijn-net-mensen/)

### Shift left — hooks > goede bedoelingen

Waarom CLAUDE.md je regel niet afdwingt, en wat wel. De casus: een check die in
de CI faalt, twintig minuten nadat je al verder was, terwijl dezelfde check
als hook 21 milliseconden kost. Vijf lagen van zacht naar hard (CLAUDE.md,
skills, permissions, hooks en CI) en welke regel waar hoort. Met een
leesversie en code als hand-out.

- **Vorm:** dev-sessie
- **Lengte:** ±1 uur
- **Taal:** Nederlands
- **Deck:** [/slides/claude-shift-left/](/slides/claude-shift-left/),
  [leesversie](/slides/claude-shift-left/lees/),
  [code + hand-out](https://github.com/MWest2020/westerweel-work/tree/main/workshops/claude-shift-left)

### Docker — van image naar registry

Het mentale model achter containers: een container is geen VM, en een image is
geen container. Waarom `docker commit` je CI sloopt en een Dockerfile niet.
Bouwen, taggen, pushen en pullen, met de do's en don'ts voor productie. Voor
een team dat lokaal prima images pusht, maar vastloopt zodra de CI/CD het
overneemt.

- **Vorm:** dev-sessie
- **Lengte:** ±1 uur
- **Taal:** Nederlands
- **Deck:** [/slides/docker-101/](/slides/docker-101/)

## Onderwerpen

Waar ik graag over praat, ook buiten de talks hierboven:

- AI-agents in operations: context, kennisbanken, guardrails, evaluatie.
- Soevereine infrastructuur: Kubernetes, Proxmox, GitOps, eigen ijzer.
- Compliance die de praktijk volgt: ISO 27001, levende documentatie.
- SRE: SLO's die bij de klant beginnen, toil opruimen.

## Bio

Voor organisatoren, om over te nemen.

**Kort**

> Mark Westerweel is Site Reliability Engineer bij Schiphol. Hij bouwt
> infrastructuur voor Nederlandse organisaties die soevereiniteit serieus
> nemen, en zoekt uit hoe AI-agents veilig kunnen meedraaien in operations.
> Hij schrijft op westerweel.work.

**Lang**

> Mark Westerweel is Site Reliability Engineer bij Schiphol, waar hij SLO's
> definieert die bij de klant beginnen en toil opruimt. Daarvoor werkte hij
> jaren in en rond Common Ground en het Nederlandse gemeentelijke landschap:
> multi-tenant Kubernetes, Nextcloud op schaal, ISO 27001-trajecten en
> subsidieaanvragen.
>
> Naast zijn werk bouwt hij een agent-ecosysteem op eigen hardware: een met de
> hand opgebouwd Kubernetes-cluster, agents die code bouwen in een kooi, en
> SREna, een SRE-agent die volledig lokaal draait. Hij is Claude Certified
> Architect (Foundation) en een van GitHub's eerste 5.000 agentic AI
> engineers. Hij schrijft op westerweel.work.

## Contact

Mail [mark@westerweel.work](mailto:mark@westerweel.work) met datum,
evenement en doelgroep.
