---
name: writing-plan
description: Turn an approved spec into a bite-sized, file-exact implementation plan before any code gets touched. Use once a spec or set of requirements exists for a multi-step task, as the step right before implementation/TDD begins.
---

# Writing a Plan

## Overview

Write an implementation plan assuming the engineer executing it has zero context on this codebase: exact files to touch, the actual code (not a description of it), how to test each step, and any docs worth a glance. Every task is bite-sized. DRY, YAGNI, TDD, frequent commits.

Assume a skilled developer who knows almost nothing about this toolset or domain, and who won't infer test design from vibes.

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md` (follow the project's existing convention if one already differs).

## Scope check

If the spec spans multiple independent subsystems, it should already have been split during grilling or spec-writing. If it wasn't, say so and propose splitting into separate plans, one per subsystem, each producing working, testable software on its own.

## File structure first

Before writing tasks, map out which files get created or modified and what each one owns. This is where the real decomposition decisions get made:

- One clear responsibility per file.
- Files that change together live together; split by responsibility, not by technical layer.
- In an existing codebase, follow its established patterns rather than unilaterally restructuring, but if a file already being touched has grown unwieldy, a split can be a task in the plan.

## Task granularity

Each step is one action, a few minutes of work: write the failing test, run it and confirm it fails, write the minimal implementation, run it and confirm it passes, commit. Nothing bigger gets its own bullet.

## No placeholders

These are plan failures, never write them: "TBD" / "implement later" / "add appropriate error handling" / "write tests for the above" without the actual test code / "similar to Task N" instead of repeating the code / any type, function, or method referenced but never defined in an earlier task.

Every step must contain the exact content an engineer needs: exact file paths, complete code, exact commands with the expected output.

## Unresolved decisions loop back

If writing the plan surfaces a decision the spec left open - a choice of approach, a design
edge nobody settled - stop and take it back to **grill-me** rather than deciding it silently
inside the plan. A plan is where settled decisions become steps, not where open ones get made.

## Plan header

Every plan starts with a short header stating the goal in one sentence, a 2-3 sentence architecture summary, and the key tech/libraries involved, followed by numbered tasks with `- [ ]` checkboxes so progress is trackable.

## Self-review before handoff

After writing the full plan, check it with fresh eyes:

1. **Spec coverage:** walk each requirement in the spec, confirm a task implements it; list any gap.
2. **Placeholder scan:** search for the red flags above and fix them.
3. **Type consistency:** do names, signatures, and properties used in later tasks match what earlier tasks defined? A function called one thing in Task 3 and another in Task 7 is a bug in the plan.

Fix issues inline as you find them; no need to re-run the whole review afterward.

## Handoff

Once the plan is saved and self-reviewed, hand it to the build: **tdd** to work it
test-first yourself, or **subagent-driven-development** to dispatch a fresh subagent per
task with a review after each. The user picks.
