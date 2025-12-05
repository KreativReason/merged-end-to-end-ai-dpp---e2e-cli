# ADR Directory Structure

This directory implements **Approach B: Directory-Based ADR Separation** for managing Architecture Decision Records in the End-to-End Agentic Development Pipeline.

## Overview

The pipeline uses a dual-file ADR architecture to separate mothership (pipeline/framework) decisions from project-specific (application) decisions.

## File Structure

```
docs/adr/
├── README.md           ← This file (pattern documentation)
├── mothership.json     ← Pipeline/framework ADRs (read-only, inherited)
└── project.json        ← Application-specific ADRs (mutable)
```

## File Descriptions

### `mothership.json` - Pipeline Framework Decisions

**Scope**: Pipeline architecture, agent design, workflow patterns

**Format**: Markdown with embedded protocol (`adr_file_content` field)

**Lifecycle**:
- Created by the mothership pipeline development team
- Inherited by all generated projects as read-only reference
- Never modified by generated projects

**Example ADRs**:
- ADR-0001: Meta-Development Project Factory System
- ADR-0002: Two-Stage Scaffolding Architecture
- ADR-0003: Agent Inheritance and Project Lifecycle Management
- ADR-0004: Beta Testing Improvements and Production Readiness
- ADR-0010: ADR Separation Architecture (Mothership vs Project)

**Purpose**: Provides generated projects with context about the pipeline's architectural decisions, helping development teams understand inherited patterns and constraints.

### `project.json` - Application-Specific Decisions

**Scope**: Technology stack, authentication, database, application architecture

**Format**: Structured JSON with `decisions` array (see Pydantic `Decision` model)

**Lifecycle**:
- Created by ADR agent during project planning phase
- Updated by development team as project evolves
- Mutable - can be extended with new decisions

**Example ADRs** (Richtungswechsel ROI Tracker):
- ADR-0001: Use Clerk for Authentication and User Management
- ADR-0002: Use Firebase (Firestore, Functions, Storage) as Backend Platform
- ADR-0003: Adopt German-Language-First Architecture
- ADR-0004: Multi-Tenancy via Organization-Advisor Hierarchical Model
- ADR-0005: Formula Preservation via Direct Migration

**Purpose**: Documents project-specific technology choices and rationale for future developers and stakeholders.

## Independent ID Namespaces

Each file maintains its own ADR ID sequence:
- `mothership.json` has ADR-0001, ADR-0002, ADR-0003, etc.
- `project.json` has ADR-0001, ADR-0002, ADR-0003, etc.

**No conflicts** because the files are separate and have different scopes.

## Design Principles

### 1. Separation of Concerns
- **Mothership**: Framework/pipeline decisions (what the factory does)
- **Project**: Application/technology decisions (what the product does)

### 2. Clear Boundaries
- File name explicitly indicates scope (no metadata parsing needed)
- Follows industry pattern: `node_modules/` (inherited) vs `src/` (custom)

### 3. Read-Only Inheritance
- Mothership ADRs are reference documentation only
- Generated projects receive copy but never modify it
- Future: File permissions can enforce read-only access

### 4. Dual Format Support
- Mothership uses markdown for comprehensive documentation
- Projects use structured JSON for validation and programmatic access

### 5. Scalability
- Pattern supports multi-layer inheritance (project → sub-project)
- Each layer has its own mothership + project ADR pair

## Scaffolder Requirements

The Scaffolder agent must implement the following when generating projects:

### Required Actions

1. **Copy Mothership ADRs**
   ```bash
   cp docs/adr/mothership.json ../generated-projects/{project-name}/docs/adr/mothership.json
   ```
   - Copy as-is (no modifications)
   - Set file permissions to read-only (future enhancement)

2. **Copy Project ADRs**
   ```bash
   cp docs/adr/project.json ../generated-projects/{project-name}/docs/adr/project.json
   ```
   - This becomes the generated project's mutable ADR file
   - Development team can add new ADRs as needed

3. **Copy Pattern Documentation**
   ```bash
   cp docs/adr/README.md ../generated-projects/{project-name}/docs/adr/README.md
   ```
   - Ensures generated project understands the pattern

4. **Update Validation Scripts**
   - Ensure Pydantic models support both formats
   - Validate both files during project generation
   - Include validation checks in generated project CI/CD

### File Permissions (Future)

```bash
# Set mothership ADRs as read-only
chmod 444 docs/adr/mothership.json

# Keep project ADRs writable
chmod 644 docs/adr/project.json
```

### Generated Project Structure

```
generated-project/
├── docs/
│   ├── adr/
│   │   ├── README.md           ← Copy from mothership
│   │   ├── mothership.json     ← Read-only reference from parent
│   │   └── project.json        ← Mutable project-specific ADRs
│   ├── prd.json
│   ├── erd.json
│   ├── flow.json
│   └── tasks.json
├── app/
│   └── models.py               ← Must support dual-format ADRs
└── ...
```

## Validation

Both files must validate against updated `ADRModel` in `app/models.py`:

```python
from app.models import ADRModel

# Validate mothership.json
with open('docs/adr/mothership.json', 'r') as f:
    mothership = ADRModel(**json.load(f))

# Validate project.json
with open('docs/adr/project.json', 'r') as f:
    project = ADRModel(**json.load(f))
```

### Pydantic Model Requirements

The `ADRModel` supports:
- **Scope field**: `"mothership" | "project"`
- **Dual format support**:
  - Markdown format: `adr_file_content`, `decisions_added`, `index_entries`
  - JSON format: `decisions` array
- **Validator**: Ensures at least one format is present

## Migration from Legacy Structure

If you have existing projects with single `docs/adr.json`:

1. Determine which ADRs are mothership vs project
2. Split into `docs/adr/mothership.json` and `docs/adr/project.json`
3. Add `scope` field to each file
4. Update file paths in agent configurations
5. Validate both files against updated models

## References

- **ADR-0010**: ADR Separation Architecture (Mothership vs Project) - Full documentation in `mothership.json`
- **ADR-0003**: Agent Inheritance and Project Lifecycle Management
- **Pydantic Models**: `app/models.py` (ADRModel, ADRData, Decision, DecisionMetadata, IndexEntry)
- **Agent Spec**: `agents/ADR.agent.md` (updated to support dual-file structure)

## Benefits

✅ **No ID Conflicts**: Independent namespaces eliminate ambiguity
✅ **Clear Inheritance**: Scaffolder knows what to copy
✅ **Better Organization**: Related ADRs grouped by scope
✅ **Future-Proof**: Scales to complex project hierarchies
✅ **Self-Documenting**: Directory structure explains architecture
✅ **Dual Format Support**: Accommodates markdown + JSON

## Questions?

Refer to ADR-0010 in `mothership.json` for complete architectural context, alternatives considered, and implementation details.
