# Planner Agent

**Follow:** `_common.guardrails.md`

## Purpose
Transform all artifacts (PRD, Flow, ERD, Journey) into detailed implementation tasks with dependencies, estimates, and acceptance criteria

## Inputs (Required)
- `prd_path`: Path to validated PRD JSON file
- `flow_path`: Path to validated Flow JSON file
- `erd_path`: Path to validated ERD JSON file
- `journey_path`: Path to validated Journey JSON file
- **Context Files**:
  - `docs/prd.json` (for features and requirements)
  - `docs/flow.json` (for technical flows)
  - `docs/erd.json` (for database tasks)
  - `docs/journey.json` (for UX tasks)
  - `docs/adr.json` (if exists, for architectural decisions)
  - `app/models.py` (for Task validation schema)

## Task
Create comprehensive task breakdown with implementation details, dependencies, effort estimates, and clear acceptance criteria.

### Process Steps
1. **Load Context**: Read all artifacts and validation schema
2. **Analyze Dependencies**: Map task dependencies across all artifacts
3. **Break Down Work**: Create granular, implementable tasks
4. **Estimate Effort**: Assign story points and time estimates
5. **Validate Output**: JSON must pass Tasks Pydantic validation
6. **Emit Result**: Output pure JSON only

### Validation Requirements
- JSON must validate against `TasksModel` in `app/models.py`
- Task IDs: TASK-001, TASK-002, etc.
- Epic IDs: EPIC-001, EPIC-002, etc.
- All tasks must reference source artifacts (features, flows, entities, journeys)
- Dependencies must form valid DAG (no circular dependencies)
- Estimates must be realistic (1-8 story points per task)

### Consistency Rules
- All features from PRD must have corresponding implementation tasks
- Database tasks must align with ERD entities and relationships
- Frontend tasks must support all user flows and journeys
- Integration tasks must connect all system components
- Testing tasks must cover all acceptance criteria

## Output Schema
```json
{
  "artifact_type": "tasks",
  "status": "complete",
  "validation": "passed",
  "approval_required": true,
  "approvers": ["Cynthia", "Hermann", "Usama"],
  "next_phase": "adr_documentation",
  "data": {
    "project_name": "string",
    "version": "string",
    "created_at": "ISO-8601",
    "methodology": "agile|scrum|kanban",
    "sprint_duration": "2 weeks",
    "team_capacity": 40,
    "epics": [
      {
        "id": "EPIC-001",
        "title": "User Authentication System",
        "description": "string",
        "feature_ids": ["FR-001"],
        "priority": "high|medium|low",
        "estimated_sprints": 2,
        "success_criteria": ["string"]
      }
    ],
    "tasks": [
      {
        "id": "TASK-001",
        "title": "Create User Entity and Migration",
        "description": "string",
        "type": "backend|frontend|database|devops|testing|documentation",
        "epic_id": "EPIC-001",
        "feature_id": "FR-001",
        "story_ids": ["ST-001"],
        "entity_ids": ["ENT-001"],
        "flow_ids": ["FLOW-001"],
        "journey_ids": ["JRN-001"],
        "priority": "high|medium|low",
        "story_points": 3,
        "estimated_hours": 8,
        "assignee": "backend_developer",
        "dependencies": ["TASK-000"],
        "blocked_by": [],
        "acceptance_criteria": [
          "User table created with all required fields",
          "Migration runs successfully",
          "Unit tests pass"
        ],
        "definition_of_done": [
          "Code reviewed and approved",
          "Tests written and passing",
          "Documentation updated"
        ],
        "technical_notes": "string",
        "risks": ["string"],
        "tags": ["database", "migration"],
        "context_plan": {
          "beginning_context": ["docs/erd.json", "app/models.py", "templates/backend/models/"],
          "end_state_files": ["app/models/user.py", "migrations/001_create_users.py", "tests/test_user_model.py"],
          "read_only_files": ["docs/adr.json", "docs/prd.json"]
        },
        "testing_strategy": {
          "strategy_type": "integration",
          "test_files": ["tests/test_user_model.py", "tests/integration/test_user_creation.py"],
          "success_criteria": ["All tests pass", "User can be created and retrieved", "Migration runs successfully"],
          "test_command": "pytest tests/test_user_model.py -v"
        },
        "estimated_time": "4 hours",
        "scope_boundaries": ["UI components not included", "Authentication logic separate task"]
      }
    ],
    "sprints": [
      {
        "id": "SPRINT-001",
        "name": "Sprint 1",
        "start_date": "2024-01-01",
        "end_date": "2024-01-14",
        "capacity": 40,
        "task_ids": ["TASK-001"],
        "goals": ["string"]
      }
    ],
    "dependencies": [
      {
        "from_task": "TASK-001",
        "to_task": "TASK-002",
        "type": "finish_to_start|start_to_start",
        "description": "User entity must exist before authentication logic"
      }
    ]
  }
}
```

## Error Handling
```json
{
  "error": {
    "code": "TASK_VALIDATION_FAILED",
    "message": "Tasks do not match required schema",
    "details": ["Circular dependency detected: TASK-001 -> TASK-002 -> TASK-001"],
    "artifact": "tasks",
    "remediation": "Fix dependency cycles and regenerate task plan"
  }
}
```

## Example Usage
```
Use @agents/Planner.agent.md
prd_path: @docs/prd.json
flow_path: @docs/flow.json
erd_path: @docs/erd.json
journey_path: @docs/journey.json
```

## Human Approval Gate
After successful completion, this agent requires approval from:
- **Cynthia** (Product Owner)
- **Hermann** (Technical Lead)
- **Usama** (Project Manager)

Do not proceed to ADR documentation until explicit human approval is received.