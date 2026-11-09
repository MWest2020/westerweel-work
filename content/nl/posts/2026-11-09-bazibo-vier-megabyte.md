---
title: "Bazibo: spelletjes zonder reclame, en zonder ons"
date: 2026-11-09
draft: false
tags: ["bazibo", "soevereiniteit", "privacy", "open source", "kinderen", "apps"]
translationKey: "bazibo-vier-megabyte"
summary: "Een spelletjesapp voor kinderen van ruim vier megabyte. Geen account, geen cookies, niks dat naar ons toe gaat. En een euro voor alles."
---

Ik speelde laatst met mijn kind een bubble shooter op mijn telefoon.
Leuk spel, alleen zat het vol reclame. Bubble shooter-code is nou ook
niet bepaald zeldzaam, dus dacht ik: dat maken we zelf. Zonder reclame.

Dat is inmiddels [Bazibo](https://bazibo.nl) geworden. Zes spelletjes
voor kinderen van een jaar of 3 tot 10: bubbels schieten, Dogudoku (een
soort sudoku met hondjes), Picturedoku (sudoku met plaatjes), vier op
een rij, een slangetje dat leert tellen en spellen, en kleurplaten met
mandala's voor de groteren. Klok kijken komt eraan. Alles in het
Nederlands en het Engels.

De naam komt van *bāzi*, Perzisch voor spel. Het klinkt ook een beetje
als gazebo, vandaar het prieeltje in het logo.

## Klein

De Android-app is ruim 4 MB. Op de website is het nog geen megabyte.
Kijk voor de grap eens hoe groot een gemiddelde spelletjesapp in de
store is. Dat loopt al snel in de tientallen of honderden megabytes.

Dat komt niet doordat ik zo slim ben. Er zit gewoon weinig in. Geen
game-engine, geen reclame-SDK, geen analytics. Het is HTML, CSS en
JavaScript. De bubbels, de hondjes en de mandala's worden in code
getekend, en de geluidjes worden ter plekke gemaakt. Er zit geen enkel
geluidsbestand in. De enige plaatjes zijn de app-iconen.

## Niks verzamelen

Geen account, geen server, geen cookies. We meten niks en we volgen
niemand. De spelletjes maken niet eens een internetverbinding.

Voortgang, sterren, kleurplaten en of je betaald hebt: dat staat
allemaal op de telefoon zelf. Het gaat hooguit mee in de back-up die je
telefoon toch al maakt, onder je eigen Google- of Apple-account. Daar
kunnen wij niet bij.

Daar zit wel een nadeel aan. Omdat er geen account is, werkt alles per
toestel. Speelt je kind op de telefoon en op de tablet, dan zijn dat
twee losse voortgangen. Nieuwe telefoon zonder back-up? Dan begint het
weer bij level 1.

De aankoop raak je niet kwijt, die zit bij Google Play. Met hetzelfde
account tik je op "Aankoop herstellen" en alles staat weer open, ook op
de tablet.

De voortgang bewaar je met de gewone back-up van je telefoon (Android:
Instellingen › Google › Back-up). Daarnaast bouw ik "Voortgang
overzetten": je laat een QR-code zien op het ene toestel en scant die
met het andere. Geen server ertussen.

O ja, de website. Die draait bij een gewone hoster, en die houdt zoals
elke webserver logbestanden bij met IP-adressen. Dat staat ook in de
[privacyverklaring](https://bazibo.nl/nl/privacy/). De app zelf praat
niet met de website.

## Open source, en een euro

De code staat op [GitHub](https://github.com/MWest2020/bazibo), onder
MIT. Wie wil, kan precies zien wat de app doet. En wat hij niet doet.

Elk spel heeft een gratis stuk. Voor een euro, eenmalig, krijg je alles:
alle levels en daarna eindeloos nieuwe puzzels. Geen abonnement, geen
munten, geen reclame die je weg moet kopen. Kopen gaat via een
rekensommetje voor ouders, zodat je kind niet zomaar op "kopen" tikt.

Van die euro bouw ik verder. En een deel gaat terug naar de
opensourceprojecten waar dit op draait, zoals Capacitor en de plugin
voor de aankopen. Zonder die mensen had ik dit niet zo snel in elkaar
gezet.

## Wat ik ervan leerde

Weglaten is makkelijker dan bouwen. Geen account betekent geen
wachtwoorden, geen database en geen datalek. Geen server betekent niks
om te patchen.

De formulieren van Google voor kinderapps waren daardoor ook zo
ingevuld. Verzamelt de app gegevens? Nee. Advertenties? Nee. Klaar.

Het meeste werk zat in de randjes. Een terugknop die doet wat je
verwacht. Een slot op de aankoop dat een kleuter niet omzeilt. Voortgang
die niet kwijtraakt als de app een keer raar opstart. Ik heb het met
AI-agents gebouwd, en elk spel liet ik eerst door een aparte agent
nakijken voordat het live ging. Die vond elke keer wel iets.

Spelen kan op [bazibo.nl](https://bazibo.nl). In de Play Store staat
hij binnenkort.
