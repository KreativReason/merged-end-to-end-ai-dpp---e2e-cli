# Triage Command

> Process review findings into prioritized, actionable todos

## Usage

```
/kreativreason:triage [source]
```

## Description

The Triage command processes findings from code reviews, organizes them by priority, and creates structured todo files for systematic resolution.

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | No | Review report path or "latest" (default: latest) |
| `auto_assign` | No | Automatically assign based on file ownership (default: false) |

## When to Use

- After `/kreativreason:review` generates findings
- When processing external code review feedback
- To organize and prioritize technical debt

## Workflow

### Phase 1: Load Findings

```
1. Load review report (latest or specified)
2. Extract all findings from agent reports
3. Deduplicate overlapping issues
```

### Phase 2: Prioritize

Apply priority matrix:

| Severity | Frequency | Priority |
|----------|-----------|----------|
| Critical | Any | P0 - Immediate |
| High | Any | P1 - This sprint |
| Medium | Multiple | P1 - This sprint |
| Medium | Single | P2 - Next sprint |
| Low | Any | P3 - Backlog |

### Phase 3: Categorize

Group findings by:
- Category (security, performance, architecture, simplicity, data)
- Affected area (file/module)
- Related issues

### Phase 4: Create Todos

Generate todo files with full context:

```
todos/
├── P0/
│   └── (empty - no critical issues)
├── P1/
│   ├── PERF-001-open-n+1-query-orders.md
│   └── SEC-002-open-input-validation.md
├── P2/
│   ├── ARCH-001-open-coupling-payment.md
│   └── SIMP-001-open-factory-complexity.md
└── P3/
    └── SIMP-002-open-remove-dead-code.md
```

## Output Schema

```json
{
  "artifact_type": "triage_report",
  "status": "complete",
  "data": {
    "source": "reviews/pr-123-review.json",
    "triaged_at": "ISO-8601",
    "summary": {
      "total_findings": 15,
      "P0": 0,
      "P1": 3,
      "P2": 5,
      "P3": 7
    },
    "by_category": {
      "security": 2,
      "performance": 3,
      "architecture": 4,
      "simplicity": 4,
      "data_integrity": 2
    },
    "todos_created": [
      {
        "id": "PERF-001",
        "priority": "P1",
        "title": "N+1 query in orders API",
        "file_path": "todos/P1/PERF-001-open-n+1-query-orders.md"
      }
    ],
    "action_plan": {
      "immediate": [],
      "this_sprint": [
        "PERF-001: Fix N+1 query",
        "SEC-002: Add input validation"
      ],
      "next_sprint": [
        "ARCH-001: Reduce coupling",
        "SIMP-001: Simplify factory"
      ],
      "backlog": [
        "SIMP-002: Remove dead code"
      ]
    },
    "estimated_effort": {
      "P1_items": "5 story points",
      "P2_items": "8 story points",
      "P3_items": "3 story points"
    }
  }
}
```

## Todo File Format

```markdown
---
id: PERF-001
status: open
priority: P1
category: performance
source: review/pr-123
created: 2024-01-15T10:30:00Z
assignee: null
---

# N+1 Query in Orders API

## Context
Found during PR #123 review by performance-oracle agent.

## Problem
Each order triggers separate database query for items.
- Current: 100 orders = 101 queries
- Impact: ~2s response time for list endpoint

## Location
- File: `src/api/orders.py`
- Line: 78
- Function: `get_orders_with_items()`

## Current Code
```python
def get_orders_with_items(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    for order in orders:
        order.items = get_items(order.id)  # N+1!
    return orders
```

## Proposed Solution
```python
def get_orders_with_items(user_id):
    orders = Order.query.filter_by(user_id=user_id)\
        .options(joinedload(Order.items))\
        .all()
    return orders
```

## Acceptance Criteria
- [ ] Query count reduced to 2 (orders + items)
- [ ] Response time < 200ms for 100 orders
- [ ] Existing tests still pass
- [ ] No changes to API response format

## References
- [SQLAlchemy Eager Loading](https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html)
- Related: PERF-003 (similar pattern in products API)
```

## Priority Definitions

| Priority | SLA | Description |
|----------|-----|-------------|
| **P0** | Immediate | Security vulnerability, data corruption risk |
| **P1** | This sprint | Significant issue, blocks quality bar |
| **P2** | Next sprint | Should fix, doesn't block merge |
| **P3** | Backlog | Nice to have, tech debt cleanup |

## Example

```
/kreativreason:triage

> 📋 Triaging latest review findings...
>
> Source: reviews/pr-123-review.json
> Total findings: 15
>
> Prioritizing...
>   P0 (Immediate): 0
>   P1 (This sprint): 3
>   P2 (Next sprint): 5
>   P3 (Backlog): 7
>
> Creating todo files...
>   ✓ todos/P1/PERF-001-open-n+1-query-orders.md
>   ✓ todos/P1/SEC-002-open-input-validation.md
>   ✓ todos/P1/ARCH-003-open-missing-error-handler.md
>   ✓ todos/P2/ARCH-001-open-coupling-payment.md
>   ... (8 more)
>
> 📊 Summary:
>   This sprint: 3 items (~5 story points)
>   Next sprint: 5 items (~8 story points)
>   Backlog: 7 items (~3 story points)
>
> Suggested next steps:
>   1. Review P1 items with team
>   2. Add P1 items to current sprint
>   3. Schedule P2 items for next sprint planning
```

## Resolve Todos

After triage, resolve todos with:

```
/kreativreason:resolve_todo todos/P1/PERF-001-open-n+1-query-orders.md
```

Or resolve multiple in parallel:

```
/kreativreason:resolve_parallel todos/P1/
```
