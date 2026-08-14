# S8 Agentic Playbook

Solution8's curated Claude Code skill set, as a plugin.

Most of these are [Matt Pocock's](https://github.com/mattpocock/skills), vendored with small
tweaks. A handful are ours. We curate rather than author, and
[ATTRIBUTION.md](./ATTRIBUTION.md) says exactly which is which.

**There is no workflow you have to follow.** The Main Flow below is what we usually do, not a
process anyone is signed up to. Skills are tools; reach for the ones that help.

## Install

```
/plugin marketplace add solution8-com/INT-s8-agentic-playbook
/plugin install s8-playbook@solution8
```

## Get Started

- **`setup-dev-repo`** - create a new dev repo or adopt an existing one, then wire the stack, dev
  environment and commit gate, mirror the checks in CI, and prove the gate actually blocks.

## Main Flow

The usual path from an idea to code that landed.

```
grill-me  ->  to-spec  ->  to-issues  ->  pickup-issue  ->  implement
```

- **`grill-me`** - a relentless interview that sharpens a plan until the open decisions are settled.
- **`to-spec`** - turn the conversation into a durable spec.
- **`to-issues`** - break a spec into tracer-bullet vertical slices, published as GitHub issues with
  their blocking edges and an `afk` / `hitl` label.
- **`pickup-issue`** - read one issue and its comments, ask what is unclear, sort out the worktree,
  then hand over. Writes no code.
- **`implement`** - build what was already decided. It never reopens the plan, which is what
  separates it from typing "build this" at a fresh agent.

Review is not a skill here. Claude Code ships `/code-review` - use `/code-review low` for a small
change that matters, the full pass at a checkpoint in a fresh session, and `review-suite` below when
you want a broad quality sweep.

## Shape

For when you do not know enough yet to write a spec.

- **`wayfinder`** - charts a map of the decisions a big piece of work needs, then works one per
  session. Start here on anything that runs for weeks. It subsumes the research and prototyping.
- **`prototype`** - build a throwaway to answer one design question before committing.
- **`research`** - chase a question back to primary sources in a background agent, written up with
  citations.
- **`visual-spec`** - render a spec as a self-contained HTML overview for a human to read.

## Utilities

- **`improve-codebase-architecture`** - find shallow modules worth deepening. Periodic, not per issue.
- **`diagnosing-bugs`** - disciplined root-cause debugging, reproduce first, fix second.
- **`wait-what`** - re-pitch the last message in plain language when it did not land.
- **`ui-report`** - drive Playwright through the flows this session changed, screenshot each state,
  and hand back one self-contained HTML report.
- **`review-suite`** - seven quality passes (dead code, duplication, security, authz, docs drift,
  error handling, over-engineering) run in parallel, merged into one triage board with issue export.

## Misc

Useful, occasional, and nobody has to use them.

- **`wizard`** - generate a script that walks a human through the steps only they can do:
  provisioning, credentials, one-off migrations. Secrets never touch the model.
- **`to-questionnaire`** - turn the questions someone else has to answer into a fillable form.
- **`start`** - pick up where the last session left off.
- **`update-docs`** - save session progress to the ledger and refresh docs the work drifted from.
  Not a dev skill. It is for the projects where you need to remember what you told a client.

## Reports

`ui-report`, `review-suite` and `visual-spec` write self-contained HTML to `.claude/reports/`,
styled with `assets/report.css` so every report looks the same on any machine.
`setup-dev-repo` adds that folder to `.gitignore`.

## Two skills you will not see listed

`tdd` and `grilling` ship in the plugin but are not in the groups above. They exist because
`implement` and `grill-me` call them. You are not meant to invoke them directly.

## License

MIT - see [LICENSE](./LICENSE). Upstream notices are in [ATTRIBUTION.md](./ATTRIBUTION.md).
