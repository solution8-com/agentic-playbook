# HTML Report Format

The architectural review is rendered as a single self-contained HTML file in `.claude/reports/`. **No CDNs, no external fonts, no network** - it opens from disk and keeps working when a URL moves or the client's firewall blocks it. Every diagram is hand-built: inline SVG for graph-shaped things (call graphs, dependencies, sequences), positioned divs for the more editorial visuals (mass diagrams, cross-sections). Layout is yours to work out - that is the cost of not shipping a diagram library, and it buys a file that renders forever.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review — {{repo name}}</title>
    <style>
      /* Inline the plugin's shared assets/report.css here, then add only what
         this report needs on top: dashed seam lines, arrow heads, and so on. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: var(--red); }
      .deep { background: var(--panel-2); outline: 2px solid var(--amber); }
      .node rect { fill: var(--panel-2); stroke: var(--line); stroke-width: 1.5; }
      .node text { font-size: 11px; fill: var(--ink); }
    </style>
  </head>
  <body>
    <main class="wrap">
      <header>...</header>
      <section id="candidates">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header

Repo name, date, and a compact legend: solid box = module, dashed line = seam, red arrow = leakage, amber-edged box = deep module. No introduction paragraph — straight into the candidates.

## Candidate card

The diagrams carry the weight. Prose is sparse, plain, and uses the architecture glossary terms without ceremony.

Each candidate is one `<article>`:

- **Title** — short, names the deepening (e.g. "Collapse the Order intake pipeline").
- **Badge row** — recommendation strength (`Strong` = emerald, `Worth exploring` = amber, `Speculative` = slate), plus a tag for the dependency category (`in-process`, `local-substitutable`, `ports & adapters`, `mock`).
- **Files** — monospaced list, using the stylesheet's `.mono`.
- **Before / After diagram** — the centrepiece. Two columns, side by side. See patterns below.
- **Problem** — one sentence. What hurts.
- **Solution** — one sentence. What changes.
- **Wins** — bullets, ≤6 words each. e.g. "Tests hit one interface", "Pricing logic stops leaking", "Delete 4 shallow wrappers".
- **ADR callout** (if applicable) — one line in an amber-tinted box.

No paragraphs of explanation. If the diagram needs a paragraph to be understood, redraw the diagram.

## Diagram patterns

Pick the pattern that fits the candidate. Mix them. Don't make every diagram look the same — variety is part of the point.

### Dependency graph (good for leakage across a seam)

Hand-built inline SVG. Boxes on a grid you place yourself, arrows as `<line>` or `<path>`, the leaking edge in red and dashed. Keep it to a handful of nodes — if it needs auto-layout, it is too big to be a useful diagram.

```html
<div class="card">
  <svg viewBox="0 0 420 120" role="img" aria-label="Order intake dependencies">
    <g class="node">
      <rect x="8"   y="40" width="110" height="36" rx="6"/>
      <text x="63"  y="63" text-anchor="middle">OrderHandler</text>
    </g>
    <rect x="152" y="40" width="110" height="36" rx="6"/>
    <text x="207" y="63" text-anchor="middle">OrderValidator</text>
    <rect x="296" y="40" width="110" height="36" rx="6"/>
    <text x="351" y="63" text-anchor="middle">OrderRepo</text>

    <line x1="118" y1="58" x2="152" y2="58" marker-end="url(#a)"/>
    <line x1="262" y1="58" x2="296" y2="58" marker-end="url(#a)"/>
    <!-- the leak: dashed, red, crossing the seam -->
    <path class="seam leak" d="M351 76 V104 H63 V76" fill="none" marker-end="url(#a)"/>

    <defs>
      <marker id="a" viewBox="0 0 10 10" refX="9" refY="5"
              markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M0 0 L10 5 L0 10 z"/>
      </marker>
    </defs>
  </svg>
</div>
```

### Cross-section (good for layered shallowness)

Stack horizontal bands to show the layers a call passes through. Before: 6 thin layers each doing nothing. After: 1 thick band labelled with the consolidated responsibility.

### Mass diagram (good for "interface as wide as implementation")

Two rectangles per module — one for interface surface area, one for implementation. Before: interface rectangle is nearly as tall as the implementation rectangle (shallow). After: interface rectangle is short, implementation rectangle is tall (deep).

### Call-graph collapse

Before: a tree of function calls rendered as nested boxes. After: the same tree collapsed into one box, with the now-internal calls shown faded inside it.

## Style guidance

- Lean editorial, not corporate-dashboard. Generous whitespace. The shared stylesheet already sets serif headings and the palette; work inside it.
- Colour sparingly and semantically: `--red` for leakage, `--green` for the resolved state, `--line` and `--muted` for everything structural.
- Keep diagrams ~320px tall so before/after sits comfortably side by side without scrolling.
- Module labels inside diagrams read as schematic, not as UI: small, uppercase, letter-spaced, monospace.

## Top recommendation section

One larger card. Candidate name, one sentence on why, anchor link to its card. That's it.

## Tone

Plain English, concise — but the architectural nouns and verbs come straight from the architecture glossary. Concision is not an excuse to drift.

**Use exactly:** module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality.

**Never substitute:** component, service, unit (for module) · API, signature (for interface) · boundary (for seam) · layer, wrapper (for module, when you mean module).

**Phrasings that fit the style:**

- "Order intake module is shallow — interface nearly matches the implementation."
- "Pricing leaks across the seam."
- "Deepen: one interface, one place to test."
- "Two adapters justify the seam: HTTP in prod, in-memory in tests."

**Wins bullets** name the gain in glossary terms: *"locality: bugs concentrate in one module"*, *"leverage: one interface, N call sites"*, *"interface shrinks; implementation absorbs the wrappers"*. Don't write *"easier to maintain"* or *"cleaner code"* — those terms aren't in the glossary and don't earn their place.

No hedging, no throat-clearing, no "it's worth noting that…". If a sentence could be a bullet, make it a bullet. If a bullet could be cut, cut it. If a term isn't in the architecture glossary, reach for one that is before inventing a new one.
