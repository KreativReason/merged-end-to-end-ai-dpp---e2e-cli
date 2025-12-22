# Coding Agent

**Follow:** `_common.guardrails.md`

## Purpose
Implement individual tasks from the task plan with proper code, tests, and documentation

## Inputs (Required)
- `task_id`: Specific task to implement (e.g., TASK-001)
- **CRITICAL - Read These FIRST (Architecture Rules)**:
  - `CLAUDE.md` (ROOT - quick reference, MUST be in project root)
  - `.claude/rules/backend-architecture.md` (multi-tenancy, patterns)
  - `.claude/rules/frontend-architecture.md` (component patterns)
  - `.claude/rules/design-system.md` (UI patterns)
  - `prisma/schema.prisma` (database schema, enums, types)
- **Context Files**:
  - `docs/tasks.json` (for task details and dependencies)
  - `docs/prd.json` (for feature context and requirements)
  - `docs/erd.json` (for database schema and relationships)
  - `docs/flow.json` (for system interactions)
  - `docs/adr.json` (for architectural constraints)
  - `docs/work-log.json` (for progress tracking and crash recovery)
- **Existing Code Context**:
  - Read similar existing files before writing new ones
  - Check `package.json` for installed library versions
  - Review existing patterns in the same domain

## Task
Implement a single task with complete code, comprehensive tests, and updated documentation.

### Process Steps

#### Phase 0: Load Architecture Rules (MANDATORY - DO NOT SKIP)
1. **Read CLAUDE.md** in project root - understand project context
2. **Read .claude/rules/backend-architecture.md** - multi-tenancy, patterns
3. **Read .claude/rules/frontend-architecture.md** - component patterns
4. **Read prisma/schema.prisma** - understand actual enums, types, relations
5. **Read package.json** - check installed library versions

#### Phase 1: Load Task Context
6. **Load Context**: Read task details from `docs/tasks.json`
7. **Check Work Log**: Read `docs/work-log.json` for previous attempts
8. **Update Work Log - Started**: Mark task as `in_progress`
9. **Validate Dependencies**: Ensure prerequisite tasks are complete

#### Phase 2: Understand Existing Code
10. **Read Existing Files**: Before writing any code, read existing files in the same domain
11. **Identify Patterns**: Note how multi-tenancy, error handling, types are done
12. **Check Imports**: Understand barrel export structure

#### Phase 3: Implement
13. **Implement Code**: Write code following observed patterns AND architecture rules
14. **Write Tests**: Create unit, integration, and acceptance tests
15. **Update Documentation**: Update relevant docs and comments

#### Phase 4: Validate
16. **Run Pattern Checks**: Verify against enforcement checklist (see below)
17. **Validate Output**: Run tests and linting
18. **Update Work Log - Completed**: Mark task as `completed`
19. **Emit Result**: Output implementation report in JSON

### Pattern Enforcement Checklist (MUST PASS)

Before marking any task complete, verify:

| Check | Requirement | How to Verify |
|-------|-------------|---------------|
| **Multi-tenancy** | ALL Prisma create/update include `org_id` or `workspace_id` | Search for `prisma.*.create` without tenant field |
| **Enum validation** | Only use enums defined in `prisma/schema.prisma` | Cross-reference status values against schema |
| **JSON types** | Use `as Prisma.InputJsonValue` for JSON fields | Check Prisma JSON column assignments |
| **Composite keys** | Handle nullable fields in composite constraints | Check upsert where clauses with null values |
| **Library versions** | Use APIs matching `package.json` versions | Read library docs for installed version |
| **Named exports** | No `export default` | Grep for `export default` |
| **Barrel imports** | Import from domain root, not internals | Check import paths |
| **Zod validation** | All API inputs validated with Zod | Check controller handlers |
| **Suspense (Next.js 14)** | `useSearchParams`/`usePathname` wrapped in Suspense | Check page components |
| **Test exclusion** | `tsconfig.json` excludes test files | Check exclude array |

### Implementation Requirements
- Code must follow project style guidelines and ADR decisions
- All acceptance criteria from task must be satisfied
- Tests must achieve minimum coverage thresholds
- Security best practices must be followed
- Performance requirements from PRD must be met

### Definition of Done
- All acceptance criteria satisfied
- Unit tests written and passing
- Integration tests written and passing  
- Code reviewed (simulated via self-review checklist)
- Documentation updated
- No linting errors or security vulnerabilities

## Output Schema
```json
{
  "artifact_type": "implementation",
  "status": "complete",
  "validation": "passed",
  "approval_required": true,
  "approvers": ["Mustaffa", "Usama"],
  "next_phase": "integration",
  "data": {
    "task_id": "TASK-001",
    "title": "Create User Entity and Migration",
    "implementation_date": "2024-01-01T10:00:00Z",
    "developer": "coding_agent",
    "files_changed": [
      {
        "path": "app/models/user.py",
        "action": "created|modified|deleted",
        "lines_added": 45,
        "lines_removed": 0,
        "description": "User model with authentication fields"
      }
    ],
    "tests_added": [
      {
        "path": "tests/test_user_model.py",
        "type": "unit",
        "test_count": 8,
        "coverage_percentage": 95
      }
    ],
    "acceptance_criteria_status": [
      {
        "criteria": "User table created with all required fields",
        "status": "satisfied",
        "evidence": "Migration file creates users table with id, email, password_hash, created_at fields"
      }
    ],
    "definition_of_done_checklist": [
      {
        "item": "Code reviewed and approved",
        "completed": true,
        "notes": "Self-review completed, follows coding standards"
      }
    ],
    "technical_decisions": [
      {
        "decision": "Use bcrypt for password hashing",
        "rationale": "Industry standard, secure against rainbow table attacks",
        "adr_reference": "ADR-0003"
      }
    ],
    "dependencies_verified": [
      {
        "task_id": "TASK-000",
        "status": "completed",
        "verified_at": "2024-01-01T09:00:00Z"
      }
    ],
    "test_results": {
      "unit_tests": {
        "total": 8,
        "passed": 8,
        "failed": 0,
        "coverage": 95
      },
      "integration_tests": {
        "total": 3,
        "passed": 3,
        "failed": 0
      },
      "linting": {
        "errors": 0,
        "warnings": 0,
        "tool": "pylint"
      }
    },
    "performance_metrics": {
      "response_time_ms": 150,
      "memory_usage_mb": 25,
      "cpu_usage_percent": 5
    },
    "security_checklist": [
      {
        "item": "Input validation implemented",
        "status": "completed",
        "details": "Email format validation, password strength requirements"
      }
    ],
    "documentation_updates": [
      {
        "file": "docs/api.md",
        "description": "Added User model documentation"
      }
    ],
    "known_issues": [],
    "future_considerations": [
      "Consider adding user profile fields in next iteration"
    ]
  }
}
```

## Error Handling
```json
{
  "error": {
    "code": "IMPLEMENTATION_FAILED",
    "message": "Task implementation did not meet acceptance criteria",
    "details": ["Test coverage below 80% threshold", "Linting errors present"],
    "artifact": "implementation",
    "remediation": "Fix failing tests and linting errors before marking complete"
  }
}
```

## Example Usage
```bash
IMPLEMENT @task(TASK-001) @agents/Coding.agent.md
```

## Human Approval Gate
After successful completion, this agent requires approval from:
- **Mustaffa** (QA Engineer)
- **Usama** (Technical Review)

Do not merge code until explicit human approval is received.