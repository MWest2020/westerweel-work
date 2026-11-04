---
title: "Context is alles"
date: 2026-11-04
draft: false
tags: ["ai", "agents", "context", "sre", "soevereiniteit", "lokale modellen"]
translationKey: "context-is-alles"
summary: "Een agent die gokt, mist meestal context, geen intelligentie. Van een hub voor infra-repo's naar SREna, een lokale SRE-agent: de kennisbank gaat hallucineren tegen, niet het model."
---

*Over de kennisbank als het eigenlijke verschil, en waarom die de
sleutel is tot een soevereine SRE-agent.*

Een paar maanden geleden vroeg iemand aan een agent hoe je een
onderdeel van ons cluster upgradet. De agent gaf een keurig antwoord in
stappen, met de juiste commando's en een paar verstandige
waarschuwingen. Het klonk als iemand die het al tien keer had gedaan.

Alleen stond de procedure al gedocumenteerd, in een repo die de agent
gewoon kon lezen. De agent had die niet opgezocht. Hij had zelf iets
plausibels in elkaar gezet uit modelkennis en wat rondzoeken. Niemand
kon herleiden waar het antwoord vandaan kwam, wie het had gecontroleerd
of hoe oud het was.

Het model had de verkeerde context, of eigenlijk geen context.
Sindsdien vat ik bijna alles wat ik met agents bouw samen in één zin:

**Context(management) is alles.**

### Eén ingang, en een vaste volgorde

In [een eerder stuk](/posts/2026-07-14-levende-documentatie-met-gates-en-agents/)
beschreef ik hoe we documentatie "levend" maakten: docs naast de code,
een afdwingbaar contract, gates, en een MCP-server die agents de
geaggregeerde documentatie geeft *met herkomst*. Eigenaar, reviewdatum,
bron. Daarna kwam de vraag hoe je zorgt dat een agent die server ook
echt gebruikt.

Het antwoord is een MCP: die laad je in, en die stuurt de agent naar de
kennisbank. Een sessie start in de hub, de coördinator voor een stuk of
tien infrastructuur-repo's. Samen regelen ze drie dingen.

1. Wat erin gaat: elke vraag over een component, het cluster, een
   versie of een procedure begint met een zoekactie in de kennisbank.
   Dat is de eerste handeling: vóór `grep`, vóór `kubectl` en vóór
   modelkennis. Een treffer ís het antwoord, met bronvermelding. Levert
   de kennisbank niets op, dan mag de agent zelf zoeken, maar dan moet
   hij zeggen dat de kennisbank niets had.
2. In welke volgorde: die regel stond eerst alleen in de instructies.
   Toen zagen we in een lange sessie dat hij wegzakte: instructies in
   gewone tekst verdampen naarmate de context voller raakt. Nu spuit een
   hook de regel bij *elke* prompt opnieuw in. Dat kost vier regels
   tekst en een paar tokens per beurt.
3. Wat eruit blijft: elke repo heeft een cataloog van operaties die een
   agent zelfstandig mag doen, en wat daar niet in staat, vraagt hij
   eerst. Muterende clustercommando's zijn technisch geblokkeerd. En de
   regels zelf (instructies, hooks, permissies) zijn voor de agent
   alleen-lezen. Een agent die zijn eigen kooi mag aanpassen, zit niet
   in een kooi.

Sindsdien verzint een agent zo'n procedure nauwelijks nog. Niet omdat
het model beter werd,
maar omdat de context dat werd.

### Thuis: hetzelfde patroon

Thuis werk ik op dezelfde manier, alleen in een ander domein.

- Mijn [handbook](https://github.com/MWest2020/handbook) is de hub van
  al mijn eigen repo's. In de beschrijving staat het letterlijk: *"It's
  where I tell agents to go."* De documentatie leeft in de projecten
  zelf, en de hub bevat alleen de kaart, de specs en de pijplijn.
- [Habitat](https://github.com/MWest2020/habitat) laat Claude
  Code-agents zelfstandig werken op een thuiscluster van drie
  mini-pc's ([homelab](https://github.com/MWest2020/homelab)). Ze
  werken in een kooi: uitgaand verkeer staat dicht behalve naar een
  allowlist, ze hebben minimale rechten en elke run laat een audit-spoor
  achter in git. Ook hier geldt: agents verbouwen hun eigen kooi niet.
- [Ratatoskr](https://github.com/MWest2020/ratatoskr) is de chatlaag
  daarboven. Ik wilde, in mijn eigen woorden, *"eigenlijk maar met één
  agent spreken"*. Die ene agent routeert door naar specialisten
  (bouwer, reviewer, architect, red team). Hun definities staan op één
  plek in het handbook, dus de bouwer in de chat is dezelfde als die in
  het cluster.
- Mijn tweede brein is een markdown-en-git-kluis met een deterministische
  kern. Planning, datums en matching zijn gewone Python, en het taalmodel
  zit alleen aan de randen. Elke bewering verwijst naar een bron, en
  bronnen zijn onveranderlijk.

Overal komt het op hetzelfde neer: de agent begint bij de kennisbank en
blijft binnen grenzen die hij zelf niet kan verschuiven. De kwaliteit
van zijn werk hangt vooral af van wat het model te zien krijgt.

### De logische volgende stap: een SRE-agent die lokaal draait

Als het vooral om context draait, en de context voor SRE-werk bestaat
uit logs, incidenten, configuraties en runbooks, dan is die context
precies wat je het minst graag de deur uit stuurt.

Daarom bouw ik aan SREna: een SRE-agent die volledig lokaal draait. Het
model, de gateway en de gesprekken staan allemaal op de eigen machine,
en er gaat geen operationele data naar een cloudmodel. Ze krijgt
dezelfde behandeling als de agents hierboven: een kennisbank als
grondwaarheid, herkomst bij elk antwoord, en alleen bronnen waarvoor
expliciet toestemming is gegeven.

De potentie is groot. Een collega die midden in de nacht een incident
krijgt, kan het gesprek voeren met iemand die de runbooks, de
dashboards en de geschiedenis kent, met bronvermelding, zonder dat er
één logregel het gebouw verlaat.

Ik ben daar wel eerlijk over: we zitten in de evaluatiefase. Er zijn
nog geen gebruikers. We vergelijken dezelfde agents met een cloudmodel
als baseline, en het lokale model haalt die baseline nog niet. De
modelkeuze is nog open. Daar is te weinig data voor, en ik verwacht pas
in het eerste kwartaal van 2027 een besluit.

Echte anekdotes heb ik dus nog nauwelijks. Ze is er gewoon nog niet. Wat ik wel al zie, is dat annoteren werkt. Elke bron in de kennisbank krijgt een label. Goud is door een mens bevestigd, zilver komt uit een bron maar is niet nagekeken, en brons is puur AI. Wat als goud gemarkeerd staat, neemt ze beter mee en weegt ze zwaarder. En omdat elk stuk kennis een label heeft, geeft ze eerlijk aan waar haar antwoord vandaan komt. Dat helpt ook bij de evaluatie: je ziet welke agent zijn werk goed deed en welke niet. Het idee is niet van mij. Ik heb het geleend van Google, uit hun werk aan AI voor SRE.

### Wat een lokaal model je leert

Een groot cloudmodel is vergevingsgezind. Ontbreekt er een bron, dan
vult het de leemte met brede kennis, en vaak klinkt dat ook nog goed.
Precies wat die agent uit de opening deed. Een kleiner lokaal model
doet dat ook, maar slechter. Daardoor valt het gat op.

Dat voelde in het begin als een tegenvaller. Inmiddels zie ik het als
het nuttigste wat het lokale model doet: het is een eerlijke spiegel
van je context.

Hallucinaties hebben een adres. Als het model iets verzon, kwam dat
meestal door een bron die ontbrak of niet klopte. Het probleem zat in
de kennisbank, en daar is het ook op te lossen.

Het contextvenster is een budget. Alles wat je erin stopt, gaat af van
iets anders. Een te ruime zoekactie of een volledig logbestand duwt de
instructies eruit, en dan krijg je afgebroken of onzinnige output.
Kleine, afgebakende zoekacties werken beter dan alles in één keer.

Een model dat "maar wat probeert", heeft te veel ruimte. Bij toolcalls
ging het mis zodra het model zelf moest raden welke aanroep zinvol was.
Waar we nu op inzetten: minder tools, gestructureerde output, en
citaten die mechanisch worden gecontroleerd, zodat het model eerder
weigert dan gokt.

Permissies zijn ook context. Toegang tot informatie is iets anders dan
toestemming om die aan een model te geven, en dat is weer iets anders
dan toestemming om haar te delen. Die grens leg je vast in de kennisbank
zelf, zodat een prompt die niet hoeft te onthouden.

Pin alles, en meet zelf. Leg het model vast op een exacte revisie, en
pin de runtime samen met al zijn afhankelijkheden. Kiezen doe je op wat het
model op je eigen machine doet; de benchmark van de maker zegt weinig
over hoe het op jouw hardware en jouw taken presteert. En dat betekent eval-runs, heel veel eval-runs.
Zonder baseline is elke indruk een gevoel.

De grootste les past in één zin: de kennisbank is wat hallucineren
tegengaat, niet het model.

### Context is het eigenlijke werk, en het is van jou

Met een cloudmodel kun je slordig zijn met context en kom je er vaak
mee weg. Een lokaal model straft dat af. Maar het werk dat je doet om
een lokaal model bruikbaar te maken (bronnen cureren, herkomst
vastleggen, de volgorde afdwingen, grenzen trekken) maakt *elk* model
beter. En dat werk blijft staan als je van model wisselt.

Dat is voor mij de kern van soevereiniteit bij AI. Waar het model
draait telt, en wie de context bezit telt nog meer: je kennis, waar die
vandaan komt en waar de grenzen liggen. Die context staat in gewone
bestanden in git en is van jou. Daardoor wordt het model vervangbaar.
In het eerste kwartaal van 2027 valt de modelkeuze. De context gaat
gewoon mee.

Context(management) is alles.

---

*P.S. Thuis draai ik geen grote lokale modellen. Daar heb ik de hardware
(nog) niet voor, dus het zware werk loopt via mijn Claude-abonnement.
Wat er wel lokaal draait, zijn hele kleine, gespecialiseerde modellen. Heeft iemand nog
een machine met heel veel geheugen over die een goed thuis zoekt? Ik
ken een homelab dat graag wil meedoen.*
