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
| `setup-dev-repo` | Setup | ours | - | Two issue labels (`afk`/`hitl`) instead of eight; adds `.claude/reports/` to `.gitignore`. 2026-08-17: the complex/simple fork and the five-question stack interview were cut - this runs after planning, so the stack is already decided and re-asking boxes the user in before the grill has happened. `CONTEXT.md` deliberately not seeded, with the reason written in. 2026-08-18: the EXT-/INT- naming table replaced by asking the user for name and owner - a public-bound repo should not ship internal naming rules - and the Common mistakes table cut as restating the body |
| `grill-me` | Main Flow | merged | `productivity/grill-me` + `productivity/grilling` | Matt's `grill-me` is a one-line delegator to `grilling`. Merged into one self-contained file rather than shipping a hidden skill nobody invokes. Body is his `grilling` verbatim. 2026-08-17: `disable-model-invocation: true` dropped. The flag came from his `grill-me` wrapper; his `grilling` carries no such flag, so he could reach the interview method both ways and our merge had silently collapsed it to typed-only. With 97 Skill calls in 1,200 sampled sessions, typed-only means never. The description already carries a trigger clause, so the model can route to it |
| `to-spec` | Main Flow | tweaked | `engineering/to-spec` | Tracker-setup sentence removed |
| `to-issues` | Main Flow | tweaked | `engineering/to-tickets` | Renamed. Tracker note points at `setup-dev-repo` rather than `/setup-matt-pocock-skills`; `ready-for-agent` label replaced by `afk`/`hitl` with `hitl` as default |
| `pickup-issue` | Main Flow | ours | - | Rewritten 2026-08-14, down from 82 lines. Reads issue + comments, asks only about ambiguity, resolves the worktree, hands to `implement`. No draft PR. 2026-08-17: that handoff was broken from the day it was written - the last line invokes `/implement`, which was typed-only, so the chain dead-stopped. Fixed by the set-wide unflagging rather than by rewording the handoff |
| `implement` | Main Flow | tweaked | `engineering/implement` | Final `/code-review` replaced by `/code-review low`, with a note that the deep pass belongs in a fresh session. Matt publishes the self-review-bias argument himself. 2026-08-17: `disable-model-invocation` dropped. **This is the sharpest of the set-wide unflaggings and the one to think twice about on refresh** - unlike `grill-me`, upstream has no unflagged twin, so the flag was Matt's deliberate guard on the one skill that writes and commits code unprompted. Ours on purpose: the guard moves to the `hitl` default label, and without this `pickup-issue` cannot hand off. 2026-08-18: the ending changed - implement stops at the commit and hands the branch to the user for review; it merges only on explicit permission, an `afk` label counting as that permission |
| `wayfinder` | Shape | tweaked | `engineering/wayfinder` | `/grilling` -> `/grill-me`; `/domain-modeling` references dropped (not shipped); tracker-setup sentence removed. 2026-08-18: tracker hardcoded to GitHub via `gh` - upstream's tracker-doc layer and local-markdown fallback belong to `/setup-matt-pocock-skills`, which we do not ship; wayfinder now creates its own `wayfinder:*` labels if missing, and the `research/<name>` branch is stated as wayfinder's own convention rather than `/research`'s |
| `prototype` | Shape | verbatim | `engineering/prototype` | none |
| `research` | Shape | verbatim | `engineering/research` | none |
| `visual-spec` | Shape | ours | - | Restyled 2026-08-17 off the S8 white/red house palette onto the shared `assets/report.css`, matching `verify-feature` and `review-suite`. Reports are working documents, so they carry no branding. Output moved to `.claude/reports/` |
| `improve-codebase-architecture` | Utilities | tweaked | `engineering/improve-codebase-architecture` | `/grilling` -> `/grill-me`; `/codebase-design` and `/domain-modeling` references dropped (not shipped), vocabulary kept inline |
| `diagnosing-bugs` | Utilities | verbatim | `engineering/diagnosing-bugs` | none. Kept his name; supersedes our `systematic-debugging` fork. Refresh hazard, noted 2026-08-18: upstream main has since cut the Phase 6 post-mortem handoff to `/improve-codebase-architecture` - a skill we ship - so "take theirs" would silently drop it; decide deliberately |
| `wait-what` | Utilities | tweaked | `productivity/wait-what` | One clause added: keep the re-pitch short. Note: it does **not** supersede an explain-from-scratch skill, as previously recorded here - `wait-what` re-pitches *the last message* when it did not land, which is a different job from explaining a topic cold |
| `verify-feature` | Utilities | Emil Vladinov | - | Was `ui-report` until 2026-08-17, when Emil widened it from UI screenshots to full runtime verification: four fixed categories (UI, endpoints, database, behavioral), a cached `verify-recipe` of project facts, six behavioral archetypes scanned off the diff, required negative cases, and an artifact ledger that reverts everything the run created. Kept from our earlier port, which his new copy had reverted: OS temp working dir, `.claude/reports/` output, cross-platform open, and the shared `assets/report.css`. Builder gained `sections` - tables, evidence blocks, notes - plus `na`/`notes` statuses, and stays backwards compatible with `ui-report` manifests |
| `review-suite` | Utilities | Emil Vladinov | - | Same porting. 2026-08-18: verify stage added before the report - one adversarial subagent per blocker/high - and every pass file now ends with the empty-result-is-valid line |
| `wizard` | Misc | verbatim | `engineering/wizard` | none |
| `to-questionnaire` | Misc | verbatim | `productivity/to-questionnaire` | none |
| `start` | Misc | tweaked | obra/superpowers | Dangling `start-dev` reference removed, and the claim that `grill-me` maintains `CONTEXT.md` dropped - the shipped `grill-me` does no such thing. 2026-08-18: the at-a-phase-boundary ladder cut - `start` fires at session start, the ladder fires mid-session, so it could never be in context when it was needed; the content is parked for the modules |
| `update-docs` | Misc | lifted | Matt's handoff lineage | Reshaped for our ledger + handoff model |
| `tdd` | Utilities | tweaked | `engineering/tdd` | Reference to `/codebase-design` (not shipped) replaced by the vocabulary inline. 2026-08-18: listed in the README under Utilities - `implement` calls it, and you can also invoke it directly |

**Set-wide changes:**

- Matt ships Codex sidecar YAMLs in some skills' `agents/` directories. We do not adopt them and
  they are stripped on vendoring.
- Several of his skills call `/domain-modeling`, `/codebase-design` and `/setup-matt-pocock-skills`,
  which we do not ship. Every such reference is removed rather than repointed. Where the reference
  carried real content (the architecture vocabulary), the content is kept inline.
- **A reference to a skill that does not exist is the bug class to watch for on every refresh.**
  Re-run the slash-reference scan after taking anything new from upstream.
- **`disable-model-invocation` is dropped from the whole Main Flow (2026-08-17), deliberately.**
  `setup-dev-repo`, `grill-me`, `to-spec`, `to-issues`, `pickup-issue`, `implement`, `wayfinder` and
  `update-docs` are all model-invocable. Upstream flags most of these; we do not. Two reasons. The
  flow could not self-start, which is the mechanism behind 97 Skill calls against 4,811 Bash in 1,200
  sampled sessions - the skills were unreachable, not unloved. And `setup-dev-repo` creates exactly
  two issue labels, `afk` and `hitl`: work marked `afk` is meant to run unattended, and a flow that
  cannot propel itself can never run `afk` at all. **The human-in-the-loop guard lives in the label,
  not the frontmatter** - `hitl` is the default, so nothing runs unattended unless it is marked to.
  Only three skills stay typed-only, because for them autonomous invocation is meaningless rather
  than risky: `wait-what` (re-pitches the *last message*), `to-questionnaire`, and
  `improve-codebase-architecture` (a long analysis run you ask for).
- **On refresh, do not restore the flag.** A `verbatim`/`tweaked` diff will show upstream carrying
  `disable-model-invocation` where we do not. That is this decision, not drift.
- **2026-08-18, from Kasper's read-through:** `assets/report.css` v2 - the report family went dark,
  layout language adopted from Syv AI's `visual-plan` output (rebuilt from scratch, not copied;
  still unbranded and network-free). `review-suite` gained an adversarial verify stage before the
  report and every pass file states that an empty result is valid. `skills/` flattened to one
  directory per skill - grouping lives in the README only.

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
