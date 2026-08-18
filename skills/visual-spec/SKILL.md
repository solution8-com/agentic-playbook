---
name: visual-spec
description: Produce a self-contained HTML overview of a spec in the playbook's visual style, for human review. Use when a spec has been published and seeing its shape would help, or when a user asks to "visualize the spec", "visualise the spec", or "give me an overview to review". Usually offered at the end of to-spec.
---

# Visual Spec

## Overview

Turns a published spec into a single self-contained HTML overview a human can scan. The spec
stays the source of truth; this is the at-a-glance view of it.

Usually offered as the last step of **to-spec**. Produce it when seeing the shape visually
would help, and skip it when it would not.

## When to use

- Offered at the end of **to-spec**, on specs where the structure is worth seeing.
- A user asks to "visualize the spec", "give me an overview to review".

Skip it on a small or linear spec. An overview of four bullet points is not worth the file.

## Process

1. **Read the spec.** Take the published spec (issue or markdown file) as input.
2. **Build the overview.** Produce one self-contained HTML file: the spec's problem and goals, the key decisions, the scope, and a simple structural diagram of the pieces and how they relate. Summary-level, not a full re-render of every line.
3. **Style it with the shared stylesheet** (see below). Self-contained: inline everything, no
   external assets and no network requests.
4. **Surface it.** Write it to `.claude/reports/<YYYY-MM-DD>-spec-<slug>.html` and report the
   file path so the human can open it. Do NOT block anything waiting for them to look.

## Visual style

**Inline the plugin's shared `assets/report.css`** — the same stylesheet `verify-feature` and
`review-suite` use, so every report this set produces reads as one family. Read it from the
plugin root and paste it into a `<style>` block; the file must render with no network.

Reports are working documents, not client deliverables, so they carry **no branding** - no house
palette, no logo, no accent colours borrowed from anywhere else. Use the classes the stylesheet
already defines rather than inventing new ones:

| Need | Class |
|---|---|
| Page frame | `.wrap` |
| Header line above the title | `.eyebrow`, then `.meta` for the subline |
| Lead paragraph | `.summary` |
| A section | `.flow`, with `.flow-head` for its heading row |
| A compact item | `.card` |
| Status marker | `.badge` plus `.ok` / `.bad` / `.muted` / `.na` |
| Inline verdict in prose or a table cell | `.ok` / `.warn` |
| Tables | `.tablewrap` around `table.results` |
| Literal output that is itself the evidence | `.evidence` |
| Settled decision or accepted risk | `.callout` / `.callout.risk` |
| Module map (create / modify / test rows) | `.modmap` with `.verb create\|modify\|test` |
| Code walked through with margin notes | `.annotated` with `.anno-notes`, `.note`, `.ln` |
| Before / after comparison | `.cols` with `.col` / `.col.after` |
| Closing verification checklist | `.checks` |
| In / out scope pills | `.pill.in` / `.pill.out` |

For a structural diagram, hand-build it with inline SVG or divs using the stylesheet's existing
variables (`--amber`, `--green`, `--red`, `--blue`, `--line`, `--muted`, `--panel`). Do not pull
in a diagram library.

Anything the stylesheet genuinely does not cover goes in a short extra `<style>` block below the
inlined sheet - but if it is a component the other report skills would also want, add it to
`assets/report.css` instead so all three stay in step.

No accented Danish characters.

## Output

- One self-contained HTML file in `.claude/reports/`, styled by the shared stylesheet, rendering
  with no network.
- Summary depth: overview plus structural diagram, not a line-by-line walkthrough.

## Related skills

- **to-spec** - the stage that offers this at the end; supplies the spec being visualized.
