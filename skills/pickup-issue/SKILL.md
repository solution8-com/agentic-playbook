---
name: pickup-issue
description: Pick up one issue in a fresh session - isolate it in a git worktree, open a draft PR, see what the parallel sessions hold, and load only the code the issue touches. Use when starting work on a specific issue, when the user says "pickup issue #N", "grab #N", "let's work on #N", or names an issue to start on, typically one session per tile of the day's battle plan.
---

# Pickup Issue

## Overview

One issue, one session, one worktree. This is the front door of an issue session: it
isolates the work, makes it visible to the other sessions running in parallel, loads the
minimum context, and hands off to planning.

Parallel work runs as **parallel sessions**, each opened with this skill, coordinated
through git - worktrees keep the working copies apart, draft PRs make each session's
claim and progress visible to the rest.

## Process

### 1. Read the issue in full

Title, body, labels, acceptance criteria, blocking relationships, linked spec and ADRs.
If the issue is blocked by an open issue, stop and say so - the battle plan may have
moved. If the issue is too thin to work from, flag it rather than guessing.

### 2. Isolate: worktree + branch

Create a git worktree on a fresh branch (`issue-<n>-<slug>`), off current main. The
worktree is what lets several sessions build simultaneously without touching each other's
files.

### 3. Claim: open a draft PR immediately

Open a **draft PR** from the branch before any work exists - title, issue link
("Closes #N"), one line on intent. The draft is the claim: any session or human looking
at the repo sees who holds what. It is also where CI will report from the first push.

### 4. Look around: read the other draft PRs

List the open draft PRs and read what files each holds. This is how parallel sessions
see each other. If another draft touches the files this issue needs, note the overlap
and the landing order the battle plan intended - and plan to rebase rather than race.

### 5. Load the code the issue touches - and nothing else

Scope from what the issue names (files, functions, symbols, error strings) and walk one
hop out to direct dependencies and callers. **Search as you go; never pre-load the
repo.** On a huge codebase this is the difference between a working session and a
drowned one: a bad search costs one extra tool call, a bad pre-load costs the context
window and cannot be undone.

Signals of over-reading: files the issue never mentions opened "to be safe"; context
filling with modules that cannot be tied back to the task.

### 6. Hand off

- **`hitl` issue** (open decisions expected): into **grill-me**, scoped to this issue,
  then **to-spec**, then **writing-plan**, then the build - **tdd** or
  **subagent-driven-development**, the user's choice.
- **`afk` issue** (small, decision-free): skip the grilling; go straight to a brief
  **to-spec** / **writing-plan** and build.

One issue. Never two.

## Common mistakes

| Mistake | Fix |
|---|---|
| Working on main, or in the main checkout | Worktree + branch first. Isolation is what makes the parallel sessions safe. |
| Deferring the draft PR until there is code | The draft is the claim, not the result. Open it first. |
| Skipping the look at other drafts | That is the coordination mechanism. Racing a file another session holds wastes both. |
| Pre-loading the repo "to understand it" | Scope from the issue; expand on demand. |
| Grilling an afk issue | If there is nothing to decide, there is nothing to grill. Build it. |
| Starting a second issue in the session | One session, one issue, one worktree. |

## Related skills

- **start-dev** - the day plan whose tiles this picks up.
- **grill-me** - next for hitl issues; issue-scoped decisions.
- **to-spec** / **writing-plan** - how the issue gets tackled, then how the code gets written.
- **tdd** / **subagent-driven-development** - the build, either way.
- **close-issue** - the other bookend: merge, tidy, clean up the worktree.
