---
title: "Claude Code via mobiel — hoe ik 't bouwde"
date: 2026-05-17
draft: false
tags: ["devops", "tooling", "homelab"]
summary: "Een LXC, Tailscale, tmux, en een SSH-key per apparaat. Persistent, multi-device, niets in een blackbox."
---

SSH naar je workstation vanaf je telefoon is het naïeve antwoord op
"Claude Code mobiel". Werkt, maar valt om op het moment dat 4G even
flikkert, of als je laptop uit gaat. Wat ik wilde was: typen op de
telefoon in de trein, thuis voor de desktop gaan zitten en exact zien
waar de cursor stond. Eén sessie, vier apparaten, geen vendor in het
pad.

Dit is hoe die setup eruit ziet. Niets futuristisch — vier
componenten, allemaal saai.

### De architectuur

1. **Een [LXC](https://linuxcontainers.org/)-container op een
   [Proxmox](https://www.proxmox.com/)-host.** Geen Claude Code op mijn
   werkstation; een eigen container die altijd aan staat, geïsoleerd
   van de rest. Eén machine die voor "Claude Code" verantwoordelijk
   is, en niks anders.
2. **[Tailscale](https://tailscale.com/) op elk apparaat.** Geen
   poorten doorzetten, geen publiek IP, geen
   [DDNS](https://en.wikipedia.org/wiki/Dynamic_DNS). Mijn laptop,
   telefoon, en de container zitten in een private tailnet en zien
   elkaar via stabiele namen — ook door carrier-grade NAT heen.
3. **[tmux](https://github.com/tmux/tmux) in de container.** Sessies
   overleven SSH-disconnects, dus m'n telefoon-naar-de-zak laten gaan
   kost geen werk. En — dit is de echte feature — meerdere clients
   kunnen tegelijk aan dezelfde sessie hangen.
4. **Per-device SSH-keys.** Iedere apparaat heeft z'n eigen sleutel,
   gelabeld in `authorized_keys`. Verlies van telefoon = één regel
   eruit, geen rotatie van álle keys.

### De killer feature: shared tmux

Eén sessie, meerdere clients tegelijk. Typen op de telefoon zie ik
realtime op het desktop-scherm verschijnen. Detachen op één client
laat de andere clients gewoon zitten.

```bash
# Eerste keer, vanaf de desktop
ssh user@container
tmux new -A -s main

# Later, vanaf de telefoon (SSH-app naar keuze, over de tailnet)
ssh user@container
tmux a -t main
```

`Ctrl-b d` detacht alleen die ene client. Voor losse parallelle
sessies (bv. coderen apart van logs volgen): een ander `-s`-label en
je hebt twee onafhankelijke sessies in dezelfde container.

Mobiel-tip die het bruikbaar maakt: `set -g mouse on` in
`~/.tmux.conf`. Tikken om tussen panes te schakelen werkt dan zoals
je hoopt dat het werkt.

### Provisioning: IaC, niet handwerk

De container zelf is [Terraform](https://www.terraform.io/): één
resource, Proxmox-provider, klaar. De binnenkant is
[Ansible](https://www.ansible.com/): een handjevol rollen voor
SSH-hardening, Tailscale-installatie, Node.js, Claude Code zelf, en
een GitHub-identiteit. Idempotent: opnieuw draaien is "0 changes" als
de container al kloppend is.

Concreet gevolg: "verloren container herbouwen" is een commando-paar
in plaats van een uurtje klikken. Tweede gevolg: elke wijziging aan de
binnenkant is een commit, niet een aantekening op een post-it.

### Mobiele kant

Op Android gebruik ik [Termius](https://termius.com/). Het keypair laat
ik in de app zelf genereren — de private key blijft op de telefoon en
verlaat 'm nooit. Public key toevoegen aan de Ansible-vars, de
base-rol opnieuw draaien, en de telefoon zit in de container.

Tailscale-app op de telefoon installeren, inloggen, klaar — het
apparaat krijgt een tailnet-adres en kan de container via z'n
stabiele naam bereiken in plaats van een wisselend mobiel IP.

### Wat kost het

- **Een Proxmox-host.** Een mini-pc of een stevige Pi is genoeg — een
  huis-LXC-host hoeft niet groot.
- **Setup-tijd: niet weken, wel uren.** Hoeveel hangt af van hoe
  comfortabel je bent met Terraform en Ansible.
- **Een Tailscale-account.** Gratis voor persoonlijk gebruik. Als je
  echt geen Tailscale wil is [WireGuard](https://www.wireguard.com/) +
  DDNS een optie — minder leuk om in de lucht te houden, maar het kan.

### Wat het niet is

Geen cloud-magie, geen autonome agent die op een server door blijft
draaien zonder dat ik 't merk. Het is een terminal-sessie op mijn
eigen ijzer, met goede netwerk-bedrading en wat luxe voor multi-device
gebruik. Maar als je je code en je AI-tooling niet aan een derde
partij wil overdragen, en je wil tegelijk vanaf elk scherm kunnen
werken — dit is wat dat in 2026 betekent.
