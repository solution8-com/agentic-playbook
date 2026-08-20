---
name: handoff
description: Compact the current conversation into a handoff document a fresh session can pick up from. Use at the end of a working session, when the context nears its edge, or when the user asks to wrap up or hand over.
argument-hint: "What will the next session be used for?"
---

# Handoff

Write a handoff document so a fresh agent can continue this work without re-deriving it.

**Save it to the OS temporary directory (`$TMPDIR`), never into the workspace.** A handoff is
scaffolding for the next session, not a document the repo has to maintain. Name it
`handoff-<repo-or-project>-YYYY-MM-DD.md` and state the full path when you are done.

## What goes in

- **Where the work stands** - what landed, what is half-done, what is blocked and on what.
- **What the next session should do first**, in order.
- **Decisions made in conversation that live nowhere else.** This is the load-bearing part. A
  decision settled out loud and never written down is the only thing a fresh agent genuinely
  cannot recover.
- **Suggested skills** - name the skills the next session should reach for, and where it
  re-enters the flow: idea-first (`grill-me` → `to-spec` → `to-issues` → `pickup-issue` →
  `implement`) or issue-first (`pickup-issue` → `grill-me` → `implement`).

## What stays out

**Do not duplicate anything already captured somewhere durable** - specs, plans, issues, commits,
diffs, ADRs. Reference them by path, issue number or URL instead. The tracker and the git history
are the project's memory; this document exists only for what they do not hold.

Skip anything the next agent can read off the code in less time than it takes to read your summary
of it.

## Before you save

Redact secrets - API keys, tokens, passwords, personal data. A handoff gets pasted around.

If the user passed an argument, treat it as what the next session will focus on and cut everything
that does not serve it.
