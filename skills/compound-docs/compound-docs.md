# Compound Docs Skill

## Purpose

Automatically generate and maintain documentation that compounds knowledge over time, capturing patterns, decisions, and learnings.

## Philosophy

> Documentation should grow smarter with every feature, not just bigger.

## Capabilities

### Pattern Documentation

Automatically capture reusable patterns:

```markdown
## Pattern: API Error Handling

### Context
How we handle errors in API routes.

### Implementation
```typescript
export function apiHandler(handler: Handler) {
  return async (req: Request) => {
    try {
      return await handler(req);
    } catch (error) {
      if (error instanceof ValidationError) {
        return Response.json({ error: error.message }, { status: 400 });
      }
      console.error(error);
      return Response.json({ error: 'Internal error' }, { status: 500 });
    }
  };
}
```

### Usage
```typescript
export const POST = apiHandler(async (req) => {
  const data = await req.json();
  // handler logic
});
```

### First Used
PR #45 - User Authentication

### Also Used In
- PR #67 - Payment Processing
- PR #89 - Report Generation
```

### Decision Recording

Link patterns to ADRs:

```markdown
## Decision: Use Zod for Validation

### Why
- TypeScript inference
- Runtime validation
- Consistent with API layer

### Alternative Considered
- Yup (less TS support)
- Manual validation (error-prone)

### References
- ADR-0005: Validation Strategy
- Pattern: Form Validation
```

### Knowledge Indexing

Maintain searchable index:

```json
{
  "patterns": {
    "api-error-handling": {
      "file": "docs/patterns/api-error-handling.md",
      "tags": ["api", "errors", "typescript"],
      "usage_count": 15
    }
  },
  "decisions": {
    "validation-strategy": {
      "file": "docs/adr/ADR-0005.md",
      "status": "accepted",
      "related_patterns": ["form-validation", "api-validation"]
    }
  }
}
```

## Auto-Documentation Triggers

| Event | Documentation Generated |
|-------|------------------------|
| New pattern detected | Pattern doc created |
| Pattern reused | Usage count updated |
| ADR created | Index updated |
| Code review feedback | Learning captured |

## Commands

### Capture Pattern
```bash
/kreativreason:compound capture-pattern "API Error Handling"
```

### Find Similar
```bash
/kreativreason:compound find-similar "error handling"
```

### Generate Onboarding
```bash
/kreativreason:compound generate-onboarding
```

## Output Schema

```json
{
  "artifact_type": "compound_doc",
  "action": "pattern_captured|decision_linked|knowledge_indexed",
  "data": {
    "pattern": {
      "name": "API Error Handling",
      "category": "backend",
      "first_seen": "PR #45",
      "usage_count": 1,
      "file_created": "docs/patterns/api-error-handling.md"
    },
    "index_updated": true,
    "related_docs": [
      "docs/adr/ADR-0005.md",
      "docs/patterns/form-validation.md"
    ]
  }
}
```

## Integration

- Runs during `/kreativreason:work` to capture new patterns
- Runs during `/kreativreason:review` to link decisions
- Generates onboarding docs from accumulated knowledge
