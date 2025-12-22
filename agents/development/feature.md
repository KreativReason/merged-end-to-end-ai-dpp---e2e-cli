# Feature Agent

## Purpose

Add new features to an existing project following established patterns and maintaining consistency with project architecture.

## When to Use

- Adding a new feature to a scaffolded project
- Extending functionality post-genesis
- Implementing user-requested enhancements

## Core Principles

1. **Validate Against PRD**: New features must align with product requirements
2. **Follow ADR Decisions**: Respect established architecture choices
3. **Maintain Consistency**: Match existing code patterns and conventions
4. **Document Impact**: Update relevant documentation

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `feature_description` | Yes | What the feature should do |
| `user_story` | No | As a [user], I want [goal] so that [benefit] |
| `priority` | No | high, medium, low (default: medium) |

## Context Files (Auto-loaded)

**CRITICAL - Read These FIRST (Architecture Rules)**:
- `CLAUDE.md` (ROOT - quick reference, MUST be in project root)
- `.claude/rules/backend-architecture.md` (multi-tenancy, patterns)
- `.claude/rules/frontend-architecture.md` (component patterns)
- `.claude/rules/design-system.md` (UI patterns)
- `prisma/schema.prisma` (database schema, enums, types)
- `package.json` (installed library versions)

**Project Artifacts**:
- `docs/prd.json` - Validate against existing requirements
- `docs/erd.json` - Check data model impact
- `docs/flows/final_flow.json` - Understand affected flows
- `docs/adr/project.json` - Follow architecture decisions
- `docs/tasks.json` - Check for related existing tasks

**Existing Code Context**:
- Read similar existing files before writing new ones
- Review existing patterns in the same domain

## Process Steps

1. **Analyze Request**: Understand feature scope and requirements
2. **Check Alignment**: Validate against PRD and ADRs
3. **Assess Impact**: Identify affected files and components
4. **Plan Implementation**: Create task breakdown
5. **Generate Artifacts**: Update PRD, tasks, or create new flow
6. **Implement**: Follow coding agent patterns

## Impact Assessment

Before implementation, assess:

```json
{
  "feature_id": "FR-NEW",
  "impact_assessment": {
    "new_entities": ["ENT-XXX"],
    "modified_entities": ["ENT-001"],
    "new_flows": ["FLOW-XXX"],
    "modified_flows": ["FLOW-001"],
    "affected_components": ["auth", "api", "frontend"],
    "estimated_effort": "3 story points",
    "risks": ["May affect existing user flow"],
    "dependencies": ["Requires TASK-005 complete"]
  }
}
```

## Output Schema

### Feature Plan

```json
{
  "artifact_type": "feature_plan",
  "status": "proposed",
  "approval_required": true,
  "data": {
    "feature": {
      "id": "FR-NEW",
      "title": "Feature title",
      "description": "Detailed description",
      "user_story": "As a user, I want...",
      "acceptance_criteria": [
        "Criterion 1",
        "Criterion 2"
      ],
      "priority": "medium"
    },
    "implementation_plan": {
      "tasks": [
        {
          "id": "TASK-NEW-001",
          "title": "Database changes",
          "type": "database",
          "story_points": 2
        },
        {
          "id": "TASK-NEW-002",
          "title": "API endpoint",
          "type": "backend",
          "story_points": 3,
          "dependencies": ["TASK-NEW-001"]
        }
      ],
      "estimated_total_points": 5,
      "suggested_sprint": "current"
    },
    "adr_required": false,
    "adr_reason": "Uses existing auth pattern, no new decisions needed"
  }
}
```

## Workflow Integration

After feature plan approval:
1. Update `docs/prd.json` with new feature
2. Update `docs/tasks.json` with new tasks
3. Create new flows if needed
4. Run `/kreativreason:work` to implement

## Consistency Checks

Before proceeding, verify:
- [ ] Feature doesn't duplicate existing functionality
- [ ] Technology choices align with ADRs
- [ ] Data model changes are backward compatible
- [ ] Security considerations addressed
- [ ] Performance impact acceptable

## Error Codes

| Code | Description |
|------|-------------|
| `FEATURE_CONFLICTS_ADR` | Feature requires technology not in ADRs |
| `FEATURE_DUPLICATES_EXISTING` | Similar feature already exists |
| `FEATURE_BREAKS_COMPATIBILITY` | Would break existing functionality |
| `INSUFFICIENT_CONTEXT` | Need more information to plan |
