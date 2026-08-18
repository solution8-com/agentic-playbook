# Docs-drift pass

Hunt documentation that claims to describe current state but no longer does. The governing policy: docs describing current state stay true or get deleted — git history is the archive, so "outdated, see X" markers and stale sections are findings, not features.

## Hunt

1. **Inventory the docs in scope** that make current-state claims: READMEs, CLAUDE.md/AGENTS.md, `docs/` guides, setup/run instructions, inline architecture notes, API descriptions. Exclude append-only records by design — ADRs, changelogs, worklogs — and clearly-dated plans (though a *consumed* plan still lying around is itself a finding under the ephemeral-docs policy).
2. **Extract the checkable claims** from each: commands and scripts, paths, ports, env var names, endpoints and their shapes, described behaviours and flows, technology names ("we use X for Y"), counts ("~100 functions").
3. **Verify each claim against the code**, cheapest check first: does the file/path exist, is the script in `package.json`, does the env var appear in the code, does the endpoint folder exist, does the described flow match the implementation. For behavioural claims, read the implementation far enough to confirm or refute — "probably fine" is not a verdict.

## Verify — the false-positive gate

A claim is drifted only when you can quote both sides: the doc's sentence and the code that contradicts it. Ambiguous prose that *could* be read as wrong gets reported as low-severity "imprecise", quoting the reading that misleads.

## Severity

High: a claim that sends a follower down a broken path (wrong command, wrong port, endpoint that's gone) or misdescribes behaviour someone would build against. Medium: stale references that cost a detour; consumed plans/handoffs still present. Low: imprecision, drifted counts.

## Report

Return the JSON findings array per the schema in your dispatch prompt. `evidence` quotes the doc line and the contradicting code; `recommendation` is "update to say X" or "delete (policy: current-state docs stay true or go)".

An empty findings array is a valid result - a weak finding costs more than a missing one. Do not pad.
