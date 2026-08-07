# S8 Agentic Playbook - Skills

This directory is S8's agentic-coding playbook skill set: the curated collection of
Claude Code skills that encode how S8 plans, builds, verifies, and ships software with
agents. Each skill is one `SKILL.md` (plus any bundled resources) covering a single
stage or utility in the workflow.

**Scope: Claude Code in the terminal.** These 25 skills are how S8 works today, on a
laptop, in a shell - parallel work runs as parallel *sessions*, coordinated through git
(worktrees and draft PRs), not through an orchestrator product. `CATALOG.md` holds the
full research and source-mapping; this README is the working index.

> **Helm is parked.** The playbook was previously written partly against Helm, S8's
> agent cockpit, which is still half built. That content lives in `docs/helm-parked.md`
> and comes back after the Kasper / Emil / Martin sync. The current Build-lane shape
> (day plan, waves, one session per issue) is deliberately easy to link to Helm later.
> The external/public build comes after the modules.

The skills span three lanes plus utilities:

- **Project Start** - run once per project, to go from an idea to grabbable issues.
- **Build** - issue-driven work on bigger repos: a day-level plan, then one session per issue.
- **Simplified** - smaller work, ad hoc work with no issues filed, and less-technical teammates.

## How a project actually starts

**The differentiator is project size.**

**Bigger projects start at `wayfinder`** - a new product, a client engagement, a
substantial build, anything running for weeks across many sessions. At that size you do
not know what you do not know yet, so you chart a map of the decisions rather than
guessing at a plan.

Crucially, **wayfinder subsumes the research and the prototyping.** Its ticket types are
`research`, `prototype`, `grilling` and `task`, so walking the map is *how* those happen,
in the order the fog actually demands.

**Smaller projects start at `grill-me`** - an automation, a script, a small tool, a bug
fix. There a map costs more than the fog it clears.

## How a working day runs (the Build lane)

```
DAY   (one orchestrator session)
  start-dev -> scope the day -> read the board -> plan WAVES -> battle-plan HTML -> human review
  ... issue sessions run ...
  update-docs at day end (recommended, not required)

ISSUE (one fresh session per issue - never agents inside a session)
  pickup-issue #N -> worktree + draft PR + read other drafts + load only the issue's code
    -> grill-me (hitl issues) -> to-spec -> writing-plan
    -> tdd  OR  subagent-driven-development
    -> commit -> CI green -> close-issue (merge, delete branch, clean worktree)

REVIEW (optional, two modes)
  A: fresh session on one PR before it lands (recommended for bigger issues)
  B: fresh session on the day's diff at day end
  In-scope mechanical findings are fixed; out-of-scope findings become new issues.
```

A **wave** is a set of issues touching different hot files, so their sessions run in
parallel without conflicts. A wave is finished when its tiles are **merged**, not built.

This lane is for issue-driven work on bigger repos. Smaller things take the Simplified
lane, or a bare grill-me -> to-spec -> writing-plan run for work that never gets filed as
an issue.

## Session bookends: two parallel pairs

- **pickup-issue / close-issue** bookend *issue sessions*: claim and isolate one issue,
  then land and tidy it.
- **start / update-docs** bookend *everyday sessions* and the day-level loop: pick up
  where you left off, then save session state to the ledger. Issue sessions do not
  update docs - the day does, once, to keep parallel sessions from fighting over the
  ledger.

## Skill index (by lane)

### Project Start (run once per project, the planning arc)

`grill-me`, `to-spec` and `writing-plan` run again at ISSUE level in the Build lane -
nested scope, same tools at two altitudes. `wayfinder` does not: it stays at project level.

- **setup-skills** - *(global)* Install the playbook skills into a repo, then check git and gh are ready.
- **setup-dev-repo** - Create a new dev repo or adopt an existing one, then wire the stack, dev env and commit gate.
- **wayfinder** - **Bigger projects start here.** Two modes: one session charts the map, then a new session per ticket works it. Never more than one ticket per session.
- **research** - Chase a question back to primary sources in a background agent, and write up the findings with citations. A wayfinder ticket type, and usable on its own.
- **prototype** - Build a throwaway prototype to answer one design question before committing. Also a wayfinder ticket type.
- **grill-me** - Relentless interview, asked in rounds along the question frontier, to settle the open decisions. The way in on small work; a ticket type inside a map.
- **to-spec** - Turn the design conversation, or a resolved map, into a durable spec and publish it.
- **visual-spec** - Produce a self-contained HTML overview of a spec for human review. Optional.
- **to-issues** - Break a plan/spec/PRD into tracer-bullet vertical slices, published as sub-issues of the spec with blocking edges and hot files, labelled by type / severity / autonomy (hitl by default when more grilling is plausible). On an existing board, re-wires the existing issues' dependencies too.

### Build (day level, then one session per issue)

- **start-dev** - The day orchestrator. Scopes the day, reads dependencies / hot files / sizes, plans waves of parallel issues, and emits a battle-plan HTML for human review.
- **pickup-issue** - One issue, one fresh session: worktree + draft PR, read the other drafts, load only the code the issue touches, then hand to grill-me (hitl) or straight to the build (afk).
- **grill-me / to-spec / writing-plan** - The same planning trio, scoped to the one issue.
- **tdd** - Test-driven red-green-refactor loop, one vertical slice at a time.
- **subagent-driven-development** - The other build method: dispatch a fresh subagent per plan task, with a review after each and a broad final review.
- **code-review** - Optional, two modes: on one PR before it lands, or on the day's diff at day end. Annotates first, parallel Standards + Spec passes, drives the browser if UI changed. Auto-applies mechanical in-scope fixes; out-of-scope findings become new issues.
- **close-issue** - Wait for CI green, merge, delete the branch, clean up the worktree. Docs move to day level.

### Simplified (smaller work, ad hoc work, less-technical teammates)

- **start** - Continue from where you left off by reading project state.
- **grill-me** - The interview; records what gets settled in the ledger, and an ADR when the decision passes the three locks.
- **to-spec** - Make the settled design durable before building.
- **writing-plan** - Turn the spec into a bite-sized, file-exact implementation plan.
- **tdd / subagent-driven-development** - The build, either method.
- **code-review** - If needed.
- **update-docs** - Save session progress to `ledger.md`, refresh any project docs the work drifted from, and create a handoff doc.

### Mid-work utilities (usable from inside any lane)

- **research** - Investigate a question against high-trust primary sources; capture one cited findings file.
- **systematic-debugging** - Disciplined root-cause debugging with a feedback loop before any fix (alias: diagnosing-bugs).
- **improve-codebase-architecture** - Find deepening opportunities; refactor shallow modules into deep ones. Periodic: at the end of a session once in a while, at a milestone, or on a smell. It is the counterpart to per-PR review, catching the duplication and drift a single-diff reviewer cannot see. Local refactor stays in tdd's refactor step.
- **wizard** - Generate an interactive bash script that walks a human through the steps only they can perform: provisioning, credentials, one-off migrations. The agent writes it; the human runs it, so secrets never touch the model.
- **to-questionnaire** - Turn the questions someone else must answer into a fillable S8-styled HTML questionnaire with exportable answers. The stakeholder loop out of a grilling session.
- **explain-like-im-ten** - Re-explain what was just said in plain language when a message didn't land.
- **update-skills** - Pull the newest skills into a repo, showing what changed first.

### Meta

- **writing-for-agents** - The reference every skill here is written against, and for any other document an agent reads: CLAUDE.md, specs, docs behind pointers. Fires on its own when agent config is being edited.

## Sourcing

Which upstream each skill came from lives in `CATALOG.md` only - skill files carry no
upstream names.

Deliberately absent: `assign-issues` (multi-person orchestration, parked pending the team
sync), `verify-task-done` (CI and the issue's acceptance criteria are the gate),
`executing-plans` (superseded by `subagent-driven-development`).
