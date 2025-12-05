# Common Agent Guardrails

**Project:** Richtungswechsel ROI Tracker - SaaS Migration

These rules apply to ALL agents in this project.

## Output Format

### Pure JSON Output Only
- **JSON ONLY**: Never output prose, explanations, or markdown around JSON
- **No code fences**: Do not wrap JSON in ```json``` blocks
- **Pure JSON**: Output must be valid JSON that can be parsed directly
- **No commentary**: Save explanations for commit messages, not agent output

### Exceptions
- Error messages may include context
- Human approval gates may output status messages
- Debugging mode (if explicitly requested) may include explanations

## Stable ID Management

### ID Formats
All IDs must follow these patterns:
- **Features**: `FR-###` (e.g., FR-001, FR-002)
- **Stories**: `ST-###` (e.g., ST-001, ST-002)
- **Tasks**: `TASK-###` (e.g., TASK-001, TASK-002)
- **ADRs**: `ADR-####` (e.g., ADR-0001, ADR-0002)
- **Entities**: `ENT-###` (e.g., ENT-001, ENT-002)
- **Flows**: `FLOW-###` (user flows), `SFLOW-###` (system flows)
- **Bugs**: `BUG-###` (e.g., BUG-001, BUG-002)

### ID Stability Rules
1. **Never reuse IDs**: Once assigned, an ID is permanent
2. **Sequential allocation**: IDs increment sequentially (no gaps allowed)
3. **Cross-artifact references**: Use exact IDs when linking artifacts
4. **Deletion handling**: Mark as deprecated, don't delete or reuse

## Context Loading (CRITICAL)

### Load Before Acting
**ALWAYS** read relevant context files before generating output:

#### For Feature Development:
```bash
docs/prd.json           # Product requirements
docs/adr/project.json   # Project-specific decisions
docs/adr/mothership.json # Inherited pipeline decisions (read-only)
docs/erd.json           # Database schema
docs/tasks.json         # Existing tasks
```

#### For Bug Fixes:
```bash
docs/prd.json           # Feature context
docs/erd.json           # Data model
docs/tasks.json         # Related tasks
.github/ISSUES.md       # Known issues
```

#### For Architecture Decisions:
```bash
docs/prd.json           # Requirements driving decision
docs/adr/project.json   # Existing project decisions
docs/adr/mothership.json # Inherited framework decisions
docs/erd.json           # Current data architecture
```

### Why Context Loading Matters
- Prevents duplicate work
- Maintains consistency with existing decisions
- Ensures ID stability
- Avoids conflicting with existing features/tasks

## Human Approval Gates

### When to Stop
Agents MUST stop and wait for human approval after:
- Generating ADR (requires Hermann + Usama approval)
- Creating scaffolding plan (requires Cynthia + Usama approval)
- Major refactoring proposals
- Breaking changes to APIs or database schema
- Deployment to production

### Approval Format
When stopping for approval, output:
```json
{
  "status": "awaiting_approval",
  "approval_required": true,
  "approvers": ["Name1", "Name2"],
  "reason": "Clear explanation of what needs approval",
  "next_steps": "What happens after approval"
}
```

## Pydantic Validation

### Always Validate
ALL generated artifacts MUST:
1. Validate against Pydantic models in `app/models.py` (from mothership)
2. Pass JSON schema validation
3. Include all required fields
4. Use correct data types

### Validation Command
```bash
python3 -c "from app.models import <ModelName>; import json; <ModelName>(**json.load(open('path/to/artifact.json')))"
```

If validation fails, fix the output before proceeding.

## Project-Specific Rules

### German Language Architecture
- **Database fields**: ALWAYS use German names (e.g., `aktuelleJaehrlicheEinnahmen`)
- **Code variables**: Use English for readability
- **UI labels**: German text throughout
- **Comments**: English code comments, German field explanations

### German Field Examples
```typescript
// ✅ CORRECT: German field name with English variable
const currentRevenue = roiInput.aktuelleJaehrlicheEinnahmen;

// ❌ WRONG: English field name
const currentRevenue = roiInput.currentAnnualRevenue;
```

### Multi-Tenancy Requirements
- **organizationId**: MUST be included in ALL data entities
- **Security rules**: Firestore rules must enforce organization isolation
- **Queries**: Always filter by organizationId
- **Admin access**: Validate admin role before cross-organization queries

### Formula Preservation
- **ROI calculations**: Never modify MVP formulas without explicit approval
- **Testing**: Always test calculations against spreadsheet reference
- **Migration**: Port formulas line-by-line, don't refactor
- **Documentation**: Comment formulas with business logic explanations

## Error Handling

### Error Output Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": ["Detail 1", "Detail 2"],
    "artifact": "artifact_type",
    "remediation": "How to fix this error"
  }
}
```

### Common Error Codes
- `VALIDATION_FAILED`: Pydantic validation error
- `ID_CONFLICT`: Duplicate or invalid ID
- `CONTEXT_MISSING`: Required file not found
- `APPROVAL_REQUIRED`: Human approval gate triggered
- `GERMAN_FIELD_VIOLATION`: English field name used instead of German

## File Operations

### Read Before Write
- **ALWAYS** read existing files before editing
- **NEVER** overwrite without reading current state
- **PRESERVE** existing content when adding new sections

### Atomic Operations
- Complete file operations atomically
- Don't leave files in half-written state
- Validate JSON after writing

### Backup Strategy
- Critical files should be backed up before major changes
- Use git for version control
- Tag releases for rollback capability

## Testing Requirements

### Before Committing
ALL code changes require:
1. **Unit tests**: Test individual functions
2. **Integration tests**: Test component interactions
3. **Validation**: Test against Pydantic models
4. **Manual verification**: Run development server and test UI

### Test Coverage
- Minimum 80% coverage for business logic
- 100% coverage for calculation functions (ROI, projections)
- Integration tests for all API endpoints
- E2E tests for critical user flows

## Communication Protocol

### With Users
- Be concise and direct
- Provide file paths with line numbers (e.g., `lib/firebase/config.ts:42`)
- Use bullet points for lists
- Avoid emojis unless user uses them first

### With Other Agents
- Output pure JSON (no prose)
- Include all required metadata
- Follow schema exactly
- Validate before output

## Reference Documentation

- **Mothership ADRs**: `docs/adr/mothership.json` (READ-ONLY)
- **Project ADRs**: `docs/adr/project.json` (MUTABLE)
- **ADR Pattern**: See `docs/adr/README.md` for Approach B explanation
- **Pydantic Models**: `app/models.py` in mothership repository
- **Pipeline Docs**: See mothership `README.md` for full pipeline documentation

## Version

- **Guardrails Version**: 1.0.0
- **Project**: Richtungswechsel ROI Tracker - SaaS Migration
- **Last Updated**: 2025-10-16
- **Inherited From**: End-to-End Agentic Development Pipeline (Mothership)
