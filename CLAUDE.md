# KreativReason E2E Pipeline - Claude Configuration

## Overview

This is the **Merged KreativReason End-to-End Pipeline** - combining the validated human-in-the-loop system with the expanded agent ecosystem. It provides:

1. **Project Genesis**: Transform client interviews into production-ready projects with Pydantic-validated artifacts
2. **Compounding Development**: Make each unit of engineering work easier than the last
3. **Python Validation Layer**: Deterministic schema enforcement and linting
4. **Multi-Agent Review**: 11 specialized code reviewers across languages and concerns

## Architecture

```
┌─────────────────────────────────────────┐
│     LLM Agents (35 Markdown Prompts)    │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│   Python Validation Layer (Pydantic)    │
│   app/models.py, lint_prd.py, lint_erd  │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│      Human Approval Gates (Enforced)    │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│   Deterministic Scaffolding (Python)    │
│   scripts/scaffold_apply.py             │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│     Generated Project Repository        │
└─────────────────────────────────────────┘
```

## Project Structure

```
merged-end-to-end-ai-dpp---e2e-cli/
├── .claude-plugin/
│   └── plugin.json           # Plugin configuration + validation refs
├── app/                      # Python validation layer
│   ├── models.py             # Pydantic schemas (750+ lines)
│   ├── lint_prd.py           # PRD validator
│   ├── lint_erd.py           # ERD validator
│   └── test_pipeline.py      # Integration tests
├── agents/
│   ├── genesis/              # Project creation (8 agents)
│   ├── development/          # Ongoing work (4 agents)
│   ├── review/               # Code review (11 agents)
│   ├── design/               # UI/UX iteration (3 agents)
│   ├── workflow/             # Automation (5 agents)
│   ├── research/             # Documentation (3 agents)
│   └── docs/                 # README generation (1 agent)
├── commands/workflows/       # 6 command workflows
├── skills/                   # 8 reusable capabilities
├── scripts/
│   └── scaffold_apply.py     # Deterministic file generation
├── docs/                     # Generated artifacts storage
├── templates/                # Project scaffolding templates
└── Makefile                  # Build targets
```

## Commands Reference

### Genesis Phase Commands

| Command | Description |
|---------|-------------|
| `/kreativreason:genesis` | Full pipeline: Interview → PRD → Flow → ERD → Journey → Tasks → ADR → Scaffold → Working Project |
| `/kreativreason:handoff` | Transition from genesis to development phase |

### Development Phase Commands

| Command | Description |
|---------|-------------|
| `/kreativreason:plan` | Transform feature/bug into structured plan |
| `/kreativreason:work` | Execute work plan with continuous testing |
| `/kreativreason:review` | Multi-agent code review (11 reviewers in parallel) |
| `/kreativreason:triage` | Process review findings into actionable todos |

## Validation Layer

All genesis artifacts are validated against Pydantic schemas before proceeding:

```bash
# Validate PRD
python app/lint_prd.py docs/prd.json

# Validate ERD
python app/lint_erd.py docs/erd.json

# Run scaffolding (after approval)
python scripts/scaffold_apply.py docs/scaffold-plan.json
```

### Pydantic Models (`app/models.py`)

- `PRDModel` - Product Requirements Document
- `FlowModel` - User/System Flows
- `ERDModel` - Entity Relationships
- `JourneyModel` - User Journeys
- `TasksModel` - Implementation Tasks
- `ADRModel` - Architecture Decisions
- `ScaffoldModel` - Project Structure Plan

## Human Approval Gates

The following stages require explicit human approval:

| Stage | Reviewers | Validation |
|-------|-----------|------------|
| PRD Complete | Product Owner, Tech Lead | `lint_prd.py` |
| ERD Complete | Tech Lead, DBA | `lint_erd.py` |
| Tasks Complete | Product Owner, Lead Dev | Schema validation |
| Scaffold Plan | Product Owner, Tech Lead | Schema validation |
| Code Merge | Code Reviewer | Review agents |

**Critical**: Never auto-advance without human approval. The Python validation layer enforces this.

## Stable ID Conventions

| Artifact | Format | Example |
|----------|--------|---------|
| Features | FR-### | FR-001 |
| Stories | ST-### | ST-001 |
| Tasks | TASK-### | TASK-001 |
| ADRs | ADR-#### | ADR-0001 |
| Entities | ENT-### | ENT-001 |
| Scaffold Items | SCAFFOLD-### | SCAFFOLD-001 |

**Never regenerate existing IDs** - they are immutable references.

## Agent Categories

### Genesis Agents (8)
Validated against Pydantic schemas:
- `prd.md` - Product Requirements
- `flow.md` - User/System Flows
- `erd.md` - Entity Relationships
- `journey.md` - User Journeys
- `planner.md` - Task Breakdown
- `adr.md` - Architecture Decisions
- `scaffolder.md` - Project Structure
- `guardrails.md` - Common Rules

### Review Agents (11)
Multi-language, multi-concern analysis:
- `security-sentinel.md` - OWASP, injection, auth
- `performance-oracle.md` - N+1, memory, caching
- `architecture-strategist.md` - ADR alignment, coupling
- `code-simplicity-reviewer.md` - YAGNI, over-engineering
- `data-integrity-guardian.md` - Schema safety, migrations
- `dhh-rails-reviewer.md` - Rails conventions
- `kieran-rails-reviewer.md` - Deep Rails analysis
- `kieran-typescript-reviewer.md` - TypeScript patterns
- `kieran-python-reviewer.md` - Python/PEP patterns
- `julik-frontend-races-reviewer.md` - Race conditions
- `pattern-recognition-specialist.md` - Design patterns

### Design Agents (3)
Visual iteration and QA:
- `figma-design-sync.md` - Figma ↔ Implementation
- `design-iterator.md` - Screenshot-based refinement
- `design-implementation-reviewer.md` - Visual QA

### Development Agents (4)
- `coding.md` - Implementation guidance
- `feature.md` - New feature workflow
- `bugfix.md` - Bug fix workflow
- `migration.md` - Project updates

### Workflow Agents (5)
- `bug-reproduction-validator.md` - Pre-fix validation
- `lint.md` - Multi-language linting
- `pr-comment-resolver.md` - Review feedback
- `spec-flow-analyzer.md` - Spec gap detection
- `style-editor.md` - Documentation polish

### Research Agents (3)
- `repo-analyst.md` - Codebase patterns
- `best-practices-researcher.md` - Industry solutions
- `framework-docs-researcher.md` - API docs (Context7)

## Skills

| Skill | Purpose |
|-------|---------|
| `git-worktree` | Isolated branch development |
| `file-todos` | Structured todo management |
| `validation` | JSON/Pydantic validation |
| `artifact-sync` | Cross-artifact consistency |
| `frontend-design` | Design system reference |
| `gemini-imagegen` | Mockup generation |
| `compound-docs` | Pattern documentation |
| `skill-creator` | Create new skills |

## MCP Servers

- **Playwright**: Browser automation for screenshots, visual testing
- **Context7**: Framework documentation lookup

## Error Handling

All agents output errors in JSON format:

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Description of what failed",
    "details": ["Specific issue 1", "Specific issue 2"],
    "artifact": "prd|flow|erd|etc",
    "remediation": "How to fix the issue"
  }
}
```

## Critical Rules

1. **Validate before emit** - All JSON must pass Pydantic validation
2. **Never regenerate IDs** - Existing IDs are immutable
3. **Stop at approval gates** - Never auto-advance without human approval
4. **Maintain consistency** - Cross-reference artifacts correctly
5. **Document patterns** - Capture reusable patterns for compounding value
6. **Use Python validators** - Run `lint_prd.py`/`lint_erd.py` after generation
