# Artifact Sync Skill

## Purpose

Maintain consistency and synchronization between pipeline artifacts as changes occur.

## Overview

This skill ensures that changes to one artifact (e.g., adding a feature to PRD) are properly propagated to dependent artifacts (flows, tasks, etc.).

## Dependency Graph

```
PRD (source of truth)
 │
 ├─► Flow (references PRD features/stories)
 │    │
 │    └─► ERD (supports flow data requirements)
 │         │
 │         └─► Journey (maps touchpoints to entities)
 │              │
 │              └─► Tasks (implements all above)
 │                   │
 │                   └─► ADR (documents decisions)
 │                        │
 │                        └─► Scaffold (applies all)
```

## Skill Functions

### `check_sync_status()`

Checks if all artifacts are synchronized.

**Output:**
```json
{
  "in_sync": false,
  "status": {
    "prd": {
      "last_modified": "2024-01-15T10:30:00Z",
      "hash": "abc123"
    },
    "flow": {
      "last_modified": "2024-01-15T09:00:00Z",
      "hash": "def456",
      "synced_with_prd": false,
      "missing_features": ["FR-016", "FR-017"]
    },
    "erd": {
      "last_modified": "2024-01-15T09:00:00Z",
      "hash": "ghi789",
      "synced_with_flow": true
    }
  },
  "sync_required": ["flow"],
  "recommendation": "Re-run flow agent to incorporate new PRD features"
}
```

### `get_change_impact(artifact_type, changes)`

Analyzes impact of proposed changes.

**Input:**
```json
{
  "artifact_type": "prd",
  "changes": {
    "added_features": ["FR-016"],
    "modified_features": ["FR-005"],
    "removed_features": []
  }
}
```

**Output:**
```json
{
  "impact_analysis": {
    "flow": {
      "impact": "high",
      "required_changes": [
        "Add flows for FR-016",
        "Review flows for FR-005"
      ]
    },
    "erd": {
      "impact": "medium",
      "required_changes": [
        "May need new entities for FR-016"
      ]
    },
    "journey": {
      "impact": "medium",
      "required_changes": [
        "Update touchpoints for modified feature"
      ]
    },
    "tasks": {
      "impact": "high",
      "required_changes": [
        "Add tasks for new feature",
        "Review existing task estimates"
      ]
    }
  },
  "estimated_effort": "2-4 hours to resync all artifacts"
}
```

### `propagate_change(source_artifact, change)`

Propagates a change to dependent artifacts.

**Input:**
```json
{
  "source_artifact": "prd",
  "change": {
    "type": "add_feature",
    "feature": {
      "id": "FR-016",
      "title": "Export Reports",
      "stories": [...]
    }
  }
}
```

**Output:**
```json
{
  "propagation_result": {
    "source": "prd",
    "affected_artifacts": ["flow", "erd", "journey", "tasks"],
    "actions": [
      {
        "artifact": "flow",
        "action": "create_placeholder",
        "details": "Created FLOW-016 placeholder for FR-016"
      },
      {
        "artifact": "tasks",
        "action": "create_task",
        "details": "Created TASK-045: Implement Export Reports"
      }
    ],
    "manual_review_required": [
      "flow: Detailed flow steps needed",
      "erd: Entity design needed"
    ]
  }
}
```

### `sync_artifact(artifact_type)`

Synchronizes an artifact with its dependencies.

**Input:**
```json
{
  "artifact_type": "flow"
}
```

**Output:**
```json
{
  "sync_result": {
    "artifact": "flow",
    "status": "synced",
    "changes_made": [
      "Added placeholder for FR-016",
      "Updated feature reference for FR-005"
    ],
    "manual_action_required": [
      "Complete flow steps for FLOW-016"
    ],
    "validation": {
      "valid": true,
      "warnings": 1
    }
  }
}
```

### `generate_sync_report()`

Generates comprehensive sync status report.

**Output:**
```json
{
  "report": {
    "generated_at": "2024-01-15T14:30:00Z",
    "overall_status": "needs_attention",
    "artifacts": {
      "prd": {"status": "source", "version": "1.3.0"},
      "flow": {"status": "out_of_sync", "behind_by": 2},
      "erd": {"status": "synced", "version": "1.2.0"},
      "journey": {"status": "synced", "version": "1.2.0"},
      "tasks": {"status": "out_of_sync", "behind_by": 1},
      "adr": {"status": "synced", "version": "1.1.0"}
    },
    "recommended_actions": [
      "1. Re-run flow agent for FR-016, FR-017",
      "2. Re-run planner agent after flow update"
    ],
    "estimated_sync_time": "1-2 hours"
  }
}
```

## Sync Rules

### Automatic Propagation
- ID references (feature_id, story_id, etc.)
- Timestamps and version numbers
- Status fields

### Manual Review Required
- Business logic changes
- Architectural decisions
- New entity designs
- Flow step details

## Conflict Resolution

When changes conflict:

```json
{
  "conflict": {
    "artifact": "flow",
    "field": "feature_id",
    "current_value": "FR-005",
    "incoming_value": null,
    "reason": "Feature FR-005 was removed from PRD"
  },
  "resolution_options": [
    {
      "option": "remove",
      "description": "Remove flow that references deleted feature"
    },
    {
      "option": "reassign",
      "description": "Reassign flow to different feature"
    },
    {
      "option": "keep",
      "description": "Keep flow as orphan (not recommended)"
    }
  ]
}
```

## Version Tracking

Each artifact tracks:
```json
{
  "version": "1.2.0",
  "last_modified": "2024-01-15T10:30:00Z",
  "modified_by": "agent/prd",
  "parent_versions": {
    "prd": "1.3.0"
  },
  "hash": "sha256:abc123..."
}
```

## Integration

### With Genesis Pipeline
Sync runs automatically between pipeline stages.

### With Development Phase
Manual sync check recommended before major features.

### With Migration
Sync status verified during mothership updates.
