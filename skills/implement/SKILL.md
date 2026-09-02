---
name: implement
description: "Implement a piece of work based on a spec or set of tickets. Use when work arrives from /pickup-issue, or when the user asks to implement or build something already specced in a ticket."
---

# Implement

A build runs tests, typechecks and reads their output over and over. That is hundreds of tool
results this session never needs. **Dispatch the build to a subagent, then audit its receipt.**
The build procedure lives in [`references/procedure.md`](references/procedure.md), for the
subagent to read.

**Already a subagent?** Read `references/procedure.md` and build it yourself.

Two steps stay here, because the subagent cannot do them: the review, and the audit.

## 1. Brief

The subagent cannot read this conversation, so the brief is the plan. Dispatch one
`general-purpose` agent. Its prompt carries:

1. Read `<absolute path to this skill>/references/procedure.md` first, and follow it.
2. **The plan in full**, written out rather than referenced: the ticket, the spec, or what this
   conversation agreed. Include the decisions already settled and the alternatives already
   rejected, so the subagent builds them rather than reopening them.
3. What `pickup-issue` confirmed and contradicted against the live tree, with the `file:line`
   for each.
4. Repo root, current branch, the worktree path where the work lives, and the trunk.
5. The gate command, when this session already knows it.
6. The project memory directory.
7. Any scope the user set: files to leave alone, surfaces to skip.

## 2. Relay the review

The subagent commits, reports the SHA and the seams it tested, and stops.

Run `/code-review low` and name the target explicitly: the branch or worktree path where the
work lives. Review subagents inherit the session's working directory, not the builder's
worktree, so an untargeted review can pass without ever seeing the diff. A review that saw no
diff is not a review.

Do not run a deep review here. An agent reviewing code it just wrote is biased toward its own
solution, so the deep pass belongs in a fresh session against a fixed point.

Relay the findings with `SendMessage`. The subagent's context is intact, so it fixes them in
place, re-runs the gate, runs the verification, and returns its receipt.

## 3. Audit the receipt

Audit it against evidence outside the subagent's own words. **Done when every receipt claim is
either confirmed or named as unverified in your report.**

- `git log --oneline <trunk>..HEAD` matches the commits it claims.
- `git diff --stat <trunk>..HEAD` stayed inside the plan's boundary. A file well outside it is a
  finding for the user.
- `git status --short` shows a clean tree.
- Re-run the gate yourself and confirm exit 0.
- The new tests exist and cover the seams the subagent named before it started.
- Where the diff touched UI, an endpoint or the database, the `verify-feature` report exists at
  the path the receipt names. Do not read the report, it embeds screenshots. Audit from the receipt.

Correct the subagent with `SendMessage` rather than starting a second run.

## 4. Report

The branch first, then the commits, the gate command and its exit code, what the review fixed,
and the `verify-feature` report path where there is one. Then anything your audit contradicted,
and anything the subagent left out.

Then stop: hand the branch to the user to review and merge. Do not merge it yourself unless the
user has said to for this work. An issue labelled `afk` counts as that permission.
