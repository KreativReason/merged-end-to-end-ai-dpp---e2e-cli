# KreativReason E2E Pipeline

> From conversation to code, from code to compounding value.

A unified development pipeline that transforms client interviews into production-ready projects with **Pydantic-validated artifacts**, **human approval gates**, and **deterministic scaffolding**.

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
# Clone the repository
git clone https://github.com/KreativReason/merged-end-to-end-ai-dpp---e2e-cli.git
cd merged-end-to-end-ai-dpp---e2e-cli

# Install Python dependencies
pip install pydantic

# Use with Claude Code
claude
```

## Pipeline Phases

### Phase 1: Genesis (Interview → Project)

```
/kreativreason:genesis
```

1. **Interview Transcript** → You provide the raw conversation
2. **PRD Agent** → Generates Product Requirements → `lint_prd.py` validates → **Human Approval**
3. **Flow Agent** → Generates User/System Flows → **Human Approval**
4. **ERD Agent** → Generates Entity Relationships → `lint_erd.py` validates → **Human Approval**
5. **Journey Agent** → Generates User Journeys
6. **Planner Agent** → Breaks down into Tasks → **Human Approval**
7. **ADR Agent** → Documents Architecture Decisions
8. **Scaffolder Agent** → Creates project plan → **Human Approval**
9. **scaffold_apply.py** → Generates actual files

### Phase 2: Development (Continuous)

```
/kreativreason:plan "Add user authentication"
/kreativreason:work plans/add-user-auth.md
/kreativreason:review #123
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
├── lint_prd.py    # PRD-specific validation rules
├── lint_erd.py    # ERD-specific validation rules
└── test_pipeline.py
```

### Commands (6 workflows)

- `genesis` - Full project creation pipeline
- `plan` - Feature/task planning
- `work` - Execute plans with testing
- `review` - Multi-agent code review
- `handoff` - Genesis → Development transition
- `triage` - Process review findings

### Skills (8 capabilities)

- `git-worktree` - Isolated branch development
- `file-todos` - Structured todo management
- `validation` - JSON/Pydantic validation
- `artifact-sync` - Cross-artifact consistency
- `frontend-design` - Design system reference
- `gemini-imagegen` - Mockup generation
- `compound-docs` - Pattern documentation
- `skill-creator` - Create new skills

## Validation Examples

```bash
# Validate a PRD
python app/lint_prd.py docs/prd.json

# Validate an ERD
python app/lint_erd.py docs/erd.json

# Apply scaffold plan (after approval)
python scripts/scaffold_apply.py docs/scaffold-plan.json
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

## Project Isolation

Generated projects live **outside** this CLI:

```
~/Projects/
├── acme-app/           # Generated project
├── client-portal/      # Generated project
└── saas-platform/      # Generated project

merged-e2e-pipeline/    # This CLI (stays lightweight)
├── app/                # Validation layer
├── agents/             # Agent definitions
└── docs/               # Artifact storage
```

## MCP Servers

- **Playwright**: Browser automation for screenshots and visual testing
- **Context7**: Framework documentation lookup (Next.js, React, FastAPI, Django, Rails, Prisma, etc.)

## License

MIT

## Author

[KreativReason](https://github.com/kreativreason)
