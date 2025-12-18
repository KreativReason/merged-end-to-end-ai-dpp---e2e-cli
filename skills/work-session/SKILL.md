# Work Session Skill

## Purpose

Manage work session persistence for crash recovery and progress tracking. This skill provides utilities for updating `docs/work-log.json` and `CHANGELOG.md` in child projects.

## Overview

When executing tasks via `/kreativreason:work`, this skill tracks progress to enable:
- **Crash Recovery**: Resume from last checkpoint after API errors or context overflow
- **Progress Visibility**: Know which tasks are completed vs. pending
- **Change History**: Maintain a human-readable changelog

## Files Managed

| File | Purpose |
|------|---------|
| `docs/work-log.json` | Machine-readable progress tracking |
| `CHANGELOG.md` | Human-readable change history |

## Skill Functions

### `init_session(plan_file, branch_name?)`

Initialize a new work session. Call at the start of `/kreativreason:work`.

**Input:**
```json
{
  "plan_file": "plans/feat-user-auth.md",
  "branch_name": "feature/user-auth"
}
```

**Output:**
```json
{
  "session_id": "WS-1703123456",
  "started_at": "2024-12-21T10:00:00Z",
  "status": "active",
  "previous_sessions": 2,
  "tasks_already_completed": ["TASK-001", "TASK-002"]
}
```

**Side Effects:**
- Creates new session entry in `docs/work-log.json`
- Sets `current_task_id` to null
- Updates `updated_at` timestamp

### `check_crashed_session()`

Check if there's a crashed or active session that needs attention.

**Output (No issues):**
```json
{
  "has_crashed_session": false,
  "has_active_session": false
}
```

**Output (Crashed session found):**
```json
{
  "has_crashed_session": true,
  "crashed_session": {
    "session_id": "WS-1703123456",
    "started_at": "2024-12-21T08:00:00Z",
    "last_checkpoint": "2024-12-21T08:45:00Z",
    "current_task_id": "TASK-004",
    "tasks_completed": ["TASK-001", "TASK-002", "TASK-003"],
    "tasks_in_progress": ["TASK-004"]
  },
  "recommendation": "Resume from TASK-004"
}
```

### `start_task(task_id)`

Mark a task as in-progress. Call before starting implementation.

**Input:**
```json
{
  "task_id": "TASK-003"
}
```

**Output:**
```json
{
  "task_id": "TASK-003",
  "status": "in_progress",
  "started_at": "2024-12-21T10:15:00Z",
  "attempt_count": 1
}
```

**Side Effects:**
- Updates task in `task_status` map
- Sets `current_task_id` in active session
- Updates `last_checkpoint`
- Writes to `docs/work-log.json`

### `complete_task(task_id, files_modified, commit_sha?)`

Mark a task as completed. Call after successful implementation.

**Input:**
```json
{
  "task_id": "TASK-003",
  "files_modified": [
    "src/auth/middleware.ts",
    "src/auth/types.ts"
  ],
  "commit_sha": "abc1234"
}
```

**Output:**
```json
{
  "task_id": "TASK-003",
  "status": "completed",
  "completed_at": "2024-12-21T10:45:00Z",
  "duration": "30 minutes",
  "files_modified": 2
}
```

**Side Effects:**
- Updates task in `task_status` map
- Increments `tasks_completed` counter
- Adds commit to task's commit list
- Updates `last_checkpoint`
- Writes to `docs/work-log.json`

### `fail_task(task_id, error_message)`

Mark a task as failed. Call when implementation encounters unrecoverable error.

**Input:**
```json
{
  "task_id": "TASK-003",
  "error_message": "Test failures: 3 assertions failed in auth.test.ts"
}
```

**Output:**
```json
{
  "task_id": "TASK-003",
  "status": "failed",
  "failed_at": "2024-12-21T10:45:00Z",
  "attempt_count": 2,
  "last_error": "Test failures: 3 assertions failed in auth.test.ts"
}
```

**Side Effects:**
- Updates task status to "failed"
- Stores error message
- Increments attempt count
- Writes to `docs/work-log.json`

### `end_session(status, summary?)`

Finalize a work session. Call at the end of `/kreativreason:work`.

**Input:**
```json
{
  "status": "completed",
  "summary": "Implemented user authentication with JWT tokens"
}
```

**Output:**
```json
{
  "session_id": "WS-1703123456",
  "status": "completed",
  "ended_at": "2024-12-21T12:00:00Z",
  "duration": "2 hours",
  "tasks_completed": 5,
  "tasks_failed": 0,
  "total_commits": 5,
  "total_files_changed": 12
}
```

**Side Effects:**
- Updates session status
- Sets `ended_at`
- Calculates summary stats
- Appends to `CHANGELOG.md`
- Writes final `docs/work-log.json`

### `get_task_status(task_id?)`

Get the status of a specific task or all tasks.

**Input (specific task):**
```json
{
  "task_id": "TASK-003"
}
```

**Output:**
```json
{
  "task_id": "TASK-003",
  "status": "completed",
  "started_at": "2024-12-21T10:15:00Z",
  "completed_at": "2024-12-21T10:45:00Z",
  "attempt_count": 1,
  "files_modified": ["src/auth/middleware.ts"],
  "commits": ["abc1234"]
}
```

**Input (all tasks):**
```json
{}
```

**Output:**
```json
{
  "tasks": {
    "TASK-001": { "status": "completed" },
    "TASK-002": { "status": "completed" },
    "TASK-003": { "status": "in_progress" },
    "TASK-004": { "status": "pending" }
  },
  "summary": {
    "completed": 2,
    "in_progress": 1,
    "pending": 1,
    "failed": 0
  }
}
```

### `update_changelog(version, changes, tasks_completed)`

Append an entry to CHANGELOG.md.

**Input:**
```json
{
  "version": "0.2.0",
  "changes": [
    "Added user authentication with JWT",
    "Created protected routes middleware",
    "Added sign-in and sign-up pages"
  ],
  "tasks_completed": ["TASK-001", "TASK-002", "TASK-003"]
}
```

**Side Effects:**
- Appends new entry under `## [version]` section
- Groups changes by type (Added, Changed, Fixed, etc.)
- Links to relevant task IDs

## Work Log Schema

The `docs/work-log.json` file follows this schema (from `app/models.py`):

```json
{
  "artifact_type": "work_log",
  "status": "active",
  "validation": "passed",
  "data": {
    "project_name": "my-project",
    "created_at": "ISO-8601",
    "updated_at": "ISO-8601",
    "sessions": [
      {
        "session_id": "WS-{timestamp}",
        "started_at": "ISO-8601",
        "ended_at": "ISO-8601 or null",
        "status": "active|completed|crashed|paused",
        "plan_file": "plans/feat-auth.md",
        "branch_name": "feature/auth",
        "current_task_id": "TASK-003 or null",
        "tasks_attempted": [...],
        "tasks_completed": 3,
        "tasks_failed": 0,
        "total_commits": 3,
        "last_checkpoint": "ISO-8601"
      }
    ],
    "task_status": {
      "TASK-001": {
        "task_id": "TASK-001",
        "status": "completed",
        "started_at": "ISO-8601",
        "completed_at": "ISO-8601",
        "attempt_count": 1,
        "files_modified": ["..."],
        "commits": ["abc123"]
      }
    },
    "total_sessions": 3,
    "total_tasks_completed": 15,
    "total_commits": 20
  }
}
```

## Integration with Work Command

The `/kreativreason:work` command uses this skill:

```
Phase 0: Session Initialization
├── check_crashed_session()
├── [If crashed] Prompt user to resume
└── init_session(plan_file, branch)

Phase 2: Execute
├── For each task:
│   ├── start_task(task_id)
│   ├── [implement]
│   ├── [test]
│   └── complete_task(task_id, files, commit) OR fail_task(task_id, error)

Phase 4: Ship It
└── end_session("completed", summary)
```

## Error Recovery

### Session Left Active (Unclean Exit)

If Claude Code crashes mid-session:
1. Session remains with `status: "active"`
2. `current_task_id` indicates which task was in progress
3. Next run detects this and offers to resume

### Detecting Crash vs. Pause

| Indicator | Crash | Intentional Pause |
|-----------|-------|-------------------|
| `status` | "active" | "paused" |
| `ended_at` | null | null |
| `current_task_id` | set | null |
| Time since `last_checkpoint` | > 5 min | recent |

## Example Usage

```python
# At start of work session
session = init_session("plans/feat-auth.md", "feature/auth")
print(f"Starting session {session['session_id']}")
print(f"Already completed: {session['tasks_already_completed']}")

# For each task
start_task("TASK-003")
# ... implementation ...
complete_task("TASK-003", ["src/auth.ts"], "abc123")

# At end
end_session("completed", "Implemented authentication")
```
