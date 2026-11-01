---
# Eén boek = dit ene bestand. De opmaak staat in layouts/boekenclub/;
# hier staat alleen inhoud. Alles hieronder komt van Mark (opdracht of
# interview, 2026-11-01); niets is door de bouwer ingevuld.
# Per inzicht kan er een `nugget` bij (een concreet voorbeeld uit het boek) met
# optioneel `chapter` (bijvoorbeeld "hfst. 7"); die komen van Mark.
# 2026-11-01: het boek is Becoming SRE, niet Seeking SRE (Mark). Hoofdstukken
# alleen waar de inhoudsopgave van Becoming SRE het onderwerp letterlijk noemt.
title: "Becoming SRE"
subtitle: "First Steps Toward Reliability for You and Your Organization"
author: "David N. Blank-Edelman"
publisher: "O'Reilly Media"
year: 2024
weight: 1                 # volgorde in de boekenclub
date: 2026-11-01
photo: ""                 # eigen foto voor de cover (pad onder static/), leeg = typografische cover
quote: ""                 # hooguit één citaat onder de 15 woorden, alleen aangeleverd door Mark

hook: "SRE is geen recept: je zoekt teams op, tot ze jou opzoeken."

insights:
  - title: "Groene en rode vlaggen"
    text: "Scherpe signalen waaraan je ziet of SRE in een organisatie gezond is, of juist niet."
    nugget: "Rood: geen tijd voor engineering, alleen brandjes blussen en postmortems waar niemand iets mee doet. Groen: twee of drie keer per kwartaal on-call, hooguit een paar incidenten per dienst."
    doe: "De groene en rode vlaggen geven richting."
  - title: "Cultuur en profiel"
    text: "Cultuur en het profiel van een SRE: wat voor mens je moet zijn, niet alleen welke techniek je beheerst."
    nugget: "Onderzoeken hoe dingen falen en hoe dat voor de eindgebruiker voelt. SLO's baseer je op gebruikers, niet op eigen drempelwaarden."
    chapter: "hfst. 2"
    doe: "Cultuur is waar we naar zoeken bij nieuwe collega's."
  - title: "Er is geen ‘zo moet het’"
    text: "SRE ziet er niet overal hetzelfde uit. Zoek wat bij jouw organisatie past, met de vlaggen als kompas."
    nugget: "Een SRE-label op DevOps of een L3-servicedesk plakken werkt niet. Het gaat erom wie verantwoordelijk is voor de betrouwbaarheid."
    chapter: "hfst. 12"
  - title: "Van push naar pull"
    emphasis: true
    text: "Mensen en samenwerking staan centraal. Ontwikkelaars die niet van meetings houden, kunnen beter niet aan SRE beginnen. Eerst push je: jij gaat naar de teams. Het doel is pull: de teams komen naar jou. Dat is het teken dat het werkt."
    nugget: "Push: SRE loopt achter het bedrijf aan en wordt lastig gevonden. Pull: teams vragen zelf: moet er niet iemand van SRE bij?"
    doe: "Van push naar pull: daar streven we naar."
  - title: "Toegankelijker dan het Google-boek"
    text: "Leest makkelijker dan Site Reliability Engineering (1e editie), dat vrij snel heel Google-specifiek wordt."

scores:
  - name: "Direct toepasbaar"
    value: 5
    note: "zeker voor startende teams"
  - name: "Diepgang"
    value: 4
    note: "een sterk punt"
  - name: "Leesbaarheid"
    value: 5
  - name: "Houdbaarheid"
    value: 3.6
    note: "over vijf jaar misschien achterhaald, de kern blijft"

for_whom_line: "Voor startende SRE-teams en managers die SRE's aannemen."
for_whom:
  - "Startende SRE-teams"
  - "Product leads en managers die SRE's aannemen"
  - "Iedereen die nieuwsgierig is naar SRE"
not_for_whom:
  - "Mensen buiten tech"

further_reading:
  - title: "The Site Reliability Workbook"
    year: 2018
  - title: "Site Reliability Engineering, 2e editie"
    year: 2026
  - title: "Seeking SRE"
    year: 2018
  - title: "SRE with AIOps"
    year: 2026
question: "Welke zou jij als eerste lezen? Of mis ik er een?"
---
