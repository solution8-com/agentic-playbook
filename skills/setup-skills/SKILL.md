---
name: setup-skills
description: Install the S8 playbook skills into the current repo and check the environment is ready to use them. Run once per repo, before anything else.
disable-model-invocation: true
---

# Setup Skills

## Overview

The first command on any repo. It puts the playbook's skills into the project and confirms the
environment can actually run them.

It **stops when done** rather than chaining onward. If `gh` turns out to be unauthenticated,
you want to know that before a project gets built on top of it, not halfway through.

## Process

### 1. Check whether the skills are already here

Look for the playbook skills in the repo before installing anything.

| Found | Do |
|---|---|
| Not there | Install them (below) |
| Already there | Say so, install nothing, and point at `/update-skills` if they want the newest |

Never reinstall over an existing set. Re-running this on a repo that already has skills should
be a no-op with a clear message, not a silent overwrite - overwriting can drop local changes
someone made deliberately.

### 2. Install

```
npx skills add solution8-com/INT-s8-agentic-playbook
```

This pulls the current version straight from GitHub into the repo. Nothing is installed
globally, so each repo keeps the skills it was set up with.

### 3. Confirm they resolved

List the skills the harness actually picked up, grouped by lane. This matters more than it
sounds: an install that silently failed to register looks exactly like one that worked, and the
first symptom is a slash command that does not exist.

If nothing resolved, the install did not register - say so plainly and point back at the
install step rather than continuing.

### 4. Check the environment

Report a short PASS or ACTION line for each. **Do not fix anything silently.**

- **git** - `git rev-parse --is-inside-work-tree`. If this is not a repo, offer to `git init`
  (ask first).
- **GitHub CLI** - `gh --version`, then `gh auth status`. This is the one that matters most,
  but be precise about what breaks: `start-dev`, `pickup-issue` and `close-issue` **hard-fail**
  without `gh` - there is no issue frontier to read and no PR to open. `to-spec` and
  `to-issues` **degrade** instead, falling back to markdown under `docs/`. Unauthenticated,
  the hard failures surface one at a time during real work instead of once here.
  `gh auth login` is interactive, so the user must run it themselves - suggest they type
  `! gh auth login`.

### 5. Orient and stop

Two lines: which lanes exist, and that `/setup-dev-repo` is next if this is a dev project. Then
stop. Do not start setting up the project.

## Done when

- [ ] Skills are present, either freshly installed or confirmed already there
- [ ] The resolved skills have been listed
- [ ] git and `gh auth` status reported, with a clear action for anything failing
- [ ] The user knows what to run next

## Common mistakes

| Mistake | Fix |
|---|---|
| Reinstalling over an existing set | Check first. Overwriting can drop deliberate local changes. |
| Reporting success without listing what resolved | An install that did not register looks identical to one that did. |
| Silently fixing a failed check | Report it. `gh auth login` is interactive and belongs to the user. |
| Chaining into `setup-dev-repo` | Stop. A failed environment check should surface before anything is built on it. |

## Related skills

- **update-skills** - repo-level. Pulls the newest skills once a set is already installed.
- **setup-dev-repo** - the next step for a dev project.
