# Handoff Command

> Transition a project from genesis to development phase

## Usage

```
/kreativreason:handoff project_path:<path>
```

## Description

The Handoff command completes the genesis phase by installing development agents, configuring project connections, and preparing the project for the ongoing development cycle.

**Note**: Handoff operates on the **external project directory** created by genesis, not within the CLI.

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `project_path` | Yes | Absolute path to generated project (the `output_path` from genesis) |

## When to Use

Run handoff after:
- `/kreativreason:genesis` completes scaffold apply
- Manually scaffolded project needs development agents
- Updating an existing project's agent configuration

## What Handoff Does

### 1. Verify Genesis Completion

```
Check for required artifacts:
  ✓ docs/prd.json
  ✓ docs/flows/
  ✓ docs/erd.json
  ✓ docs/journey.json
  ✓ docs/tasks.json
  ✓ docs/adr/project.json
  ✓ docs/scaffold-applied.json
```

### 2. Install Development Agents

Copy from plugin templates to project:

```
project/
├── .claude/
│   └── commands/
│       ├── plan.md      → /plan
│       ├── work.md      → /work
│       ├── review.md    → /review
│       ├── feature.md   → /feature
│       └── bugfix.md    → /bugfix
├── agents/
│   ├── coding.md
│   ├── feature.md
│   ├── bugfix.md
│   └── _guardrails.md
```

### 3. Configure Project Connection

Create mothership connection:

```json
// mothership/connection.json
{
  "mothership_version": "1.0.0",
  "project_version": "1.0.0",
  "genesis_date": "2024-01-15T10:30:00Z",
  "genesis_pipeline": "kreativreason-e2e-cli",
  "project_name": "My Project",
  "sync_enabled": true,
  "last_sync": null
}
```

### 4. Generate Quick Reference

Create project-specific quick reference:

```markdown
// DEVELOPMENT.md

## Quick Start

### Add a Feature
/kreativreason:plan "Feature description"
/kreativreason:work plans/feat-xxx.md

### Fix a Bug
/kreativreason:bugfix severity:high "Bug description"

### Code Review
/kreativreason:review #PR_NUMBER

## Project Commands
- /plan - Create implementation plan
- /work - Execute plan
- /review - Multi-agent code review
- /feature - Add new feature
- /bugfix - Fix bugs systematically
```

### 5. Initialize Development State

```json
// .kreativreason/state.json
{
  "phase": "development",
  "genesis_complete": true,
  "active_plans": [],
  "completed_features": [],
  "pending_reviews": []
}
```

## Output Schema

```json
{
  "artifact_type": "handoff_report",
  "status": "complete",
  "data": {
    "project_path": "/path/to/project",
    "handoff_at": "ISO-8601",
    "genesis_verified": true,
    "components_installed": {
      "commands": ["plan", "work", "review", "feature", "bugfix"],
      "agents": ["coding", "feature", "bugfix", "_guardrails"],
      "config": ["connection.json", "state.json"]
    },
    "mothership_connection": {
      "status": "configured",
      "sync_enabled": true
    },
    "next_steps": [
      "Review docs/tasks.json for first sprint tasks",
      "Run /kreativreason:plan for first feature",
      "Set up CI/CD if not already configured"
    ],
    "available_commands": {
      "/plan": "Create implementation plans",
      "/work": "Execute plans with testing",
      "/review": "Multi-agent code review",
      "/feature": "Add new features",
      "/bugfix": "Systematic bug fixes"
    }
  }
}
```

## Verification Checklist

Before handoff completes, verify:

```markdown
## Genesis Artifacts
- [ ] PRD exists and is valid
- [ ] Flows exist and reference PRD
- [ ] ERD exists and aligns with flows
- [ ] Journey maps exist
- [ ] Tasks are defined
- [ ] ADRs document decisions

## Project Structure
- [ ] Source code directories exist
- [ ] Dependencies installed
- [ ] Environment template exists
- [ ] Git initialized

## Development Ready
- [ ] Can run dev server
- [ ] Can run tests
- [ ] Lint passes
```

## Example

```
/kreativreason:handoff project_path:~/Projects/acme-app

> 🔄 Starting handoff process...
> Project: ~/Projects/acme-app
>
> Verifying genesis completion...
>   ✓ docs/prd.json
>   ✓ docs/flows/
>   ✓ docs/erd.json
>   ✓ docs/journey.json
>   ✓ docs/tasks.json
>   ✓ docs/adr/project.json
>   ✓ docs/scaffold-applied.json
>
> Installing development agents...
>   ✓ Installed 5 commands
>   ✓ Installed 4 agents
>   ✓ Created mothership connection
>   ✓ Generated DEVELOPMENT.md
>
> 🎉 Handoff complete!
>
> Your project is ready for development at:
>   ~/Projects/acme-app
>
> Available commands:
>   /plan    - Create implementation plans
>   /work    - Execute plans
>   /review  - Code review
>   /feature - Add features
>   /bugfix  - Fix bugs
>
> Suggested first steps:
>   1. cd ~/Projects/acme-app
>   2. Review docs/tasks.json for sprint planning
>   3. Run: /kreativreason:plan "First feature from tasks"
```

## Post-Handoff Workflow

```
Genesis Complete
      │
      ▼
  Handoff
      │
      ▼
┌─────────────────────────────────────┐
│         Development Cycle           │
│                                     │
│    /plan → /work → /review → merge  │
│         ↑                    │      │
│         └────────────────────┘      │
│                                     │
│    Repeat for each feature/fix      │
└─────────────────────────────────────┘
```
