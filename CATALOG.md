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
| `onboarding` | Setup | ours | - | Added 2026-08-25 from an 18-question grill. Specified by a real failure, not an imagined one - Jacob's own words: *"Casper sent me the repo and I was like, what do I do with this?"*, then *"what about the existing sessions I have? What about the existing skills that I have?"*. Covers the post-install pair only; the first question is answered by the README's paste-block, because at that moment nothing is installed and no skill can reach the person. Audits five global surfaces and never the user's code, suggests with a plain reason and applies nothing without a yes, backs up before editing, and closes on the Main Flow in plain English. Absorbs the tour from `guide`. Exempt from the retired-name check: talking about skills the plugin does not ship is its job |
| `setup-repo` | Setup | ours | - | **Renamed from `setup-dev-repo` 2026-08-25**, and its refusal turned into a branch: every project gets a repo, `CLAUDE.md`, issue labels and a tracker, while only projects with code get a stack, tests and a commit gate. "Dev" told IT teams and managers the skill was not for them, which is backwards from the 2026-08-21 targeting decision - they are the wedge. The internal vocabulary went with it: "context repo" and one Danish word had no business in a public-bound repo. Two issue labels (`afk`/`hitl`) instead of eight; adds `.claude/reports/` to `.gitignore`. 2026-08-17: the complex/simple fork and the five-question stack interview were cut - this runs after planning, so the stack is already decided and re-asking boxes the user in before the grill has happened. `CONTEXT.md` deliberately not seeded, with the reason written in. 2026-08-18: the EXT-/INT- naming table replaced by asking the user for name and owner - a public-bound repo should not ship internal naming rules - and the Common mistakes table cut as restating the body |
| `grill-me` | Main Flow | merged | `productivity/grill-me` + `productivity/grilling` | Matt's `grill-me` is a one-line delegator to `grilling`. Merged into one self-contained file rather than shipping a hidden skill nobody invokes. Body is his `grilling` verbatim. 2026-08-17: `disable-model-invocation: true` dropped. The flag came from his `grill-me` wrapper; his `grilling` carries no such flag, so he could reach the interview method both ways and our merge had silently collapsed it to typed-only. With 97 Skill calls in 1,200 sampled sessions, typed-only means never. The description already carries a trigger clause, so the model can route to it. 2026-08-18: pacing changed - one question at a time instead of batching the whole frontier into a numbered round. The first body divergence from Matt's `grilling`, ours on purpose: two independent sessions hit the round format as a friction on the same day |
| `to-spec` | Main Flow | tweaked | `engineering/to-spec` | Tracker-setup sentence removed |
| `to-issues` | Main Flow | tweaked | `engineering/to-tickets` | Renamed. Tracker note points at `setup-dev-repo` rather than `/setup-matt-pocock-skills`; `ready-for-agent` label replaced by `afk`/`hitl` with `hitl` as default |
| `pickup-issue` | Main Flow | ours | - | Rewritten 2026-08-14, down from 82 lines. Reads issue + comments, asks only about ambiguity, resolves the worktree, hands to `implement`. No draft PR. 2026-08-17: that handoff was broken from the day it was written - the last line invokes `/implement`, which was typed-only, so the chain dead-stopped. Fixed by the set-wide unflagging rather than by rewording the handoff. 2026-08-18: two additions out of the first live chain run - step 1 now checks the issue's claims against the live tree before any code is written (an issue is a hypothesis, including last week's; the one durable job of a plan gate), and the worktree path is stated as a default that yields to an existing repo convention (a `wt-*` hook collision surfaced in the field). 2026-08-25: step 1 gains a local-ticket path and reads the tracker note - it could only ever run `gh issue view`, so the chain snapped between `to-issues` and here for anyone off GitHub, and the tickets `to-issues` wrote locally had nothing that could pick them up. 2026-08-20: step 1 gains three-state claim resolution with `file:line` receipts, the absence-claims-are-hardest rule, and a ripple check into the acceptance criteria - mechanics taken from our own `ground-issue` work; step 2 becomes the settled-or-grill fork, since the Main Flow is joined wherever the work already is - so an issue can arrive with nothing settled, and step 2 hands back to grill-me rather than asking the user which flow they are in |
| `implement` | Main Flow | tweaked | `engineering/implement` | Final `/code-review` replaced by `/code-review low`, with a note that the deep pass belongs in a fresh session. Matt publishes the self-review-bias argument himself. 2026-08-17: `disable-model-invocation` dropped. **This is the sharpest of the set-wide unflaggings and the one to think twice about on refresh** - unlike `grill-me`, upstream has no unflagged twin, so the flag was Matt's deliberate guard on the one skill that writes and commits code unprompted. Ours on purpose: the guard moves to the `hitl` default label, and without this `pickup-issue` cannot hand off. 2026-08-18: the ending changed - implement stops at the commit and hands the branch to the user for review; it merges only on explicit permission, an `afk` label counting as that permission. Same day, from the second live chain run: the `/code-review low` step must name its target branch/worktree explicitly - review sub-agents inherit the session's directory, and an untargeted review in a worktree flow passed without seeing the diff |
| `wayfinder` | Shape | tweaked | `engineering/wayfinder` | `/grilling` -> `/grill-me`; `/domain-modeling` references dropped (not shipped); tracker-setup sentence removed. 2026-08-18: tracker hardcoded to GitHub via `gh` - upstream's tracker-doc layer and local-markdown fallback belong to `/setup-matt-pocock-skills`, which we do not ship; wayfinder now creates its own `wayfinder:*` labels if missing, and the `research/<name>` branch is stated as wayfinder's own convention rather than `/research`'s |
| `prototype` | Shape | verbatim | `engineering/prototype` | none |
| `research` | Shape | verbatim | `engineering/research` | none |
| `visual-spec` | Shape | ours | - | Restyled 2026-08-17 off the S8 white/red house palette onto the shared `assets/report.css`, matching `verify-feature` and `review-suite`. Reports are working documents, so they carry no branding. Output moved to `.claude/reports/` |
| `improve-codebase-architecture` | Utilities | tweaked | `engineering/improve-codebase-architecture` | `/grilling` -> `/grill-me`; `/codebase-design` and `/domain-modeling` references dropped (not shipped), vocabulary kept inline |
| `diagnosing-bugs` | Utilities | verbatim | `engineering/diagnosing-bugs` | none. Kept his name; supersedes our `systematic-debugging` fork. Refresh hazard, noted 2026-08-18: upstream main has since cut the Phase 6 post-mortem handoff to `/improve-codebase-architecture` - a skill we ship - so "take theirs" would silently drop it; decide deliberately |
| `wait-what` | Utilities | tweaked | `productivity/wait-what` | One clause added: keep the re-pitch short. Note: it does **not** supersede an explain-from-scratch skill, as previously recorded here - `wait-what` re-pitches *the last message* when it did not land, which is a different job from explaining a topic cold. 2026-08-20: `disable-model-invocation` removed and the description rewritten as a trigger condition |
| `verify-feature` | Utilities | ours | - | Was `ui-report` until 2026-08-17, when it widened from UI screenshots to full runtime verification: four fixed categories (UI, endpoints, database, behavioral), a cached `verify-recipe` of project facts, six behavioral archetypes scanned off the diff, required negative cases, and an artifact ledger that reverts everything the run created. Kept from our earlier port, which the newer copy had reverted: OS temp working dir, `.claude/reports/` output, cross-platform open, and the shared `assets/report.css`. Builder gained `sections` - tables, evidence blocks, notes - plus `na`/`notes` statuses, and stays backwards compatible with `ui-report` manifests |
| `review-suite` | Utilities | ours | - | Same porting. 2026-08-18: verify stage added before the report - one adversarial subagent per blocker/high - and every pass file now ends with the empty-result-is-valid line |
| `suggest` | Misc | ours | - | **Renamed from `guide` 2026-08-25 and the tour cut**, which now lives in `onboarding`. The two halves sat on different clocks - routing is needed whenever someone is unsure, touring happens once at the start - so splitting them leaves one skill doing one job instead of two half-sharing it. The name also stopped colliding with `modules/guide-setup.md` and `modules/guide-daily.md`, where "guide" means the hands-on docs layer, and `suggest` states the register the playbook actually holds. Originally added 2026-08-18: router + tour, with a `gh auth status` preflight (the one good piece of Syv's setup skill we otherwise lacked). Routes a situation to a skill, or tours the groups. Register is suggest-never-push, per the governing principle |
| `wizard` | Misc | verbatim | `engineering/wizard` | none |
| `to-questionnaire` | Misc | verbatim | `productivity/to-questionnaire` | none |
| `handoff` | Misc | tweaked | `productivity/handoff` | Kept the two decisions that make it work - the doc goes to `$TMPDIR` rather than the workspace, and anything already captured in a spec, issue, commit or diff is referenced rather than restated. Added: what goes in is weighted toward decisions settled in conversation that live nowhere else, and the suggested-skills section names which of the two Main Flow entry points the next session re-enters at |
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
  `setup-dev-repo`, `grill-me`, `to-spec`, `to-issues`, `pickup-issue`, `implement` and `wayfinder`
  are all model-invocable. Upstream flags most of these; we do not. Two reasons. The flow could not
  self-start, which is the mechanism behind 97 Skill calls against 4,811 Bash in 1,200 sampled
  sessions - nobody was ignoring the skills, they were unreachable. And `setup-dev-repo`
  creates exactly two issue labels, `afk` and `hitl`: work marked `afk` is meant to run unattended,
  and a flow that cannot propel itself can never run `afk` at all. **The human-in-the-loop guard
  lives in the label** - `hitl` is the default, so nothing runs unattended unless it is marked to.
  Two skills stay typed-only, because for them autonomous invocation would achieve nothing:
  `to-questionnaire` and `improve-codebase-architecture` (a long analysis run you ask for).
  **`wait-what` joined the model-invocable set 2026-08-20** - the flag came off *and* its
  description was rewritten from a command into a trigger condition, because the flag alone leaves
  a skill reachable but never reached.
- **`start` and `update-docs` left the set on 2026-08-20.** Both are good skills. They assume a
  *project* that may not be code, and this playbook assumes a repo, a tracker and code. Docs
  written beside a codebase drift, cannot be tested, and can be confidently wrong, while the
  tracker and the git history already hold the state. They move to the internal playbook, alongside
  ADR authoring, where the work being tracked is not always a repo. `handoff` replaces them here
  and writes nothing durable.
- **`start` and `update-docs` came back on 2026-08-27.** The reason they left expired: on
  2026-08-25 `setup-dev-repo` became `setup-repo` and stopped refusing non-code projects, so the
  playbook no longer assumes a repo, a tracker and code. The drift argument still holds and now
  decides *which* skill runs rather than whether either ships - `handoff` owns repos with code and
  writes nothing durable; `update-docs` owns docs, training and planning repos, where nothing else
  carries the state and a doc that drifts still beats no record at all. Repo type is read off
  manifest presence, the same rule `setup-repo` already uses, so nothing new is configured. `start`
  is the read side for both and reads both destinations.
- **The tracker layer is back, 2026-08-25, owned by us.** `wayfinder`, `to-spec` and `to-issues`
  had their tracker-setup sentences stripped because upstream's tracker-doc layer and
  local-markdown fallback belonged to `/setup-matt-pocock-skills`, which we do not ship. That trade
  left a hole nobody walked into until now: `to-issues` could write local tickets that
  `pickup-issue` had no way to read, so the Main Flow snapped between step three and step four for
  anyone not on GitHub. The layer is now `.claude/tracker.md`, written by `setup-repo` and read by
  the flow skills, with **absence meaning GitHub** so the recommended path stays configuration-free.
- **On refresh, do not restore the flag.** A `verbatim`/`tweaked` diff will show upstream carrying
  `disable-model-invocation` where we do not. That gap is this decision showing up in the diff.
  Leave it.
- **2026-08-18, from Kasper's read-through:** `assets/report.css` v2 - the report family went dark,
  layout language adopted from Syv AI's `visual-plan` output (rebuilt from scratch; still
  unbranded and network-free). `review-suite` gained an adversarial verify stage before the
  report and every pass file states that an empty result is valid. `skills/` flattened to one
  directory per skill - grouping lives in the README only.

## How to refresh

1. Clone upstream at its latest tag.
2. For every row marked `verbatim`, diff our copy against the upstream path. Take theirs.
3. For every row marked `tweaked`, diff, then re-apply the change in the "What we changed" column.
4. Update the pinned commit in the Upstreams table.

Rows marked `ours` never need this.

## Cut in the 2026-08-14 rescope

The set went from 25 skills to 20. It has moved since: `guide` and `handoff` in, then `start` and
`update-docs` out on 2026-08-20 and back in on 2026-08-27, split from `handoff` by repo type. Cut
in the rescope, with the reason:

| Cut | Why |
|---|---|
| `setup-skills`, `update-skills` | The plugin installs and updates itself |
| `start-dev` | Day orchestration and wave planning. A slash command at most |
| `close-issue` | The models already know to merge on green. A line in `CLAUDE.md` covers it |
| `writing-plan` | Guardrails on a model that no longer needs them |
| `subagent-driven-development` | Built for Opus-plans-Sonnet-builds. Agents hold long work now |
| `code-review` | Claude Code ships `/code-review` with an effort level. Ours would have collided with the built-in of the same name |
| `writing-for-agents` | How we author skills. Kept locally, out of the plugin |
| `verify-task-done` | Cut earlier. CI plus the issue's acceptance criteria are the gate |

## Pending

- The repo is still private and still carries the `INT-` prefix. Renaming to
  `solution8-com/s8-agentic-playbook` and going public is a deliberate later step; the install
  paths in README and `plugin.json` change with it.
