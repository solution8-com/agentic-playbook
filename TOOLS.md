# Tools

Things worth adding to a Claude Code setup, what each one is for, and when it earns its place.

## At a glance

| Tool | Kind | What it does |
|---|---|---|
| [Context7](#context7) | MCP | Current docs for any library, so Claude stops writing against last year's API |
| [Playwright](#playwright) | MCP | A real browser it can click through and screenshot |
| [Supabase](#supabase) | MCP | Query, migrate and inspect your database |
| [n8n](#n8n) | MCP | Build and debug automations |
| [Vercel](#vercel) | MCP | Deploys, build logs, preview URLs |
| [Miro](#miro) | MCP | Read and write the boards the planning lives on |
| [GitHub](#github-gh) | CLI | Issues, PRs, CI runs. The one to install first |
| [Azure](#azure-az) | CLI | Azure resources, deployments, logs |
| [Postgres](#postgres-psql) | CLI | Query a database directly instead of guessing at it |
| [context-mode](#context-mode) | Plugin | Keeps big command output out of the conversation |
| [Caveman](#caveman) | Plugin | Makes Claude answer tersely |
| [Language servers](#language-servers) | Plugin | Real types and go-to-definition instead of grep |
| [uv](#uv) | CLI | Fast Python environments and versions |
| [ruff](#ruff) | CLI | Python lint and format in one command |

---

## MCPs

An MCP gives Claude a new set of tools - a database it can query, a browser it can drive, a
service it can talk to.

**Keep the ones you rarely use switched off.** Every enabled MCP loads its full set of tools into
every session whether you touch them or not, so a long list of live MCPs makes each conversation
more expensive before you have typed anything. Install what looks useful, leave most of it off,
and switch one on for the project that needs it.

### Context7

Claude's knowledge of any library is frozen at whenever it was trained. It will confidently write
code against an API that changed months ago and give you no warning, because from its side nothing
looks wrong. Context7 fetches the library's real documentation at the moment you ask, so the
answer comes from today's docs rather than from memory.

Most valuable on fast-moving frameworks, on anything you have upgraded recently, and any time
Claude writes code that looks completely reasonable and does not run.

```
claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key <key>
```

### Playwright

Gives Claude a real browser it can drive: open a page, click through a flow, fill a form, take
screenshots, read the console. It turns "this should work" into "I watched it work", which matters
most on frontend changes, where a passing typecheck proves very little.

The `ui-report` skill runs on this one. Worth configuring it to omit image responses - Claude
asserts against the accessibility tree, and the screenshots are there for you to look at rather
than for the model to read.

```
claude mcp add playwright -- npx -y @playwright/mcp@latest
```

### Supabase

Connects Claude to your Supabase project: inspect tables, run queries, apply migrations, read
logs. It saves pasting schemas into the chat, and it lets Claude check what the data actually
looks like before writing code against it - the difference between assuming a column is never
null and knowing it.

```
claude mcp add supabase -- npx -y @supabase/mcp-server-supabase@latest
```

### n8n

Lets Claude build and inspect n8n automations directly: create a workflow, check how a node is
configured, look at what actually happened in a failed run. Useful when the job is wiring services
together rather than writing code, and best at the debugging end, where the question is usually
"which node did this die on".

```
claude mcp add n8n -- npx n8n-mcp
```

### Vercel

Deployments and preview builds. Claude can see whether a deploy went green, read the build log
when it did not, and find the preview URL for a branch. Most useful while prototyping, when you
are pushing often and want the answer without opening a dashboard.

```
claude mcp add --transport http vercel https://mcp.vercel.com
```

### Miro

Reads and writes Miro boards. If the planning for something lives on a board, this saves
transcribing it - Claude reads the stickies itself and can write results back.

One gotcha worth knowing: the tag pills on a sticky only come back when you fetch that sticky
individually, so a bulk read of a board will quietly miss them.

```
See Miro's own MCP documentation for the current endpoint
```

---

## CLIs

Command-line tools. Claude drives a terminal well, and unlike an MCP a CLI costs nothing while you
are not using it.

### GitHub (`gh`)

The most-used tool here, and the one to install first. Issues, pull requests, CI runs, releases,
all without leaving the terminal.

Several skills lean on it: `pickup-issue` reads an issue and its comments through it,
`review-suite` files its findings as new issues, `ui-report` waits on CI with it. Run
`gh auth login` after installing, or none of that works.

```
brew install gh && gh auth login
```

### Azure (`az`)

Manage Azure from the terminal: resources, deployments, configuration, logs. Claude works well
with it because the commands are predictable and it can read the output straight back.

If you also run the Azure MCP, you probably do not need both. The CLI covers the same ground
without costing context in every session.

```
brew install azure-cli
```

### Postgres (`psql`)

Query a database directly. Instead of inferring what is in a table from migration files, Claude
can look. It is also the quickest way to settle whether a bug is in the code or in the data, which
is usually the first fork in a debugging session.

`libpq` gives you just the client. Install the full Postgres package only if you want a server
running locally too.

```
brew install libpq
```

---

## Plugins

Installed inside Claude Code with `/plugin`.

### context-mode

Big commands produce big output, and by default all of it lands in the conversation and stays
there for the rest of the session. One long test run can cost you more room than the code you are
working on. context-mode runs the command in a sandbox and hands Claude only the part that answers
the question.

Most valuable on log-heavy work: test runs, build output, large data files, long git histories.

```
/plugin marketplace add mksglu/context-mode
```

### Caveman

Makes Claude answer tersely - filler stripped out, code, commands and error text left exact. Over
a long session that adds up.

Worth knowing the published savings are disputed: the project advertises 65%, while JetBrains
measured 8.5% across 86 real coding tasks. The gap is that the big number comes from chat-style
question answering, and in agentic coding most of the tokens are code and tool output, which does
not compress.

```
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
```

### Language servers

Gives Claude the same information your editor has: real types, go-to-definition,
find-all-references. Without one it is searching for text and inferring the rest, which goes wrong
exactly where you would expect - overloaded names, re-exports, anything generic.

Install the one your project speaks. The marketplace carries around twenty, including Go, Rust,
Java and C#.

```
/plugin marketplace add boostvolt/claude-code-lsps
/plugin install vtsls@claude-code-lsps      # TypeScript
/plugin install pyright@claude-code-lsps    # Python
```

---

## Also worth having

### uv

Python environments and dependency management, fast enough that you stop avoiding it. It handles
the Python version too, so a project can pin its own without anything global changing. If you have
been maintaining a pile of virtualenvs by hand, this replaces all of it.

```
brew install uv
```

### ruff

Python linting and formatting in one tool, quick enough to run on every save. The real benefit
with an agent is giving it a single command that both checks and fixes style, so it stops
inventing its own conventions halfway through a file.

```
uv tool install ruff
```
