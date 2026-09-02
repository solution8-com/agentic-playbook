# Implement - the build procedure

The full build procedure. `SKILL.md` dispatches a subagent here, and this file is what that
subagent follows. Already running as a subagent? This is your procedure. Work it top to bottom.

Your brief carries the plan, the branch, the worktree path and the repo root. Build what the
brief describes. The plan is settled, so do not reopen its decisions. Where the brief marks a
claim as contradicted, build on what the tree holds, not on what the ticket says.

Work autonomously. The parent audits your receipt at the end, so the ordinary build decisions
are yours.

## 1. Name the seams

Use `/tdd` where possible, at the seams the plan agreed. List the seams you intend to test in
your first message to the parent, then run the loop uninterrupted, one cycle straight into the
next. The parent checks the finished tests against this list.

Match the neighbours. `.claude/rules/`, `AGENTS.md` and the tests already beside the code you
touch define where tests go, what they mock and how they read. They outrank generic habits.

## 2. Build

Run typechecking regularly, single test files regularly, and the full test suite once at the
end.

Run the repo's own gate, the one its `AGENTS.md`, `CLAUDE.md` or `package.json` names, until it
exits 0. The whole suite goes green, not only the tests you added.

## 3. Commit and pause

Commit to the current branch. The review diffs committed work, so this commit is what makes the
change visible to it.

Report to the parent: the commit SHA, the gate command, and the seams you tested. Then stop.

The parent runs `/code-review low` and relays the findings. Fix what they name, re-run the gate,
commit.

## 4. Verify the running app

Check what the diff touched. **If it touched UI, an endpoint or the database**, read the
`verify-feature` skill's `references/procedure.md` and follow it yourself. You already hold the
build context it needs, so do not dispatch it further.

You built this code, so you already believe it works. Pick the flows and the assertions from
the ticket and the diff, not from what you remember intending. Where a check fails, report the
failure rather than adjusting the check. Verification reports, it does not fix.

**Where the diff touched none of those three, skip it and say so in one line.** A pure refactor
produces a report of nothing-applicable rows, and an artifact per commit that proves nothing
trains people to stop opening them.

## 5. The receipt

Send the parent:

- Every commit SHA, with a one-line subject.
- The gate command and its exit code on the final run.
- The seams you named, and the test file that covers each.
- Each review finding, and how you fixed it.
- The `verify-feature` report path, or the one line that says why it was skipped.
- Anything in the plan you left out, and why.
