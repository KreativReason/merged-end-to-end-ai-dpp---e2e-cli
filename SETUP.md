# Production Setup Guide

This guide explains how to install and use the merged E2E Pipeline in production.

---

## Installation

### Step 1: Clone the Repository

```bash
# Navigate to your projects directory
cd ~/Projects

# Clone the merged pipeline
git clone https://github.com/KreativReason/merged-end-to-end-ai-dpp---e2e-cli.git
cd merged-end-to-end-ai-dpp---e2e-cli
```

### Step 2: Install Python Dependencies

```bash
pip install pydantic
```

### Step 3: Configure Claude Code

Add the plugin to your Claude Code settings. Edit `~/.claude/settings.json`:

```json
{
  "plugins": [
    "~/Projects/merged-end-to-end-ai-dpp---e2e-cli"
  ]
}
```

Alternatively, you can work directly from within the cloned directory.

### Step 4: (Optional) Set Up MCP Servers

The plugin supports two MCP servers for enhanced capabilities:

**Playwright** (for screenshots and visual testing):
```bash
npx -y @playwright/mcp@latest
```

**Context7** (for framework documentation lookup):
- Configured automatically via `plugin.json`
- Provides docs for Next.js, React, FastAPI, Django, Rails, Prisma, etc.

---

## Two Ways to Use the Pipeline

### Option A: Full Genesis Pipeline (New Projects)

Use this when starting a brand new project from a client interview.

```
/kreativreason:genesis
```

**What you provide:**
- Interview transcript (paste directly or provide path)
- Project name
- Output directory

**What happens:**

| Step | Agent | Output | Approval Required |
|------|-------|--------|-------------------|
| 1 | PRD | `docs/prd.json` | ✅ Yes (validated by `lint_prd.py`) |
| 2 | Flow | `docs/flow.json` | No |
| 3 | ERD | `docs/erd.json` | ✅ Yes (validated by `lint_erd.py`) |
| 4 | Journey | `docs/journey.json` | No |
| 5 | Planner | `docs/tasks.json` | ✅ Yes |
| 6 | ADR | `docs/adr.json` | No |
| 7 | Scaffolder | `docs/scaffold-plan.json` | ✅ Yes |
| 8 | Build | Complete project directory | N/A |

**Example:**

```
/kreativreason:genesis

Interview transcript: interviews/client-call.md
Project name: "BookEasy - Service Booking Platform"
Output directory: ~/Projects/bookeasy
```

### Option B: Development Commands (Existing Projects)

Use these commands on projects that already exist.

#### Plan a Feature or Bugfix

```
/kreativreason:plan "Add user authentication with OAuth"
```

Creates a structured implementation plan with tasks.

#### Execute a Plan

```
/kreativreason:work plans/add-auth.md
```

Executes the plan in an isolated git worktree with continuous testing.

#### Code Review (11 Agents in Parallel)

```
/kreativreason:review #123
```

Runs 11 specialized reviewers:
- Security Sentinel (OWASP, injection, auth)
- Performance Oracle (N+1, memory, caching)
- Architecture Strategist (ADR alignment, coupling)
- Code Simplicity Reviewer (YAGNI, over-engineering)
- Data Integrity Guardian (schema safety, migrations)
- DHH Rails Reviewer (Rails conventions)
- Kieran Rails/TypeScript/Python Reviewers (language-specific)
- Julik Frontend Races Reviewer (async bugs)
- Pattern Recognition Specialist (design patterns)

#### Process Review Findings

```
/kreativreason:triage
```

Organizes review findings into actionable todos.

#### Transition from Genesis to Development

```
/kreativreason:handoff
```

Sets up a generated project for ongoing development.

---

## Command Reference

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/kreativreason:genesis` | Full pipeline: Interview → Project | Starting a new project |
| `/kreativreason:plan` | Create implementation plan | Planning a feature or bugfix |
| `/kreativreason:work` | Execute a plan | Implementing planned work |
| `/kreativreason:review` | Multi-agent code review | Before merging PRs |
| `/kreativreason:triage` | Organize review findings | After running review |
| `/kreativreason:handoff` | Genesis → Development transition | After scaffolding completes |

---

## Manual Validation Commands

Run these to validate artifacts outside of the pipeline:

```bash
# Validate PRD
python app/lint_prd.py docs/prd.json

# Validate ERD
python app/lint_erd.py docs/erd.json

# Apply scaffold plan manually (after approval)
python scripts/scaffold_apply.py docs/scaffold-plan.json --output ~/Projects/new-app
```

---

## Project Structure After Genesis

When you run the full genesis pipeline, your generated project looks like this:

```
~/Projects/new-app/
├── src/                      # Application code
├── tests/                    # Test suite
├── .cursor/rules/            # Project-specific editor rules
├── agents/                   # Project-specific agents
│   ├── Coding.agent.md       # Implementation guidance
│   ├── Feature.agent.md      # New feature workflow
│   └── Bugfix.agent.md       # Bug fix workflow
├── docs/                     # Specs copied from genesis
│   ├── prd.json
│   ├── erd.json
│   └── ...
├── README.md
└── ...
```

The generated project has its own agents for ongoing development, so you can continue using AI-assisted workflows.

---

## Using Individual Agents

You can also invoke agents directly using the `@agent` syntax:

```
@agents/genesis/prd.md implement

Generate PRD from client interview:
- transcript_path: interviews/client-interview.md
- project_name: "My App"
```

Available agent categories:
- `agents/genesis/` - PRD, Flow, ERD, Journey, Planner, ADR, Scaffolder
- `agents/development/` - Coding, Feature, Bugfix, Migration
- `agents/review/` - 11 code review specialists
- `agents/design/` - Figma sync, Design iterator, Implementation reviewer
- `agents/workflow/` - Lint, PR resolver, Bug validator, Spec analyzer
- `agents/research/` - Repo analyst, Best practices, Framework docs

---

## Human Approval Gates

The pipeline enforces human review at critical stages:

| Stage | Reviewers | Validation Script |
|-------|-----------|-------------------|
| PRD Complete | Product Owner, Tech Lead | `app/lint_prd.py` |
| ERD Complete | Tech Lead, DBA | `app/lint_erd.py` |
| Tasks Complete | Product Owner, Lead Dev | Schema validation |
| Scaffold Plan | Product Owner, Tech Lead | Schema validation |
| Code Merge | Code Reviewer | Review agents |

**Important:** The pipeline will not auto-advance past these gates. You must explicitly approve each stage.

---

## Troubleshooting

### "Plugin not found"

Ensure the plugin path is correct in your Claude Code settings:
```bash
ls ~/.claude/settings.json
cat ~/.claude/settings.json | grep plugins
```

### "Validation failed"

Check the artifact against the schema:
```bash
python app/lint_prd.py docs/prd.json
# Or
python app/lint_erd.py docs/erd.json
```

### "Agent not found"

Verify agents exist:
```bash
ls agents/genesis/
ls agents/development/
ls agents/review/
```

### "Pydantic not installed"

Install the dependency:
```bash
pip install pydantic
```

---

## Next Steps

1. **Run a test genesis** with a sample interview to verify setup
2. **Configure MCP servers** for design iteration capabilities
3. **Review USAGE_GUIDE.md** for detailed step-by-step examples
4. **Review WORKFLOW.md** for team collaboration patterns

---

## Quick Start Example

```bash
# 1. Clone and setup
git clone https://github.com/KreativReason/merged-end-to-end-ai-dpp---e2e-cli.git
cd merged-end-to-end-ai-dpp---e2e-cli
pip install pydantic

# 2. Open Claude Code in this directory
claude

# 3. Run the genesis command
/kreativreason:genesis

# 4. Follow the prompts to provide interview transcript and project details
```

That's it! The pipeline will guide you through each step with validation and approval gates.
