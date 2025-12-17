# Frontend Architecture Guide

**Vivavolt 2.0 - Acquisition-Ready Architecture**

This document defines the architectural patterns and conventions for the frontend codebase. **All developers and AI coding agents must follow these guidelines.**

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Directory Structure](#directory-structure)
3. [Domain Structure](#domain-structure)
4. [Import Rules](#import-rules)
5. [Naming Conventions](#naming-conventions)
6. [Component Patterns](#component-patterns)
7. [Content Constants](#content-constants)
8. [Code Quality Enforcement (Husky)](#code-quality-enforcement-husky)
9. [User Roles & Domain Mapping](#user-roles--domain-mapping)
10. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
11. [Checklist for New Features](#checklist-for-new-features)

---

## Architecture Overview

### Domain-Driven Organization

This codebase is organized by **business domains** rather than technical layers:

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND ARCHITECTURE                     │
│                                                             │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │  Sales  │ │  Leads  │ │   CRM   │ │Reporting│  ...     │
│  │ Domain  │ │ Domain  │ │ Domain  │ │ Domain  │          │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘          │
│       │           │           │           │                │
│       └───────────┴─────┬─────┴───────────┘                │
│                         │                                   │
│              ┌──────────┴──────────┐                       │
│              │       Shared        │                       │
│              │  (Layout, Icons)    │                       │
│              └─────────────────────┘                       │
│                         │                                   │
│              ┌──────────┴──────────┐                       │
│              │    Components/UI    │                       │
│              │  (Design System)    │                       │
│              └─────────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

### Backend Alignment

The frontend domain structure **mirrors the backend exactly**:

| Frontend Domain     | Backend Domain      | Purpose                                |
| ------------------- | ------------------- | -------------------------------------- |
| `domains/sales`     | `domains/sales`     | Calendar, appointments, agents, tasks  |
| `domains/leads`     | `domains/leads`     | Lead management, vendors, import       |
| `domains/crm`       | `domains/crm`       | Pipelines, deals, activities, contacts |
| `domains/d2d`       | `domains/d2d`       | Door-to-door operations                |
| `domains/reporting` | `domains/reporting` | Analytics, KPIs, transactions          |
| `domains/teams`     | `domains/teams`     | Team management, users, profiles       |
| `domains/admin`     | `domains/admin`     | Tenant admin, auth, permissions        |
| `domains/booking`   | `domains/booking`   | Smart booking, scheduling              |

---

## Directory Structure

```
src/
├── domains/                    # Business domain modules
│   ├── d2d/                   # Door-to-Door Canvasser App
│   │   ├── components/
│   │   │   ├── dashboard/     # D2D dashboard & stats
│   │   │   └── leads/         # Duplicate lead handling
│   │   └── index.js           # Barrel export
│   │
│   ├── sales/                 # Sales Agent App
│   │   ├── components/
│   │   │   ├── calendar/      # Appointments & scheduling
│   │   │   ├── tasks/         # Task management
│   │   │   └── dashboard/     # Sales metrics & charts
│   │   └── index.js
│   │
│   ├── crm/                   # CRM Module
│   │   ├── components/
│   │   │   ├── deals/         # Deal kanban & forms
│   │   │   ├── contacts/      # Contact management
│   │   │   ├── companies/     # Company management
│   │   │   └── pipelines/     # Pipeline configuration
│   │   └── index.js
│   │
│   ├── leads/                 # Lead Management
│   │   ├── components/        # Lead tables, forms, imports
│   │   └── index.js
│   │
│   ├── teams/                 # Team Management
│   │   ├── components/        # Team CRUD modals
│   │   └── index.js
│   │
│   ├── admin/                 # Administration
│   │   ├── components/
│   │   │   ├── tenants/       # Multi-tenant management
│   │   │   ├── users/         # User management
│   │   │   └── vendors/       # Vendor configuration
│   │   └── index.js
│   │
│   ├── reporting/             # Analytics & Reports
│   │   ├── components/
│   │   │   ├── d2d/           # D2D-specific reports
│   │   │   ├── sales/         # Sales-specific reports
│   │   │   ├── calls/         # Call analytics
│   │   │   └── shared/        # Cross-domain reports
│   │   └── index.js
│   │
│   ├── booking/               # Smart Booking System
│   │   ├── components/
│   │   │   └── smart-booking/ # Smart booking widget
│   │   ├── hooks/             # Booking-specific hooks
│   │   └── index.js
│   │
│   └── index.js               # Central domain exports
│
├── shared/                    # Cross-cutting infrastructure
│   ├── components/
│   │   ├── layout/            # Header, Sidebar, Layout
│   │   ├── icons/             # Flag icons, shared icons
│   │   ├── map/               # Map-related components
│   │   └── ui/                # Shared UI utilities
│   └── index.js
│
├── components/                # Design system ONLY
│   └── ui/                    # Primitives: Button, Card, Modal, etc.
│
├── app/                       # Next.js App Router (thin wrappers)
├── context/                   # React Context providers
├── hooks/                     # Custom React hooks
├── services/                  # API service layer
├── types/                     # TypeScript types
└── utils/                     # Utility functions
```

---

## Domain Structure

### What is a Domain?

A domain is a **self-contained business module** that encapsulates:

- Components (UI for this business area)
- Hooks (domain-specific data fetching)
- Types (domain-specific types)

### Feature Structure

```
domains/{domain}/
├── components/
│   ├── {feature}/
│   │   ├── feature-name.jsx      # Main component
│   │   ├── feature-helper.jsx    # Helper components
│   │   └── index.js              # Feature barrel
│   └── index.js                  # Components barrel
├── constants/                    # Content constants (UI text)
│   ├── {feature}.content.js      # Feature-specific content
│   └── index.js                  # Constants barrel
├── hooks/                        # Domain-specific hooks
├── types/                        # Domain-specific types
└── index.js                      # Domain barrel
```

### Barrel Export Pattern

```javascript
// domains/sales/components/calendar/index.js
export { CalendarView } from './calendar-view'
export { AppointmentDetailDrawer } from './appointment-detail-drawer'
export { NewAppointmentDrawer } from './new-appointment-drawer'

// domains/sales/constants/index.js
export * from './calendar.content'
export * from './dashboard.content'

// domains/sales/components/index.js
export * from './calendar'
export * from './tasks'
export * from './dashboard'

// domains/sales/index.js
export * from './components'
export * from './constants' // Include content constants in domain barrel
```

---

## Import Rules

### REQUIRED: Import via Barrel Exports

```javascript
// CORRECT - Import from domain's public API
import { CalendarView, AppointmentDetailDrawer } from '@/domains/sales'
import { DealsKanban, ContactsTable } from '@/domains/crm'
import { LeadsTable, UploadLeadsModal } from '@/domains/leads'
import { SmartBookingDrawer, SmartBookingButton } from '@/domains/booking'
import { Header, Sidebar, FlagDE } from '@/shared'
import { Button, Card, Modal } from '@/components/ui'
```

### FORBIDDEN: Internal Path Imports

```javascript
// FORBIDDEN - Never reach into domain internals
import { CalendarView } from '@/domains/sales/components/calendar/calendar-view'

// FORBIDDEN - Legacy locations no longer supported
import { Something } from '@/components/layout/...'
import { Something } from '@/components/dashboard/...'
```

### Dependency Direction

```
app/ (pages) → domains/ → shared/ → components/ui/
                  ↓
              services/
```

**Rules:**

1. Pages import from domains
2. Domains can import from other domains via barrels
3. Domains can import from shared/
4. shared/ can import from components/ui/
5. **NEVER**: components/ui/ importing from domains (circular!)

---

## Naming Conventions

### File Names: kebab-case

```
calendar-view.jsx
appointment-detail-drawer.jsx
lead-details-table.jsx
smart-booking-drawer.jsx
```

### Component Names: PascalCase

```javascript
export function CalendarView() { ... }
export function AppointmentDetailDrawer() { ... }
export function SmartBookingDrawer() { ... }
```

### Exports: Named Exports Only

```javascript
// CORRECT - Named exports in barrels
export { CalendarView } from './calendar-view'
export { AppointmentModal } from './appointment-modal'

// FORBIDDEN - Default exports in barrels
export default CalendarView // NEVER in index.js
```

### Functions: camelCase

```javascript
const handleSubmit = () => { ... }
const fetchAppointments = async () => { ... }
const searchAgents = async () => { ... }
```

---

## Component Patterns

### Container + Presentational

```
Calendar.jsx      - Container (data fetching, auth, state)
CalendarView.jsx  - Presentational (UI only, receives props)
```

**Container (like Backend Controller):**

- Handles authentication context
- Fetches data from services
- Manages state
- Calls services for mutations

**Presentational (like Backend Service):**

- Pure UI rendering
- Receives data via props
- Emits events via callbacks
- No direct service calls

### Example

```javascript
// smart-booking-drawer.jsx (Container)
'use client'
import { useAuth } from '@/hooks/useAuth'
import { useAgentSearch } from '../hooks/use-agent-search'
import { AgentCard } from './agent-card'

export function SmartBookingDrawer({ leadId }) {
  const { user } = useAuth()
  const { agents, loading, searchAgents } = useAgentSearch()

  const handleSearch = params => {
    searchAgents({ ...params, tenantId: user.tenant_id })
  }

  return (
    <div className="smart-booking-drawer">
      <AgentSearchForm onSearch={handleSearch} />
      {agents?.map(agent => (
        <AgentCard key={agent.id} agent={agent} />
      ))}
    </div>
  )
}

// agent-card.jsx (Presentational)
export function AgentCard({ agent, onSelectSlot }) {
  return (
    <div className="agent-card">
      <h3>
        {agent.first_name} {agent.last_name}
      </h3>
      <TimeSlotGrid slots={agent.slots} onSelect={onSelectSlot} />
    </div>
  )
}
```

### Keep Pages Thin

```javascript
// app/user/dashboard/calendar/page.jsx
import { Calendar } from '@/domains/sales'

export default function CalendarPage() {
  return <Calendar />
}
```

---

## Content Constants

### Why Content Constants?

**No hardcoded text in components.** All UI text, labels, and static content should live in structured constant files. This:

1. Makes content easily updatable without touching component logic
2. Enables future CMS/i18n integration (same structure, swap source)
3. Keeps components lightweight and focused on UI logic
4. Allows component reuse with different content

### Content File Structure

```javascript
// domains/sales/constants/calendar.content.js

export const calendarContent = {
  // Page metadata
  meta: {
    title: 'Appointments Calendar',
    description: 'Manage your sales appointments',
  },

  // Empty state
  emptyState: {
    heading: 'No appointments scheduled',
    description: "You don't have any appointments for this period.",
    actionLabel: 'Create Appointment',
  },

  // Error state
  errorState: {
    heading: 'Failed to load appointments',
    description: 'There was an error loading your appointments.',
    retryLabel: 'Try Again',
  },

  // Loading state
  loadingState: {
    message: 'Loading appointments...',
  },

  // Actions/Buttons
  actions: {
    create: 'New Appointment',
    refresh: 'Refresh',
    export: 'Export',
    filter: 'Filter',
  },

  // Field labels
  labels: {
    date: 'Date',
    time: 'Time',
    customer: 'Customer',
    status: 'Status',
  },

  // Table headers
  tableHeaders: {
    date: 'Date',
    customer: 'Customer Name',
    status: 'Status',
    actions: 'Actions',
  },

  // Placeholders
  placeholders: {
    searchCustomer: 'Search for customer...',
    selectDate: 'Select a date',
  },

  // Confirmations
  confirmations: {
    delete: 'Are you sure you want to delete this appointment?',
    cancel: 'Are you sure you want to cancel?',
  },

  // Success messages
  success: {
    created: 'Appointment created successfully',
    updated: 'Appointment updated successfully',
    deleted: 'Appointment deleted successfully',
  },

  // Validation messages
  validation: {
    dateRequired: 'Date is required',
    customerRequired: 'Customer is required',
  },
}
```

### Using Content in Components

```javascript
// domains/sales/components/calendar/calendar-view.jsx
import { Button } from '@/components/ui/button'
import { calendarContent } from '../../constants'

export function CalendarView({ appointments, loading, error, onRefresh, onCreate }) {
  const { meta, emptyState, errorState, loadingState, actions } = calendarContent

  if (loading) return <div>{loadingState.message}</div>

  if (error) {
    return (
      <div>
        <h2>{errorState.heading}</h2>
        <p>{errorState.description}</p>
        <Button onClick={onRefresh}>{errorState.retryLabel}</Button>
      </div>
    )
  }

  if (appointments.length === 0) {
    return (
      <div>
        <h2>{emptyState.heading}</h2>
        <p>{emptyState.description}</p>
        <Button onClick={onCreate}>{emptyState.actionLabel}</Button>
      </div>
    )
  }

  return (
    <div>
      <h1>{meta.title}</h1>
      <Button onClick={onCreate}>{actions.create}</Button>
      <Button onClick={onRefresh}>{actions.refresh}</Button>
      {/* Calendar UI */}
    </div>
  )
}
```

### Content Categories Reference

| Category        | Purpose               | Example Keys                                 |
| --------------- | --------------------- | -------------------------------------------- |
| `meta`          | Page/section metadata | `title`, `description`                       |
| `emptyState`    | No data states        | `heading`, `description`, `actionLabel`      |
| `errorState`    | Error states          | `heading`, `description`, `retryLabel`       |
| `loadingState`  | Loading states        | `message`                                    |
| `actions`       | Button labels         | `create`, `edit`, `delete`, `save`, `cancel` |
| `labels`        | Field labels          | `name`, `email`, `status`, `date`            |
| `tableHeaders`  | Table column headers  | Column names                                 |
| `placeholders`  | Input placeholders    | `search`, `select`, `enter`                  |
| `confirmations` | Confirmation dialogs  | `delete`, `cancel`, `submit`                 |
| `success`       | Success messages      | `created`, `updated`, `deleted`              |
| `validation`    | Validation errors     | `required`, `invalid`, `tooLong`             |

### Future CMS Integration

When ready to make content dynamic, replace hardcoded object with API response:

```javascript
// Before (static)
import { calendarContent } from '../../constants'

// After (dynamic)
const { data: calendarContent } = useFetch('/api/content/calendar')

// Component code stays the same!
const { meta, emptyState, actions } = calendarContent
```

The backend API would return the same structure:

```json
{
  "meta": { "title": "Calendar", "description": "..." },
  "emptyState": { "heading": "No appointments", "description": "..." },
  "actions": { "create": "New Appointment", "refresh": "Refresh" }
}
```

This allows:

- Admin panel to edit content without code changes
- A/B testing different copy
- Multi-language support (i18n)
- Client-specific customization

---

## Code Quality Enforcement (Husky)

### Overview

We use **Husky** + **lint-staged** to enforce code standards before commits. Developers **cannot commit code** that violates our standards.

### What Gets Checked

| Check        | What it does                           |
| ------------ | -------------------------------------- |
| `eslint`     | Enforces code style and catches errors |
| `prettier`   | Formats code consistently              |
| `tsc`        | TypeScript type checking               |
| Import order | Ensures consistent import organization |

### Pre-commit Flow

```
Developer runs: git commit -m "feat: add calendar"
                    ↓
            Husky triggers pre-commit hook
                    ↓
            lint-staged runs on staged files
                    ↓
        ┌───────────────────────────────┐
        │  1. ESLint check              │
        │  2. Prettier format           │
        │  3. TypeScript check          │
        │  4. Auto-fix what's possible  │
        └───────────────────────────────┘
                    ↓
            ┌──────┴──────┐
            │             │
         PASS          FAIL
            │             │
      Commit succeeds   Commit blocked
                          │
                    Developer must fix
                    issues before committing
```

### Configuration Files

```
.husky/
├── pre-commit          # Runs lint-staged before commit
└── commit-msg          # Validates commit message format (optional)

package.json            # lint-staged configuration
.eslintrc.js           # ESLint rules
.prettierrc            # Prettier formatting rules
```

### package.json Scripts

```json
{
  "scripts": {
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "type-check": "tsc --noEmit",
    "prepare": "husky install"
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,css}": ["prettier --write"]
  }
}
```

### Setup Instructions

```bash
# Install dependencies
npm install -D husky lint-staged prettier

# Initialize Husky
npx husky install

# Add pre-commit hook
npx husky add .husky/pre-commit "npx lint-staged"

# Make hook executable
chmod +x .husky/pre-commit
```

### Benefits

1. **Consistent code style** - All code looks the same regardless of author
2. **Catches errors early** - Before they reach code review
3. **Auto-fixes issues** - Formatting is automatic
4. **Enforces standards** - Junior devs can't bypass architecture rules
5. **Clean git history** - No "fix lint" commits

### ESLint Custom Rules (Recommended)

```javascript
// .eslintrc.js - Add rules to enforce our architecture
module.exports = {
  rules: {
    // Enforce barrel imports
    'no-restricted-imports': [
      'error',
      {
        patterns: [
          {
            group: ['@/domains/*/*/**'],
            message: 'Import from domain barrel (@/domains/sales) not internal paths',
          },
        ],
      },
    ],

    // Enforce named exports in index files
    'import/no-default-export': 'error',

    // Enforce kebab-case file names
    'check-file/filename-naming-convention': [
      'error',
      {
        '**/*.{jsx,tsx}': 'KEBAB_CASE',
      },
    ],
  },
}
```

---

## User Roles & Domain Mapping

| Role              | Primary Domain(s)            |
| ----------------- | ---------------------------- |
| D2D_AGENT         | d2d, leads                   |
| SALES_AGENT       | sales, leads, crm, booking   |
| TEAM_LEAD         | d2d, sales, teams, reporting |
| REGIONAL_DIRECTOR | All domains                  |
| TENANT_ADMIN      | All domains + admin          |
| SUPER_ADMIN       | All domains + admin          |

---

## Common Mistakes to Avoid

### 1. Importing from Internal Paths

```javascript
// WRONG
import { CalendarView } from '@/domains/sales/components/calendar/CalendarView'

// CORRECT
import { CalendarView } from '@/domains/sales'
```

### 2. Business Components in components/ui/

```javascript
// WRONG - LeadsTable is business logic
src / components / ui / LeadsTable.jsx

// CORRECT - In its domain
src / domains / leads / components / leads - table.jsx
```

### 3. Default Exports in Barrels

```javascript
// WRONG
export default CalendarView

// CORRECT
export { CalendarView } from './calendar-view'
```

### 4. Cross-Domain Internal Imports

```javascript
// WRONG - Reaching into another domain's internals
import { something } from '@/domains/leads/components/internal/helper'

// CORRECT - Via barrel
import { something } from '@/domains/leads'
```

### 5. PascalCase File Names

```javascript
// WRONG
CalendarView.jsx
AppointmentDetailDrawer.jsx

// CORRECT
calendar - view.jsx
appointment - detail - drawer.jsx
```

### 6. Missing Tenant Context

```javascript
// WRONG - API call without tenant context
const agents = await bookingApi.searchAgents({ leadId })

// CORRECT - Include tenant from auth context
const agents = await bookingApi.searchAgents({ leadId, tenantId: user.tenant_id })
```

---

## Checklist for New Features

Before adding any new feature:

- [ ] Identify the correct domain (matches backend domain)
- [ ] Create component in domain's components folder
- [ ] Use kebab-case for file names
- [ ] Use named exports only (no default exports in index.js)
- [ ] Add barrel exports to all index.js files
- [ ] Follow Container + Presentational pattern
- [ ] **Create content constants file** (`domains/{domain}/constants/{feature}.content.js`)
- [ ] **No hardcoded text in components** - use content constants
- [ ] **Include all states**: empty, error, loading in content
- [ ] Keep pages thin (import from domain, render)
- [ ] Handle all API response formats
- [ ] Include tenant context in API calls
- [ ] Cross-domain calls use barrel imports only

---

## Guidelines Summary

1. **All business logic** → `domains/{domain}/`
2. **UI primitives only** → `components/ui/`
3. **Truly shared utilities** → `shared/`
4. **Pages are thin wrappers** → Import from domains
5. **No backwards dependencies** → Domains never import from pages
6. **Named exports only** → No default exports in barrels
7. **kebab-case files** → PascalCase components
8. **Match backend domains** → Frontend domains mirror backend exactly
9. **Include tenant context** → All API calls scoped to tenant
10. **No hardcoded text** → Use content constants for all UI text

---

## Related Documentation

- Backend `ARCHITECTURE.md` - Backend architecture (mirrors this structure)
- `.claude/CLAUDE.md` - Quick reference for AI agents
- `../../plans/content-constants-architecture.md` - Full content constants documentation
- `../../plans/husky-setup-plan.md` - Husky + lint-staged setup guide
- `../../plans/frontend-legacy-elimination-plan.md` - Migration plan details
