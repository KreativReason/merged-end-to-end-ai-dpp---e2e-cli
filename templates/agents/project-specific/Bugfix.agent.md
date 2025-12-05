# Bugfix Agent

**Follow:** `_common.guardrails.md`

## Purpose
Diagnose and fix bugs in the Richtungswechsel ROI Tracker application while maintaining German field names, multi-tenancy, and formula integrity.

## Inputs (Required)
- `bug_description`: Clear description of the bug
- `reproduction_steps`: Steps to reproduce (if available)
- `expected_behavior`: What should happen
- `actual_behavior`: What actually happens
- **Context Files**:
  - `docs/prd.json` (to understand intended behavior)
  - `docs/erd.json` (to verify data model)
  - `docs/adr/project.json` (to check architectural decisions)
  - Relevant source files (based on bug location)

## Task
Diagnose root cause, implement fix, add regression tests, and verify no side effects.

### Process Steps
1. **Reproduce Bug**: Verify bug exists and understand scope
2. **Load Context**: Read relevant code, tests, and documentation
3. **Diagnose Root Cause**: Identify why bug occurs
4. **Assess Impact**: Determine if bug affects other features
5. **Implement Fix**: Write minimal, focused fix
6. **Add Regression Test**: Prevent bug from recurring
7. **Verify No Side Effects**: Run full test suite
8. **Validate Output**: Check fix resolves issue without breaking other features
9. **Emit Result**: Output bugfix report JSON

### Validation Requirements
- Bug is reproducible before fix
- Fix resolves the issue completely
- Regression test added and passing
- No existing tests broken by fix
- German field names preserved
- Multi-tenancy not compromised
- Formula calculations still match spreadsheet (if applicable)

## Bug Categories

### Category 1: German Language Issues
```typescript
// ❌ BUG: English field name used
const revenue = data.currentRevenue; // WRONG

// ✅ FIX: Use German field name
const revenue = data.aktuelleJaehrlicheEinnahmen; // CORRECT
```

### Category 2: Multi-Tenancy Violations
```typescript
// ❌ BUG: Query doesn't filter by organization
const inputs = await db.collection('roiInputs').get();

// ✅ FIX: Filter by organizationId
const inputs = await db.collection('roiInputs')
  .where('organizationId', '==', currentUserOrgId)
  .get();
```

### Category 3: Formula Calculation Errors
```typescript
// ❌ BUG: Incorrect formula
const roi = (revenue - costs) / costs; // Doesn't match MVP

// ✅ FIX: Use MVP formula exactly
const roi = ((revenue - costs) / costs) * 100; // Matches MVP line 245
```

### Category 4: Clerk Authentication Issues
```typescript
// ❌ BUG: Not checking organization membership
const canAccess = user.id === resourceOwnerId;

// ✅ FIX: Check organization membership
const canAccess = user.publicMetadata.organizationId === resource.organizationId;
```

### Category 5: Chart.js Display Errors
```typescript
// ❌ BUG: English chart labels
const options = {
  plugins: {
    title: { text: 'Monthly Revenue' }
  }
};

// ✅ FIX: German chart labels
const options = {
  plugins: {
    title: { text: 'Monatlicher Umsatz' }
  }
};
```

## Bug Severity Levels

### Critical (P0)
- Data loss or corruption
- Security vulnerability
- Complete feature failure
- Multi-tenancy breach (data leakage between organizations)
- Formula producing wrong calculations

**Response Time**: Immediate fix required

### High (P1)
- Major feature not working
- German language not displaying correctly
- Authentication failure
- Performance degradation (>2 second response times)

**Response Time**: Fix within 24 hours

### Medium (P2)
- Minor feature issues
- UI rendering problems
- Non-critical validation errors
- Chart display issues

**Response Time**: Fix within 1 week

### Low (P3)
- Cosmetic issues
- Minor text errors
- Enhancement requests disguised as bugs

**Response Time**: Fix in next sprint

## Output Schema

```json
{
  "artifact_type": "bugfix",
  "status": "complete",
  "validation": "passed",
  "approval_required": true,
  "approvers": ["Mustaffa", "Usama"],
  "next_phase": "deployment",
  "data": {
    "bug_id": "BUG-001",
    "title": "Bug title",
    "severity": "critical|high|medium|low",
    "reported_date": "2025-10-16T00:00:00Z",
    "fixed_date": "2025-10-16T00:00:00Z",
    "developer": "Claude Code",
    "root_cause": {
      "category": "multi_tenancy_violation",
      "description": "Query not filtering by organizationId",
      "affected_files": ["lib/firebase/queries.ts"],
      "introduced_in": "TASK-003"
    },
    "reproduction_steps": [
      "Step 1",
      "Step 2",
      "Step 3"
    ],
    "expected_behavior": "What should happen",
    "actual_behavior": "What actually happens",
    "fix_description": "Detailed description of the fix",
    "files_changed": [
      {
        "path": "lib/firebase/queries.ts",
        "action": "modified",
        "lines_added": 5,
        "lines_removed": 2,
        "description": "Added organizationId filter to query"
      }
    ],
    "regression_test": {
      "path": "__tests__/lib/queries.test.ts",
      "description": "Test verifies organizationId filter is applied",
      "test_count": 3
    },
    "test_results": {
      "regression_test_passing": true,
      "existing_tests_passing": true,
      "total_tests": 125,
      "passed": 125,
      "failed": 0
    },
    "side_effects": {
      "identified": false,
      "description": "No side effects detected"
    },
    "verification": {
      "manual_testing": "Manually tested with 2 organizations, verified isolation",
      "automated_testing": "All tests passing",
      "formula_verification": "Not applicable"
    },
    "related_bugs": [],
    "documentation_updates": [
      {
        "file": "docs/ARCHITECTURE.md",
        "description": "Documented query pattern for multi-tenancy"
      }
    ]
  }
}
```

## Formula Bug Protocol

If bug affects ROI calculations:

1. **Verify Against Spreadsheet**: Compare output with Excel reference
2. **Check MVP**: Verify against verified MVP formulas
3. **Run Calculation Tests**: Execute full test suite with known inputs
4. **Document Changes**: If formula must change, document why in ADR
5. **Get Approval**: Formula changes require Hermann + Usama approval

```typescript
// Example: Fixing formula bug
describe('Formula Verification', () => {
  it('should match spreadsheet reference calculation', () => {
    // Input from spreadsheet row 5
    const input = {
      aktuelleJaehrlicheEinnahmen: 100000,
      durchschnittlicherKundenwert: 5000,
      kundengewinnungskosten: 500
    };

    const result = calculateRoi(input);

    // Expected output from spreadsheet cell F5
    expect(result.roi).toBeCloseTo(85.5, 1); // ±0.1% tolerance
    expect(result.nettoMehrwert).toBeCloseTo(42750, 0);
  });
});
```

## Multi-Tenancy Bug Protocol

If bug involves data leakage:

1. **Immediate Action**: Mark as P0 Critical
2. **Audit Scope**: Check all affected queries
3. **Fix Security Rules**: Update Firestore rules if needed
4. **Verify Isolation**: Test with multiple organizations
5. **Add Tests**: Prevent similar bugs

```typescript
// Example: Multi-tenancy regression test
describe('Multi-Tenancy Isolation', () => {
  it('should prevent cross-organization data access', async () => {
    const org1Id = 'org-1';
    const org2Id = 'org-2';

    // Create data for org1
    await createRoiInput({ value: 100 }, org1Id);

    // Try to query from org2
    const results = await getRoiInputs(org2Id);

    // Should return empty (no cross-org access)
    expect(results).toHaveLength(0);
  });
});
```

## German Language Bug Protocol

If bug involves German text display:

1. **Check Field Names**: Verify German database field names used
2. **Check UI Labels**: Verify German labels in components
3. **Check Locale**: Verify date/number formatting uses German locale
4. **Check Encoding**: Verify UTF-8 encoding for umlauts (ä, ö, ü, ß)

```typescript
// Example: German language regression test
describe('German Language Support', () => {
  it('should display German field labels correctly', () => {
    render(<RoiForm />);

    expect(screen.getByLabelText('Aktuelle jährliche Einnahmen')).toBeInTheDocument();
    expect(screen.getByLabelText('Kundengewinnungskosten')).toBeInTheDocument();
  });

  it('should format numbers in German locale', () => {
    const formatted = formatCurrency(1234.56, 'de-DE');
    expect(formatted).toBe('1.234,56 €');
  });
});
```

## Error Handling

```json
{
  "error": {
    "code": "BUGFIX_FAILED",
    "message": "Bug fix failed validation",
    "details": [
      "Regression test not passing",
      "Fix introduced new bug in related feature"
    ],
    "artifact": "bugfix",
    "remediation": "Revise fix to pass regression test and verify no side effects"
  }
}
```

## Human Approval Gate

After successful completion, this agent requires approval from:
- **Mustaffa** (QA Engineer - testing validation)
- **Usama** (Lead Developer - code review)

For P0 Critical bugs, immediate deployment after approval.

## Bug Prevention Checklist

After fixing bug, consider:
- [ ] Can this bug be detected by a lint rule?
- [ ] Should we add a pre-commit hook to prevent this?
- [ ] Do we need to update coding standards documentation?
- [ ] Should we add this pattern to common guardrails?
- [ ] Do other features have the same vulnerability?

## Commit Message Format

```
fix(<scope>): <brief description>

Root cause: <explanation>
Fix: <what was changed>
Testing: <how it was verified>

Fixes BUG-001
```

Example:
```
fix(multi-tenancy): Add organizationId filter to roiInputs query

Root cause: Query was fetching all roiInputs without organization filter
Fix: Added .where('organizationId', '==', userOrgId) to query
Testing: Manual testing with 2 orgs + regression test added

- Verified no cross-org data leakage
- All existing tests passing
- Added regression test in __tests__/lib/queries.test.ts

Fixes BUG-001
```
