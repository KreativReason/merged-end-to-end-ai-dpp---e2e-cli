# Vivavolt 2.0 Backend Architecture Guide

This document defines the architectural patterns, conventions, and best practices for the Vivavolt 2.0 backend codebase. **All developers and AI coding agents must follow these guidelines.**

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Directory Structure](#directory-structure)
3. [Domain Structure](#domain-structure)
4. [Module Boundary Rules](#module-boundary-rules)
5. [Controller + Service Pattern](#controller--service-pattern)
6. [Security Requirements](#security-requirements)
7. [Data Access Patterns](#data-access-patterns)
8. [Naming Conventions](#naming-conventions)
9. [Import Rules](#import-rules)
10. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
11. [Checklist for New Features](#checklist-for-new-features)

---

## Architecture Overview

### Modular Monolith

The backend is organized as a **Modular Monolith** - a single deployable application with strongly enforced module boundaries.

```
┌─────────────────────────────────────────────────────────────┐
│                    MODULAR MONOLITH                         │
│                    (Single Deployment)                      │
│                                                             │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │  Sales  │ │  Leads  │ │   CRM   │ │Reporting│  ...     │
│  │ Module  │ │ Module  │ │ Module  │ │ Module  │          │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘          │
│       │           │           │           │                │
│       └───────────┴─────┬─────┴───────────┘                │
│                         │                                   │
│              ┌──────────┴──────────┐                       │
│              │   Infrastructure    │                       │
│              │  (GHL, Storage, etc)│                       │
│              └─────────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

### Frontend Alignment

The backend domain structure **mirrors the frontend exactly**:

| Frontend Domain     | Backend Domain      | Purpose                               |
| ------------------- | ------------------- | ------------------------------------- |
| `domains/sales`     | `domains/sales`     | Calendar, appointments, agents, tasks |
| `domains/leads`     | `domains/leads`     | Lead management, vendors              |
| `domains/crm`       | `domains/crm`       | Pipelines, deals, activities          |
| `domains/d2d`       | `domains/d2d`       | Door-to-door operations               |
| `domains/reporting` | `domains/reporting` | Analytics, KPIs, transactions         |
| `domains/teams`     | `domains/teams`     | Team management, users, profiles      |
| `domains/admin`     | `domains/admin`     | Tenant admin, auth, permissions       |
| `domains/booking`   | `domains/booking`   | Booking, smart-booking                |

---

## Directory Structure

```
src/
├── domains/                      # Business modules (mirrors frontend)
│   ├── sales/                   # Calendar, appointments, agents, tasks
│   │   ├── index.ts             # Barrel export: export * from './features'
│   │   └── features/
│   │       ├── index.ts
│   │       ├── appointments/
│   │       │   ├── index.ts
│   │       │   ├── appointments.controller.ts
│   │       │   ├── appointments.service.ts
│   │       │   └── appointments.schema.ts
│   │       ├── agents/
│   │       ├── calendar/
│   │       └── tasks/
│   │
│   ├── leads/                   # Lead management, vendors
│   │   └── features/
│   │       ├── lead/
│   │       ├── vendor/
│   │       └── import/
│   │
│   ├── crm/                     # Pipelines, deals, activities (BLUEPRINT)
│   │   └── features/
│   │       ├── pipeline/
│   │       ├── deal/
│   │       ├── activity/
│   │       └── contact/
│   │
│   ├── reporting/               # KPIs, transactions
│   │   └── features/
│   │       ├── kpi/
│   │       ├── transactions/
│   │       └── agent-performance/
│   │
│   ├── teams/                   # Team management, users
│   │   └── features/
│   │       ├── team/
│   │       ├── users/
│   │       └── profile/
│   │
│   ├── admin/                   # Tenant admin, auth
│   │   └── features/
│   │       ├── tenants/
│   │       ├── auth/
│   │       └── permission/
│   │
│   ├── booking/                 # Booking features
│   │   └── features/
│   │       ├── booking/
│   │       └── smart-booking/
│   │
│   └── d2d/                     # Door-to-door
│
├── infrastructure/              # External services & integrations
│   ├── integrations/
│   │   ├── ghl/                # GoHighLevel CRM
│   │   │   ├── ghl.service.ts
│   │   │   └── index.ts
│   │   └── reonic/             # Reonic solar platform
│   │       ├── reonic.service.ts
│   │       └── index.ts
│   ├── storage/                # Google Cloud Storage, audio uploads
│   │   ├── google-cloud-storage.service.ts
│   │   ├── audio-upload.service.ts
│   │   └── index.ts
│   ├── email/                  # Email service & templates
│   │   ├── email.service.ts
│   │   ├── templates/
│   │   └── index.ts
│   ├── webhooks/               # Webhook processing
│   │   ├── webhook.service.ts
│   │   ├── webhook.controller.ts
│   │   └── index.ts
│   ├── sync/                   # Multi-process synchronization
│   │   ├── multi-process-sync.service.ts
│   │   └── index.ts
│   └── index.ts
│
├── middleware/                  # Express middleware
│   ├── auth.middleware.ts
│   ├── permission.middleware.ts
│   └── index.ts
│
├── routes/                      # Express route definitions
├── validators/                  # Zod schemas
├── utils/                       # Utility functions
├── models/                      # Data models
├── cron/                        # Scheduled jobs
├── workers/                     # Background workers
└── index.ts                     # Application entry point
```

---

## Domain Structure

### What is a Domain?

A domain is a **self-contained business module** that encapsulates:

- Controllers (request handling)
- Services (business logic)
- Schemas (validation)
- Types/interfaces

### Feature Structure

Each feature within a domain follows this pattern:

```
domains/{domain}/features/{feature}/
├── index.ts                    # Barrel export
├── {feature}.controller.ts     # HTTP request handling
├── {feature}.service.ts        # Business logic
├── {feature}.schema.ts         # Zod validation schemas
└── {feature}.types.ts          # TypeScript types (optional)
```

### Barrel Export Pattern

```typescript
// domains/sales/features/appointments/index.ts
export { AppointmentsService } from './appointments.service'
export * as appointmentsController from './appointments.controller'
export type { CreateAppointmentInput, AppointmentFilters } from './appointments.types'

// domains/sales/features/index.ts
export * from './appointments'
export * from './agents'
export * from './calendar'
export * from './tasks'

// domains/sales/index.ts
export * from './features'
```

---

## Module Boundary Rules

### Rule 1: Import via barrel exports ONLY

```typescript
// CORRECT - Import from domain's public API
import { AppointmentsService } from '@/domains/sales'
import { LeadService } from '@/domains/leads'

// FORBIDDEN - Never reach into module internals
import { AppointmentsService } from '@/domains/sales/features/appointments/appointments.service'
```

### Rule 2: No circular dependencies

```typescript
// If sales depends on leads, leads CANNOT depend on sales
// Plan dependency direction carefully
```

### Rule 3: Domains own their database tables

```typescript
// Only leads domain writes to leads table
// Other domains READ via leads domain's public API

// In domains/sales/features/appointments/appointments.service.ts
import { LeadService } from '@/domains/leads';  // Cross-module read

// FORBIDDEN: Direct DB access to another domain's table
prisma.lead.findUnique({ ... });  // NO! Use LeadService instead
```

### Rule 4: Direct function calls (no events)

```typescript
// Modular monolith = same process = just call functions
import { LeadService } from '@/domains/leads'

await LeadService.updateLeadStatus(leadId, 'qualified', tenantId)

// No EventEmitter, no message queue - keep it simple
```

---

## Controller + Service Pattern

This pattern mirrors the frontend's **Container + Presentational** pattern.

### Controller (like Container)

- Handles HTTP request/response
- Authentication/authorization
- Input validation with Zod
- Calls services for business logic
- **Never contains business logic**

### Service (like Presentational)

- Pure business logic
- Receives parameters (never reads from `req`)
- Returns data
- Database operations
- Cross-module calls

### Example

```typescript
// domains/sales/features/appointments/appointments.controller.ts
import { Router } from 'express'
import { authenticate } from '@/middleware/auth.middleware'
import { requirePermission } from '@/middleware/permission.middleware'
import { createAppointmentSchema } from './appointments.schema'
import { AppointmentsService } from './appointments.service'

const router = Router()
router.use(authenticate)

export const create = [
  requirePermission('booking.create'),
  async (req, res, next) => {
    try {
      const tenantId = req.user!.tenant_id
      const data = createAppointmentSchema.parse(req.body)

      const appointment = await AppointmentsService.create({
        ...data,
        tenantId,
      })

      res.status(201).json({ success: true, data: appointment })
    } catch (error) {
      next(error)
    }
  },
]

export const list = [
  requirePermission('booking.view'),
  async (req, res, next) => {
    try {
      const tenantId = req.user!.tenant_id
      const appointments = await AppointmentsService.list(tenantId, req.query)
      res.json({ success: true, data: appointments })
    } catch (error) {
      next(error)
    }
  },
]
```

```typescript
// domains/sales/features/appointments/appointments.service.ts
import { prisma } from '@/infrastructure/database/prisma'

export interface CreateAppointmentData {
  tenantId: number
  leadId: number
  userId: number
  scheduledAt: Date
}

export class AppointmentsService {
  static async create(data: CreateAppointmentData) {
    return prisma.appointment.create({
      data: {
        tenant_id: data.tenantId, // ALWAYS include tenant_id
        lead_id: data.leadId,
        assigned_to: data.userId,
        scheduled_at: data.scheduledAt,
        status: 'scheduled',
      },
    })
  }

  static async list(tenantId: number, filters?: AppointmentFilters) {
    return prisma.appointment.findMany({
      where: {
        tenant_id: tenantId, // ALWAYS include tenant_id
        ...filters,
      },
    })
  }
}
```

```typescript
// domains/sales/features/appointments/appointments.schema.ts
import { z } from 'zod'

export const createAppointmentSchema = z.object({
  leadId: z.number().int().positive(),
  userId: z.number().int().positive(),
  scheduledAt: z.coerce.date(),
})

export type CreateAppointmentInput = z.infer<typeof createAppointmentSchema>
```

---

## Security Requirements

### 1. Authentication on ALL routes

```typescript
router.use(authenticate) // REQUIRED on every domain router
```

### 2. Permission checks on endpoints

```typescript
router.get('/leads', requirePermission('leads.view'), ...);
router.post('/leads', requirePermission('leads.create'), ...);
router.put('/leads/:id', requirePermission('leads.update'), ...);
router.delete('/leads/:id', requirePermission('leads.delete'), ...);
```

### 3. Tenant isolation in ALL queries

```typescript
// EVERY database query must include tenant_id
prisma.lead.findMany({
  where: {
    tenant_id: tenantId, // MANDATORY
    status: 'new',
  },
})

// NEVER do this - SECURITY VULNERABILITY
prisma.lead.findMany({ where: { status: 'new' } }) // Missing tenant_id!
```

### 4. Input validation with Zod

```typescript
import { z } from 'zod'

const createLeadSchema = z.object({
  firstName: z.string().min(1).max(100),
  lastName: z.string().min(1).max(100),
  email: z.string().email(),
  phone: z.string().optional(),
})

// In controller - ALWAYS validate before using
const data = createLeadSchema.parse(req.body)
```

---

## Data Access Patterns

### Standard Response Format

```typescript
// Success with single item
return { success: true, data: result }

// Success with list
return { success: true, data: items, total: count }

// Error (use AppError class)
throw new AppError('Lead not found', 404)
```

### Pagination

```typescript
export async function listLeads(tenantId: number, options: PaginationOptions) {
  const { page = 1, limit = 20 } = options
  const skip = (page - 1) * limit

  const [data, total] = await Promise.all([
    prisma.lead.findMany({
      where: { tenant_id: tenantId },
      skip,
      take: limit,
      orderBy: { created_at: 'desc' },
    }),
    prisma.lead.count({ where: { tenant_id: tenantId } }),
  ])

  return { data, total, page, limit }
}
```

### Cross-Module Communication

```typescript
// domains/sales/features/appointments/appointments.service.ts
import { LeadService } from '@/domains/leads'

export async function completeAppointment(
  appointmentId: number,
  outcome: string,
  tenantId: number
) {
  const appointment = await prisma.appointment.update({
    where: { id: appointmentId, tenant_id: tenantId },
    data: { status: 'completed', outcome },
  })

  // Cross-module call via barrel export
  if (outcome === 'qualified') {
    await LeadService.updateLeadStatus(appointment.lead_id, 'qualified', tenantId)
  }

  return appointment
}
```

---

## Naming Conventions

### File Names: kebab-case

```
appointment-duration.controller.ts
calendar-events.service.ts
lead-tunnel-data-processor.service.ts
```

### Exports: Named exports only (NO default exports)

```typescript
// CORRECT - Named exports
export const appointmentsController = { ... };
export { AppointmentsService } from './appointments.service';
export class LeadService { ... }

// FORBIDDEN - Default exports
export default appointmentsController;  // NEVER
export default class LeadService { }    // NEVER
```

### Classes: PascalCase

```typescript
export class LeadService { ... }
export class VendorController { ... }
```

### Functions: camelCase

```typescript
export function getAgentsWithSlots() { ... }
export function createAppointment() { ... }
```

### Variables: camelCase

```typescript
const tenantId = req.user.tenant_id;
const appointmentData = { ... };
```

---

## Import Rules

### Allowed Imports

```typescript
// Domain imports from other domains via barrel
import { LeadService } from '@/domains/leads'
import { AgentService, AppointmentsService } from '@/domains/sales'

// Domain imports from infrastructure
import { GHLService } from '@/infrastructure/integrations/ghl'
import { EmailService } from '@/infrastructure/email'
import { uploadBuffer } from '@/infrastructure/storage'

// Domain imports from middleware/utils
import { authenticate } from '@/middleware'
import { AppError } from '@/utils/error'

// Internal feature imports (within same domain)
import { AppointmentsService } from './appointments.service'
```

### Forbidden Imports

```typescript
// NEVER import internal domain files from outside
import { LeadService } from '@/domains/leads/features/lead/lead.service' // WRONG!

// NEVER import from old legacy paths
import { LeadService } from '@/services/lead.service' // WRONG - path doesn't exist!
```

### Dependency Direction

```
routes → domains → infrastructure
            ↓
    middleware/utils
```

---

## Common Mistakes to Avoid

### 1. Missing tenant_id in queries

```typescript
// WRONG - Security vulnerability!
prisma.lead.findMany({ where: { status: 'new' } })

// CORRECT
prisma.lead.findMany({ where: { tenant_id: tenantId, status: 'new' } })
```

### 2. Business logic in controllers

```typescript
// WRONG
router.post('/', async (req, res) => {
  const lead = await prisma.lead.create({ data: req.body });
  if (lead.status === 'qualified') {
    await prisma.appointment.create({ ... });  // Business logic in controller!
  }
});

// CORRECT
router.post('/', async (req, res) => {
  const data = createLeadSchema.parse(req.body);
  const lead = await LeadService.create(data, req.user.tenant_id);
  res.status(201).json({ success: true, data: lead });
});
```

### 3. Skipping input validation

```typescript
// WRONG - Trusting raw input
const lead = await LeadService.create(req.body, tenantId)

// CORRECT - Validate first
const data = createLeadSchema.parse(req.body)
const lead = await LeadService.create(data, tenantId)
```

### 4. Using default exports

```typescript
// WRONG
export default class LeadService { }
export default leadController;

// CORRECT
export class LeadService { }
export const leadController = { ... };
```

### 5. Missing authentication

```typescript
// WRONG
router.get('/leads', async (req, res) => { ... });

// CORRECT
router.use(authenticate);
router.get('/leads', requirePermission('leads.view'), async (req, res) => { ... });
```

### 6. Importing from internal paths

```typescript
// WRONG
import { LeadService } from '@/domains/leads/features/lead/lead.service'

// CORRECT
import { LeadService } from '@/domains/leads'
```

---

## Checklist for New Features

Before adding any new feature:

- [ ] Identify the correct domain (matches frontend domain)
- [ ] Create feature folder with controller, service, schema, index.ts
- [ ] Use kebab-case for file names
- [ ] Use named exports only (no default exports)
- [ ] Add barrel exports to all index.ts files
- [ ] Include `authenticate` middleware on router
- [ ] Add `requirePermission()` on each endpoint
- [ ] Include `tenant_id` in ALL database queries
- [ ] Validate input with Zod schemas
- [ ] Use standard response format `{ success: true, data: ... }`
- [ ] Cross-module calls use barrel imports only
- [ ] No direct database access to other domains' tables

---

## Blueprint: CRM Domain

The CRM domain (`src/domains/crm/`) is fully modular and serves as the **reference implementation**:

```
domains/crm/
├── index.ts                  # export * from './features'
└── features/
    ├── index.ts              # Exports all features
    ├── pipeline/
    │   ├── index.ts
    │   ├── pipeline.service.ts
    │   └── pipeline.controller.ts
    ├── deal/
    │   ├── index.ts
    │   ├── deal.service.ts
    │   └── deal.controller.ts
    ├── activity/
    │   ├── index.ts
    │   ├── activity.service.ts
    │   └── activity.controller.ts
    └── contact/
        ├── index.ts
        ├── contact.service.ts
        └── contact.controller.ts
```

**When in doubt, follow the CRM domain patterns.**

---

## AI Coding Agent Instructions

If you are an AI coding assistant working on this codebase:

1. **Read this file first** before making any changes
2. **Never skip tenant_id** in database queries - this is a security requirement
3. **Always add authentication** to new routes
4. **Use barrel exports** - never import internal module files
5. **Follow CRM as blueprint** - it shows the correct patterns
6. **Keep controllers thin** - business logic goes in services
7. **Validate all input** with Zod schemas
8. **Use kebab-case** for file names
9. **Use named exports only** - no default exports
10. **Match frontend domains** - if unsure which domain, check the frontend

---

## Related Documentation

- `CLAUDE.md` - Quick reference for AI agents
- `MIGRATION_GUIDE.md` - Import patterns reference
- Frontend `ARCHITECTURE.md` - Frontend architecture (mirrors this structure)
