# Over-engineering pass

Hunt complexity that exists for needs the code doesn't have. The measure is the **deletion test**: if removing an abstraction would *concentrate* the logic into one clearer place, the abstraction is the problem; if removal would *scatter* it, the abstraction is earning its keep.

Read the repo's conventions and ADRs (locations in your dispatch prompt) first — a pattern the repo has deliberately standardised is not over-engineering, however heavy it looks.

## Hunt

- Abstractions with exactly one implementation or one caller: interfaces, factories, wrapper classes, "strategy" patterns serving a single strategy.
- Layers that only forward — a function/class whose body is one call to the next layer with the same arguments.
- Configuration, options, or parameters that only ever take one value everywhere in the scope.
- Speculative generality: generics, hooks, plugin points, and "future-proof" branches for futures that never arrived.
- Indirection that makes reading harder than the thing it abstracts: reading the abstraction plus its one use costs more than reading inlined code would.
- State machines, queues, or caching layered onto flows simple enough for a direct call.

## Verify — the false-positive gate

Before reporting, for each candidate:

1. Count the real callers/implementations (grep, not memory). Two or more genuine variants clears the finding.
2. Check `git log --follow` on the file: was the flexibility ever exercised? Recent churn toward more variants also clears it.
3. Apply the deletion test and write the answer into the evidence: what the code would look like without it, in one sentence.

## Severity

Blocker: never applies here. High: the indirection misleads readers about what actually happens, or spans several files. Medium: local ceremony with a clear inline. Low: naming/shape nits.

## Report

Return the JSON findings array per the schema in your dispatch prompt. `recommendation` names what to inline or delete and where the surviving logic lands.

An empty findings array is a valid result - a weak finding costs more than a missing one. Do not pad.
