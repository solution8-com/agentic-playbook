# Adversarial check generators

Loaded from step 4 when the run is adversarial. Each **generator** takes the diff and stamps out
concrete checks: read the diff with the generator in mind, enumerate the axis it names (states,
roles, pointers, fields), and turn each instance into a planned check with its own verdict row. A
generator whose axis is absent from the diff yields one explicit n/a row. That is the same rule as
the four categories: a missing section must stay distinguishable from a forgotten one.

Two rules govern the whole file.

**The collapse rule.** Matrices multiply. Four deadline variants by four transitions by four
surfaces is 64 cells, and most cells cannot fail on their own, because only one code path reads
both axes. Walk each axis in full at one representative point of the other axes, then add
interaction cells only where the code gives a reason. A handler that reads both axes is such a
reason: reopening a past-deadline task resets the notification markers, which couples transition
and deadline. Name the chosen interaction cells and their reasons in the plan. Rigor shows in
which cells you chose, not in how many.

**Prove the negative at the layer below.** A rejection seen at the surface (403, a hidden button,
an error toast) is half a check. The other half sits at the persistence layer: the denied create
left no row, the failed transition left the old state, the aborted send left no outbox entry.
Wherever a generator rejects something, follow with the absence query.

## 1. State-matrix walk

Recover the entity's state machine from the diff: the status enum, and every handler that writes
it. Walk every legal transition, forward and backward. The backward ones (reopen, undo,
un-archive) are where the reset bugs live, because the arming fields (notification markers,
sent-at timestamps, counters) must rewind and rarely do. After each transition, assert the new
state at the database and at the surfaces of generator 2. Attempt each illegal transition through
the API: it must be rejected, and it must leave no side effect.

## 2. Live-update and reload consistency

After every mutation, every surface derived from the changed data must update without a refetch:
list sections, "Showing X of Y" counters, badges, KPI tiles, parent-page rows. Then hard-reload
once per flow and assert that the refetched state agrees with what the live updates showed. Drift
between live and refetch means one of the two paths computes it wrong, and the reload tells you
which world the database believes.

## 3. Permission matrix

Build the grid: the roles from recipe field 8 (admin, plain member or assignee, unrelated user,
cross-org where the app is multi-tenant) against every operation the diff adds or changes, with
the expected allow or deny for each cell. Denials are dual-surface. The API rejects (403 or 404,
per project convention) **and** the UI affordance is absent. An open API behind a hidden button is
the exploitable half. A visible button that returns 403 is the broken half. Assert both. Apply the
negative-proof rule to every denied write.

## 4. Dangling-pointer sweep

For every entity the diff lets you delete, or hide behind a permission, enumerate every place a
pointer to it survives: links on other pages, notification links, embedded references in stored
bodies, cached lists, browser history. Probe each pointer after the delete. Look for a designed
terminal state (a tombstone, a "no longer available" page, a redirect), for focus that lands
somewhere usable, and, where the pointer crosses a permission boundary, for a payload that carries
no field of the hidden thing: no label, and no id in the tombstone JSON. Read the response body,
not the rendered DOM. Deleted-target and access-denied are two different designed states. Assert
that they stay distinguishable.

## 5. Input-abuse kit

Stamp these onto every new or changed endpoint and search field, through direct API calls:

- Wrong-type and malformed values in each field. Expect 400, never 500.
- LIKE metacharacters `%` and `_`, and quotes, in search. Expect literals, never a full-bucket match.
- Oversized collections, such as a 50-element array where the UI sends 3. Expect a bound and a 400.
- Offset and limit set negative, zero, and huge. Expect clamping, and stable results.
- Another org's or another bucket's id in every id-shaped field. Expect 403 or 404, not 500, and no data.
- Markup and template syntax in stored text, such as `<img onerror=...>` or a literal `{{ref:...}}`
  typed by hand. Expect verbatim storage, inert rendering, and survival of an edit round-trip.
- Very long strings, and multibyte or emoji text. Expect acceptance or a clean rejection, with no
  truncation surprise after a reload.

## 6. Failure injection

Stop the backend mid-session. Recipe field 4 says how, and project memory may record deeper
fault-injection levers. Every changed surface must degrade to an explicit designed state, such as
a retry panel or a "could not load" row, and a failed submit must re-enable the composer with the
draft intact. An eternal spinner or a swallowed draft is a fail. Restart, retry, and assert the
recovery. Where you can, also kill the backend between submit and response, which is the
half-committed window.

## 7. Fix-phase regression re-checks

The bugs fixed while this feature was built are its most likely regressions. Each one marks a spot
where the design was wrong once. Collect them from the branch's commit subjects, the issue thread
and the session, then re-run each original reproduction exactly, one row for each.

## 8. Empty and zero states

Take a user with zero data: every new surface must render its designed empty state, not a
skeleton, not a crash, and not stale demo data. Then turn the feature's org or tenant flag off:
dual-surface again, the UI absent **and** the API rejecting. A flag that only hides the button is
a permission bug in a CSS costume.

## 9. Concurrency probes

Double-click every submit that creates something: exactly one row. Work the same record from two
sessions: the second write's outcome is whatever the design says, last-write-wins or a conflict,
but never a torn merge of both. A mutation from session A must reach session B's display by that
surface's designed mechanism, whether that is a live update, a poll, or the next navigation.

## 10. Pagination under mutation

With a paginated list open on page 1, delete or insert an item inside that window, then fetch page
2: no skipped rows, and no duplicated rows. Offset pagination shifts under mutation, and this
two-call check is what catches it.

## 11. Clock edges

Where the diff gives a date its meaning ("today", "overdue", "upcoming"), assert the
classification at the boundary: a deadline of today just before and just after the cutoff, and a
client timezone ahead of the server's. The database stores one instant. The label must follow the
project's declared timezone rule, not whichever machine the browser runs on.

## 12. Exactly-once side effects

Where the diff arms or resets notification, email or webhook state, the marker columns are half
the story. After re-arming, by reopening a done task or re-triggering the condition, prove the
effect fires exactly once: one new row in the outbox or log. Zero means the reset never happened.
Two means the reset armed it twice.

## Reporting the matrix

Emit each generator's results as a `checks` JSON block, with `{name, ok, detail}` rows, so the
builder renders and tallies them. A matrix hand-transcribed into prose is where cells quietly go
missing. A cell that reproduces a known-accepted finding carries `"accepted": true`, with the
deferral pointer in `detail`. The plan's chosen interaction cells appear even when they pass, and
the collapse rule's decisions go in the section notes ("deadline variants walked at one
transition; interaction cells: reopen by past-deadline"), so the coverage is auditable rather than
asserted.
