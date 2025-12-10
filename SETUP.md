# Setup Guide

This guide explains how to install and configure the KreativReason E2E Pipeline for your team.

---

## Prerequisites

- **Claude Code CLI** - Install from [claude.com](https://claude.com/claude-code)
- **Python 3.10+** with Pydantic
- **Node.js 20+** (for generated projects)
- **Git** for version control

---

## Installation

### Option 1: Install from GitHub (Recommended for Teams)

```bash
# In Claude Code (run from Cursor terminal or standalone)
/plugin install github:KreativReason/merged-end-to-end-ai-dpp---e2e-cli
```

This installs the plugin globally. All team members with repo access can install the same way.

### Option 2: Install from Local Clone

```bash
# 1. Clone the repository
git clone https://github.com/KreativReason/merged-end-to-end-ai-dpp---e2e-cli.git
cd merged-end-to-end-ai-dpp---e2e-cli

# 2. Install Python dependencies
pip install pydantic

# 3. Install plugin in Claude Code
/plugin install /path/to/merged-end-to-end-ai-dpp---e2e-cli
```

---

## Plugin Management

### Enable/Disable Per Project

```bash
# Enable in current project
/plugin enable kreativreason-e2e-pipeline

# Disable when not needed
/plugin disable kreativreason-e2e-pipeline

# Check status
/plugin list
```

### Updates

When improvements are pushed to GitHub:

```bash
/plugin update kreativreason-e2e-pipeline
```

Team members should run this periodically to get the latest agents, commands, and fixes.

---

## Verify Installation

After installing, verify the plugin is working:

```bash
# List available commands
/help

# You should see:
# /kreativreason:genesis
# /kreativreason:plan
# /kreativreason:work
# /kreativreason:review
# /kreativreason:triage
# /kreativreason:handoff
```

---

## MCP Servers

The plugin configures two MCP servers automatically:

### Playwright (Screenshots & Visual Testing)

```bash
# Verify Playwright MCP is available
npx -y @playwright/mcp@latest
```

Used for:
- Design iteration screenshots
- Visual regression testing
- Browser automation

### Context7 (Framework Documentation)

Automatically configured. Provides documentation lookup for:
- Next.js, React, Vue
- FastAPI, Django, Rails
- Prisma, TypeORM
- And more

---

## Team Setup Workflow

### For Team Lead / Admin

1. **Fork or clone** the repository to your organization
2. **Configure** the GitHub repo URL in documentation
3. **Share installation command** with team:
   ```bash
   /plugin install github:YourOrg/merged-end-to-end-ai-dpp---e2e-cli
   ```

### For Team Members

1. **Ensure Claude Code access** - Get API key if needed
2. **Run installation command** from team lead
3. **Verify installation** with `/help`
4. **Enable plugin** in projects with `/plugin enable kreativreason-e2e-pipeline`

---

## Using with Cursor

The plugin works in Claude Code launched from **any terminal**, including Cursor's integrated terminal:

1. Open Cursor
2. Open the integrated terminal (`Ctrl+`` ` or `Cmd+`` `)
3. Run `claude` to start Claude Code
4. Use plugin commands normally

---

## Directory Structure

After installation, the plugin provides:

```
kreativreason-e2e-pipeline/
├── commands/workflows/     # 6 slash commands
│   ├── genesis.md
│   ├── plan.md
│   ├── work.md
│   ├── review.md
│   ├── triage.md
│   └── handoff.md
├── agents/                 # 35 specialized agents
│   ├── genesis/           # PRD, ERD, Flow, etc.
│   ├── development/       # Coding, Feature, Bugfix
│   ├── review/            # 11 code reviewers
│   ├── design/            # Figma, Visual QA
│   ├── workflow/          # Linting, PR handling
│   ├── research/          # Docs, Best practices
│   └── docs/              # README generation
├── skills/                 # 8 reusable capabilities
├── app/                    # Python validation layer
│   ├── models.py          # Pydantic schemas
│   ├── lint_prd.py        # PRD validator
│   └── lint_erd.py        # ERD validator
└── scripts/
    └── scaffold_apply.py  # Deterministic scaffolding
```

---

## Troubleshooting

### "Plugin not found"

```bash
# Check installed plugins
/plugin list

# Reinstall if needed
/plugin install github:KreativReason/merged-end-to-end-ai-dpp---e2e-cli
```

### "Command not found"

```bash
# Ensure plugin is enabled
/plugin enable kreativreason-e2e-pipeline

# Refresh commands
/help
```

### "Pydantic validation failed"

```bash
# Install Pydantic
pip install pydantic

# Or with specific version
pip install pydantic>=2.0
```

### "Permission denied" on GitHub install

Ensure you have access to the repository:
- For private repos, authenticate with `gh auth login`
- Or use local clone method

---

## Next Steps

1. **Read [USAGE_GUIDE.md](USAGE_GUIDE.md)** for step-by-step examples
2. **Run a test genesis** with a sample interview
3. **Review [WORKFLOW.md](WORKFLOW.md)** for team collaboration patterns

---

## Quick Reference

```bash
# Install
/plugin install github:KreativReason/merged-end-to-end-ai-dpp---e2e-cli

# Update
/plugin update kreativreason-e2e-pipeline

# Enable/Disable
/plugin enable kreativreason-e2e-pipeline
/plugin disable kreativreason-e2e-pipeline

# Commands
/kreativreason:genesis      # New project from interview
/kreativreason:plan         # Plan feature/bugfix
/kreativreason:work         # Execute plan
/kreativreason:review       # 11-agent code review
/kreativreason:triage       # Process findings
/kreativreason:handoff      # Genesis → Development
```
