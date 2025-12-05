# Work Command

> Execute implementation plans with continuous testing and quality checks

## Usage

```
/kreativreason:work <plan_path>
```

## Description

The Work command executes implementation plans systematically, using git worktrees for isolation, continuous testing after each change, and automatic PR creation upon completion.

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `plan_path` | Yes | Path to plan file (e.g., plans/feat-user-auth.md) |
| `worktree` | No | Use git worktree for isolation (default: true) |

## Workflow

### Phase 1: Quick Start

```
1. Read and clarify the work document completely
2. Set up environment:
   - Create git worktree (if enabled)
   - Create feature branch
   - Verify dependencies
3. Create actionable task list using TodoWrite
4. Identify dependencies and priorities
```

### Phase 2: Execute

```
For each task:
  1. Mark task as in_progress
  2. Read relevant context files
  3. Implement following existing patterns
  4. Run tests after each significant change
  5. Mark task as completed
  6. Commit with conventional format
```

### Phase 3: Quality Check

```
1. Run full test suite
2. Run linting checks
3. Optionally invoke review agents:
   - code-simplicity-reviewer
   - security-sentinel (if auth/data changes)
   - performance-oracle (if performance-critical)
4. Address any findings
```

### Phase 4: Ship It

```
1. Create commits using conventional format
2. Generate pull request:
   - Summary from plan
   - Testing notes
   - Links to related issues
3. Notify completion
4. Clean up worktree (if used)
```

## Git Worktree Isolation

When `worktree: true` (default):

```
main/                    # Your main working directory (untouched)
.worktrees/
  feat-user-auth/        # Isolated feature development
    - All changes here
    - Can run tests independently
    - Merged back to main via PR
```

Benefits:
- Main branch stays clean
- Can switch between features
- Easy rollback if implementation fails

## Task Execution Loop

```
while tasks_remaining:
    task = get_next_task()
    TodoWrite(task.id, status="in_progress")

    # Implementation
    read_context(task.context_plan.beginning_context)
    implement(task)

    # Continuous testing
    run_tests(task.testing_strategy.test_command)
    if tests_fail:
        fix_and_retry()

    # Progress
    commit(task)
    TodoWrite(task.id, status="completed")
```

## Output Schema

### Progress Updates

```json
{
  "phase": "execute",
  "task_id": "PLAN-TASK-002",
  "status": "in_progress",
  "progress": {
    "completed": 2,
    "total": 5,
    "current": "Creating auth middleware"
  }
}
```

### Completion Report

```json
{
  "artifact_type": "work_report",
  "status": "complete",
  "data": {
    "plan": "plans/feat-user-auth.md",
    "started_at": "ISO-8601",
    "completed_at": "ISO-8601",
    "duration": "45 minutes",
    "tasks_completed": 5,
    "files_changed": 8,
    "files_created": 3,
    "tests_added": 4,
    "tests_passing": true,
    "commits": [
      {
        "sha": "abc123",
        "message": "feat(auth): install and configure Clerk"
      },
      {
        "sha": "def456",
        "message": "feat(auth): add auth middleware for protected routes"
      }
    ],
    "pull_request": {
      "number": 123,
      "url": "https://github.com/org/repo/pull/123",
      "title": "feat: Add user authentication"
    },
    "quality_checks": {
      "tests": "passing",
      "lint": "passing",
      "review_findings": []
    }
  }
}
```

## Commit Convention

```
<type>(<scope>): <description>

[optional body]

Refs: PLAN-TASK-XXX
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## PR Template

```markdown
## Summary
- Implemented user authentication using Clerk
- Added protected routes middleware
- Created sign-in and sign-up pages

## Changes
- `src/middleware.ts` - Route protection
- `src/app/sign-in/page.tsx` - Sign-in page
- `src/app/sign-up/page.tsx` - Sign-up page

## Testing
- [x] Unit tests for auth utilities
- [x] Integration tests for middleware
- [x] Manual testing of sign-in flow

## Plan Reference
Implements: plans/feat-user-auth.md

---
🤖 Generated with KreativReason E2E CLI
```

## Example

```
/kreativreason:work plans/feat-dark-mode-toggle.md

> 🚀 Starting work on: feat-dark-mode-toggle
>
> Setting up...
>   ✓ Created worktree at .worktrees/feat-dark-mode-toggle
>   ✓ Created branch: feature/dark-mode-toggle
>
> Tasks:
>   [ ] Extend ThemeContext with toggle function
>   [ ] Create DarkModeToggle component
>   [ ] Add toggle to settings page
>   [ ] Persist preference to localStorage
>
> Working on: Extend ThemeContext...
>   ✓ Modified src/context/theme.tsx
>   ✓ Tests passing (12/12)
>   ✓ Committed: feat(theme): add toggle function to ThemeContext
>
> Working on: Create DarkModeToggle component...
>   ✓ Created src/components/DarkModeToggle.tsx
>   ✓ Tests passing (15/15)
>   ✓ Committed: feat(ui): create DarkModeToggle component
>
> [... continues ...]
>
> 🎉 Work complete!
>   PR created: https://github.com/org/repo/pull/45
>   Duration: 32 minutes
>   Files changed: 4
>   Tests added: 3
```

## Core Principles

1. **Start fast, execute faster**: Get clarification upfront, don't pause mid-work
2. **Match existing patterns**: Study codebase, don't reinvent
3. **Test continuously**: Run tests after each change
4. **Ship complete**: Don't leave features half-done
