---
name: pickup-issue
description: Load one issue's context and set up its workspace, then hand to /implement. Use when the user names an issue to work on ("pick up #12", "let's do issue 40", "start on the auth one"), or points at an issue URL and wants work to begin.
---

# Pick up an issue

Get the context and the workspace right, then hand over. **This skill does not write code.**

## 1. Read the issue

```
gh issue view <N> --comments
```

Read the body **and the comments**. Decisions get made in comment threads and never make it back into the body, so a body-only read will build the wrong thing confidently.

If the issue references a parent, a spec, or a blocking issue, read those too.

## 2. Ask what is unclear

Ask only about ambiguity **in the issue itself**: what to build, what done means, where the scope stops.

Do not ask about implementation approach - that is `/implement`'s job, and asking invites a redesign of work that was already settled. Do not re-open decisions the issue records as made.

If the issue is clear, say so in one line and keep going. No ceremony.

## 3. Resolve the workspace

Worktrees are what stop parallel sessions from corrupting each other. Two builds in one checkout share an index and a HEAD, and the failures are ugly: a commit amended onto another session's work, a stash that disappears.

- **Nothing in progress** - create one:
  `git worktree add ../<repo>-<slug> -b <branch>`
- **A related issue, same area, current tree clean** - reuse the tree, **sequentially**. Finish one issue, then start the next. Never two issues in flight in one tree.
- **Grouping** - if sibling issues look worth taking together, name them and let the user confirm. Do not decide it silently.

Branch off the default branch and merge the branch back when the work lands. No draft PR.

**Caveat worth knowing:** `refs/stash` is shared across worktrees, so a `git stash` in one shows up in all of them. Prefer a commit on the branch over a stash.

## 4. Hand off

State the issue number, the branch and the worktree path in one line, then invoke `/implement`.
