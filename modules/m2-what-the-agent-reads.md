# What the agent reads

A senior developer joins on Monday. You hand them the onboarding page and they read it once. Two
other things shape their first pull request: the code they read on the way there, and the build
that rejects it at four o'clock. An agent learns from the same three sources, in the same order of
importance. It starts from nothing each session, so those three are all it has.

**In this module:**

- What decides the result: the material and the tools you hand over
- The three surfaces it reads: your instruction file, your code, your checks
- Why a check beats a written rule for the expensive mistakes

## Equipping the agent

**Clever wording was a workaround for weak models. The material you hand over decides the result
now.**

Phrasing once carried the result, because models were weak enough that the wrapper mattered. That
advice has expired. You equip the model instead: the most relevant information you have, and tools
to find the rest.

Give the agent a way to run the app or query the database, and it checks its answer. Without that
access, the same model guesses in the same confident voice. Fit matters more than quantity: every
tool takes room in the context window, used or not. Prefer the tools that show the agent the real
system.

In plain terms: better material moves the result, not better wording.

## Three surfaces the agent reads

**Three things shape what the agent writes: its instruction files, your codebase, and your
automatic checks.**

```mermaid
flowchart LR
    I[Instruction files<br><i>read every session</i>] --> P[What the agent<br>works from]
    C[The codebase<br><i>read while it works</i>] --> P
    H[Automatic checks<br><i>answer on every action</i>] --> P
    P --> O[The code it writes]
```

**Instruction files** are the standing brief. In Claude Code that file is `CLAUDE.md`, read at the
start of every session. That makes it the most valuable text you own, and the most expensive place
to be wrong. A good line pays back every day, a stale line costs every day, and every line takes
room the agent needs.

This has been measured. A repository instructions file did not generally improve task success, and
it added over 20% to the cost of every run. The agent followed the instructions well, but the
repository *overview* did not help, because the agent can see the folder layout by looking. So keep
what stays true and what the code does not show: the non-standard convention, the reason behind an
odd-looking decision. Cut the tour. In our experience one screen is a good target, re-read monthly,
because nothing errors when a line goes stale.

This is also why a generated file is a bad start. A generator writes down everything it can see -
the folder tour, the obvious conventions, the file list - which is precisely the material the
measurement found unhelpful, and you pay for every line of it on every run afterwards. Start nearly
empty and grow the file from real corrections: the times the agent got something wrong that a
sentence would have prevented.

## The codebase is the loudest of the three

**The twenty files around the edit set the pattern. You get a twenty-first that does the same.**

You can write "always handle errors properly" in the instruction file. If the surrounding code
swallows errors, you get one more file that swallows errors. The agent reads far more code than
instructions, and the code shows how the work is done here. Names and folder structure count too:
the same filename in `tests/` and in `src/core/` means two different things.

So the old disciplines are worth more now. Clear boundaries, small pieces with obvious jobs, one
consistent way of working, runnable tests: each is also a message the agent copies forward. In a
messy area it re-reads more and burns more of its window. Mess taxes every task. When output drops
off in one corner of the repo, look at that code first.

## A written rule and an automatic check

**A written rule lowers the odds of a mistake. An automatic check removes them.**

"Never run the command that erases shared history." "Always run the formatter." Written like that,
both rules are wishes. The agent can miss a rule, misread it, or lose it when a long session gets
summarised. An automatic check is a small program, called a hook, that runs on every action, blocks
the bad ones and tells the agent why. The linter is its ancestor.

|  | A written rule | An automatic check |
|---|---|---|
| Where it lives | your instruction file | a program that runs on every action |
| How well it holds | usually | always |
| How it fails | quietly, you find out later | loudly, with a reason |
| Fits | judgment calls: keep functions small | clear yes/no calls: dangerous commands, secrets |
| Costs | a line of the window, every session | a few lines of code, once |

Sort your rules by the cost of breaking each one. Write a check for the expensive ones: lost data,
a leaked password, a change to the live system. A check that fixes beats one that forbids: an
after-edit formatter enforces itself. Each rule a check enforces is a line the instruction file no
longer needs.

## What you can do

- **Hand over the material before you polish the sentence.** The relevant file, the real error, the
  actual ticket beat any wording.
- **Read your instruction file top to bottom this week.** Cut what the code shows and what stopped
  being true.
- **Fix the pattern before you scale the work.** Clean the area first if many tasks will run
  through it ([`review-suite`](../skills/review-suite/SKILL.md), `/code-review low`).
- **Turn your two or three most expensive rules into checks.** The rest stays prose.
- **Give the agent a way to check its own work**: tests, a way to run the app, read access to the
  data ([`tdd`](../skills/tdd/SKILL.md), [`verify-feature`](../skills/verify-feature/SKILL.md)).
- **Write the reasons down when you catch yourself repeating them** ([`grill-me`](../skills/grill-me/SKILL.md), [`to-spec`](../skills/to-spec/SKILL.md)).
  Repeated explanation belongs on one of the three surfaces.

## What to remember

- Clever phrasing was a workaround for weak models. Results now come from the information and
  tools you supply.
- Three surfaces shape the output: the instruction files, the codebase, the automatic checks.
- Keep in the instruction file what stays true and what the code cannot show. Cut the repo tour;
  that part has been measured.
- The codebase teaches louder than the instruction file. Mess taxes every task.
- A written rule lowers the odds. An automatic check removes them. Sort by the cost of breaking
  each rule.
