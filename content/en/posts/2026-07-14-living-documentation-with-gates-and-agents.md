---
title: "Documentation that lies is worse than no documentation"
date: 2026-07-14
draft: false
tags: ["ai", "agents", "documentation", "devops", "compliance"]
translationKey: "living-docs-gates"
summary: "Stale documentation has always been a slow-burning problem, but now that AI agents read that documentation as ground truth, it has become an acute one. How we made documentation 'living' with an enforceable contract, gates that block unverified changes, and an MCP server that gives agents context with provenance — so they cite instead of guess. From 63 findings to zero. And why this pattern doubles as the foundation for a chatbot on your cluster: talking to the devops colleague who is on holiday, with sources attached."
---

*How to build documentation that cannot go stale without someone
noticing — and why that suddenly matters now that agents are reading
along.*

Everyone knows the page. The wiki says the deploy runs through script
A, but script A was replaced by pipeline B three months ago. The README
describes a configuration option that no longer exists. Nobody
remembers who owns the document, so nobody feels responsible for
fixing it.

Stale documentation is worse than no documentation. No documentation
forces you to go and look at how things actually are. Stale
documentation gives you **false confidence** — you act on information
that was correct, once.

For years this was a slow-burning problem that teams accepted as a fact
of nature. But something has changed: **AI agents now read that
documentation too.** And that turns slow-burning into acute.

### Why agents sharpen the problem

An experienced human can smell that a page is old. The screenshots
don't match anymore, the tone is from two reorganisations ago, the team
member mentioned has long left. People have a built-in scepticism
reflex.

An agent has no such reflex. It reads the page and takes it as truth.
Or worse: if there is no page, it falls back on model knowledge — an
assumption about how systems *like* yours usually work. In an
environment with dozens of repositories and infrastructure that changes
weekly, "usually" is precisely not good enough.

We work on a platform that spans many repositories, with agents working
in them daily. We kept seeing three problems come back:

1. **Documentation drift.** Docs going stale relative to the code,
   duplicated content diverging across repos, and no periodic control
   on accuracy whatsoever.
2. **Unverified changes.** Changes being pushed without the tests,
   checks or accompanying documentation coming along. "Done" meant: the
   code compiles.
3. **Agents without ground truth.** Agents having to scrape context
   together from scratch every session, and falling back on assumptions
   in the absence of a reliable source.

Three problems, one underlying cause: nothing bolted reality and the
description of reality together. So that is what we built. Three
mechanisms.

### Mechanism 1: a docs contract instead of good intentions

The first step is boring and underrated: agree on what documentation
*is* and where it *lives* — and make that agreement checkable.

For us, documentation lives in `/docs` inside the repository of the
component itself. Never centralised, never copied. The central portal
*aggregates* those folders on every build and is itself a disposable
artifact — the source repo remains the single source of truth. That
structurally removes duplication, the root of divergence.

None of that principle is new: this is docs-as-code, as the
[Write the Docs](https://www.writethedocs.org/guide/docs-as-code/)
community and Anne Gentle's
[*Docs Like Code*](https://www.docslikecode.com/) have prescribed for
years — documentation in version control, next to the code, through the
same review as the code. What we mainly added is enforcement. Every
page is also exactly one kind — tutorial, how-to, reference or
explanation — following Daniele Procida's
[Diátaxis](https://diataxis.fr/) framework.

Every page carries two mandatory fields in its front matter:

```yaml
last_reviewed: 2026-07-14
owner: platform-team
```

It looks like nothing, but it changes everything. `owner` means someone
is always accountable. `last_reviewed` means freshness is measurable —
and a review without changes counts: updating the date *is* the act
that extends the shelf life.

And the most important rule: **documentation changes in the same PR as
the code it describes.** "Done" means: code, tests and docs updated.
Not as a guideline on a poster, but as a check that blocks your push.
Which brings us to mechanism two.

### Mechanism 2: gates — enforce instead of hope

Agreements without enforcement are wishes. So a set of gates runs
before every push, shared across all repositories and pinned to a
specific version (so it is reviewable *which* check ran at *which*
push):

- **Contract check**: is the structure right, does every page carry a
  valid owner and review date, is nothing duplicated?
- **Executable doc claims**: marked code blocks in the documentation
  are actually executed as dry-runs. A page claiming "this command
  verifies X" is held to that claim itself.
- **Tests and dry-runs** of the component itself.
- **Secret scanning**, so no credential ever slips into docs or code.

The gates run in gate mode: they fix nothing silently, they block and
report. And they are themselves covered by unit tests — a check you
don't know works is theatre.

On top of that, a pipeline checks the whole thing weekly, even when
nobody pushes: a strict build, a freshness check (every page must have
been reviewed within a year), and a link check. If a scheduled run goes
red, exactly one drift issue opens automatically — and closes itself
once things are green again. Drift stops being a feeling and becomes an
issue with a timestamp.

Does it work? The baseline audit across eight repositories produced 63
findings — not a single page had an owner or review date. After
remediation: zero findings, and the gates keep it that way. Best
detail: during rollout, the executable doc claims immediately caught
two real errors in existing documentation. The check proved itself on
day one.

### Mechanism 3: agents get context with provenance

Once the foundation is sound, you can let agents stand on it. We serve
the aggregated documentation to agents through an
[MCP server](https://modelcontextprotocol.io/) with three read-only
tools: list components, search, and read a page.

The crux is what comes with every answer: **provenance**. Component,
page, owner, review date and a direct link to the source. The working
instruction for the agent is explicit: handbook content beats model
knowledge, and if the model contradicts the page, the page wins — and
the agent flags the discrepancy instead of reasoning it away.

That flips the dynamic. Instead of an agent scraping context together
every session and filling gaps with assumptions, you get an agent that
cites. Every statement traces back to a page, an owner and a date. And
because the MCP server reads exactly the same source list as the
portal, there is no second truth that can quietly diverge.

The final layer is an operations catalogue per repository: which
actions may an agent perform autonomously, which only as a proposal,
which require a human, and which are forbidden. With one closing rule:
**if it is not in the catalogue, a human is required.** Pushing and
production mutations are always done by a human.

### From documentation to conversation: talk to your cluster

Once this was in place, the pattern turned out to open one more door —
perhaps the most important one. Documentation that is current,
traceable and machine-readable is exactly the foundation a chatbot
needs to be useful instead of dangerous.

Anyone who has ever asked a language model about their own
infrastructure knows the two flavours:

**You:** "What's the current image tag for the Nextcloud deployment on
production?"

**Bot without ground truth:** "Probably `latest`, or maybe 28.0.0 —
that came out recently…"

**Bot with ground truth:** queries the MCP server, reads the deployment
configuration and the matching handbook page, and answers: "28.0.2,
rolled out on July 11; the chart values live in this repo — source:
page *deployments*, owner platform-team, last reviewed this month."

The first answer is a guess delivered with confidence — the most
dangerous combination there is. The second is a quote with a footnote.
Same model, same question; the only difference is the layer
underneath.

That makes this pattern the natural foundation for an assistant on
your platform: talking to your cluster infrastructure the way you talk
to that one devops colleague who knows everything — even when that
colleague is on holiday. With two differences in the bot's favour: it
cites its sources with every answer, and it is not *allowed* to do
anything. Read, search, cite — mutation is not in its catalogue, and
what is not in the catalogue requires a human.

### What it buys you

- **Documentation that cannot silently go stale.** Every page has an
  owner and an expiry date, and a weekly check that raises the alarm.
- **Changes that cannot land unverified.** The push is physically
  blocked until code, tests and docs are right.
- **Agents that cite instead of guess.** Ground truth with provenance,
  and clear limits on what they may do on their own.

And there is a by-product that is no side note in regulated
environments: every run log of these checks is directly usable as
evidence that documented information is kept up to date — an obligation
you would otherwise have to demonstrate in an ISO 27001 audit with
manual effort and good intentions. Here, the evidence is a by-product
of simply working.

### The sober conclusion

Nothing above is spectacular. Front matter, pre-push hooks, a cron job,
a search function. That is exactly the point. The temptation with
"AI-ready documentation" is to build something impressive — vector
databases, automatic summaries, generated docs. We went the other way:
make the documentation itself reliable, checkable and fresh, and give
agents a boring, predictable read interface with source attribution.

Living documentation is not documentation that writes itself. It is
documentation that cannot lie without a light going on somewhere.

---

*A piece about provenance should cite its own sources. The term
"living documentation" originates in Gojko Adzic's
[*Specification by Example*](https://gojko.net/books/specification-by-example/)
and was developed further by Cyrille Martraire in his book
[*Living Documentation*](https://leanpub.com/livingdocumentation). The
docs-as-code school of thought comes from the Write the Docs community,
the page taxonomy from Daniele Procida's Diátaxis. What we added is
mainly the combination: gates that enforce the contract, and a read
interface with provenance for agents.*
