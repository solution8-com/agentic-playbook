---
name: implement
description: "Implement a piece of work based on a spec or set of tickets. Use when work arrives from /pickup-issue, or when the user asks to implement or build something already specced in a ticket."
---

Implement the work described by the user in the spec or tickets.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use `/code-review low` to check the work does what the ticket asked - and name
the target explicitly: the branch or worktree path where this work actually lives. Review
sub-agents inherit the session's working directory, not the builder's worktree, so an
untargeted review can pass without ever seeing the diff. A review that saw no diff is not a
review.

Do not run a deep review here. An agent reviewing code it just wrote is biased toward its own solution, so the deep pass belongs in a fresh session against a fixed point.

Then check what the diff touched. **If it touched UI, an endpoint or the database, run
`/verify-feature`** - dispatch it to a sub-agent with a clean context, handing it the branch or
worktree path as its brief and nothing else. Not inline: the same bias that keeps the deep review
out of this session applies harder to verification, where the agent also chooses which flows to
drive and which assertions to make. Evidence written by the context that wrote the code is worth
less than evidence written by one that has never seen it. Report the path of the report it
returns; do not summarise its verdict in place of it.

**Where the diff touched none of those three, skip it and say so in one line.** A pure refactor
produces a report of nothing-applicable rows, and an artifact per commit that proves nothing
trains people to stop opening them.

Commit your work to the current branch, then stop: report the branch and hand it to the user to review and merge. Do not merge it yourself unless the user has said to for this work - an issue labelled `afk` counts as that permission.
