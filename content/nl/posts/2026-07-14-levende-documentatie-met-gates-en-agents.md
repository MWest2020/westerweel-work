---
title: "Documentatie die liegt is erger dan geen documentatie"
date: 2026-07-14
draft: false
tags: ["ai", "agents", "documentation", "devops", "compliance"]
translationKey: "living-docs-gates"
summary: "Verouderde documentatie was altijd al een sluipend probleem, maar sinds AI-agents die documentatie als waarheid lezen is het een acuut probleem. Hoe wij documentatie 'levend' maakten met een afdwingbaar contract, gates die ongeteste wijzigingen tegenhouden, en een MCP-server die agents context geeft mét herkomst — zodat ze citeren in plaats van gokken. Van 63 bevindingen naar nul. En waarom dit patroon meteen de basis is voor een chatbot op je cluster: praten met de devops-collega die met vakantie is, mét bronvermelding."
---

*Hoe je documentatie bouwt die niet kán verouderen zonder dat iemand
het merkt — en waarom dat opeens urgent is nu agents meelezen.*

Iedereen kent de pagina. De wiki zegt dat de deploy via script A loopt,
maar script A is drie maanden geleden vervangen door pipeline B. De
README beschrijft een configuratie-optie die niet meer bestaat. Niemand
weet nog wie de eigenaar is van het document, dus niemand voelt zich
geroepen het te repareren.

Verouderde documentatie is erger dan geen documentatie. Geen
documentatie dwingt je om te kijken hoe het écht zit. Verouderde
documentatie geeft je **vals vertrouwen** — je handelt op informatie
die klopte, ooit.

Jarenlang was dit een sluipend probleem dat teams accepteerden als
natuurverschijnsel. Maar er is iets veranderd: **AI-agents lezen die
documentatie nu ook.** En daarmee is het van sluipend acuut geworden.

### Waarom agents het probleem verscherpen

Een ervaren mens ruikt dat een pagina oud is. De screenshots kloppen
niet meer, de toon is van twee reorganisaties geleden, het genoemde
teamlid is al weg. Mensen hebben een ingebouwde scepsis-reflex.

Een agent heeft die reflex niet. Die leest de pagina en neemt haar als
waarheid. Of erger: als er géén pagina is, valt hij terug op
modelkennis — een aanname over hoe systemen zoals het jouwe *meestal*
werken. In een omgeving met tientallen repository's en een
infrastructuur die per week verandert, is "meestal" precies niet goed
genoeg.

Wij werken aan een platform dat uit vele repository's bestaat, met
agents die daar dagelijks in meewerken. We zagen drie problemen steeds
terugkomen:

1. **Documentatie-drift.** Docs die achterblijven bij de code,
   gedupliceerde inhoud die per repo uit elkaar groeit, en geen enkele
   periodieke controle op juistheid.
2. **Ongeverifieerde wijzigingen.** Aanpassingen die gepusht werden
   zonder dat tests, checks of de bijbehorende documentatie mee waren.
   "Klaar" betekende: de code compileert.
3. **Agents zonder grondwaarheid.** Agents die per sessie opnieuw
   context bij elkaar moesten schrapen, en bij gebrek aan een
   betrouwbare bron terugvielen op aannames.

Drie problemen, één onderliggende oorzaak: er was niets dat de
werkelijkheid en de beschrijving van de werkelijkheid aan elkaar
vastklonk. Dus dat hebben we gebouwd. Drie mechanismen.

### Mechanisme 1: een docs-contract in plaats van goede bedoelingen

De eerste stap is saai en onderschat: spreek af wat documentatie *is*
en waar ze *leeft* — en maak die afspraak controleerbaar.

Bij ons leeft documentatie in `/docs` in de repository van de component
zelf. Nooit centraal, nooit gekopieerd. Het centrale portaal
*aggregeert* die mappen bij elke build en is zelf een wegwerpartefact —
de bronrepo blijft de enige waarheid. Daarmee is duplicatie (de bron
van divergentie) structureel weg.

Elke pagina draagt twee verplichte velden in de front matter:

```yaml
last_reviewed: 2026-07-14
owner: platform-team
```

Dat lijkt niets, maar het verandert alles. `owner` betekent dat er
altijd iemand aanspreekbaar is. `last_reviewed` betekent dat
houdbaarheid meetbaar is — en een review zonder wijziging telt: de
datum bijwerken ís de handeling die de houdbaarheid verlengt.

En de belangrijkste regel: **documentatie wijzigt in dezelfde PR als de
code die zij beschrijft.** "Klaar" betekent: code, tests én docs
bijgewerkt. Niet als richtlijn op een poster, maar als check die je
push tegenhoudt. Waarmee we bij mechanisme twee zijn.

### Mechanisme 2: gates — afdwingen in plaats van hopen

Afspraken zonder handhaving zijn wensen. Dus draait er vóór elke push
een set gates, gedeeld over alle repository's en vastgepind op een
specifieke versie (zodat reviewbaar is wélke controle draaide bij wélke
push):

- **Contract-check**: klopt de structuur, staat op elke pagina een
  geldige eigenaar en reviewdatum, is er nergens gedupliceerd?
- **Uitvoerbare doc-claims**: gemarkeerde codeblokken in de
  documentatie worden écht uitgevoerd als dry-run. Een pagina die
  beweert "dit commando controleert X" wordt daar zelf op afgerekend.
- **Tests en dry-runs** van de component zelf.
- **Secret-scanning**, zodat er nooit een credential in docs of code
  glipt.

De gates draaien in gate-modus: ze repareren niets stilletjes, ze
blokkeren en melden. En ze zijn zelf gedekt door unit tests — een
controle waarvan je niet weet of hij werkt, is theater.

Daarbovenop draait een pijplijn die het geheel wekelijks controleert,
óók als niemand iets pusht: een strikte build, een versheids-controle
(elke pagina moet binnen een jaar gereviewd zijn), en een linkcheck.
Gaat een geplande run rood, dan opent er automatisch precies één
drift-issue — dat vanzelf sluit zodra het weer groen is. Drift is
daarmee geen gevoel meer, maar een issue met een timestamp.

Werkt het? De nulmeting over acht repository's leverde 63 bevindingen
op — geen enkele pagina had een eigenaar of reviewdatum. Na de
remediatie: nul bevindingen, en de gates houden dat zo. Mooiste detail:
bij de uitrol vonden de uitvoerbare doc-claims meteen twee echte fouten
in bestaande documentatie. De controle bewees zichzelf op dag één.

### Mechanisme 3: agents krijgen context mét herkomst

Nu het fundament klopt, kun je er agents op laten staan. We serveren de
geaggregeerde documentatie aan agents via een [MCP-server](https://modelcontextprotocol.io/)
met drie read-only tools: componenten opsommen, zoeken, en een pagina
lezen.

De crux zit in wat er bij elk antwoord meekomt: **herkomst**. Component,
pagina, eigenaar, reviewdatum en een directe link naar de bron. De
werkinstructie voor de agent is expliciet: de handboek-inhoud gaat
boven modelkennis, en spreekt het model de pagina tegen, dan wint de
pagina — en flagt de agent de discrepantie in plaats van haar weg te
redeneren.

Dat draait de dynamiek om. In plaats van een agent die per sessie
context bij elkaar scharrelt en gaten opvult met aannames, heb je een
agent die citeert. Elke uitspraak is herleidbaar tot een pagina, een
eigenaar en een datum. En omdat de MCP-server exact dezelfde bronlijst
leest als het portaal, bestaat er geen tweede waarheid die stiekem kan
afwijken.

De laatste laag is een operatie-cataloog per repository: welke
handelingen mag een agent autonoom doen, welke alleen als voorstel,
welke vereisen een mens, en welke zijn verboden. Met als sluitregel:
**staat het niet in het cataloog, dan is een mens vereist.** Pushen en
productie-mutaties doet altijd een mens.

### Van documentatie naar gesprek: praat met je cluster

Toen dit eenmaal stond, bleek het patroon nog een deur te openen —
misschien wel de belangrijkste. Documentatie die actueel, herleidbaar
en machine-leesbaar is, is precies het fundament dat een chatbot nodig
heeft om nuttig te zijn in plaats van gevaarlijk.

Iedereen die weleens een taalmodel iets over de eigen infrastructuur
heeft gevraagd, kent de twee smaken:

**Jij:** "Welke image-tag draait de Nextcloud-deployment op productie?"

**Bot zonder grondwaarheid:** "Waarschijnlijk `latest`, of misschien
28.0.0 — die is recent uitgekomen…"

**Bot mét grondwaarheid:** raadpleegt de MCP-server, leest de
deployment-configuratie en de bijbehorende handboekpagina, en
antwoordt: "28.0.2, uitgerold op 11 juli; de chart-values staan in
deze repo — bron: pagina *deployments*, eigenaar platform-team, laatst
gereviewd deze maand."

Het eerste antwoord is een gok met een stellige toon — de gevaarlijkste
combinatie die er bestaat. Het tweede is een citaat met een voetnoot.
Zelfde model, zelfde vraag; het verschil is uitsluitend de laag
eronder.

Dat maakt dit patroon de natuurlijke basis voor een assistent op je
platform: praten met je cluster-infra zoals je praat met die ene
devops-collega die alles weet — óók als die collega met vakantie is.
Met twee verschillen in het voordeel van de bot: hij geeft bij elk
antwoord zijn bronnen, en hij mág niets. Lezen, zoeken, citeren —
muteren staat niet in zijn cataloog, en wat niet in het cataloog staat,
vereist een mens.

### Wat het oplevert

- **Documentatie die niet ongemerkt kan verouderen.** Elke pagina heeft
  een eigenaar en een houdbaarheidsdatum, en een wekelijkse controle
  die aan de bel trekt.
- **Wijzigingen die niet ongetest binnenkomen.** De push wordt fysiek
  tegengehouden tot code, tests en docs kloppen.
- **Agents die citeren in plaats van gokken.** Grondwaarheid met
  herkomst, en heldere grenzen aan wat ze zelfstandig mogen.

En er is een bijvangst die in gereguleerde omgevingen géén bijzaak is:
elke run-log van deze controles is direct bruikbaar als bewijs dat
gedocumenteerde informatie actueel wordt gehouden — een verplichting
die je in een ISO 27001-audit anders met handwerk en goede bedoelingen
moet aantonen. Hier is het bewijs een bijproduct van gewoon werken.

### De nuchtere slotsom

Niets van het bovenstaande is spectaculair. Front matter, pre-push
hooks, een cron-job, een zoekfunctie. Dat is precies het punt. De
verleiding bij "AI-ready documentatie" is om iets indrukwekkends te
bouwen — vectordatabases, automatische samenvattingen, gegenereerde
docs. Wij kozen de andere kant op: maak de documentatie zelf
betrouwbaar, controleerbaar en vers, en geef agents een saaie,
voorspelbare leesinterface met bronvermelding.

Levende documentatie is geen documentatie die zichzelf schrijft. Het is
documentatie die niet kán liegen zonder dat er ergens een lampje gaat
branden.
