---
name: to-spec
description: Turn the settled design conversation into a durable spec and publish it, then offer a visual overview where the structure is worth seeing.
disable-model-invocation: true
---

# To Spec

## Overview

Takes the design that a **grill-me** session has settled, writes it down as a durable spec, and publishes it. Where the spec's structure is worth seeing, it then offers **visual-spec** for a scannable overview.

It sits after grilling and before **to-issues**, which breaks the spec into work.

## When to use

- The open decisions have been resolved (usually by **grill-me**) and the design needs to become durable.
- A user asks to "turn this into a spec / PRD", "write it up", "make it durable", "publish the spec".

Do NOT use it to explore an undecided design - that is **grill-me**. This skill assumes convergence has already happened.

## Where the spec goes

By default the project tracks issues on **GitHub via the `gh` CLI**. Publish the spec as a new GitHub issue.

**Fallback:** if `gh` is unavailable, or the repo has no GitHub remote, write the spec to `docs/spec/<slug>.md` instead (`<slug>` being a short kebab-case name for the feature). Tell the user where you wrote it.

## Process

1. **Confirm convergence.** Check the decisions are actually settled. If a genuine gap remains - a decision the conversation never reached, not one you would like restated - hand back to **grill-me** rather than papering over gaps in the spec.

2. **Explore the repo** to understand the current state of the codebase, if you haven't already. If the project has a `CONTEXT.md` or other glossary, **use its vocabulary throughout the spec** - the terms were settled during grilling for exactly this reason. Respect any ADRs in the area you're touching.

3. **Sketch the test seams.** Work out the seams at which you'll test the feature. Prefer existing seams to new ones, and use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better; the ideal number is one.

   **Check with the user that these seams match their expectations.**

4. **Write the spec** using the template below, then publish it: `gh issue create` with the spec as the issue body, or the `docs/spec/<slug>.md` fallback.

5. **Offer visual-spec.** On a spec whose structure is worth seeing, chain into **visual-spec** for a scannable overview. Skip it on a small or linear spec; it gates nothing either way.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts: not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>

## Synthesis, not a second interview

Purely **synthesis-first**. A grilling session runs immediately before this, so re-asking what
was just settled is the quickest way to make a skill annoying enough that people route around
it. Read the conversation and write the spec.

The seams check in step 3 is the one deliberate exception, because seams are usually decided
here rather than during grilling.

## Related skills

- **grill-me** - the predecessor stage that resolves decisions before this runs.
- **prototype** - if a prototype produced a decision-encoding snippet, it belongs in Implementation Decisions.
- **visual-spec** - offered at the end when the spec's structure is worth seeing.
- **to-issues** - the successor stage; breaks the published spec into grabbable issues.
