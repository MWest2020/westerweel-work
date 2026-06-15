---
title: "Curated, shareable skillsets for AI agents"
date: 2026-06-15
draft: true
tags: ["ai", "claude-code", "skills", "provenance", "devops"]
translationKey: "curated-skillsets"
summary: "A skill for an AI agent is a markdown file. That's exactly the problem: anyone can drop one, nobody knows if it's any good. Here's how I turn them into a curated, signed, shareable library — and why the point isn't the skills, it's the curation."
---

I recently came across a GitHub repo with a single skill in it:
[`owasp-security`](https://github.com/agamm/claude-code-owasp) — OWASP
Top 10:2025, ASVS 5.0, the LLM Top 10, neatly laid out as a checklist
for an AI agent. 233 stars, MIT licence, looks solid. The temptation is
to copy it into `~/.claude/skills/` and move on.

I didn't. Instead I ran it through a pipeline, and that's where the
story is.

### A skill is just a file — and that's the problem

To Claude Code (and most agents) a
[skill](https://github.com/anthropics/skills) is a `SKILL.md`: some
frontmatter, a "when to use", and a slab of instructions. Low friction,
which is the charm. But it also means: no quality bar, no provenance,
no idea whether the content still holds. You collect a handful, they
quietly rot, and your agent behaves like the worst one that happens to
fire.

For code we've solved this for years — review, versions, provenance,
signing. For skills most people do nothing. So I built a small CLI,
`skill-forge`, that treats skills as what they are: artifacts that
deserve curation.

### The curation loop

Skills arrive as **drafts**, not truth. Then:

| Step | What happens |
|---|---|
| `import` | bring it in, record provenance (origin + source URLs) |
| `judge` | an LLM scores it against a fixed rubric (clarity, actionability, coverage, provenance) |
| `promote` | only if the score clears the bar (total ≥ 0.75, every axis ≥ 0.50) |
| `refine` | improve across numbered iterations, with a diff and an audit trail |

Back to `owasp-security`. The judge gave it 0.87 — strong on
actionability and coverage. But one axis stuck at 0.60:
**provenance**. The `## Source` section pointed only at the GitHub
repo, not at the OWASP and ASVS standards the skill actually leans on.
A fair finding. One `refine` later — authoritative sources added, the
rest untouched — it sat at 0.88 with that axis at 0.85. Only then
promote.

The point isn't the score. The point is that a *judgement* sits in the
middle, with a trail someone else can re-walk. Not a loose folder of
prompts, but a library with provenance — each skill signed with an
Ed25519 stamp, so tampering shows.

### The core: skillsets you can share

This is the reason the thing exists. A curated skill is nice; a curated
*set* you can share is the whole point.

Skills carry **tags**, and a *skillset* is simply a query: "every live
skill tagged `security`". No separate file, no registry — a tag and a
question. With that you mount a vetted subset instead of your whole
library:

```bash
forge ls --tag security                 # what's in the set
forge sync claude-code --tag security    # mount only that set
```

A review container gets the `security` set. An exam-prep container
gets the `examenstof` set. Neither gets the rest, and neither has to
trust a shared disk.

### The future plan: skillsets over the wire

That last bit — "no shared disk" — is where this is headed. `sync`
works through symlinks: fine on one machine, useless for a
containerized agent. So there's now a small, **read-only** MCP server
on top:

```bash
forge serve mcp    # tools: list_skills, get_skill, get_skillset
```

A container starts it, asks `get_skillset("security")`, and gets the
vetted set over the protocol — provenance included, never able to reach
the rest of the library. Read-only is a hard line: the server serves
the curated output, never the curation itself. Importing, scoring,
promoting — that stays local and deliberate.

### Why this, and no more

The through-line is the one I keep for infrastructure: boring and
auditable. No federation, no marketplace, no clever distribution web —
that layer was deliberately stripped back out when it didn't earn its
keep. What's left is the smallest core that does the job: curate, sign,
group, and hand over read-only.

An AI agent is only as good as the instructions it's allowed to load.
Those instructions deserve the same discipline as your code: a bar to
get in, a provenance to fall back on, and a way to share exactly the
right set — no more, no less.
