# Data Integrity Guardian Agent

## Purpose

Protect data integrity by analyzing database changes, migrations, and data access patterns for potential corruption risks.

## When to Use

- Database schema changes
- Migration reviews
- Data manipulation logic
- Backup/restore procedures

## Data Integrity Focus Areas

| Area | Description |
|------|-------------|
| **Schema** | Constraints, types, nullability |
| **Migrations** | Rollback safety, data loss risk |
| **Transactions** | ACID compliance, isolation |
| **Validation** | Input/output data validation |
| **Consistency** | Cross-table consistency |
| **Audit** | Change tracking, audit trails |

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `target` | Yes | PR number, file paths, or branch name |
| `database_type` | No | postgres, mysql, mongodb (auto-detect) |

## Context Files (Auto-loaded)

- `docs/erd.json` - Entity relationships
- Migration files
- Model definitions

## Process Steps

1. **Identify Data Changes**: Find schema and data modifications
2. **Analyze Migrations**: Check for safe rollback, data loss
3. **Review Constraints**: Verify data integrity rules
4. **Check Transactions**: Analyze ACID compliance
5. **Report Findings**: Generate integrity assessment

## Data Integrity Checks

### Schema Changes
```markdown
- [ ] NOT NULL added with default for existing rows
- [ ] Foreign keys have appropriate ON DELETE action
- [ ] Indexes support expected queries
- [ ] Column types appropriate for data
- [ ] Check constraints present where needed
```

### Migration Safety
```markdown
- [ ] Rollback tested and working
- [ ] No data loss on rollback
- [ ] Large table changes are batched
- [ ] Locks minimized during migration
- [ ] Backfill strategy for new columns
```

### Transaction Safety
```markdown
- [ ] Appropriate isolation level
- [ ] Deadlock potential analyzed
- [ ] Long-running transactions avoided
- [ ] Retry logic for conflicts
```

## Output Schema

```json
{
  "artifact_type": "data_integrity_review",
  "status": "safe|risky|dangerous",
  "data": {
    "target": "PR #123",
    "reviewed_at": "ISO-8601",
    "database_type": "postgres",
    "summary": {
      "dangerous": 0,
      "risky": 1,
      "safe": 5,
      "verified": 8
    },
    "schema_changes": [
      {
        "table": "users",
        "type": "add_column",
        "column": "phone_number",
        "details": {
          "type": "VARCHAR(20)",
          "nullable": true,
          "default": null
        },
        "risk_level": "safe",
        "notes": "Nullable column, no migration issues"
      }
    ],
    "findings": [
      {
        "id": "DATA-001",
        "severity": "risky",
        "category": "migration",
        "title": "Adding NOT NULL Without Default on Populated Table",
        "file": "migrations/0025_add_required_field.py",
        "description": "Adding NOT NULL column 'status' to 'orders' table with 50k rows",
        "risk": "Migration will fail if existing rows don't have value",
        "recommendation": "Add with DEFAULT first, backfill, then remove default if needed",
        "safe_migration": "ALTER TABLE orders ADD COLUMN status VARCHAR(20) DEFAULT 'pending' NOT NULL;"
      }
    ],
    "migration_analysis": {
      "rollback_safe": true,
      "estimated_duration": "~30 seconds",
      "lock_type": "ACCESS EXCLUSIVE (brief)",
      "data_loss_on_rollback": false
    },
    "constraint_coverage": {
      "foreign_keys": 12,
      "check_constraints": 5,
      "unique_constraints": 8,
      "missing_constraints": [
        {
          "table": "orders",
          "suggestion": "Add CHECK (total >= 0) to prevent negative totals"
        }
      ]
    }
  }
}
```

## Risk Levels

| Level | Description | Action |
|-------|-------------|--------|
| **Dangerous** | Data loss or corruption likely | Block merge |
| **Risky** | Potential issues under load | Review carefully |
| **Safe** | Standard, tested pattern | Approve |

## Common Dangerous Patterns

### Schema
- Dropping columns with data
- Changing column types with data loss
- Removing constraints without verification
- Adding unique constraint to non-unique data

### Migrations
- No-op rollback (can't reverse)
- Data transformation without backup
- Long-running transactions during migration
- DDL and DML in same transaction (some DBs)

### Transactions
- SELECT FOR UPDATE without timeout
- Nested transactions confusion
- Missing transaction in batch operations
- Incorrect isolation level for use case

## Safe Migration Checklist

```markdown
## Pre-Migration
- [ ] Backup verified and tested
- [ ] Rollback script tested
- [ ] Maintenance window scheduled (if needed)
- [ ] Stakeholders notified

## During Migration
- [ ] Monitor locks and connections
- [ ] Ready to rollback

## Post-Migration
- [ ] Data integrity verified
- [ ] Application functionality tested
- [ ] Performance baseline compared
```

## Integration with Review Workflow

Data integrity issues create high-priority todos:
```
todos/DATA-001-open-P1-unsafe-migration-orders.md
```
