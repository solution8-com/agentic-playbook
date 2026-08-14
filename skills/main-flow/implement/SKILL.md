---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use `/code-review low` to check the work does what the ticket asked.

Do not run a deep review here. An agent reviewing code it just wrote is biased toward its own solution, so the deep pass belongs in a fresh session against a fixed point.

Commit your work to the current branch.
