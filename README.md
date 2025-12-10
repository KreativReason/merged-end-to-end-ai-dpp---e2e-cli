# KreativReason E2E Pipeline

> From conversation to code, from code to compounding value.

A Claude Code plugin that transforms client interviews into production-ready projects with **Pydantic-validated artifacts**, **human approval gates**, and **deterministic scaffolding**.

## Installation

### For Teams (Recommended)

```bash
# In Claude Code (from Cursor terminal or standalone)
/plugin install github:KreativReason/merged-end-to-end-ai-dpp---e2e-cli
```

### From Local Clone

```bash
# Clone the repository
git clone https://github.com/KreativReason/merged-end-to-end-ai-dpp---e2e-cli.git

# Install in Claude Code
/plugin install /path/to/merged-end-to-end-ai-dpp---e2e-cli
```

### Updates

When improvements are pushed to GitHub:

```bash
/plugin update kreativreason-e2e-pipeline
```

## What's Different About This System

| Feature | Traditional AI Coding | This Pipeline |
|---------|----------------------|---------------|
| **Validation** | Trust the LLM | Pydantic enforces schemas |
| **Approval Gates** | Suggested in prompts | Enforced in Python |
| **Scaffolding** | LLM writes files | Deterministic script |
| **Consistency** | Varies per run | Stable IDs, validated refs |
| **Review** | Single perspective | 11 parallel reviewers |

## Quick Start

```bash
# 1. Install plugin (once)
/plugin install github:KreativReason/merged-end-to-end-ai-dpp---e2e-cli

# 2. Enable in your project
/plugin enable kreativreason-e2e-pipeline

# 3. Run genesis (new project from interview)
/kreativreason:genesis

# Or development commands (existing project)
/kreativreason:plan "Add user authentication"
/kreativreason:work
/kreativreason:review
```

## Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/kreativreason:genesis` | Interview → PRD → ERD → Tasks → Project | Starting new project |
| `/kreativreason:plan` | Create implementation plan | Planning feature/bugfix |
| `/kreativreason:work` | Execute plan with testing | Implementing work |
| `/kreativreason:review` | 11-agent code review | Before merging PRs |
| `/kreativreason:triage` | Process review findings | After review |
| `/kreativreason:handoff` | Genesis → Development transition | After scaffolding |

## Pipeline Phases

### Phase 1: Genesis (Interview → Project)

```
/kreativreason:genesis
```

1. **Interview Transcript** → You provide the raw conversation
2. **PRD Agent** → Product Requirements → `lint_prd.py` validates → **Human Approval**
3. **Flow Agent** → User/System Flows
4. **ERD Agent** → Entity Relationships → `lint_erd.py` validates → **Human Approval**
5. **Journey Agent** → User Journeys
6. **Planner Agent** → Task Breakdown → **Human Approval**
7. **ADR Agent** → Architecture Decisions
8. **Scaffolder Agent** → Project Structure → **Human Approval**
9. **scaffold_apply.py** → Generates actual files

### Phase 2: Development (Continuous)

```bash
/kreativreason:plan "Add user authentication"
/kreativreason:work
/kreativreason:review
/kreativreason:triage
```

## Components

### Agents (35 total)

| Category | Count | Purpose |
|----------|-------|---------|
| Genesis | 8 | Project creation (PRD, ERD, Flow, etc.) |
| Development | 4 | Coding, features, bugfixes, migrations |
| Review | 11 | Security, performance, architecture, language-specific |
| Design | 3 | Figma sync, visual iteration, QA |
| Workflow | 5 | Linting, PR comments, bug validation |
| Research | 3 | Codebase analysis, best practices, docs |
| Docs | 1 | README generation |

### Python Validation Layer

```
app/
├── models.py      # Pydantic schemas for all artifacts
├── lint_prd.py    # PRD validation
└── lint_erd.py    # ERD validation
```

### Skills (8 capabilities)

- `git-worktree` - Isolated branch development
- `file-todos` - Structured todo management
- `validation` - JSON/Pydantic validation
- `artifact-sync` - Cross-artifact consistency
- `frontend-design` - Design system reference
- `gemini-imagegen` - Mockup generation
- `compound-docs` - Pattern documentation
- `skill-creator` - Create new skills

## Validation

```bash
# Validate PRD
python app/lint_prd.py docs/prd.json

# Validate ERD
python app/lint_erd.py docs/erd.json

# Apply scaffold (after approval)
python scripts/scaffold_apply.py \
  --plan docs/scaffold-plan.json \
  --prd docs/prd.json \
  --erd docs/erd.json \
  --approved-by "ProductOwner" \
  --approved-by "TechLead" \
  --output docs/scaffold-applied.json \
  --project-dir ~/Projects/new-app
```

## Stable ID Conventions

IDs are **never regenerated**. Once assigned, they're immutable:

| Artifact | Format | Example |
|----------|--------|---------|
| Features | FR-### | FR-001 |
| Stories | ST-### | ST-001 |
| Tasks | TASK-### | TASK-001 |
| ADRs | ADR-#### | ADR-0001 |
| Entities | ENT-### | ENT-001 |

## MCP Servers

Automatically configured when plugin is enabled:

- **Playwright**: Browser automation for screenshots and visual testing
- **Context7**: Framework documentation lookup

## Requirements

- Claude Code CLI
- Python 3.10+ with Pydantic (`pip install pydantic`)
- Node.js 20+ (for generated projects)

## Documentation

- [SETUP.md](SETUP.md) - Installation and configuration
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Step-by-step examples
- [WORKFLOW.md](WORKFLOW.md) - Team collaboration patterns
- [CLAUDE.md](CLAUDE.md) - Claude Code instructions

## License

UNLICENSED - Private team use only

## Author

[KreativReason](https://github.com/kreativreason)
