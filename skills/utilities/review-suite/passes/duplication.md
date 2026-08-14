# Duplication pass

Hunt the same *intent* implemented more than once — logic, JSX, queries, validation — and name the extraction that would unify it. The prize is a single source of truth: one place to fix the next bug.

Distinguish duplication of intent from coincidental similarity. Two hunks that look alike but change for different reasons are better left apart; forcing them together creates the coupling the over-engineering pass would then flag. The **rule of three** calibrates: two occurrences is a note, three or more is a finding.

## Hunt

- Copy-pasted logic across files: same algorithm, same error handling, same data massaging with renamed variables. `npx jscpd <paths>` casts a wide net if available; treat hits as candidates.
- Repeated JSX/UI blocks that want a shared component — same structure and styling recurring across pages, diverging only in data.
- The same validation, formatting, or parsing reimplemented at several sites (dates, currency, permission checks, API error shapes).
- Parallel switch/if-cascades on the same discriminator across files — a change to the type means finding every cascade.
- Utility functions re-invented per module because nobody knew one existed (search shared/util/helper directories for the near-twin).

## Verify — the false-positive gate

For each candidate:

1. Confirm shared intent: would a bug fix in one site necessarily belong in the others? A "no" clears the finding.
2. Diff the occurrences precisely — the parts that *differ* become the extraction's parameters. If the parameter list balloons, the sites weren't duplicates; drop or downgrade.
3. Name where the extraction lives, following the repo's conventions for shared code (check the conventions files from your dispatch prompt).

## Severity

High: three-plus sites, or two sites already diverged (a bug fixed in one, not the other — check git history for this, it's the strongest evidence there is). Medium: clean two-to-three-site duplication. Low: small repeated fragments barely worth a helper.

## Report

Return the JSON findings array per the schema in your dispatch prompt. `location` lists every occurrence; `recommendation` names the shared component/helper/hook, its proposed home, and its parameters.
