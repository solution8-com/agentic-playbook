---
name: start-dev
description: Plan the working day - cut the open issues into parallel waves and render a reviewable battle-plan HTML.
disable-model-invocation: true
---

# Start Dev

## Overview

The day-level orchestrator. It answers one question: **given the open issues, what is the
best plan for today?** The output is a battle plan - waves of issues that can run in
parallel - rendered as a self-contained HTML file the user reviews and pushes back on
before anything starts.

This skill plans; it does not build. Each tile in the plan is picked up later in its own
fresh session via **pickup-issue**. Run this in a session of its own, and prefer the most
capable planning model available for it - the whole day rides on this reasoning.

This is for issue-driven work on bigger repos. Smaller work, or work with no issues filed,
skips the ceremony: the Simplified flow (grill-me, to-spec, writing-plan, build) covers it.

## Process

### 1. Scope the day

Ask, briefly:

- **Mode.** Clear as many issues as possible (the usual case), or push one urgent issue
  through? Everything below assumes the first; the second needs no battle plan.
- **Time.** An hour, a half day, a full day, something running in the background? This
  sets how many waves are realistic, not which issues exist.

Skip anything the user already said.

### 2. Read the board

- `gh issue list` - open issues with labels (`type`, `severity`, `afk`/`hitl`) and
  blocking relationships (written by **to-issues**).
- **Which files does each issue touch?** From the issue bodies and linked specs. This is
  the load-bearing read: parallelism is decided by file overlap, not by topic.
- Size each issue: **S / M / L / XL**, judged from the issue body against the codebase.

### 3. Find the hot files, then cut the waves

- **Hot files force order.** When several issues touch the same file, they serialize into
  a **spine**: an ordered chain through that file, foundations first. Everything else is
  parallel by default. Name each spine and the order explicitly - this is the part the
  human most needs to sanity-check.
- **A wave is a set of issues that touch different hot files**, so one agent per issue can
  run simultaneously without stepping on the others. Order waves so each lands the pieces
  the next one needs.
- **Finish a wave before starting the next** - merged, not just built.
- Write **coordination notes** per wave where they earn their place: which issue owns a
  shared file, which files are append-only ("rebase before merge, conflicts are only on
  trailing lines"), what rebases on what.

### 4. Emit the battle plan

Render the plan as one self-contained HTML file, following [TEMPLATE.html](TEMPLATE.html)
- the structure is the contract, the content in it is example only:

- **Stats row**: open issues, open PRs, waves to full clear, agents in wave 1.
- **The spines**: each hot file with its ordered issue chain and one line on why.
- **The waves**: per wave a title, agent count, a one-line intent, and a tile per issue -
  number, effort tag, title, one-liner, files touched (owner marked), and status:
  agent-ready (`afk`), needs-input-first (`hitl`), or hold.
- **Coordination notes** where a wave needs them.

Then **stop and hand it to the user.** The plan is a proposal: the dependency claims and
wave cuts are exactly where a human spots what the issue bodies did not say. Revise on
pushback.

### 5. Point at execution

Once the plan stands: each tile is picked up with **pickup-issue** in a fresh session -
`hitl` tiles when the user is around to be grilled, `afk` tiles any time. The day ends
back in this session with **update-docs** - recommended, not required.

## Common mistakes

| Mistake | Fix |
|---|---|
| Planning waves by topic instead of file overlap | Two issues on the same file serialize, whatever their topics. Two issues on different files parallelize, however related they sound. |
| Starting wave 2 while wave 1 has unmerged PRs | A wave is done when it is merged. Unmerged work is a rebase bomb for the next wave. |
| Building anything from this session | This skill plans. Tiles are picked up in fresh sessions via pickup-issue. |
| Presenting the plan as final | It is a proposal. The human review of dependencies and wave cuts is the point of the HTML. |
| Sizing from issue titles | Read the bodies against the code. A one-line title can hide an XL. |

## Related skills

- **pickup-issue** - executes one tile of the plan in a fresh session.
- **to-issues** - wrote the issues and blocking edges this reads.
- **close-issue** - lands each tile; a wave is done when its tiles are merged.
- **update-docs** - closes the day from this session. Recommended, not required.
