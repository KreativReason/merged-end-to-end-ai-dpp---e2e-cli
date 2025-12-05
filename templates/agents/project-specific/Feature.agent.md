# Feature Agent

**Follow:** `_common.guardrails.md`

## Purpose
Add new features to the Richtungswechsel ROI Tracker application by creating user stories, tasks, and implementation plans.

## Inputs (Required)
- `feature_description`: Clear description of the feature to add
- `user_persona`: Target user (financial advisor, coaching company admin)
- **Context Files**:
  - `docs/prd.json` (to ensure no duplicate features)
  - `docs/erd.json` (to understand data model)
  - `docs/tasks.json` (to identify next task ID)
  - `docs/adr/project.json` (to align with architectural decisions)

## Task
Analyze feature request and generate complete feature specification including user stories, acceptance criteria, technical tasks, and implementation plan.

### Process Steps
1. **Load Context**: Read existing features, ERD, tasks, and ADRs
2. **Analyze Feature**: Understand scope, dependencies, and impact
3. **Generate User Stories**: Create detailed user stories with acceptance criteria
4. **Create Tasks**: Break down into implementable tasks with estimates
5. **Identify Data Changes**: Determine if ERD updates are needed
6. **Check ADR Impact**: Identify if new architectural decisions are required
7. **Validate Output**: JSON must follow FeatureSpecificationModel schema
8. **Emit Result**: Output pure JSON only

### Validation Requirements
- No duplicate feature IDs (check existing PRD)
- User stories follow format: "As a [persona], I want [goal] so that [benefit]"
- Acceptance criteria are testable
- Tasks have clear definition of done
- Story points estimate included (1-8 scale)
- Dependencies on existing features identified

## German Language Requirements

### UI Components
- All labels, buttons, form fields in German
- Error messages in German
- Help text and tooltips in German

### Database Fields
- Use German field names in Firestore (e.g., `aktivitaeten`, `monatlicheEinnahmen`)
- Document German→English mappings in comments
- Follow existing naming conventions from ERD

### Code Comments
- Code variables in English
- Comments explaining German terms
- JSDoc with German field descriptions

## Output Schema

```json
{
  "artifact_type": "feature_specification",
  "status": "complete",
  "validation": "passed",
  "approval_required": true,
  "approvers": ["Hermann", "Usama"],
  "next_phase": "implementation",
  "data": {
    "feature": {
      "id": "FR-011",
      "title": "Feature Title",
      "description": "Detailed feature description",
      "priority": "high|medium|low",
      "user_persona": "financial_advisor|admin",
      "user_stories": [
        {
          "id": "ST-031",
          "title": "Story Title",
          "description": "As a [persona], I want [goal] so that [benefit]",
          "acceptance_criteria": [
            "Testable criterion 1",
            "Testable criterion 2"
          ],
          "priority": "high",
          "story_points": 5
        }
      ]
    },
    "tasks": [
      {
        "id": "TASK-016",
        "title": "Task Title",
        "description": "Detailed task description",
        "type": "frontend|backend|database|testing",
        "story_ids": ["ST-031"],
        "estimated_hours": 8,
        "story_points": 5,
        "dependencies": ["TASK-001"],
        "acceptance_criteria": [
          "Criterion 1",
          "Criterion 2"
        ],
        "definition_of_done": [
          "Code implemented",
          "Tests passing",
          "Deployed to staging"
        ],
        "context_plan": {
          "beginning_context": ["File1.ts", "File2.tsx"],
          "end_state_files": ["NewFile.ts"],
          "read_only_files": ["ReferenceFile.ts"]
        },
        "testing_strategy": {
          "strategy_type": "integration",
          "test_files": ["NewFile.test.ts"],
          "success_criteria": ["All tests pass", "80%+ coverage"]
        }
      }
    ],
    "erd_changes": {
      "required": false,
      "changes": []
    },
    "adr_required": false,
    "architectural_concerns": [],
    "implementation_notes": [
      "Note 1",
      "Note 2"
    ],
    "estimated_completion": "2 weeks"
  }
}
```

## Integration with Existing System

### Update PRD
After approval, add feature to `docs/prd.json`:
```bash
# Read existing PRD
# Append new feature to features array
# Validate with PRDModel
# Write updated PRD
```

### Update Tasks
Add tasks to `docs/tasks.json`:
```bash
# Read existing tasks
# Append new tasks to tasks array
# Update sprint allocations
# Validate with TasksModel
# Write updated tasks
```

### Trigger ERD Update (if needed)
If `erd_changes.required = true`:
```bash
# Create ERD update proposal
# Get approval from Hassan + Usama
# Update docs/erd.json
```

### Trigger ADR (if needed)
If `adr_required = true`:
```bash
# Create ADR proposal
# Get approval from Hermann + Usama
# Update docs/adr/project.json
```

## Example Usage

```
Use @agents/Feature.agent.md
feature_description: "Add CSV import functionality for bulk data entry"
user_persona: "financial_advisor"
```

## Multi-Tenancy Validation

For all features, verify:
- [ ] organizationId included in all data entities
- [ ] Firestore security rules enforce organization isolation
- [ ] UI filters data by current user's organization
- [ ] Admin features check role before execution

## Firebase Integration

For features requiring Firebase changes:
- [ ] Cloud Functions defined for server-side logic
- [ ] Firestore security rules updated
- [ ] Storage rules updated (if file uploads involved)
- [ ] Indexes defined for new queries

## Clerk Integration

For features requiring authentication changes:
- [ ] Webhook handling for user sync
- [ ] Role validation (admin vs user)
- [ ] Organization membership validation
- [ ] Public metadata updates (if storing role info)

## Chart.js Integration

For features with visualizations:
- [ ] German labels on all charts
- [ ] Responsive design (mobile + desktop)
- [ ] Chart data formatted correctly
- [ ] Colors match brand (#003f5c, #ffb600)
- [ ] Accessibility (alt text, ARIA labels)

## Error Handling

```json
{
  "error": {
    "code": "FEATURE_CONFLICT",
    "message": "Feature already exists or conflicts with existing feature",
    "details": ["Existing feature FR-003 has similar functionality"],
    "artifact": "feature_specification",
    "remediation": "Review existing features and modify request to avoid duplication"
  }
}
```

## Human Approval Gate

After successful completion, this agent requires approval from:
- **Hermann** (Product Owner)
- **Usama** (Lead Developer)

Do not proceed to implementation until explicit human approval is received.

## Notes

- Features should align with coaching ROI tracking domain
- Consider impact on existing RW projections and IST tracking
- Validate against German spreadsheet reference if applicable
- Preserve MVP formula integrity for calculation features
- Test with sample German data before finalizing
