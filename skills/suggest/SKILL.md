---
name: suggest
description: Point someone at the skill that fits what they are doing. Use when they are unsure what to reach for ("what do I use for...", "is there a skill for this"), or describe a piece of work without naming a skill.
---

# Suggest

Work out what someone is doing and name the skill that fits, with one line on why. Suggest, never
push - the Main Flow is what we usually do, not a process anyone must follow, and most work needs
no skill at all.

Orientation is not this skill's job. Someone new to the playbook wants `onboarding`, which runs
once and sets them up against what they already have.

## Preflight

Run `gh auth status` once, quietly. Much of the flow (issues, branches, PRs) runs through
the `gh` CLI; if it is not authenticated, say so and point at `gh auth login` before routing
anywhere that needs it.

## Route

For build work, work out **where their work already is - never ask**. The Main Flow is one chain,
joined at whichever point matches what exists:

```
grill-me  ->  to-spec  ->  to-issues  ->  pickup-issue  ->  implement
```

Nothing written down means the whole chain. A spec already written starts at `to-issues`. A named
issue, a URL, or "pick up #12" starts at `pickup-issue` - and if its decisions were never settled,
`pickup-issue` hands back to `grill-me` before anything gets built. The signal is in what they
said, so read it and route.

Then match the situation to the skill, with one line on why:

| Situation | Skill |
|---|---|
| An idea, still fuzzy, decisions unsettled | `grill-me` |
| Work too big to hold in one head | `wayfinder` |
| "Would this design even feel right?" | `prototype` |
| A screen or layout with a lot still undefined | `design` - Claude Code ships it, not us |
| A question needing sources, not opinions | `research` |
| Decisions settled, nothing written down | `to-spec` |
| A spec that needs to become tickets | `to-issues` |
| A ticket ready to build | `pickup-issue` (hands to `grill-me` or `implement`) |
| Something broken, failing, or slow | `diagnosing-bugs` |
| "Prove this feature actually works" | `verify-feature` |
| A branch or codebase to sweep for quality | `review-suite` |
| A repo to stand up, with or without code | `setup-repo` |
| Steps only a human can do (credentials, dashboards) | `wizard` |
| Session ending with decisions that live nowhere else | `handoff` |

If nothing fits, say so plainly - most work needs no skill at all.

## The two questions that come after the build

Neither is a step in the flow, and saying so is part of the job:

- **Review.** `implement` already runs `/code-review low` over its own diff. A full `/code-review`
  in a fresh session is worth it at the end of a work session, and `review-suite` is for sweeping
  a whole branch or codebase.
- **`verify-feature`.** Worth a run when a human has to trust the result - client-facing work,
  anything with a UI, a change nobody is going to read the diff of. Where the tests already carry
  the proof, skip it. Never advise it as a routine gate after every slice.
