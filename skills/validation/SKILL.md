# Validation Skill

## Purpose

Validate JSON artifacts against Pydantic schemas, ensuring data integrity throughout the E2E pipeline.

## Overview

This skill provides utilities for validating pipeline artifacts (PRD, Flow, ERD, Journey, Tasks, ADR, Scaffold) against their defined schemas.

## Supported Schemas

| Artifact | Schema | File |
|----------|--------|------|
| PRD | `PRDModel` | `app/models.py` |
| Flow | `FlowModel` | `app/models.py` |
| ERD | `ERDModel` | `app/models.py` |
| Journey | `JourneyModel` | `app/models.py` |
| Tasks | `TasksModel` | `app/models.py` |
| ADR | `ADRModel` | `app/models.py` |
| Scaffold | `ScaffoldModel` | `app/models.py` |

## Skill Functions

### `validate_artifact(artifact_type, data)`

Validates artifact data against its schema.

**Input:**
```json
{
  "artifact_type": "prd",
  "data": { ... artifact JSON ... }
}
```

**Output (Success):**
```json
{
  "valid": true,
  "artifact_type": "prd",
  "validation_time": "0.023s",
  "warnings": []
}
```

**Output (Failure):**
```json
{
  "valid": false,
  "artifact_type": "prd",
  "errors": [
    {
      "field": "features[0].id",
      "error": "Invalid format: expected FR-XXX",
      "value": "feature-1"
    },
    {
      "field": "owner_email",
      "error": "Field required",
      "value": null
    }
  ],
  "error_count": 2
}
```

### `validate_file(file_path)`

Validates a JSON file against its inferred schema.

**Input:**
```json
{
  "file_path": "docs/prd.json"
}
```

**Output:**
```json
{
  "valid": true,
  "file_path": "docs/prd.json",
  "artifact_type": "prd",
  "file_size": "12.5KB",
  "validation_time": "0.045s"
}
```

### `validate_cross_references()`

Validates cross-references between artifacts.

**Output:**
```json
{
  "valid": true,
  "checks": [
    {
      "check": "Flow references PRD features",
      "status": "pass",
      "details": "All 15 flow feature_ids exist in PRD"
    },
    {
      "check": "ERD entities support flows",
      "status": "pass",
      "details": "All data requirements covered"
    },
    {
      "check": "Tasks reference valid artifacts",
      "status": "warning",
      "details": "TASK-015 references non-existent FLOW-099"
    }
  ],
  "warnings": 1,
  "errors": 0
}
```

### `get_schema(artifact_type)`

Returns the schema definition for an artifact type.

**Input:**
```json
{
  "artifact_type": "prd"
}
```

**Output:**
```json
{
  "artifact_type": "prd",
  "schema": {
    "type": "object",
    "required": ["project_name", "features"],
    "properties": {
      "project_name": {"type": "string"},
      "features": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["id", "title"],
          "properties": {
            "id": {"type": "string", "pattern": "^FR-\\d{3}$"},
            "title": {"type": "string", "minLength": 3}
          }
        }
      }
    }
  }
}
```

## ID Validation Rules

### Feature IDs
- Pattern: `FR-XXX` (e.g., FR-001, FR-002)
- Must be unique within PRD
- Cannot be regenerated once created

### Story IDs
- Pattern: `ST-XXX` (e.g., ST-001, ST-002)
- Must reference valid feature

### Flow IDs
- Pattern: `FLOW-XXX` (e.g., FLOW-001)
- Must reference valid PRD feature

### Entity IDs
- Pattern: `ENT-XXX` (e.g., ENT-001)
- Must be unique within ERD

### Task IDs
- Pattern: `TASK-XXX` (e.g., TASK-001)
- Must reference valid source artifacts

### ADR IDs
- Pattern: `ADR-XXXX` (e.g., ADR-0001)
- 4-digit zero-padded

## Validation Modes

### Strict Mode (Default)
All required fields must be present, all references must be valid.

### Lenient Mode
Warnings instead of errors for missing optional fields.

```json
{
  "artifact_type": "prd",
  "data": { ... },
  "mode": "lenient"
}
```

### Draft Mode
Minimal validation for work-in-progress artifacts.

```json
{
  "artifact_type": "prd",
  "data": { ... },
  "mode": "draft"
}
```

## Integration with Pipeline

### Before Agent Output
Each genesis agent validates output before emitting:

```python
result = agent.generate()
validation = validate_artifact(artifact_type, result)
if not validation.valid:
    return error_response(validation.errors)
```

### Continuous Validation
Run validation across all artifacts:

```bash
/kreativreason:validate --all

> Validating pipeline artifacts...
>   ✓ docs/prd.json (valid)
>   ✓ docs/flows/final_flow.json (valid)
>   ✓ docs/erd.json (valid)
>   ✓ docs/journey.json (valid)
>   ✓ docs/tasks.json (valid)
>   ✓ docs/adr/project.json (valid)
>
> Cross-reference check...
>   ✓ All references valid
>
> Result: All artifacts valid
```

## Error Messages

| Error Code | Description | Resolution |
|------------|-------------|------------|
| `MISSING_REQUIRED` | Required field missing | Add the field |
| `INVALID_ID_FORMAT` | ID doesn't match pattern | Fix ID format |
| `DUPLICATE_ID` | ID already exists | Use unique ID |
| `INVALID_REFERENCE` | Referenced ID not found | Fix reference |
| `TYPE_MISMATCH` | Wrong data type | Fix value type |
| `CONSTRAINT_VIOLATION` | Value doesn't meet constraint | Fix value |
