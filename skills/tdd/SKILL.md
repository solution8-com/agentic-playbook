---
name: tdd
description: Test-driven development with a disciplined red-green-refactor loop, one vertical slice at a time. Tests verify behavior through public interfaces, not implementation. Use when implementing any feature or bugfix, when the user mentions TDD, red-green-refactor, or test-first, or as the build step of an issue session.
---

# TDD

## Overview

Write the test first. Watch it fail. Write the smallest code that passes. Refactor.
Repeat, one behavior at a time.

**Core principle:** if you never watched the test fail, you don't actually know it
tests the right thing.

**Tests verify behavior through a public interface, not implementation details.**
Code changes; a good test shouldn't have to. A test that reads like a spec ("user can
retry a failed operation up to 3 times") survives refactors because it never touches
internal structure.

## The rule

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code before the test existed? Delete it, don't keep it "for reference," and
write the test fresh. Adapting deleted code while writing the test is the same
mistake wearing a disguise.

## Vertical slices, not horizontal

```
ONE TEST -> ONE IMPLEMENTATION -> REPEAT
never: write every test, then write every implementation
```

Writing all the tests first and all the code second produces tests that check the
*shape* you imagined instead of the behavior you built. Each cycle should teach you
something the previous one didn't.

## When to use

Use for any feature, bugfix, or behavior change in this repo. Ask the user first
before skipping it for throwaway prototypes, generated code, or plain config edits.

Between the two build methods: prefer **subagent-driven-development** when the plan is
long, its tasks are independent and fully specified, or the issue runs `afk`; build
test-first yourself with this skill when tasks are coupled, exploratory, or you are
steering mid-build.

If you're using TDD to write a regression test for a bug found via the
**systematic-debugging** skill, this is the skill that writes that test.

## Phase 0: plan before touching code

- Confirm the interface change with the user (what's the public surface?).
- List the behaviors worth testing and prioritize them; you can't test everything, so
  cover critical paths and non-trivial logic, not every edge case.
- Watch for a chance to keep the module's interface small while its implementation
  does the real work (a "deep module," not a thin pass-through).
- Get a nod from the user on the plan before writing the first test.

## Red, green, refactor

1. **Red** - write one small failing test for one behavior. Real code, no mocks
   standing in for the thing you're testing.
2. **Verify red** - run it. It must fail, not error, and fail for the reason you
   expect (missing feature, not a typo). If it already passes, you're testing
   existing behavior; fix the test.
3. **Green** - write the minimum code that makes it pass. No extra features, no
   drive-by refactors elsewhere.
4. **Verify green** - run the full suite. Everything passes, output is clean (no
   warnings hiding in the noise).
5. **Refactor** - only while green. Remove duplication, sharpen names, and look for a
   chance to deepen the module (push complexity behind a small interface). Add no new
   behavior here.
6. Repeat for the next behavior.

## What a good test looks like

| Quality | Good | Bad |
|---|---|---|
| Minimal | tests one thing | name has "and" in it: split it |
| Clear | name states the behavior | `test('test1')` |
| Durable | survives a refactor | breaks when you rename an internal helper |

If a test breaks on a pure refactor (no behavior change), it was coupled to
implementation, not behavior. That's the signal to loosen it.

**The tautological test** is the other quiet rot: the expected value is computed the same
way the code computes it, so the test passes by construction. Expected values come from
somewhere else - a known-good literal, a worked example, the spec. If there is no
independent source of truth to assert against, question whether this change needs the
loop at all.

## Common mistakes

| Excuse | Reality |
|---|---|
| "Too simple to need a test" | Simple code still breaks; the test costs 30 seconds. |
| "I'll test after, to confirm it works" | A test written after the code passes on the first run either way; it proves nothing. |
| "Already tested it by hand" | Ad hoc isn't repeatable and leaves no record. |
| "Keep the old code as reference while I write the test" | You'll lean on it. Delete means delete. |
| "This test is annoying to write" | Listen to it: hard-to-test usually means the interface is too coupled. Simplify it instead of forcing a mock. |

## When stuck

- Don't know how to test it: write down the API you wish existed, then write the
  assertion first.
- Test needs a huge setup: pull the setup into a helper; if it's still huge, the
  design is too tangled.
- You need to mock everything to isolate the unit: mocks are for system boundaries only
  (external APIs, the clock, randomness), never your own modules. That's a coupling
  smell, not a mocking problem - inject the dependency instead.

## Checklist

- [ ] Every new function or behavior has a test
- [ ] Watched each test fail before writing the fix
- [ ] Each test failed for the right reason
- [ ] Minimal code written to reach green
- [ ] Full suite green, output clean
- [ ] Edge cases and error paths covered where they matter

## Related skills

- **systematic-debugging** - use it to find the root cause before writing the
  regression test that locks the fix in.
- **improve-codebase-architecture** - when the refactor step keeps surfacing the same
  friction, hand it off as a candidate for a deeper look.
