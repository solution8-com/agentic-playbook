# Hands-on guide 1 - Setting up your Claude environment

The cards (modules 1-9) say *why*. This says *how*, with the actual commands and file names.
It is dated on purpose - tools change, and this page changes with them. Written Aug 2026
against Claude Code as it is now.

## The whole flow in one picture

```
idea ->  grill-me  ->  to-spec  ->  to-issues  ->  pickup-issue  ->  implement  ->  YOU review & merge
         (interview)   (write it   (tickets       (read ticket,     (build, test,
                        down)       + labels)      set up space)     check, commit)
```

A suggestion, not a pipeline - skip what doesn't fit the task. Every step is a skill in the
`s8-playbook` plugin; install commands live in the plugin's README.

## Your instructions files

Claude reads these automatically, in this order:

1. `~/.claude/CLAUDE.md` - **global**: how *you* work, everywhere. Applies to every project.
2. The project's `CLAUDE.md` - what's true of *this* project: how to run it, what's unusual.
3. `CLAUDE.local.md` - personal overrides for one machine; not committed.

The rule (module 3): global says how you work, the project file says what the project is,
and neither repeats what the code already shows. Keep each to one screen - every line is
read every session, so every stale line does damage every session. And don't let a
generator write this file for you: generated files dump everything they can see, and you
pay for every line forever. Start nearly empty and grow it from real corrections
(`setup-repo` seeds a lean one).

## What a well-set-up repo looks like

- `CLAUDE.md` - one screen, see above. `setup-repo` seeds it.
- `docs/` - only what the repo genuinely needs. Session state lives in the tracker and the git
  history; `handoff` writes the leftovers to a temp file rather than into the repo.
- `CONTEXT.md` - a glossary, only if the project has real domain vocabulary.
- `.claude/` - settings, and `reports/` where the review and verification reports land.
- One command that runs the tests. If checking is hard, checking stops happening (module 1).

## The status line - your context gauge

Run `/statusline` and have it show at least the **model** and **context usage**. The context
gauge is the one instrument you should always see (module 2: sessions get worse before they
get full). Config lands in `~/.claude/settings.json` under `statusLine`.

## Hooks in ten lines

A hook is a small program that runs automatically on every action (module 3: a written rule
is a wish, an automatic check is a wall). Config: `settings.json`, under `"hooks"`.

- **Before an action** (`PreToolUse`): your script gets the action; exit code 2 *blocks* it
  and the reason is shown to the agent. Use for: dangerous commands, secrets, the live
  system.
- **After an edit** (`PostToolUse`): run the formatter, so style enforces itself and leaves
  your instructions file entirely.

Start with one blocking hook for the single action that would hurt most, not a rule system.

## The pipeline - same checks, twice

- The **commit gate** runs the checks locally before a change is saved; **CI** runs the same
  checks on the server for every branch and merge. `setup-repo` wires both and proves
  the gate actually blocks.
- Keep the two identical. A check that exists only in CI gets discovered late; one that
  exists only locally proves nothing to your team.
- Green counts on the exact version being merged - see guide 2, "Finishing a change".
- Agents *inside* the pipeline (triggered by a failing build, handling incidents) are real
  and coming - and the highest-risk end of autonomy. Only behind scoped rights, hooks and
  human gates; the playbook deliberately doesn't teach it yet.

## Permissions - the everyday posture

Cycle modes with Shift+Tab. The sane default day (module 6):

- **Accept edits** inside containment - the agent edits and runs freely *on its own branch*.
- **Plan mode** when you want it to look and think before touching anything.
- **Ask-everything** only while you're new and still reading the prompts.
- **Bypass everything** only in a sandbox you could delete without a thought.

## Worktrees - a room per agent

Two sessions working in one checkout corrupt each other - they share one working state, so
you get a commit amended onto the *other* session's work, or changes that simply vanish. A
worktree gives each session its own folder and its own branch. Two ways to get one (module 6):

- `claude --worktree` (or `-w`) starts the session in a fresh worktree with its own branch.
- In the flow, `pickup-issue` sets one up per issue - you don't have to think about it.

Know the limit: a worktree isolates *files only*. Stashed changes are shared across all
worktrees (prefer a commit on the branch over a stash), and so is everything outside git -
ports, a local database, `.env` files. Two parallel agents can still fight over those.

## Tools

MCPs, CLIs and plugins - what we actually recommend and how to install each - live in
`TOOLS.md` in the plugin repo. Two rules:

- Connect only what the day's work needs: every connected tool eats context (module 2).
- Review every extension **once, before it first runs**. An MCP server or plugin is
  executable instructions from the internet. Third-party: read what it does at install
  time. Your own team's: review it in the change that adds it. After that one review,
  trust it and move on.
