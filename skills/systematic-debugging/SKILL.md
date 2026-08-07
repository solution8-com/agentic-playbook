---
name: systematic-debugging
description: Disciplined root-cause debugging for any bug, failing test, performance regression, or unexpected behavior. Builds a feedback loop, then reproduces, hypothesizes, instruments, fixes, and locks the fix in with a regression test. Use before proposing any fix, especially when a "quick patch" feels obvious or time is short. Also answers to diagnosing-bugs.
---

# Systematic Debugging

## Overview

Guessing wastes time and creates new bugs; a patch that hides the symptom just means
it comes back later, somewhere else. Find the root cause before touching code.

**The rule:**

```
NO FIX WITHOUT A REPRODUCIBLE FEEDBACK LOOP AND A ROOT-CAUSE FINDING FIRST
```

If you haven't built a loop and traced the cause, you're not ready to propose a fix,
no matter how obvious it looks.

## When to use

Any bug, failing test, regression, or "that shouldn't happen" moment. Use it
*especially* when you're under time pressure, a fix seems obvious, you've already
tried something that didn't work, or you don't fully understand what's going on yet.

## Phase 1: build the feedback loop

This is the actual skill; everything after this is mechanical once you have a fast,
reliable pass/fail signal. Spend the most effort here.

Ways to build one, roughly in order of how often they apply:

1. A failing test at whatever seam reaches the bug (unit, integration, e2e).
2. A script hitting a running dev server (curl, an RPC call, a driven terminal
   session).
3. A CLI or fixture-driven invocation, diffed against known-good output.
4. A headless browser pass (Playwright) driving the UI and checking DOM/console.
5. A captured trace or payload replayed through the code path in isolation.
6. A throwaway harness exercising just the broken path with mocked dependencies.
7. A fuzz loop, if the failure is "sometimes wrong," to find the failure shape.
8. A bisection harness (`git bisect run`) if the bug appeared between two known
   states.

Iterate on the loop itself: make it faster (skip unrelated setup), sharper (assert on
the exact symptom, not "didn't crash"), and more deterministic (pin time, seed
randomness, isolate the filesystem and network). A flaky 30-second loop barely beats
no loop at all; a deterministic 2-second one does most of the work for you.

For flaky/non-deterministic bugs, the goal isn't a clean repro, it's a *higher*
reproduction rate: loop the trigger, add stress, narrow timing windows. A 50%-flake
bug is debuggable; 1% usually isn't yet.

If you genuinely can't build a loop: stop, say so, list what you tried, and ask the
user for environment access, a captured artifact (log, HAR file, screen recording), or
permission to add temporary instrumentation. Don't skip ahead to guessing.

**Phase-1 completion gate.** Before you form a single hypothesis (Phase 4), you must be
able to name one command you have *already* run and paste its exact invocation and its
output - the reproducible red. If you can't paste a real command and its failing
output, you don't have a loop yet: stay in Phase 1, do not advance.

## Phase 2: reproduce and investigate

1. Read the error completely, stack trace included. It usually contains the answer.
2. Confirm the loop reproduces the *same* failure the user described, not a
   coincidentally-similar one.
3. Minimise the reproduction: shrink to the smallest input, fixture, or case that
   still fails, stripping away everything that doesn't change the red. A one-line repro
   points at the cause far faster than the full scenario, and it becomes the
   seam-level test in Phase 6.
4. Check what changed recently: `git diff`, recent commits, dependency bumps, config
   or environment drift.
5. In a multi-component flow (UI -> API -> service -> DB), add instrumentation at
   each boundary before guessing which one is at fault, then trace from there.
6. Trace the data backward from the failure to its source; fix at the source, not
   where the symptom surfaced.

## Phase 3: pattern analysis

- Find a working example of similar code in the repo. What does it do differently?
- If you're implementing a known pattern, read the reference implementation in full,
  not a skim.
- List every difference between the working and broken paths, even ones that "can't
  matter."

## Phase 4: hypothesize

Write 3-5 ranked, falsifiable hypotheses before testing any of them (generating only
one anchors you on the first idea that sounds plausible). Each one should state a
prediction: "if X is the cause, changing Y makes the bug disappear." If you can't
state the prediction, it's a guess, not a hypothesis; sharpen or drop it.

Share the ranked list with the user before testing when you can; they often re-rank
it instantly with context you don't have. Don't block on this if they're away.

## Phase 5: instrument

Change one variable at a time. Prefer a debugger/REPL breakpoint over a pile of logs.
Tag any temporary debug log with a unique marker (e.g. `[DEBUG-a4f2]`) so cleanup is
one grep. For performance regressions, measure first with a real baseline
(`performance.now()`, a profiler, a query plan) before touching code; logs are
usually the wrong tool for performance bugs.

## Phase 6: fix and regression-test

If a correct test seam exists, turn the minimized repro into a failing test there
first (this is where the **tdd** skill's red-green-refactor loop takes over), watch it
fail, apply one root-cause fix (no bundled "while I'm here" changes), watch it pass,
then re-run the original Phase 1 loop against the un-minimized scenario.

If no correct seam exists, that absence is itself a finding, worth flagging for
Phase 7 rather than skipped over.

If the fix doesn't hold: stop and count attempts. Fewer than 3, go back to Phase 2
with what you just learned. Three or more failed fixes in a row means the
architecture, not the hypothesis, is the problem, surface that to the user before
attempting a fourth.

## Phase 7: cleanup and post-mortem

- [ ] Original repro no longer reproduces
- [ ] Regression test passes, or the missing seam is documented
- [ ] All `[DEBUG-...]` instrumentation removed
- [ ] Throwaway harnesses deleted or clearly marked
- [ ] The commit/PR message states which hypothesis turned out correct

Then ask: what would have prevented this? If the answer is architectural (no test
seam, tangled coupling, hidden dependency), hand the specifics to the
**improve-codebase-architecture** skill; you have more information now than when you
started, so make that call after the fix lands, not before.

## Red flags: stop and go back to Phase 1

"Quick fix now, investigate later" - "just try changing X" - "I'll change a few
things and run the tests" - "it's probably X" - "I don't fully understand it but this
might work" - "one more fix attempt" after two failures already - each fix revealing a
new problem somewhere else. Any of these means stop, go build the loop, find the root
cause.

## Common mistakes

| Excuse | Reality |
|---|---|
| "Simple issue, skip the process" | Simple bugs have root causes too; the process is fast for them. |
| "Emergency, no time to be systematic" | Guess-and-check thrashing is slower than the loop. |
| "Try this first, investigate if it fails" | The first fix sets the pattern; do it right from the start. |
| "Multiple changes at once saves a round trip" | You lose the ability to tell which change worked, and you can introduce new bugs. |
| "I see the problem, let me just fix it" | Seeing the symptom isn't the same as knowing the cause. |

## Related skills

- **tdd** - writes the regression test in Phase 6 once a correct seam is found.
- **improve-codebase-architecture** - when the Phase 7 post-mortem points at a
  structural cause rather than a local bug.
