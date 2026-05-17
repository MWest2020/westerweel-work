---
title: "Claude Code via mobiel — drie paden"
date: 2026-05-17
draft: true
tags: ["devops", "tooling"]
summary: "Anthropic's remote control, SSH met tmux, of een third-party wrapper. Welke past wanneer."
---

Soms zit je in de trein. Soms krijg je een ingeving op de bank. Claude
Code is een CLI-tool, maar dat hoeft niet te betekenen dat je vastzit
aan je workstation. Er zijn op het moment van schrijven drie manieren
om vanaf je telefoon iets met Claude Code te doen — elk met andere
trade-offs.

### 1. Anthropic's remote control — eenvoudigst

Anthropic levert ingebouwde remote control: vanaf je telefoon koppel je
aan je actieve desktop-sessie, zonder VPN of poort-doorzetters.

1. Start Claude Code in je terminal.
2. Typ `/remote-control` in die sessie.
3. Open de Claude-app op je telefoon en kies daar de sessie.

Je telefoon toont wat je desktop doet. Vragen stellen, wijzigingen
bekijken, taken sturen — allemaal vanaf je broekzak.

**Voordeel:** nul setup. Geen sleutels, geen netwerk-kennis.
**Nadeel:** je computer moet aan staan. Het is een live-koppeling met
een actieve sessie, geen autonome cloud-agent.

### 2. SSH + tmux — meeste controle

Voor wie geen tussenpersoon wil tussen z'n telefoon en z'n eigen
machine: SSH naar een server (thuis, VPS, private cloud) waar Claude
Code draait, en tmux houdt de sessie persistent zodat een telefoon-in-
de-zak je niet kost wat je aan het doen was.

Op je telefoon een fatsoenlijke SSH-client (Termius en Blink op iOS,
Termius en Termux op Android). Op de server draait `claude` binnen een
tmux-sessie. De korte versie:

```bash
tmux new -s work       # nieuwe sessie met naam
Ctrl-b d               # detach — sessie blijft draaien
tmux ls                # alle sessies tonen
tmux attach -t work    # weer erin
```

Meerdere sessies parallel werkt vanzelf — een sessie per project, of
één voor coderen en één voor logs. Voor mobiel-comfort helpt
`set -g mouse on` in `~/.tmux.conf`: tikken om tussen panes te
schakelen.

**Voordeel:** alles blijft op eigen ijzer. Geen vendor in het pad.
Bestanden op de server zijn direct toegankelijk; ook handig voor langer
draaiende taken die je gewoon laat lopen.
**Nadeel:** setup-kost. Een server (of LXC, of Pi), SSH-keys op orde,
en het accepteren dat een telefoon-toetsenbord nooit een laptop wordt.

### 3. Third-party wrappers — Happy CLI en vrienden

In de community zijn er apps die een CLI-coding-agent in een
mobiel-vriendelijk jasje wikkelen. Happy CLI is de bekendste — mirrort
je terminal-sessie naar een Android- of iOS-app, met betere UI dan een
platte SSH-client.

**Voordeel:** mobiele UX zonder zelf een SSH-stack overeind te houden.
**Nadeel:** je zet een derde partij in het pad tussen jou en je code.
Voor wat je doet en deelt is dat een bewuste afweging waard.

### Welke past wanneer

- **Snel iets bekijken, geen tijd voor setup:** optie 1.
- **Je hebt al een homelab of VPS en geeft om soevereiniteit:** optie 2.
- **Mobiel-eerst, wil meteen beginnen:** optie 3 — lees wel even de
  privacy-policy.

Zelf landde ik op optie 2. Past bij hoe ik verder ook werk: eigen
ijzer, alles auditeerbaar, niets in een blackbox dat ik niet zelf kan
uitzetten. Maar als optie 1 een gesprek-aanknopen dertig seconden
makkelijker maakt, is dat ook gewoon waarde. Kies wat past bij je
threat model en je geduld voor setup, niet bij wat het hipste klinkt.
