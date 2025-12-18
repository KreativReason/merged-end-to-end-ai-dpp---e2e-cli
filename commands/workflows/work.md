# Work Command

> Execute implementation plans with continuous testing, quality checks, and **persistent progress tracking**

## Usage

```
/kreativreason:work <plan_path>
```

## Description

The Work command executes implementation plans systematically, using git worktrees for isolation, continuous testing after each change, and automatic PR creation upon completion.

**Crash Recovery**: All progress is persisted to `docs/work-log.json`. If a session crashes, you can resume from the last checkpoint.

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `plan_path` | Yes | Path to plan file (e.g., plans/feat-user-auth.md) |
| `worktree` | No | Use git worktree for isolation (default: true) |
| `resume` | No | Resume from crashed/paused session (default: auto-detect) |

## Workflow

### Phase 0: Session Initialization (Crash Recovery)

```
1. Check for existing work-log.json in docs/
2. If found, check for crashed/active sessions:
   - If crashed session exists → offer to resume
   - If active session exists → warn and ask to continue or start fresh
3. Create new WorkSession entry:
   - session_id: WS-{timestamp}
   - started_at: now
   - status: "active"
   - plan_file: <plan_path>
4. Write updated work-log.json immediately
5. Load task_status to know which tasks are already completed
```

### Phase 1: Quick Start

```
1. Read and clarify the work document completely
2. Set up environment:
   - Create git worktree (if enabled)
   - Create feature branch
   - Verify dependencies
3. Create actionable task list using TodoWrite
   - Skip tasks already marked "completed" in work-log.json
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

## Task Execution Loop (with Persistence)

```
while tasks_remaining:
    task = get_next_task()

    # === CHECKPOINT: Task Started ===
    update_work_log({
        task_id: task.id,
        status: "in_progress",
        started_at: now,
        attempt_count: +1
    })
    TodoWrite(task.id, status="in_progress")

    # Implementation
    read_context(task.context_plan.beginning_context)
    implement(task)

    # Continuous testing
    run_tests(task.testing_strategy.test_command)
    if tests_fail:
        # === CHECKPOINT: Task Failed ===
        update_work_log({
            task_id: task.id,
            status: "failed",
            last_error: error_message
        })
        fix_and_retry()

    # Progress
    commit_sha = commit(task)

    # === CHECKPOINT: Task Completed ===
    update_work_log({
        task_id: task.id,
        status: "completed",
        completed_at: now,
        commits: [commit_sha],
        files_modified: changed_files
    })
    update_changelog(task, commit_sha)
    TodoWrite(task.id, status="completed")
```

### Checkpoint Frequency

Progress is saved to `docs/work-log.json` at these points:
- Session start
- Each task start (in_progress)
- Each task completion
- Each task failure
- Each commit
- Session end (completed/paused/crashed)

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

## Crash Recovery

If a session crashes (API error, context overflow, etc.), the next `/kreativreason:work` will:

1. Detect the crashed session in `docs/work-log.json`
2. Show what was completed vs. in-progress
3. Offer to resume from the last checkpoint

```
> 🔄 Detected crashed session WS-1703123456
>
> Completed tasks: TASK-001, TASK-002, TASK-003
> In progress: TASK-004 (started 15 min ago)
> Remaining: TASK-005, TASK-006
>
> Resume from TASK-004? [Y/n]
```

### Manual Recovery

If auto-detection fails, check `docs/work-log.json`:
```bash
cat docs/work-log.json | jq '.data.task_status'
```

## Session Finalization

At the end of a successful session:
```
1. Mark session status = "completed"
2. Update session.ended_at
3. Calculate summary stats
4. Append to CHANGELOG.md
5. Write final work-log.json
```

## Core Principles

1. **Start fast, execute faster**: Get clarification upfront, don't pause mid-work
2. **Match existing patterns**: Study codebase, don't reinvent
3. **Test continuously**: Run tests after each change
4. **Ship complete**: Don't leave features half-done
5. **Persist progress**: Save checkpoints so crashes don't lose work
