# Review Command

> Perform comprehensive multi-agent code reviews

## Usage

```
/kreativreason:review <target>
```

## Description

The Review command performs exhaustive code reviews using multiple specialized agents in parallel, analyzing security, performance, architecture, simplicity, and data integrity.

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `target` | Yes | PR number (#123), GitHub URL, file paths, or branch name |
| `depth` | No | quick, standard, thorough (default: standard) |
| `focus` | No | security, performance, architecture, all (default: all) |

## Review Agents (Parallel Execution)

```
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Agent Review                            │
├─────────────────┬──────────────┬──────────────┬────────────────┤
│ security-       │ performance- │ architecture-│ code-          │
│ sentinel        │ oracle       │ strategist   │ simplicity     │
├─────────────────┼──────────────┼──────────────┼────────────────┤
│ OWASP checks    │ N+1 queries  │ ADR align    │ Over-engineer  │
│ Injection       │ Memory leaks │ Patterns     │ Complexity     │
│ Auth bypass     │ Slow paths   │ Coupling     │ YAGNI          │
│ Data exposure   │ Caching      │ Cohesion     │ Readability    │
└─────────────────┴──────────────┴──────────────┴────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │ data-integrity-  │
                    │ guardian         │
                    ├──────────────────┤
                    │ Schema safety    │
                    │ Migration risk   │
                    │ Constraints      │
                    └──────────────────┘
```

## Workflow

### Phase 1: Target Determination

```
1. Identify review type (PR, branch, files)
2. Check git status
3. Offer worktree isolation if needed
4. Fetch PR metadata (if applicable)
5. Ensure proper checkout
```

### Phase 2: Parallel Analysis

Launch all review agents simultaneously:
- Security Sentinel
- Performance Oracle
- Architecture Strategist
- Code Simplicity Reviewer
- Data Integrity Guardian

### Phase 3: Deep Analysis

After initial scan:
1. Stakeholder perspective analysis (dev, ops, user, security)
2. Scenario exploration (edge cases, concurrency, scaling)
3. Multi-angle reviews (technical, business, risk)

### Phase 4: Synthesis

Combine all agent findings:
1. Deduplicate overlapping findings
2. Prioritize by severity
3. Group by category
4. Generate actionable todos

### Phase 5: Todo Creation

Create structured todo files:

```
todos/
  SEC-001-open-P1-sql-injection-users.md
  PERF-001-open-P2-n+1-query-orders.md
  ARCH-001-open-P2-tight-coupling-payment.md
  SIMP-001-discussion-simplify-factory.md
```

## Output Schema

```json
{
  "artifact_type": "code_review",
  "status": "pass|warn|fail",
  "data": {
    "target": "PR #123",
    "reviewed_at": "ISO-8601",
    "depth": "standard",
    "summary": {
      "verdict": "warn",
      "blocking_issues": 0,
      "critical": 0,
      "high": 2,
      "medium": 5,
      "low": 8,
      "info": 12
    },
    "agent_reports": {
      "security": {
        "status": "pass",
        "findings_count": 3,
        "critical": 0
      },
      "performance": {
        "status": "warn",
        "findings_count": 2,
        "critical": 0
      },
      "architecture": {
        "status": "pass",
        "findings_count": 4,
        "critical": 0
      },
      "simplicity": {
        "status": "warn",
        "findings_count": 3,
        "critical": 0
      },
      "data_integrity": {
        "status": "pass",
        "findings_count": 2,
        "critical": 0
      }
    },
    "top_findings": [
      {
        "id": "PERF-001",
        "severity": "high",
        "agent": "performance-oracle",
        "title": "N+1 Query in Orders API",
        "file": "src/api/orders.py",
        "line": 78
      }
    ],
    "todos_created": [
      "todos/PERF-001-open-P2-n+1-query-orders.md",
      "todos/ARCH-001-open-P2-tight-coupling-payment.md"
    ],
    "praise": [
      "Clean separation in auth module",
      "Good test coverage for new features",
      "Consistent error handling"
    ],
    "recommendation": "Address P2 issues before merge, P3 can follow"
  }
}
```

## Todo File Format

```markdown
---
id: PERF-001
status: open
priority: P2
category: performance
file: src/api/orders.py
line: 78
---

# N+1 Query in Orders API

## Problem
Each order triggers separate database query for items.
100 orders = 101 queries, ~2s response time.

## Current Code
```python
for order in orders:
    items = get_items(order.id)
```

## Proposed Solution
Use eager loading or batch query.

```python
orders = Order.query.options(joinedload(Order.items)).all()
```

## Acceptance Criteria
- [ ] Query count reduced to 2 (orders + items)
- [ ] Response time < 200ms for 100 orders
- [ ] No changes to API response format
```

## Severity Definitions

| Severity | Description | Action |
|----------|-------------|--------|
| **Critical** | Security/data risk, blocks merge | Must fix now |
| **High** | Significant issue | Fix before merge |
| **Medium** | Should address | Fix before/after merge |
| **Low** | Minor improvement | Next sprint |
| **Info** | Suggestion | Optional |

## Example

```
/kreativreason:review #123

> 🔍 Reviewing PR #123: feat: Add user authentication
>
> Launching review agents...
>   ⏳ security-sentinel
>   ⏳ performance-oracle
>   ⏳ architecture-strategist
>   ⏳ code-simplicity-reviewer
>   ⏳ data-integrity-guardian
>
> Analysis complete:
>   ✓ security-sentinel: PASS (3 info findings)
>   ⚠ performance-oracle: WARN (1 high, 1 medium)
>   ✓ architecture-strategist: PASS (aligned with ADRs)
>   ⚠ code-simplicity-reviewer: WARN (1 over-engineered)
>   ✓ data-integrity-guardian: PASS
>
> Created todos:
>   - todos/PERF-001-open-P2-session-lookup.md
>   - todos/SIMP-001-discussion-auth-factory.md
>
> 📋 Summary: WARN - 2 issues to address before merge
>
> Recommendation:
>   1. Address PERF-001 (add caching for session lookup)
>   2. Discuss SIMP-001 (factory may be over-engineered)
>   3. Then merge
```

## Quick Review Mode

For faster feedback:

```
/kreativreason:review #123 depth:quick

> Quick review (pattern-based only)...
> Complete in 15 seconds
> No critical issues found
```
