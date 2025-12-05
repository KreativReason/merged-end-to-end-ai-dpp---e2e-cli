# File Todos Skill

## Purpose

Manage structured todo files for tracking code review findings, technical debt, and implementation tasks.

## Overview

This skill provides utilities for creating, updating, and organizing todo files with consistent formatting, priority management, and status tracking.

## File Format

### Todo File Structure

```markdown
---
id: PERF-001
status: open
priority: P1
category: performance
source: review/pr-123
created: 2024-01-15T10:30:00Z
updated: 2024-01-15T10:30:00Z
assignee: null
tags: [database, optimization]
---

# Short Title

## Context
How this issue was discovered.

## Problem
What's wrong and why it matters.

## Location
- File: `path/to/file.py`
- Line: 45
- Function: `function_name()`

## Current Code
```language
// problematic code
```

## Proposed Solution
```language
// fixed code
```

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## References
- Links to docs, related issues
```

### File Naming Convention

```
{id}-{status}-{priority}-{slug}.md

Examples:
  PERF-001-open-P1-n+1-query-orders.md
  SEC-002-resolved-P1-sql-injection.md
  ARCH-001-open-P2-coupling-issue.md
```

## Skill Functions

### `create_todo(finding)`

Creates a new todo file from a finding.

**Input:**
```json
{
  "id": "PERF-001",
  "priority": "P1",
  "category": "performance",
  "title": "N+1 query in orders API",
  "source": "review/pr-123",
  "file": "src/api/orders.py",
  "line": 78,
  "problem": "Each order triggers separate query",
  "solution": "Use eager loading",
  "acceptance_criteria": ["Query count < 3", "Response < 200ms"]
}
```

**Output:**
```json
{
  "status": "created",
  "path": "todos/P1/PERF-001-open-P1-n+1-query-orders.md",
  "id": "PERF-001"
}
```

### `update_todo_status(id, status)`

Updates todo status and renames file accordingly.

**Input:**
```json
{
  "id": "PERF-001",
  "status": "in_progress"
}
```

**Output:**
```json
{
  "status": "updated",
  "old_path": "todos/P1/PERF-001-open-P1-n+1-query.md",
  "new_path": "todos/P1/PERF-001-in_progress-P1-n+1-query.md"
}
```

### `resolve_todo(id, resolution_notes)`

Marks todo as resolved with resolution details.

**Input:**
```json
{
  "id": "PERF-001",
  "resolution_notes": "Fixed in commit abc123, added eager loading",
  "pr_number": 125
}
```

**Output:**
```json
{
  "status": "resolved",
  "path": "todos/resolved/PERF-001-resolved-P1-n+1-query.md",
  "resolved_at": "2024-01-16T14:30:00Z"
}
```

### `list_todos(filter)`

Lists todos with optional filtering.

**Input:**
```json
{
  "status": "open",
  "priority": "P1",
  "category": null
}
```

**Output:**
```json
{
  "todos": [
    {
      "id": "PERF-001",
      "title": "N+1 query in orders",
      "priority": "P1",
      "status": "open",
      "path": "todos/P1/PERF-001-open-P1-n+1-query.md"
    },
    {
      "id": "SEC-002",
      "title": "Input validation missing",
      "priority": "P1",
      "status": "open",
      "path": "todos/P1/SEC-002-open-P1-input-validation.md"
    }
  ],
  "total": 2
}
```

### `get_todo_summary()`

Gets overview of all todos by status and priority.

**Output:**
```json
{
  "summary": {
    "total": 15,
    "by_status": {
      "open": 10,
      "in_progress": 3,
      "resolved": 2
    },
    "by_priority": {
      "P0": 0,
      "P1": 4,
      "P2": 6,
      "P3": 5
    },
    "by_category": {
      "security": 2,
      "performance": 4,
      "architecture": 5,
      "simplicity": 4
    }
  },
  "action_required": {
    "P0_count": 0,
    "P1_open": 3,
    "stale_count": 1
  }
}
```

## Directory Structure

```
todos/
├── P0/                    # Immediate (critical)
├── P1/                    # This sprint
│   ├── PERF-001-open-P1-n+1-query.md
│   └── SEC-002-in_progress-P1-validation.md
├── P2/                    # Next sprint
│   └── ARCH-001-open-P2-coupling.md
├── P3/                    # Backlog
│   └── SIMP-001-open-P3-dead-code.md
└── resolved/              # Completed todos
    └── PERF-002-resolved-P1-caching.md
```

## Status Values

| Status | Description |
|--------|-------------|
| `open` | Not started |
| `in_progress` | Being worked on |
| `blocked` | Waiting on dependency |
| `resolved` | Completed |
| `wont_fix` | Decided not to address |

## Integration Points

### With /kreativreason:review
Review command creates todos automatically via this skill.

### With /kreativreason:triage
Triage command organizes todos by priority.

### With /kreativreason:work
Work command can pick up todos to resolve.

## Templates

### Security Finding Template
```markdown
## Impact
- Severity: {severity}
- Attack Vector: {vector}
- Affected Users: {scope}

## Remediation Steps
1. Step one
2. Step two
```

### Performance Finding Template
```markdown
## Metrics
- Current: {current_value}
- Target: {target_value}
- Improvement: {percentage}%

## Benchmarks
Before/after comparison data
```
