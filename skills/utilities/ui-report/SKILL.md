---
name: ui-report
description: Build an end-of-session UI screenshot report — optionally wait for CI to go green, drive Playwright through the flows this session changed, and deliver one self-contained HTML report with embedded screenshots, deleting all working artifacts afterward. Use when the user wants screenshots of new UI in a skimmable report, says "show me what it looks like", or asks to verify the UI and capture the result as a feature wraps up.
---

# UI Report

End a feature session with proof: drive the app through what changed, screenshot each state, and hand over one skimmable HTML file. Division of labour: image responses are omitted in this setup, so **assert through accessibility snapshots** (`browser_snapshot`) — the screenshots are for the human, and the report carries the pixels.

## 0. Wait for CI — only when asked, or when the point is verifying a fresh push

`gh pr checks --watch` (or `gh run watch <id>`) until conclusive. Green → continue. Red → stop and report the failing job with a link; a UI report of a broken build helps nobody. Long waits are fine — that's the "monitor, then report" ask.

## 1. Resolve the target

First match wins:

1. A URL the user gave — deployed site or PR preview environment (post-CI runs usually want the preview URL the workflow emitted; find it in the PR checks/comments).
2. A dev server already running — probe the project's documented port (its CLAUDE.md/AGENTS.md or run skill names it).
3. Start one yourself the way the project documents (its own run/dev skill or package scripts), in the background. Remember that you started it — cleanup stops it.

Flows behind login use the dev credentials the project documents (`.env.local`, docs). A flow you can't reach is reported as **blocked** with the reason — every planned flow appears in the report with a verdict; silently dropping one hides exactly what the user asked to see.

## 2. Plan the flows

Derive what changed this session: `git diff <trunk>...HEAD --stat` (or the session's own edits) → changed routes/components → the user-visible flows they belong to. Completion criterion for the plan: every changed surface appears in at least one flow. State the flow list to the user in one line and proceed; pause for confirmation only when the diff-to-flow mapping is genuinely ambiguous.

## 3. Drive and capture

Create a fresh working dir under the OS temp directory (`$TMPDIR`, falling back to `/tmp`, or `%TEMP%` on Windows): `<tmpdir>/ui-report-<slug>/`. Per flow, with the Playwright MCP:

- Navigate and interact through the flow like a user would (fill the form, submit, toggle the thing).
- Assert with `browser_snapshot`: the element/chip/row is present, absent, or correctly labelled — and for persistence claims, still there after a reload. Snapshot at assertion points, not after every step.
- `browser_take_screenshot` each state worth showing, `filename` inside the working dir, numbered for order: `01-dashboard-empty.png`, `02-dashboard-added.png`. Note the actual saved path from the tool result.
- `browser_console_messages` once per flow — errors belong in the report even when the flow passed.
- Record the verdict: **pass** (assertions held), **fail** (what broke — screenshot the broken state too), **blocked** (why).

## 4. Build the report

Write `manifest.json` in the working dir, then run the bundled builder — it embeds every screenshot as base64 so the report is a single self-contained file:

```
python3 "<absolute path to this skill>/scripts/build_report.py" "<workdir>/manifest.json" ".claude/reports/<YYYY-MM-DD>-ui-report-<slug>.html"
```

Print the absolute path of the report, then try to open it: `open` on macOS, `xdg-open` on Linux, `start ""` on Windows. If opening fails, say so and move on - the path is the deliverable, not the window.

### Manifest schema

```json
{
  "title": "Onboarding assessment UI",
  "repo": "learn-wings", "branch": "feat/x", "commit": "abc1234",
  "base_url": "http://localhost:8080", "date": "2026-07-24",
  "summary": "One short paragraph: what shipped and the overall verdict.",
  "flows": [
    {
      "name": "Create assessment",
      "status": "pass",
      "notes": "What was done and what was asserted (snapshot checks).",
      "console": "Console errors observed, or empty string.",
      "shots": [
        { "path": "C:\\...\\01-form-empty.png", "caption": "What this state shows." }
      ]
    }
  ]
}
```

`status` is `pass` | `fail` | `blocked`. Captions say what the human should notice, not what Playwright did.

## 5. Clean up

Delete the working dir (screenshots and manifest — the report has its own embedded copies), `browser_close`, and stop any dev server you started. Completion: the report file is the only artifact left, and your final message gives its path plus a one-line verdict per flow.
