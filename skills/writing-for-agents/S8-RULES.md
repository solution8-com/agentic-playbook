# S8 house rules

The catalog-specific branch of [`writing-for-agents`](SKILL.md): what applies when the skill you are writing belongs to this repo's `skills/` catalog. The universal reference is `SKILL.md`, the skill mechanics are `SKILL-MECHANICS.md`; this file carries only the house law, the testing discipline, and the review checklist.

## When a technique deserves a skill

**Write one when:** the technique wasn't obvious, you'd want it again on a different project, it applies broadly, and it involves a judgment call worth encoding.

**Don't write one for:** a one-off fix, something already well documented, a project-specific convention (that belongs in `CLAUDE.md` or `docs/`), or a mechanical rule a script or hook could enforce instead.

## Structure

```
skills/<skill-name>/
├── SKILL.md          # required
├── REFERENCE.md      # heavy reference, only if needed
├── EXAMPLES.md       # worked examples, only if needed
└── scripts/          # deterministic helper scripts, only if needed
```

Flat namespace: every skill lives at `skills/<skill-name>/`, one level, no nesting.

Keep inline: principles, patterns, and code samples under ~50 lines. Split out once `SKILL.md` passes ~100 lines, a section is a genuinely separate domain, or a section is advanced/rarely needed. Add a script only for deterministic operations (validation, formatting); a script is cheaper and more reliable than regenerating the same logic every run.

## SKILL.md template

```markdown
---
name: skill-name
description: <see Descriptions below>
---

# Skill Name

## Overview
What is this, in 1-2 sentences. Core principle.

## When to use
Concrete triggers, symptoms, situations · when NOT to use.

## Core pattern / process
Steps, or a before/after. A checklist for anything multi-step.

## Quick reference
A table for scanning common cases.

## Common mistakes
What goes wrong, and the fix.

## It's working if
Observable success criteria, not prose. What you can check from outside.

## Related skills
Name only in-collection skills the reader might chain into.
```

## Descriptions, house examples

The rules live in `SKILL.md` (a description is a context pointer) and `SKILL-MECHANICS.md` (model-invoked keeps rich trigger branches; user-invoked gets a human-facing one-liner, trigger lists stripped). Never summarize the workflow in a description: an agent that reads the steps there follows the description and skips the body. House examples:

```yaml
# model-invoked: capability + trigger branches, no workflow spoiler
description: Test-driven development with a red-green-refactor loop. Use when implementing any feature or bugfix, before writing implementation code.

# user-invoked: one line for the human browsing the catalog
description: Get interviewed in rounds about a plan or design until every decision is settled.

# weak: summarizes the workflow, the agent will follow it and skip the body
description: Use for TDD; write a test first, watch it fail, write minimal code, refactor
```

Name skills active and verb-first, by what they do (`pickup-issue`, not `issue-helpers`); a gerund works well for a process (`writing-plan`).

## Catalog conventions

- **Self-contained.** A skill in `skills/` may reference only other skills in `skills/`, never an external plugin. Reference by name in prose ("use the **tdd** skill"), never with `@path`, which force-loads the file before it's needed.
- **English bodies.**
- **No metadata in the skill file.** No tag lines, no source or positioning notes, no header blockquotes: frontmatter and instructions only. A skill file is a prompt - every line of it loads on invocation - and metadata kept in two places drifts. Classification (source, lane, interaction axes) lives in `skills/CATALOG.md` and only there; upstream names and repo links never appear in a skill file.
- **No internal history in the body either.** No decision dates, no "an earlier version did X", no rename trails: the skill describes itself as it is, and history lives in the catalog and the ledger. This covers the skills README too - the index describes the set as it is. If a design decision must travel with the skill (an alias, a dropped convention), write it into the instruction where it applies, not as a note about the past.
- **Nothing in a skill reads as an obligation** - the playbook advises, it never mandates. Describe when a skill applies, not that it must be run.
- **No time-sensitive info, no narrative retelling of one incident, consistent terminology throughout.**

## Testing: skill authoring is TDD for documentation

If you haven't watched an agent fail *without* the skill, you don't actually know the skill fixes the right gap.

```
RED      Run a realistic scenario with a fresh subagent, without the skill.
         Write down its exact choices and rationalizations, verbatim.
GREEN    Write the smallest skill that addresses those specific failures.
         Re-run the same scenario with the skill; the agent should now comply.
REFACTOR Agent found a new loophole? Add an explicit counter, re-test.
```

For discipline-enforcing skills (hard rules, like TDD's "no code before a test"), stress it with time pressure and sunk cost, capture every excuse the agent makes in a rationalization table, and state up front that violating the letter is violating the spirit, it closes off a whole class of "technically I followed it" arguments. For technique/reference skills, confirm a fresh agent can apply the technique to a new scenario and find what it needs without extra hand-holding.

## Review checklist

- [ ] `name` uses only letters, numbers, hyphens, and matches the directory name
- [ ] Description follows the invocation split (trigger branches if model-invoked, human-facing one-liner if user-invoked) and doesn't spoil the workflow
- [ ] `SKILL.md` stays tight (roughly under 100-150 lines); depth pushed one file out
- [ ] No metadata blockquotes: frontmatter and instructions only; classification and lineage live in `skills/CATALOG.md`
- [ ] Cross-references only in-collection skills, by name, never `@path`
- [ ] A no-op pass has run on the final draft: delete any line that doesn't change behaviour versus the default
- [ ] Steering is positive, not by prohibition, except hard guardrails
- [ ] Tested against a real scenario, not just read back
- [ ] Timeless wording, one name per concept, zero storytelling

## Related skills

- **grill-me** - useful for gathering requirements when the shape of a new skill isn't obvious yet.
- **tdd** - the discipline the testing section borrows from.
