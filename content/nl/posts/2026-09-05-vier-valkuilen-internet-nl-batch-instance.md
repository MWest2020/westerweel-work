---
title: "De handleiding volgen was precies het probleem"
date: 2026-09-05
draft: false
tags: ["devops", "security", "compliance", "homelab", "tooling"]
translationKey: "internetnl-selfhosting-traps"
summary: "Internet.nl meet of je domein IPv6, DNSSEC, RPKI en TLS goed heeft staan. Wil je dat voor een hele vloot domeinen, dan heb je de batch-API nodig, en die vraagt een account. Zelf hosten kan — maar één variabele in de officiële handleiding sloopt stilletjes al je uitgaand verkeer, en de certbot in het image start niet eens op, dus je certificaat verloopt zonder dat iets alarm slaat. Vier valkuilen, met de exacte foutmeldingen, en wat ze zeggen over documentatie die technisch klopt."
---

*Vier valkuilen bij het zelf draaien van een Internet.nl batch-instance —
en waarom "de documentatie klopt" niet hetzelfde is als "de documentatie
helpt".*

Internet.nl is een van de nuttigste publieke diensten die Nederland heeft.
Je typt een domein in, en je krijgt terug of IPv6, DNSSEC, RPKI, TLS en je
mailbeveiliging op orde zijn. Voor overheden en leveranciers is het geen
vrijblijvend cijfer: het raakt aan de pas-toe-of-leg-uit-lijst, en met NIS2
en de ENISA-kaders erbovenop moet je zulke dingen niet alleen goed hebben
staan, maar ook kunnen aantónen.

Daar wringt het. Aantonen doe je niet met een screenshot van een website.
Een auditor die vraagt "hoe weet je dat dit vorige maand ook zo stond"
heeft niets aan een plaatje. Je wilt een meting die elke dag draait, een
resultaat dat je kunt diffen, en een pipeline die piept als je score zakt.

Dat kan, want de batch-API bestaat. Alleen heb je daar een account voor
nodig, en niet iedereen krijgt er een. Blijft over: zelf hosten. De
documentatie daarvoor is er, is uitgebreid, en klopt op elke regel die ik
heb nagelezen.

En toch stond ik dagen stil.

Wat hieronder staat is geen kritiek op het project. Internet.nl is open
source, goed onderhouden, en de Docker-deployment is beter gedocumenteerd
dan het meeste dat ik in productie tegenkom. Het zijn de vier plekken waar
je de handleiding letterlijk kunt volgen en alsnog met een kapotte instance
eindigt. Ik schrijf ze op met de exacte foutmeldingen erbij, want dat is
wat je intypt bij een zoekmachine als je er middenin zit.

## 1. Eén variabele, twee betekenissen

De batch-handleiding zegt dit:

```
INTERNETNL_DOMAINNAME=example.com \
IPV4_IP_PUBLIC=127.0.0.1 \
IPV6_IP_PUBLIC=::1 \
envsubst < docker/host-dist.env > docker/host.env
```

Met de uitleg erbij: zet die publieke IP-variabelen op loopback, want dat
schakelt de connectietest-DNS-server uit, en die gebruikt een
batch-instance niet. Dat is waar. Ik heb het gedaan.

Alles kwam gezond op. Elke container `healthy`, geen enkele klacht in de
logs. En elke test die ik indiende faalde. De resolver kon niets opzoeken,
routinator kon zijn RPKI-data niet ophalen, en niets op het
`public-internet`-netwerk kon ook maar iets bereiken.

De oorzaak staat in `docker/compose.yaml`, in het netwerkblok:

```yaml
      # set NAT source IPs to the configured public IPs
      com.docker.network.host_ipv4: $IPV4_IP_PUBLIC
      com.docker.network.host_ipv6: $IPV6_IP_PUBLIC
```

Dezelfde twee variabelen. Eén variabele draagt twee volstrekt losse
betekenissen: het adres waarop de connectietest luistert, én het bronadres
waarnaar Docker élk uitgaand pakket herschrijft. De waarde die het eerste
uitzet, vertelt het tweede om al je verkeer naar `127.0.0.1` te NAT'en.

Als je het eenmaal weet, zie je het meteen in `iptables -t nat -L
POSTROUTING`. Als je het niet weet, zoek je in de verkeerde hoek, want alle
symptomen wijzen naar DNS.

De fix: zet de échte publieke adressen in `docker/host.env`, precies zoals
de niet-batch-handleiding zegt, en zet de connectietest-DNS-server apart uit
door de `UNBOUND_PORT_*`-variabelen aan loopback te binden. Dan heb je
werkend uitgaand verkeer én geen publiek bereikbare DNS-listener, wat de
handleiding ook bedoelde.

## 2. Certbot start niet op, dus je certificaat verloopt gewoon

Deze is stiller en daarmee gemener. Je certificaat wordt niet vernieuwd, en
je merkt het pas als het verlopen is. De cron in de container draait wel,
maar levert een Python-traceback in plaats van een verlenging:

```
+ /opt/certbot/bin/certbot renew --post-hook 'nginx -s reload'
Traceback (most recent call last):
  File "/opt/certbot/bin/certbot", line 5, in <module>
    from certbot.main import main
  File "/opt/certbot/lib/python3.12/site-packages/certbot/_internal/main.py", line 20, in <module>
    import josepy as jose
  File "/opt/certbot/lib/python3.12/site-packages/josepy/__init__.py", line 41, in <module>
    from josepy.json_util import (
```

Het is een incompatibiliteit tussen de vastgezette `josepy` en de
`pyOpenSSL` in het image, rond het verdwijnen van `X509Req`. In de
container is het te repareren:

```sh
docker exec internetnl-prod-webserver-1 /opt/certbot/bin/pip install -U certbot josepy
```

Maar let op: die fix leeft in de schrijfbare laag van de container en is
weg zodra het image wordt bijgewerkt. Zet een herinnering op de
vervaldatum van je certificaat tot upstream een gerepareerd image
uitbrengt. Het staat daar
[als issue](https://github.com/internetstandards/Internet.nl/issues/2142).

Dit is precies het soort ding waarom ik "een instance draaien" een dienst
noem en geen script. Je bent niet klaar als het werkt.

## 3. De compose-wrapper wil een terminal

Alles wat je over SSH vanuit een script of CI-job doet faalt, terwijl
hetzelfde commando prima werkt als je zelf ingelogd bent. De wrapper start
de compose-container met een hard ingebakken `-ti`:

```sh
exec docker run -ti --rm --pull=never \
```

Die `-t` wil een terminal, en een `ssh host 'commando'` geeft er geen.
Forceer er dan een met `ssh -tt`. Twee t's, niet één: met één `-t` weigert
ssh juist als stdin geen terminal is, wat precies de situatie is die je
probeert op te lossen.

## 4. Een nieuw netwerk laat oude containers achter

Na een compose-run die het netwerk opnieuw aanmaakt, kunnen sommige
containers elkaar niet meer bereiken. Ze zien er gezond uit. Ze hangen
alleen nog aan een netwerk-ID dat niet meer bestaat. Herstarten helpt niet,
want dan koppelen ze aan diezelfde dode ID. Weggooien en opnieuw laten
maken wel:

```sh
docker ps -a --filter status=exited -q | xargs -r docker rm
docker/compose.sh ... up -d
```

## Wat dit zegt over documentatie

Ik schreef eerder dat [verouderde documentatie erger is dan geen
documentatie](/posts/2026-07-14-levende-documentatie-met-gates-en-agents/).
Deze vier gevallen zijn een variant daarop die me nog meer bezighoudt: de
documentatie is niet verouderd. Elke zin klopt. Valkuil één is gewoon een
waar statement over wat die variabele doet — het is alleen niet het
volledige verhaal, en het ontbrekende deel staat in een ander bestand.

Dat is geen documentatieprobleem dat je met beter schrijven oplost. Het is
een ontwerpprobleem dat in de documentatie zichtbaar wordt: een variabele
die twee dingen betekent, kún je niet in één zin eerlijk uitleggen. De
handleiding lijdt aan de code.

De les die ik eruit haal, en die ik in mijn eigen projecten probeer vast te
houden: als je een instructie schrijft waarbij je "en dit heeft verder geen
gevolgen" niet met droge ogen kunt opschrijven, dan is dat een signaal over
je code, niet over je tekst.

## Wat ik ermee gebouwd heb

Er draait nu een keten die dit alles verbergt voor wie er geen zin in
heeft. Een eigen batch-instance op een VPS, bereikbaar over een tailnet,
met daarvoor een facade die tenants, limieten en een auditspoor regelt. Een
CLI en een GitHub Action die je build laten falen als je score zakt. En een
demo waar je zonder account een domein kunt intypen.

Elke ochtend meet het zichzelf, en de uitkomst staat onverkort op de
[demopagina](https://mwest2020.github.io/internetnl-cli-demo/) — inclusief
het domein dat er duidelijk slechter af komt dan de rest. Dat laat ik er met
opzet staan: dat domein is publiek dicht, en een scorebord dat alleen groene
vinkjes toont meet niets.

- **Code en de vier valkuilen uitgeschreven:**
  [github.com/MWest2020/internetnl-cli](https://github.com/MWest2020/internetnl-cli)
- **Zelf proberen, zonder account:**
  [mwest2020.github.io/internetnl-cli-demo](https://mwest2020.github.io/internetnl-cli-demo/)

Eén huisregel, en die geldt ook voor jou: meet alleen hosts die je zelf
beheert of waarvoor je expliciet toestemming hebt.
