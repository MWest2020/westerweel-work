---
title: "Bazibo: four megabytes, no trackers"
date: 2026-11-09
draft: false
tags: ["bazibo", "sovereignty", "privacy", "open source", "children", "apps"]
translationKey: "bazibo-vier-megabyte"
summary: "A children's games app of four megabytes, with no account, cookies or trackers. What I learned from building small, why everything stays on the device, and why the full version costs one euro."
---

*About Bazibo, an app with games for children, and what I learned by
keeping it as small and as boring as possible.*

It started with a bubble shooter on my phone, played with my kid.
The game itself was fun, but it was full of ads. So I thought: this
can be done differently.

That became [Bazibo](https://bazibo.nl). Six games for children aged 3
to 10: Bubble Shooter, Dogudoku, Picturedoku, Four in a Row, Snake and
Colouring. Telling the time is on its way. Everything in Dutch and
English. The name comes from *bāzi*, the Persian word for play.

## Four megabytes

The Android app is about 4 megabytes. The web version is under one.
Many game apps in the store run to tens or hundreds of megabytes. The
difference isn't cleverness. It's what you leave out.

Bazibo is plain HTML, CSS and JavaScript, on a canvas and in SVG.
There's no game engine. The bubbles, the dogs, the mandalas and the
clock are drawn in code. The sounds are made on the spot with the Web
Audio API; there isn't a single sound file in it. The only images are
the app icons. And there's no ad SDK and no analytics. Those are what
make apps big.

## Everything stays on the device

Bazibo has no account, no server and no cookies. We measure nothing
and we follow no one. The games make no internet connection at all.

What the app remembers, like stars, progress, colouring pages and
whether the full version was bought, lives on the device itself. At
most it goes along in your phone's normal backup, under your own
Google or Apple account. We can't reach it.

That's the sovereignty I often write about, but small: your child's
data stays yours because it goes nowhere else.

## Honestly: it works per device

There's a downside, and I don't want to hide it. Because there's no
account, everything works per device. If your child plays on a phone
and on a tablet, those are two separate sets of progress. They don't
sync. Get a new phone without a backup, and your child starts over.

You don't lose the purchase. That lives with Google Play, and with the
same account you get it back with "Restore purchase", on every device.

Want to keep the progress? Turn on your phone's normal backup (Android:
Settings › Google › Backup). It includes Bazibo, and a new phone gets
it back. Coming soon is "Move progress": a QR code on one device,
scanned by the other. No server, no internet.

And the website? It runs at an ordinary hosting company. Like any web
server, it keeps log files with IP addresses, for security and
troubleshooting. That's in the
[privacy policy](https://bazibo.nl/en/privacy/) too. The app itself
doesn't use the website.

## Open source, and one euro

All the code is open on
[GitHub](https://github.com/MWest2020/bazibo), under the MIT licence.
Anyone can check what the app does, and what it doesn't.

Every game has a free part. The full version costs one euro, once, for
everything. No subscription, no coins, no ads to buy your way out of.
The purchase sits behind a sum for parents, so a child can't buy
anything by accident.

That euro is for further development: more games, more levels. And we
give part of it back to the open-source projects Bazibo is built on,
such as Capacitor, cordova-plugin-purchase, Playwright and fastlane.
Without them this would have been a lot more work.

## What I learned

- **Leaving things out is easier than adding them.** No account means
  no passwords, no database and no data breach. No server means
  nothing to patch.
- **Collecting nothing makes the store easy.** Google's forms for
  children's apps and data safety were quick to fill in. Almost every
  answer was "no".
- **Drawing in code scales.** A mandala generator makes endless new
  colouring pages without the app growing by a byte.
- **The edges are the real test.** A parental gate, a back button that
  does what you expect, progress that survives a failed start. That's
  where most of the work was.

I built it with AI agents, with an independent review per game before
anything went live. Those reviews kept finding things I hadn't seen
myself.

Bazibo is at [bazibo.nl](https://bazibo.nl) and is coming soon to the
Google Play Store. The code is at
[github.com/MWest2020/bazibo](https://github.com/MWest2020/bazibo).
