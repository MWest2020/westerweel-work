---
title: "Your sovereignty assessment is a snapshot. Your footprint isn't."
date: 2026-09-21
draft: true
tags: ["sovereignty", "open source", "dns", "measurement", "government"]
translationKey: "wanderer-meten"
summary: "The Dutch DICTU sovereignty assessment works on what you declare: you pick a supplier, walk five dimensions, get a score. Useful — but it measures what you think you have. Wanderer measures what is actually there: DNS, mail, certificates, the path your traffic takes, and who is actually reachable when something goes wrong. Passive, open source, and honest about what it does not know. With a public demo and the verdict on my own domain, which was not flattering."
---

*A scanner that measures an organisation's externally visible footprint —
and why "unknown" must never quietly become "fine".*

The DICTU sovereignty assessment, and derivatives such as
[soevereiniteitstoets.nl](https://soevereiniteitstoets.nl), work on
**declared** services. You pick a supplier, walk five dimensions and fifteen
criteria, and out comes a score. That is useful work, and it has two limits.

The first: it is a snapshot. The second, and this one is harder: it assumes
you *know* which services are in scope. In practice nobody knows that
precisely. Every municipality has SaaS that came in as a pilot years ago, an
MX record pointing somewhere nobody can still explain, a CDN the supplier
chose, and a login screen that quietly federates to an American identity
provider.

No questionnaire survives that. For that you have to look.

## What it measures

[Wanderer](https://github.com/MWest2020/wanderer) looks at one domain from the
outside and answers seven questions, each about one link in the chain:

- **Where is it hosted?** The apex addresses, their AS number and the country
  of registration.
- **Where does the mail go?** The MX hosts, and where *those* live.
- **Who runs the DNS?** The nameservers, and their jurisdiction.
- **Which route does the traffic take?** A traceroute per hop, with AS and
  country — because traffic between two Dutch endpoints can happily travel via
  Frankfurt or Ashburn.
- **Who sits in front?** CDNs and hyperscalers in the path.
- **What does the page pull in?** Third-party resources loaded by the site.
- **Who issued the certificate?** The CA that holds your cryptographic
  identity.

This month an eighth was added, and it is the question that completes the
others: **who is accountable, and can you reach them?** A domain whose
registrant sits behind a privacy proxy, whose contact address in the DNS zone
bounces, that runs through an anonymous reseller and publishes no
`security.txt`, is unaccountable infrastructure. For a public organisation
that is as much a sovereignty gap as an American nameserver: incident
response, handover and legal recourse all hang on an identifiable
counterparty.

## Passive, and that is a design choice

Everything Wanderer does is what an ordinary visitor does: DNS queries, RDAP
lookups, a TLS handshake, an HTTPS request, a traceroute. No port scans, no
brute force, no SMTP connections to see whether a mailbox exists.

That last one is a deliberate boundary. You *could* verify the contact address
from the DNS zone by opening an SMTP conversation without sending mail.
Technically it works. But it shows up in abuse logs, and at that point your
sovereignty scanner has become something that looks like reconnaissance for an
attack. So Wanderer checks that the mail domain exists and accepts mail, and
**says outright that delivery was not verified**.

## Being honest about what you don't know

This is the part I thought about most.

A scanner that says "no" where it means "I don't know" is worse than no
scanner. People start fixing things that aren't broken, and what *is* broken
disappears into the noise. So Wanderer has four answers — yes, no, unknown,
and not applicable — and an unknown never silently turns into a yes.

The sharpest example is `.nl`. SIDN publishes no registrant data in RDAP, for
anyone. The question "is the registrant recognisable as your organisation?"
is therefore, for *every* Dutch domain, unanswerable through the official
route. A scanner that turns that into a "no" is blaming the Dutch government
for the registry's policy. Wanderer says: **n/a — the registry does not
publish registrant data for .nl**, and lets the other questions carry the
story. There are workarounds — registrar APIs, scraping — but they don't fit
an instrument that takes its own limits seriously.

The same goes for a domain's expiry date: SIDN doesn't publish that either.
That is not a hole in the measurement, it is the passive ceiling. And a
ceiling should be visible, not explained away.

## From one answer to a fleet

For a single domain you want a sentence, not a table: *"No — the mail runs
through an American provider"*. That sentence sits at the top, and the
evidence unfolds beneath it: which observation, which rule, which threshold.

The moment you put forty domains side by side, yes/no stops working —
everything reads "no" as soon as one thing is off, and you can't see who is
in better shape. So there it is **x out of n**: how many questions were
answered sovereign out of the number that *could* be answered, with the
unanswered ones counted separately alongside. And always with the heaviest
open finding attached, because a score that weighs everything equally invites
you to close the easiest gap.

Click through to a rule and it explains itself: what it checks, why it
matters, which observation it uses, and **which threshold decides the
verdict**. That last part is not a detail. "Expires within 30 days" or "above
90 days" are assumptions, and an assumption you cannot see is one you cannot
refute. And next to every negative verdict stands one concrete action — not
"ensure a recognisable registrant", but "ask your registrar to remove the
privacy proxy on this domain".

## My own domain doesn't score well

There is a public demo at
[wanderer.westerweel.work/demo](https://wanderer.westerweel.work/demo). One
preset domain, no login, no scan button — an open scan button would turn such
an instance into a scanner-for-third-parties, which is precisely what you
don't want to build.

That domain is mine. And the verdict is:

> **No — Hosting: hosted at Cloudflare — apex IPs in CA, CA, CA, CA (outside
> EEA)**

That is uncomfortable, and that is the point. I am building an instrument that
points at dependency on American providers, and my own infrastructure hangs
behind a single American edge: the DNS zone, the apex addresses, and every
public entrance to my cluster. This week I wrote that down as a decision
rather than a habit: for now it stays — there are no users carrying the risk —
with three moments at which it comes back up. As soon as someone other than me
logs in. As soon as personal data flows over it. As soon as I offer this to
third parties.

What I do in the meantime: my own names sit on the same weekly scan schedule
as the domains I check for other people. A dependency you know about is the
one that most easily drops out of sight.

## Where this is going

Wanderer is open source under the EUPL-1.2. There is a CLI, and this week
binaries and a GitHub Action are landing so you can run it in your own
pipeline — on your side, on your domains, with nothing coming back to me.

For anyone who wants to use it seriously there is also an agent that runs on a
host and reports what is installed and where that machine talks to. Because
half of the dependencies are invisible from the outside.

Interested in taking a look, or in pointing this at your own fleet? Let me
know.
