# S8 Agentic Playbook - Skills Catalog (V3)

> Status: **V3, all 25 skills authored.** Every skill in the
> table below has a `SKILL.md`. This file is the source-mapping and lane reference behind
> the set; the working index is `README.md`; the authoritative behavior for any skill is
> its own `SKILL.md`.
>
> **Scope as of 2026-08-04: Claude Code in the terminal.** Helm is parked in
> `docs/helm-parked.md`, and the external/public build comes after the modules. See
> section 1.
>
> This is a rewrite of the older V2 catalog, which was a pre-authoring research + draft-spec
> document (no `SKILL.md` files existed yet, two lanes, a per-issue AFK/HITL label model).
> The original V2 per-skill research is retained as an appendix for provenance, but is
> superseded by the authored skills and by this document wherever the two disagree. See
> "Changed since V2".
>
> `skills/` is a lift-and-shift folder: the intent is that it eventually moves to a
> standalone agent-playbook repo, so nothing here assumes an app-specific path other than
> this file's own location.

## 1. Scope: Claude Code in the terminal

The playbook is S8's agentic-coding playbook: the curated Claude Code skill set that
encodes how S8 plans, builds, verifies, and ships software with agents.

**Milestone 1, and what this document describes, is the internal playbook as skills for
Claude Code in the terminal.** A laptop and a shell, no orchestrator. Then the 8 modules.
Then Helm. Then the external build.

### Helm is parked (2026-08-04)

The set was previously written partly against **Helm**, S8's agent cockpit, which is still
half built. That meant skills describing themselves by their position in a pipeline the
engine has not finished - `verify-with-playwright` as "the UI branch of the lane",
`start-dev` as "effectively a no-op inside Helm". Anticipation rather than documentation,
and it made the set hard to reason about.

So Helm came out, preserved verbatim in **`docs/helm-parked.md`**: one internal-only skill
(`helm-to-tasks`, taking the catalog from 27 to 26; `choose-issue` later merged into
`start-dev`, making it 25), ten `## Helm behavior (internal only)`
sections, and the design positions that leaned on Helm's invariants. Helm is a separate
track with Kasper, Emil and Martin, and folds back in after that sync.

Three consequences, because they undo earlier reasoning:

- **The look at interface changes** was justified by Helm refusing to automate it. Out of
  frame, it is a playbook convention again and stands on its own merits or not at all.
- **The merge wall** was reinstated on 2026-07-27 because Helm hard-codes never-push. With
  that argument gone, the wall was removed on the same day; see "The merge wall" below.
- **The task-topology gap** is dormant. It needed both dependency graphs, and only the
  GitHub one is live.

### The external build comes later

The two-variant convention (INTERNAL Helm-aware vs EXTERNAL public) depended on the
strippable Helm sections, which are parked. **There is currently one build.** The external
playbook is the final milestone.

When it returns it needs three transforms, not two: strip the reinstated Helm sections,
drop internal-only skills, and **rewrite the install path** from
`solution8-com/INT-s8-agentic-playbook` to `solution8-com/s8-agentic-playbook`. The third rule exists
because the path sits in ordinary prose, so the other two leave it untouched and ship the
public build an install command pointing at a repo its `INT-` prefix says is private. Find
every occurrence rather than tracking line numbers that drift:

```
grep -rl 'solution8-com/INT-s8-agentic-playbook' skills/
```

The public repo drops the prefix rather than taking one. `EXT-` is already reserved for
client engagements (`setup-dev-repo`, Module 2), so `EXT-agentic-playbook` would read as a
project for a client named "agentic". An unprefixed name is the public-facing one.

## 2. The three lanes (split by audience / sophistication)

V3 has three workflow lanes, split by **who is driving** and how much ceremony fits, plus
one maintenance activity that sits outside the lanes.

### Lane 1 - Project Start (once per project)

The planning arc, run once per project to go from an idea to a set of grabbable issues.
Audience: whoever kicks off a project.

**The split is project size** (settled 2026-08-04).

**Bigger project** - a new product, a client engagement, a substantial build; anything
running for weeks across many sessions:

```
setup-skills -> setup-dev-repo -> wayfinder
  (the map's tickets ARE the research, prototyping and grilling)
  -> to-spec -> [visual-spec, optional] -> to-issues
```

**Smaller project** - an automation, a script, a small tool, a bug fix:

```
setup-skills -> setup-dev-repo -> grill-me -> to-spec -> to-issues
```

**Wayfinder is how bigger projects start.** On something that size you do not know what you
do not know yet, so you chart the decisions rather than guessing at a plan. The key
structural point: **wayfinder subsumes the research and prototyping.** Its ticket types are
`research`, `prototype`, `grilling` and `task`, so walking the map is *how* those happen, in
the order the fog demands rather than as fixed stages guessed at up front. They stay
invocable on their own outside a map. A spec written from a resolved map is far deeper than
one written from a single grilling session, because every decision behind it was worked as
its own ticket.

On a smaller project the map costs more than the fog it clears. In the register the playbook
uses throughout: this is the recommended default for its size band, not a rule.

This is the PROJECT-level planning of the nested-planning model; see Lane 2 for the inner,
issue-level re-planning.

### Lane 2 - Build (day level + one session per issue)

Reshaped 2026-08-05 (superseding the 2026-08-04 per-issue loop). Two levels:

```
DAY   (one orchestrator session)
  start-dev -> scope the day -> read the board -> plan WAVES -> battle-plan HTML
    -> human reviews and pushes back
  ... issue sessions run ...
  update-docs at day end (recommended, not required)

ISSUE (one fresh session per issue)
  pickup-issue #N -> worktree + draft PR + read other drafts + load only the issue's code
    -> grill-me (hitl issues; afk issues skip it) -> to-spec -> writing-plan
    -> tdd OR subagent-driven-development
    -> commit -> CI green -> close-issue (merge, delete branch, clean worktree)

REVIEW (optional, two modes)
  A: fresh session on one PR before it lands (recommended for bigger issues)
  B: fresh session on the day's diff at day end
```

Periodically, not per issue: `improve-codebase-architecture` - at the end of a session once
in a while, at a milestone, or on a smell.

The shape, and why it hangs together:

**Parallel work runs as parallel sessions, never as agents inside one session.** Each issue
gets a fresh session opened with `pickup-issue`. Coordination is through git: **worktrees**
keep working copies apart, **draft PRs opened at pickup** make each session's claim and
progress visible to the others. This is also the shape that links most naturally to Helm
later.

**A wave is a set of issues touching different hot files**, so their sessions run in
parallel without conflicts. Hot files force order: issues sharing a file serialize into a
spine. `start-dev` cuts the waves and renders them as a battle-plan HTML (template bundled
with the skill) that the human reviews before anything starts. A wave is finished when its
tiles are **merged**, not built.

**`start-dev` was rebuilt as the day orchestrator** (2026-08-05). The old front-door
behavior - read the issue, load only the code it touches - moved into `pickup-issue`,
which also owns the worktree, the draft PR, and the look at what parallel sessions hold.

**The issue-level planning trio is `grill-me` -> `to-spec` -> `writing-plan`** - the same
tools as Project Start at a smaller altitude. `hitl` issues route through the grilling;
`afk` issues (small, decision-free) skip straight to a brief spec/plan and the build.

**The build method is a choice: `tdd` or `subagent-driven-development`** (vendored in
2026-08-05). Test-first by hand, or a fresh subagent per plan task with a review after
each.

**`verify-task-done` was cut** (2026-08-05). The gate is CI plus the issue's acceptance
criteria, run for real before closing; `close-issue` carries a "when not to merge" list
for the cases where that gate is not real.

**`code-review` is optional and flexible** (2026-08-05, revising the 2026-08-04 per-issue
default: mandatory per-issue review overkills small slices). Mode A - a fresh session on
one PR before it lands - is the researched recommendation for bigger issues
(`docs/research/2026-08-04-code-review-cadence.md` still stands: attention per review is
fixed, per-change review converges across the industry). Mode B - the day's diff at day
end - is the lighter option, reviewing already-merged code with eyes open. Either way it
annotates first, auto-applies only mechanical in-scope fixes, and **files out-of-scope
findings as new issues** rather than gold-plating. Browser driving on UI-touching diffs
stays. Heavier passes escalate to the built-in `/code-review` and `/security-review`.

**Author annotation stays** - before either pass, the agent walks its own diff and writes
down the non-obvious decisions and why; `close-issue` carries the annotations into the PR
body. Strongest single effect in the research.

**Docs move to the day level.** Issue sessions do not run `update-docs` - parallel
sessions writing one ledger file conflict. The orchestrator session closes the day with
one `update-docs` run, recommended rather than required. The PR body is each issue's
durable record.

**`close-issue` merges on green** (was `close-task`; renamed and slimmed 2026-08-05 - no
docs step, no ad hoc path). See "The merge wall" below. Ad hoc no-issue work belongs to
the Simplified flow instead.

**The cross-issue concern stays with `improve-codebase-architecture`**: a single-diff
reviewer cannot see three slices each adding a near-identical helper. Periodic
architecture passes are the fix, not batched review.

This lane is for **issue-driven work on bigger repos**. Smaller things take Lane 3, or a
bare grill-me -> to-spec -> writing-plan for work never filed as issues. **`wayfinder` is
deliberately absent here** - one issue is below the threshold where a decision map pays
for itself.

### Lane 3 - Simplified (smaller work, ad hoc work, less-technical teammates)

For less-technical teammates, simpler client projects, and any work not filed as issues.
Loops. Flow (executing-plans replaced by the build-method choice, 2026-08-05):

```
start -> grill-me -> to-spec -> writing-plan -> tdd OR subagent-driven-development
  -> code-review (if needed) -> update-docs  (loops)
```

### Issue labels: three dimensions, descriptive not routing

Settled 2026-08-04, adopting Emil's tracker convention. `to-issues` stamps one label from
each group. **Nothing gates on them** - they tell whoever reads the issue list what kind of
work each slice is.

| Group | Labels | What it answers |
|---|---|---|
| **Type** | `feature` / `bug` / `task` | What kind of work is this? |
| **Severity** | `high` / `medium` / `low` | How much does it matter? `start-dev` weighs it when cutting waves |
| **Autonomy** | `afk` / `hitl` | Is a person needed *during* the build? |

Type and severity are conventional; anyone will recognise them. **Autonomy is the one
specific to working this way**, and it answers what a normal tracker cannot: can I set this
running and walk away? The test is *during the build* - every issue gets human attention
eventually, so "a human sees it at some stage" would make everything `hitl` and distinguish
nothing.

**The default leans `hitl`** (2026-08-05): a slice where further grilling is plausible is
`hitl`; `afk` is reserved for small, decision-free slices. Downstream, `pickup-issue`
routes `hitl` through `grill-me` and lets `afk` skip it, so an optimistic `afk` means a
real decision gets guessed instead of asked.

**The `ui` label is gone.** It briefly routed work to a Playwright branch and a UI gate.
Both are gone: nothing consumed it, Emil had not seen the convention used anywhere, and
whether a change touched the interface is answered better by the diff than by a guess made
before the work started. `code-review` drives the browser when the diff shows the interface
changed.

**Why descriptive rather than routing, generally.** Labels are written at planning time,
before anyone knows what the diff will contain, so routing later work off them was routing
off a guess. `code-review` and `close-issue` decide from **what the diff actually touched**,
which is better evidence and survives a wrong label. The one soft exception is autonomy:
`pickup-issue` uses it to decide whether grilling comes first - a planning-time question,
which is what a planning-time label can honestly answer.

This supersedes V2's per-issue `afk`/`hitl` routing and the interim V3 position of a single
routing `ui` label. Provisional to the extent that the whole scheme is still to be synced
with Emil.

Human gates that remain: **planning**, and a human judging how a UI actually feels, which no
assertion captures.

### Maintenance (outside the three lanes)

`improve-codebase-architecture` is periodic maintenance: at the end of a session once in a
while, at a milestone, or on a smell - never per issue. It is the deliberate counterpart to
per-issue code review, covering what a single-slice reviewer structurally cannot see. It scans for deepening opportunities (shallow modules
that could become deep) and presents them as a visual HTML report to act on.

### Session bookends - two parallel pairs

Session skills come in two parallel pairs:

- `pickup-issue` / `close-issue` - **issue-session bookends** for Lane 2.
- `start` / `update-docs` - **everyday-session bookends** for all employees (Lane 3,
  general use, and the day-level close of Lane 2).

## 3. Full catalog table (25 skills)

Source values: `vendored-verbatim` (taken as-is from an upstream source), `lifted`
(based on an upstream skill but renamed/reshaped for S8), `custom` (net-new S8 process).
All skills are authored as first-pass drafts unless flagged otherwise.

| # | skill | lane / role | source | authored |
|---|---|---|---|---|
| 1 | `setup-skills` | Project Start (entry; **global**, not repo-level) | custom | authored |
| 2 | `setup-dev-repo` | Project Start | custom | authored |
| 3 | `update-skills` | Utility (repo maintenance) | custom | authored |
| 4 | `wayfinder` | Project Start; the default entry point for non-trivial work | vendored-verbatim (matt-pocock) | first-pass |
| 5 | `research` | Wayfinder ticket type + mid-work utility | lifted (matt-pocock) | first-pass |
| 6 | `prototype` | Wayfinder ticket type + mid-work utility | vendored-verbatim (matt-pocock; 3 files, `LOGIC.md` + `UI.md`) | authored |
| 7 | `grill-me` | Wayfinder ticket type; small-project entry; Build + Simplified | lifted (syv-ai, + matt-pocock `grilling`/`domain-modeling`) | first-pass |
| 8 | `to-spec` | Project Start + Build | lifted (base: skill(CC) `to-prd`) | first-pass |
| 9 | `visual-spec` | Project Start | custom | first-pass |
| 10 | `to-issues` | Project Start | lifted (matt-pocock `to-tickets` + syv-ai publishing) | authored |
| 11 | `start-dev` | Build (day orchestrator; rebuilt 2026-08-05, template bundled) | custom | authored |
| 12 | `pickup-issue` | Build (issue-session bookend; holds the old front-door discipline) | custom | authored |
| 13 | `writing-plan` | Build (issue level) + Simplified | lifted (superpowers `writing-plans`) | first-pass |
| 14 | `tdd` | Build + Simplified (build method) | lifted (matt-pocock / superpowers) | first-pass |
| 15 | `subagent-driven-development` | Build + Simplified (build method) | vendored-verbatim (superpowers, refs localized) | first-pass |
| 16 | `code-review` | Build + Simplified; optional, two modes | lifted (matt-pocock + superpowers) | authored |
| 17 | `close-issue` | Build (issue-session bookend); merges on green; was `close-task` | custom | authored |
| 18 | `start` | Simplified (session bookend) | vendored-verbatim (superpowers / skill(CC)) | first-pass |
| 19 | `update-docs` | Simplified + day-level bookend; was `update-ledger` | lifted (skill(CC)) | authored |
| 20 | `systematic-debugging` | Mid-work utility (alias: `diagnosing-bugs`) | lifted (matt-pocock / superpowers) | first-pass |
| 21 | `improve-codebase-architecture` | Maintenance (outside the lanes) | lifted (matt-pocock) | first-pass |
| 22 | `writing-for-agents` | Meta; governs any document an agent reads; was `write-a-skill` | vendored-verbatim (matt-pocock, 2 files; house rules appended in `S8-RULES.md`) | authored |
| 23 | `wizard` | Utility (manual human procedures; likely onboarding-track engine) | vendored-verbatim (matt-pocock, `template.sh` bundled) | authored |
| 24 | `to-questionnaire` | Utility (stakeholder loop out of a grilling session) | lifted (matt-pocock; output changed to fillable S8 HTML) | authored |
| 25 | `explain-like-im-ten` | Utility (re-explain in plain language) | lifted (matt-pocock `wait-what`, renamed, ELI10 register) | authored |

Counts: **25 skills total** - 6 `vendored-verbatim`, 12 `lifted`, 7 `custom`. One build.

Removed 2026-08-05: `assign-issues` (multi-person orchestration, parked pending the
Emil/Martin sync), `verify-task-done` (cut - the gate is CI plus the issue's acceptance
criteria, run before closing), `executing-plans` (superseded by
`subagent-driven-development` as the Simplified build method).

**Skill files carry no metadata (decided 2026-08-05).** No tag lines, no source notes, no
positioning blockquotes - a skill file is a prompt, every line of it loads on invocation,
and metadata kept in two places drifts (it did, twice, in two days). This catalog is the
sole record: sources in the table above and section 4, the interaction axes below.
Upstream names appear here and nowhere else.

### Per-skill interaction axes (moved out of the skill files, 2026-08-05)

`human` = what a person does during the skill. `automatic` = who may invoke it; "manual"
skills carry `disable-model-invocation: true` in frontmatter, which is the enforcing
switch - this column just records intent.

| skill | human | automatic |
|---|---|---|
| `setup-skills` | reports and stops | manual, never self-invoked |
| `setup-dev-repo` | asks a few questions, otherwise runs through | manual - creates repos, installs deps, writes hooks |
| `update-skills` | confirms before applying | manual, never self-invoked |
| `wayfinder` | HITL - the map is worked with a person | manual, never self-invoked |
| `research` | AFK once the question is handed off | auto-eligible (unlocked 2026-08-04 so wayfinder can fire it) |
| `prototype` | HITL to pick the branch and judge; AFK to build | auto-eligible (unlocked 2026-08-04) |
| `grill-me` | HITL | manual (typed, not self-triggering) |
| `to-spec` | configurable - the gate around it is workflow-defined | manual to start, then offers visual-spec |
| `visual-spec` | AFK to produce, a person consumes | offered, not forced |
| `to-issues` | approves the breakdown before publishing | manual |
| `start-dev` | scopes the day, then reviews the battle plan | manual, never self-invoked |
| `pickup-issue` | names the issue; hands off after loading | auto-eligible (fires when the user names an issue to work on; flipped 2026-08-06) |
| `writing-plan` | AFK | auto-eligible |
| `tdd` | AFK | auto-eligible |
| `subagent-driven-development` | AFK between checkpoints; picks it over tdd | auto-eligible |
| `code-review` | configurable; auto-applies mechanical in-scope fixes only | auto-eligible |
| `close-issue` | none in the normal path | auto, including the merge |
| `start` | AFK to read, then asks what to work on | auto-eligible (fires on "where were we" / session-start phrasings; flipped 2026-08-06) |
| `update-docs` | AFK to produce, the user reads the result | manual |
| `systematic-debugging` | AFK | auto-eligible |
| `improve-codebase-architecture` | HITL - the user picks which finding to act on | manual |
| `writing-for-agents` | HITL | auto-eligible (fires when a skill, `CLAUDE.md` or `AGENTS.md` is being edited) |
| `wizard` | confirms the stage list; runs the finished script alone | auto-eligible (fires at a manual-procedure wall) |
| `to-questionnaire` | answers two questions, then sends the doc | manual |
| `explain-like-im-ten` | reads the re-pitch | manual |

Four skills left the set on 2026-08-04. `helm-to-tasks` was parked in `docs/helm-parked.md`.
The other three were merged into skills that were already doing the same job at the same
moment: `choose-issue` into the old `start-dev`, the old doc-sync skill into what is now
`update-docs`, and `verify-with-playwright` into `code-review`. `visual-map` was renamed
`visual-spec`. Three more left on 2026-08-05 (see the note under the table above).

## 4. Source taxonomy

The upstream ecosystems, researched before any skill was drafted, collapse into three
source values in the table above. Provenance notes:

| value | meaning | upstream |
|---|---|---|
| `vendored-verbatim` | taken as-is (or near-as-is) from an upstream source | `wayfinder`, `prototype`, `start`, `subagent-driven-development` (superpowers; plugin-specific references localized), `wizard` (matt-pocock), `writing-for-agents` (matt-pocock; house rules appended in `S8-RULES.md`) |
| `lifted` | based on an upstream skill but renamed and reshaped for S8 | `grill-me`, `to-issues`, `to-spec`, `tdd`, `code-review`, `systematic-debugging`, `writing-plan`, `research`, `update-docs`, `improve-codebase-architecture`, `to-questionnaire`, `explain-like-im-ten`. |
| `custom` | net-new S8 process (no public precedent) | `setup-dev-repo`, `setup-skills`, `update-skills`, `start-dev`, `pickup-issue`, `close-issue`, `visual-spec` |

Two provenance findings from the original research still hold:

- **`syv` is a personal fork of `matt-pocock`.** The local `skill(CC)` set (installed via
  `npx skills add syv-ai/agentic-coding-playbook`) mirrors Matt Pocock's skills almost
  line for line. So `lifted`-from-`skill(CC)` entries are functionally matt-pocock-derived,
  already vendored onto the machine. Where V3 renames or reshapes one (e.g. `to-prd` ->
  `to-spec`), the delta is what makes it `lifted` rather than `vendored-verbatim`.
- **Matt Pocock's user-invoked vs model-invoked axis** maps onto how skills are reached in
  the lanes (typed/orchestrating vs auto-eligible mid-work), though V3 no longer tracks it
  as a per-skill tag.

Naming note: the canonical directory names are `tdd`, `writing-plan`,
`subagent-driven-development`. `systematic-debugging` is one merged skill;
`diagnosing-bugs` is an alias only.

## 5. Decisions settled (2026-07-27)

Every gating question that blocked these skills has been answered. Recorded here because
several reverse earlier design positions, and the old framing survives in dated notes.

| Skill | Settled |
|---|---|
| `setup-dev-repo` | **Merged from `create-repo` + `project-setup`.** Looks first: creates the repo (EXT/INT naming, labels, license) or discovers an existing one. Then asks complex-or-simple, wires stack, dev env and commit gate, mirrors the checks in CI, proves the gate blocks, and seeds a slim `CLAUDE.md` recording the commands it verified. Dev projects only. |
| `setup-skills` | **The one global skill**, because a skill cannot install itself. Runs `npx skills add`, confirms the skills resolved, checks git and `gh auth`, then stops without chaining onward. |
| `update-skills` | Repo-level. Pulls the newest skills, showing what changed and asking before applying. This is the update path that per-repo install otherwise lacks. Installed skills carry no version stamp, so it diffs contents three ways against a git baseline, and names local edits before overwriting them. |
| `pickup-issue` (relevance) | Decided by searching as the work reaches it. No dependency-graph walk, no relevance manifest. (Settled for the old `start-dev`; the discipline moved here 2026-08-05.) |
| `update-docs` | Was `update-ledger`; absorbed the old doc-sync skill (2026-08-04), renamed (2026-08-05). Ledger and handoff always; project docs only where the work drifted; an ADR when a decision outlives the work and passes the three locks. |
| `grill-me` | Absorbed `grill-with-docs`. Ledger always; an ADR only when the decision outlives the work. **Rounds, not one-per-turn (2026-08-06):** each round asks the whole frontier of currently-answerable questions in the numbered ❓/➡️ format; hard questions get a message to themselves, quick confirmations travel grouped. |
| `to-spec` | Synthesis-first, never a re-interview. Name stands despite the upstream collision. |
| `visual-spec` | **Optional**, human-invoked. Not a gate. Retires the earlier "sign-off before `to-issues`" position. |
| `to-issues` | Publishes slices as real GitHub sub-issues of the spec, with blocking edges between siblings **and re-wired edges on existing issues** (2026-08-05). Labels each on type, severity and autonomy - `hitl` by default where further grilling is plausible - read off the slice rather than asked per issue, confirmed once in the existing approval gate. Template gained a Hot files section for wave planning. |
| `code-review` | **Optional, two modes** (2026-08-05): a fresh session on one PR before it lands (recommended for bigger issues), or the day's diff at day end. No line-count trigger. Annotates the diff first. Auto-applies mechanical in-scope findings only; out-of-scope findings become new issues; logic, auth, secrets, data and migrations are reported, not fixed. Drives the browser when the diff touched the interface. |
| `close-issue` | Was `close-task`. Waits for CI, then **merges on green** (2026-08-04), deletes the branch and cleans the worktree (2026-08-05). No docs step (day level owns docs) and no ad hoc path (Simplified owns no-issue work). Carries a "when not to merge" list for cases where the gate is not real. |
| `start-dev` | **Rebuilt 2026-08-05 as the day orchestrator.** Scopes the day, reads dependencies / hot files / sizes, cuts waves of parallel issues, emits a battle-plan HTML (bundled TEMPLATE.html) for human review. The old front-door duties moved to `pickup-issue`. |
| `pickup-issue` | New 2026-08-05. One issue, one fresh session: worktree + draft PR at pickup, reads the other drafts, loads only the code the issue touches, then grill-me for `hitl` or straight to build for `afk`. |

### Adopted from Matt Pocock skills v1.2 (2026-08-06)

His v1.2.0 (released 2026-08-05) was crawled in full; the evidence base lives in
`docs/research/2026-08-05-matt-pocock-aihero/` (63 note files incl. verbatim skill
sources and the release-video transcript). Adopted after a grilling session:

- **`grill-me` asks in rounds** along the question-graph frontier (see its row above).
  Ungrillable questions route to `prototype` mid-session.
- **`writing-for-agents` vendored** (replacing the custom theory-free `write-a-skill`):
  the two loads, context pointers, completion criteria, leading words, the no-op test,
  the cache rule. Model-invocable. S8 catalog law kept in `S8-RULES.md`.
- **Three new skills:** `wizard`, `to-questionnaire` (output changed from markdown to a
  fillable S8-styled HTML with local autosave + answer export), `explain-like-im-ten`
  (his `wait-what`, renamed to the house register).
- **`improve-codebase-architecture`** gained his YAGNI scoping filter and the
  last-~20-commits exploration bias; **`start`** gained the phase-boundary tree
  (continue > clear > handoff > subagent > compact).
- **Description convention adopted** from his skill mechanics: model-invoked skills carry
  trigger-branch descriptions; user-invoked skills carry a human-facing one-liner.
  Applied to skills touched in this wave; the rest are swept as the walkthrough visits
  them.
- **The no-em-dash rule is removed** from the house conventions (2026-08-06), which is
  what lets vendored files be truly verbatim.
- Deliberately not adopted: his `grilling`-as-separate-primitive split (one front door
  here), `triage`, `teach`, Codex sidecar YAMLs, marketplace distribution (task #8
  evaluates the install path).

### The merge wall is gone (2026-08-04)

**`close-issue` merges on green.** No human gate on trunk promotion.

The history matters, because this is the third position on it. Removed on 2026-07-27 in
favour of merge-on-green, reinstated the same day because Helm hard-codes a *never-push*
invariant, and now removed again. Two things changed:

- **Helm is parked**, so "the engine forbids it" is no longer an argument the playbook has
  to respect. It becomes a Helm question, for the Helm track.
- **Kasper does not look at merges in GitHub.** A gate nobody stands at is not protecting
  anything; it is where work stops moving. That is a fact about actual use, and it is what
  made the wall indefensible rather than merely inconvenient.

**Provisional: "build it like this for now", and to be synced with Emil and Martin.**

What it rests on, unchanged from the first reversal because it was always the real
argument: *auto-promotion is safe exactly to the degree the acceptance checks are complete.*
This is not a judgement that the agent's code is trustworthy, it is a bet on the checks.
With `verify-task-done` cut (2026-08-05), the gate is narrower and every part of it is
load-bearing:

- **CI**, which `setup-dev-repo` wires and `close-issue` waits on - the last thing between
  a change and trunk, and unlike a local hook it cannot be bypassed.
- **The issue's acceptance criteria, run for real** before closing - written by
  `to-issues`, executed in the build session, never concluded from reading the code.
- `close-issue`'s **"when not to merge"** list for the cases where the gate is not real:
  no meaningful project checks, no acceptance criteria, CI not configured, or the change
  touches auth, secrets, payments, migrations or data deletion.
- **Optional pre-merge review** (code-review mode A) for bigger issues, in a fresh session
  on the PR.

The remaining human gates are **planning** (the battle-plan review, the grilling) and **a
look at interface changes**.

### Distribution: one global skill, everything else per repo

Settled 2026-07-29 after two earlier answers. Skills install **into the repo**:

```
npx skills add solution8-com/INT-s8-agentic-playbook
```

Each repo therefore pins the version that built it - a client project from last year keeps the
skills it was set up with. The cost is that updates do not propagate, which is what
`update-skills` exists for.

`setup-skills` is the single exception and lives globally, because a repo-level skill cannot be
what installs repo-level skills. It encodes no workflow - it runs an install and checks three
things - so there is very little in it to drift. The one stale-able detail is the hardcoded
repo path, which is also why the variant build carries transform rule (3) above: the public
build installs from `solution8-com/s8-agentic-playbook` instead.

Which command exists tells you which situation you are in: no skills installed means
`/update-skills` does not exist, so the global one is the only option.

### Skills removed

Ten skills were cut on 2026-07-27. With three setup skills added (`setup-dev-repo`, which
merged `create-repo` and `project-setup`, plus `setup-skills` and `update-skills`), the
catalog went from 34 to 27:

| Cut | Why |
|---|---|
| `grill-with-docs` | An 11-line stub delegating to two other skills. Merged into `grill-me`. |
| `grilling` | Internal plumbing behind the grill skills, never invoked directly. |
| `read-docs` | `start-dev` run a second time. Re-running `start-dev` is the refresh path. |
| `update-issue` | `gh issue edit` wearing a skill costume. The agent does it inline. |
| `implement` | Thin orchestrator over `tdd` and `code-review`, which the lane already sequences. |
| `domain-modeling` | Overlapped `grill-me` and `wayfinder` on most projects. |
| `mega-research` | Never left draft. |
| `brainstorming` | Already marked legacy, absorbed into `wayfinder`. |
| `create-repo` + `project-setup` | Merged into `setup-dev-repo`. Two entry points meant knowing which to run, and on an existing repo the wrong one did nothing useful. |

## 6. Changed since V2

- **V2 was pre-authoring; V3 is fully authored.** V2 had zero `SKILL.md` files (a research
  + draft-spec document). All 25 skills now exist as authored files on disk.
- **Helm came in, then went back out.** V3 added an INTERNAL vs EXTERNAL/public split built
  from strippable `## Helm behavior (internal only)` sections plus the internal-only
  `helm-to-tasks` skill. On 2026-08-04 all of it was parked in `docs/helm-parked.md`,
  because Helm is half built and the playbook was anticipating it rather than documenting
  it. One build for now; the variant convention returns with Helm.
- **Two lanes became three, split by audience.** V2 had Project Start + Agentic
  Engineering. V3 adds the **Simplified** lane (gentler, for less-technical teammates) and
  renames Agentic Engineering to the Build lane.
- **AFK/HITL stopped being a router.** V2 routed each issue with an `afk`/`hitl` label chosen
  up front. V3 first replaced this with a single `ui` work-type label, then (2026-08-04)
  settled on **three descriptive axes** adopted from Emil's tracker convention: type
  (`feature`/`bug`/`task`), severity (`high`/`medium`/`low`), and autonomy (`afk`/`hitl`)
  for whether a person is needed *during* the build. The `ui` label is gone entirely. The
  labels came back; the routing did not. Nothing gates on them - `code-review` and
  `close-issue` decide from the diff. See "Issue labels" above. The remaining human gates
  are planning, and a person judging how a UI actually feels.
- **New skills since V2:** `wayfinder`, `start`, `update-docs`, `writing-plan`,
  `improve-codebase-architecture` as explicit maintenance; later `pickup-issue` and
  `subagent-driven-development` (2026-08-05). Also added then cut again:
  `verify-task-done` and `executing-plans`.
- **Renames / shape decisions settled:** `to-prd` -> `to-spec`; canonical dir names `tdd`,
  `writing-plan`; `systematic-debugging` merged (`diagnosing-bugs` alias); `close-task`
  briefly a superset of the old V2 `close-issue`, before returning to the `close-issue`
  name in its 2026-08-05 slimmed form.
- **`improve-codebase-architecture` moved out of the lanes** into milestone/smell-triggered
  maintenance.
- **Nested planning made explicit:** project-level planning in Project Start, issue-level
  re-planning at the head of the Build lane.

## 7. Appendix - original V2 per-skill research (pre-authoring)

> **Historical.** This section records the research done before any skill was written, and
> is kept as a dated record rather than maintained. It describes 34 skills, several of which
> were cut on 2026-07-27, and predates the decisions in section 5. Where the two disagree,
> section 5 is current.

> Retained for provenance. These notes predate the authored `SKILL.md` files and use the
> older framing (s8-dash naming, per-issue AFK/HITL labels, "MEGA Research" placeholder).
> Where they disagree with the sections above or with a skill's own `SKILL.md`, the newer
> source wins. They are kept because the behavior sketches and source reasoning are still
> useful research.

### Project Start lane

**`create-repo`** - source: `custom`. Runs when a user creates a new repo from inside the
app (not a CLI-first flow). Applies the team naming convention to the repo name and initial
scaffold, baked into the skill rather than read from config. No public precedent.

**`project-setup`** - source: `custom`, patterned after the local `setup` skill and
`setup-syv-skills`'s onboarding shape. Scaffolds git, installs/points at the repo skills,
and seeds a slim `CLAUDE.md` following the "seed a slim pointer, don't force a fat one"
pattern. Runs after `create-repo` or when it detects a repo with no skills wired up.

**`start-dev` (= `read-docs`)** - source: `custom`. Fires when a developer picks up an
issue. Reads project docs plus only the code relevant to the issue - explicitly never the
whole repo. First stage of the per-issue lane. Exposed as two entry points: auto on issue
pick (`start-dev`) and manual mid-work (`read-docs`).

**`update-docs`** (standalone) - source: `custom`. Mid-work counterpart to `read-docs`:
syncs docs when the work has drifted from what was documented. Distinct from
`update-ledger`, which only handles the dev-session ledger + handoff.

**`grill-with-docs`** - source: matt-pocock (his `grill-with-docs`: a grilling session
that also sharpens `CONTEXT.md` and captures decisions as ADRs). The S8 delta is wiring
into the ledger/ADR memory layer.

**`grill-me`** - source: matt-pocock (via the local `skill(CC)` copy, near-verbatim his
`grilling`/`grill-me`). Lighter sibling of `grill-with-docs`: same relentless
one-question-at-a-time loop, but writes nothing to ADRs or a glossary.

**`to-spec`** - source: `lifted`, renamed from the local `to-prd`. Turns the conversation
into a durable spec and publishes it (GitHub issue or file). Collides in name only with
Matt Pocock's own `to-spec`, which synthesizes with no interview. Defining behavior: runs
`visual-spec` at the end.

**`visual-spec`** - source: `custom`. Produces a self-contained HTML overview (S8 house
style) of the spec for human review. Rhymes with matt-pocock's "present findings as a
visual HTML report" pattern.

**`to-issues`** - source: `lifted`, base is the local `to-issues` (matt-pocock's
`to-tickets`): breaks a plan/spec into independently-grabbable vertical-slice issues. V2
delta was the routing label stamped on each issue; V3 replaces per-issue labels with the
work-type AFK/UI split.

**`assign-issues`** - source: `custom`. A popup: how many people, optional per-person
strengths, and it divides the freshly created issues among them. Matt Pocock's closest
relative, `wayfinder`, splits work across sessions, not people, so it is not the same shape.

### Agentic Engineering lane

**`implement`** - source: matt-pocock (his `implement`: build the work described by a spec
or tickets, driving `tdd` at pre-agreed seams and closing with `code-review` before
committing). In V3 this is a thin, standalone-only orchestrator.

**`tdd`** - source: matt-pocock / superpowers (both ship one; the local `skill(CC)` `tdd`
is present and MP-derived). Red-green-refactor, one vertical slice at a time.

**`code-review`** - source: `lifted`. Base is Matt Pocock's `code-review` (two parallel
sub-agents: Standards - repo conventions + a Fowler smell baseline - and Spec - does the
diff faithfully implement the issue) fused with superpowers' receiving/requesting-code-review
discipline. It auto-applies the fixes it finds; the open question is how much auto-apply is
safe (Q12).

**`systematic-debugging` / `diagnosing-bugs`** - source: matt-pocock / superpowers. A
disciplined reproduce -> isolate -> hypothesize -> instrument -> fix -> regression-test
loop. One merged skill in V3; `diagnosing-bugs` is an alias.

**`close-task`** - source: `custom`. Superset of the old `close-issue`. Always updates
docs; if there is an issue, chains commit -> PR -> resolve issue -> delete branch,
respecting the project's auto-merge toggle, then auto-exits the session. Also works with no
issue attached. Its automation must stop short of the human-only merge / branch-delete wall.

### Mid-work utilities / future / meta

**`research`** - source: matt-pocock (his `research`: investigate a question against
high-trust primary sources and capture findings as a cited Markdown file, run as a
background agent). Narrower than `mega-research`.

**`mega-research`** (was "MEGA Research") - source: `custom`, still a **draft**. A thin
orchestrator answering "has someone already built this?" over `deep-research` + `gh-stars`
+ `deepwiki` + one net-new `gh-search` primitive. Not all underlying tools are built yet.

**`write-a-skill`** - source: `lifted` from the local `skill(CC)` copy (informed by matt-
pocock's `writing-great-skills` and superpowers' `writing-skills`). Meta-skill for
authoring a `SKILL.md` with proper frontmatter, progressive disclosure, and a discoverable
description.

## 8. Sources consulted

- Local skill files under `~/.claude/skills/*/SKILL.md` (the syv/`agentic-coding-playbook`
  collection).
- The `superpowers` plugin skills present in this environment.
- `https://github.com/mattpocock/skills` and its raw `README.md` on `main`.
- The originating PRD and ledger for the lane framing, the custom-skill contract, and the
  memory/hard-wall model.
- The 25 authored `SKILL.md` files in this directory (V3).
