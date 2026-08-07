---
name: close-issue
description: Land a finished issue - wait for the checks, merge the PR, delete the branch, and clean up the worktree. Use when an issue's build is done and committed, when the user says "close the issue", "land it", "merge it", or as the final stage of an issue session.
---

# Close Issue

## Overview

The end of an issue session. The work is built and pushed on the issue's branch, the
draft PR exists since pickup; this skill flips it to ready, waits for green, lands it,
and leaves the repo tidy.

**It merges on green.** The whole path is automatic. Nothing here is
a judgement that the agent's code is trustworthy; it is a bet on the checks. **CI is the
gate - the last thing between the change and trunk - so if a project's checks are weak,
this merges weak work.** Say so rather than merging quietly, and see "When not to merge".

Docs are not updated here. Doc updates happen at the **day level** - parallel issue
sessions writing the same ledger file produce conflicts, so **update-docs** runs once,
from the orchestrator session, at the end of the day. The PR body is this issue's durable
record.

## Process

1. **Confirm the build is done.** The work is committed and pushed, the acceptance
   criteria from the issue have been run and pass, and any code-review findings on this
   PR are resolved - applied or dismissed with a reason. Do not proceed on a red suite or
   an unfinished slice.
2. **Finalize the PR.** Mark the draft ready for review. Make the body current: what
   changed, why, what was verified. If **code-review** ran on this PR, carry its diff
   annotations into the body - the non-obvious decisions and why. Link the issue with
   "Closes #N".
3. **Wait for the checks.** CI plus any acceptance commands. Report what they said.
4. **Merge**, once everything is green. Merging closes the PR and the linked issue. If
   anything is red, stop and report.
5. **Tidy.** Delete the branch, remove the worktree. Leave nothing behind but the merged
   PR and the closed issue.
6. **Report done.** What landed, where the PR is, what the checks returned.

## What green means

Green is what lands the work, so it has to mean something:

- The project's own check command passes (build, lint, types, tests).
- The issue's acceptance criteria are satisfied, verified by **running** them rather than
  by reading the code and concluding they hold.
- CI is green on the PR - the one check that cannot be bypassed locally.

One thing green does **not** cover: problems that only show up across several issues.
`improve-codebase-architecture` looks for those, periodically rather than per issue.

## When not to merge

Merge on green assumes there is a real gate. Stop and hand back when there is not:

| Situation | Why it blocks |
|---|---|
| The project has no meaningful checks | Nothing was verified. Merging is a coin flip with extra steps. |
| The issue had no acceptance criteria | Nothing defined "done", so green only means "did not crash". |
| CI is not configured, or runs nothing | CI is the last thing between the change and trunk. |
| The change touches auth, secrets, payments, migrations or deletes data | Reversibility is the point. These earn a human even when green. |

Say which one applies and leave the PR open. Do not merge and mention it afterwards.

## Common mistakes

| Mistake | Fix |
|---|---|
| Disabling or weakening a check to get green | That is not passing, it is removing the thing that would have told you. Doubly bad when green merges. |
| Merging when the checks are meaningless | Green against no tests is not green. See "When not to merge". |
| Closing on a red suite | A red check stops everything. |
| Updating the ledger from an issue session | Docs are day-level. Parallel sessions writing one ledger file conflict. |
| Leaving the worktree or branch behind | Tidy is part of closing. Stale worktrees confuse the next pickup. |
| Skipping the PR body because it merges anyway | The PR is the issue's durable record, and where CI reports. Make it current. |

## Related skills

- **pickup-issue** - the other bookend; created the worktree and draft PR this closes.
- **code-review** - optional before this, on the PR; its annotations go in the PR body.
- **update-docs** - runs at day level, from the orchestrator session, not here.
- **improve-codebase-architecture** - the periodic pass for cross-issue problems.
