---
name: update-skills
description: Update this repo's S8 playbook skills to the newest version on GitHub, showing what changed before applying it.
disable-model-invocation: true
---

# Update Skills

## Overview

Skills install per repo, which means a project keeps whatever version it was set up with. That
is deliberate - a client repo from last year still behaves the way it did. The cost is that
improvements do not arrive on their own. This is how you pull them in, deliberately, on a repo
you are actively working in.

Being available at all tells you the skills are installed. If they are not, `setup-skills` is
what you want instead.

## Process

Installed skills carry no version stamp, so there is nothing to compare version numbers
against. Compare **contents** instead, in three directions, and let the repo's own git history
supply the baseline.

1. **Fetch upstream to a scratch directory.** Do not install over the live set yet. Get the
   current `main` somewhere you can read it without changing anything.

2. **Find the baseline.** The commit that installed or last updated the skills is the last bulk
   change to the skills directory:

   ```
   git log --oneline -- <skills-dir>
   ```

   Everything committed to those paths *after* it is a local edit. Uncommitted working-tree
   changes to skill files count too, and are the easiest to lose.

3. **Diff three ways, and keep the results separate.** They mean different things and must not
   be merged into one list:

   | Comparison | Tells you |
   |---|---|
   | upstream vs baseline | What the update actually brings |
   | local vs baseline | What someone changed **here**, deliberately |
   | upstream vs local | The raw overwrite, which conflates the two above |

   A skill that appears in both the first and second column is a **conflict**: the update and a
   local edit both touch it, and applying blind loses the local one.

4. **Show it before touching anything.** One line per skill is enough for the routine cases;
   the point is that the user sees the shape of the change. Conflicts and local edits get
   named individually, because those are the ones with something to lose.

5. **Ask before applying.** Updating changes how the agent behaves, including on work already
   in flight, so this is a decision rather than a formality. If there are local edits, ask
   about those specifically - "update everything" and "update everything except the two skills
   this repo customised" are different answers.

6. **Apply.**
   ```
   npx skills add solution8-com/INT-s8-agentic-playbook
   ```

   This overwrites. Anything reported in step 3 as a local edit and not explicitly agreed to is
   about to be lost, so re-apply those on top afterwards, or do not run the install at all.

7. **Report what moved**, and flag anything that changes an in-progress workflow - a renamed
   skill, a removed one, a changed gate.

## When not to run this

- **Mid-task.** Finish what is in flight first. Changing the tooling under a running workflow
  is how you get a failure that looks like a bug in your work.
- **On a repo you are only visiting.** If you are reading a client codebase rather than
  building in it, its skills can stay where they are.

## Common mistakes

| Mistake | Fix |
|---|---|
| Updating without showing the diff | The user cannot consent to a change they have not seen. |
| Showing only what upstream added | That is half the diff. It says nothing about the local edits about to be overwritten. |
| Applying over an uncommitted skill change | Working-tree edits have no git baseline to recover from. Commit or stash first. |
| Updating mid-task | Finish first. New rules mid-flight look like bugs. |
| Treating it as routine maintenance | Old repos keeping old skills is the point of per-repo install, not a problem to sweep away. |

## Related skills

- **setup-skills** - global. Installs the skills when a repo has none.
