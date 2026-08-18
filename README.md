# S8 Agentic Playbook

> Solution8's curated Claude Code skill set, as a plugin.

Most of these are [Matt Pocock's](https://github.com/mattpocock/skills), vendored with small
tweaks. A handful are ours. We curate rather than author, and
[ATTRIBUTION.md](./ATTRIBUTION.md) says exactly which is which.

**There is no workflow you have to follow.** The Main Flow below is what we usually do, not a
process anyone is signed up to. Skills are tools; reach for the ones that help.

| Group | Skills | What it's for |
|---|---|---|
| [Setup](#setup) | 1 | Standing up a new dev project the rest of this can work in |
| [Main Flow](#main-flow) | 5 | Idea to code that landed |
| [Shape](#shape) | 4 | Working out what to build, before there is a spec to write |
| [Utilities](#utilities) | 6 | Reached for mid-work, in whatever order the work demands |
| [Misc](#misc) | 4 | Occasional, and nobody has to use them |

## Install

```
/plugin marketplace add solution8-com/INT-s8-agentic-playbook
/plugin install s8-playbook@solution8
```

Installing the plugin subscribes you to updates - when a skill changes here, every install picks it
up automatically. No reinstall, no version pinning.

## Setup

> Standing up a new dev project the rest of this can work in.

- **`setup-dev-repo`** - create a new dev repo or adopt an existing one, then wire the stack, dev
  environment and commit gate, mirror the checks in CI, and prove the gate actually blocks.

## Main Flow

> The usual path from an idea to code that landed.

```
grill-me  ->  to-spec  ->  to-issues  ->  pickup-issue  ->  implement
```

- **`grill-me`** - a relentless interview that sharpens a plan until the open decisions are settled -
  it gets you and your coding agent on the same page about exactly what you want built, before
  anything is built.
- **`to-spec`** - turn the conversation into a durable spec.
- **`to-issues`** - break a spec into tracer-bullet vertical slices, published as GitHub issues with
  their blocking edges and an `afk` (safe to run unattended) / `hitl` (human in the loop - the
  default) label.
- **`pickup-issue`** - read one issue and its comments, ask what is unclear, sort out the worktree,
  then hand over. Writes no code and no plan - the issue already is the plan.
- **`implement`** - build what was already decided. It never reopens the plan, which is what
  separates it from typing "build this" at a fresh agent.

Review is not a skill here. Claude Code ships `/code-review` - use `/code-review low` for a small
change that matters, and at the end of a work session run the full pass over the diff in a fresh
session. `review-suite` below is for a broad quality sweep.

## Shape

> For when you do not know enough yet to write a spec.

- **`wayfinder`** - charts a map of the decisions a big piece of work needs, then works one per
  session. Start here on anything that runs for weeks. It subsumes the research and prototyping.
- **`prototype`** - build a throwaway to answer one design question before committing.
- **`research`** - chase a question back to primary sources in a background agent, written up with
  citations.
- **`visual-spec`** - render a spec as a self-contained HTML overview for a human to read.

## Utilities

> Reached for mid-work, in whatever order the work demands.

- **`improve-codebase-architecture`** - find shallow modules worth deepening. Periodic, not per issue.
- **`diagnosing-bugs`** - disciplined root-cause debugging, reproduce first, fix second.
- **`wait-what`** - re-pitch the last message in plain language when it did not land.
- **`verify-feature`** - drive the real app through the diff: UI flows, endpoints, database and
  behavioral side effects, handed back as one self-contained HTML report with screenshots. Run it
  when you finish implementing a feature.
- **`review-suite`** - seven quality passes (dead code, duplication, security, authz, docs drift,
  error handling, over-engineering) run in parallel, merged into one triage board with issue export.
  Run it when a big feature or branch wraps up.

- **`tdd`** - the red-green loop, and what makes a test worth keeping. `implement` calls it at
  pre-agreed seams; you can also invoke it yourself.

## Misc

> Occasional, and nobody has to use them.

- **`wizard`** - generate a script that walks a human through the steps only they can do:
  provisioning, credentials, one-off migrations. Secrets never touch the model.
- **`to-questionnaire`** - turn the questions someone else has to answer into a fillable form.
- **`start`** - pick up where the last session left off.
- **`update-docs`** - save session progress to the ledger and refresh docs the work drifted from.
  Works in any repo, dev included; it earns its keep on long-running projects where you need to
  remember what was agreed and where you left off.

## Reports

> Every report looks the same on any machine.

`verify-feature`, `review-suite` and `visual-spec` write self-contained HTML to `.claude/reports/`,
styled with `assets/report.css`. `setup-dev-repo` adds that folder to `.gitignore`.

## Tools

> What to install alongside the skills.

[TOOLS.md](./TOOLS.md) covers the MCPs, CLIs and plugins worth having - including the three things
the skills actually need (`gh`, Playwright MCP, Python 3) and which MCPs are worth keeping
switched off until you need them.

| Tool | Kind | What it's for |
|---|---|---|
| [Context7](./TOOLS.md#context7) | MCP | Current library documentation |
| [Playwright](./TOOLS.md#playwright) | MCP | A real browser to drive |
| [Supabase](./TOOLS.md#supabase) | MCP | Your database, queryable |
| [n8n](./TOOLS.md#n8n) | MCP | Automations, and their failures |
| [Vercel](./TOOLS.md#vercel) | MCP | Deploys, build logs, preview URLs |
| [Miro](./TOOLS.md#miro) | MCP | Boards read and written in place |
| [GitHub](./TOOLS.md#github-gh) | CLI | Issues, PRs and CI from the terminal |
| [Azure](./TOOLS.md#azure-az) | CLI | Azure resources and deployments |
| [Postgres](./TOOLS.md#postgres-psql) | CLI | Direct database queries |
| [context-mode](./TOOLS.md#context-mode) | Plugin + MCP | Big output kept out of the conversation |
| [Caveman](./TOOLS.md#caveman) | Plugin | Shorter replies |
| [Language servers](./TOOLS.md#language-servers) | Plugin | Real types instead of grep |

## License

MIT - see [LICENSE](./LICENSE). Upstream notices are in [ATTRIBUTION.md](./ATTRIBUTION.md).
