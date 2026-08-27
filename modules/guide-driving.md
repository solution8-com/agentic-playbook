# Hands-on guide 2 - Driving the agent day to day

The cards say *why*; this says *what to actually watch and do* while working. Dated on
purpose - written Aug 2026 against Claude Code as it is now.

## The context gauge

Everything the agent reads and does fills its working memory, and quality drops well before
it's full (*The context window*). So:

- Keep the gauge visible (see guide 1: status line).
- `/context` shows what's eating the window when you're surprised.
- Our house habit: start wrapping up around 40%. That number is a habit, not a law - the
  card in *The context window* says so out loud - but a shared habit beats everyone improvising.

## Session hygiene

- **One task, one session.** `/clear` when you switch tasks - it wipes the conversation and
  keeps only the instructions files.
- **`/compact`** squeezes the current conversation into a summary. Use it only when you must
  continue mid-task; a fresh session with a written handoff is almost always better.
- **Ending a work session, on a repo with code:** `handoff` compacts what only exists in the
  chat - the decisions nobody wrote down - into a note the next session opens with. It writes
  outside the repo, because the tracker and the commits already hold the rest. That is what
  makes killing a session free (*The context window*).
- **Ending a work session, on a docs or planning repo:** `update-docs` instead. There is no
  tracker and no commit history carrying the decisions, so the note has to be durable: a ledger
  entry, a handoff in the repo, and any project doc the work actually drifted from.
- **Opening one:** `start` reads whichever of the two wrote last, before it does anything else.
  A session that starts by guessing is a session that starts wrong.
- **Esc** stops the agent mid-action (Ctrl+C if Esc is ignoring you). Interrupt early - a
  wrong direction gets more expensive every minute you let it run.

## Choosing a model

The menu changes every few months - as of Aug 2026 it runs from Fable 5 at the top through
Opus and Sonnet to Haiku 4.5. The logic outlives the menu:

- **Biggest model** where judgment concentrates: planning, review, hard debugging, anything
  you'd give your most senior person.
- **Middle** for everyday building.
- **Small and fast** for mechanical bulk work: renames, formatting, simple sweeps.
- Stuck in a loop of failed attempts? Switching *up* is usually cheaper than three more
  retries. `/model` switches mid-session.

## Red flags - signs the agent is off

Each of these means stop and steer, not "hope it works out":

| What you see | What it usually means | What to do |
|---|---|---|
| The change is far bigger than the task - a "small fix" arrives as 400 changed lines | It's doing more than asked: uninvited refactoring, scope creep | Stop. Ask for the *minimal* change; put the extra ideas in a ticket comment (*Deciding before building*) |
| "Everything works as expected", no evidence | A claim, not a check | Ask for the check that could have failed: the test run, the output (*Verifying agent work*) |
| It repeats work, forgets instructions, contradicts itself | Context rot - the session is past its best | Wrap up, write the handoff, start fresh (*The context window*) |
| It delivered something quietly smaller than what was asked | Goal-shrinking under difficulty | Compare against the ticket, not against what got built (*Verifying agent work*, gate three) |
| It edited the *test* until things passed | Gaming the check instead of fixing the code | Hard stop. Restore the test, reproduce the failure, then fix (*Verifying agent work*) |
| Files far outside the task are changing | Scope drift | Stop; narrow the brief; keep it on its own branch so drift is cheap to discard (*Working unattended*) |
| Long confident explanations, nothing actually run | Guessing, not measuring | "Run it and show me" - evidence, not theory (*Verifying agent work*) |
| A vague request came back with zero questions | It guessed your meaning and built the guess | Interview first next time - that's what `grill-me` is for (*Deciding before building*) |

## Finishing a change

The flow stops at the commit on purpose: the agent builds and commits on its branch, and a
*person* decides what happens next - unless the ticket carries an `afk` label, which is that
decision made in advance (*Working as a team*: you own what you hand in). From there, two
good paths - the playbook deliberately has no default:

- **Branch, then merge it yourself.** One feature branch per issue; when the work checks
  out, merge to main and delete the branch. Right when you're the only person who'd review
  it anyway - most solo and small-team work runs this way, including most of ours.
- **Branch, then a pull request.** The PR gives review a surface: a colleague reads the
  change, the checks show green on exactly what will merge, and the approval is on record.
  Right when several people share the code, or the project is big enough that "who checked
  this?" needs an answer.

Pick per repo. The skills work with either - and with whatever your organisation's repo
settings enforce. Protected branches and required reviews beat any written convention
(*What the agent reads*: a rule is a wish, an automatic check is a wall). Whichever path: green only
counts if the checks ran on the exact version being merged, not the branch as it looked ten
minutes ago (*Verifying agent work*).

## When to watch and when to walk away

Marked the work `hitl`? Stay close and interrupt freely. Marked it `afk`? Let it run and
judge the result at the end instead - interrupting unattended work defeats the point of
labelling it (*Working unattended*). The label was the decision; make it when you create the ticket,
not in the moment.
