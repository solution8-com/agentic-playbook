---
name: pickup-issue
description: Load one issue's context and set up its workspace, then hand to /implement. Use when the user names an issue to work on ("pick up #12", "let's do issue 40", "start on the auth one"), or points at an issue URL and wants work to begin.
---

# Pick up an issue

Get the context and the workspace right, then hand over. **This skill does not write code.**

## 1. Read the issue

```
gh issue view <N> --comments
```

Read the body **and the comments**. Decisions get made in comment threads and never make it back into the body, so a body-only read will build the wrong thing confidently.

If the issue references a parent, a spec, or a blocking issue, read those too.

Then **check the issue's claims against the live tree**. An issue is a hypothesis, including last
week's: the paths, counts and code references it states go stale between writing and pickup. Worse,
an issue drafted by an agent without repo access mixes verified fact and confident guess in prose
that reads identically - the verified parts check out, so the guessed parts get trusted too.

Resolve every claim to one of three states, and never quietly promote one:

- **Confirmed** - with the `file:line` that shows it.
- **Contradicted** - with the `file:line` of what is actually there instead.
- **Unknown** - with the search terms you tried. An unknown left standing as an unknown is a good
  outcome. An unknown rounded up to confirmed is how the wrong thing gets built.

**Claims of absence are the hardest and the most often wrong** - "there is no X", "nothing handles
Y". Confirming absence takes positive search evidence, so record what you searched rather than only
that you found nothing.

Then trace each contradiction forward. A wrong claim rarely stays local: name the acceptance
criteria, scope statements and design decisions that rested on it. Surface all of it and let the
user rule before any code gets written - do not build on a stale premise.

## 2. Decide whether it is settled enough to build

An issue from `/to-issues` arrives with its decisions already made. An issue written by someone
else - a designer, a client, a colleague in a hurry - often does not. Telling those two apart is
this step's whole job.

Read for **open decisions**, not for detail: are what to build, what done means, and where the
scope stops actually settled?

- **Settled** - say so in one line and hand to `/implement`. No ceremony.
- **Not settled** - name the open decisions and hand to `/grill-me` first, then `/implement`.

Do not settle them yourself. An issue with open decisions is a plan nobody finished, and finishing
it silently is how you build the wrong thing confidently.

Either way, do not re-open decisions the issue records as **made**. Disagreeing with a settled
decision is a conversation with whoever settled it, not a thing to quietly revise here.

## 3. Resolve the workspace

Worktrees are what stop parallel sessions from corrupting each other. Two builds in one checkout share an index and a HEAD, and the failures are ugly: a commit amended onto another session's work, a stash that disappears.

- **Nothing in progress** - create one:
  `git worktree add ../<repo>-<slug> -b <branch>`
  The path is a default, not a rule. If the repo already has a worktree convention - a naming
  scheme, or hooks keyed on the path - follow that instead.
- **A related issue, same area, current tree clean** - reuse the tree, **sequentially**. Finish one issue, then start the next. Never two issues in flight in one tree.
- **Grouping** - if sibling issues look worth taking together, name them and let the user confirm. Do not decide it silently.

Branch off the default branch. No draft PR. Merging back is the user's call - `/implement` stops at the commit and hands the branch over for review.

**Caveat worth knowing:** `refs/stash` is shared across worktrees, so a `git stash` in one shows up in all of them. Prefer a commit on the branch over a stash.

## 4. Hand off

State the issue number, the branch and the worktree path in one line, then invoke `/grill-me` or `/implement` - whichever step 2 landed on.
