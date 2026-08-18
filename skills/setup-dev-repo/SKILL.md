---
name: setup-dev-repo
description: Set up a dev project - create the repo or adopt an existing one, then wire the stack, dev environment and commit gate. Dev projects only, never context repos.
---

# Setup Dev Repo

## Overview

Gets a dev project ready to work in. It looks first, because the two situations need different
things: a brand-new project has to be created, and an existing one has to be understood.
Everything after that first branch is the same.

**Dev projects only.** A context repo - training material, uddannelse, documentation - has no
stack, no tests and no commit gate, so there is nothing here for it. Do not run this on one.

## Step 0: look before you act

Establish which situation you are in before changing anything:

- `git rev-parse --is-inside-work-tree` - is this a repo at all?
- Manifests: `package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `Cargo.toml`,
  `*.csproj`, `pom.xml`, `Gemfile`.
- Existing tooling: a lockfile, `.pre-commit-config.yaml`, `.husky/`, workflows under
  `.github/workflows/`, a configured formatter or linter.

No manifest and no repo means **new project**. Anything already there means **existing
project**, and the job changes from building to understanding.

## New project

### 1. Name it

**Ask the user what the repo should be called and which owner (account or org) it belongs
under.** Do not guess and do not derive it from a convention - naming schemes are the owner's
business, and renaming a repo later breaks every clone and remote. This is the cheapest possible
moment to be sure.

### 2. Create it

Create the repository under the correct owner, with an empty first commit so the default
branch exists. Seed only:

| Seeded | Why |
|---|---|
| Issue labels: `afk` `hitl` | `to-issues` stamps one on every slice: can a person walk away while this is built? `afk` for small, decision-free work, `hitl` where a decision is still plausible. Nothing gates on them. Type and severity are deliberately absent - GitHub gives you those and nothing here read them |
| A license | One file, and awkward to remember later |
| The default branch | Nothing else works without it |

Not seeded: a starter `.github/` directory (an empty template folder is clutter the agent
reads past every session - add it the day a real PR template exists), and not branch
protection (those rules need per-project thought, and a rule set too tight silently blocks the
agent's own pull requests).

### 3. Take the stack from the plan

By the time this runs the stack is usually already settled - `grill-me` or `wayfinder` decided it,
or the user named it in the same breath as the repo. Read it off what you have and confirm in one
line rather than re-asking.

Ask only about what is genuinely still open, and only where the answer changes what you build. The
two that are rarely inferable are the **package manager** (`uv` vs `pip`, `bun` vs `npm`) and
**what kind of thing this is** - CLI, library, web service - because that shapes the layout.
Everything else: take the ecosystem standard and say which one you took.

**Match the question to the person** - someone who names a stack gets answered in those terms;
someone who does not know gets a recommendation they can take without bluffing.

### 4. Scaffold

1. `git init` if needed; a language-appropriate `.gitignore`, plus `.claude/reports/` so generated reports never get committed.
2. The minimal layout and manifest for the chosen stack.
3. Install dependencies with the project's package manager (`bun`, `uv`).
4. A formatter, a linter or type-checker, and a test runner - plus **one trivial passing
   test**, so the suite is green from the first commit and the gate has something to run.
5. The commit gate (below).
6. An initial commit.

## Existing project

### 1. Identify the stack

Read the manifests and lockfiles. Do not assume - a repo with a `package.json` may still be
driven by a Makefile.

### 2. Install the dependencies

With the project's own package manager, read off the lockfile. Note anything else the repo
says it needs to run: required runtime versions, env vars (`.env.example`), services
(`docker-compose.yml`, a README "Getting started"). Nothing in step 3 can run until this has.

### 3. Find the real commands, then run them

Look for what the project actually uses for format, lint, type-check, test and build:
`package.json` scripts, a `Makefile` or `Taskfile`, `pyproject.toml`, `tox.ini`, the CI
workflows.

**Then run each one and confirm it works.** This is the step that matters. Config rots: a repo
can claim `npm test` works when it has not for a year, and a command taken on trust puts
everything built on top of it on a broken foundation. A documented command is a claim, not
evidence.

### 4. Fill the gaps

If a formatter, linter or test gate is missing, propose adding it - but **match what is already
there** rather than imposing a different stack on someone else's codebase.

## The commit gate (both paths)

The mechanism differs per ecosystem, the principle does not: run the fast deterministic checks
on every commit, block on failure, and auto-format so all output meets the project's style.

1. **Use the project's native mechanism** - the `pre-commit` framework, Husky with lint-staged,
   a plain git hook, whatever fits.
2. **Order the checks cheapest first**: format, then lint and type-check, then the fast test
   subset. Keep it quick; slow and end-to-end tests belong in CI.
3. **Mirror the same checks in CI.** A local gate can be walked past with `git commit
   --no-verify`, so a gate that exists only locally is a suggestion. CI is where it becomes a
   rule. Every project gets this; on a small one it is a single workflow running the same commands,
   nothing more.

   **This step is load-bearing, not hygiene.** Work merges once its checks are
   green, so CI is the last thing standing between a change and trunk. A project whose CI
   runs nothing will merge anything.

### Prove it blocks

**Do not report the gate as working until you have watched it work.** Make a commit that
violates a rule and confirm it is rejected. Then make a clean one and confirm it passes.

A misconfigured gate is indistinguishable from a working one right up until something broken
sails through months later. Installing it is not evidence; watching it block is.

## Seed `CLAUDE.md` (both paths)

Write a slim `CLAUDE.md` at the repo root. Other skills read it as the conventions file -
`pickup-issue` sessions read it at the head of every issue, and the built-in `/code-review`
checks the diff against it - so
a repo without one leaves both of them guessing.

Do this last, because by now you know things that were only assumptions at the start. Record
what you **verified**, not what you intended:

| Include | Why |
|---|---|
| The stack, in one line | The first thing any session needs |
| The real commands for test, lint, type-check, build | You just ran them. These are evidence, not claims |
| How the commit gate works and what it runs | So nobody re-derives it or works around it |
| Repo-specific conventions that are not guessable from the code | The only part a human has to supply |

**`CONTEXT.md` is deliberately not seeded.** Several skills read the domain glossary, but an
empty one is clutter the agent reads past every session, and the vocabulary does not exist yet on
day one. `update-docs` creates it the first time a term is worth recording.

**Slim pointer, not a fat template.** Every line here is re-read at the start of every session
forever, so it is the most expensive prose in the repo. Aphorisms, restated best practice and
anything the agent could learn by reading one file are pure cost. If a section would be true of
any project, leave it out.

On an **existing repo that already has one**, do not overwrite it. Propose additions for
whatever the discovery step learned that the file does not already say, the same way missing
linters are proposed rather than imposed.

## Report

Say what was wired, what the checks returned, and what a human still needs to handle - secrets,
deploy targets, anything requiring an account you do not have.

End by pointing at the next stage, sized to the project: on a bigger project - weeks of work,
many sessions - suggest **wayfinder**, since at that size there is fog you cannot chart yet. On
a smaller one, or when the user already knows the shape, suggest **grill-me**. Suggest, do not
launch.

## Done when

- [ ] A fresh clone can install everything without manual fixes
- [ ] The format, lint/type-check and test commands exist and were **run**, not read
- [ ] The commit gate was seen blocking a bad commit and passing a clean one
- [ ] CI runs the same checks as the gate
- [ ] A slim `CLAUDE.md` records the stack, the verified commands and the gate
- [ ] The user knows what only a human can still do (secrets, deploy targets)

## Related skills

- **wayfinder** / **grill-me** - the planning that continues once the project runs. Often they
  already ran and settled the stack; this skill just wired it.
