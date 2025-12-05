# Common Agent Guardrails

**ALL agents must follow these rules without exception.**

## Output Format
- **JSON ONLY**: Never output prose, explanations, or markdown around JSON
- **No code fences**: Do not wrap JSON in ```json``` blocks
- **Pure JSON**: Output must be valid JSON that can be parsed directly
- **No commentary**: Never add explanatory text before or after JSON

## Validation Requirements
- **Read models.py first**: Always check Pydantic models before generating JSON
- **Validate before emit**: JSON must pass Pydantic validation
- **Fail fast**: Stop immediately if validation fails
- **Report validation errors**: Output validation errors in JSON format if they occur

## Context Awareness
- **Load existing artifacts**: Read all relevant docs/*.json files before acting
- **Check consistency**: Ensure new output is consistent with existing artifacts
- **Reference stable IDs**: Use existing FR-###, ST-###, TASK-###, ADR-#### IDs
- **Maintain relationships**: Preserve cross-references between artifacts

## Stable ID Management
- **Never regenerate**: Existing IDs are immutable
- **Increment only**: Add new items with next available ID
- **Format consistency**: 
  - Features: FR-001, FR-002, etc.
  - Stories: ST-001, ST-002, etc.
  - Tasks: TASK-001, TASK-002, etc.
  - ADRs: ADR-0001, ADR-0002, etc.
  - SOW items: SOW-001, SOW-002, etc.

## Human Approval Gates
- **Stop for approval**: Never auto-advance to next pipeline phase
- **Declare completion**: End output with status indicating approval needed
- **List approvers**: Specify who needs to approve (per Chat_GPT_Setup_Instructions.mdc)
- **Wait for explicit go-ahead**: Do not assume approval

## Error Handling
- **JSON format for errors**: Even errors must be in JSON format
- **Include error codes**: Use consistent error classification
- **Provide context**: Include enough detail for debugging
- **Suggest remediation**: When possible, suggest how to fix the issue

## Agent Coordination
- **Read agent specs**: Follow the specific agent.md file for your role
- **Use template pattern**: Follow agents/_template.agent.md structure
- **Declare dependencies**: State what artifacts you need to read
- **Signal completion**: Indicate when your phase is complete

## Example Error Output
```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "PRD JSON does not match Pydantic model",
    "details": ["Missing required field: project_name", "Invalid format: owner_email"],
    "artifact": "prd",
    "remediation": "Fix validation errors and regenerate"
  }
}
```

## Example Success Output
```json
{
  "artifact_type": "prd",
  "status": "complete",
  "validation": "passed",
  "approval_required": true,
  "approvers": ["Cynthia", "Hermann", "Usama"],
  "next_phase": "flow_design",
  "data": {
    // ... actual artifact content
  }
}
```