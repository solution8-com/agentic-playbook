# Error-handling pass

Hunt failure paths that lie: errors swallowed, rejections lost, resources leaked, users shown success while the operation failed. For every candidate the question is concrete — *when this fails, what actually happens?* — and the finding states that consequence, not just the pattern.

## Hunt

- **Swallowed errors.** Empty `catch` blocks; catch-log-continue where the flow cannot meaningfully continue; catches that return a default the caller can't distinguish from success.
- **Lost rejections.** Promises without `await`/`.catch` (fire-and-forget mutations are the classic), `async` callbacks passed where nothing awaits them, `Promise.all` where one failure should not abort the rest (or `allSettled` where it should).
- **Missing failure branches.** Network/IO/DB calls whose error path is simply absent; UI that renders loading→success with no error state; responses assumed `ok` without checking.
- **Cause destruction.** Re-thrown errors that drop the original (`throw new Error("failed")` discarding the caught cause); logs of `err.message` where the stack mattered; generic 500s hiding what broke (while, conversely, internal details leaking into user-facing messages is its own finding).
- **Cleanup on the sad path.** DB clients/transactions released only on success (no `finally`, no rollback), file handles, locks, timers, subscriptions that survive a throw.
- **Trust in partial completion.** Multi-step mutations with no story for step 2 failing after step 1 committed.

## Verify — the false-positive gate

Trace each candidate to its consequence and write it into the evidence: what the user sees, what state is left behind, what the logs show. A deliberate, commented decision to degrade gracefully — or an outer layer that demonstrably catches it — clears the finding; quote the layer that convinced you. "Error handling exists somewhere up the stack" without locating it convinces nobody.

## Severity

Blocker: silent data loss or corruption (failed write reported as success, missing rollback mid-transaction). High: failures invisible to both user and logs; leaked connections/transactions under load. Medium: missing error states, cause-destroying rethrows, fire-and-forget of consequence. Low: log-quality nits.

## Report

Return the JSON findings array per the schema in your dispatch prompt. `evidence` states the traced consequence; `recommendation` names the handling that belongs there (surface, retry, rollback, error state) — matching how the repo's healthy paths already do it.
