---
title: "Speaker"
summary: "Talks and dev sessions on AI agents in operations, context and SRE. For meetups and conferences, in Dutch or English."
translationKey: "speaker"
---

I talk about what happens when you put AI agents into operations: what context
they need, where the boundaries belong, and how you prove it works. I also run
dev sessions on the craft itself, such as containers and where a check
belongs. For meetups and conferences on SRE, DevOps and cloud native, in
English or Dutch.

The decks are on the [workshops](/en/workshops/) page and run in your browser.

## Talks

### Agents, skills & tools

Lessons learned building SREna, a local SRE agent, told in stories. The
toddler and the cookie jar: an agent uses whatever is within reach, so you
decide what is in the kitchen. The golem: how far do you let an agent walk on
its own, from monitoring only to fully self-directed. David against Goliath: a
small local model against a cloud baseline, and where it still loses.

- **Format:** talk
- **Language:** English
- **Deck:** [/slides/agents-skills-tools/](/slides/agents-skills-tools/) (draft)

### Context is everything

An agent that guesses is usually missing context, not intelligence. This talk
goes from an MCP that sends agents to the knowledge base to SREna, an SRE
agent that runs entirely locally. With gold, silver and bronze as hallmarks on
sources, and what a small local model teaches you about your own context. The
biggest lesson: the knowledge base is what prevents hallucination, not the
model.

- **Format:** talk
- **Language:** English or Dutch
- **Deck:** [/slides/context-is-alles/](/slides/context-is-alles/?lang=en),
  goes with [the blog post](/en/posts/2026-11-04-context-is-everything/)

### AIs are just like people *(only different)*

Why AI agents make the same mistakes as people, and what you can do about it.
Attention (what sits in the middle of the context gets lost), a briefing as
for a new colleague, one craft per agent and a separate reviewer. And where
the comparison ends: no memory between sessions, never tired, but wrong with
great confidence. Ends with a checklist for tomorrow.

- **Format:** talk or workshop
- **Language:** English or Dutch
- **Deck:** [/slides/ai-zijn-net-mensen/](/slides/ai-zijn-net-mensen/?lang=en)

### Shift left — hooks > good intentions

Why CLAUDE.md doesn't enforce your rule, and what does. The case: a check that
fails in CI twenty minutes after you moved on, while the same check as a hook
takes 21 milliseconds. Five layers from soft to hard (CLAUDE.md, skills,
permissions, hooks and CI) and which rule belongs where. With a reading
version and code as a hand-out.

- **Format:** dev session
- **Length:** ~1 hour
- **Language:** Dutch
- **Deck:** [/slides/claude-shift-left/](/slides/claude-shift-left/),
  [reading version](/slides/claude-shift-left/lees/),
  [code + hand-out](https://github.com/MWest2020/westerweel-work/tree/main/workshops/claude-shift-left)

### Docker — from image to registry

The mental model behind containers: a container is not a VM, and an image is
not a container. Why `docker commit` breaks your CI while a Dockerfile
doesn't. Building, tagging, pushing and pulling, with the dos and don'ts for
production. For a team that pushes images fine from a laptop, but gets stuck
the moment CI/CD takes over.

- **Format:** dev session
- **Length:** ~1 hour
- **Language:** Dutch
- **Deck:** [/slides/docker-101/](/slides/docker-101/)

## Topics

What I like to talk about, also beyond the talks above:

- AI agents in operations: context, knowledge bases, guardrails, evaluation.
- Sovereign infrastructure: Kubernetes, Proxmox, GitOps, own hardware.
- Compliance that follows practice: ISO 27001, living documentation.
- SRE: SLOs that start with the customer, killing toil.

## Bio

For organisers, to copy as is.

**Short**

> Mark Westerweel is a Site Reliability Engineer at Schiphol Airport. He
> builds infrastructure for Dutch organisations that take sovereignty
> seriously, and works out how AI agents can safely take part in operations.
> He writes at westerweel.work.

**Long**

> Mark Westerweel is a Site Reliability Engineer at Schiphol Airport, where he
> defines customer-first SLOs and kills toil. Before that he spent years in
> and around Common Ground and the Dutch municipal landscape: multi-tenant
> Kubernetes, Nextcloud at scale, ISO 27001 work and grant applications.
>
> Next to his work he builds an agent ecosystem on his own hardware: a
> Kubernetes cluster built by hand, agents that build code inside a cage, and
> SREna, an SRE agent that runs entirely locally. He is a Claude Certified
> Architect (Foundation) and one of GitHub's first 5,000 agentic AI
> engineers. He writes at westerweel.work.

## Contact

Email [mark@westerweel.work](mailto:mark@westerweel.work) with the date, the
event and the audience.
