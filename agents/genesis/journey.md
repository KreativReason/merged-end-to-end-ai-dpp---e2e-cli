# Journey Agent

**Follow:** `_common.guardrails.md`

## Purpose
Transform PRD, Flow, and ERD into detailed user journey maps with touchpoints, emotions, and optimization opportunities

## Inputs (Required)
- `prd_path`: Path to validated PRD JSON file
- `flow_path`: Path to validated Flow JSON file
- `erd_path`: Path to validated ERD JSON file
- **Context Files**:
  - `docs/prd.json` (for user stories and features)
  - `docs/flow.json` (for user flows and interactions)
  - `docs/erd.json` (for data touchpoints)
  - `app/models.py` (for Journey validation schema)

## Task
Create comprehensive user journey maps that combine user flows with emotional context, pain points, and optimization opportunities.

### Process Steps
1. **Load Context**: Read PRD, Flow, ERD, and validation schema
2. **Map User Personas**: Extract user types and their contexts
3. **Create Journey Maps**: Transform flows into journeys with emotions
4. **Identify Touchpoints**: Map system interactions and data points
5. **Validate Output**: JSON must pass Journey Pydantic validation
6. **Emit Result**: Output pure JSON only

### Validation Requirements
- JSON must validate against `JourneyModel` in `app/models.py`
- Journey IDs: JRN-001, JRN-002, etc.
- Touchpoint IDs: TP-001, TP-002, etc.
- All journeys must reference valid flows and user stories
- Emotional states must be from predefined list

### Consistency Rules
- Journeys must cover all user stories from PRD
- Touchpoints must align with flow steps and ERD entities
- Pain points must have corresponding optimization opportunities
- Journey phases must follow logical user progression

## Output Schema
```json
{
  "artifact_type": "journey",
  "status": "complete",
  "validation": "passed",
  "approval_required": true,
  "approvers": ["Cynthia", "Hassan"],
  "next_phase": "task_planning",
  "data": {
    "project_name": "string",
    "version": "string",
    "created_at": "ISO-8601",
    "personas": [
      {
        "id": "PERSONA-001",
        "name": "Primary User",
        "description": "string",
        "goals": ["string"],
        "pain_points": ["string"],
        "context": "string"
      }
    ],
    "journeys": [
      {
        "id": "JRN-001",
        "name": "User Onboarding Journey",
        "description": "string",
        "persona_id": "PERSONA-001",
        "flow_ids": ["FLOW-001"],
        "story_ids": ["ST-001"],
        "phases": [
          {
            "id": "PHASE-001",
            "name": "Discovery",
            "description": "string",
            "duration_estimate": "5 minutes",
            "touchpoints": [
              {
                "id": "TP-001",
                "name": "Landing Page",
                "type": "web|mobile|email|support",
                "description": "string",
                "flow_step_id": "STEP-001",
                "data_entities": ["ENT-001"],
                "user_actions": ["view", "click"],
                "system_actions": ["display", "track"],
                "emotional_state": "curious|frustrated|confident|confused|satisfied",
                "pain_points": ["string"],
                "opportunities": ["string"]
              }
            ]
          }
        ],
        "success_metrics": [
          {
            "metric": "conversion_rate",
            "target": "85%",
            "measurement": "phase completion rate"
          }
        ]
      }
    ],
    "optimization_opportunities": [
      {
        "id": "OPP-001",
        "title": "Streamline Registration",
        "description": "string",
        "impact": "high|medium|low",
        "effort": "high|medium|low",
        "touchpoint_ids": ["TP-001"],
        "expected_improvement": "string"
      }
    ]
  }
}
```

## Error Handling
```json
{
  "error": {
    "code": "JOURNEY_VALIDATION_FAILED",
    "message": "Journey does not match required schema",
    "details": ["Invalid flow_id reference: FLOW-999"],
    "artifact": "journey",
    "remediation": "Fix flow references and regenerate journey maps"
  }
}
```

## Example Usage
```
Use @agents/Journey.agent.md
prd_path: @docs/prd.json
flow_path: @docs/flow.json
erd_path: @docs/erd.json
```

## Human Approval Gate
After successful completion, this agent requires approval from:
- **Cynthia** (Product Owner)
- **Hassan** (UX Designer)

Do not proceed to Task planning until explicit human approval is received.