---
name: pickup-issue
description: Load one issue's context and set up its workspace, then hand to /implement. Use when the user names an issue to work on ("pick up #12", "let's do issue 40", "start on the auth one"), or points at an issue URL and wants work to begin.
---

Get the context and the workspace right, then hand over. This skill writes no code and no plan - the issue already is the plan.

**Read the issue**: `gh issue view <N> --comments`. The comments are not optional - decisions get made in threads and never make it back into the body, so a body-only read builds the wrong thing confidently. If the issue references a parent, a spec, or a blocking issue, read those too.

**Ask only what is unclear in the issue itself** - what to build, what done means, where the scope stops. Implementation approach is `/implement`'s job, and asking about it invites redesigning work that was already settled. If the issue is clear, say so in one line and keep going.

**Resolve the workspace.** Worktrees are what stop parallel sessions corrupting each other - two builds in one checkout share an index and a HEAD, and the failures are ugly. Nothing in progress: `git worktree add ../<repo>-<slug> -b <branch>`. A related issue in the same area with a clean tree: reuse the tree, sequentially - never two issues in flight in one tree. Sibling issues worth taking together: name them and let the user confirm. Branch off the default branch, merge back when the work lands, no draft PR. One caveat: `refs/stash` is shared across worktrees, so prefer a commit on the branch over a stash.

**Hand off**: state the issue number, the branch and the worktree path in one line, then invoke `/implement`.
