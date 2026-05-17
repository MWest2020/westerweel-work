---
title: "Claude Code from your phone — how I built it"
date: 2026-05-17
draft: false
tags: ["devops", "tooling", "homelab"]
translationKey: "mobile-claude-code"
summary: "An LXC, Tailscale, tmux, and an SSH key per device. Persistent, multi-device, nothing in a black box."
---

SSH from your phone to your workstation is the naive answer to "mobile
Claude Code". Works, but falls over the moment 4G flickers, or when
your laptop goes to sleep. What I wanted was: type on the phone on a
train, sit down at the desk at home, and see the cursor exactly where
I left it. One session, four devices, no vendor in the path.

Here's what that setup looks like. Nothing futuristic — four
components, all boring.

### The architecture

1. **An [LXC](https://linuxcontainers.org/) container on a
   [Proxmox](https://www.proxmox.com/) host.** No Claude Code on my
   workstation; a dedicated container that's always on, isolated from
   everything else. One machine responsible for "Claude Code" and
   nothing else.
2. **[Tailscale](https://tailscale.com/) on every device.** No port
   forwarding, no public IP, no
   [DDNS](https://en.wikipedia.org/wiki/Dynamic_DNS). My laptop, phone,
   and the container live on a private tailnet and reach each other by
   stable names — even through carrier-grade NAT.
3. **[tmux](https://github.com/tmux/tmux) inside the container.**
   Sessions outlive SSH disconnects, so phone-back-in-pocket costs me
   nothing. And — the real feature — multiple clients can attach to
   the same session at the same time.
4. **Per-device SSH keys.** Each device has its own key, labelled in
   `authorized_keys`. Losing a phone = one line removed, no rotation
   of every key.

### The killer feature: shared tmux

One session, multiple clients at once. What I type on the phone shows
up on the desktop screen in real time. Detach on one client and the
others stay put.

```bash
# First time, from the desktop
ssh user@container
tmux new -A -s main

# Later, from the phone (SSH app of choice, over the tailnet)
ssh user@container
tmux a -t main
```

`Ctrl-b d` detaches just that one client. For independent parallel
sessions (e.g. coding separate from log-watching): pick a different
`-s` label and you have two independent sessions in the same
container.

Mobile-comfort tip that makes it bearable: `set -g mouse on` in
`~/.tmux.conf`. Tapping to switch panes then works the way you'd hope
it works.

### Provisioning: IaC, not by hand

The container itself is [Terraform](https://www.terraform.io/): one
resource, Proxmox provider, done. The inside is
[Ansible](https://www.ansible.com/): a handful of roles for SSH
hardening, Tailscale install, Node.js, Claude Code itself, and a
GitHub identity. Idempotent: re-running is "0 changes" when the
container is already in shape.

Concrete consequence: "rebuild a lost container" is a pair of commands
instead of an hour of clicking. Second consequence: every change to
the inside is a commit, not a sticky note.

### The mobile side

On Android I use [Termius](https://termius.com/). I have the keypair
generated inside the app — the private key stays on the phone and
never leaves it. Add the public key to the Ansible vars, re-run the
base role, and the phone is in the container.

Install the Tailscale app on the phone, sign in, done — the device
gets a tailnet address and can reach the container by its stable name
instead of a shifting mobile IP.

### What it costs

- **A Proxmox host.** A mini-PC or a beefy Pi is enough — a home-LXC
  host doesn't need to be big.
- **Setup time: not weeks, but hours.** How many depends on how
  comfortable you are with Terraform and Ansible.
- **A Tailscale account.** Free for personal use. If you really don't
  want Tailscale, [WireGuard](https://www.wireguard.com/) + DDNS is
  an option — less fun to keep healthy, but doable.

### What it isn't

No cloud magic, no autonomous agent that keeps running on a server
without my noticing. It's a terminal session on my own iron, with good
network plumbing and a little luxury for multi-device use. But if you
don't want to hand your code and AI tooling to a third party, and at
the same time want to work from any screen — that's what that means
in 2026.
