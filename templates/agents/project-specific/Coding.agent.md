# Coding Agent

**Follow:** `_common.guardrails.md`

## Purpose
Implement tasks from the task backlog by writing production-ready code with tests, documentation, and validation.

## Inputs (Required)
- `task_id`: The TASK-### ID to implement
- **Context Files**:
  - `docs/tasks.json` (to load task details)
  - `docs/prd.json` (for feature context)
  - `docs/erd.json` (for data model)
  - `docs/adr/project.json` (for architectural decisions)
  - Files listed in `task.context_plan.beginning_context`

## Task
Implement the specified task following all acceptance criteria, definition of done items, and project-specific coding standards (German field names, multi-tenancy, formula preservation).

### Process Steps
1. **Load Task Context**: Read task details and all referenced context files
2. **Review Dependencies**: Verify all dependent tasks are completed
3. **Implement Code**: Write production-ready code following standards
4. **Write Tests**: Implement testing strategy from task
5. **Run Validation**: Execute tests, linting, type checking
6. **Update Documentation**: Update relevant docs if needed
7. **Validate Output**: Check all acceptance criteria met
8. **Emit Result**: Output implementation report JSON

### Validation Requirements
- All acceptance criteria satisfied
- All definition of done items completed
- Tests written and passing (per testing_strategy)
- TypeScript compilation successful
- ESLint passing (no errors)
- Code follows German field name conventions
- Multi-tenancy validated (organizationId present)

## Coding Standards

### TypeScript Best Practices
```typescript
// ✅ CORRECT: German field names with English variables
interface RoiInput {
  aktuelleJaehrlicheEinnahmen: number; // Current annual revenue
  durchschnittlicherKundenwert: number; // Average customer value
  kundengewinnungskosten: number; // Customer acquisition cost
}

const calculateRoi = (input: RoiInput) => {
  const revenue = input.aktuelleJaehrlicheEinnahmen;
  const customerValue = input.durchschnittlicherKundenwert;
  // ... calculations
};
```

### Firebase Firestore Patterns
```typescript
// ✅ CORRECT: organizationId in all documents
const createRoiInput = async (data: RoiInputData, orgId: string) => {
  await db.collection('roiInputs').add({
    ...data,
    organizationId: orgId, // Required for multi-tenancy
    createdAt: FieldValue.serverTimestamp()
  });
};

// ✅ CORRECT: Query filtered by organization
const getRoiInputs = (orgId: string) => {
  return db.collection('roiInputs')
    .where('organizationId', '==', orgId)
    .get();
};
```

### Clerk Authentication Patterns
```typescript
// ✅ CORRECT: Validate organization membership
const validateAccess = async (userId: string, resourceOrgId: string) => {
  const user = await clerkClient.users.getUser(userId);
  const userOrgId = user.publicMetadata.organizationId;

  if (userOrgId !== resourceOrgId) {
    throw new Error('Unauthorized: Organization mismatch');
  }
};
```

### Chart.js Configuration
```typescript
// ✅ CORRECT: German labels
const chartOptions = {
  plugins: {
    title: {
      display: true,
      text: 'Monatliche Umsatzentwicklung' // German title
    },
    legend: {
      labels: {
        generateLabels: (chart) => [{
          text: 'Tatsächlicher Umsatz', // German label
          fillStyle: '#003f5c'
        }]
      }
    }
  },
  scales: {
    y: {
      title: {
        display: true,
        text: 'Umsatz (€)' // German axis label
      }
    },
    x: {
      title: {
        display: true,
        text: 'Monat' // German axis label
      }
    }
  }
};
```

## Testing Requirements

### Unit Tests (Jest)
```typescript
// Example: functions/src/__tests__/calculateRoi.test.ts
describe('calculateRoi', () => {
  it('should calculate ROI correctly with German field names', () => {
    const input = {
      aktuelleJaehrlicheEinnahmen: 100000,
      durchschnittlicherKundenwert: 5000,
      kundengewinnungskosten: 500
    };

    const result = calculateRoi(input);

    expect(result.roi).toBeCloseTo(0.85, 2);
    expect(result.nettoMehrwert).toBeGreaterThan(0);
  });

  it('should handle division by zero gracefully', () => {
    const input = {
      aktuelleJaehrlicheEinnahmen: 0,
      durchschnittlicherKundenwert: 0,
      kundengewinnungskosten: 500
    };

    expect(() => calculateRoi(input)).not.toThrow();
  });
});
```

### Integration Tests (React Testing Library)
```typescript
// Example: __tests__/components/RoiAnalyseForm.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import RoiAnalyseForm from '@/components/RoiAnalyseForm';

describe('RoiAnalyseForm', () => {
  it('should display German field labels', () => {
    render(<RoiAnalyseForm />);

    expect(screen.getByLabelText('Aktuelle jährliche Einnahmen')).toBeInTheDocument();
    expect(screen.getByLabelText('Durchschnittlicher Kundenwert')).toBeInTheDocument();
  });

  it('should validate German number format', async () => {
    render(<RoiAnalyseForm />);

    const input = screen.getByLabelText('Aktuelle jährliche Einnahmen');
    fireEvent.change(input, { target: { value: '50.000,00' } }); // German format

    // Should accept German number format
    expect(input).toHaveValue('50.000,00');
  });
});
```

## Formula Preservation Protocol

When implementing ROI calculations:

```typescript
// ✅ CORRECT: Preserve MVP formula exactly
// Source: MVP roi-final.html line 234-245
const calculateMonthlyProjection = (
  baseCustomers: number,
  monthlyGrowthRate: number,
  month: number
) => {
  // Formula preserved from MVP (verified against spreadsheet)
  const customers = baseCustomers * Math.pow(1 + monthlyGrowthRate, month);
  return Math.round(customers * 100) / 100; // Round to 2 decimals
};

// ❌ WRONG: Don't refactor MVP formulas without approval
const calculateMonthlyProjection = (base: number, rate: number, month: number) => {
  return base * (1 + rate * month); // WRONG: Changes formula logic
};
```

## Output Schema

```json
{
  "artifact_type": "implementation",
  "status": "complete",
  "validation": "passed",
  "approval_required": true,
  "approvers": ["Mustaffa", "Usama"],
  "next_phase": "code_review",
  "data": {
    "task_id": "TASK-016",
    "title": "Task title",
    "implementation_date": "2025-10-16T00:00:00Z",
    "developer": "Claude Code",
    "files_changed": [
      {
        "path": "app/components/NewComponent.tsx",
        "action": "created",
        "lines_added": 150,
        "lines_removed": 0,
        "description": "Created new component with German labels"
      }
    ],
    "tests_added": [
      {
        "path": "__tests__/components/NewComponent.test.tsx",
        "type": "integration",
        "test_count": 5,
        "coverage_percentage": 95
      }
    ],
    "acceptance_criteria_status": [
      {
        "criteria": "Component displays German labels",
        "status": "satisfied",
        "evidence": "Tests verify German text rendering"
      }
    ],
    "definition_of_done_checklist": [
      {
        "item": "Code implemented",
        "completed": true,
        "notes": "All acceptance criteria met"
      },
      {
        "item": "Tests passing",
        "completed": true,
        "notes": "95% coverage achieved"
      },
      {
        "item": "TypeScript compiles",
        "completed": true,
        "notes": "No type errors"
      }
    ],
    "technical_decisions": [
      {
        "decision": "Used Chart.js for visualization",
        "rationale": "Aligns with ADR-0002 technology stack",
        "adr_reference": null
      }
    ],
    "dependencies_verified": [
      {
        "task_id": "TASK-001",
        "status": "completed",
        "verified_at": "2025-10-16T00:00:00Z"
      }
    ],
    "test_results": {
      "unit_tests": {
        "total": 10,
        "passed": 10,
        "failed": 0,
        "coverage": 95
      },
      "integration_tests": {
        "total": 5,
        "passed": 5,
        "failed": 0,
        "coverage": 85
      },
      "linting": {
        "errors": 0,
        "warnings": 2
      }
    },
    "performance_metrics": {
      "response_time_ms": 150,
      "memory_usage_mb": 45,
      "cpu_usage_percent": 12
    },
    "security_checklist": [
      {
        "item": "organizationId validated in all queries",
        "status": "completed",
        "details": "Firestore rules enforce organization isolation"
      },
      {
        "item": "User input sanitized",
        "status": "completed",
        "details": "Zod validation on all form inputs"
      }
    ],
    "documentation_updates": [
      {
        "file": "docs/ARCHITECTURE.md",
        "description": "Updated component diagram"
      }
    ],
    "known_issues": [],
    "future_considerations": [
      "Consider adding caching for improved performance"
    ]
  }
}
```

## Multi-Tenancy Checklist

Before marking task complete, verify:
- [ ] `organizationId` present in all data writes
- [ ] Queries filtered by `organizationId`
- [ ] Firestore security rules enforce organization isolation
- [ ] Admin checks validate role before cross-org access
- [ ] UI components display org-scoped data only
- [ ] Tests verify organization isolation

## German Language Checklist

Before marking task complete, verify:
- [ ] All UI labels in German
- [ ] Database fields use German names
- [ ] Form validation messages in German
- [ ] Error messages in German
- [ ] Chart labels and tooltips in German
- [ ] Date/number formatting uses German locale (DD.MM.YYYY, €)

## Error Handling

```json
{
  "error": {
    "code": "IMPLEMENTATION_FAILED",
    "message": "Task implementation failed validation",
    "details": [
      "2 acceptance criteria not satisfied",
      "Test coverage below 80% threshold"
    ],
    "artifact": "implementation",
    "remediation": "Address failing criteria and add tests to meet coverage threshold"
  }
}
```

## Human Approval Gate

After successful completion, this agent requires approval from:
- **Mustaffa** (QA Engineer - testing validation)
- **Usama** (Lead Developer - code review)

Do not merge code until explicit human approval is received.

## Pre-Commit Checklist

Before submitting for review:
- [ ] All tests passing (`npm run test`)
- [ ] TypeScript compilation successful (`npm run build`)
- [ ] ESLint passing (`npm run lint`)
- [ ] Prettier formatting applied (`npm run format`)
- [ ] German field names validated
- [ ] Multi-tenancy validated
- [ ] Documentation updated
- [ ] Commit message follows convention

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Example:
```
feat(roi-calculator): Add CSV export functionality

- Implemented German-labeled CSV export
- Added server-side generation via Cloud Function
- Includes all 17 RW projection columns
- Tests verify German headers and formatting

Closes TASK-012
```
