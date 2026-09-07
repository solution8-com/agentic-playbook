# Verify Feature - procedure

The full runtime verification procedure. `SKILL.md` dispatches a subagent here, and this file is
what that subagent follows. Already running as a subagent? This is your procedure. Work it top to
bottom, and work it autonomously. The two guardrails in step 5 are the only checks that gate an
action, and the parent audits your receipt (step 11) at the end.

## The contract

End a feature with proof: make the running dev stack match the code under verification, drive
every changed surface (UI, API, database, behavior) and hand over one skimmable HTML file where
every claim carries evidence. Division of labour: assert through accessibility snapshots and query
results, which a machine can check, and screenshot for the human. The report carries the pixels
and the tables.

This procedure is strictly runtime verification. Pair it with `/code-review` for static analysis.
Do not fold a review pass in here.

## 0. Wait for CI, only when asked, or when the point is verifying a fresh push

`gh pr checks --watch` (or `gh run watch <id>`) until conclusive. Green, continue. Red, stop and
report the failing job with a link. A verification report of a broken build helps nobody. Long
waits are fine, because "monitor, then report" is the ask.

## 1. Resolve the target

The argument works like `/code-review`'s: a commit, a range, a branch, or an issue number (resolve
the issue to its branch and commits). With no argument, the target is the current branch's diff
against its **merge base with the trunk**, or the session's own edits if the tree is dirty.

Trunk resolution order: the project's `verify-recipe` memory, then the branch's `@{upstream}`,
then the repo's default branch. State the resolved target and trunk in the report summary, and say
which source named the trunk, so a wrong guess is visible instead of silent.

## 2. Load or discover the recipe

Verification needs project facts that no generic procedure can know. Check project memory for a
**`verify-recipe`** entry. If it exists, trust the entry but verify the load-bearing parts. Is the
server actually on that port? If it does not exist, discover the facts once and **write the memory
before you finish**. That is what makes the second run in any repo cheap:

1. Frontend URL and dev login credentials.
2. API base, and how to authenticate a scripted call: the token endpoint, and the header shape.
3. Database engine, path or DSN, and how to query it directly.
4. How to restart the backend: what must be killed, whether that is a watcher or the full process
   tree where there is no hot reload, and whether migrations run at startup.
5. The trunk branch, for the merge base.
6. Screenshot-root and tooling quirks. The Playwright MCP may only write inside its allowed roots,
   often `<repo>/.playwright-mcp`. Check them, and note that the directory is usually git-ignored.
7. Safe test fixtures: users, items or records that you may mutate and clean up.
8. **Permission-role fixtures**: one login per role the app distinguishes (admin, plain member,
   unrelated user, and cross-org where the app is multi-tenant), and how to mint a session or an
   API token as each. The permission matrix is only as complete as this roster, so a missing role
   blocks its own checks rather than quietly narrowing the run.

A fact you cannot discover marks its dependent checks **blocked** in the report, with the reason.
Never skip it silently, and never guess it.

Beside the recipe, check for a **`verify-invariants`** memory: the project-wide behavioral
contracts that outlive any one feature, such as "every mutation updates the dependent surfaces
without a refetch", or "a denial hides the affordance and rejects the API call". Every invariant
the diff touches becomes a planned assertion, at either depth. When a run surfaces a new contract
of this kind, a rule the team clearly holds that no single feature owns, grow the memory the same
way the recipe grows.

The third memory is feature-scoped: a **`verify-contracts`** register, which holds the
verification knowledge that no generic generator can re-derive cheaply at run time. Each entry
covers one feature area and carries three things:

1. The trigger paths and symbols, meaning the files that implement the area.
2. The matrix and invariant rows to assert whenever those files change: coercion tables, lifecycle
   rules, and "X is structurally absent from Y" invariants.
3. Pointers to that area's known-accepted deferrals.

The register exists because this knowledge is cheap exactly once, at review or scoping time, when
the findings are already in context. A later run either reads it from the register, or pays to
rediscover it, or worse, never walks it at all. The growth rule mirrors the recipe's: when a run,
or the scoping or review session that commissions one, surfaces feature-specific matrices, write
or extend the register entry before you finish. Then the next run detects them, instead of
depending on whoever writes the prompt to remember them.

## 3. Preflight

Run the project's *existing* build and typecheck commands, from the recipe or the project docs.
Never introduce new tooling. A broken build stops the run: report everything as blocked, because
verifying code that does not compile is noise. A passing build gets one summary row in the report,
which names the known pre-existing failures so that nobody rediscovers them every run. For
example: "67 errors, all in known stale test files, 0 new".

## 4. Plan the checks

Derive the applicable categories from the diff. The report always shows all four. A category the
diff does not touch gets an explicit "n/a, nothing in this diff touches it" row, because a
silently missing section is indistinguishable from a forgotten one.

| Category | What proves it |
|---|---|
| **UI flows** | Drive the changed surfaces like a user, assert through accessibility snapshots, and screenshot each state worth showing |
| **Endpoints** | Scripted calls (curl plus the recipe's auth) against every new or changed route. A route is proven by its response, not by a reading of the router file |
| **Database** | Direct queries: migrations applied, backfills correct, rows shaped as designed. Where the diff contains a migration or a backfill, run the **double-restart idempotency check**: snapshot, restart, snapshot, and the second diff must be empty. That is exactly the bug class that only shows the second time |
| **Behavioral** | Server-side effects driven through the API or the UI, and verified at the persistence layer, before and after |

A frontend route change is a UI flow: navigate to the route in both states. A backend route change
is an endpoint check. There is no separate "routes" category.

**Behavioral archetypes.** Scan the diff for these. Each one present becomes an assertion:

1. Rows or records **created** as a side effect. Prove the row, with its typed fields.
2. Rows **suppressed**. Prove the absence: a before and after count, with the suppressing
   condition on.
3. **Gates and flags**, such as a feature switch or a kill switch. Prove both states, and prove
   whether the flip needs a restart.
4. **Permission boundaries**: 403 or 404 for the wrong user, 200 for the right one.
5. **Cascades and cleanup on delete**: the dependent rows actually go away.
6. **Idempotency**: repeat the operation, and nothing duplicates.

**Negative cases are required where they apply.** Each endpoint and behavioral section shows at
least one negative case, whether that is an authz rejection, a validation rejection, a flag-off
state or a suppression, or it states why none applies. Positive-only verification is where "it
works" lies live.

**Contract detection.** Before you choose the depth, match the diff's changed files against each
`verify-contracts` entry's trigger paths. Every matched entry's assertion rows join the planned
checks, at whichever depth runs, and the report summary names the contracts that matched, or
states that none did. A stale trigger glob then shows up as a visible mismatch instead of a silent
skip.

**Two depths.** The default depth is everything above, the archetypes plus the required negatives,
and it fits a normal feature diff. When the request asks for it ("adversarial", "walk the
matrices", "try to break it"), or when the diff covers a whole feature rather than a patch, read
[`adversarial.md`](adversarial.md), beside this file, before you plan. Its check **generators**
(the state-matrix walk, the permission matrix, the dangling-pointer sweep, the input-abuse kit,
failure injection, and more) expand the diff into a full adversarial plan, and its collapse rule
keeps the matrices from going combinatorial. Adversarial runs cost hours, not minutes, so the dial
belongs to the user. At default depth, say when a diff looks like it deserves the deeper run.

**Known-accepted findings.** Before you drive, collect the deviations that somebody already ruled
on: deferred issues named in the request, "known, accepted" notes on the issue thread, the
Accepted pointers of any matched `verify-contracts` entries, and an accepted register in the
`verify-invariants` memory. A check that reproduces one gets the status `accepted`, with a pointer
to where it was deferred. It is never a `fail`, which re-litigates a settled decision, and it is
never a silent skip, which loses the evidence that the behavior is still present.

## 5. Make the stack match the code

Verify what is actually running first: which process, which build, and since when. Then restart
the dev stack so that it runs the code under verification. Do this autonomously, because asking
before each restart would defeat the point of the run. Two guardrails, with no exceptions:

- Check that the evidence supports the restart before you kill anything: the right process tree,
  and the right port.
- Every state change goes into the artifact ledger of step 8 and surfaces in the report's **State
  left behind** section. That covers restarts, database writes, flag flips and config edits.

Watch the startup log for migration output and for errors. A restart that fails is a finding, not
an inconvenience.

## 6. Drive and capture

Create a working directory for the manifest. Screenshots go wherever the browser tooling's allowed
roots dictate, which is recipe field 6. For each UI flow, with the Playwright MCP: interact like a
user, assert with `browser_snapshot` (present, absent, labelled, and still there after a reload
for any persistence claim), take a `browser_take_screenshot` of each state worth showing, numbered
`01-...png`, and read `browser_console_messages` once per flow. Errors belong in the report even
when the flow passed. For large pages, save the snapshots to file and grep them, rather than
pulling full trees into context.

Two captures cost nothing at drive time and pay off in the report, so do them by default:

- **Mark the load-bearing region.** When a caption would say "notice the X", record X's
  `getBoundingClientRect()` in the same evaluate that asserts it, and emit it as `marks` on the
  shot. For viewport screenshots at deviceScaleFactor 1, CSS px equals image px. For full-page
  screenshots, add `scrollY` to `y`. The builder draws clay callout boxes on the image, so the
  evidence points at itself instead of relying on prose.
- **Capture state changes as flip pairs.** When a check is two states of the same screen, such as
  before and after a save, or a flag on and off, screenshot both at the same scroll position and
  emit them as one `flip` shot instead of two figures. The reader toggles them in place, and the
  change pops.

Endpoints: capture the status and the response shape that matters. Database: use read-only queries
wherever you can. Behavioral: record the actual rows and counts. Where a raw row *is* the proof, a
typed notification row or a zero count after suppression, it goes into the report verbatim as an
evidence block.

Evidence is **curated**, not transcribed. The report is for a human who skims for confidence, and
the full transcript lives in the session. Every planned check appears with a verdict: **pass**,
**fail** (say what broke, and screenshot the broken state), or **blocked** (say why).

## 7. Fix mode, only when the request says fix

The default contract is measure and report: fails get evidence, and the code stays untouched. When
the request says fix until green, and it will usually name a branch, the contract changes:

- Fix on the named branch, in the project's commit style, and keep each fix scoped to the failing
  check's cause.
- After every fix, make the stack match the code again (step 5). Where the recipe says there is no
  hot reload, that means the full restart. Then re-run the failed check **and every green check
  the fix could plausibly reach**. A fix that breaks a neighbour must be caught by this run, not
  by the next person.
- The report tells the true story. A fixed check's notes read `fail -> fixed in <commit> -> pass`.
  First-pass green and fixed-then-green carry different risk, and flattening them into one "pass"
  hides exactly what a reviewer needs.
- A fix that grows past the feature's own boundary, such as schema rework or a refactor of a
  neighbouring subsystem, is a finding, not a task. Mark the check `fail`, record the boundary in
  Observations, and leave the decision to the user.

## 8. Cleanup contract, a hard rule

Behavioral checks require creating data, so track an artifact ledger as you go. Every comment,
row, preference change, flag flip and restart goes in it, each with how to revert it. Before you
build the report, walk the ledger and revert everything: delete the test records through the same
APIs where you can, restore the changed settings, and confirm the baselines, such as a max-id back
at its pre-test value. Deliberate leftovers are allowed, a feature flag left on for a reason, but
they must appear in **State left behind**. That section exists so that the next person knows
exactly what this run changed about their environment.

## 9. Build the report

Write `manifest.json` in the working directory, then run the bundled builder. It embeds every
screenshot as base64, so the report is one self-contained file:

```
python3 "<absolute path to this skill>/scripts/build_report.py" "<workdir>/manifest.json" "<the report path from your brief>"
```

Where the brief names no report path, use `.claude/reports/<YYYY-MM-DD>-verify-<slug>.html` inside
the repo, or the report directory the project's own docs name.

Open the result. The skeleton is fixed, always in this order. The builder renders whatever it is
given, so the order is this skill's contract, and every report then reads the same way:

1. Summary: the verdict, the target, the trunk, and the preflight row.
2. UI flows, with screenshots.
3. Endpoints.
4. Database.
5. Behavioral.
6. Observations: the non-blocking findings you found along the way, such as a wrong status code, a
   missing admin UI, or a pre-existing quirk.
7. State left behind.

### Manifest schema

```json
{
  "title": "Task notifications #6796 - live verification",
  "repo": "platform (apps/cloud)", "branch": "6796-tasks-now", "commit": "bda3d63",
  "base_url": "http://localhost:3000", "date": "2026-08-17",
  "summary": "One short paragraph: what was verified, against which trunk, and the overall verdict. Raw HTML allowed.",
  "flows": [
    {
      "name": "Kill switch OFF - task UI disappears",
      "status": "pass",
      "notes": "What was done and what was asserted (plain text, escaped).",
      "console": "Console errors observed, or empty string.",
      "shots": [
        { "path": "01-home-disabled.png", "caption": "What the human should notice.",
          "marks": [ { "x": 840, "y": 312, "w": 180, "h": 44, "label": "chip preserved" } ] },
        { "caption": "One flip figure, toggled in place by the reader.",
          "flip": [ { "path": "02-before.png", "label": "Before", "marks": [] },
                    { "path": "03-after.png", "label": "After" } ] }
      ]
    }
  ],
  "sections": [
    {
      "name": "Endpoint results",
      "status": "pass",
      "notes": "Intro sentence. Raw HTML allowed here and in table cells: <code>, <span class=\"ok\">, <span class=\"warn\">.",
      "blocks": [
        { "type": "table", "headers": ["Call", "Expected", "Result"], "rows": [["<code>GET /api/x</code>", "403", "<span class=\"ok\">403</span> - message"]] },
        { "type": "checks", "path": "api_results.json" },
        { "type": "evidence", "text": "raw rows or log lines that ARE the proof (escaped, mono)" },
        { "type": "notes", "html": "a follow-up paragraph" }
      ]
    }
  ]
}
```

`status` is `pass`, `fail`, `blocked`, `na`, `notes`, `accepted` or `auto`. Use `notes` for
Observations, `na` for an untouched category, and `accepted` for a reproduced known-accepted
finding, which renders muted and stays out of the overall verdict. `auto` derives the status from
the section's `checks` blocks: any hard failure makes it a fail, otherwise it passes. Flows are for
the screenshot-bearing UI checks, and sections are for everything else.

**Prefer `checks` over a hand-transcribed table** when a verify script already emitted results.
Have the script write `{ "results": [ { "name", "ok", "detail" } ] }`, or a bare list, to a JSON
file in the working directory, and reference it with `{ "type": "checks", "path": "..." }`, which
is manifest-relative. The builder renders the pass and fail table and the tally itself, so the
report cannot drift from what the checks actually said. A check row may also carry
`"accepted": true`, which renders as ACCEPTED with the deferral pointer in `detail` and stays out
of the fail tally. Keep hand-authored `table` blocks for curated views, the expected-against-actual
ones with prose. Use `marks` in the natural PNG pixels of the screenshot file.

The builder adds the interactivity on its own: a verdict strip with jump chips and an overall
verdict, pass sections collapsed while fail and blocked stay open, a lightbox with wheel zoom,
drag pan and double-click 1:1, flip toggles, mark overlays, and a Copy-as-markdown button that
exports the whole report for GitHub. There is nothing to author for these beyond the fields above.

## 10. Clean up and hand over

Delete the working directory and the screenshots, because the report embeds its own copies. Close
the browser, and stop anything you started that the user does not need running. If you discovered
the recipe this run, write the `verify-recipe` memory now. You are done when the report file is
the only artifact left.

## 11. The receipt

The parent keeps its context small on purpose and will never open the report, so your final
message is a **receipt**, not a transcript. Send these rows, then stop:

- The absolute path of the HTML report.
- One verdict line per category: UI flows, Endpoints, Database, Behavioral.
- Every `fail` and every `blocked` check, one sentence each.
- Every `accepted` check, with the pointer to where it was deferred.
- The **State left behind** list.
- The commit SHAs, after a fix-mode run.
- The memories you wrote or extended: `verify-recipe`, `verify-invariants`, `verify-contracts`.
