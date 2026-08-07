---
name: code-review
description: Review a diff with parallel Standards and Spec passes, drive the UI in a browser if the interface changed, then auto-apply the mechanical fixes it finds rather than stopping at a report. Runs on a PR before it lands, or over the day's diff at the end of a work session. Use when the user says "review this", "review the PR", "review today's work", or "review and fix".
---

# Code Review

## Overview

Review the diff along two axes at once, then fix what the review found in the same
pass. There is no hand-off report and no human gate between "here are the findings" and
"the findings are applied", the finding and the fix are one motion.

**Core principle:** review is not done when the problems are named, it is done when
they are fixed and re-verified. But auto-applying changes unsupervised has a blast
radius, so the skill applies fixes only within an agreed safety boundary and re-runs
the suite after.

## What diff to review - two modes, neither mandatory

Review is **optional and flexible**: reviewing every issue before
every merge is overkill for small slices. Two modes:

- **Mode A - one PR, before it lands** (recommended for bigger or riskier issues). A
  fresh session reviews the issue's branch before `close-issue` merges it:

  ```
  git diff main...HEAD        # this issue's branch
  ```

- **Mode B - the day's diff, at the end of the work session.** A fresh session reviews
  everything that landed today. Lighter ceremony; the trade is that it reviews already
  merged code, so findings become follow-up fixes or new issues rather than pre-merge
  changes.

### Why mode A gets the recommendation

The evidence favors per-change, pre-integration review. Mode B stays available with eyes
open about the trade.

**No line-count trigger.** The widely-repeated "defect detection drops past 200-400 lines"
is a time budget converted into lines at an assumed reading rate, not a measured threshold -
the original study says so in its own text. If a single issue's diff is genuinely too big to
hold in one sitting (roughly 10+ files is the better signal), that is a sign the slice was
too fat. Split the review, and note it so `to-issues` slices thinner next time.

### What this skill does NOT catch

Problems that only appear **across** several issues: three slices that each added a
near-identical helper, a convention that drifted over an afternoon, an abstraction that
stopped fitting two issues ago. A per-issue reviewer cannot see those, and batching reviews
is the wrong fix - it buys them at the cost of attention on everything else.

Those belong to **improve-codebase-architecture**, run periodically rather than per issue.

### Expect most findings not to be bugs

Most findings will be convention, naming and preference, not defects. That is normal, and
it is why the auto-apply boundary below matters: most of what this produces should be
applied quietly or dropped, not escalated.

## Annotate the diff first

**Before either pass runs, walk your own diff and write down what is not obvious.** Each
non-trivial decision: what you did, and why. Where something looks wrong but is handling a
case that is not visible locally, say so.

Treat the annotation as a **prompt to re-examine your own work**, not as a defence of it.
If writing "I did it this way because..." produces no good reason, that is the finding -
fix it before the review starts.

`close-issue` carries these annotations into the PR body, where they are also what a human
reads first.

## The two review passes (run in parallel)

1. **Standards pass.** Repo conventions (`CLAUDE.md`/`AGENTS.md`), plus a code-smell
   baseline (Fowler smells: duplication, long functions, feature envy, primitive
   obsession, and so on). Is the diff clean, idiomatic, and consistent with the
   codebase?
2. **Spec pass.** Does the diff faithfully implement the originating issue/spec? Are
   the acceptance criteria met? Anything missing, out of scope, or subtly wrong against
   what the issue intended?

Run both, then merge their findings into one list before applying anything.

## If the diff touched the interface, drive it

Unit tests can be green while the UI is broken: a component throws on mount, a route 404s,
a form never submits. When the diff touched the interface, **open it in a real browser
through the Playwright MCP** as part of this review.

Judge that from the diff, not from a label. A slice nobody called UI work can still have
edited a component.

What to do:

1. **Bring up the app** and get its URL. Take the dev-server command from `CLAUDE.md`. If
   it is not discoverable, say so and stop - guessing a port produces a confident pass
   against nothing.
2. **Load the screens the change touched** and confirm they render without console errors.
3. **Drive the flows the changes affect** - click, type, submit - and assert the expected
   result appears. Scope to what changed; breadth is the test suite's job.
4. **Capture a snapshot** of the key state, so there is something concrete to look at.

Fold what this finds into the same findings list as the two passes above. A render failure
or a dead flow is a Spec-category finding: report it, do not guess at a fix.

**Unit-green is not UI-working**, and this is the only place in the lane that checks the
difference. A human judging how the UI actually *feels* is still a separate thing, and
still worth doing - no assertion captures it.

## Auto-apply, with a boundary

After findings are collected, apply the fixes, but only inside this boundary. **The test
is mechanical versus judgement, not confident versus unsure.** This is the one stage that
changes code with nobody watching, so a wrong call about "unambiguous intent" lands
silently in a commit.

- **Apply directly: mechanical fixes only, in scope only.** Convention and smell
  corrections, naming, formatting, dead code, unused imports, test naming and structure,
  missing error handling with an obvious shape. These have one right answer that the diff
  itself makes evident.
- **Out of scope for the issue under review: file a new issue, do not fix.** A real
  finding that belongs to another part of the codebase, or would grow the change beyond
  what the issue asked, becomes a labelled issue to be tackled another time. Never
  gold-plate the diff to satisfy the review.
- **Report and stop on everything else**, including Spec-category findings and anything
  whose fix has more than one defensible answer. A behaviour gap against the issue is a
  judgement call about intent, however clear it looks. Write it up with the evidence and
  let a human decide.
- **Report and stop inside the repo's high-risk areas**, whatever the project treats as
  such (auth, permissions, secrets, data handling, migrations, and any area its own
  conventions doc marks sensitive). This holds even in AFK mode.

Verify each finding is real before acting on it, do not perform agreement by applying
noise, and do not blindly implement a suggestion you can show is wrong.

The danger is not that an auto-applied fix is wrong. It is that it is **plausible and
wrong in an area where being wrong is expensive** - and a fix the agent applied to itself
gets far less scrutiny than one it had to propose. Report-and-stop findings go
into the report with the reasoning, for a human to weigh.

## After applying

1. **Re-run the full suite.** Applied fixes must leave the suite green and the output
   clean. A fix that breaks a test is not a fix.
2. **Re-review the applied changes** briefly, an auto-applied fix can introduce its own
   smell.
3. **Summarize** what was found, what was auto-applied, and what was escalated for a
   human (unclear-intent and high-risk-area findings), so the auto-apply stays
   auditable.

## Common mistakes

| Mistake | Fix |
|---|---|
| Stopping at a findings report | This skill applies and re-verifies; a report alone is the old behavior. |
| Fixing out-of-scope findings in place | File a new issue instead. Gold-plating the diff grows the change past the issue. |
| Reviewing without annotating first | The annotation is the highest-leverage step in the skill and takes a minute. |
| Auto-applying a Spec fix on a guessed intent | If intent is unclear, escalate, don't guess. |
| Touching high-risk areas unattended | Flag findings in the repo's sensitive areas for a human. |
| Not re-running tests after applying | Every applied fix must leave the suite green. |
| Applying a finding you can't verify is real | Verify first; performative fixes add noise. |

## Heavier passes

For a deeper generic review, Claude Code's built-in `/code-review` is a good escalation;
for diffs touching auth, secrets, payments or infra, the built-in `/security-review` is
the right tool. This skill stays the lane's default because it knows the workflow - the
annotation step, the auto-apply boundary, and where out-of-scope findings go.

## Related skills

- **tdd** / **subagent-driven-development** - produce the tested diff this skill reviews.
- **improve-codebase-architecture** - the periodic pass that catches what a single review
  structurally cannot: duplication and drift across many issues.
- **close-issue** - in mode A runs after this, carries the annotations into the PR, and
  merges on green.
- **to-issues** - where out-of-scope findings become new issues.
