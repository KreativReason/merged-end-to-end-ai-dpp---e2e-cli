# Common Agent Guardrails

**ALL agents must follow these rules without exception.**

## Output Format
- **JSON ONLY**: Never output prose, explanations, or markdown around JSON
- **No code fences**: Do not wrap JSON in ```json``` blocks
- **Pure JSON**: Output must be valid JSON that can be parsed directly
- **No commentary**: Never add explanatory text before or after JSON

## Validation Requirements
- **Read models.py first**: Always check Pydantic models before generating JSON
- **Validate before emit**: JSON must pass Pydantic validation
- **Fail fast**: Stop immediately if validation fails
- **Report validation errors**: Output validation errors in JSON format if they occur

## Context Awareness
- **Load existing artifacts**: Read all relevant docs/*.json files before acting
- **Check consistency**: Ensure new output is consistent with existing artifacts
- **Reference stable IDs**: Use existing FR-###, ST-###, TASK-###, ADR-#### IDs
- **Maintain relationships**: Preserve cross-references between artifacts

## Stable ID Management
- **Never regenerate**: Existing IDs are immutable
- **Increment only**: Add new items with next available ID
- **Format consistency**: 
  - Features: FR-001, FR-002, etc.
  - Stories: ST-001, ST-002, etc.
  - Tasks: TASK-001, TASK-002, etc.
  - ADRs: ADR-0001, ADR-0002, etc.
  - SOW items: SOW-001, SOW-002, etc.

## Human Approval Gates
- **Stop for approval**: Never auto-advance to next pipeline phase
- **Declare completion**: End output with status indicating approval needed
- **List approvers**: Specify who needs to approve (per Chat_GPT_Setup_Instructions.mdc)
- **Wait for explicit go-ahead**: Do not assume approval

## Error Handling
- **JSON format for errors**: Even errors must be in JSON format
- **Include error codes**: Use consistent error classification
- **Provide context**: Include enough detail for debugging
- **Suggest remediation**: When possible, suggest how to fix the issue

## Agent Coordination
- **Read agent specs**: Follow the specific agent.md file for your role
- **Use template pattern**: Follow agents/_template.agent.md structure
- **Declare dependencies**: State what artifacts you need to read
- **Signal completion**: Indicate when your phase is complete

## Example Error Output
```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "PRD JSON does not match Pydantic model",
    "details": ["Missing required field: project_name", "Invalid format: owner_email"],
    "artifact": "prd",
    "remediation": "Fix validation errors and regenerate"
  }
}
```

## Example Success Output
```json
{
  "artifact_type": "prd",
  "status": "complete",
  "validation": "passed",
  "approval_required": true,
  "approvers": ["Cynthia", "Hermann", "Usama"],
  "next_phase": "flow_design",
  "data": {
    // ... actual artifact content
  }
}
```

---

# Generated Project Architecture Rules

**These rules apply to ALL generated child projects and must be enforced during scaffolding.**

## Architecture Style: Modular Monolith

All projects follow domain-driven modular monolith architecture:

```
src/
├── domains/                  # Business domain modules
│   ├── {domain-name}/       # One folder per bounded context
│   │   ├── index.ts         # PUBLIC API - barrel export (ONLY import from here)
│   │   ├── features/        # Feature implementations
│   │   ├── components/      # Domain-specific UI (frontend)
│   │   ├── hooks/           # Domain-specific hooks (frontend)
│   │   ├── {domain}.controller.ts  # Thin HTTP layer (backend)
│   │   ├── {domain}.service.ts     # Business logic (backend)
│   │   └── {domain}.repository.ts  # Data access (backend)
│   └── ...
├── shared/                   # Cross-domain utilities ONLY
├── infrastructure/           # External integrations
└── middleware/               # Express/framework middleware
```

## Domain Mapping Rules

- **Propose-Validate-Confirm**: AI proposes domain groupings → Validate aggregate roots → Human confirms
- **One Aggregate Root**: Each domain MUST have exactly ONE root entity
- **Bounded Contexts**: Entities belong to ONE domain only
- **Explicit Dependencies**: Cross-domain imports must go through barrel exports

## File Naming & Exports

| Rule | Requirement | Enforcement |
|------|-------------|-------------|
| File Names | `kebab-case.ts` | ESLint `check-file` |
| Exports | Named exports ONLY | ESLint `no-default-export` |
| Barrel Exports | Every domain has `index.ts` | Architecture validation |
| Import Depth | NEVER reach into domain internals | ESLint `no-restricted-imports` |

### Barrel Export Pattern

```typescript
// ✅ CORRECT - src/domains/sales/index.ts (PUBLIC API)
export { SalesService } from './sales.service'
export { createDeal, getDealById } from './features/deals'
export type { Deal, DealStatus } from './types'

// ✅ CORRECT - Importing from barrel
import { SalesService, createDeal } from '@/domains/sales'

// ❌ FORBIDDEN - Reaching into internals
import { validateDeal } from '@/domains/sales/features/deals/validation'
```

## Backend Architecture Rules

### Controller + Service Pattern

- **Controllers**: Thin HTTP layer only (validation, auth, response formatting)
- **Services**: ALL business logic lives here
- **Repositories**: Data access abstraction (Prisma wrapped)

```typescript
// Controller - THIN (no business logic)
@Controller('deals')
export class DealsController {
  constructor(private readonly dealsService: DealsService) {}

  @Post()
  async create(@Body() dto: CreateDealDto, @Req() req: AuthenticatedRequest) {
    const validated = CreateDealSchema.parse(dto) // Zod validation
    return this.dealsService.createDeal(validated, req.user.tenantId)
  }
}

// Service - FAT (all business logic)
@Injectable()
export class DealsService {
  async createDeal(data: CreateDealInput, tenantId: string): Promise<Deal> {
    // Business logic, validation, orchestration
  }
}
```

### Tenant Isolation (CRITICAL)

**Every database query MUST include tenant_id filtering.**

```typescript
// ✅ CORRECT - Tenant isolation
async findDeals(tenantId: string) {
  return this.prisma.deal.findMany({
    where: { tenant_id: tenantId } // ALWAYS include
  })
}

// ❌ FORBIDDEN - No tenant isolation
async findDeals() {
  return this.prisma.deal.findMany() // SECURITY VIOLATION
}
```

### Zod Validation (Runtime)

- **All API inputs**: Validate with Zod schemas
- **Schema location**: `src/domains/{domain}/schemas/`
- **Error handling**: Return structured validation errors

```typescript
// src/domains/sales/schemas/deal.schema.ts
import { z } from 'zod'

export const CreateDealSchema = z.object({
  title: z.string().min(1).max(200),
  value: z.number().positive(),
  stageId: z.string().uuid()
})

export type CreateDealInput = z.infer<typeof CreateDealSchema>
```

## Frontend Architecture Rules

### Container + Presentational Pattern

- **Container Components**: Data fetching, state, business logic
- **Presentational Components**: Pure UI, receive props only
- **Domain Mirroring**: Frontend domains MUST match backend domains

```typescript
// Container - Handles data and logic
// src/domains/sales/features/deal-list/deal-list.container.tsx
export function DealListContainer() {
  const { deals, isLoading } = useDeals()
  const handleSelect = (id: string) => { /* logic */ }

  return <DealListView deals={deals} loading={isLoading} onSelect={handleSelect} />
}

// Presentational - Pure UI
// src/domains/sales/features/deal-list/deal-list.view.tsx
interface DealListViewProps {
  deals: Deal[]
  loading: boolean
  onSelect: (id: string) => void
}

export function DealListView({ deals, loading, onSelect }: DealListViewProps) {
  // Pure rendering, no data fetching
}
```

### Content Constants (No Hardcoded Strings)

**UI text MUST be in constants files, never inline.**

```typescript
// ✅ CORRECT - src/domains/sales/content/deal-list.content.ts
export const DEAL_LIST_CONTENT = {
  title: 'Your Deals',
  emptyState: 'No deals yet. Create your first deal to get started.',
  actions: {
    create: 'New Deal',
    export: 'Export to CSV'
  }
} as const

// ✅ CORRECT - Using content constant
<h1>{DEAL_LIST_CONTENT.title}</h1>

// ❌ FORBIDDEN - Hardcoded string
<h1>Your Deals</h1>
```

### Feature Organization

```
src/domains/sales/features/deal-list/
├── index.ts                      # Feature barrel export
├── deal-list.container.tsx       # Container component
├── deal-list.view.tsx            # Presentational component
├── deal-list.hooks.ts            # Feature-specific hooks
├── deal-list.content.ts          # UI text constants
└── deal-list.test.tsx            # Tests
```

## Design System Rules

### Glassmorphism Components

All projects include pre-built glassmorphism components:

- `GlassCard` - Frosted glass container
- `GlassBadge` - Status/tag badges
- `GlassButton` - Primary action button
- `FloatingOrbs` - Animated background

### Color Presets

| Preset | Primary | Use Case |
|--------|---------|----------|
| `creative` | #3b82f6 (Blue) | Consumer/innovative apps |
| `corporate` | #14b8a6 (Teal) | Enterprise/B2B apps |
| `neutral` | #6b7280 (Gray) | Utility/minimal apps |
| `custom` | Client-specified | Brand-specific projects |

### Tailwind Configuration

Generated projects include preconfigured `tailwind.config.js` with:
- Brand colors from design preset
- Glass effect utilities
- Float animation keyframes
- Font family configuration

## Quality Enforcement

### ESLint Rules (Auto-configured)

```javascript
// Enforced via .eslintrc.js
{
  'no-restricted-imports': ['error', {
    patterns: [{
      group: ['@/domains/*/*/**'],
      message: 'Use domain barrel export instead'
    }]
  }],
  'import/no-default-export': 'error',
  'check-file/filename-naming-convention': ['error', {
    '**/*.{ts,tsx}': 'KEBAB_CASE'
  }]
}
```

### Husky Pre-commit Hooks

```bash
# Runs on every commit
npx lint-staged    # Lint staged files
npx tsc --noEmit   # Type check
```

### lint-staged Configuration

```json
{
  "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
  "*.{json,md}": ["prettier --write"]
}
```

## Architecture Validation Checklist

Before scaffolding completes, verify:

- [ ] Each domain has exactly one aggregate root entity
- [ ] No circular dependencies between domains
- [ ] All domains have barrel exports (`index.ts`)
- [ ] Frontend domains mirror backend domains
- [ ] Design preset is valid (creative/corporate/neutral/custom)
- [ ] Tenant isolation pattern documented
- [ ] ESLint and Husky configurations included
- [ ] `.claude/rules/` folder with architecture documentation

## AI Context Injection

Generated projects include AI-readable context:

| File | Purpose |
|------|---------|
| `.claude/rules/backend-architecture.md` | Backend patterns for AI |
| `.claude/rules/frontend-architecture.md` | Frontend patterns for AI |
| `.claude/rules/design-system.md` | UI/design rules for AI |
| `CLAUDE.md` | Quick project reference |
| `.cursorrules` | Cursor IDE integration |
| `PROJECT_CONTEXT.md` | Business context summary |

This ensures AI assistants understand and follow the project's architecture when making changes.