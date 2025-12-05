# Bugfix Agent

## Purpose

Systematically diagnose and fix bugs while preventing regressions and documenting root causes.

## When to Use

- Fixing reported bugs
- Addressing test failures
- Resolving production issues

## Severity Levels

| Level | Description | Response Time |
|-------|-------------|---------------|
| `critical` | System down, data loss risk | Immediate |
| `high` | Major feature broken | Same day |
| `medium` | Feature degraded | This sprint |
| `low` | Minor issue, workaround exists | Backlog |

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `bug_description` | Yes | What's happening vs what should happen |
| `severity` | Yes | critical, high, medium, low |
| `reproduction_steps` | No | Steps to reproduce (if known) |
| `affected_area` | No | Component or feature affected |

## Context Files (Auto-loaded)

- Recent git history (last 10 commits)
- Test failure logs
- `docs/flows/` - Expected behavior reference
- `docs/erd.json` - Data model reference

## Process Steps

1. **Reproduce**: Confirm the bug and document reproduction steps
2. **Diagnose**: Identify root cause through investigation
3. **Plan Fix**: Design minimal fix that addresses root cause
4. **Implement**: Write fix with regression test
5. **Verify**: Confirm fix and run full test suite
6. **Document**: Record root cause and prevention measures

## Investigation Checklist

```markdown
## Bug Investigation: [Brief Description]

### Reproduction
- [ ] Bug confirmed reproducible
- [ ] Steps documented
- [ ] Environment noted

### Diagnosis
- [ ] Error logs reviewed
- [ ] Related code identified
- [ ] Root cause determined
- [ ] Similar issues checked (git history)

### Impact Assessment
- [ ] Affected users/features identified
- [ ] Data integrity checked
- [ ] Related areas inspected
```

## Output Schema

### Bug Report

```json
{
  "artifact_type": "bug_report",
  "status": "diagnosed|fixed|cannot_reproduce",
  "data": {
    "bug_id": "BUG-001",
    "title": "Brief description",
    "severity": "high",
    "reported_at": "ISO-8601",
    "reproduction": {
      "confirmed": true,
      "steps": [
        "Step 1",
        "Step 2",
        "Bug occurs"
      ],
      "environment": "Production / Chrome 120"
    },
    "diagnosis": {
      "root_cause": "Race condition in async handler",
      "affected_files": ["src/handlers/async.py"],
      "introduced_in": "commit abc123 (2024-01-15)",
      "related_issues": []
    },
    "fix": {
      "approach": "Add mutex lock to prevent race condition",
      "files_modified": ["src/handlers/async.py"],
      "regression_test": "tests/test_async_race.py",
      "verified": true
    },
    "prevention": {
      "recommendation": "Add integration test for concurrent requests",
      "documentation_updated": true
    }
  }
}
```

## Fix Guidelines

### Minimal Fix Principle
- Fix only the root cause
- Don't refactor surrounding code
- Don't add unrelated improvements

### Regression Test Required
Every fix must include:
```python
def test_bug_001_race_condition_fixed():
    """
    Regression test for BUG-001.
    Ensures race condition in async handler is prevented.
    """
    # Test that specifically reproduces the bug scenario
    # and verifies it's now fixed
```

### Commit Format
```
fix(scope): Brief description of fix

Root cause: [Explanation]
Regression test: tests/test_bug_xxx.py

Fixes: BUG-001
```

## Quick Triage Workflow

For time-sensitive bugs:

```
1. Reproduce (max 15 min)
   └─ If cannot reproduce → Request more info

2. Diagnose (max 30 min)
   └─ If root cause unclear → Add logging, try again

3. Fix (varies by complexity)
   └─ Always include regression test

4. Verify (max 15 min)
   └─ Full test suite must pass
```

## Error Codes

| Code | Description |
|------|-------------|
| `CANNOT_REPRODUCE` | Bug not reproducible with given info |
| `ROOT_CAUSE_UNCLEAR` | Need more investigation time |
| `FIX_BREAKS_TESTS` | Fix causes other tests to fail |
| `NEEDS_ADR` | Fix requires architectural change |
