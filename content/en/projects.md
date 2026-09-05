---
title: "Projects"
translationKey: "projecten"
summary: "Personal projects: sovereign tooling, an agent ecosystem on my own hardware, and measurable internet standards."
---

Personal work, next to the consulting. Common thread: open source where
possible, own hardware where necessary, and boring-but-auditable over clever.

## Wordsworth — a sovereign PII pipeline

A document pipeline that turns government documents into a searchable,
privacy-safe corpus: ingest → pseudonymisation → indexing → hybrid search
and question-answering, all self-hosted (PostgreSQL, OpenSearch, a local LLM
via Ollama, S3-compatible object store) — no document and no model call ever
leaves the hardware.

Pseudonymisation is **reversible with key-gated reveal**: detection runs
deterministically (Dutch BSN checksum, IBAN mod-97) plus ML entities, values
are replaced by stable tokens, and only someone holding a valid grant *and*
the cryptographic key can reveal, per PII type. The search index never
contains clear personal data; the append-only audit table doubles as the
pipeline's state machine. Envelope encryption via OpenBao Transit;
fail-closed on any doubt.

- **Demo (synthetic data):** [mwest2020.github.io/wordsworth-demo](https://mwest2020.github.io/wordsworth-demo/)
- **Code:** [github.com/MWest2020/wordsworth](https://github.com/MWest2020/wordsworth) (EUPL-1.2)

## Boomhuis — and the pattern behind it

Boomhuis ("treehouse") is the communication layer of my agent ecosystem: a
self-hosted [buzz](https://github.com/block/buzz) relay (Nostr protocol)
with channels where I and a handful of chat-native agents — builder,
reviewer, architect, marketing — collaborate asynchronously. Every identity
(human and agent) has its own keypair; everything is searchable and
auditable; reachable only over my own tailnet. The repo is private (it holds
identities), but the pattern is worth sharing.

The pattern: **separate the layers, give each layer one job.**

1. **Git is the truth.** Code, verdicts, and audit trails live in git. Chat
   messages are coordination and mirror — never authoritative state.
2. **Execution lives in a cage.** Agents that build code run as Kubernetes
   Jobs with deny-by-default allowlists per role
   ([habitat](https://github.com/MWest2020/habitat), EUPL-1.2), with no
   access to the relay or to secrets. Communication and execution only meet
   through git.
3. **Knowledge has a hub.** One repo
   ([handbook](https://github.com/MWest2020/handbook)) is the inventory and
   entry point; documentation aggregates there, not in every chat again.
4. **Identity is a keypair, not an account name.** Agents are relay members
   with their own keys, roles, and channel permissions — adding, rotating,
   and revoking are ordinary, auditable operations.
5. **Soft advice, hard boundaries.** What an agent *should* do lives in
   conventions; what an agent *must not* do is enforced at the runtime
   boundary. (Why that distinction matters:
   [the shift-left session](/slides/claude-shift-left/), in Dutch.)

No platform bought, no SaaS: a relay, a cluster, a few repos, and strict
agreements. It doesn't scale to a thousand people — it only has to scale to
one human and a crew of agents.

## netnl — measurable internet, in bulk

A command-line client for the **[Internet.nl](https://internet.nl) batch
API**: test a whole fleet of domains for IPv6, DNSSEC, RPKI, and TLS instead
of one domain per browser tab. Submit a host list, poll until the run
finishes (resumable after a closed laptop), and get the result as a diffable
table or JSON for pipelines. A GitHub Action ships with it, so your build
fails the moment your score drops — a CI gate on your own standards
compliance instead of a screenshot in an audit folder.

House rule: **only measure hosts you operate** or have explicit permission
to test.

The batch API needs an account, and that is where nearly everyone gives up.
So there is now a full chain behind it: a self-hosted batch instance on a
VPS, reached over a tailnet, with a **facade** in the homelab in front of it
handling tenants, limits and an audit trail. Anyone who chips in for the
electricity gets a key mailed automatically; the webhook mints it, sends it
once, and stores it nowhere it could be read back.

It measures itself every morning, and the current standing is on the
[demo page](https://mwest2020.github.io/internetnl-cli-demo/) — including
the domain that comes off markedly worse. That number stays up on purpose:
the domain is deliberately closed to the public, and a scoreboard showing
nothing but green ticks measures nothing.

You can host it yourself, but it is a service, not a script. The
[four traps](https://github.com/MWest2020/internetnl-cli/blob/main/docs/how-to/self-hosting-pitfalls.md)
that cost me days are documented separately, including the one where the
official manual leaves you with an instance that cannot reach anything.

- **Code:** [github.com/MWest2020/internetnl-cli](https://github.com/MWest2020/internetnl-cli) (MIT)
- **Try it, no account needed:** [mwest2020.github.io/internetnl-cli-demo](https://mwest2020.github.io/internetnl-cli-demo/)
- **A key for the API:** [buy a coffee](https://buymeacoffee.com/mark.westerweel) from $2 — beta, best-effort, no SLA
