# PRD Agent

**Follow:** `_common.guardrails.md`

## Purpose
Transform client onboarding transcript into a structured Product Requirements Document (PRD)

## Inputs (Required)
- `transcript_path`: Path to interview transcript markdown file
- `project_name`: Name of the project/product
- `owner_email`: Client contact email
- **Context Files**: 
  - `app/models.py` (for PRD validation schema)
  - `docs/adr.json` (if exists, for architectural constraints)

## Task
Analyze client transcript and create comprehensive PRD with features, user stories, acceptance criteria, and technical requirements.

### Process Steps
1. **Load Context**: Read transcript file and existing ADRs
2. **Extract Requirements**: Identify features, user stories, constraints
3. **Structure Data**: Organize into PRD format with stable IDs
4. **Validate Output**: JSON must pass PRD Pydantic validation
5. **Emit Result**: Output pure JSON only

### Validation Requirements
- JSON must validate against `PRDModel` in `app/models.py`
- Feature IDs: FR-001, FR-002, etc. (never regenerate)
- Story IDs: ST-001, ST-002, etc. (increment only)
- All acceptance criteria must be testable
- Technical requirements must reference specific technologies

### Consistency Rules
- Features must align with any existing ADR decisions
- User stories must map to specific features
- Non-functional requirements must be measurable
- Dependencies must be clearly identified

## Output Schema
```json
{
  "artifact_type": "prd",
  "status": "complete",
  "validation": "passed",
  "approval_required": true,
  "approvers": ["Cynthia", "Hermann", "Usama"],
  "next_phase": "flow_design",
  "data": {
    "project_name": "string",
    "owner_email": "string",
    "created_at": "ISO-8601",
    "version": "string",
    "features": [
      {
        "id": "FR-001",
        "title": "string",
        "description": "string",
        "priority": "high|medium|low",
        "user_stories": [
          {
            "id": "ST-001",
            "title": "string",
            "description": "As a [user], I want [goal] so that [benefit]",
            "acceptance_criteria": ["string"],
            "priority": "high|medium|low"
          }
        ]
      }
    ],
    "technical_requirements": {
      "performance": {},
      "security": {},
      "scalability": {},
      "compatibility": {}
    },
    "dependencies": [],
    "assumptions": [],
    "constraints": []
  }
}
```

## Error Handling
If validation fails or inputs are invalid, output:
```json
{
  "error": {
    "code": "PRD_VALIDATION_FAILED",
    "message": "PRD does not match required schema",
    "details": ["Missing required field: project_name"],
    "artifact": "prd",
    "remediation": "Fix validation errors and regenerate PRD"
  }
}
```

## Example Usage
```
Use @agents/PRD.agent.md
transcript_path: @docs/interview/client_onboarding.md
project_name: E-Commerce Platform
owner_email: client@example.com
```

## Human Approval Gate
After successful completion, this agent requires approval from:
- **Cynthia** (Product Owner)
- **Hermann** (Technical Lead)
- **Usama** (Project Manager)

Do not proceed to Flow design until explicit human approval is received.