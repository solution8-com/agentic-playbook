# Tools

The MCPs, CLIs and plugins worth adding to a Claude Code setup. Almost all of it is optional. Three
things are not: [`gh`](#github-gh), which several skills read and write GitHub through,
[Playwright](#playwright), which `verify-feature` drives the browser with, and Python 3, which the
`verify-feature` report builder runs on. Python 3 ships with macOS and every Linux distribution, so
in practice it is already there.

| Tool | Kind | What it's for |
|---|---|---|
| [Context7](#context7) | MCP | Current library documentation |
| [Playwright](#playwright) | MCP | A real browser to drive |
| [Supabase](#supabase) | MCP | Your database, queryable |
| [n8n](#n8n) | MCP | Automations, and their failures |
| [Vercel](#vercel) | MCP | Deploys, build logs, preview URLs |
| [Miro](#miro) | MCP | Boards read and written in place |
| [GitHub](#github-gh) | CLI | Issues, PRs and CI from the terminal |
| [Azure](#azure-az) | CLI | Azure resources and deployments |
| [Postgres](#postgres-psql) | CLI | Direct database queries |
| [context-mode](#context-mode) | Plugin + MCP | Big output kept out of the conversation |
| [Caveman](#caveman) | Plugin | Shorter replies |
| [Language servers](#language-servers) | Plugin | Real types instead of grep |

## Reviewing what you install

An MCP server or a plugin is executable instructions from the internet, running with your agent's
access to your machine and your repos. Review each one **once, before it first runs**. Third-party:
read what it does at install time. Your own team's: review it in the change that adds it. After that
one review, trust it and move on - a rule you re-litigate every session is a rule nobody keeps.

## MCPs

An MCP gives Claude a new set of tools: a database it can query, a browser it can drive.

**Keep the ones you rarely use switched off.** Every enabled MCP loads its full set of tools into
every session whether you touch them or not, so a long list of live MCPs makes each conversation
more expensive before you have typed anything. Install what looks useful, leave most of it off,
and switch one on for the project that needs it.

### Context7

> Stops Claude writing confident code against an API that changed six months ago.

Claude's knowledge of any library is frozen at whenever it was trained. It will write against an
old API and give you no warning, because from its side nothing looks wrong. Context7 fetches the
library's real documentation at the moment you ask, so the answer comes from today's docs rather
than from memory.

Most valuable on fast-moving frameworks, on anything you have upgraded recently, and any time
Claude writes code that looks completely reasonable and does not run.

```
claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key <key>
```

### Playwright

> Turns "this should work" into "I watched it work".

Gives Claude a real browser it can drive: open a page, click through a flow, fill a form, take
screenshots, read the console. It matters most on frontend changes, where a passing typecheck
proves very little.

The `verify-feature` skill runs on this one. Worth configuring it to omit image responses - Claude
asserts against the accessibility tree, and the screenshots are there for you to look at rather
than for the model to read.

```
claude mcp add playwright -- npx -y @playwright/mcp@latest
```

### Supabase

> See the real shape of the data before writing code against it.

Connects Claude to your Supabase project: inspect tables, run queries, apply migrations, read
logs. It saves pasting schemas into the chat, and it is the difference between assuming a column
is never null and knowing it.

```
claude mcp add supabase -- npx -y @supabase/mcp-server-supabase@latest
```

### n8n

> Best at the debugging end, where the question is which node died.

Lets Claude build and inspect n8n automations directly: create a workflow, check how a node is
configured, read what happened in a run that failed. Useful when the job is wiring services
together rather than writing code.

```
claude mcp add n8n -- npx n8n-mcp
```

### Vercel

> The deploy answer without opening a dashboard.

Deployments and preview builds. Claude can see whether a deploy went green, read the build log
when it did not, and find the preview URL for a branch. Most useful while prototyping, when you
are pushing often.

```
claude mcp add --transport http vercel https://mcp.vercel.com
```

### Miro

> Saves transcribing a board by hand.

Reads and writes Miro boards. If the planning for something lives on a board, Claude reads the
stickies itself and can write results back.

One gotcha: the tag pills on a sticky only come back when you fetch that sticky individually, so a
bulk read of a board will quietly miss them.

The endpoint moves, so take it from Miro's own MCP documentation.

## CLIs

Command-line tools. Claude drives a terminal well, and unlike an MCP a CLI costs nothing while
you are not using it.

### Status line (`statusline.sh`)

> Ships in this repo. The context gauge the modules tell you to keep visible.

[`statusline.sh`](./statusline.sh) prints the model, the repo and branch, your usage windows, and a
context bar that names the zone it is in: SMART, DUMB, DANGER, COMPACT. Its thresholds are the ones
in [*The context window*](../modules/m1-the-context-window.md), at 40, 60 and 80 percent, so the bar
and the module say the same thing.

Hand the file to Claude and ask it to wire it up, or point `statusLine.command` at it yourself in
`~/.claude/settings.json`. It needs [`jq`](#jq). The usage-window segments appear on Pro and Max
plans only.

### jq

Reads JSON on the command line. Worth having on its own, and the status line above will not run
without it. `brew install jq`.

### GitHub (`gh`)

> The one to install first. Several skills stop working without it.

Issues, pull requests, CI runs, releases, all without leaving the terminal. `pickup-issue` reads
an issue and its comments through it, `review-suite` files its findings as new issues, and
`verify-feature` waits on CI with it.

Run `gh auth login` after installing, or none of that works.

```
brew install gh && gh auth login
```

### Azure (`az`)

> Predictable commands, and Claude can read the output straight back.

Manage Azure from the terminal: resources, deployments, configuration, logs.

If you also run the Azure MCP, you probably do not need both. The CLI covers the same ground
without costing context in every session.

```
brew install azure-cli
```

### Postgres (`psql`)

> Settles whether a bug is in the code or in the data.

Query a database directly. Instead of inferring what is in a table from migration files, Claude
can look - which is usually the first fork in a debugging session.

`libpq` gives you the command-line tool on its own. Install the full Postgres package only if you
want a server running locally too.

```
brew install libpq
```

## Plugins

Installed inside Claude Code with `/plugin`.

### context-mode

> One long test run can cost more room than the code you are working on.

Big commands produce big output, and by default all of it lands in the conversation and stays
there for the rest of the session. context-mode runs the command in a sandbox and hands Claude
only the part that answers the question.

Most valuable on log-heavy work: test runs, build output, large data files, long git histories.

```
/plugin marketplace add mksglu/context-mode
```

### Caveman

> Filler out, code and errors exact.

Makes Claude answer tersely. Over a long session that adds up.

Worth knowing the published savings are disputed: the project advertises 65%, while JetBrains
measured 8.5% across 86 real coding tasks. The gap is that the big number comes from chat-style
question answering, and in agentic coding most of the tokens are code and tool output, which does
not compress.

```
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
```

### Language servers

> Without one, it is searching for text and inferring the rest.

Gives Claude the same information your editor has: real types, go-to-definition,
find-all-references. Guessing goes wrong exactly where you would expect - overloaded names,
re-exports, anything generic.

Install the one your project speaks. The marketplace carries around twenty, including Go, Rust,
Java and C#.

```
/plugin marketplace add boostvolt/claude-code-lsps
/plugin install vtsls@claude-code-lsps      # TypeScript
/plugin install pyright@claude-code-lsps    # Python
```
