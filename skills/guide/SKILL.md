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

Match the situation to the skill, with one line on why:

| Situation | Skill |
|---|---|
| An idea, still fuzzy, decisions unsettled | `grill-me` |
| Work too big to hold in one head | `wayfinder` |
| "Would this design even feel right?" | `prototype` |
| A question needing sources, not opinions | `research` |
| Decisions settled, nothing written down | `to-spec` |
| A spec that needs to become tickets | `to-issues` |
| A ticket ready to build | `pickup-issue` (hands to `implement`) |
| Something broken, failing, or slow | `diagnosing-bugs` |
| "Prove this feature actually works" | `verify-feature` |
| A branch or codebase to sweep for quality | `review-suite` |
| A new repo to stand up | `setup-dev-repo` |
| Steps only a human can do (credentials, dashboards) | `wizard` |
| Session starting | `start` |
| Session ending, or a milestone landed | `update-docs` |

If nothing fits, say so plainly - most work needs no skill at all.

## Tour

If they want the overview instead: show the Main Flow in one line (`grill-me` -> `to-spec`
-> `to-issues` -> `pickup-issue` -> `implement` -> a human reviews and merges), then the
README's groups - Setup, Main Flow, Shape, Utilities, Misc - one sentence each, and point at
`tools/README.md` for the recommended tools. Close by offering to route whatever they are actually
working on right now.
