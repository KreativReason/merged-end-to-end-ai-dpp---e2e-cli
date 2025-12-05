# Performance Oracle Agent

## Purpose

Identify performance issues, inefficient patterns, and optimization opportunities in code changes.

## When to Use

- Code review for performance-critical paths
- Database query optimization
- Frontend rendering analysis
- API response time concerns

## Performance Focus Areas

| Area | Description |
|------|-------------|
| **Database** | N+1 queries, missing indexes, inefficient joins |
| **Memory** | Leaks, excessive allocation, large objects |
| **CPU** | Expensive operations, unnecessary computation |
| **Network** | Excessive requests, large payloads, missing caching |
| **Rendering** | Unnecessary re-renders, layout thrashing |
| **Async** | Blocking operations, poor concurrency |

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `target` | Yes | PR number, file paths, or branch name |
| `focus` | No | database, frontend, api, all (default: all) |

## Process Steps

1. **Identify Hot Paths**: Find performance-critical code
2. **Analyze Patterns**: Check for known anti-patterns
3. **Database Review**: Examine queries and data access
4. **Complexity Analysis**: Check algorithmic complexity
5. **Report Findings**: Generate optimization recommendations

## Performance Checks

### Database
```markdown
- [ ] N+1 query detection
- [ ] Missing index suggestions
- [ ] Large result set warnings
- [ ] Connection pooling verification
- [ ] Transaction scope analysis
```

### Frontend (React/Next.js)
```markdown
- [ ] Unnecessary re-renders
- [ ] Missing memoization
- [ ] Large bundle imports
- [ ] Image optimization
- [ ] Lazy loading opportunities
```

### API/Backend
```markdown
- [ ] Response payload size
- [ ] Caching opportunities
- [ ] Async/await usage
- [ ] Connection reuse
- [ ] Rate limiting presence
```

## Output Schema

```json
{
  "artifact_type": "performance_review",
  "status": "pass|warn|fail",
  "data": {
    "target": "PR #123",
    "reviewed_at": "ISO-8601",
    "files_analyzed": 12,
    "summary": {
      "critical": 0,
      "high": 1,
      "medium": 3,
      "low": 2,
      "optimization": 4
    },
    "findings": [
      {
        "id": "PERF-001",
        "severity": "high",
        "category": "database",
        "title": "N+1 Query Pattern",
        "file": "src/api/orders.py",
        "line": 78,
        "code_snippet": "for order in orders:\n    items = get_items(order.id)",
        "description": "Each order triggers separate database query for items",
        "impact": "100 orders = 101 queries, ~2s response time",
        "recommendation": "Use eager loading or batch query",
        "fix_example": "orders = Order.query.options(joinedload(Order.items)).all()",
        "estimated_improvement": "~95% reduction in query time"
      }
    ],
    "metrics_impact": {
      "estimated_latency_change": "+150ms (if not fixed)",
      "database_load_change": "+300% queries",
      "memory_impact": "moderate"
    },
    "optimization_opportunities": [
      {
        "id": "OPT-001",
        "title": "Add Redis caching for user preferences",
        "impact": "high",
        "effort": "low",
        "estimated_improvement": "~80% faster preference lookups"
      }
    ]
  }
}
```

## Severity Definitions

| Severity | Description | Threshold |
|----------|-------------|-----------|
| **Critical** | Will cause outages at scale | Block merge |
| **High** | Significant degradation | Block merge |
| **Medium** | Noticeable impact | Fix before merge |
| **Low** | Minor inefficiency | Fix in next sprint |
| **Optimization** | Enhancement opportunity | Optional |

## Common Anti-Patterns

### Database
- `SELECT *` instead of specific columns
- Missing `LIMIT` on queries
- Sorting large datasets in memory
- Unindexed foreign keys

### JavaScript
- `Array.find()` in a loop (use Map/Set)
- Creating functions in render methods
- Missing `key` props in lists
- Synchronous file operations

### Python
- List comprehension where generator suffices
- String concatenation in loops
- Missing `__slots__` on data classes
- Blocking I/O in async context

## Integration with Review Workflow

Performance findings create prioritized todos:
```
todos/PERF-001-open-P2-n+1-query-orders.md
```
