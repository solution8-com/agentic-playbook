# Tools

Things worth adding to a Claude Code setup, and what each one is for.

## MCPs

An MCP gives Claude a new set of tools - a database it can query, a browser it can drive.

**Keep the ones you rarely use switched off.** Every enabled MCP loads its tools into every
session whether you touch them or not, so a long list of live MCPs makes each conversation
more expensive before you have typed anything. Turn one on for the project that needs it.

| Tool | What it does | Install |
|---|---|---|
| **Context7** | Looks up current documentation for a library or framework, so Claude answers from today's docs instead of what it happens to remember. | `claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key <key>` |
| **Playwright** | Opens a real browser. Claude can click through your app, fill forms and take screenshots. (`ui-report` needs this.) | `claude mcp add playwright -- npx -y @playwright/mcp@latest` |
| **Supabase** | Work with your database: tables, migrations, queries, logs. | `claude mcp add supabase -- npx -y @supabase/mcp-server-supabase@latest` |
| **n8n** | Build and run automations and workflows. | `claude mcp add n8n -- npx n8n-mcp` |
| **Vercel** | Deploy, and check preview builds. | `claude mcp add --transport http vercel https://mcp.vercel.com` |
| **Miro** | Read and write Miro boards. Useful when the planning lives on one. | See Miro's MCP docs |

## CLIs

Command-line tools. Claude drives a terminal well, and a CLI costs nothing when you are not
using it.

| Tool | What it does | Install |
|---|---|---|
| **GitHub** (`gh`) | Issues, pull requests, CI runs, releases, all from the terminal. The most-used tool here. | `brew install gh && gh auth login` |
| **Azure** (`az`) | Manage Azure resources, deployments and logs. | `brew install azure-cli` |
| **Postgres** (`psql`) | Query a database directly instead of guessing at it from the schema files. | `brew install libpq` |

## Plugins

Installed inside Claude Code with `/plugin`.

| Tool | What it does | Install |
|---|---|---|
| **context-mode** | Runs heavy commands in a sandbox and hands Claude only the answer, not the raw output. Saves a lot of room on log-heavy and data-heavy work. | `/plugin marketplace add mksglu/context-mode` |
| **Caveman** | Makes Claude answer tersely - strips the filler out of its replies while leaving code, commands and error text exact. Worth it on long sessions. | `claude plugin marketplace add JuliusBrussee/caveman`<br>`claude plugin install caveman@caveman` |
| **Language servers** | Gives Claude real type information and go-to-definition instead of making it search through text. One per language - `vtsls` for TypeScript, `pyright` for Python, and around twenty more. | `/plugin marketplace add boostvolt/claude-code-lsps`<br>`/plugin install vtsls@claude-code-lsps` |

## Also worth having

- **uv** - modern Python environments and dependencies, fast. `brew install uv`
- **ruff** - Python lint and format in one tool. `uv tool install ruff`
