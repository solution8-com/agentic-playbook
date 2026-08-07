---
name: improve-codebase-architecture
description: Scan a codebase area for deepening opportunities - refactors that turn shallow modules into deep ones - and present them as a visual HTML report to pick from.
disable-model-invocation: true
---

# Improve Codebase Architecture

## When to run it

Periodic, not per issue. Any of:

- **At the end of a session, once in a while.** Not every session - often enough that drift
  does not compound. This is the routine trigger.
- At a milestone, when a chunk of work has landed and the shape has settled.
- On a smell: the same helper written a third time, a module nobody wants to touch, a
  convention that has quietly split in two.

**This is the counterpart to per-issue code review, which structurally cannot see across
issues.** Batching reviews is the wrong fix - a bigger diff just gets less attention per
line - so run this periodically instead.

Local cleanup inside one issue stays in **tdd**'s refactor step. This is for the shape of
the codebase, not for tidying a function.

## Overview

Surface architectural friction in a codebase area and propose **deepening
opportunities**: refactors that turn a shallow module (interface nearly as complex as
its implementation) into a deep one (a small interface hiding real leverage). The goal
is testability and making the area easier for both humans and agents to work in.

## Vocabulary

Use these terms consistently in every finding; don't drift into "component,"
"service," or "boundary" instead.

- **Module** - anything with an interface and an implementation: a function, class,
  controller, store, or a whole domain directory.
- **Interface** - everything a caller must know to use the module: types,
  invariants, error modes, ordering, config, not just the function signature.
- **Depth** - how much behavior sits behind how small an interface. Deep = high
  leverage. Shallow = the interface is nearly as complicated as what's behind it.
- **Seam** - a place behavior can be swapped without editing in place (a plugin
  registry, an RPC controller boundary, an adapter around an external service).
- **Deletion test** - imagine deleting the module. If the complexity vanishes, it
  was a pass-through that wasn't earning its keep. If it reappears across every
  caller, it was doing real work.

If the repo you're touching has ADRs, a glossary, or its own conventions doc, read them
first and let them inform naming and avoid re-litigating settled decisions. Where those
live varies by repo: `CONTEXT.md`, `docs/adr/`, or a conventions tree of its own.

## Process

### 1. Explore

Read whatever the repo documents about the area first, loading the narrowest relevant
page rather than the whole tree. Scope the walk before starting it: read the last ~20
commit messages and bias exploration toward actively-developed paths, and apply YAGNI
to the area itself - friction in code nobody is touching does not earn a card. Then use
the Agent tool with `subagent_type: Explore` to walk the actual code.
Don't apply a fixed checklist; explore and note friction:

- Where does understanding one concept mean bouncing across many small files?
- Where is a module's interface almost as complex as what it wraps?
- Where were pure functions extracted for testability, but the real bugs live in how
  they're called (no locality)?
- Where do two modules leak details across their seam that neither should know about
  the other?
- What's hard to test through its current interface?

Run the deletion test on anything that looks shallow. "Complexity reappears
elsewhere" is the signal that it's a real candidate.

Identify the repo's own high-risk areas and treat them accordingly: anything the project
marks sensitive in its conventions doc, plus the usual suspects (persistence and
migrations, auth and secrets, process or transport layers, self-update paths). Note
friction there, but flag those findings as needing extra care in review rather than
something to act on quickly.

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory, never into the repo.
Resolve the temp dir from `$TMPDIR` (fallback `/tmp`), write to
`<tmpdir>/architecture-review-<timestamp>.html`, and open it (`open <path>` on
macOS). Tell the user the absolute path.

Use Tailwind via CDN for layout and Mermaid via CDN for graph-shaped relationships
(call graphs, dependency chains, sequences); hand-drawn SVG/CSS works better for more
editorial before/after comparisons. Each candidate gets its own card:

- **Files** - which modules are involved.
- **Problem** - why the current shape causes friction.
- **Solution** - what would change, in plain language.
- **Benefits** - in terms of locality, leverage, and what tests would improve.
- **Before/after diagram**.
- **Recommendation strength** - `Strong`, `Worth exploring`, or `Speculative`.

Close with a **Top recommendation**: which candidate to tackle first and why.

Don't propose concrete interfaces yet in the report. Ask the user which candidate to
explore.

### 3. Grilling loop

Once picked, walk the design with the user (the **grill-me** skill pairs well here):
constraints, dependencies, the shape of the deepened module, what sits behind the new
seam, which tests survive the refactor.

- If a new concept gets a name during the conversation and the project keeps a
  glossary, add the term there.
- If the user rejects a candidate for a reason worth remembering, and this repo
  records architecture decisions, offer to write it down so a future pass doesn't
  re-suggest the same refactor.

## Related skills

- **grill-me** - the interview loop for the grilling step once a candidate is picked.
- **systematic-debugging** - when a bug's post-mortem points here instead of the
  other direction.
- **tdd** - once an interface is agreed, drive the actual refactor test-first.
