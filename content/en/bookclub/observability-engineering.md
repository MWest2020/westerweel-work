---
# One book = this one file; the English translation of
# content/nl/boekenclub/observability-engineering.md. Content from Mark's brief of
# 2026-11-14; nothing about the book was made up by the builder. No chapter numbers,
# no employer named. Scores and "read it yourself": Mark (mail 2026-11-14).
title: "Observability Engineering"
translationKey: "boekenclub-observability-engineering"
subtitle: "Achieving Production Excellence"
author: "Charity Majors, Liz Fong-Jones and George Miranda"
publisher: "O'Reilly Media"
year: 2022
weight: 3
date: 2026-11-14
photo: ""
quote: ""

hook: "This book is just freaking gold. It goes deep from the first chapters, and held up a mirror to me the whole way through."

insights:
  - title: "High cardinality, high dimensionality, explorability"
    text: "Nuggets of gold from the start. Valid observability needs high-cardinality data, high dimensionality and the ability to explore it. That basic formula gets you a long way. In my opinion, that section alone is almost worth the price of the book."
  - title: "The basics, and debugging from first principles"
    text: "The fundamentals are well covered: the three pillars, what an event is, what spans are and what goes in them. Some of it may feel obvious to experienced readers, much like the ‘90% common sense’ complaint about Platform Engineering, but it's done well. And you learn to investigate from first principles: a verifiable way to get to the bottom of problems."
    nugget: "A guest chapter from Slack: how they did it, what works and what doesn't."
  - title: "Dashboards that confirm your own bias"
    emphasis: true
    text: "The hard truth that hits closest to home. Many engineers monitor only via logging and build dashboards on known unknowns, mostly to confirm their own bias. I see it wherever I work. With LAMP stacks that maybe worked twenty years ago; with microservices and the cloud it can't. Prepare for unknown unknowns."
  - title: "Honest about their own bias"
    text: "Hats off: they built Honeycomb and openly admit their bias. Even so, they fairly explain when buying is better, and what you hit when you build your own. That goes for any open-source tool: build it if you really need to and you're big enough. Otherwise you're fooling yourself, with hidden maintenance and capacity."
  - title: "Open source is free, but not free"
    text: "Open source is free, but not free of time, energy and capacity. I see that fallacy online a lot. SaaS can be expensive; the book explains why, and how to bring those costs down. It closes with a maturity model, which is good too."

scores:
  - name: "Directly applicable"
    value: 4.5
  - name: "Depth"
    value: 5
    note: "from the very first chapters"
  - name: "Readability"
    value: 4.5
  - name: "Shelf life"
    value: 5
    note: "timeless"

for_whom_line: "For engineers and teams moving from logs and dashboards to real observability."
for_whom:
  - "Engineers who now monitor mainly through logging"
  - "Teams moving to microservices and the cloud"
  - "Anyone choosing between building and buying"
not_for_whom:
  - "People outside tech"

further_heading: "Read it yourself"
further_reading:
  - title: "This book: free PDF via honeycomb.io"
question: "Which hard truth hit you hardest?"
---
