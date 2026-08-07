---
name: setup-dev-repo
description: Set up a dev project - create the repo or adopt an existing one, then wire the stack, dev environment and commit gate. Dev projects only, never context repos.
disable-model-invocation: true
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

Repo names say who the work is for:

| Kind | Pattern | Example |
|---|---|---|
| Client engagement | `EXT-<client>-<project>` | `EXT-elservice-fakturaflow` |
| S8's own work | `INT-<project>` | `INT-s8-agentic-playbook` |

Lower-kebab after the prefix. The client segment exists only on external repos.

**Ask which it is if the user has not said.** It is not inferable - "fakturaflow" does not tell
you whether a client is behind it - and renaming a repo later breaks every clone and remote.
This is the cheapest possible moment to be sure.

### 2. Create it

Create the repository under the correct owner, with an empty first commit so the default
branch exists. Seed only:

| Seeded | Why |
|---|---|
| Issue labels: `feature` `bug` `task`, `high` `medium` `low`, `afk` `hitl` | `to-issues` stamps one from each group on every slice, so the issue list is readable at a glance. They describe the work; nothing gates on them |
| A license | One file, and awkward to remember later |
| The default branch | Nothing else works without it |

Not seeded: a starter `.github/` directory (an empty template folder is clutter the agent
reads past every session - add it the day a real PR template exists), and not branch
protection (those rules need per-project thought, and a rule set too tight silently blocks the
agent's own pull requests).

### 3. Ask what kind of project

One question, with the recommendation shown:

- **Complex** - a full application: framework, database, auth, the usual stack.
- **Simple** - a script or small tool: a language, a test runner, a commit gate. No framework,
  no database.

**If complex, interview the stack** - five questions, each with a recommended default the
user can simply take:

1. Language and runtime (and version)?
2. Package manager - the non-obvious one (`uv` vs `pip`, `bun` vs `npm`)?
3. What kind of thing is it - CLI, library, web service? It shapes the layout.
4. Test runner (recommend the ecosystem standard)?
5. Formatter and linter (recommend the ecosystem standard)?

**If simple**, skip the interview: pick the ecosystem standards for the language at hand and
confirm them in one line.

**Skip anything already answered.** If the user said "set up a python cli", do not ask about
language or project shape - confirm what is left and move on. Only ask questions whose answer
changes what you build.

**Match the question to the person.** Someone who names a stack should be answered in those
terms, not walked through a beginner's interview. Someone who does not know should be able to
take the recommendation without having to bluff. Both paths end in a working project.

### 4. Scaffold

1. `git init` if needed; a language-appropriate `.gitignore`.
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
   rule. Both complex and simple projects get this; on a simple project it is one workflow
   running the same commands, nothing more.

   **This step is load-bearing, not hygiene.** `close-issue` merges a PR once its checks are
   green, so CI is the last thing standing between a change and trunk. A project whose CI
   runs nothing will merge anything.

### Prove it blocks

**Do not report the gate as working until you have watched it work.** Make a commit that
violates a rule and confirm it is rejected. Then make a clean one and confirm it passes.

A misconfigured gate is indistinguishable from a working one right up until something broken
sails through months later. Installing it is not evidence; watching it block is.

## Seed `CLAUDE.md` (both paths)

Write a slim `CLAUDE.md` at the repo root. Other skills read it as the conventions file -
`pickup-issue` sessions read it at the head of every issue, `code-review` checks the diff against it - so
a repo without one leaves both of them guessing.

Do this last, because by now you know things that were only assumptions at the start. Record
what you **verified**, not what you intended:

| Include | Why |
|---|---|
| The stack, in one line | The first thing any session needs |
| The real commands for test, lint, type-check, build | You just ran them. These are evidence, not claims |
| How the commit gate works and what it runs | So nobody re-derives it or works around it |
| Repo-specific conventions that are not guessable from the code | The only part a human has to supply |

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

- [ ] Dependencies install cleanly from a fresh clone
- [ ] The format, lint/type-check and test commands exist and were **run**, not read
- [ ] The commit gate was seen blocking a bad commit and passing a clean one
- [ ] CI runs the same checks as the gate
- [ ] A slim `CLAUDE.md` records the stack, the verified commands and the gate
- [ ] The user knows what only a human can still do (secrets, deploy targets)

## Common mistakes

| Mistake | Fix |
|---|---|
| Running this on a context repo | It has no stack or gate. There is nothing here for it. |
| Guessing the EXT/INT prefix | Ask. Renaming later breaks every clone and remote. |
| Trusting a documented command | Run it. Config rots quietly. |
| Reporting the gate works without seeing it block | You have installed something, not verified it. |
| Imposing a new stack on an existing repo | Match the conventions already there. |
| Asking a question whose answer changes nothing | If the shape is already known, stop asking. |
| Writing a fat `CLAUDE.md` | It is re-read every session forever. Anything true of any project is pure cost. |
| Overwriting an existing `CLAUDE.md` | Propose additions instead. Someone wrote what is there on purpose. |

## Related skills

- **setup-skills** - the global bootstrap that installs the skills and checks the environment.
  Runs before this.
- **wayfinder** / **grill-me** - the planning stages that follow, once the project runs.
