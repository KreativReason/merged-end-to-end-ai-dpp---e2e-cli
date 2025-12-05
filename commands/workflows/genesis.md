# Genesis Command

> Transform client interview into a production-ready project

## Usage

```
/kreativreason:genesis transcript_path:<path> output_path:<path>
```

## Description

The Genesis command executes the complete E2E pipeline, transforming a client interview transcript into a fully scaffolded, ready-to-develop project. This is the entry point for new projects.

**Important**: Projects are always created in an **external directory** specified by `output_path`. This keeps the CLI lightweight and prevents bloat from accumulating generated projects.

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `transcript_path` | Yes | Path to client interview transcript (markdown) |
| `output_path` | Yes | Absolute path where project will be created (e.g., `~/Projects/my-app`) |
| `project_name` | No | Override project name (extracted from transcript if not provided) |

## Pipeline Stages

```
Interview → PRD → Flow → ERD → Journey → Tasks → ADR → Scaffold Plan → Scaffold Apply → Handoff
```

Each stage has a human approval gate before proceeding.

## Workflow

### Stage 1: Requirements (PRD)
```
1. Load interview transcript
2. Invoke genesis/prd agent
3. Generate docs/prd.json
4. PAUSE for human approval
```

### Stage 2: Flows
```
1. Load approved PRD
2. Invoke genesis/flow agent
3. Generate docs/flows/
4. PAUSE for human approval
```

### Stage 3: Data Model (ERD)
```
1. Load approved PRD + Flows
2. Invoke genesis/erd agent
3. Generate docs/erd.json
4. PAUSE for human approval
```

### Stage 4: User Journeys
```
1. Load all approved artifacts
2. Invoke genesis/journey agent
3. Generate docs/journey.json
4. PAUSE for human approval
```

### Stage 5: Task Planning
```
1. Load all approved artifacts
2. Invoke genesis/planner agent
3. Generate docs/tasks.json
4. PAUSE for human approval
```

### Stage 6: Architecture Decisions (ADR)
```
1. Load all approved artifacts
2. Invoke genesis/adr agent
3. Generate docs/adr/project.json
4. PAUSE for human approval
```

### Stage 7: Scaffolding Plan
```
1. Load all approved artifacts
2. Invoke genesis/scaffolder agent (mode: plan)
3. Generate docs/scaffold-plan.json
4. PAUSE for human approval
```

### Stage 8: Scaffolding Apply
```
1. Load approved scaffold plan
2. Invoke genesis/scaffolder agent (mode: apply, output_path: <output_path>)
3. Create complete project structure at output_path
4. Install dependencies
5. Initialize git repository
6. Register project in CLI's .kreativreason/projects.json
```

### Stage 9: Handoff
```
1. Invoke /kreativreason:handoff
2. Install development agents
3. Configure project connection
4. Ready for development phase
```

## Approval Gates

Each stage requires explicit approval before proceeding:

| Stage | Approvers | What to Check |
|-------|-----------|---------------|
| PRD | Product Owner, Tech Lead | Requirements accuracy |
| Flow | Product Owner, UX Designer | User flow correctness |
| ERD | Tech Lead, DBA | Data model completeness |
| Journey | Product Owner, UX Designer | User experience quality |
| Tasks | Product Owner, Tech Lead, PM | Implementation plan |
| ADR | Tech Lead, Architect | Technology decisions |
| Scaffold | Product Owner, Tech Lead | Project structure |

## Output

Upon completion, you have:

**In the generated project** (at `output_path`):
- Complete project documentation in `docs/`
- Scaffolded codebase with chosen tech stack
- Development agents installed
- Git repository initialized
- `mothership/connection.json` linking back to CLI
- Ready to run `/kreativreason:plan` for first feature

**In the CLI** (stays lightweight):
- Project reference in `.kreativreason/projects.json`
- No generated code stored here

## Example

```
/kreativreason:genesis transcript_path:interviews/acme-client-call.md output_path:~/Projects/acme-app

> Starting Genesis pipeline...
> Output path: ~/Projects/acme-app
>
> Stage 1: Generating PRD from transcript...
> ✓ PRD generated: docs/prd.json
>
> 🛑 APPROVAL REQUIRED
> Please review docs/prd.json
> Approvers: Product Owner, Tech Lead
>
> Type 'approve' to continue or provide feedback
```

## Resuming Genesis

If interrupted, genesis can resume from the last completed stage:

```
/kreativreason:genesis --resume

> Detected incomplete genesis at Stage 4 (Journey)
> Previous stages verified:
>   ✓ PRD (approved)
>   ✓ Flow (approved)
>   ✓ ERD (approved)
>
> Resuming from Journey stage...
```

## Error Handling

If any stage fails validation:
```json
{
  "stage": "erd",
  "status": "failed",
  "error": {
    "code": "ERD_VALIDATION_FAILED",
    "message": "Entity reference not found",
    "details": ["REL-005 references non-existent ENT-999"],
    "remediation": "Fix entity references and regenerate"
  },
  "action": "Fix the issue and run: /kreativreason:genesis --resume"
}
```

## Post-Genesis

After successful genesis, the project is ready for the development cycle:
1. `/kreativreason:plan` - Plan new features
2. `/kreativreason:work` - Implement plans
3. `/kreativreason:review` - Review code changes
