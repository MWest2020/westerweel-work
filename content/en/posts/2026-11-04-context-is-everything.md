---
title: "Context is everything"
date: 2026-11-04
draft: false
tags: ["ai", "agents", "context", "sre", "sovereignty", "local models"]
translationKey: "context-is-alles"
summary: "An agent that guesses is usually missing context, not intelligence. From a hub for infra repos to SREna, a local SRE agent: the knowledge base is what prevents hallucination, not the model."
---

*On the knowledge base as the real difference, and why it is the key to
a sovereign SRE agent.*

A few months ago someone asked an agent how to upgrade a component of
our cluster. The agent gave a neat answer in steps, with the right
commands and a few sensible warnings. It sounded like someone who had
done it ten times before.

Except the procedure was already documented, in a repo the agent could
simply read. The agent had not looked it up. It had put together
something plausible from model knowledge and some searching around.
Nobody could trace where the answer came from, who had checked it, or
how old it was.

The model had the wrong context, or really no context at all. Since
then I sum up almost everything I build with agents in one sentence:

**Context (management) is everything.**

### One entry point, and a fixed order

In [an earlier post](/en/posts/2026-07-14-living-documentation-with-gates-and-agents/)
I described how we made documentation "living": docs next to the code,
an enforceable contract, gates, and an MCP server that gives agents the
aggregated documentation *with provenance*. Owner, review date, source.
The next question was how to make sure an agent actually uses that
server.

The answer is a hub: the coordinator for ten or so infrastructure
repos. Whoever starts a session starts it there. The entry point to the
knowledge centre is the MCP server; the hub makes sure the agent
actually uses it. It takes care of three things.

1. What goes in: every question about a component, the cluster, a
   version or a procedure starts with a search in the knowledge base.
   That is the first action: before `grep`, before `kubectl` and before
   model knowledge. A hit is the answer, with its source. If the
   knowledge base has nothing, the agent may search on its own, but it
   has to say that the knowledge base came up empty.
2. In what order: at first that rule lived only in the instructions.
   Then we saw it fade during a long session: instructions in plain
   text evaporate as the context fills up. Now a hook injects the rule
   again with *every* prompt. That costs four lines of text and a few
   tokens per turn.
3. What stays out: every repo has a catalogue of operations an agent
   may perform on its own, and for anything not in it, the agent asks
   first. Mutating cluster commands are blocked technically. And the
   rules themselves (instructions, hooks, permissions) are read-only to
   the agent. An agent that can modify its own cage is not in a cage.

Since then an agent hardly ever makes up such a procedure. Not because
the model got better, but because the context did.

### At home: the same pattern

At home I work the same way, just in a different domain.

- My [handbook](https://github.com/MWest2020/handbook) is the hub of
  all my own repos. Its description says it literally: *"It's where I
  tell agents to go."* The documentation lives in the projects
  themselves, and the hub holds only the map, the specs and the
  pipeline.
- [Habitat](https://github.com/MWest2020/habitat) lets Claude Code
  agents work autonomously on a home cluster of three mini PCs
  ([homelab](https://github.com/MWest2020/homelab)). They work in a
  cage: outbound traffic is closed except to an allowlist, they have
  minimal rights, and every run leaves an audit trail in git. Here too:
  agents do not rebuild their own cage.
- [Ratatoskr](https://github.com/MWest2020/ratatoskr) is the chat layer
  on top. In my own words, I *"really only want to talk to one agent"*.
  That one agent routes to specialists (builder, reviewer, architect,
  red team). Their definitions live in one place in the handbook, so
  the builder in the chat is the same one as in the cluster.
- My second brain is a markdown-and-git vault with a deterministic
  core. Scheduling, dates and matching are plain Python, and the
  language model sits only at the edges. Every claim points to a
  source, and sources are immutable.

Everywhere it comes down to the same thing: the agent starts at the
knowledge base and stays within boundaries it cannot move itself. The
quality of its work depends mostly on what the model gets to see.

### The logical next step: an SRE agent that runs locally

If it is mostly about context, and the context for SRE work consists of
logs, incidents, configurations and runbooks, then that context is
exactly what you least want to send out the door.

That is why I am building SREna: an SRE agent that runs entirely
locally. The model, the gateway and the conversations all live on the
machine itself, and no operational data goes to a cloud model. She gets
the same treatment as the agents above: a knowledge base as ground
truth, provenance with every answer, and only sources for which
explicit permission has been given.

The potential is large. A colleague who gets an incident in the middle
of the night can have the conversation with someone who knows the
runbooks, the dashboards and the history, with sources cited, without a
single log line leaving the building.

I will be honest about it: we are in the evaluation phase. There are no
users yet. We compare the same agents against a cloud model as a
baseline, and the local model does not reach that baseline yet. The
model choice is still open. There is too little data for it, and I do
not expect a decision before the first quarter of 2027.

So I hardly have real anecdotes yet. She simply is not there
yet. What I do already see is that annotation works. Every source in
the knowledge base gets a label. Gold is confirmed by a human, silver
comes from a source but has not been checked, and bronze is pure AI. What is marked as gold she
takes along better and weighs more heavily. And because every piece of
knowledge has a label, she is honest about where her answer comes from.
That helps with evaluation too: you can see which agent did its job
well and which did not. The idea is not mine. I borrowed it from
Google, from their work on AI for SRE.

### What a local model teaches you

A large cloud model is forgiving. If a source is missing, it fills the
gap with broad knowledge, and often that even sounds good. Exactly what
the agent in the opening did. A smaller local model does the same, but
worse. That is what makes the gap visible.

At first that felt like a setback. By now I see it as the most useful
thing the local model does: it is an honest mirror of your context.

Hallucinations have an address. When the model made something up, it
was usually because a source was missing or wrong. The problem was in
the knowledge base, and that is also where it can be fixed.

The context window is a budget. Everything you put in comes at the
expense of something else. A search that is too broad or a full log
file pushes the instructions out, and then you get truncated or
nonsensical output. Small, bounded searches work better than everything
at once.

A model that "just tries something" has too much room. Tool calls went
wrong as soon as the model had to guess which call made sense. What we
are betting on now: fewer tools, structured output, and citations that
are checked mechanically, so that the model would rather refuse than
guess.

Permissions are context too. Access to information is something other
than permission to give it to a model, and that in turn is something
other than permission to share it. You record that boundary in the
knowledge base itself, so a prompt does not have to remember it.

Pin everything, and measure yourself. Lock the model to an exact
revision, and pin the runtime together with all its dependencies. You
choose based on what the model does on your own machine; the maker's
benchmark says little about how it performs on your hardware and your
tasks. And that means eval runs, lots of eval runs. Without a baseline,
every impression is a feeling.

The biggest lesson fits in one sentence: the knowledge base is what
prevents hallucination, not the model.

### Context is the real work, and it is yours

With a cloud model you can be sloppy with context and often get away
with it. A local model punishes that. But the work you do to make a
local model usable (curating sources, recording provenance, enforcing
the order, drawing boundaries) makes *every* model better. And that
work stays when you switch models.

To me that is the core of sovereignty in AI. Where the model runs
matters, and who owns the context matters even more: your knowledge,
where it comes from and where the boundaries are. That context lives in
plain files in git and it is yours. That is what makes the model
replaceable. The model choice will be made in the first quarter of
2027. The context simply comes along.

Context (management) is everything.

---

*P.S. At home I do not run large local models. I do not have the
hardware for it (yet), so the heavy lifting runs on my Claude
subscription. What does run locally are very small, specialised models. Does anyone
have a machine with a lot of memory looking for a good home? I know a
homelab that would love to join in.*
