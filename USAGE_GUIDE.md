# Usage Guide: Running the Pipeline

## Overview

This guide shows you **exactly how to use** the End-to-End Agentic Development Pipeline to transform a client interview into a production-ready project.

---

## Pipeline Execution Flow

```
Client Interview → PRD → Flow → ERD → Journey → Tasks → ADR → Scaffolded Project
```

Each step uses specialized agents that you invoke with the `@agent` syntax in your AI coding assistant (Cursor, Claude Code, etc.).

---

## Prerequisites

1. Client interview transcript saved as markdown file (e.g., `interviews/client-interview.md`)
2. AI coding assistant with agent support (Cursor or Claude Code)
3. Project initialized with this pipeline system

---

## Step-by-Step Usage

### Step 1: Prepare Client Interview

Create a markdown file with the client interview transcript:

```bash
mkdir -p interviews
nano interviews/client-interview.md
```

**Example Interview Format:**
```markdown
# Client Interview - [Project Name]
Date: 2025-10-01
Client: John Doe (john@example.com)

## Requirements Discussed

**Q: What problem are you trying to solve?**
A: We need a platform where users can book appointments with service providers...

**Q: Who are your target users?**
A: Both service providers and customers...

[Continue with full transcript...]
```

---

### Step 2: Generate PRD (Product Requirements Document)

In your AI coding assistant, type:

```
@PRD.agent.md implement

Generate PRD from client interview:
- transcript_path: interviews/client-interview.md
- project_name: "Appointment Booking Platform"
- owner_email: "john@example.com"
```

**What happens:**
1. PRD agent reads the interview transcript
2. Extracts features, user stories, requirements
3. Creates `docs/prd.json` with structured requirements
4. Marks status as `approval_required: true`

**Output:** `docs/prd.json`

**Next:** Human approval gate (Cynthia + Hermann + Usama review)

---

### Step 3: Generate Flow Diagram

After PRD is approved:

```
@Flow.agent.md implement

Generate user flow from approved PRD:
- prd_path: docs/prd.json
```

**What happens:**
1. Flow agent reads approved PRD
2. Creates user flow diagrams (Mermaid format)
3. Maps user journeys through the application
4. Creates `docs/flow.json`

**Output:** `docs/flow.json`

---

### Step 4: Generate ERD (Entity Relationship Diagram)

```
@ERD.agent.md implement

Generate database schema from PRD and Flow:
- prd_path: docs/prd.json
- flow_path: docs/flow.json
```

**What happens:**
1. ERD agent analyzes requirements and flows
2. Designs database schema with entities and relationships
3. Creates validation rules and constraints
4. Creates `docs/erd.json`

**Output:** `docs/erd.json`

**Next:** Human approval gate (Cynthia + Hassan + Usama review)

---

### Step 5: Generate User Journey Map

```
@Journey.agent.md implement

Generate user journey map:
- prd_path: docs/prd.json
- flow_path: docs/flow.json
- erd_path: docs/erd.json
```

**What happens:**
1. Journey agent maps complete user experiences
2. Identifies touchpoints, pain points, opportunities
3. Creates `docs/journey.json`

**Output:** `docs/journey.json`

---

### Step 6: Generate Task Breakdown

```
@Planner.agent.md implement

Break down project into Linear tasks:
- prd_path: docs/prd.json
- flow_path: docs/flow.json
- erd_path: docs/erd.json
- journey_path: docs/journey.json
```

**What happens:**
1. Planner agent creates detailed task breakdown
2. Organizes tasks by phase and priority
3. Creates Linear-compatible task list
4. Creates `docs/tasks.json`

**Output:** `docs/tasks.json`

**Next:** Human approval gate (Cynthia + Hermann + Usama review)

---

### Step 7: Generate Architecture Decisions

```
@ADR.agent.md implement

Generate architecture decisions:
- prd_path: docs/prd.json
- erd_path: docs/erd.json
- tasks_path: docs/tasks.json
```

**What happens:**
1. ADR agent analyzes all previous artifacts
2. Makes technology stack decisions (NextJS vs FastAPI, etc.)
3. Decides on architecture patterns
4. Creates/updates `docs/adr.json`

**Output:** `docs/adr.json` (updated with new decisions)

---

### Step 8: Generate Scaffolding Plan (Stage 1)

```
make scaffold-plan

# Or manually:
@Scaffolder.agent.md implement plan

Generate scaffolding plan:
- prd_path: docs/prd.json
- erd_path: docs/erd.json
- adr_path: docs/adr.json
- tasks_path: docs/tasks.json
```

**What happens:**
1. Scaffolder agent (planning mode) reads all artifacts
2. Creates detailed project structure plan
3. Specifies all files, dependencies, configurations
4. Creates `docs/scaffold-plan.json`
5. **DOES NOT CREATE ANY FILES** (planning only)

**Output:** `docs/scaffold-plan.json`

**Next:** Human approval gate (Cynthia + Usama review plan)

---

### Step 9: Execute Scaffolding (Stage 2)

**ONLY after plan approval:**

```
make scaffold-apply

# Or manually:
@Scaffolder.agent.md implement build

Execute approved scaffolding plan:
- plan_path: docs/scaffold-plan.json
- output_dir: ../generated-projects/[project-name]
```

**What happens:**
1. Scaffolder agent (build mode) reads approved plan
2. Creates complete project directory structure
3. Generates all boilerplate code (CRUD, Auth, etc.)
4. Installs dependencies
5. Configures environments
6. Creates project-specific agents and rules
7. Sets up git repository

**Output:** Complete project in `../generated-projects/[project-name]/`

---

## Using Rules and Context

### Adding Context with @ Mentions

You can reference specific files for additional context:

```
@PRD.agent.md @interviews/client-interview.md @docs/adr.json implement

Generate PRD considering existing architectural decisions
```

### Using Guardrails

All agents automatically follow common guardrails. To add custom rules:

```
@PRD.agent.md @custom-rules.md implement

Generate PRD with custom validation rules
```

---

## Advanced Usage

### Re-running Stages

If you need to regenerate an artifact:

```
@PRD.agent.md implement

Regenerate PRD with updated requirements:
- transcript_path: interviews/client-interview-v2.md
- project_name: "Appointment Booking Platform"
- owner_email: "john@example.com"
- preserve_ids: true  # Keep existing FR-001, ST-001 IDs
```

### Partial Updates

Update specific sections:

```
@ERD.agent.md implement

Update ERD to add new "Payment" entity:
- prd_path: docs/prd.json
- existing_erd: docs/erd.json
- new_requirements: "Add payment processing with Stripe"
```

### Validation

Validate artifacts before approval:

```bash
# PRD validation
python -m app.validators.prd_validator docs/prd.json

# ERD validation
python -m app.validators.erd_validator docs/erd.json
```

---

## Example: Complete Pipeline Run

Here's a real example from start to finish:

```bash
# 1. Create interview transcript
mkdir -p interviews
nano interviews/saas-booking-platform.md
# [Add interview content...]

# 2. Generate PRD
```
In AI assistant:
```
@PRD.agent.md implement
transcript_path: interviews/saas-booking-platform.md
project_name: "BookEasy - Service Booking Platform"
owner_email: "founder@bookeasy.com"
```

Wait for approval ✓

```bash
# 3. Generate Flow
```
```
@Flow.agent.md implement
prd_path: docs/prd.json
```

```bash
# 4. Generate ERD
```
```
@ERD.agent.md implement
prd_path: docs/prd.json
flow_path: docs/flow.json
```

Wait for approval ✓

```bash
# 5. Generate Journey
```
```
@Journey.agent.md implement
prd_path: docs/prd.json
flow_path: docs/flow.json
erd_path: docs/erd.json
```

```bash
# 6. Generate Tasks
```
```
@Planner.agent.md implement
prd_path: docs/prd.json
flow_path: docs/flow.json
erd_path: docs/erd.json
journey_path: docs/journey.json
```

Wait for approval ✓

```bash
# 7. Generate ADR
```
```
@ADR.agent.md implement
prd_path: docs/prd.json
erd_path: docs/erd.json
tasks_path: docs/tasks.json
```

```bash
# 8. Generate Scaffolding Plan
```
```
@Scaffolder.agent.md implement plan
prd_path: docs/prd.json
erd_path: docs/erd.json
adr_path: docs/adr.json
tasks_path: docs/tasks.json
```

Wait for approval ✓

```bash
# 9. Build Project
```
```
@Scaffolder.agent.md implement build
plan_path: docs/scaffold-plan.json
output_dir: ../generated-projects/bookeasy
```

```bash
# 10. Verify output
cd ../generated-projects/bookeasy
ls -la
# Should see: src/, tests/, .cursor/, agents/, README.md, etc.

# 11. Push to GitHub
git remote add origin https://github.com/your-org/bookeasy.git
git push -u origin main
```

**Done!** You now have a complete, production-ready project repository.

---

## Status Tracking During Pipeline

As you run each step, update the project status:

```bash
# After each stage completes
make save-status
```

This tracks progress in `PROJECT_STATUS.json` and syncs with the team.

---

## Troubleshooting

### "Agent not found"

Make sure you're using the correct agent file name:
```bash
ls agents/
# Should show: PRD.agent.md, Flow.agent.md, etc.
```

### "Validation failed"

Check the artifact against the schema:
```bash
cat docs/prd.json | jq .
python -m app.validators.prd_validator docs/prd.json
```

### "Approval required"

Check who needs to approve:
```bash
cat docs/prd.json | jq '.approvers'
# Shows: ["Cynthia", "Hermann", "Usama"]
```

### "File not found"

Ensure previous steps completed:
```bash
ls docs/
# Should show: prd.json, flow.json, erd.json, etc.
```

---

## Quick Reference Commands

```bash
# Status management
make status              # Check current pipeline status
make save-status         # Save progress

# Validation
python -m app.validators.prd_validator docs/prd.json
python -m app.validators.erd_validator docs/erd.json

# Scaffolding
make scaffold-plan       # Generate plan (Stage 1)
make scaffold-apply      # Build project (Stage 2)
```

---

## Next Steps After Scaffolding

Once the project is generated:

1. **Navigate to project:**
   ```bash
   cd ../generated-projects/[project-name]
   ```

2. **Review project-specific README:**
   ```bash
   cat README.md
   ```

3. **Start development:**
   ```bash
   npm install          # or appropriate package manager
   npm run dev          # Start development server
   ```

4. **Use project-specific agents:**
   The generated project has its own `.cursor/rules/` and `agents/` for feature development

5. **Report back to mothership:**
   Progress syncs back to the main pipeline via `mothership/` directory

---

## Summary

**The complete flow is:**

1. Write client interview → `interviews/client-interview.md`
2. `@PRD.agent.md implement` → `docs/prd.json` → Approval
3. `@Flow.agent.md implement` → `docs/flow.json`
4. `@ERD.agent.md implement` → `docs/erd.json` → Approval
5. `@Journey.agent.md implement` → `docs/journey.json`
6. `@Planner.agent.md implement` → `docs/tasks.json` → Approval
7. `@ADR.agent.md implement` → `docs/adr.json`
8. `@Scaffolder.agent.md implement plan` → `docs/scaffold-plan.json` → Approval
9. `@Scaffolder.agent.md implement build` → `../generated-projects/[project]/`
10. `cd ../generated-projects/[project]` → Start building features!

**Key insight:** Each `@agent.md` file is a specialized AI agent that you invoke by mentioning it in your coding assistant, then giving it the `implement` command with required parameters.

---

*Need help? See [WORKFLOW.md](WORKFLOW.md) for team collaboration or [README.md](README.md) for system overview.*
