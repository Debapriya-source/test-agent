# Py Autonomous Agent

Simple autonomous coding agent. Code, test, and ship based on plans. Uses SQLite for task tracking and Claude Code CLI for AI.

## Features

- **Plan-based execution** - Markdown files or interactive
- **SQLite task tracking** - Persistent state
- **Auto-detect test frameworks** - pytest, jest, vitest, go test, cargo test
- **MCP server support** - Inherits existing Claude configs
- **Tech stack config** - Auto-configure MCP servers based on your stack
- **90+ built-in MCPs** - Databases, AI, DevOps, and more
- **Custom MCP support** - Add your own MCP servers
- **User-controlled shipping** - Git ops always prompt

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- [Claude Code CLI](https://github.com/anthropics/claude-code) installed
- Docker (for most MCP servers)

## Installation

```bash
# Clone and install
git clone https://github.com/Debapriya-source/py-autonomous-agent.git
cd py-autonomous-agent
uv sync

# Or install directly
uv add git+https://github.com/Debapriya-source/py-autonomous-agent.git
```

## Quick Start

```bash
cd /path/to/your-project

# Initialize (configures default MCPs: playwright, claude-code-sdk)
uv run agent init

# Add your tech stack
uv run agent stack add github supabase

# Create plan (interactive)
uv run agent plan -i

# Or from file
uv run agent plan my-plan.md

# Execute
uv run agent run -a

# Check status
uv run agent status
```

## Plan Format

```markdown
# Feature Name

- [ ] First task
- [ ] Second task
- [ ] Write tests
- [ ] Ship changes
```

Or numbered:
```markdown
# Bug Fix

1. Investigate issue
2. Fix root cause
3. Add test
4. Ship
```

## Commands

| Command | Description |
|---------|-------------|
| `uv run agent init` | Initialize in project |
| `uv run agent plan <file>` | Load plan from markdown |
| `uv run agent plan -i` | Interactive plan creation |
| `uv run agent run` | Execute next task |
| `uv run agent run -a` | Execute all tasks |
| `uv run agent run -t <id>` | Execute specific task |
| `uv run agent status` | Show task status |
| `uv run agent knowledge` | Show project info |
| `uv run agent validate` | Run tests + review |
| `uv run agent reset` | Clear all tasks |

## Tech Stack

Configure MCP servers based on your tech stack. Docker-based servers are preferred.

```bash
uv run agent stack list              # show available stacks (90+)
uv run agent stack presets           # show preset collections
uv run agent stack add <stack...>    # add tech stacks
uv run agent stack preset <name>     # add preset collection
uv run agent stack configure <srv>   # configure server auth
uv run agent stack configure <srv> -i  # interactive auth setup
uv run agent stack pending           # show pending config
uv run agent stack show              # show current config
uv run agent stack info <stack>      # details about a stack
```

### Default Servers (always configured)

- `playwright` - Browser automation (Docker)
- `claude-code-sdk` - Claude Code SDK for agents

### Available Stacks (90+)

| Category | Stacks |
|----------|--------|
| **Databases** | postgres, mysql, mongodb, redis, sqlite, supabase, neon, planetscale, turso, upstash, neo4j |
| **Vector DBs** | qdrant, pinecone, weaviate, chroma, milvus |
| **Git/DevOps** | github, gitlab, bitbucket, docker, kubernetes, terraform, pulumi |
| **Cloud** | aws, gcp, azure, cloudflare, vercel, netlify, fly, railway, render |
| **AI/ML** | openai, anthropic, groq, mistral, cohere, replicate, huggingface, together, perplexity |
| **Search** | algolia, typesense, meilisearch, elasticsearch, tavily, exa, serper, brave-search |
| **Communication** | slack, discord, telegram, teams, twilio |
| **Productivity** | notion, linear, jira, asana, trello, monday, clickup, todoist, confluence |
| **Email** | sendgrid, resend, mailgun, postmark |
| **Payments** | stripe, paypal, shopify |
| **Auth** | auth0, clerk, firebase |
| **Analytics** | segment, mixpanel, amplitude, posthog, datadog, newrelic, grafana, sentry |
| **CMS** | contentful, sanity, strapi |
| **CRM** | hubspot, salesforce |
| **Data** | snowflake, bigquery, databricks, airtable, google-sheets |
| **Scraping** | firecrawl, browserbase, apify |
| **Code Exec** | e2b, modal |
| **Secrets** | vault, doppler |
| **Queues** | rabbitmq, kafka |
| **Misc** | memory, fetch, time, git, sequential-thinking, zapier, make |

### Presets

```bash
uv run agent stack preset <name>
```

| Preset | Includes |
|--------|----------|
| `web-basic` | fetch, memory, github, git |
| `fullstack-postgres` | fetch, memory, github, postgres, docker, git |
| `fullstack-supabase` | fetch, memory, github, supabase, git |
| `serverless` | fetch, memory, github, vercel, neon, upstash, git |
| `ai-agent` | memory, fetch, openai, qdrant, github, e2b, firecrawl |
| `ai-search` | memory, fetch, tavily, exa, qdrant, openai |
| `saas` | github, supabase, stripe, resend, posthog, sentry |
| `startup` | github, vercel, supabase, stripe, resend, slack, linear |
| `enterprise` | github, jira, confluence, slack, datadog, vault |
| `devops` | github, docker, kubernetes, aws, sentry, terraform |
| `ecommerce` | github, shopify, stripe, sendgrid, algolia, segment |
| `ml-ops` | github, aws, s3, snowflake, databricks, huggingface |

### Examples

```bash
# Add individual stacks
uv run agent stack add postgres github

# Add with credentials
uv run agent stack add github -e GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx

# Interactive credential setup
uv run agent stack configure postgres -i

# Use a preset
uv run agent stack preset startup -e GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx
```

## Custom MCP Servers

Add your own MCP servers not in the built-in list:

```bash
uv run agent stack custom                    # list custom MCPs
uv run agent stack custom-add <name> <cmd>   # add custom MCP
uv run agent stack custom-remove <name>      # remove custom MCP
```

### Examples

```bash
# Add npm package MCP (use -p flag for npm packages)
uv run agent stack custom-add my-mcp @myorg/my-mcp-server -p -d "My custom MCP"

# Add with custom command and args
uv run agent stack custom-add db-tool docker -a run -a -i -a --rm -a mcp/db-tool

# Add with environment variables
uv run agent stack custom-add api-mcp npx -a @company/api-mcp \
  -e "API_KEY:API key for the service" \
  -e "API_URL:Base URL endpoint"

# Then use it like any built-in stack
uv run agent stack add my-mcp
uv run agent stack configure my-mcp -i

# Remove when no longer needed
uv run agent stack custom-remove my-mcp
```

## MCP Servers (Manual)

For direct MCP management without using tech stacks:

```bash
uv run agent mcp list                 # show servers
uv run agent mcp add <name> <pkg>     # add server
uv run agent mcp remove <name>        # remove server
uv run agent mcp test <name>          # test connection
```

Config priority: `.agent/mcp.json` > `.claude/settings.json` > `~/.claude/settings.json`

Example:
```bash
uv run agent mcp add fs @anthropic/mcp-server-filesystem
uv run agent mcp add github @anthropic/mcp-server-github -e GITHUB_TOKEN=xxx
```

## Skills/Plugins

```bash
uv run agent skills list           # show skills
uv run agent skills enable <name>  # enable skill
uv run agent skills disable <name> # disable skill
```

Built-in skills:
- `feature-dev` - Guided feature development (auto-selected for "feature", "implement", "add", "create", "build" tasks)
- `agent-sdk-dev:new-sdk-app` - Create Agent SDK app

Skills auto-select based on task keywords when enabled.

## Project Data

Created in `.agent/`:
```
.agent/
├── agent.db     # SQLite database
├── mcp.json     # MCP server config
├── stack.json   # Tech stack & custom MCPs
├── skills.json  # Skills config
└── plans/       # Plan files
```

## Example Workflow

```bash
cd ~/projects/my-api
uv run agent init

# Add your stack
uv run agent stack preset saas -e GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx
uv run agent stack configure supabase -i
uv run agent stack configure stripe -i

# Create plan
cat > auth.md << 'EOF'
# Add Authentication

- [ ] Create auth middleware
- [ ] Add login endpoint
- [ ] Write tests
- [ ] Ship
EOF

uv run agent plan auth.md
uv run agent run -a
uv run agent status
```

## Development

```bash
git clone https://github.com/Debapriya-source/py-autonomous-agent.git
cd py-autonomous-agent
uv sync
uv run ruff check agent/
uv run agent --help
```

## License

MIT
