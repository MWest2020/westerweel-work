---
title: "Ricin breaks your model. Not your data."
date: 2026-06-17
draft: false
tags: ["ai", "privacy", "security", "rag", "compliance"]
translationKey: "output-safety-vs-data"
summary: "Why the most popular AI safety test secures the front door while leaving the back door wide open. Output safety and data confidentiality are technically two completely different mechanisms — and conflating them is exactly what's behind the confusion on the work floor. Here's how models actually handle your data, and what to arrange instead of the theatre."
---

*Why the most popular AI safety test secures the front door while leaving
the back door wide open — and what to arrange instead.*

When organisations test the safety of an AI model, they almost always look
at the same side of the coin: **what comes out?**

In my case, after too much *Breaking Bad*: how do you make ricin? The model
politely refuses. That test passes. The conclusion people then draw on the
work floor is logical but dangerous: "The filters work, so the system is
safe."

But here's the crucial fallacy. The ricin test proves that the **output
security** is in order. The model doesn't spit out dangerous things. But
that test, misleadingly, answers the wrong question. Because the real
question for an organisation isn't what comes *out* of the model, but what
happens to the data you put **in**.

Output safety and data confidentiality are technically two completely
different mechanisms. They have nothing to do with each other. While you're
reassured that the model doesn't generate bioweapons, your sensitive input
can still leave your organisation through the back door.

To see how that works, we need to look at a discussion I had recently at an
organisation on the work floor.

### The trigger: a conversation in a regulated sector

This piece grew out of a conversation with an organisation in a heavily
regulated sector. A team of professionals there had been working
organically with language models for a while to analyse texts and compare
internal documents. Very sensible and efficient work.

But when processing documents with sensitive information, it started to
itch. The internal guidelines contained data that is deliberately not
public. One half of the team was therefore cautious: "Doesn't this data go
into the model, and could someone else pull it back out later?" The other
half played it down: "Nonsense, you don't get weird things out of it, the
filters are very strict. After all, the model refuses when you ask for
scary stuff."

See what's happening here? The reassurance about what goes *out* (no misuse
via the output) masks the risk of what goes *in* (data confidentiality of
the input). Because the team was working on individual *consumer*
subscriptions (ChatGPT Plus). And that's precisely the leak at the back
door.

### How a model is trained (and why it's frozen)

To understand why that front-door filter doesn't protect your input, we
need to look at how such a model comes to exist. A language model is trained
in two phases, and both are **offline**.

First, **pretraining**: the model learns, on enormous amounts of text, to
predict the next bit of text over and over. Months of compute, whole halls
of GPUs. What comes out are the *weights* — the learned parameters, billions
of numbers. Then **post-training**: shaping the behaviour with human
feedback and rules (RLHF, Constitutional AI), including the safety training
that teaches the model to refuse, for example, bioweapons.

The point to hold on to: training is a separate, expensive, one-off
process. The model you use is a frozen snapshot from after that training. It
does *not learn* while you talk to it. Your prompt changes not a single
weight live.

> Want to actually see this instead of taking it on faith? Play with
> [bbycroft.net/llm](https://bbycroft.net/llm) — an interactive 3D
> cross-section of a GPT as it processes tokens — and watch the transformer
> series by [3Blue1Brown on
> YouTube](https://www.youtube.com/watch?v=wjZofJX0v4M). An hour of your
> time, and you'll never take a marketing promise at face value again.

### How your data gets into (or past) a model

There are three ways to make a model "know something about your
organisation". People judge them on one axis, while there are two — and
conflating those two is exactly what's behind the confusion on the work
floor.

- **Axis 1 — does your data end up in the *weights*?** Does it become a
  permanent part of the model, where someone else could later pull it back
  out through memorisation?
- **Axis 2 — does your data leave your *premises*?** Does it go to a third
  party's servers, outside your own control and jurisdiction?

Against those two axes, the three methods look like this:

- **Fine-tuning / continued training** — your data is baked into a (copy of
  the) model. The weights change (axis 1: yes) and it runs at an external
  provider (axis 2: yes). What's in there can come back out: memorisation is
  real, not a hypothesis.
- **RAG (retrieval-augmented generation)** — your documents sit in your own
  vector store; the weights stay untouched (axis 1: no). But watch out: on
  each question the relevant chunks are retrieved and *sent to the model in
  the prompt*. If that model runs in the cloud, those chunks — including your
  sensitive internal data — still leave your premises (axis 2: yes). RAG
  protects the weights, not automatically the confidentiality.
- **In-context / prompting** — you paste context into the window of that one
  conversation. One-off, no weight update (axis 1: no). But the prompt does
  go to the provider (axis 2: yes).

Here's the fallacy I heard on the work floor. "Our data becomes the model
and comes back out for someone else" is an **axis 1** fear, and that indeed
applies mainly to fine-tuning. But the sensitive internal data from the real
case is almost entirely an **axis 2** problem: the data leaves your
premises, regardless of whether it's ever trained on. And axis 2 is in play
on *every* cloud call — prompting, RAG and fine-tuning. That's why "we only
do RAG, no fine-tuning" doesn't solve the confidentiality question.

### Inference is not training — but logging can become it after all

We just saw that a prompt doesn't change a weight live. Yet there's an
indirect route back to axis 1, and it doesn't run via the conversation but
via the *logs*. Your prompt only ends up in a future model if (a) the
provider stores your input *and* (b) that storage is included in a later
training round. That depends entirely on your subscription type — not on
whether you pay, but on the *kind* of account:

- **Commercial** (API, Enterprise, Business): by default they do *not* train
  on it. See for example Anthropic's
  [privacy page](https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training)
  or OpenAI's [enterprise privacy](https://openai.com/enterprise-privacy/).
- **Consumer** (Free / Pro / Plus): by default they do, unless you actively
  opt out via the settings.
- **The feedback button**: watch out — a thumbs up or down can pull that
  specific conversation into the training pool after all, *even* on
  enterprise (see this
  [explainer with sources](https://secureprivacy.ai/blog/gpt-5-training-data-opt-out)).

This "Shadow AI" gap of individual consumer accounts on the work floor is,
in practice, the real risk. If data goes into the training pipeline, it can
come back out through memorisation. In the Reddit lawsuit against Anthropic,
for instance, it was argued that a model could reproduce deleted posts
almost verbatim. *That's* why your contract type is the control — not the
model behaviour at the front.

### Guardrails protect the wrong side

That ricin refusal comes from misuse controls. The first layer sits in the
weights (post-training). The second layer is **Constitutional Classifiers**:
a separate filter layer *around* the model that scans and blocks both the
input and the output. This isn't a change to the weights, it's a guardrail
around them (read the [research paper](https://arxiv.org/abs/2501.18837) or
Anthropic's [own
explanation](https://www.anthropic.com/research/constitutional-classifiers)).

Those classifiers aren't a sham — they demonstrably block jailbreaks and do
exactly what they promise. But note *which* side they protect: they handle
**output safety** (what the model puts out). They say nothing at all about
**data confidentiality** (what happens to your input). They're real
controls, just on the wrong axis for your question. The ricin test measures
the first and wrongly reassures you about the second. *That's* the theatre:
not the guardrail, but the test as proof of data security.

Even the promise "we delete data after 30 days" isn't a law of nature. In
the New York Times lawsuit OpenAI had to *retain* certain data, straight
through its own deletion policy
([explanation](https://openai.com/index/response-to-nyt-data-demands/)). But
look who fell outside the order: Enterprise, ZDR and EU customers. The order
cut through the default retention promise, but precisely the tier and region
controls held. That's not a footnote to my advice — it's the proof of it.
(The order has since been largely reversed, but the point stands: *delete*
is a UI feature, not a guarantee.)

### So what should you actually arrange?

Not testing the front door with scary questions. Rather, setting up the
legal and technical framework at the back:

1. **DPIA** (data protection impact assessment) before you start. This
   forces your team to get the risks sharp.
2. **Data Processing Agreement (DPA)** with every provider that touches
   personal data. No DPA = unlawful processing.
3. **Zero Data Retention (ZDR)** contracted explicitly for sensitive flows.
   ZDR means input and output aren't stored after the answer. Note: this is
   never on by default — you have to request it per endpoint. Without a ZDR
   contract, even an API often has a retention period for abuse detection.
4. **EU region / data residency** locked down contractually.
5. **Data minimisation and pseudonymisation**: no identifiable personal data
   in prompts unless strictly necessary.

Working on individual consumer subscriptions right now? Then the fastest win
is the simplest: switch to **ChatGPT Business**. In euros it's even slightly
cheaper than individual Plus subscriptions, training is off by default, and
you get management and oversight of what's happening. Mind you: "not
training" isn't the same as "not storing" — for the truly sensitive flows
the next question remains the most important.

### The question everyone skips

And finally, the most important question:

**Do you even need a cloud model for this task?**

For editing, summarising, structuring or comparing texts? No. A local model
— [Ollama](https://ollama.com) on a decent GPU, or an EU-hosted private
instance — handles that fine.

If the data never leaves your own infrastructure, both axis 1 and axis 2
fall away in one go: no training, no retention, no jurisdiction question.
That also settles that whole discussion on the work floor at a stroke. If
the data doesn't leave the house, the risk the cautious colleagues worry
about is gone — and the others had a point too, because information can be
misused through plenty of other routes. But that's an argument about the
output. About what you give away on the input side, it says nothing. So you
solve it on the input side.

The safest data is the data that never leaves your house. And a model that
refuses ricin at the front door does not protect the data at the back door.
Arrange the framework, not the theatre.
