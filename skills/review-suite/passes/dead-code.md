# Dead-code pass

Hunt code that can be deleted with zero behaviour change: unreferenced exports, unreachable branches, orphaned files and assets. Dead code's cost is that every reader must first discover it's dead — deletion is the fix, and git history is the archive.

This pass lives or dies on its verification gate: dead-code tooling false-positives constantly (dynamic imports, DI, route tables, reflection). A finding you haven't grep-verified is a finding you haven't made.

## Hunt

Tool-assisted first — cheap, wide nets; treat every hit as a *candidate*, never a finding:

- `npx knip` (or the repo's configured equivalent — ts-prune, depcheck) from the relevant package root.
- If `mcp__jcodemunch__*` tools are available in your session, `find_dead_code` / `find_unused_paths`.
- The compiler/linter's unused-symbol output where available.

Then manual sweeps tooling misses:

- Exports imported by nothing (search the import, not the definition).
- Branches gated on flags/conditions that are constant in this codebase (a flag that is always false, an env check that can't vary).
- Commented-out code blocks.
- Files, styles, assets, and translation keys referenced by nothing.
- Dependencies in `package.json` imported by nothing.

## Verify — the false-positive gate

For each candidate, hunt for the reference that would keep it alive, and record the searches you ran in the evidence:

1. Grep the bare name across the whole repo (not just the scope) — including string form: dynamic `import()`, route registrations, config files, templates, test files.
2. Check for framework magic: convention-based loading (file-based routing, function folders auto-registered by name), DI containers, reflection.
3. Check whether it's a published surface: package entry points, public API of a library, endpoints an external caller may hit.

Test-only usage is a real state — report it as "only referenced by its own tests" rather than dead; the recommendation is to decide whether the tests or the code should go.

## Severity

High: whole dead files/endpoints/dependencies that readers keep encountering. Medium: dead branches and exports inside live files. Low: commented-out fragments, unused keys.

## Report

Return the JSON findings array per the schema in your dispatch prompt. `evidence` names the searches that came back empty; `recommendation` is the deletion, plus anything that must move first.

An empty findings array is a valid result - a weak finding costs more than a missing one. Do not pad.
