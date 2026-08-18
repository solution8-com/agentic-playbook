---
name: verify-feature
description: Live runtime verification of a diff — drive the real app through UI flows, hit the endpoints, inspect the database, and prove behavioral side effects, compiled into one self-contained HTML evidence report with screenshots. Use whenever the user wants a feature verified, tested end-to-end, or proven working ("verify this", "make sure it works", "test the new UI", "can we merge this?" evidence), wants screenshots of new UI in a skimmable report, or says "show me what it looks like" as a feature wraps up.
---

# Verify Feature

End a feature with proof: make the running dev stack match the code under verification, drive
every changed surface — UI, API, database, behavior — and hand over one skimmable HTML file
where every claim carries evidence. Division of labour: assert through accessibility snapshots
and query results (machine-checkable), screenshot for the human — the report carries the pixels
and the tables.

This skill is strictly runtime verification. Pair with `/code-review` for static analysis; do
not fold a review pass in here.

## 0. Wait for CI — only when asked, or when the point is verifying a fresh push

`gh pr checks --watch` (or `gh run watch <id>`) until conclusive. Green → continue. Red → stop
and report the failing job with a link; a verification report of a broken build helps nobody.
Long waits are fine — that's the "monitor, then report" ask.

## 1. Resolve the target

The argument works like `/code-review`'s: a commit, a range, a branch, or an issue number
(resolve the issue to its branch/commits). With no argument: the current branch's diff against
its **merge base with the trunk** — or the session's own edits if the tree is dirty.

Trunk resolution order: the project's `verify-recipe` memory → the branch's `@{upstream}` → the
repo's default branch. State the resolved target and trunk (and which source named the trunk) in
the report summary, so a wrong guess is visible instead of silent.

## 2. Load or discover the recipe

Verification needs project facts no generic procedure can know. Check project memory for a
**`verify-recipe`** entry. If it exists, trust-but-verify the load-bearing parts (is the server
actually on that port?). If not, discover the facts once and **write the memory before
finishing** — that is what makes the second run in any repo cheap:

1. Frontend URL + dev login credentials
2. API base + how to authenticate a scripted call (token endpoint, header shape)
3. Database engine + path/DSN, and how to query it directly
4. How to restart the backend, and whether migrations run at startup
5. Trunk branch for merge-base
6. Screenshot-root or tooling quirks — the Playwright MCP may only write inside its allowed
   roots, often `<repo>/.playwright-mcp`; check them, and note the dir is usually git-ignored
7. Safe test fixtures: users, items, or records that may be mutated and cleaned up

A fact you cannot discover marks its dependent checks **blocked** in the report with the reason —
never silently skipped, and never guessed.

## 3. Preflight

Run the project's *existing* build/typecheck commands (from the recipe or project docs — never
introduce new tooling). Broken build → stop, report everything as blocked; verifying code that
doesn't compile is noise. Passing → one summary row in the report, noting known pre-existing
failures so they aren't rediscovered every run (e.g. "67 errors, all in known stale test files,
0 new").

## 4. Plan the checks

Derive the applicable categories from the diff. The report always shows all four — a category the
diff doesn't touch gets an explicit "n/a — nothing in this diff touches it" row, because a
silently missing section is indistinguishable from a forgotten one.

| Category | What proves it |
|---|---|
| **UI flows** | Drive the changed surfaces like a user; assert via accessibility snapshots; screenshot each state worth showing |
| **Endpoints** | Scripted calls (curl + recipe auth) against every new/changed route — routes are proven by their responses, not by reading the router file |
| **Database** | Direct queries: migrations applied, backfills correct, rows shaped as designed. When the diff contains a migration/backfill, run the **double-restart idempotency check**: snapshot → restart → snapshot → diff must be empty on the second run — that is exactly the bug class that only shows the second time |
| **Behavioral** | Server-side effects driven through API/UI and verified at the persistence layer (before/after) |

Frontend route changes are UI flows (navigate to the route in both states); backend route changes
are endpoint checks. There is no separate "routes" category.

**Behavioral archetypes** — scan the diff for these; each one present becomes an assertion:

1. Rows/records **created** as a side effect (prove the row, with its typed fields)
2. Rows **suppressed** (prove the absence: before/after count with the suppressing condition on)
3. **Gates/flags** (feature switch, kill switch — prove both states, and whether the flip needs a restart)
4. **Permission boundaries** (403/404 for the wrong user, 200 for the right one)
5. **Cascades/cleanup on delete** (dependent rows actually go away)
6. **Idempotency** (repeat the operation; nothing duplicates)

**Negative cases are required where applicable**: each endpoint/behavioral section shows at least
one negative case (authz rejection, validation rejection, flag-off, suppression) or states why
none applies. Positive-only verification is where "it works" lies live.

## 5. Make the stack match the code

Verify what is actually running first (which process, which build, since when) — then restart the
dev stack so it runs the code under verification. Do this autonomously; asking before each restart
would defeat the point of the run. Two guardrails, no exceptions:

- Check the evidence supports the restart before killing anything (right process tree, right port).
- Every state change — restarts, DB writes, flag flips, config edits — goes into the artifact
  ledger (step 7) and surfaces in the report's **State left behind** section.

Watch the startup log for migration output and errors; a restart that fails is a finding, not an
inconvenience.

## 6. Drive and capture

Create a fresh working dir under the OS temp directory (`$TMPDIR`, falling back to `/tmp`, or
`%TEMP%` on Windows): `<tmpdir>/verify-feature-<slug>/`. Screenshots go wherever the browser
tooling's allowed roots dictate (recipe field 6).

Per UI flow, with the Playwright MCP: interact like a user, assert with `browser_snapshot`
(present/absent/labelled, and still-there-after-reload for persistence claims),
`browser_take_screenshot` each state worth showing (numbered: `01-...png`),
`browser_console_messages` once per flow — errors belong in the report even when the flow passed.
For large pages, save snapshots to file and grep them rather than pulling full trees into context.

Endpoints: capture status + the response shape that matters. Database: read-only queries wherever
possible. Behavioral: record the actual rows/counts — when a raw row *is* the proof (a typed
notification row, a 0-count after suppression), it goes in the report verbatim as an evidence
block.

Evidence is **curated**, not transcribed: the report is for a human skimming for confidence; the
full transcript lives in the session. Every planned check appears with a verdict — **pass**,
**fail** (what broke, screenshot the broken state), or **blocked** (why).

## 7. Cleanup contract — hard rule

Behavioral checks require creating data, so track an artifact ledger as you go: every comment,
row, preference change, flag flip, restart — each with how to revert it. Before building the
report, walk the ledger and revert everything: delete test records via the same APIs where
possible, restore changed settings, confirm baselines (e.g. max-id back to its pre-test value).
Deliberate leftovers (a feature flag intentionally left on) are allowed but must be listed in
**State left behind** — the section exists so the next person knows exactly what this run changed
about their environment.

## 8. Build the report

Write `manifest.json` in the working dir, then run the bundled builder — it embeds every
screenshot as base64 so the report is a single self-contained file:

```
python3 "<absolute path to this skill>/scripts/build_report.py" "<workdir>/manifest.json" ".claude/reports/<YYYY-MM-DD>-verify-<slug>.html"
```

Print the absolute path of the report, then try to open it: `open` on macOS, `xdg-open` on Linux,
`start ""` on Windows. If opening fails, say so and move on - the path is the deliverable, not the
window.

**Fixed skeleton, always this order** (the builder renders whatever it's given — the order is this
skill's contract, so every report reads the same way):

1. Summary (verdict + target + trunk + preflight row)
2. UI flows (with screenshots)
3. Endpoints
4. Database
5. Behavioral
6. Observations — non-blocking findings discovered along the way (wrong status codes, missing admin UI, pre-existing quirks)
7. State left behind

### Manifest schema

```json
{
  "title": "Task notifications #6796 — live verification",
  "repo": "platform (apps/cloud)", "branch": "6796-tasks-now", "commit": "bda3d63",
  "base_url": "http://localhost:3000", "date": "2026-08-17",
  "summary": "One short paragraph: what was verified, against which trunk, and the overall verdict. Raw HTML allowed.",
  "flows": [
    {
      "name": "Kill switch OFF — task UI disappears",
      "status": "pass",
      "notes": "What was done and what was asserted (plain text, escaped).",
      "console": "Console errors observed, or empty string.",
      "shots": [ { "path": "/abs/path/01-home-disabled.png", "caption": "What the human should notice." } ]
    }
  ],
  "sections": [
    {
      "name": "Endpoint results",
      "status": "pass",
      "notes": "Intro sentence. Raw HTML allowed here and in table cells: <code>, <span class=\"ok\">, <span class=\"warn\">.",
      "blocks": [
        { "type": "table", "headers": ["Call", "Expected", "Result"], "rows": [["<code>GET /api/x</code>", "403", "<span class=\"ok\">403</span> — message"]] },
        { "type": "evidence", "text": "raw rows / log lines that ARE the proof (escaped, mono)" },
        { "type": "notes", "html": "a follow-up paragraph" }
      ]
    }
  ]
}
```

`status` is `pass` | `fail` | `blocked` | `na` | `notes` (use `notes` for Observations, `na` for
untouched categories). Flows are for screenshot-bearing UI checks; sections for everything else.

Styling comes from the plugin's shared `assets/report.css`, inlined by the builder — so this
report, `review-suite` and `visual-spec` all read as one set.

## 9. Clean up and hand over

Delete the working dir and screenshots (the report embeds its own copies), close the browser, stop
anything you started that the user doesn't need running. If the recipe was discovered this run,
write the `verify-recipe` memory now. Completion: the report file is the only artifact left, and
the final message gives its path plus a one-line verdict per category.
