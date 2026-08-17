# Catalog - where each skill came from

> Make the next refresh against upstream a diff rather than an archaeology dig.

That is this file's only job. It records what we took, from where, and what we changed. Nothing else. The
working index is [README.md](./README.md); the licensing record is
[ATTRIBUTION.md](./ATTRIBUTION.md).

Skill files themselves carry no provenance notes. Metadata kept in two places drifts, and it did,
twice, in two days. This is the only record.

## Upstreams

| Upstream | Pinned at | Licence |
|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | v1.2.3, commit `8b78b53`, 2026-08-13 | MIT |
| [obra/superpowers](https://github.com/obra/superpowers) | as vendored 2026-08 | MIT |

**We do not track Matt continuously.** He ships faster than we can merge, and pretending otherwise
is the promise most likely to break. Refresh deliberately, using the table below.

## The table

`verbatim` means byte-identical to upstream apart from the noted change. `ours` means no public
precedent.

| Skill | Group | Source | Upstream path | What we changed |
|---|---|---|---|---|
| `setup-dev-repo` | Get Started | ours | - | Two issue labels (`afk`/`hitl`) instead of eight; adds `.claude/reports/` to `.gitignore`. 2026-08-17: the complex/simple fork and the five-question stack interview were cut - this runs after planning, so the stack is already decided and re-asking boxes the user in before the grill has happened. `CONTEXT.md` deliberately not seeded, with the reason written in |
| `grill-me` | Main Flow | merged | `productivity/grill-me` + `productivity/grilling` | Matt's `grill-me` is a one-line delegator to `grilling`. Merged into one self-contained file rather than shipping a hidden skill nobody invokes. Body is his `grilling` verbatim |
| `to-spec` | Main Flow | tweaked | `engineering/to-spec` | Tracker-setup sentence removed |
| `to-issues` | Main Flow | tweaked | `engineering/to-tickets` | Renamed. Tracker note points at `setup-dev-repo` rather than `/setup-matt-pocock-skills`; `ready-for-agent` label replaced by `afk`/`hitl` with `hitl` as default |
| `pickup-issue` | Main Flow | ours | - | Rewritten 2026-08-14, down from 82 lines. Reads issue + comments, asks only about ambiguity, resolves the worktree, hands to `implement`. No draft PR |
| `implement` | Main Flow | tweaked | `engineering/implement` | Final `/code-review` replaced by `/code-review low`, with a note that the deep pass belongs in a fresh session. Matt publishes the self-review-bias argument himself |
| `wayfinder` | Shape | tweaked | `engineering/wayfinder` | `/grilling` -> `/grill-me`; `/domain-modeling` references dropped (not shipped); tracker-setup sentence removed |
| `prototype` | Shape | verbatim | `engineering/prototype` | none |
| `research` | Shape | verbatim | `engineering/research` | none |
| `visual-spec` | Shape | ours | - | Restyled 2026-08-17 off the S8 white/red house palette onto the shared `assets/report.css`, matching `verify-feature` and `review-suite`. Reports are working documents, so they carry no branding. Output moved to `.claude/reports/` |
| `improve-codebase-architecture` | Utilities | tweaked | `engineering/improve-codebase-architecture` | `/grilling` -> `/grill-me`; `/codebase-design` and `/domain-modeling` references dropped (not shipped), vocabulary kept inline |
| `diagnosing-bugs` | Utilities | verbatim | `engineering/diagnosing-bugs` | none. Kept his name; supersedes our `systematic-debugging` fork |
| `wait-what` | Utilities | tweaked | `productivity/wait-what` | One clause added: keep the re-pitch short. Note: it does **not** supersede an explain-from-scratch skill, as previously recorded here - `wait-what` re-pitches *the last message* when it did not land, which is a different job from explaining a topic cold |
| `verify-feature` | Utilities | Emil Vladinov | - | Was `ui-report` until 2026-08-17, when Emil widened it from UI screenshots to full runtime verification: four fixed categories (UI, endpoints, database, behavioral), a cached `verify-recipe` of project facts, six behavioral archetypes scanned off the diff, required negative cases, and an artifact ledger that reverts everything the run created. Kept from our earlier port, which his new copy had reverted: OS temp working dir, `.claude/reports/` output, cross-platform open, and the shared `assets/report.css`. Builder gained `sections` - tables, evidence blocks, notes - plus `na`/`notes` statuses, and stays backwards compatible with `ui-report` manifests |
| `review-suite` | Utilities | Emil Vladinov | - | Same porting. Seven passes unchanged |
| `wizard` | Misc | verbatim | `engineering/wizard` | none |
| `to-questionnaire` | Misc | verbatim | `productivity/to-questionnaire` | none |
| `start` | Misc | tweaked | obra/superpowers | Dangling `start-dev` reference removed, and the claim that `grill-me` maintains `CONTEXT.md` dropped - the shipped `grill-me` does no such thing |
| `update-docs` | Misc | lifted | Matt's handoff lineage | Reshaped for our ledger + handoff model |
| `tdd` | Support | tweaked | `engineering/tdd` | Reference to `/codebase-design` (not shipped) replaced by the vocabulary inline. Not listed in the README - `implement` calls it |

**Set-wide changes:**

- Matt ships Codex sidecar YAMLs in some skills' `agents/` directories. We do not adopt them and
  they are stripped on vendoring.
- Several of his skills call `/domain-modeling`, `/codebase-design` and `/setup-matt-pocock-skills`,
  which we do not ship. Every such reference is removed rather than repointed. Where the reference
  carried real content (the architecture vocabulary), the content is kept inline.
- **A reference to a skill that does not exist is the bug class to watch for on every refresh.**
  Re-run the slash-reference scan after taking anything new from upstream.

## How to refresh

1. Clone upstream at its latest tag.
2. For every row marked `verbatim`, diff our copy against the upstream path. Take theirs.
3. For every row marked `tweaked`, diff, then re-apply the change in the "What we changed" column.
4. Update the pinned commit in the Upstreams table.

Rows marked `ours` and Emil's two never need this.

## Cut in the 2026-08-14 rescope

The set went from 25 skills to 20. Cut, with the reason:

| Cut | Why |
|---|---|
| `setup-skills`, `update-skills` | The plugin installs and updates itself |
| `start-dev` | Day orchestration and wave planning. A slash command at most, not a skill |
| `close-issue` | The models already know to merge on green. A line in `CLAUDE.md`, not a skill |
| `writing-plan` | Guardrails on a model that no longer needs them |
| `subagent-driven-development` | Built for Opus-plans-Sonnet-builds. Agents hold long work now |
| `code-review` | Claude Code ships `/code-review` with an effort level. Ours would have collided with the built-in of the same name |
| `writing-for-agents` | How we author skills, not something the plugin needs to ship. Kept locally |
| `verify-task-done` | Cut earlier. CI plus the issue's acceptance criteria are the gate |

## Pending

- The repo is still private and still carries the `INT-` prefix. Renaming to
  `solution8-com/s8-agentic-playbook` and going public is a deliberate later step; the install
  paths in README and `plugin.json` change with it.
