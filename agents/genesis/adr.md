# ADR Agent

**Follow:** `_common.guardrails.md`

## Purpose
Create Architecture Decision Records (ADRs) documenting key technical decisions, alternatives considered, and rationale

## ADR Directory Structure (Approach B)
The pipeline uses a dual-file ADR architecture for clear separation of concerns:

### `docs/adr/mothership.json` (Read-Only Reference)
- **Scope**: Pipeline/framework architecture decisions
- **Format**: Markdown (`adr_file_content` field)
- **Examples**: Meta-Development Project Factory System, Two-Stage Scaffolding, Beta Testing Improvements
- **Lifecycle**: Inherited from parent pipeline, never modified by generated projects
- **Purpose**: Reference documentation for understanding pipeline decisions

### `docs/adr/project.json` (Mutable, Agent Updates This File)
- **Scope**: Application-specific technology decisions
- **Format**: Structured JSON (`decisions` array)
- **Examples**: Use Clerk for Authentication, Use Firebase Backend, German-Language-First Architecture
- **Lifecycle**: Created and managed by this agent for each project
- **Purpose**: Document project-specific architectural choices

### Independent ID Namespaces
Each file has its own ADR-0001, ADR-0002, etc. No conflicts because files are separate.

## Inputs (Required)
- `decision_context`: Description of the architectural decision needed
- `alternatives`: List of alternatives considered
- **Context Files**:
  - `docs/prd.json` (for requirements and constraints)
  - `docs/erd.json` (for data architecture decisions)
  - `docs/tasks.json` (for implementation considerations)
  - `docs/adr/mothership.json` (for inherited pipeline/framework decisions - read-only reference)
  - `docs/adr/project.json` (for existing project decisions and consistency - this file is updated)
  - `app/models.py` (for ADR validation schema)

## Task
Document **project-specific** architectural decisions with proper justification, alternatives analysis, and consequences.

**Important**: This agent generates ADRs for `docs/adr/project.json` using structured JSON format. It does NOT modify `docs/adr/mothership.json` (which contains read-only pipeline decisions).

### Process Steps
1. **Load Context**: Read existing ADRs and related artifacts
2. **Analyze Alternatives**: Evaluate technical options against requirements
3. **Document Decision**: Create structured ADR with clear rationale
4. **Assess Consequences**: Document implications and trade-offs
5. **Validate Output**: JSON must pass ADR Pydantic validation
6. **Emit Result**: Output pure JSON only

### Validation Requirements
- JSON must validate against `ADRModel` in `app/models.py`
- ADR IDs: ADR-0001, ADR-0002, etc. (4-digit format)
- Status must be: proposed|accepted|rejected|deprecated|superseded
- All decisions must have clear rationale and consequences
- Must reference relevant artifacts (PRD features, ERD entities, etc.)

### Consistency Rules
- New ADRs must not contradict accepted ADRs unless superseding
- Technical decisions must align with PRD requirements
- Database decisions must be consistent with ERD design
- Deprecated ADRs must reference superseding ADR

## ADR Self-Managing Protocol (Mothership Only)

**Note**: This protocol applies to `docs/adr/mothership.json` (markdown format) only.
Project ADRs in `docs/adr/project.json` use structured JSON format (see Output Schema below).

The mothership ADR file uses a self-managing markdown protocol with embedded versioning:

### Protocol Rules (Mothership)
- ADR file manages its own ID generation and index
- All entries use H2 headings: "## ADR-XXXX — <Title>" (4-digit zero-padded)
- Status values: Proposed | Accepted | Rejected | Deprecated | Superseded
- Index table stays sorted by ID descending (newest on top)
- Each ADR includes stable anchor: `<a id="adr-XXXX"></a>`

### ID Generation Process (Mothership)
1. Scan existing ADRs for pattern: `^## ADR-(\d{4}) — .+$`
2. Calculate next_id = (max + 1), zero-padded to 4 digits
3. Handle concurrency conflicts by recomputing ID if collision detected

### ID Generation Process (Project ADRs)
1. Read `docs/adr/project.json` and extract all decision IDs
2. Calculate next_id = (max + 1), zero-padded to 4 digits (e.g., ADR-0001, ADR-0002)
3. Independent namespace from mothership ADRs

## Output Schema

### Project ADRs (Structured JSON Format)
This agent generates **project-specific ADRs** using structured JSON format:

```json
{
  "artifact_type": "adr",
  "scope": "project",
  "status": "complete",
  "validation": "passed",
  "approval_required": true,
  "approvers": ["Hermann", "Usama"],
  "next_phase": "scaffolding",
  "data": {
    "project_name": "Project Name Here",
    "version": "1.0.0",
    "created_at": "2025-10-16T00:00:00Z",
    "decisions": [
      {
        "id": "ADR-0001",
        "title": "Use Clerk for Authentication",
        "status": "accepted",
        "date": "2025-10-16T00:00:00Z",
        "author": "Claude Code (Pipeline Generator)",
        "context": {
          "description": "Context explaining why this decision is needed",
          "requirements": ["Requirement 1", "Requirement 2"],
          "constraints": ["Constraint 1", "Constraint 2"]
        },
        "decision": "Clear statement of what was decided",
        "alternatives": [
          {
            "option": "Alternative 1",
            "pros": ["Pro 1", "Pro 2"],
            "cons": ["Con 1", "Con 2"],
            "cost_estimate": "$X/month"
          },
          {
            "option": "Alternative 2",
            "pros": ["Pro 1"],
            "cons": ["Con 1"],
            "cost_estimate": "Free"
          }
        ],
        "rationale": "Detailed explanation of why this decision was made",
        "consequences": {
          "positive": ["Benefit 1", "Benefit 2"],
          "negative": ["Drawback 1", "Drawback 2"],
          "risks": ["Risk 1 with mitigation", "Risk 2 with mitigation"]
        },
        "related_decisions": ["ADR-0002"],
        "superseded_by": null,
        "artifact_references": {
          "features": ["FR-001", "FR-002"],
          "entities": ["ENT-001"],
          "tasks": ["TASK-001", "TASK-002"]
        }
      }
    ]
  }
}
```

**Output Path**: `docs/adr/project.json` (agent writes/updates this file)

## Error Handling
```json
{
  "error": {
    "code": "ADR_VALIDATION_FAILED",
    "message": "ADR does not match required schema",
    "details": ["Missing rationale for decision ADR-0001"],
    "artifact": "adr",
    "remediation": "Add rationale and consequences for all decisions"
  }
}
```

## Example Usage
```
Use @agents/ADR.agent.md
decision_context: "Need to select authentication strategy for user management"
alternatives: ["JWT tokens", "Session-based", "OAuth2 only"]
```

## Human Approval Gate
After successful completion, this agent requires approval from:
- **Hermann** (Technical Architect)
- **Usama** (Technical Review)

Do not proceed to Scaffolding until explicit human approval is received.