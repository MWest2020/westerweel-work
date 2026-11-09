---
title: "Bazibo: vier megabyte, geen tracker"
date: 2026-11-09
draft: false
tags: ["bazibo", "soevereiniteit", "privacy", "open source", "kinderen", "apps"]
translationKey: "bazibo-vier-megabyte"
summary: "Een kinderspelletjes-app van vier megabyte, zonder account, cookies of trackers. Wat ik leerde van klein bouwen, waarom alles op het toestel blijft, en waarom de volledige versie één euro kost."
---

*Over Bazibo, een app met spelletjes voor kinderen, en wat ik leerde
door hem zo klein en zo saai mogelijk te houden.*

Het begon met een bubble shooter op de telefoon, samen met mijn kind.
Het spel zelf was leuk, maar het zat vol reclame. Toen dacht ik: dit
kan anders.

Dat werd [Bazibo](https://bazibo.nl). Zes spellen voor kinderen van 3
tot 10 jaar: Bubbels schieten, Dogudoku, Picturedoku, Vier op een rij,
Slangetje en Kleurplaten. Klok kijken komt eraan. Alles in het
Nederlands en Engels. De naam komt van *bāzi*, het Perzische woord voor
spel.

## Vier megabyte

De Android-app is ongeveer 4 megabyte. De webversie is minder dan één.
Veel spelletjes-apps in de store zijn tientallen tot honderden
megabytes. Dat verschil zit niet in slimmigheid, maar in wat je
weglaat.

Bazibo is gewoon HTML, CSS en JavaScript, op een canvas en in SVG. Er
zit geen game-engine in. De bubbels, de hondjes, de mandala's en de
klok zijn in code getekend. De geluiden worden ter plekke gemaakt met
de Web Audio API, er zit geen enkel geluidsbestand in. De enige
plaatjes zijn de app-iconen. En er zit geen reclame-SDK en geen
analytics in. Juist die maken apps groot.

## Alles blijft op het toestel

Bazibo heeft geen account, geen server en geen cookies. We meten niets
en we volgen niemand. De spellen maken geen enkele internetverbinding.

Wat de app onthoudt, zoals sterren, voortgang, kleurplaten en of de
volledige versie gekocht is, staat op het toestel zelf. Hooguit gaat
het mee in de gewone back-up van je telefoon, onder je eigen Google- of
Apple-account. Daar kunnen wij niet bij.

Dat is de soevereiniteit waar ik het vaker over heb, maar dan klein:
de gegevens van je kind blijven van jou, omdat ze nergens anders
heen gaan.

## Eerlijk: dat werkt per toestel

Dit heeft een keerzijde, en die wil ik niet wegmoffelen. Omdat er geen
account is, werkt alles per toestel. Speel je op de telefoon en op de
tablet, dan zijn dat twee aparte voortgangen. Ze worden niet
gesynchroniseerd. Krijg je een nieuwe telefoon zonder back-up, dan
begint je kind opnieuw.

De aankoop raak je niet kwijt. Die staat bij Google Play, en met
hetzelfde account zet je hem terug met "Aankoop herstellen", op elk
toestel.

Wil je de voortgang bewaren, zet dan de gewone back-up van je telefoon
aan (Android: Instellingen › Google › Back-up). Die neemt Bazibo mee,
en op een nieuwe telefoon komt het terug. Binnenkort komt er ook
"Voortgang overzetten": een QR-code op het ene toestel, scannen met het
andere. Zonder server, zonder internet.

En de website? Die draait bij een gewone hostingpartij. Zoals elke
webserver houdt die logbestanden bij met IP-adressen, voor beveiliging
en storingen. Dat staat ook in de
[privacyverklaring](https://bazibo.nl/nl/privacy/). De app zelf gebruikt
de website niet.

## Open source, en één euro

Alle code staat open op
[GitHub](https://github.com/MWest2020/bazibo), onder de MIT-licentie.
Iedereen kan meekijken wat de app doet en wat hij níet doet.

Elk spel heeft een gratis deel. De volledige versie kost één euro,
eenmalig, voor alles. Geen abonnement, geen munten, geen reclame om weg
te kopen. De aankoop zit achter een rekensom voor ouders, zodat een
kind niet per ongeluk iets koopt.

Die euro is voor doorontwikkeling: meer spellen, meer levels. En we
geven een deel terug aan de opensourceprojecten waar Bazibo op leunt,
zoals Capacitor, cordova-plugin-purchase, Playwright en fastlane.
Zonder hen had dit veel meer werk gekost.

## Wat ik leerde

- **Weglaten is makkelijker dan toevoegen.** Geen account betekent geen
  wachtwoorden, geen database en geen datalek. Geen server betekent
  niets om te patchen.
- **Niets verzamelen maakt de store makkelijk.** De formulieren van
  Google voor kinderapps en gegevensveiligheid waren snel ingevuld. Bij
  bijna elke vraag was het antwoord "nee".
- **Tekenen in code schaalt.** Een mandala-generator maakt eindeloos
  nieuwe kleurplaten, zonder dat de app een byte groter wordt.
- **De rand is de echte test.** Een ouderslot, een terugknop die doet
  wat je verwacht, voortgang die niet kwijtraakt na een mislukte start.
  Daar zat het meeste werk.

Ik bouwde het met AI-agents, met per spel een onafhankelijke review
voordat iets live ging. Die reviews vonden steeds dingen die ik zelf
niet had gezien.

Bazibo staat op [bazibo.nl](https://bazibo.nl) en komt binnenkort in de
Google Play Store. De code staat op
[github.com/MWest2020/bazibo](https://github.com/MWest2020/bazibo).
