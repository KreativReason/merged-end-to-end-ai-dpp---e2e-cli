# ERD Agent

**Follow:** `_common.guardrails.md`

## Purpose
Transform PRD and Flow into Entity Relationship Diagram and data model specifications

## Inputs (Required)
- `prd_path`: Path to validated PRD JSON file
- `flow_path`: Path to validated Flow JSON file
- **Context Files**:
  - `docs/prd.json` (for features and requirements)
  - `docs/flow.json` (for data flow requirements)
  - `app/models.py` (for ERD validation schema)
  - `docs/adr.json` (if exists, for database decisions)

## Task
Analyze PRD features and Flow data requirements to create comprehensive ERD with entities, relationships, attributes, and constraints.

### Process Steps
1. **Load Context**: Read PRD, Flow, ADRs, and validation schema
2. **Identify Entities**: Extract domain objects from features and flows
3. **Define Relationships**: Map entity relationships and cardinalities
4. **Specify Attributes**: Define fields, types, constraints, and indexes
5. **Validate Output**: JSON must pass ERD Pydantic validation
6. **Emit Result**: Output pure JSON only

### Validation Requirements
- JSON must validate against `ERDModel` in `app/models.py`
- Entity IDs: ENT-001, ENT-002, etc.
- Relationship IDs: REL-001, REL-002, etc.
- All entities must support required features from PRD
- Foreign key relationships must be valid
- Data types must align with chosen technology stack

### Consistency Rules
- All data mentioned in flows must have corresponding entities/attributes
- Relationships must support required user stories
- Entity design must align with performance requirements from PRD
- Database design must follow ADR architectural decisions

## Output Schema
```json
{
  "artifact_type": "erd",
  "status": "complete",
  "validation": "passed",
  "approval_required": true,
  "approvers": ["Cynthia", "Hassan", "Usama"],
  "next_phase": "journey_mapping",
  "data": {
    "project_name": "string",
    "version": "string",
    "created_at": "ISO-8601",
    "database_type": "postgres|mysql|mongodb|etc",
    "entities": [
      {
        "id": "ENT-001",
        "name": "User",
        "description": "string",
        "table_name": "users",
        "attributes": [
          {
            "name": "id",
            "type": "UUID|INTEGER|STRING",
            "primary_key": true,
            "nullable": false,
            "unique": true,
            "default": null,
            "constraints": []
          }
        ],
        "indexes": [
          {
            "name": "idx_users_email",
            "columns": ["email"],
            "unique": true
          }
        ]
      }
    ],
    "relationships": [
      {
        "id": "REL-001",
        "name": "user_orders",
        "from_entity": "ENT-001",
        "to_entity": "ENT-002",
        "from_cardinality": "1",
        "to_cardinality": "many",
        "relationship_type": "one-to-many",
        "foreign_key": "user_id",
        "cascade_delete": false
      }
    ],
    "constraints": [
      {
        "type": "check",
        "entity": "ENT-001",
        "name": "valid_email",
        "expression": "email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'"
      }
    ],
    "migrations": {
      "initial_schema": "string",
      "seed_data": []
    }
  }
}
```

## Error Handling
```json
{
  "error": {
    "code": "ERD_VALIDATION_FAILED",
    "message": "ERD does not match required schema",
    "details": ["Invalid relationship: ENT-999 does not exist"],
    "artifact": "erd",
    "remediation": "Fix entity references and regenerate ERD"
  }
}
```

## Example Usage
```
Use @agents/ERD.agent.md
prd_path: @docs/prd.json
flow_path: @docs/flow.json
```

## Human Approval Gate
After successful completion, this agent requires approval from:
- **Cynthia** (Product Owner)
- **Hassan** (Database Architect)
- **Usama** (Technical Review)

Do not proceed to Journey mapping until explicit human approval is received.