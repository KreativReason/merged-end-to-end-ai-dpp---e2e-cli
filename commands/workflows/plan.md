# Plan Command

> Transform feature descriptions into comprehensive implementation plans

## Usage

```
/kreativreason:plan "<feature description>"
```

## Description

The Plan command transforms feature requests, bug reports, or improvement ideas into well-structured implementation plans. It researches the codebase, analyzes patterns, and produces actionable specifications.

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `description` | Yes | Feature description or improvement idea |
| `detail_level` | No | minimal, standard, comprehensive (default: standard) |

## Workflow

### Phase 1: Research & Context (Parallel)

Launch three research agents simultaneously:

```
┌─────────────────────────────────────────────────┐
│                  Research Phase                  │
├─────────────────┬──────────────┬────────────────┤
│ repo-analyst    │ best-        │ framework-     │
│                 │ practices    │ docs           │
│ • File patterns │ • Solutions  │ • API usage    │
│ • Conventions   │ • Approaches │ • Examples     │
│ • Related code  │ • Trade-offs │ • Caveats      │
└─────────────────┴──────────────┴────────────────┘
```

### Phase 2: Issue Planning

1. Draft searchable title (feat:, fix:, docs: prefix)
2. Analyze stakeholders affected
3. Plan content with appropriate detail
4. Gather supporting materials

### Phase 3: Acceptance Criteria

1. Run spec-flow analysis with research findings
2. Review results for gaps and edge cases
3. Define testable acceptance criteria
4. Include success metrics

### Phase 4: Implementation Details

Based on `detail_level`:

**minimal**: Quick issue with problem statement and basic criteria
**standard**: Background, technical considerations, success metrics
**comprehensive**: Phased implementation, risk analysis, resource planning

### Phase 5: Output & Options

Generate plan file and present options:

```
Plan generated: plans/feat-user-authentication.md

Options:
1. Start /kreativreason:work to implement
2. Run /kreativreason:review for plan feedback
3. Create issue in project tracker (GitHub/Linear)
4. Simplify or rework the plan
```

## Output Schema

```json
{
  "artifact_type": "implementation_plan",
  "status": "complete",
  "data": {
    "title": "feat: Add user authentication",
    "description": "Implement secure user authentication using Clerk",
    "created_at": "ISO-8601",
    "detail_level": "standard",
    "research_summary": {
      "existing_patterns": ["Repository pattern for data access"],
      "related_files": ["src/lib/auth.ts", "src/middleware.ts"],
      "framework_guidance": ["Use Clerk middleware for route protection"]
    },
    "specification": {
      "problem_statement": "Users cannot create accounts or log in",
      "proposed_solution": "Integrate Clerk for authentication",
      "stakeholders": ["End users", "Admin users", "DevOps"],
      "acceptance_criteria": [
        "Users can sign up with email/password",
        "Users can log in and maintain session",
        "Protected routes redirect unauthenticated users",
        "Admin routes require admin role"
      ]
    },
    "technical_plan": {
      "approach": "Use Clerk React SDK with Next.js middleware",
      "components": [
        {
          "name": "Auth middleware",
          "file": "src/middleware.ts",
          "action": "create"
        },
        {
          "name": "Sign-in page",
          "file": "src/app/sign-in/page.tsx",
          "action": "create"
        }
      ],
      "dependencies_to_add": ["@clerk/nextjs"],
      "environment_variables": [
        "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY",
        "CLERK_SECRET_KEY"
      ]
    },
    "tasks": [
      {
        "id": "PLAN-TASK-001",
        "title": "Install and configure Clerk",
        "type": "setup",
        "story_points": 2
      },
      {
        "id": "PLAN-TASK-002",
        "title": "Create auth middleware",
        "type": "backend",
        "story_points": 3,
        "dependencies": ["PLAN-TASK-001"]
      }
    ],
    "risks": [
      {
        "risk": "Clerk rate limits in development",
        "mitigation": "Use development keys with higher limits"
      }
    ],
    "success_metrics": [
      "Sign-up conversion rate > 80%",
      "Login success rate > 99%",
      "Page load time with auth < 200ms"
    ],
    "adr_required": false,
    "estimated_effort": "5 story points"
  }
}
```

## Plan File Location

Plans are saved to:
```
plans/<slug>.md

Example: plans/feat-user-authentication.md
```

## Integration with Other Commands

```
/kreativreason:plan "Add user auth"
  ↓ Creates plans/feat-user-auth.md

/kreativreason:work plans/feat-user-auth.md
  ↓ Executes the plan

/kreativreason:review PR#123
  ↓ Reviews the implementation
```

## Example

```
/kreativreason:plan "Add dark mode toggle to settings page"

> 🔍 Researching codebase...
>   ✓ Found existing theme context in src/context/theme.tsx
>   ✓ Settings page at src/app/settings/page.tsx
>   ✓ Using Tailwind CSS for styling
>
> 📋 Generating plan...
>   ✓ Plan created: plans/feat-dark-mode-toggle.md
>
> Summary:
>   - Extend existing ThemeContext
>   - Add toggle component to settings
>   - Persist preference to localStorage
>   - Estimated: 3 story points
>
> Options:
>   1. /kreativreason:work plans/feat-dark-mode-toggle.md
>   2. Review the plan: cat plans/feat-dark-mode-toggle.md
>   3. Create GitHub issue
```

## Constraints

- Never generates code during planning (research only)
- Maximum 125 characters for document quotes
- Uses quotation marks for exact language from sources
