---
name: to-issues
description: Break a published spec into vertical-slice GitHub sub-issues with blocking edges, labels and hot files.
disable-model-invocation: true
---

# To Issues

## Overview

Breaks a published spec into GitHub issues, each an independently-grabbable **vertical slice**
(a tracer bullet: thin but end-to-end, deliverable on its own) rather than horizontal layers
that only add up at the end. Each issue declares the issues that **block** it, so the work has
a real dependency shape rather than an implied order.

Slices are published as **real GitHub sub-issues of the spec issue**, so the spec renders
its own breakdown, and labelled on three dimensions: **type** (`feature`/`bug`/`task`),
**severity** (`high`/`medium`/`low`) and **autonomy** (`afk`/`hitl`).

Sits after **to-spec**. Downstream, **start-dev** plans the day across what this
publishes, and **pickup-issue** works the slices one session at a time.

## When to use

- A spec has been published and needs to become discrete work items.
- A user asks to "make the issues / tickets", "break this down", "cut the spec into work".

**The floor:** if the whole change fits in one fresh context window, skip this skill and go
straight to the build. Over-decomposition is the most common failure mode of issue-cutting;
twelve issues for a three-line change is worse than no issues at all.

## Where the issues go

By default the project tracks issues on **GitHub via the `gh` CLI**. Publish each slice with
`gh issue create`.

**Fallback:** if `gh` is unavailable, or the repo has no GitHub remote, write each issue to
`docs/issues/<slug>.md` (`<slug>` being a short kebab-case name for the slice). Tell the user
where you wrote them.

If the project has a `CONTEXT.md` or other glossary, use its vocabulary in issue titles and
descriptions.

## Process

### 1. Gather context

Work from what is already in the conversation. If the user passes a reference (a spec path, an
issue number or URL), fetch it and read its full body and comments.

### 2. Explore the codebase

If you have not already, explore to understand the current state of the code, and respect any
ADRs in the area you're touching.

Look for opportunities to **prefactor** the code to make the implementation easier. "Make the
change easy, then make the easy change." Any prefactoring becomes its own slice, sequenced
first.

### 3. Draft vertical slices

<vertical-slice-rules>
- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests), vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Prefer many thin slices over few thick ones
- Any prefactoring is done first
</vertical-slice-rules>

Give each slice its **blocking edges**: the other slices that must complete before it can
start. A slice with no blockers can start immediately.

**On a board with existing open issues, the edges go both ways.** A mid-project run - a
new feature grilled, specced and cut in a later session - does not just wire the new
slices to each other. Read the open issues first; where a new slice blocks or is blocked
by an existing issue, wire that edge too, and **update the existing issue** when the new
work changes its dependencies. A board where only the newest issues have honest edges is
a board whose frontier lies.

| Good slice | Bad slice |
|---|---|
| Thin end-to-end feature, shippable alone | A whole layer (all the DB, or all the UI) |
| Independently grabbable | Only meaningful once three others land |
| Clear acceptance criteria | "Refactor X" with no observable outcome |

**Check each acceptance criterion can fail.** Three broken shapes recur: a criterion
already true before the work starts, one only satisfiable by work another slice owns, and
one that restates the request instead of deriving from the behaviour. For each criterion,
name the observation that would show it false, and confirm it fails at the commit the
implementer starts from.

**Wide refactors are the exception to vertical slicing.** A wide refactor is one mechanical
change - rename a column, retype a shared symbol - whose **blast radius** fans across the whole
codebase, so a single edit breaks thousands of call sites and no vertical slice can land green.
Don't force it into a tracer bullet; sequence it as **expand-contract**:

1. **Expand:** add the new form beside the old so nothing breaks.
2. **Migrate:** move call sites over in batches sized by blast radius (per package, per directory), each batch its own issue blocked by the expand. CI stays green batch to batch because the old form still exists.
3. **Contract:** delete the old form once no caller remains, in an issue blocked by every migrate batch.

When even the batches can't stay green alone, keep the sequence but let them share an
integration branch, and have them all block a final integrate-and-verify issue. Green is
promised only there.

### 4. Label each slice

The labels are **descriptive, not routing**. They tell whoever reads the issue list what
kind of work each slice is and how urgent it is. No skill gates on them, so a wrong label
costs a reader a wrong expectation, not a broken pipeline.

Three dimensions, one label from each:

**Type** - what kind of work it is.

| Label | Meaning |
|---|---|
| `feature` | New capability |
| `bug` | Something is broken |
| `task` | Work that is neither: a migration, a config change, a cleanup |

**Severity** - how much it matters.

| Label | Meaning |
|---|---|
| `high` / `medium` / `low` | Priority, in the ordinary sense. `start-dev` orders the frontier by it. |

**Autonomy** - whether a human is needed *during* the build.

| Label | Meaning |
|---|---|
| `afk` | Nothing in this slice needs a person mid-flight. The agent can build it start to finish. |
| `hitl` | The agent has to stop and ask: an architectural call, a design choice, a decision it cannot make alone. |

The autonomy test is **during the build**, not at any point. Every issue gets human
attention eventually, so "a human sees it at some stage" would make every slice `hitl` and
the label would distinguish nothing.

**Default to `hitl` when further grilling is plausible** - an open design edge, a choice
the spec left to taste, an ambiguous acceptance criterion. Mark `afk` only when the slice
is small and decision-free: nothing left to grill. Downstream, `pickup-issue` routes
`hitl` slices through **grill-me** and lets `afk` slices skip straight to the build, so an
optimistic `afk` on a slice with a real open decision means the decision gets guessed
instead of asked.

Type and severity are the conventional tracker labels anyone will recognise.

Read all three off the slice rather than asking per issue. Confirmation happens once, in
the next step.

### 5. Quiz the user

Present the proposed breakdown as a numbered list. For each slice show:

- **Title**: short descriptive name
- **Labels**: type, severity, autonomy
- **Blocked by**: which other slices (if any) must complete first
- **What it delivers**: the end-to-end behaviour this slice makes work

Ask:

- For each slice: **what can I demo when this is done?** A slice with no answer is a
  horizontal slice in disguise - recut it.
- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct - does each slice only depend on slices that genuinely gate it?
- Should any slices be merged or split further?
- Are the labels right - is anything marked `afk` that will actually need you mid-build, and does the severity ordering match what you would work on first?

Iterate until the user approves the breakdown. **Publish nothing before that.**

One batch confirmation, not a question per issue. On a twenty-issue decomposition, asking
per slice is twenty interruptions for a low-stakes tag, which is how a useful step becomes one
people skip.

### 6. Publish

Publish the approved slices **in dependency order, blockers first**, so each slice's blocking
edges can reference real issue numbers rather than titles.

Two distinct GitHub relationships, and both are used:

| Relationship | Between | What it gives you |
|---|---|---|
| **Sub-issue** | spec issue -> each slice | The spec renders its own breakdown, so one click shows every part and how many are done |
| **Blocking** | slice -> slice | The frontier: which slices are takeable right now |

Create each slice as a **sub-issue of the spec issue**, then wire blocking edges between
siblings in a second pass, once they have real ids. Where the repo's tracker lacks native
blocking, fall back to the "Blocked by" section of the template.

Report the list, the labels, and the dependency ordering.

Do NOT close or modify the parent spec issue - it is now the parent of all of them.

<issue-template>

## Parent

The spec issue this slice came from. GitHub's sub-issue relationship already records this,
so keep the line short - it exists for the case where the source was not an issue, or where
the tracker has no native hierarchy.

## What to build

The end-to-end behaviour this slice makes work, from the user's perspective, not a
layer-by-layer implementation list.

Avoid specific file paths or code snippets - they go stale fast. Exception: if a prototype
produced a snippet that encodes a decision more precisely than prose can (state machine,
reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to
the decision-rich parts, not a working demo.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- A reference to each blocking issue, or "None - can start immediately".

## Hot files

- The files this slice will most likely own or contend on. Indicative, not a contract -
  it exists so `start-dev` can plan parallel waves by file overlap.

</issue-template>

## The frontier

Once published, the takeable work is the **frontier**: any issue whose blockers are all done.
For a purely linear chain that means top to bottom; where slices are independent it means
several can be worked at once. **start-dev** reads these edges (plus the hot files) to cut
the day into parallel waves, and **pickup-issue** claims one frontier issue per session.

These edges are **issue-level and stay on GitHub**. They describe which issues gate which,
not the ordering of steps inside one issue - that lives in the issue's own plan.

## Related skills

- **to-spec** - the predecessor; supplies the spec being decomposed.
- **start-dev** - downstream; plans the day's waves from the edges and hot files this writes.
- **pickup-issue** - downstream; works one published slice per session.
- **code-review** - files its out-of-scope findings back here as new issues.
