---
title: "Projecten"
translationKey: "projecten"
summary: "Eigen projecten: soevereine tooling, een agent-ecosysteem op eigen hardware, en meetbaar internet."
---

Eigen werk, naast het consultancy-werk. Gemene deler: open source waar het
kan, eigen hardware waar het moet, en saai-maar-auditeerbaar boven slim.

## Wordsworth — soevereine PII-straat

Een documentstraat die overheidsdocumenten omzet in een doorzoekbaar,
privacy-veilig corpus: ingest → pseudonimisering → indexering → hybride
zoeken en vraag-antwoord, alles self-hosted (PostgreSQL, OpenSearch, lokale
LLM via Ollama, S3-compatibele object-store) — er verlaat geen document en
geen modelaanroep het eigen ijzer.

De pseudonimisering is **omkeerbaar met sleutel-gated reveal**: detectie
draait deterministisch (BSN-elfproef, IBAN mod-97) plus ML-entiteiten,
waarden worden vervangen door stabiele tokens, en alleen wie een geldige
grant *én* de cryptografische sleutel heeft, kan per PII-type onthullen.
De index bevat nooit klare persoonsgegevens; de append-only audittabel is
tegelijk de state machine van de pijplijn. Envelope-encryptie via OpenBao
Transit; fail-closed bij elke twijfel.

- **Demo (synthetische data):** [mwest2020.github.io/wordsworth-demo](https://mwest2020.github.io/wordsworth-demo/)
- **Code:** [github.com/MWest2020/wordsworth](https://github.com/MWest2020/wordsworth) (EUPL-1.2)

## Boomhuis — en het patroon erachter

Boomhuis is de communicatielaag van mijn agent-ecosysteem: een zelf-gehoste
[buzz](https://github.com/block/buzz)-relay (Nostr-protocol) met kanalen
waarin ik en een handvol chat-native agents — bouwer, reviewer, architect,
marketing — asynchroon samenwerken. Elke identiteit (mens én agent) heeft een
eigen sleutelpaar; alles is doorzoekbaar en auditeerbaar; bereikbaar alleen
via het eigen tailnet. De repo is privé (er leven identiteiten in), maar het
patroon is het delen waard.

Het patroon: **scheid de lagen, en geef elke laag één taak.**

1. **Git is de waarheid.** Code, verdicts en audit-sporen leven in git.
   Chatberichten zijn coördinatie en spiegel — nooit gezaghebbende state.
2. **Executie zit in een kooi.** Agents die code bouwen draaien als
   Kubernetes-Jobs met deny-by-default allowlists per rol
   ([habitat](https://github.com/MWest2020/habitat), EUPL-1.2), zonder
   toegang tot de relay of tot secrets. Communicatie en uitvoering raken
   elkaar alleen via git.
3. **Kennis heeft één vaste plek.** Eén repo
   ([handbook](https://github.com/MWest2020/handbook)) is de inventaris en
   het startpunt; documentatie aggregeert dáár, niet in elke chat opnieuw.
4. **Identiteit is een sleutelpaar, geen accountnaam.** Agents zijn
   relay-leden met eigen keys, rollen en kanaal-rechten — toevoegen,
   roteren en intrekken zijn gewone, auditeerbare operaties.
5. **Zacht advies, harde grenzen.** Wat een agent *hoort* te doen staat in
   conventies; wat een agent *niet mag* wordt afgedwongen op de
   runtime-grens. (Waarom dat onderscheid ertoe doet:
   [de shift-left-sessie](/slides/claude-shift-left/).)

Geen platform gekocht, geen SaaS: een relay, een cluster, een paar repo's en
strakke afspraken. Het schaalt niet naar duizend man — het hoeft maar naar
één mens en een handvol agents.

## internetnl-cli — meetbaar internet, in bulk

Een command-line client voor de **batch-API van
[Internet.nl](https://internet.nl)**: test een hele vloot domeinen op IPv6,
DNSSEC, RPKI en TLS in plaats van één domein per browser-tab. Submit een
hostlijst, poll tot de run klaar is (hervatbaar na een dichtgeklapte laptop),
en krijg het resultaat als diffbare tabel of JSON voor pipelines — bruikbaar
als CI-gate op je eigen standaarden-compliance. Inclusief een gedocumenteerd
recept om een eigen batch-instance te draaien.

Huisregel: **meet alleen hosts die je zelf beheert** of waar je expliciet
toestemming voor hebt.

- **Code:** [github.com/MWest2020/internetnl-cli](https://github.com/MWest2020/internetnl-cli)
- **Demo + CI-voorbeeld:** [github.com/MWest2020/internetnl-cli-demo](https://github.com/MWest2020/internetnl-cli-demo)
