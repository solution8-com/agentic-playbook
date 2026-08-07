---
name: to-questionnaire
description: Turn the open questions in a session into a fillable questionnaire for the one person who can answer them.
disable-model-invocation: true
---

# To Questionnaire

## Overview

Turns a decision you can't settle on your own into a **questionnaire**: a self-contained document handed to the one person who holds what you're missing - a client, a stakeholder, a teammate - for them to fill in async or for the two of you to walk through in a meeting.

**Grill the user about the send, never the subject.** Interviewing you about the topic is pointless here - not knowing the topic is why you're writing to someone else. Route by whose head the answers are in:

| The answers are in... | Reach for |
| --- | --- |
| Your own head, unsharpened | **grill-me** |
| The codebase or the docs | look it up, don't ask anyone |
| Someone else's head | **to-questionnaire** |
| Nobody's head yet - the question needs something to react to | **prototype** |

The common case is a grilling session that stalls because some of what surfaced isn't yours to answer. Run this in that same conversation, take those questions offline, and carry on grilling what remains.

## The two-exchange interview

Ask only the two things the user can always answer:

1. **Who is it going to?** Role, expertise, relationship. This fixes the tone and how much context the document must carry - an outside client needs orienting, a teammate does not.
2. **What do you need back?** The concrete decisions or facts that can't be resolved alone. This becomes the checklist the finished document is measured against: every item named gets a question aimed at it.

Then stop asking. A question about the subject itself is the skill off the rails.

## The document

Build from [`TEMPLATE.html`](TEMPLATE.html): a self-contained S8-styled HTML file, saved as `to-questionnaire-<slug>.html` in the current directory. The recipient opens it in any browser, types answers directly into the answer boxes (saved locally as they type), and presses **Export answers** to get the filled-in document back as a markdown file to send in return. No server, no setup. Everything above the template's content marker is fixed library - style and the save/export machinery - and is never hand-edited; author only the content.

Shape of the content:

- A purpose line naming the decision riding on it, and a short context section written for a recipient who was never in your head.
- Questions ordered most-important-first and grouped under themed headings - async means you may only get one pass.
- One idea per question, never compound, with a *why this matters* line only where a question could be misread.
- Explicit permission to answer "I don't know" - a flagged uncertainty is useful; a confident guess that reads like a fact is not.
- A closing catch-all: anything we didn't ask that we should know?

Keep it flat: a grouped list, not a branching tree, and one document for one person per run.

## Bringing the answers back

When the exported answers return, feed them into the conversation that was waiting on them - typically as input to the next grilling round, with each answer traced back to the decision that needed it.

## It's working if

- The interview asks about the recipient and about what's needed back, then stops.
- Every "what I need back" item is traceable to a question in the document.
- The questions read as aimed at what the recipient knows, not your own open questions copied down.
- Someone who wasn't in the conversation would know why they got it and what to do with it.
- Typed answers survive closing and reopening the file, and Export produces a markdown file containing every question with its answer.

## Related skills

- **grill-me** - the session this usually forks from and returns to.
- **prototype** - for the questions nobody can answer yet.
