---
name: grill-me
description: Get interviewed in rounds about a plan or design until every decision is settled.
disable-model-invocation: true
---

# Grill Me

## Overview

A relentless interview that forces a plan or design to become precise before anyone acts on it. Run it whenever real decisions are still unresolved, and before `to-spec` turns the conversation into something durable.

## The interview is a tree, asked in rounds

Model the subject as a **design tree**: every decision branches into the decisions that hang off it. The **frontier** is the set of questions whose prerequisites are all settled - the only questions that can honestly be asked yet. A **round** asks the frontier; the answers settle decisions and move the frontier outward, and the next round asks what that unblocked. Two questions never share a round if one depends on the other.

Weight rounds by difficulty: a genuinely hard question gets a message to itself, with the context it needs; quick confirmations travel grouped. Many questions in one round is fine when they are all cheap.

Format every question so a round can be answered by number, numbering continuously across rounds:

```
❓ **Q1 - <title>**: <body, with the options where options exist>

➡️ <your recommended answer, always>
```

The user answers by number ("Q1 agree, Q2 the second option, Q3 no, because..."), which also suits dictation. If they prefer one question at a time, switch to that for the rest of the session.

## Look up facts, ask about decisions

If something can be answered by reading the codebase, the docs, or running a command, do that instead of asking - dispatch a subagent for anything slow, and don't block the round on it: only the questions downstream of a running lookup wait, the rest of the frontier is asked now. Reserve questions for what only the user can decide. An interviewer that answers its own decision questions has broken the skill, not interpreted it liberally.

## Ungrillable questions

Some questions can be answered by talking; others need something to react to - "how should this interaction feel?", "one long form or three pages?". When one surfaces, say so and route it to the **prototype** skill instead of rephrasing it; keep grilling the rest of the frontier, and fold the answer back in once the prototype has been seen. Talking through an ungrillable question is where sessions balloon.

## Scope

Count rounds, not questions: many questions across a few rounds is an ordinary session, and it ends when the frontier is empty. A session that keeps running usually means the scope was too big - break the work into smaller pieces and grill each one.

## Ask in plain text

Ask questions as plain text in the conversation. If the user asks for the pop-up UI (the AskUserQuestion tool), switch to it for the rest of the session - it is theirs to opt into, not the default.

## Sharpen the language as you go

- **Challenge fuzzy terms.** When a vague or overloaded word shows up, propose a precise canonical term and confirm it. ("You said 'account': do you mean the Customer or the User? Those aren't the same thing here.")
- **Stress-test with scenarios.** When a domain relationship comes up, invent a concrete edge case that forces precision about where the boundary actually sits.
- **Cross-reference with code.** If the user describes how something works, check whether the code agrees. Surface any contradiction immediately rather than letting it slide.
- **Challenge against the glossary.** If the repo has a `CONTEXT.md`, check each term against it and call out conflicts on the spot. ("Your glossary defines 'cancellation' as X, but you seem to mean Y - which is it?")

## Record what gets settled

Write decisions down as they land, not in a batch at the end. Three destinations, and the test between them is whether the decision **outlives the work in front of you**:

- **The ledger, always.** Every resolved question goes into `docs/ledger.md` as part of the session narrative. It is cheap, chronological, and the thing a future session reads first.
- **`CONTEXT.md`, on projects with real domain vocabulary.** Where the project has terms that a newcomer would get wrong - a Customer that isn't a User, a Booking that isn't a Reservation - keep a root `CONTEXT.md` glossary and update it the moment a term is settled, not in a batch afterwards. Create it lazily, when the first term resolves. It is a glossary and nothing else: no implementation detail, no spec, no scratch pad. Small projects and ones with no real vocabulary of their own skip it, and `start` and `update-docs` both treat it as optional for exactly that reason.
- **An ADR, only when it outlives the work - and all three locks click:** (1) **hard to reverse** - changing it later costs something real; (2) **surprising without context** - a future reader would ask "why is it built this way?"; (3) **a real trade-off** - there were genuine alternatives and one was chosen for reasons. Any lock missing, skip the ADR; the ledger entry is enough. Write one ADR per such decision, including the option you turned down and the reason.

Resist writing an ADR per resolved question. A directory of thirty thin ADRs buries the four that mattered, and a record nobody reads is the same as no record.

## Don't act until there is shared understanding

Nothing gets implemented, scaffolded, or written into a spec until the interview has genuinely converged, not merely until the user seems tired of answering.

## It's working if

- A round arrives as a numbered list, each question with its recommendation on its own ➡️ line, and the user can answer the whole round by number.
- Nothing in a round needs another question in the same round answered first, and later rounds ask things the first round could not have asked.
- Facts get looked up - files read, subagents dispatched - rather than asked, and a running lookup stalls only its own branch, never the round.
- Question count stays high while round count stays low.
- The user pushes back somewhere. A session with no pushback is a session that wasn't needed.

## Handoff

Once every branch is resolved, say so plainly and point back to whatever asked for the grilling (usually `to-spec`) so the conversation continues with the decisions locked in.
