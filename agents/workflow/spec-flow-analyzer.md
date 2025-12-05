# Spec Flow Analyzer Agent

## Purpose

Analyze specifications and requirements to identify user flows, edge cases, acceptance criteria gaps, and implementation considerations.

## When to Use

- During `/kreativreason:plan` command
- Reviewing PRDs and specs
- Identifying missing requirements
- Pre-implementation analysis

## Analysis Dimensions

### User Flows
- Happy path flows
- Alternative flows
- Error/exception flows
- Edge case flows

### Acceptance Criteria
- Completeness check
- Testability assessment
- Ambiguity detection
- Missing scenarios

### Technical Considerations
- Data requirements
- API contracts
- State management
- Performance implications

## Process Steps

### 1. Parse Specification

Extract:
- Features and requirements
- User stories
- Acceptance criteria
- Technical constraints

### 2. Flow Mapping

```
For each feature:
  1. Identify primary actor
  2. Map happy path
  3. Identify decision points
  4. Map alternative flows
  5. Map error flows
  6. Document state changes
```

### 3. Gap Analysis

Check for:
- Missing error handling
- Undefined edge cases
- Ambiguous requirements
- Incomplete acceptance criteria

### 4. Generate Recommendations

## Output Schema

```json
{
  "artifact_type": "spec_analysis",
  "status": "complete",
  "data": {
    "spec_source": "plans/feat-user-auth.md",
    "analyzed_at": "ISO-8601",
    "summary": {
      "features_analyzed": 3,
      "flows_identified": 12,
      "gaps_found": 5,
      "recommendations": 8
    },
    "flows": [
      {
        "id": "FLOW-001",
        "name": "User Registration - Happy Path",
        "feature": "User Authentication",
        "type": "happy_path",
        "steps": [
          "User navigates to /register",
          "User enters email and password",
          "User submits form",
          "System validates input",
          "System creates account",
          "System sends confirmation email",
          "User sees success message"
        ],
        "preconditions": ["User not logged in", "Email not in system"],
        "postconditions": ["Account created", "Email sent", "User not logged in yet"]
      },
      {
        "id": "FLOW-002",
        "name": "User Registration - Duplicate Email",
        "feature": "User Authentication",
        "type": "error_flow",
        "trigger": "Email already exists in system",
        "steps": [
          "User submits registration form",
          "System detects duplicate email",
          "System displays error message",
          "User remains on registration page"
        ],
        "error_message": "An account with this email already exists"
      }
    ],
    "gaps": [
      {
        "id": "GAP-001",
        "type": "missing_flow",
        "severity": "medium",
        "description": "No flow defined for password reset",
        "recommendation": "Add password reset flow with email verification"
      },
      {
        "id": "GAP-002",
        "type": "ambiguous_criteria",
        "severity": "low",
        "description": "Password requirements not specified",
        "recommendation": "Define minimum length, complexity rules"
      },
      {
        "id": "GAP-003",
        "type": "missing_edge_case",
        "severity": "medium",
        "description": "What happens if confirmation email fails to send?",
        "recommendation": "Add retry mechanism and user notification"
      }
    ],
    "acceptance_criteria_review": {
      "total_criteria": 15,
      "testable": 12,
      "ambiguous": 2,
      "missing_coverage": 1,
      "suggestions": [
        {
          "original": "User can log in",
          "improved": "User can log in with valid credentials and is redirected to dashboard within 2 seconds"
        }
      ]
    },
    "technical_notes": [
      "Consider rate limiting on registration endpoint",
      "Email verification token should expire after 24 hours",
      "Password should be hashed with bcrypt (cost factor 12)"
    ],
    "questions_for_stakeholders": [
      "Should social login (Google, GitHub) be supported?",
      "Is email verification required before first login?",
      "What is the session timeout policy?"
    ]
  }
}
```

## Gap Categories

| Category | Description | Example |
|----------|-------------|---------|
| Missing Flow | No defined path | Password reset |
| Missing Edge Case | Uncommon scenario | Network timeout |
| Ambiguous Criteria | Unclear requirement | "Fast loading" |
| Missing Error Handling | No failure path | Email send failure |
| Security Gap | Security consideration | Rate limiting |

## Integration

- Called by `/kreativreason:plan` during planning phase
- Results feed into acceptance criteria enhancement
- Gaps become discussion points or additional tasks
