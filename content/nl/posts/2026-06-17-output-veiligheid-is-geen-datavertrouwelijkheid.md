---
title: "Ricine breekt je model. Je data niet."
date: 2026-06-17
draft: false
tags: ["ai", "privacy", "security", "rag", "compliance"]
translationKey: "output-safety-vs-data"
summary: "Waarom de populairste AI-veiligheidstest de voordeur beveiligt, maar de achterdeur wagenwijd openlaat. Output-veiligheid en datavertrouwelijkheid zijn technisch twee totaal verschillende mechanismen — en juist het door elkaar halen ervan zit achter de verwarring op de werkvloer. Hier is hoe modellen écht met je data omgaan, en wat je in plaats van het toneelstukje moet regelen."
---

*Waarom de populairste AI-veiligheidstest de voordeur beveiligt, maar de
achterdeur wagenwijd openlaat — en wat je in plaats daarvan moet regelen.*

Wanneer organisaties de veiligheid van een AI-model testen, kijken ze
vrijwel altijd naar dezelfde kant van de medaille: **wat komt eruit?**

In mijn geval, na te veel *Breaking Bad*: hoe maak je ricine? Het model
weigert netjes. Die test slaagt. De conclusie die men vervolgens op de
werkvloer trekt, is logisch maar gevaarlijk: "De filters werken, dus het
systeem is veilig."

Maar hier zit de cruciale denkfout. De ricine-test bewijst dat de
**output-beveiliging** op orde is. Het model spuugt geen gevaarlijke
dingen uit. Maar die test beantwoordt misleidend genoeg de verkeerde
vraag. Want de échte vraag voor een organisatie is niet wat er *uit* het
model komt, maar wat er met de data gebeurt die je er **in** stopt.

Output-veiligheid en datavertrouwelijkheid zijn technisch twee totaal
verschillende mechanismen. Ze hebben niets met elkaar te maken. Terwijl
jij gerustgesteld bent dat het model geen biowapens genereert, kan jouw
gevoelige input aan de achterdeur alsnog je organisatie verlaten.

Om te zien hoe dat werkt, moeten we kijken naar een discussie die ik
laatst voerde bij een organisatie op de werkvloer.

### De aanleiding: een gesprek in een gereguleerde sector

Dit stuk komt voort uit een gesprek met een organisatie in een streng
gereguleerde sector. Een team van professionals werkte daar al een tijdje
organisch met taalmodellen om teksten te analyseren en interne documenten
te vergelijken. Heel verstandig en efficiënt werk.

Maar bij het verwerken van documenten met gevoelige informatie begon het
te kriebelen. De interne richtlijnen bevatten data die bewust niet publiek
is. De ene helft van het team was dan ook terughoudend: "Gaat deze data
het model niet in, en kan een ander het er dan later weer uithalen?" De
andere helft suste de boel: "Welnee, je krijgt er geen gekke dingen uit,
de filters zijn heel streng. Het model weigert immers ook als je om enge
dingen vraagt."

Zie je wat hier gebeurt? De geruststelling over wat er *uit* gaat (geen
misbruik via de output), maskeert het risico van wat er *in* gaat
(datavertrouwelijkheid van de input). Want het team werkte met losse
*consumer*-abonnementen (ChatGPT Plus). En dat is precies het lek aan de
achterdeur.

### Hoe een model getraind wordt (en waarom het bevroren is)

Om te begrijpen waarom die voordeur-filter je input niet beschermt, moeten
we kijken naar hoe zo'n model ontstaat. Een taalmodel wordt in twee fasen
getraind, en allebei zijn ze **offline**.

Eerst **pretraining**: het model leert op enorme hoeveelheden tekst telkens
het volgende stukje tekst te voorspellen. Maanden rekenen, hele zalen
GPU's. Wat eruit komt zijn de *gewichten* — de geleerde parameters,
miljarden getallen. Daarna **post-training**: het bijschaven van het gedrag
met menselijke feedback en regels (RLHF, Constitutional AI), inclusief de
veiligheidstraining die het model leert om bijvoorbeeld biowapens te
weigeren.

Het punt dat je moet onthouden: trainen is een apart, kostbaar, eenmalig
proces. Het model dat jij gebruikt is een bevroren momentopname van na die
training. Het *leert niet bij* terwijl je ermee praat. Je prompt verandert
live geen enkel gewicht.

> Wil je dit echt zien in plaats van geloven? Speel met
> [bbycroft.net/llm](https://bbycroft.net/llm) — een interactieve
> 3D-doorsnede van een GPT terwijl het tokens verwerkt — en kijk de
> transformer-reeks van [3Blue1Brown op
> YouTube](https://www.youtube.com/watch?v=wjZofJX0v4M). Een uur
> tijdsinvestering, en je neemt nooit meer een marketingbelofte voor zoete
> koek aan.

### Hoe je data in (of langs) een model komt

Er zijn drie manieren om een model "iets van jouw organisatie te laten
weten". Mensen beoordelen ze op één as, terwijl er twee zijn — en juist het
door elkaar halen van die twee zit achter de verwarring op de werkvloer.

- **As 1 — belandt je data in de *gewichten*?** Wordt ze permanent
  onderdeel van het model, waar een ander haar er later via memorisatie uit
  zou kunnen trekken?
- **As 2 — verlaat je data je *pand*?** Gaat ze naar de servers van een
  derde partij, buiten je eigen beheer en jurisdictie?

Tegen die twee assen zien de drie methoden er zo uit:

- **Fine-tuning / continued training** — jouw data wordt in een (kopie van
  het) model gebakken. De gewichten veranderen (as 1: ja) en het draait bij
  een externe provider (as 2: ja). Wat erin zit, kan eruit komen:
  memorisatie is reëel, geen hypothese.
- **RAG (retrieval-augmented generation)** — je documenten staan in je
  eigen vectorstore; de gewichten blijven onaangeraakt (as 1: nee). Maar
  let op: bij elke vraag worden de relevante stukken opgehaald en *in de
  prompt naar het model gestuurd*. Draait dat model in de cloud, dan
  verlaten die stukken — inclusief je gevoelige interne data — alsnog je
  pand (as 2: ja). RAG beschermt de gewichten, niet automatisch de
  vertrouwelijkheid.
- **In-context / prompting** — je plakt context in het venster van dat ene
  gesprek. Eenmalig, geen gewicht-update (as 1: nee). Maar de prompt gaat
  wél naar de provider (as 2: ja).

Hier zit de denkfout die ik op de werkvloer hoorde. "Onze data wordt het
model en komt er bij een ander weer uit" is een **as 1**-angst, en die
geldt inderdaad vooral bij fine-tuning. Maar de gevoelige interne data uit
de praktijkcase is bijna volledig een **as 2**-probleem: de data verlaat je
pand, los van de vraag of er ooit op getraind wordt. En as 2 speelt bij
élke cloud-call — prompting, RAG én fine-tuning. Daarom lost "we doen
alleen RAG, geen fine-tuning" het vertrouwelijkheidsvraagstuk niet op.

### Inference is geen training — maar logging kan dat alsnog worden

We zagen net dat een prompt live geen gewicht verandert. Toch is er een
indirecte route terug naar as 1, en die loopt niet via het gesprek maar via
de *logs*. Je prompt belandt alleen in een toekomstig model als (a) de
provider je input opslaat én (b) die opslag in een latere trainingsronde
wordt meegenomen. Dat hangt volledig af van je abonnementsvorm — niet van
of je betaalt, maar van het *soort* account:

- **Commercieel** (API, Enterprise, Business): standaard wordt er *niet* op
  getraind. Zie bijvoorbeeld Anthropic's
  [privacypagina](https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training)
  of OpenAI's [enterprise-privacy](https://openai.com/enterprise-privacy/).
- **Consumer** (Free / Pro / Plus): standaard wél, tenzij je actief kiest
  voor een opt-out via de instellingen.
- **De feedbackknop**: let op — een duim omhoog of omlaag kan dat specifieke
  gesprek alsnog de trainingspool in trekken, *óók* op enterprise (zie deze
  [uitleg met
  bronnen](https://secureprivacy.ai/blog/gpt-5-training-data-opt-out)).

Dit "Shadow AI"-gat van losse consumentenaccounts op de werkvloer is in de
praktijk het werkelijke risico. Als data de trainingspijplijn in gaat, kan
ze er via memorisatie ook weer uit komen. In de Reddit-rechtszaak tegen
Anthropic werd bijvoorbeeld aangevoerd dat een model verwijderde posts
vrijwel woordelijk kon reproduceren. Dáárom is je contractvorm de control —
niet het modelgedrag aan de voorkant.

### Guardrails beschermen de verkeerde kant

Die ricine-weigering komt uit misbruik-controls. De eerste laag zit in de
gewichten (post-training). De tweede laag zijn **Constitutional
Classifiers**: een aparte filterlaag *óm* het model heen die zowel de input
als de output scant en blokkeert. Dit is geen wijziging aan de gewichten,
het is een guardrail eromheen (lees de [research
paper](https://arxiv.org/abs/2501.18837) of Anthropic's [eigen
uitleg](https://www.anthropic.com/research/constitutional-classifiers)).

Die classifiers zijn geen schijnvertoning — ze blokkeren aantoonbaar
jailbreaks en doen precies wat ze beloven. Maar let op *wélke* kant ze
beschermen: ze regelen **output-veiligheid** (wat het model naar buiten
brengt). Ze zeggen helemaal niets over **datavertrouwelijkheid** (wat er
met jouw input gebeurt). Het zijn echte controls, alleen op de verkeerde as
voor jouw vraag. De ricine-test meet het eerste en stelt je onterecht
gerust over het tweede. Dát is het toneelstukje: niet de guardrail, maar de
test als bewijs van databeveiliging.

Zelfs de belofte "wij wissen data na 30 dagen" is geen natuurwet. In de New
York Times-rechtszaak moest OpenAI bepaalde data juist bewaren, dwars door
het eigen verwijderbeleid heen
([toelichting](https://openai.com/index/response-to-nyt-data-demands/)).
Maar kijk wie er buiten het bevel viel: Enterprise-, ZDR- en EU-klanten.
Het bevel sneed door de standaard-bewaarbelofte, maar precies de tier- en
regio-controls hielden stand. Dat is geen kanttekening bij mijn advies —
het is het bewijs ervoor. (Het bevel is inmiddels grotendeels teruggedraaid,
maar het punt blijft staan: *delete* is een UI-feature, geen garantie.)

### Wat moet je dan wél regelen?

Niet de voordeur testen met enge vragen. Wel het juridische en technische
kader aan de achterkant inrichten:

1. **DPIA** (gegevensbeschermingseffectbeoordeling) vóór je begint. Dit
   dwingt je team om de risico's scherp te krijgen.
2. **Verwerkersovereenkomst (DPA)** met elke provider die persoonsgegevens
   raakt. Geen DPA = onrechtmatige verwerking.
3. **Zero Data Retention (ZDR)** expliciet contracteren voor gevoelige
   flows. ZDR betekent dat input en output na het antwoord niet worden
   opgeslagen. Let op: dit staat nooit vanzelf aan — je moet het per
   endpoint aanvragen. Zonder ZDR-contract geldt ook op een API vaak een
   retentieperiode voor misbruikdetectie.
4. **EU-region / data residency** hard contractueel vastleggen.
5. **Dataminimalisatie en pseudonimisering**: geen herleidbare
   persoonsgegevens in prompts als het niet strikt nodig is.

Werk je nu op losse consumer-abonnementen? Dan is de snelste winst de
simpelste: stap over naar **ChatGPT Business**. In euro's is dat zelfs iets
goedkoper dan losse Plus-abonnementen, training staat er standaard uit, en
je krijgt beheer en overzicht over wat er gebeurt. Let wel: "niet trainen"
is niet hetzelfde als "niets bewaren" — voor de écht gevoelige flows blijft
de volgende vraag de belangrijkste.

### De vraag die iedereen overslaat

En tot slot de belangrijkste vraag:

**Heb je voor déze taak überhaupt een cloud-model nodig?**

Voor het redigeren, samenvatten, structureren of vergelijken van teksten?
Nee. Een lokaal model — [Ollama](https://ollama.com) op een fatsoenlijke
GPU, of een in de EU gehoste private instance — doet dat prima.

Als de data je eigen infrastructuur nooit verlaat, vervalt zowel as 1 als
as 2 in één klap: geen training, geen retentie, geen jurisdictievraag. Dat
lost meteen ook die hele discussie op de werkvloer op. Gaat de data het huis
niet uit, dan vervalt het risico waar de voorzichtige collega's over vallen
— en hadden de anderen óók een punt, want informatie is via genoeg andere
wegen te misbruiken. Maar dat is een argument over de output. Over wat je
aan de inputkant weggeeft, zegt het niets. Dus los je het op aan de
inputkant.

De veiligste data is de data die je huis nooit verlaat. En een model dat
ricine weigert aan de voordeur, beschermt de data aan de achterdeur niet.
Regel het kader, niet het toneelstukje.
