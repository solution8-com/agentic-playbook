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
3. **Style it to the playbook's visual system** (see below). Self-contained: inline everything, no external assets.
4. **Surface it.** Report the file path so the human can open it. Do NOT block anything waiting for them to look.

## Visual style

Style it as a **Solution8 document: white and red**, the S8 house palette (the same one
the `to-questionnaire` template uses):

- **Background** white (`#FFFFFF`); ink near-black (`#0A0A0A`); secondary text warm grey
  (`#6E6A68`); card fills `#F7F6F5`; hairlines `#E7E3E0`.
- **Primary accent red `#E3241B`**, used sparingly: the title underline, badges,
  highlights. Soft tint `#FDEEED` for callout backgrounds.
- Inside a structural diagram, where one accent is not enough for categories and states,
  the S8 diagram accents are available: orange `#FF6A1A`, amber `#FFBF00`, green
  `#16C784`, violet `#8B3DFF`, magenta `#FF2E88`.

No accented Danish characters.

## Output

- One self-contained HTML file in the Solution8 white/red document style.
- Summary depth: overview plus structural diagram, not a line-by-line walkthrough.

## Related skills

- **to-spec** - the stage that offers this at the end; supplies the spec being visualized.
