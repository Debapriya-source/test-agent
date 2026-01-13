# Test Agent

Autonomous coding agent. Code, test, ship from plans.

## Structure

- `agent/` - main package
  - `cli.py` - click commands
  - `db.py` - sqlite ops
  - `knowledge.py` - project scanning
  - `core.py` - orchestration
  - `claude_bridge.py` - claude code wrapper
  - `skills/` - coder, tester, shipper
  - `subagents/` - planner, executor, reviewer

## Usage

```bash
agent init          # scan project
agent plan file.md  # load plan
agent plan -i       # interactive
agent run           # execute
agent status        # show state
```

## Data

All in `.agent/` dir: agent.db (sqlite), plans/, config.json

## Design

- Sequential task execution
- Ship ops prompt user
- Claude Code CLI for AI
