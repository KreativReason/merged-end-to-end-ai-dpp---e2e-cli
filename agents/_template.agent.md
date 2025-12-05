# [AGENT_NAME] Agent

**Follow:** `_common.guardrails.md`

## Purpose
[Brief description of what this agent creates/transforms]

## Inputs (Required)
- `input_param_1`: [description and format]
- `input_param_2`: [description and format]
- **Context Files**: [list required files to read first]
  - `docs/[artifact].json` (if dependency)
  - `app/models.py` (for validation schema)

## Task
[Detailed description of the transformation/creation task]

### Process Steps
1. **Load Context**: Read all specified input files and dependencies
2. **Validate Input**: Ensure all required parameters are provided
3. **Transform/Create**: [specific transformation logic]
4. **Validate Output**: JSON must pass Pydantic validation
5. **Emit Result**: Output pure JSON only

### Validation Requirements
- JSON must validate against `[ModelName]` in `app/models.py`
- All stable IDs must be preserved if updating existing artifact
- New items get incremented IDs: [ID-FORMAT]
- Cross-references to other artifacts must be valid

### Consistency Rules
- [Specific rules about how this artifact relates to others]
- [What fields must be consistent with other artifacts]
- [What relationships must be maintained]

## Output Schema
```json
{
  "artifact_type": "[artifact_name]",
  "status": "complete",
  "validation": "passed|failed",
  "approval_required": true|false,
  "approvers": ["List", "Of", "Required", "Approvers"],
  "next_phase": "[next_pipeline_phase]",
  "data": {
    // Actual artifact content matching Pydantic model
  }
}
```

## Error Handling
If validation fails or inputs are invalid, output:
```json
{
  "error": {
    "code": "[ERROR_CODE]",
    "message": "[Human readable error]", 
    "details": ["List", "of", "specific", "issues"],
    "artifact": "[artifact_name]",
    "remediation": "[How to fix the issue]"
  }
}
```

## Example Usage
```
Use @agents/[AGENT_NAME].agent.md
input_param_1: [value]
input_param_2: [value]
```

## Human Approval Gate
After successful completion, this agent requires approval from:
- [List specific approvers as per Chat_GPT_Setup_Instructions.mdc]

Do not proceed to next phase until explicit human approval is received.