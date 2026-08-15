# Tools

What we install alongside the skills: MCPs, CLIs, language servers, plugins.

Two halves, and they age differently. **What the skills need** is not opinion - get it wrong
and something visibly breaks. **What we reach for** is opinion, and it dates. Treat the second
half as "what we were using in August 2026", not as a standing recommendation.

---

## What the skills need

Three things. Without them, specific skills fail rather than degrade.

| Tool | Needed by | Install |
|---|---|---|
| **GitHub CLI** (`gh`) | `pickup-issue`, `review-suite`, `ui-report`, `wizard` | `brew install gh && gh auth login` |
| **Playwright MCP** | `ui-report` | `claude mcp add playwright -- npx -y @playwright/mcp@latest` |
| **Python 3** | `ui-report`'s report builder | `brew install uv` (uv manages the runtime) |

`ui-report` assumes Playwright runs with image responses omitted - it asserts through
accessibility snapshots and keeps screenshots for the report rather than for the model.

---

## MCPs

**Every enabled MCP costs context in every session.** Its tool definitions load whether you use
them or not, so a machine with a dozen live MCPs starts every conversation heavier than it needs
to be. Install broadly, enable narrowly: keep the always-on set small and turn the rest on per
project.

| MCP | What it is | Default |
|---|---|---|
| **Context7** | Current docs for libraries and frameworks, fetched live. Stops the model answering from stale training data. | **on** |
| **Playwright** | Drives a real browser. Frontend verification, and what `ui-report` runs on. | **on** |
| **Supabase** | Database work - schema, migrations, queries, logs. | off |
| **n8n** | Automations and workflows. | off |
| **Vercel** | Deploys and previews. Useful while prototyping. | off |
| **Miro** | Boards, for planning sessions. | off |

```
claude mcp add context7  -- npx -y @upstash/context7-mcp --api-key <key>
claude mcp add playwright -- npx -y @playwright/mcp@latest
claude mcp add supabase  -- npx -y @supabase/mcp-server-supabase@latest
claude mcp add n8n       -- npx n8n-mcp
claude mcp add --transport http vercel https://mcp.vercel.com
```

The four marked `off` are worth having installed and disabled - the cost of enabling one for an
afternoon is nothing, and the cost of every session carrying all of them is real.

---

## CLIs

Claude drives a shell well. A CLI is usually a better tool than an MCP for the same service:
no schema to load, no context cost when idle, and the model already knows the commands.

| CLI | Why | Install |
|---|---|---|
| **GitHub** (`gh`) | Issues, PRs, CI runs, releases. The most-used tool in the set. | `brew install gh` |
| **Azure** (`az`) | Resources, deployments, logs. | `brew install azure-cli` |
| **Postgres** (`psql`) | Query a database directly instead of guessing from the schema. | `brew install libpq` |

---

## Language servers

Real types and real definitions instead of grep. Installed as plugins from
[`boostvolt/claude-code-lsps`](https://github.com/boostvolt/claude-code-lsps).

```
/plugin marketplace add boostvolt/claude-code-lsps
/plugin install vtsls@claude-code-lsps      # TypeScript
/plugin install pyright@claude-code-lsps    # Python
```

That marketplace also carries Go, Rust, Java, C#, PHP, Ruby, Swift, Terraform and more - install
the one your project speaks.

For Python, pair it with a modern toolchain: `uv` for environments and dependencies,
`ruff` for lint and format.

---

## Plugins

| Plugin | What it does | Install |
|---|---|---|
| **context-mode** | Runs commands and processes their output in a sandbox, so large tool output never enters the conversation. Buys back context on log-heavy and data-heavy work. | `/plugin marketplace add mksglu/context-mode` |

---

*Last reviewed 2026-08-15. The "what we reach for" half of this page is a snapshot, not a
standard - if something here is no longer what you would pick, change it.*
