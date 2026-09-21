---
title: "Je soevereiniteitstoets is een momentopname. Je voetafdruk niet."
date: 2026-09-21
draft: true
tags: ["soevereiniteit", "open source", "dns", "meten", "overheid"]
translationKey: "wanderer-meten"
summary: "De DICTU-toets werkt op wat je opgeeft: je kiest een leverancier, loopt vijf dimensies langs, krijgt een score. Nuttig — maar het meet wat je denkt te hebben. Wanderer meet wat er staat: DNS, mail, certificaten, het pad dat je verkeer aflegt, en wie er eigenlijk aanspreekbaar is. Passief, open source, en eerlijk over wat het niet weet. Met een publieke demo en de uitkomst van mijn eigen domein, die niet meeviel."
---

*Een scanner die de extern zichtbare voetafdruk van een organisatie meet —
en waarom "onbekend" nooit "goed" mag worden.*

De soevereiniteitstoets van DICTU, en afgeleiden als
[soevereiniteitstoets.nl](https://soevereiniteitstoets.nl), werken op
**opgegeven** diensten. Je kiest een leverancier, loopt vijf dimensies en
vijftien criteria langs, en er komt een score uit. Dat is nuttig werk, en het
heeft twee grenzen.

De eerste: het is een momentopname. De tweede, en die is lastiger: het gaat
ervan uit dat je wéét welke diensten meedoen. In de praktijk weet niemand dat
precies. Elke gemeente heeft SaaS die ooit als pilot binnenkwam, een
MX-record dat ergens heen wijst zonder dat iemand nog weet waarom, een CDN dat
de leverancier koos, en een inlogscherm dat stilletjes federeert naar een
Amerikaanse identiteitsprovider.

Daar is geen vragenlijst tegen bestand. Daarvoor moet je kijken.

## Wat het meet

[Wanderer](https://github.com/MWest2020/wanderer) kijkt van buitenaf naar één
domein en beantwoordt zeven vragen, elk over een stukje van de keten:

- **Waar staat de hosting?** De apex-adressen, hun AS-nummer en het land van
  registratie.
- **Waar loopt de mail?** De MX-hosts, en waar díé staan.
- **Wie draait de DNS?** De nameservers, en hun jurisdictie.
- **Welke weg legt het verkeer af?** Een traceroute per hop, met AS en land —
  want verkeer tussen twee Nederlandse punten kan prima via Frankfurt of
  Ashburn lopen.
- **Wie zit ervoor?** CDN's en hyperscalers in het pad.
- **Wat laadt de pagina mee?** Externe bronnen van derde partijen.
- **Wie gaf het certificaat uit?** De CA die je cryptografische identiteit
  beheert.

Daar is deze maand een achtste bij gekomen, en dat is de vraag die de anderen
compleet maakt: **wie is aanspreekbaar, en kun je die partij bereiken?** Een
domein waarvan de registrant achter een privacyproxy zit, waarvan het
contactadres in de DNS-zone bounced, dat via een anonieme reseller loopt en
geen `security.txt` publiceert, is onaanspreekbare infrastructuur. Voor een
publieke organisatie is dat net zo goed een soevereiniteitsgebrek als een
Amerikaanse nameserver: incidentafhandeling, overdracht en juridische stappen
hangen allemaal op een identificeerbare tegenpartij.

## Passief, en dat is een ontwerpkeuze

Alles wat Wanderer doet, is wat een gewone bezoeker ook doet: DNS-vragen,
RDAP-opvragingen, een TLS-handdruk, een HTTPS-verzoek, een traceroute. Geen
poortscans, geen brute force, geen SMTP-verbindingen om te kijken of een
mailbox bestaat.

Dat laatste is een bewuste grens. Je zou het contactadres uit de DNS-zone
kunnen verifiëren door een SMTP-gesprek te openen zonder mail te sturen.
Technisch kan het. Maar het verschijnt in abuse-logs, en dan is je
soevereiniteitsscanner iets geworden dat eruitziet als verkenning voor een
aanval. Wanderer controleert dus of het maildomein bestaat en mail accepteert,
en **zegt erbij dat aflevering niet is gecontroleerd**.

## Eerlijk zijn over wat je niet weet

Dit is het deel waar ik het meeste over heb nagedacht.

Een scanner die "nee" zegt waar hij "ik weet het niet" bedoelt, is erger dan
geen scanner. Mensen gaan dingen repareren die niet stuk zijn, en wat wél stuk
is verdwijnt in de ruis. Daarom kent Wanderer vier antwoorden — ja, nee,
onbekend, en niet van toepassing — en wordt een onbekend nooit stilzwijgend
een ja.

Het scherpste voorbeeld zit bij `.nl`. SIDN publiceert geen registrantgegevens
in RDAP, voor niemand. De vraag "is de registrant herkenbaar als jouw
organisatie?" is voor élk Nederlands domein dus principieel niet te
beantwoorden via de officiële weg. Een scanner die daar "nee" van maakt,
rekent de Rijksoverheid iets aan wat het beleid van het register is. Wanderer
zegt: **n.v.t. — het register publiceert registrantgegevens niet voor .nl**,
en laat de andere vragen het verhaal dragen. Er zijn omwegen — registrar-API's,
scrapen — maar die passen niet bij een instrument dat zijn eigen grenzen
serieus neemt.

Hetzelfde geldt voor de verloopdatum van een domein: die publiceert SIDN
evenmin. Dat is geen gat in de meting, dat is het passieve plafond. En een
plafond hoort zichtbaar te zijn, niet weggerekend.

## Van één antwoord naar een vloot

Voor één domein wil je een zin, geen tabel: *"Nee — de mail loopt via een
Amerikaanse aanbieder"*. Die zin staat bovenaan, en eronder vouwt het bewijs
open: welke waarneming, welke regel, welke grens.

Zodra je veertig domeinen naast elkaar zet, werkt ja/nee niet meer — dan staat
alles op "nee" zodra er één ding misgaat, en zie je niet wie er beter voor
staat. Daar staat dus **x van n**: hoeveel vragen soeverein beantwoord zijn van
het aantal dat beantwoord kón worden, met de onbeantwoorde apart ernaast. En
altijd met de zwaarste openstaande bevinding erbij, want een score die alles
even zwaar telt, nodigt uit om het makkelijkste gat te dichten.

Klik je door naar een regel, dan legt die zichzelf uit: wat hij controleert,
waarom het uitmaakt, welke waarneming hij gebruikt, en **welke grens het
oordeel bepaalt**. Dat laatste is geen detail. "Verloopt binnen 30 dagen" of
"boven 90 dagen" zijn aannames, en een aanname die je niet kunt zien, kun je
niet weerleggen. En bij elk negatief oordeel staat één concrete handeling —
niet "zorg voor een herkenbare registrant", maar "vraag je registrar de
privacyproxy op dit domein te verwijderen".

## Mijn eigen domein scoort niet best

Er staat een publieke demo op
[wanderer.westerweel.work/demo](https://wanderer.westerweel.work/demo). Eén
vooraf ingesteld domein, geen inlog, geen scanknop — een open scanknop zou van
zo'n instantie een scanner-voor-derden maken, en dat is precies wat je niet
wilt bouwen.

Dat domein ben ik zelf. En het oordeel is:

> **Nee — Hosting: hosted at Cloudflare — apex IPs in CA, CA, CA, CA (outside
> EEA)**

Dat is ongemakkelijk en het is het punt. Ik bouw een instrument dat
afhankelijkheid van Amerikaanse partijen aanwijst, en mijn eigen infrastructuur
hangt achter één Amerikaanse edge: de DNS-zone, de apex-adressen, en elke
publieke ingang van mijn cluster. Ik heb dat deze week opgeschreven als besluit
in plaats van als gewoonte: voorlopig blijft het zo — er zijn geen gebruikers
die er risico op lopen — met drie momenten waarop het terugkomt. Zodra iemand
anders dan ik inlogt. Zodra er persoonsgegevens over lopen. Zodra ik dit aan
derden aanbied.

Wat ik ondertussen wél doe: mijn eigen namen staan op hetzelfde wekelijkse
scanschema als de domeinen die ik voor anderen bekijk. Een afhankelijkheid die
je kent, verdwijnt namelijk het makkelijkst uit beeld.

## Waar het heen gaat

Wanderer is open source onder de EUPL-1.2. Er is een CLI, er komen deze week
binaries en een GitHub Action bij zodat je het in je eigen pijplijn kunt
draaien — bij jou, op jouw domeinen, zonder dat er iets naar mij toe gaat.

Voor wie het serieus wil gebruiken is er ook een agent die op een host draait
en rapporteert wat er geïnstalleerd staat en waar die machine naartoe praat.
Want de helft van de afhankelijkheden zie je niet van buitenaf.

Interesse om mee te kijken, of om dit op je eigen vloot los te laten? Laat het
weten.
