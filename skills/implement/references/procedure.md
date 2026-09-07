# Implement - the build procedure

The full build procedure. `SKILL.md` dispatches a subagent here, and this file is what that
subagent follows. Already running as a subagent? This is your procedure. Work it top to bottom.

Your brief carries the plan, the test mode, the branch, the worktree path and the repo root.
Build what the brief describes. The plan is settled, so do not reopen its decisions. Where the brief marks a
claim as contradicted, build on what the tree holds, not on what the ticket says.

Work autonomously. The parent audits your receipt at the end, so the ordinary build decisions
are yours.

## 1. Name the seams

**Tests off?** Skip this step, say so in one line, and go to step 2. Typechecking and the live
verification of step 4 are your gate.

Use `/tdd` where possible, at the seams the plan agreed. List the seams you intend to test in
your first message to the parent, then run the loop uninterrupted, one cycle straight into the
next. The parent checks the finished tests against this list.

One vertical slice at a time: a failing test, then just enough implementation to pass it, then
green, then the next slice. A bug fix starts with a test that reproduces the bug. Each test lands
with the implementation it drives, and the refactoring belongs to the review of step 3.

Match the neighbours. `.claude/rules/`, `AGENTS.md` and the tests already beside the code you
touch define where tests go, what they mock and how they read. They outrank generic habits.

## 2. Build

Run typechecking regularly, single test files regularly, and the full test suite once at the
end.

Run the repo's own gate, the one its `AGENTS.md`, `CLAUDE.md` or `package.json` names, until it
exits 0. Tests on: that gate runs the suite, so the whole suite goes green, not only the tests
you added.

## 3. Commit and pause

Commit to the current branch. The review diffs committed work, so this commit is what makes the
change visible to it.

Report to the parent: the commit SHA, the gate command, and the seams you tested. Then stop.

The parent runs `/code-review low` and relays the findings. Fix what they name, re-run the gate,
commit.

## 4. Verify the running app

A green suite is no evidence that the feature works in the running app, so verify it live. This
holds in both test modes, and with tests off it is most of your evidence.

Check what the diff touched. **Where it touched none of UI, an endpoint or the database, skip this
step and say so in one line.** A pure refactor produces a report of nothing-applicable rows, and
an artifact per commit that proves nothing trains people to stop opening them.

Otherwise **dispatch the verification to its own subagent, and audit its receipt.** The run drives
browsers and restarts stacks, and its hundreds of tool results do not belong in your build
context.

Dispatch one `general-purpose` agent, because the run needs the Playwright MCP tools, Bash and
file writes. Its prompt carries:

1. Read the `verify-feature` skill's `references/procedure.md` first, and follow it.
2. Repo root, current branch, the worktree path, the trunk, and the target: the branch's diff
   against its merge base with the trunk.
3. Depth: adversarial where the diff covers a whole feature, default otherwise.
4. Fix mode: **off**. You hold the build context, so the fixes are yours, not the verifier's.
5. The report path: `.claude/reports/<YYYY-MM-DD>-verify-<slug>.html`.
6. Intent: what the plan asked for, in your words. The verifier reads the diff and nothing else
   of this run.
7. Known-accepted deferrals from your brief, so the verifier marks them `accepted`.
8. The project memory directory.
9. Scope the user set: surfaces to skip, fixtures to use, an environment already running.

You built this code, so you already believe it works. That is why the flows and the assertions
come from the ticket and the diff, not from what you remember intending.

Audit the receipt against evidence outside the verifier's own words: `git status --short` shows a
clean tree, the report file exists at a plausible size, and all four categories are present. A
missing category is a silent skip.

Fix loop: fix what the receipt names, re-run the gate, and commit to the current branch. Then
re-verify with `SendMessage` to the same verifier, whose context is intact, rather than
dispatching a second one. Loop until the receipt is green. When the same failure survives three
fix attempts, stop looping and report what is stuck, and why.

## 5. The receipt

Send the parent:

- Every commit SHA, with a one-line subject.
- The gate command and its exit code on the final run.
- Tests on: the seams you named, and the test file that covers each.
- Each review finding, and how you fixed it.
- The `verify-feature` report path and the verifier's receipt rows unchanged, or the one line
  that says why the step was skipped.
- Anything in the plan you left out, and why.
