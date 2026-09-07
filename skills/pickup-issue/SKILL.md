---
name: pickup-issue
description: Load one issue's context and set up its workspace, then hand to /implement. Use when the user names an issue to work on ("pick up #12", "let's do issue 40", "start on the auth one"), or points at an issue URL and wants work to begin.
---

# Pick up an issue

Get the context and the workspace right, then hand over. **This skill does not write code.**

## 1. Read the ticket

Where tickets live is recorded in `.claude/tracker.md`, and **no such file means GitHub** - the
common case, and the default across this set.

**On GitHub:**

```
gh issue view <N> --comments
```

Read the body **and the comments**. Decisions get made in comment threads and never make it back into the body, so a body-only read will build the wrong thing confidently.

**On local files:** `to-issues` writes one file per ticket under `.scratch/<slug>/issues/<NN>-<slug>.md`, numbered in dependency order. Read the file the user named - by number, by slug, or the lowest-numbered one whose blockers are all done. There are no comments to miss, but the "Blocked by" line is load-bearing: a ticket whose blockers are still open is not takeable, and picking one up out of order builds on something that does not exist yet.

**On any other tracker:** use the read command the tracker note records. Where it says `automation: none`, ask the user to paste the ticket in - it is the one thing they can do that you cannot.

Whichever it was, everything below is the same. A ticket is a ticket.

If the ticket references a parent, a spec, or a blocking ticket, read those too.

## 2. Brief the human first

Before any exploration starts, write a brief for a reader who has no context on the codebase.
Cover what the user sees, what they expect instead, why it matters, what the discussion has
already decided or ruled out, and what is still open.

**Plain language only. The brief contains no function names, no file names, no code lines and no
identifiers.** Say "the login flow", never the name of the module that implements it. That
constraint is the point rather than a courtesy: a brief you cannot write without identifiers is a
ticket you have not understood, and the gap shows here, where it is still cheap.

Deliver the brief, then explore.

## 3. Check the claims against the tree

**Check the issue's claims against the live tree.** An issue is a hypothesis, including last
week's: the paths, counts and code references it states go stale between writing and pickup. Worse,
an issue drafted by an agent without repo access mixes verified fact and confident guess in prose
that reads identically - the verified parts check out, so the guessed parts get trusted too.

The check is greps and file reads, dozens of them, and this session needs only the verdicts.
**List the claims yourself, then dispatch the check to `Explore` agents, and audit their
receipts.** Extracting the claims is judgment, so it stays here.

Split the work into two to four independent questions, and assign each claim to the question that
can check it. The usual questions: where the behaviour lives, where the reported input enters,
what tests already cover it, and what a fix would touch. Then dispatch **one `Explore` agent per
question, all in a single message so they run concurrently**. A small ticket with one question
gets one agent. Each prompt carries:

1. The question, and the claims assigned to it, one per line, in the ticket's own words.
2. The repo root and the worktree path if one exists.
3. The rule below, and the receipt shape: the files that answer the question, each with a one-line
   role, then one row per claim, its state, and its evidence.

Resolve every claim to one of three states, and never quietly promote one:

- **Confirmed** - with the `file:line` that shows it.
- **Contradicted** - with the `file:line` of what is actually there instead.
- **Unknown** - with the search terms tried. An unknown left standing as an unknown is a good
  outcome. An unknown rounded up to confirmed is how the wrong thing gets built.

**Claims of absence are the hardest and the most often wrong** - "there is no X", "nothing handles
Y". Confirming absence takes positive search evidence, so the receipt records what was searched
rather than only that nothing was found.

Audit the receipt before you trust it. Open one Confirmed `file:line` and one Contradicted one.
An Unknown with no search terms listed is a finding, so send it back with `SendMessage` rather
than re-running. **Already a subagent?** Run the check yourself.

When every agent has finished, deliver **one map**: the files involved and what each does in this
issue, the one or two places a fix most likely goes, and a claim table with a verdict for each
claim. File paths belong here, unlike in the brief. The map is done when every question and every
claim has an answer, or an explicit "not found".

Then trace each contradiction forward. A wrong claim rarely stays local: name the acceptance
criteria, scope statements and design decisions that rested on it. A contradicted claim is a
headline, not a footnote. Surface all of it and let the user rule before any code gets written -
do not build on a stale premise.

## 4. Decide whether it is settled enough to build

A ticket from `/to-issues` arrives with its decisions already made. An issue written by someone
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

## 5. Resolve the workspace

Worktrees are what stop parallel sessions from corrupting each other. Two builds in one checkout share an index and a HEAD, and the failures are ugly: a commit amended onto another session's work, a stash that disappears.

- **Nothing in progress** - create one:
  `git worktree add ../<repo>-<slug> -b <branch>`
  The path is a default, not a rule. If the repo already has a worktree convention - a naming
  scheme, or hooks keyed on the path - follow that instead.
- **A related issue, same area, current tree clean** - reuse the tree, **sequentially**. Finish one issue, then start the next. Never two issues in flight in one tree.
- **Grouping** - if sibling issues look worth taking together, name them and let the user confirm. Do not decide it silently.

Branch off the default branch. No draft PR. Merging back is the user's call - `/implement` stops at the commit and hands the branch over for review.

**Caveats worth knowing:** a worktree isolates *files only*. `refs/stash` is shared across worktrees, so a `git stash` in one shows up in all of them - prefer a commit on the branch over a stash. So is everything outside git: ports, a local database, `.env` files. Two parallel sessions can still fight over those.

## 6. Hand off

State the issue number, the branch and the worktree path in one line, then invoke `/grill-me` or `/implement` - whichever step 4 landed on.
