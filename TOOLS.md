# Tools

Things worth adding to a Claude Code setup, and what each one is actually for.

---

## MCPs

An MCP gives Claude a new set of tools - a database it can query, a browser it can drive, a
service it can talk to.

**Keep the ones you rarely use switched off.** Every enabled MCP loads its full set of tools into
every session, whether you touch them or not, so a long list of live MCPs makes each conversation
more expensive before you have typed anything. Install what looks useful, leave most of it off,
and switch one on for the project that needs it.

**Context7**
Claude's knowledge of any library is frozen at whenever it was trained, so it will confidently
write code against an API that changed months ago. Context7 fetches the library's current
documentation at the moment you ask. Most valuable on fast-moving frameworks, and on anything you
have upgraded recently.
```
claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key <key>
```

**Playwright**
Gives Claude a real browser it can drive: open a page, click through a flow, fill a form, take
screenshots, read the console. It turns "this should work" into "I watched it work". The
`ui-report` skill runs on this one, so install it if you want UI verification.
```
claude mcp add playwright -- npx -y @playwright/mcp@latest
```

**Supabase**
Connects Claude to your Supabase project - inspect tables, run queries, apply migrations, read
logs. Saves pasting schemas into chat, and lets Claude check what the data actually looks like
before it writes code against it.
```
claude mcp add supabase -- npx -y @supabase/mcp-server-supabase@latest
```

**n8n**
Lets Claude build and inspect n8n automations directly: create workflows, check how a node is
configured, look at what happened in a failed run. Useful when the job is wiring services
together rather than writing code.
```
claude mcp add n8n -- npx n8n-mcp
```

**Vercel**
Deployments and preview builds. Claude can see whether a deploy went green, read the build log
when it did not, and find the preview URL for a branch. Handy while prototyping, when you are
pushing often and want to know quickly.
```
claude mcp add --transport http vercel https://mcp.vercel.com
```

**Miro**
Reads and writes Miro boards. If the planning for something lives on a board, this saves
transcribing it - Claude reads the stickies itself, and can write results back.
```
See Miro's own MCP documentation for the current endpoint
```

---

## CLIs

Command-line tools. Claude drives a terminal well, and unlike an MCP a CLI costs nothing while
you are not using it.

**GitHub** (`gh`)
The most-used tool here. Issues, pull requests, CI runs, releases, all without leaving the
terminal. Several skills lean on it: `pickup-issue` reads an issue and its comments through it,
`review-suite` files its findings as issues, `ui-report` waits on CI with it.
```
brew install gh && gh auth login
```

**Azure** (`az`)
Manage Azure from the terminal: resources, deployments, configuration, logs. Claude works well
with it because the commands are predictable and it can read the output straight back.
```
brew install azure-cli
```

**Postgres** (`psql`)
Query a database directly. Instead of inferring what is in a table from migration files, Claude
can just look. It is also the quickest way to settle whether a bug is in the code or in the data.
```
brew install libpq
```

---

## Plugins

Installed inside Claude Code with `/plugin`.

**context-mode**
Big commands produce big output, and by default all of it lands in the conversation and stays
there for the rest of the session. context-mode runs the command in a sandbox and hands Claude
only the part that answers the question. Most valuable on log-heavy work: test runs, build
output, large files, long git histories.
```
/plugin marketplace add mksglu/context-mode
```

**Caveman**
Makes Claude answer tersely - filler stripped out, code, commands and error text left exact. Over
a long session that adds up. Worth knowing the published savings are disputed: the project
advertises 65%, while JetBrains measured 8.5% across 86 real coding tasks.
```
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
```

**Language servers**
Gives Claude the same information your editor has - real types, go-to-definition,
find-all-references. Without one it is searching for text and inferring the rest. Install the one
your project speaks; the marketplace carries about twenty, including Go, Rust, Java and C#.
```
/plugin marketplace add boostvolt/claude-code-lsps
/plugin install vtsls@claude-code-lsps      # TypeScript
/plugin install pyright@claude-code-lsps    # Python
```

---

## Also worth having

**uv**
Python environments and dependency management, and fast enough that you stop avoiding it. Handles
the Python version too, so a project can pin its own without anything global changing.
```
brew install uv
```

**ruff**
Python linting and formatting in one tool, quick enough to run on every save. Giving Claude a
single command that both checks and fixes style keeps it from inventing its own conventions.
```
uv tool install ruff
```
