---
title: "Bazibo: games without ads, and without us"
date: 2026-11-09
draft: false
tags: ["bazibo", "sovereignty", "privacy", "open source", "children", "apps"]
translationKey: "bazibo-vier-megabyte"
summary: "A games app for kids of just over four megabytes. No account, no cookies, nothing that comes back to us. And one euro for everything."
---

A while ago I was playing a bubble shooter on my phone with my kid.
Nice game, except it was full of ads. And bubble shooter code isn't
exactly rare, so I figured: we'll make our own. Without the ads.

That turned into [Bazibo](https://bazibo.nl). Six games for kids from
about 3 to 10: a bubble shooter, Dogudoku (a sort of sudoku with
puppies), Picturedoku (sudoku with pictures), four in a row, a snake
that learns to count and spell, and colouring pages with mandalas for
the older ones. Telling time is next. Everything in Dutch and English.

The name comes from *bāzi*, Persian for game. It also sounds a bit like
gazebo, hence the little gazebo in the logo.

## Small

The Android app is just over 4 MB. On the website it's under one
megabyte. Have a look sometime at how big the average game in the store
is. Tens or hundreds of megabytes isn't unusual.

That's not because I'm clever. There's just not much in it. No game
engine, no ad SDK, no analytics. It's HTML, CSS and JavaScript. The
bubbles, the puppies and the mandalas are drawn in code, and the sounds
are made on the spot. There isn't a single sound file in it. The only
images are the app icons.

## Collecting nothing

No account, no server, no cookies. We don't measure anything and we
don't follow anyone. The games don't even open an internet connection.

Progress, stars, colouring pages and whether you paid: it all lives on
the phone itself. At most it goes along in the backup your phone already
makes, under your own Google or Apple account. We can't get to it.

There is a catch. Because there's no account, everything works per
device. If your kid plays on the phone and on the tablet, that's two
separate sets of progress. New phone without a backup? Back to level 1.

You don't lose the purchase, that sits with Google Play. With the same
account you tap "Restore purchase" and everything's unlocked again, on
the tablet too.

You keep progress with your phone's normal backup (Android: Settings ›
Google › Backup). I'm also building "Move progress": you show a QR code
on one device and scan it with the other. No server in between.

Oh, and the website. It runs at an ordinary hosting company, which,
like any web server, keeps log files with IP addresses. That's in the
[privacy statement](https://bazibo.nl/en/privacy/) too. The app itself
doesn't talk to the website.

## Open source, and one euro

The code is on [GitHub](https://github.com/MWest2020/bazibo), under
MIT. Anyone who wants to can see exactly what the app does. And what it
doesn't.

Every game has a free part. For one euro, once, you get everything: all
the levels and after that endless new puzzles. No subscription, no
coins, no ads to buy your way out of. Buying goes through a little sum
for parents, so your kid can't just tap "buy".

That euro pays for building more. And part of it goes back to the open
source projects this runs on, like Capacitor and the plugin that does
the purchases. Without those people I wouldn't have put this together
so quickly.

## What I learned

Leaving things out is easier than building them. No account means no
passwords, no database and no data breach. No server means nothing to
patch.

That also made Google's forms for kids' apps quick. Does the app collect
data? No. Ads? No. Done.

Most of the work was in the edges. A back button that does what you
expect. A lock on the purchase that a toddler can't get around. Progress
that doesn't vanish when the app starts up weird once. I built it with
AI agents, and every game went past a separate agent for review before
it went live. It found something every time.

You can play at [bazibo.nl](https://bazibo.nl). It'll be in the Play
Store soon.
