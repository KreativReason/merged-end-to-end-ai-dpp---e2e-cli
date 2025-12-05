# Migration Agent

**Follow:** `_common.guardrails.md`

## Purpose
Manage updates and synchronization between mothership pipeline and generated projects, applying template improvements and handling breaking changes.

## Inputs (Required)
- `project_path`: Path to generated project directory
- `mode`: "check" | "preview" | "apply"
- `mothership_path`: Path to mothership pipeline (default: auto-detect from mothership/connection.json)
- **Context Files**:
  - `mothership/connection.json` (for version tracking and mothership location)
  - `mothership/CHANGELOG.md` (for available updates)
  - `docs/adr/mothership.json` (for inherited ADR decisions)
  - `templates/agents/project-specific/` (for latest agent templates)
  - `app/models.py` (for validation schema)

## Task
Synchronize generated projects with mothership improvements, applying template updates, fixing bugs, and managing breaking changes while preserving project customizations.

### Process Steps
1. **Load Context**: Read project connection.json and mothership CHANGELOG.md
2. **Version Check**: Compare project version with mothership version
3. **Identify Updates**: Determine available updates since last sync
4. **Analyze Impact**: Categorize updates (non-breaking, breaking, security)
5. **Generate Plan**: Create migration plan with changes to apply (if mode=check or preview)
6. **Apply Updates**: Execute template updates and migration scripts (if mode=apply)
7. **Validate Compliance**: Verify project structure matches latest standards
8. **Update Metadata**: Update connection.json with new sync timestamp
9. **Emit Result**: Output pure JSON only

### Validation Requirements
- JSON must validate against `MigrationResultModel` in `app/models.py`
- All template updates must preserve project customizations
- Breaking changes must include migration scripts
- Version numbers must follow semantic versioning (MAJOR.MINOR.PATCH)
- Sync timestamps must be ISO-8601 format

### Consistency Rules
- Mothership ADRs remain read-only, never modified by migration
- Project-specific agents can be updated but preserve custom modifications
- .cursorrules critical rules (German fields, multi-tenancy) must never be removed
- Formula preservation rules must be maintained across updates
- organizationId requirements must be enforced in all updates

## Mode: Check

Check for available mothership updates without making changes.

### Output Schema
```json
{
  "artifact_type": "migration_check",
  "status": "complete",
  "validation": "passed",
  "approval_required": false,
  "next_phase": "migration_preview",
  "data": {
    "project_name": "string",
    "project_version": "1.0.0",
    "mothership_version": "1.2.0",
    "last_sync": "2025-10-16T15:05:42Z",
    "updates_available": true,
    "update_summary": {
      "total_updates": 3,
      "non_breaking": 2,
      "breaking": 1,
      "security": 0
    },
    "available_updates": [
      {
        "version": "1.1.0",
        "date": "2025-10-16",
        "type": "non-breaking",
        "changelog_entry": "ADR-0011: Added agent system templates",
        "affected_files": [
          "agents/_common.guardrails.md",
          "agents/Feature.agent.md"
        ]
      },
      {
        "version": "1.2.0",
        "date": "2025-10-16",
        "type": "breaking",
        "changelog_entry": "ADR-0012: Migration agent and update protocol",
        "affected_files": [
          "mothership/connection.json"
        ],
        "migration_required": true
      }
    ],
    "recommendation": "Run migration preview to see detailed changes"
  }
}
```

## Mode: Preview

Preview changes that would be applied without executing them.

### Output Schema
```json
{
  "artifact_type": "migration_preview",
  "status": "complete",
  "validation": "passed",
  "approval_required": true,
  "approvers": ["Cynthia", "Usama"],
  "next_phase": "migration_apply",
  "data": {
    "project_name": "string",
    "from_version": "1.0.0",
    "to_version": "1.2.0",
    "preview_date": "2025-10-16T19:00:00Z",
    "changes": [
      {
        "file_path": "agents/_common.guardrails.md",
        "action": "update",
        "type": "template_refresh",
        "diff_summary": "Added formula preservation section (lines 45-67)",
        "backup_created": true,
        "custom_modifications_detected": false
      },
      {
        "file_path": "mothership/connection.json",
        "action": "migrate",
        "type": "breaking_change",
        "migration_script": "scripts/migrations/v1.2.0_connection_schema.py",
        "custom_modifications_detected": true,
        "preservation_strategy": "Merge mothership updates with project customizations"
      }
    ],
    "migration_scripts": [
      {
        "version": "1.2.0",
        "script_path": "scripts/migrations/v1.2.0_connection_schema.py",
        "description": "Add reporting configuration to connection.json",
        "estimated_runtime": "< 1 second"
      }
    ],
    "backup_plan": {
      "backup_directory": "mothership/backups/pre-migration-1.2.0-20251016",
      "files_to_backup": [
        "agents/_common.guardrails.md",
        "mothership/connection.json"
      ]
    },
    "risk_assessment": {
      "level": "low",
      "breaking_changes": 1,
      "custom_modifications": 1,
      "rollback_available": true
    },
    "approval_checklist": [
      "Review diff_summary for each file change",
      "Verify migration scripts are safe to execute",
      "Confirm custom modifications will be preserved",
      "Check backup plan is adequate",
      "Approve breaking changes if acceptable"
    ]
  }
}
```

## Mode: Apply

Execute migration plan and apply updates to project.

### Output Schema
```json
{
  "artifact_type": "migration_applied",
  "status": "complete",
  "validation": "passed",
  "approval_required": false,
  "next_phase": "development",
  "data": {
    "project_name": "string",
    "from_version": "1.0.0",
    "to_version": "1.2.0",
    "applied_at": "2025-10-16T19:15:00Z",
    "changes_applied": [
      {
        "file_path": "agents/_common.guardrails.md",
        "action": "updated",
        "status": "success",
        "backup_path": "mothership/backups/pre-migration-1.2.0-20251016/_common.guardrails.md"
      },
      {
        "file_path": "mothership/connection.json",
        "action": "migrated",
        "status": "success",
        "migration_script": "scripts/migrations/v1.2.0_connection_schema.py",
        "backup_path": "mothership/backups/pre-migration-1.2.0-20251016/connection.json"
      }
    ],
    "migration_results": [
      {
        "version": "1.2.0",
        "script": "scripts/migrations/v1.2.0_connection_schema.py",
        "status": "success",
        "output": "Added reporting configuration. Custom fields preserved."
      }
    ],
    "validation_results": {
      "structure_valid": true,
      "pydantic_valid": true,
      "custom_modifications_preserved": true,
      "critical_rules_maintained": true
    },
    "sync_status": {
      "last_sync": "2025-10-16T19:15:00Z",
      "current_version": "1.2.0",
      "sync_successful": true
    },
    "rollback_instructions": [
      "Backup available at: mothership/backups/pre-migration-1.2.0-20251016/",
      "To rollback: cp mothership/backups/pre-migration-1.2.0-20251016/* ./",
      "Then update connection.json version to 1.0.0"
    ],
    "post_migration_actions": [
      "Review updated files for any needed adjustments",
      "Run tests to ensure project still works correctly",
      "Commit changes to version control",
      "Update team on new mothership features available"
    ]
  }
}
```

## Update Categories

### Non-Breaking Updates
- Template improvements (bug fixes, better patterns)
- Documentation updates
- New optional features in agents
- Security patches that don't change behavior
- Performance optimizations

**Action**: Auto-apply with backup

### Breaking Updates
- Pydantic model schema changes
- Required field additions to connection.json
- Agent specification structural changes
- .cursorrules format changes
- File path relocations

**Action**: Require migration script + approval

### Security Updates
- Critical vulnerability fixes
- Dependency version bumps for security
- Authentication/authorization improvements

**Action**: Flag for immediate attention, may auto-apply

## Preservation Rules

### Always Preserve
- Project-specific ADR decisions (docs/adr/project.json)
- Custom business logic in functions
- Project-specific environment variables
- German field names and multi-tenancy patterns
- Formula preservation rules
- Custom agent modifications specific to project domain

### Always Update
- Mothership ADR decisions (docs/adr/mothership.json)
- Common guardrails (agents/_common.guardrails.md)
- Template bug fixes
- Security patches
- Pydantic model updates

### Merge Strategy
- .cursorrules: Merge new critical rules, preserve project customizations
- Agent specifications: Update framework, preserve project examples
- connection.json: Update schema, preserve project metadata

## Error Handling

### Template Conflict
```json
{
  "error": {
    "code": "TEMPLATE_CONFLICT",
    "message": "Custom modifications detected in template file",
    "details": [
      "File: agents/Feature.agent.md has custom modifications",
      "Lines 45-67 differ from mothership template",
      "Manual merge required"
    ],
    "artifact": "migration",
    "remediation": "Review custom modifications and choose merge strategy: 'keep-custom', 'use-template', or 'manual-merge'"
  }
}
```

### Version Mismatch
```json
{
  "error": {
    "code": "VERSION_MISMATCH",
    "message": "Project version ahead of mothership",
    "details": [
      "Project version: 1.5.0",
      "Mothership version: 1.2.0",
      "Project may have been forked or manually modified"
    ],
    "artifact": "migration",
    "remediation": "Reset project to mothership version or contribute changes back to mothership"
  }
}
```

### Migration Script Failure
```json
{
  "error": {
    "code": "MIGRATION_FAILED",
    "message": "Migration script execution failed",
    "details": [
      "Script: scripts/migrations/v1.2.0_connection_schema.py",
      "Error: KeyError: 'mothership_version'",
      "Backup available at: mothership/backups/pre-migration-1.2.0-20251016/"
    ],
    "artifact": "migration",
    "remediation": "Restore from backup, review migration script, contact mothership maintainer"
  }
}
```

## Example Usage

### Check for Updates
```
Use @agents/Migration.agent.md
project_path: /Users/hermannrohr/Documents/generated-projects/richtungswechsel-roi-tracker---saas-migration/
mode: "check"
```

### Preview Migration
```
Use @agents/Migration.agent.md
project_path: /Users/hermannrohr/Documents/generated-projects/richtungswechsel-roi-tracker---saas-migration/
mode: "preview"
```

### Apply Updates
```
Use @agents/Migration.agent.md
project_path: /Users/hermannrohr/Documents/generated-projects/richtungswechsel-roi-tracker---saas-migration/
mode: "apply"
```

## Human Approval Gate
After successful preview generation, this agent requires approval from:
- **Cynthia** (Project Manager) - Approves impact on project timeline and resources
- **Usama** (Lead Developer) - Reviews technical changes and breaking updates

Apply mode requires pre-approval of preview. Check mode does not require approval.

## Related ADRs
- **ADR-0002**: Two-Stage Scaffolding Architecture (extends with update management)
- **ADR-0003**: Agent Inheritance and Project Lifecycle Management (completes lifecycle)
- **ADR-0011**: Agent System Template Implementation (manages template updates)
- **ADR-0012**: Migration Agent and Project Update Protocol (this agent's specification)

## Success Metrics
- Projects can sync with mothership updates in < 5 minutes
- Zero data loss from custom modifications during migration
- 100% rollback success rate for failed migrations
- Breaking changes handled gracefully with migration scripts
- All updates preserve critical project rules (German fields, multi-tenancy, formulas)
