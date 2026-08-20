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

While the repo is private, installing needs GitHub auth that can clone it. Two paths:

**With SSH keys set up** (the reliable path - Claude Code clones `owner/repo` over SSH):

```
/plugin marketplace add solution8-com/INT-s8-agentic-playbook
/plugin install s8-playbook@solution8
```

**With HTTPS credentials only** (`gh auth login`), give the full URL instead:

```
/plugin marketplace add https://github.com/solution8-com/INT-s8-agentic-playbook.git
/plugin install s8-playbook@solution8
```

Installing ties you to this repo - no reinstall, no version pinning. To pull the latest skills
after a change is announced:

```
/plugin marketplace update solution8
```

Claude Code's automatic marketplace refresh is not yet reliable for GitHub repos, so run the
update yourself rather than waiting for it.

## Setup

> Standing up a new dev project the rest of this can work in.

- **`setup-dev-repo`** - create a new dev repo or adopt an existing one, then wire the stack, dev
  environment and commit gate, mirror the checks in CI, and prove the gate actually blocks.

## Main Flow

> The usual path to code that landed. You join it wherever your work already is.

```
grill-me  ->  to-spec  ->  to-issues  ->  pickup-issue  ->  implement
```

Nothing written down yet? Start at the left. A spec already written? Start at `to-issues`. An issue
someone else assigned you? Start at `pickup-issue` - and if its decisions were never settled,
`pickup-issue` sends you back to `grill-me` before anything gets built. Nobody picks a flow; the
work already says where you are.

- **`grill-me`** - a relentless interview that sharpens a plan until the open decisions are settled -
  it gets you and your coding agent on the same page about exactly what you want built, before
  anything is built.
- **`to-spec`** - turn the conversation into a durable spec.
- **`to-issues`** - break a spec into tracer-bullet vertical slices, published as GitHub issues with
  their blocking edges and an `afk` (safe to run unattended) / `hitl` (human in the loop - the
  default) label.
- **`pickup-issue`** - read one issue and its comments, check its claims against the live tree,
  sort out the worktree, then work out whether the issue is settled enough to build or needs a
  grill first. Writes no code and no plan of its own.
- **`implement`** - build what was already decided. It never reopens the plan, which is what
  separates it from typing "build this" at a fresh agent.

Review is not a skill here. Claude Code ships `/code-review` - use `/code-review low` for a small
change that matters, and at the end of a work session run the full pass over the diff in a fresh
session. `review-suite` below is for a broad quality sweep.

`verify-feature` is not a step either. `implement` stops at a commit with `/code-review low`
already run; whether the behaviour also needs *proving* is a judgement about the change, not a
stage in the flow. Run it when a human has to trust the result - client-facing work, anything with
a UI, a change nobody is going to read the diff of. Skip it where the tests already carry the
proof.

## Shape

> For when you do not know enough yet to write a spec.

- **`wayfinder`** - charts a map of the decisions a big piece of work needs, then works one per
  session. Start here on anything that runs for weeks. It subsumes the research and prototyping.
- **`prototype`** - build a throwaway to answer one design question before committing.
- **`research`** - chase a question back to primary sources in a background agent, written up with
  citations.
- **`visual-spec`** - render a spec as a self-contained HTML overview for a human to read.

`design` is not a skill here either - Claude Code ships it. It opens an editable canvas you move
things around on directly, and because it runs inside the repo the layout arrives with the code it
has to sit on, instead of a screenshot you then have to explain. Reach for it when a lot is still
undefined. `prototype` stays the better tool once the direction is settled and you want two or
three variants built to compare.

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

- **`guide`** - not sure which skill fits? Routes your situation to the right one, or gives a
  tour of how the playbook hangs together. Checks `gh auth status` first, since much of the
  flow runs through GitHub.
- **`wizard`** - generate a script that walks a human through the steps only they can do:
  provisioning, credentials, one-off migrations. Secrets never touch the model.
- **`to-questionnaire`** - turn the questions someone else has to answer into a fillable form.
- **`handoff`** - compact the session into a handoff a fresh one can pick up from, written to a
  temp file rather than into the repo. The tracker and the git history are the project's memory;
  this covers only what they do not hold.
  Works in any repo, dev included; it earns its keep on long-running projects where you need to
  remember what was agreed and where you left off.

## Reports

> Every report looks the same on any machine.

`verify-feature`, `review-suite`, `visual-spec` and `improve-codebase-architecture` write
self-contained HTML to `.claude/reports/`, styled with `assets/report.css`. `setup-dev-repo` adds
that folder to `.gitignore`.

## Modules

> The teaching layer: the principles behind the skills, one lesson doc per concept.

Ten lesson docs in [`modules/`](./modules), ordered the way the agentic loop runs - context,
action, verification - then the operating topics. Each teaches one concept in plain words:
why it matters, and what you can do about it. Fresh drafts, review in progress.
[SOURCES.md](./modules/SOURCES.md) collects the reading behind all of them.

1. [The agentic loop](./modules/m0-the-agentic-loop.md) - what an agentic tool actually does, and why you are part of the loop.
2. [The context window](./modules/m1-the-context-window.md) - the agent's working memory is a budget; sessions get worse before they get full.
3. [What the agent reads](./modules/m2-what-the-agent-reads.md) - instruction files, the codebase itself, and checks that enforce instead of hope.
4. [Deciding before building](./modules/m3-deciding-before-building.md) - shared vision beats clever wording; agree what done looks like first.
5. [Handing work off](./modules/m4-handing-work-off.md) - delegation, scouts, and briefs that stand alone.
6. [Verifying agent work](./modules/m5-verifying-agent-work.md) - the three gates between "done" and done.
7. [Working unattended](./modules/m6-working-unattended.md) - containment beats supervision; when work can run alone.
8. [Teams](./modules/m7-teams.md) - a shared setup beats everyone improvising.
9. [Measuring](./modules/m8-measuring.md) - feelings aren't data; check numbers before adopting them.
10. [When rules expire](./modules/m9-when-rules-expire.md) - the expiry test: rules die a layer at a time.

## Tools

> What to install alongside the skills.

[tools/](./tools/README.md) covers the MCPs, CLIs and plugins worth having - including the three
things the skills actually need (`gh`, Playwright MCP, Python 3) and which MCPs are worth keeping
switched off until you need them.

| Tool | Kind | What it's for |
|---|---|---|
| [Context7](./tools/README.md#context7) | MCP | Current library documentation |
| [Playwright](./tools/README.md#playwright) | MCP | A real browser to drive |
| [Supabase](./tools/README.md#supabase) | MCP | Your database, queryable |
| [n8n](./tools/README.md#n8n) | MCP | Automations, and their failures |
| [Vercel](./tools/README.md#vercel) | MCP | Deploys, build logs, preview URLs |
| [Miro](./tools/README.md#miro) | MCP | Boards read and written in place |
| [GitHub](./tools/README.md#github-gh) | CLI | Issues, PRs and CI from the terminal |
| [Azure](./tools/README.md#azure-az) | CLI | Azure resources and deployments |
| [Postgres](./tools/README.md#postgres-psql) | CLI | Direct database queries |
| [context-mode](./tools/README.md#context-mode) | Plugin + MCP | Big output kept out of the conversation |
| [Caveman](./tools/README.md#caveman) | Plugin | Shorter replies |
| [Language servers](./tools/README.md#language-servers) | Plugin | Real types instead of grep |

## License

MIT - see [LICENSE](./LICENSE). Upstream notices are in [ATTRIBUTION.md](./ATTRIBUTION.md).
