---
name: guide
description: Route to the right skill for the situation, or give a tour of the playbook. Use when someone is unsure which skill fits ("what do I use for..."), asks how the playbook fits together, or is new to the plugin.
---

# Guide

Orient someone in the playbook: route them to the right skill for their situation, or walk
them through how the pieces fit. Suggest, never push - the Main Flow is what we usually do,
not a process anyone must follow.

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

## Tour

If they want the overview instead: show the Main Flow in one line (`grill-me` -> `to-spec`
-> `to-issues` -> `pickup-issue` -> `implement` -> a human reviews and merges), say you join it
wherever the work already is, then the
README's groups - Setup, Main Flow, Shape, Utilities, Misc - one sentence each, and point at
`tools/README.md` for the recommended tools. Close by offering to route whatever they are actually
working on right now.
