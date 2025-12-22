# KreativReason Full-Stack Development Guide

## Production-Grade SaaS Architecture

**Version 3.0** — Complete full-stack patterns for building multi-million dollar applications.

This guide is designed for AI agents (Claude Code, Cursor, Copilot) and developers building production-grade SaaS applications. It covers **both backend and frontend** with equal depth.

---

## Table of Contents

### Part 1: Philosophy & Principles
1. [Core Philosophy](#core-philosophy)
2. [The 10 Commandments](#the-10-commandments)
3. [Stack Overview](#stack-overview)

### Part 2: Architecture
4. [Project Structure](#project-structure)
5. [Domain-First Organization](#domain-first-organization)
6. [Frontend/Backend Alignment](#frontendbackend-alignment)

### Part 3: Backend — Domain Layer
7. [Rich Domain Models](#rich-domain-models)
8. [State as Records](#state-as-records)
9. [Domain Model Template](#domain-model-template)

### Part 4: Backend — Data Layer
10. [Database Patterns](#database-patterns)
11. [Prisma Conventions](#prisma-conventions)
12. [Multi-Tenancy](#multi-tenancy)

### Part 5: Backend — API Layer
13. [CRUD Routing Philosophy](#crud-routing-philosophy)
14. [Controller Patterns](#controller-patterns)
15. [API Response Standards](#api-response-standards)
16. [Error Handling](#error-handling)
17. [Validation with Zod](#validation-with-zod)

### Part 6: Frontend — Core Patterns
18. [Server vs Client Components](#server-vs-client-components)
19. [Data Fetching Patterns](#data-fetching-patterns)
20. [Server Actions](#server-actions)
21. [Loading & Error States](#loading--error-states)

### Part 7: Frontend — Components
22. [Component Architecture](#component-architecture)
23. [Container + Presentational](#container--presentational)
24. [Content Constants](#content-constants)
25. [UI Component Patterns](#ui-component-patterns)

### Part 8: Frontend — Forms
26. [Form Architecture](#form-architecture)
27. [React Hook Form + Zod](#react-hook-form--zod)
28. [Server Action Forms](#server-action-forms)
29. [Optimistic Updates](#optimistic-updates)

### Part 9: Frontend — State & Data
30. [State Management](#state-management)
31. [API Client](#api-client)
32. [Caching Strategies](#caching-strategies)

### Part 10: Quality & Testing
33. [TypeScript Standards](#typescript-standards)
34. [Backend Testing](#backend-testing)
35. [Frontend Testing](#frontend-testing)

### Part 11: Operations
36. [Performance Patterns](#performance-patterns)
37. [API Cost Optimization](#api-cost-optimization)
38. [Background Jobs](#background-jobs)
39. [Authentication](#authentication)
40. [Security Checklist](#security-checklist)

### Part 12: Reference
41. [Naming Conventions](#naming-conventions)
42. [Import Rules](#import-rules)
43. [What to Avoid](#what-to-avoid)
44. [Checklists](#checklists)

---

# Part 1: Philosophy & Principles

## Core Philosophy

**"Vanilla frameworks are plenty."**

We maximize what Next.js/Express/Prisma give us out of the box, minimize dependencies, and resist abstractions until absolutely necessary.

### The KreativReason Way

1. **Rich domain models** over anemic services
2. **CRUD routes** over custom endpoints
3. **Records as state** over boolean columns
4. **Server Components first** — client components only when needed
5. **Server Actions for mutations** — no API routes for forms
6. **Database-backed everything** (minimize Redis complexity)
7. **Build before npm install** (< 1 day to build? Do it yourself)
8. **TypeScript strictly** — no `any`, no escape hatches
9. **Tenant isolation always** — every query scoped
10. **Test the domain** — business logic is what matters

---

## The 10 Commandments

### 1. Thou Shalt Use Rich Domain Models

```typescript
// ❌ ANEMIC (just a Prisma wrapper)
export async function shipOrder(id: string) {
  return prisma.order.update({ where: { id }, data: { isShipped: true } })
}

// ✅ RICH (encapsulates business logic)
export class Order {
  async ship(opts: { shippedById: string; trackingNumber: string }) {
    if (this.isShipped) throw new AppError('Already shipped', 400)
    if (!this.isPaid) throw new AppError('Cannot ship unpaid order', 400)

    await prisma.$transaction([
      prisma.orderShipment.create({ data: { orderId: this.id, ...opts } }),
      prisma.orderEvent.create({ data: { orderId: this.id, action: 'shipped' } }),
    ])
    await this.reload()
  }
}
```

### 2. Thou Shalt Use State as Records

```prisma
// ❌ BOOLEAN HELL
model Order {
  isShipped Boolean @default(false)
}

// ✅ STATE RECORDS
model OrderShipment {
  id             String   @id @default(cuid())
  orderId        String   @unique
  shippedById    String   // WHO
  trackingNumber String   // DETAILS
  createdAt      DateTime // WHEN
}
```

### 3. Thou Shalt Use Server Components by Default

```typescript
// ❌ WRONG - Client component for static content
'use client'
export function OrderList({ orders }) {
  return <ul>{orders.map(o => <li key={o.id}>{o.name}</li>)}</ul>
}

// ✅ CORRECT - Server component (default)
export function OrderList({ orders }) {
  return <ul>{orders.map(o => <li key={o.id}>{o.name}</li>)}</ul>
}
```

### 4. Thou Shalt Use Server Actions for Mutations

```typescript
// ❌ WRONG - API route + fetch for form submission
// app/api/orders/route.ts
export async function POST(req) { ... }
// component
const res = await fetch('/api/orders', { method: 'POST', body: ... })

// ✅ CORRECT - Server Action
// actions/orders.ts
'use server'
export async function createOrder(formData: FormData) {
  const data = createOrderSchema.parse(Object.fromEntries(formData))
  return Order.create(data, tenantId, userId)
}
// component
<form action={createOrder}>
```

### 5. Thou Shalt Isolate Tenants

```typescript
// ❌ SECURITY BREACH
prisma.order.findMany({ where: { status: 'pending' } })

// ✅ ALWAYS INCLUDE TENANT
prisma.order.findMany({ where: { tenantId, status: 'pending' } })
```

### 6. Thou Shalt Route Everything as CRUD

```typescript
// ❌ CUSTOM VERBS
POST /api/orders/:id/ship

// ✅ CRUD RESOURCES
POST /api/orders/:id/shipment   // Create shipment record
```

### 7. Thou Shalt Keep Controllers/Actions Thin

```typescript
// ❌ BUSINESS LOGIC IN ACTION
'use server'
export async function shipOrder(orderId: string) {
  const order = await prisma.order.findUnique({ where: { id: orderId } })
  if (!order.isPaid) throw new Error('Not paid')
  await prisma.order.update({ ... })
  await prisma.event.create({ ... })
  // 20 more lines...
}

// ✅ THIN ACTION, RICH MODEL
'use server'
export async function shipOrder(orderId: string, formData: FormData) {
  const user = await getCurrentUser()
  const data = shipOrderSchema.parse(Object.fromEntries(formData))
  const order = await Order.findById(orderId, user.tenantId)
  await order.ship({ shippedById: user.id, ...data })
  revalidatePath('/orders')
  return { success: true }
}
```

### 8. Thou Shalt Validate All Input

```typescript
// ❌ TRUSTING RAW INPUT
const order = await Order.create(formData)

// ✅ VALIDATE FIRST
const data = createOrderSchema.parse(Object.fromEntries(formData))
const order = await Order.create(data, tenantId, userId)
```

### 9. Thou Shalt Never Query in Loops

```typescript
// ❌ N+1 DISASTER
for (const order of orders) {
  const customer = await prisma.customer.findFirst({ where: { id: order.customerId } })
}

// ✅ BATCH OPERATIONS
const customers = await prisma.customer.findMany({ where: { id: { in: customerIds } } })
const customerMap = new Map(customers.map(c => [c.id, c]))
```

### 10. Thou Shalt Use Named Exports Only

```typescript
// ❌ DEFAULT EXPORTS
export default function OrderList() { }
export default orderController

// ✅ NAMED EXPORTS
export function OrderList() { }
export const orderController = { ... }
```

---

## Stack Overview

### Backend Options

**Option A: Separate Express Backend**
```
Backend:  Express + Prisma + PostgreSQL + Zod
Frontend: Next.js 14 (App Router) + React + Tailwind
```

**Option B: Next.js Full-Stack**
```
Full-Stack: Next.js 14 (App Router) + Prisma + PostgreSQL + Zod + Server Actions
```

### What We Use

| Category | Technology | Why |
|----------|-----------|-----|
| Framework | Next.js 14+ (App Router) | Best React framework, RSC |
| Backend | Express or Next.js API/Actions | Simple, battle-tested |
| Database | PostgreSQL + Prisma | Type-safe, great DX |
| Validation | Zod | Runtime + TypeScript types |
| Styling | Tailwind CSS | Utility-first, fast |
| Components | shadcn/ui | Customizable, not a dependency |
| Forms | react-hook-form + Zod | Best combo |
| Testing | Vitest + Testing Library | Fast, modern |

### What We Avoid

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| NextAuth | Over-engineered | Custom JWT (~200 lines) |
| Redux, Zustand | RSC makes it unnecessary | URL state + Context |
| TanStack Query | RSC + Server Actions enough | Native patterns |
| tRPC | Adds complexity | Server Actions + Zod |
| GraphQL | REST is plenty | REST API |
| Lodash | Native JS is enough | Native methods |

---

# Part 2: Architecture

## Project Structure

### Full-Stack Next.js Project

```
src/
├── app/                          # Next.js App Router
│   ├── (auth)/                   # Auth route group (no layout)
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── signup/
│   │       └── page.tsx
│   │
│   ├── (dashboard)/              # Dashboard route group (shared layout)
│   │   ├── layout.tsx            # Dashboard layout with sidebar
│   │   ├── page.tsx              # Dashboard home
│   │   ├── orders/
│   │   │   ├── page.tsx          # List (Server Component)
│   │   │   ├── loading.tsx       # Loading state
│   │   │   ├── error.tsx         # Error boundary
│   │   │   ├── [id]/
│   │   │   │   ├── page.tsx      # Detail view
│   │   │   │   └── edit/
│   │   │   │       └── page.tsx  # Edit form
│   │   │   └── new/
│   │   │       └── page.tsx      # Create form
│   │   ├── customers/
│   │   └── settings/
│   │
│   ├── api/                      # API Routes (webhooks, external APIs only)
│   │   └── webhooks/
│   │       └── stripe/
│   │           └── route.ts
│   │
│   ├── layout.tsx                # Root layout
│   ├── loading.tsx               # Global loading
│   ├── error.tsx                 # Global error
│   └── not-found.tsx             # 404 page
│
├── domains/                      # Business logic (shared FE/BE)
│   ├── orders/
│   │   ├── models/
│   │   │   ├── Order.ts          # Rich domain model
│   │   │   ├── Order.schema.ts   # Zod schemas
│   │   │   └── Order.queries.ts  # Prisma includes
│   │   ├── actions/
│   │   │   └── order.actions.ts  # Server Actions
│   │   ├── components/
│   │   │   ├── OrderList.tsx
│   │   │   ├── OrderListView.tsx
│   │   │   ├── OrderForm.tsx
│   │   │   ├── OrderDetails.tsx
│   │   │   └── index.ts
│   │   ├── constants/
│   │   │   └── order.content.ts
│   │   ├── hooks/
│   │   │   └── useOrderForm.ts
│   │   └── index.ts              # Barrel export
│   │
│   ├── customers/
│   ├── auth/
│   └── index.ts
│
├── components/                   # Shared UI components
│   └── ui/                       # Design system (shadcn/ui)
│       ├── button.tsx
│       ├── card.tsx
│       ├── form.tsx
│       ├── input.tsx
│       ├── table.tsx
│       ├── dialog.tsx
│       ├── toast.tsx
│       └── index.ts
│
├── shared/                       # Cross-cutting concerns
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   ├── ErrorBoundary.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── EmptyState.tsx
│   └── index.ts
│
├── lib/                          # Utilities
│   ├── prisma.ts                 # Prisma client
│   ├── auth.ts                   # Auth utilities
│   ├── api.ts                    # API client (for external APIs)
│   ├── errors.ts                 # Error classes
│   ├── utils.ts                  # General utilities
│   └── validations.ts            # Shared Zod schemas
│
├── hooks/                        # Global React hooks
│   ├── useAuth.ts
│   ├── useToast.ts
│   └── useDebounce.ts
│
├── context/                      # React Context providers
│   ├── AuthContext.tsx
│   └── ToastContext.tsx
│
├── types/                        # Global TypeScript types
│   ├── auth.ts
│   └── api.ts
│
└── styles/
    └── globals.css
```

### Separate Backend (Express)

```
backend/
├── src/
│   ├── domains/
│   │   └── orders/
│   │       ├── models/
│   │       │   └── Order.ts
│   │       ├── features/
│   │       │   ├── order/
│   │       │   │   ├── order.controller.ts
│   │       │   │   ├── order.schema.ts
│   │       │   │   └── index.ts
│   │       │   └── index.ts
│   │       └── index.ts
│   ├── infrastructure/
│   ├── middleware/
│   ├── lib/
│   └── routes/
│
frontend/
├── src/
│   ├── app/
│   ├── domains/           # Frontend-only (components, hooks)
│   ├── components/
│   ├── lib/
│   │   └── api.ts         # API client to call backend
│   └── hooks/
```

---

## Domain-First Organization

### What is a Domain?

A domain is a **self-contained business module** that owns:
- Its data models (Prisma schema, domain classes)
- Its business logic (domain model methods)
- Its server actions (mutations)
- Its UI components (React components)
- Its validation schemas (Zod)
- Its content constants (UI text)

### Domain Structure

```
domains/{domain}/
├── models/                    # Backend logic
│   ├── {Model}.ts            # Rich domain model
│   ├── {Model}.schema.ts     # Zod schemas
│   └── {Model}.queries.ts    # Prisma includes
├── actions/                   # Server Actions
│   └── {model}.actions.ts
├── components/                # React components
│   ├── {Model}List.tsx       # Container
│   ├── {Model}ListView.tsx   # Presentational
│   ├── {Model}Form.tsx       # Form component
│   ├── {Model}Details.tsx    # Detail view
│   └── index.ts
├── constants/
│   └── {model}.content.ts    # UI text
├── hooks/
│   └── use{Model}Form.ts     # Form hooks
└── index.ts                   # Barrel export
```

---

# Part 3: Backend — Domain Layer

## Rich Domain Models

This is the **most important pattern** in the entire guide.

### Structure

```typescript
// domains/orders/models/Order.ts

import { prisma } from '@/lib/prisma'
import { AppError, NotFoundError } from '@/lib/errors'
import { orderWithRelations, type OrderWithRelations } from './Order.queries'
import type { CreateOrderInput, ShipOrderInput } from './Order.schema'

export class Order {
  constructor(private data: OrderWithRelations) {}

  // ═══════════════════════════════════════════════════════════════
  // FACTORY METHODS
  // ═══════════════════════════════════════════════════════════════

  static async findById(id: string, tenantId: string): Promise<Order> {
    const data = await prisma.order.findFirst({
      where: { id, tenantId },
      include: orderWithRelations,
    })
    if (!data) throw new NotFoundError('Order')
    return new Order(data)
  }

  static async findByIdOrNull(id: string, tenantId: string): Promise<Order | null> {
    const data = await prisma.order.findFirst({
      where: { id, tenantId },
      include: orderWithRelations,
    })
    return data ? new Order(data) : null
  }

  static async create(
    input: CreateOrderInput,
    tenantId: string,
    createdById: string
  ): Promise<Order> {
    const number = await this.getNextNumber(tenantId)

    const data = await prisma.order.create({
      data: {
        ...input,
        number,
        tenantId,
        createdById,
      },
      include: orderWithRelations,
    })

    await prisma.orderEvent.create({
      data: {
        orderId: data.id,
        action: 'created',
        createdById,
      },
    })

    return new Order(data)
  }

  static async list(tenantId: string, options: ListOptions = {}) {
    const { page = 1, limit = 20, status, search } = options
    const skip = (page - 1) * limit

    const where = {
      tenantId,
      ...(status && { status }),
      ...(search && {
        OR: [
          { number: { contains: search } },
          { customer: { name: { contains: search, mode: 'insensitive' } } },
        ],
      }),
    }

    const [data, total] = await prisma.$transaction([
      prisma.order.findMany({
        where,
        include: orderWithRelations,
        skip,
        take: limit,
        orderBy: { createdAt: 'desc' },
      }),
      prisma.order.count({ where }),
    ])

    return {
      data: data.map(d => new Order(d)),
      total,
      page,
      limit,
      totalPages: Math.ceil(total / limit),
    }
  }

  private static async getNextNumber(tenantId: string): Promise<number> {
    const last = await prisma.order.findFirst({
      where: { tenantId },
      orderBy: { number: 'desc' },
      select: { number: true },
    })
    return (last?.number ?? 0) + 1
  }

  // ═══════════════════════════════════════════════════════════════
  // GETTERS
  // ═══════════════════════════════════════════════════════════════

  get id() { return this.data.id }
  get number() { return this.data.number }
  get status() { return this.data.status }
  get total() { return this.data.total }
  get tenantId() { return this.data.tenantId }
  get customer() { return this.data.customer }
  get items() { return this.data.items }
  get createdAt() { return this.data.createdAt }

  // ═══════════════════════════════════════════════════════════════
  // STATE PREDICATES
  // ═══════════════════════════════════════════════════════════════

  get isPaid(): boolean {
    return this.data.payment !== null
  }

  get isShipped(): boolean {
    return this.data.shipment !== null
  }

  get isCancelled(): boolean {
    return this.data.cancellation !== null
  }

  get isOpen(): boolean {
    return !this.isShipped && !this.isCancelled
  }

  get canShip(): boolean {
    return this.isPaid && !this.isShipped && !this.isCancelled
  }

  get canCancel(): boolean {
    return !this.isShipped && !this.isCancelled
  }

  // ═══════════════════════════════════════════════════════════════
  // STATE TRANSITIONS
  // ═══════════════════════════════════════════════════════════════

  async pay(options: {
    paidById: string
    method: 'card' | 'bank' | 'cash'
    transactionId?: string
  }): Promise<void> {
    if (this.isPaid) {
      throw new AppError('Order is already paid', 400, 'ALREADY_PAID')
    }
    if (this.isCancelled) {
      throw new AppError('Cannot pay a cancelled order', 400, 'ORDER_CANCELLED')
    }

    await prisma.$transaction([
      prisma.orderPayment.create({
        data: {
          orderId: this.id,
          paidById: options.paidById,
          method: options.method,
          amount: this.total,
          transactionId: options.transactionId,
        },
      }),
      prisma.orderEvent.create({
        data: {
          orderId: this.id,
          action: 'paid',
          createdById: options.paidById,
          metadata: { method: options.method },
        },
      }),
    ])

    await this.reload()
  }

  async ship(options: ShipOrderInput & { shippedById: string }): Promise<void> {
    if (this.isShipped) {
      throw new AppError('Order is already shipped', 400, 'ALREADY_SHIPPED')
    }
    if (!this.isPaid) {
      throw new AppError('Cannot ship an unpaid order', 400, 'NOT_PAID')
    }
    if (this.isCancelled) {
      throw new AppError('Cannot ship a cancelled order', 400, 'ORDER_CANCELLED')
    }

    await prisma.$transaction([
      prisma.orderShipment.create({
        data: {
          orderId: this.id,
          shippedById: options.shippedById,
          trackingNumber: options.trackingNumber,
          carrier: options.carrier,
        },
      }),
      prisma.orderEvent.create({
        data: {
          orderId: this.id,
          action: 'shipped',
          createdById: options.shippedById,
          metadata: {
            trackingNumber: options.trackingNumber,
            carrier: options.carrier,
          },
        },
      }),
    ])

    await this.reload()
  }

  async cancel(options: {
    cancelledById: string
    reason: string
  }): Promise<void> {
    if (this.isCancelled) {
      throw new AppError('Order is already cancelled', 400, 'ALREADY_CANCELLED')
    }
    if (this.isShipped) {
      throw new AppError('Cannot cancel a shipped order', 400, 'ORDER_SHIPPED')
    }

    await prisma.$transaction([
      prisma.orderCancellation.create({
        data: {
          orderId: this.id,
          cancelledById: options.cancelledById,
          reason: options.reason,
        },
      }),
      prisma.orderEvent.create({
        data: {
          orderId: this.id,
          action: 'cancelled',
          createdById: options.cancelledById,
          metadata: { reason: options.reason },
        },
      }),
    ])

    await this.reload()
  }

  async refund(options: {
    refundedById: string
    reason: string
    amount?: number
  }): Promise<void> {
    if (!this.isPaid) {
      throw new AppError('Cannot refund an unpaid order', 400, 'NOT_PAID')
    }

    const refundAmount = options.amount ?? this.total

    await prisma.$transaction([
      prisma.orderPayment.delete({
        where: { orderId: this.id },
      }),
      prisma.orderRefund.create({
        data: {
          orderId: this.id,
          refundedById: options.refundedById,
          amount: refundAmount,
          reason: options.reason,
        },
      }),
      prisma.orderEvent.create({
        data: {
          orderId: this.id,
          action: 'refunded',
          createdById: options.refundedById,
          metadata: { amount: refundAmount, reason: options.reason },
        },
      }),
    ])

    await this.reload()
  }

  // ═══════════════════════════════════════════════════════════════
  // HELPERS
  // ═══════════════════════════════════════════════════════════════

  private async reload(): Promise<void> {
    const fresh = await prisma.order.findUnique({
      where: { id: this.id },
      include: orderWithRelations,
    })
    if (fresh) {
      this.data = fresh
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // SERIALIZATION
  // ═══════════════════════════════════════════════════════════════

  toJSON() {
    return {
      id: this.id,
      number: this.number,
      status: this.status,
      total: this.total,
      isPaid: this.isPaid,
      isShipped: this.isShipped,
      isCancelled: this.isCancelled,
      canShip: this.canShip,
      canCancel: this.canCancel,
      customer: this.customer,
      items: this.items,
      payment: this.data.payment,
      shipment: this.data.shipment,
      createdAt: this.createdAt,
    }
  }
}
```

---

## State as Records

### Schema Pattern

```prisma
// ═══════════════════════════════════════════════════════════════
// MAIN ENTITY
// ═══════════════════════════════════════════════════════════════

model Order {
  id        String   @id @default(cuid())
  number    Int
  status    String   @default("pending")
  total     Decimal  @db.Decimal(10, 2)

  // Ownership
  tenantId    String
  tenant      Tenant   @relation(fields: [tenantId], references: [id])
  customerId  String
  customer    Customer @relation(fields: [customerId], references: [id])
  createdById String
  createdBy   User     @relation("CreatedOrders", fields: [createdById], references: [id])

  // Timestamps
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  // Related
  items       OrderItem[]

  // State Records (NOT booleans!)
  payment     OrderPayment?
  shipment    OrderShipment?
  cancellation OrderCancellation?
  refund      OrderRefund?

  // Audit trail
  events      OrderEvent[]

  @@unique([tenantId, number])
  @@index([tenantId, status])
  @@index([tenantId, customerId])
  @@index([tenantId, createdAt])
}

// ═══════════════════════════════════════════════════════════════
// STATE RECORDS - Capture WHO, WHEN, WHY, HOW
// ═══════════════════════════════════════════════════════════════

model OrderPayment {
  id            String   @id @default(cuid())
  orderId       String   @unique
  order         Order    @relation(fields: [orderId], references: [id], onDelete: Cascade)
  paidById      String
  paidBy        User     @relation(fields: [paidById], references: [id])
  method        String   // 'card', 'bank', 'cash'
  amount        Decimal  @db.Decimal(10, 2)
  transactionId String?
  createdAt     DateTime @default(now())
}

model OrderShipment {
  id             String   @id @default(cuid())
  orderId        String   @unique
  order          Order    @relation(fields: [orderId], references: [id], onDelete: Cascade)
  shippedById    String
  shippedBy      User     @relation(fields: [shippedById], references: [id])
  trackingNumber String
  carrier        String
  createdAt      DateTime @default(now())
}

model OrderCancellation {
  id            String   @id @default(cuid())
  orderId       String   @unique
  order         Order    @relation(fields: [orderId], references: [id], onDelete: Cascade)
  cancelledById String
  cancelledBy   User     @relation(fields: [cancelledById], references: [id])
  reason        String
  createdAt     DateTime @default(now())
}

model OrderRefund {
  id          String   @id @default(cuid())
  orderId     String   @unique
  order       Order    @relation(fields: [orderId], references: [id], onDelete: Cascade)
  refundedById String
  refundedBy  User     @relation(fields: [refundedById], references: [id])
  amount      Decimal  @db.Decimal(10, 2)
  reason      String
  createdAt   DateTime @default(now())
}

// ═══════════════════════════════════════════════════════════════
// EVENT LOG - Full Audit Trail
// ═══════════════════════════════════════════════════════════════

model OrderEvent {
  id          String   @id @default(cuid())
  orderId     String
  order       Order    @relation(fields: [orderId], references: [id], onDelete: Cascade)
  action      String   // 'created', 'paid', 'shipped', 'cancelled', 'refunded'
  metadata    Json?
  createdById String
  createdBy   User     @relation(fields: [createdById], references: [id])
  createdAt   DateTime @default(now())

  @@index([orderId, createdAt])
}
```

---

# Part 4: Backend — Data Layer

## Prisma Conventions

### Client Singleton

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development'
    ? ['query', 'error', 'warn']
    : ['error'],
})

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma
}
```

### Query Helpers

```typescript
// domains/orders/models/Order.queries.ts
import { Prisma } from '@prisma/client'

export const orderWithRelations = {
  customer: {
    select: { id: true, name: true, email: true },
  },
  items: {
    include: {
      product: { select: { id: true, name: true, price: true } },
    },
  },
  payment: {
    include: { paidBy: { select: { id: true, name: true } } },
  },
  shipment: {
    include: { shippedBy: { select: { id: true, name: true } } },
  },
  cancellation: {
    include: { cancelledBy: { select: { id: true, name: true } } },
  },
  createdBy: {
    select: { id: true, name: true },
  },
} satisfies Prisma.OrderInclude

export type OrderWithRelations = Prisma.OrderGetPayload<{
  include: typeof orderWithRelations
}>
```

---

## Multi-Tenancy

### Every Query Must Include tenantId

```typescript
// ❌ SECURITY VULNERABILITY
prisma.order.findMany({ where: { status: 'pending' } })

// ✅ ALWAYS INCLUDE TENANT
prisma.order.findMany({ where: { tenantId, status: 'pending' } })
```

### Get Current Tenant in Server Actions

```typescript
// lib/auth.ts
import { cookies } from 'next/headers'
import { prisma } from '@/lib/prisma'

export async function getCurrentUser() {
  const cookieStore = cookies()
  const token = cookieStore.get('token')?.value

  if (!token) return null

  try {
    const payload = verifyToken(token)
    const user = await prisma.user.findUnique({
      where: { id: payload.userId },
      include: { tenant: true },
    })
    return user
  } catch {
    return null
  }
}

export async function requireAuth() {
  const user = await getCurrentUser()
  if (!user) throw new AppError('Unauthorized', 401, 'UNAUTHORIZED')
  return user
}
```

---

# Part 5: Backend — API Layer

## CRUD Routing Philosophy

Every action maps to CRUD. When something doesn't fit, **create a new resource**.

```typescript
// Core CRUD
GET    /orders              → Order.list()
POST   /orders              → Order.create()
GET    /orders/:id          → Order.findById()
PUT    /orders/:id          → order.update()
DELETE /orders/:id          → order.delete()

// State changes as sub-resources (POST to create state record)
POST   /orders/:id/payment      → order.pay()
DELETE /orders/:id/payment      → order.refund()
POST   /orders/:id/shipment     → order.ship()
POST   /orders/:id/cancellation → order.cancel()
```

---

## Validation with Zod

```typescript
// domains/orders/models/Order.schema.ts
import { z } from 'zod'

// Enums
export const ORDER_STATUSES = ['pending', 'paid', 'shipped', 'cancelled'] as const
export const PAYMENT_METHODS = ['card', 'bank', 'cash'] as const
export const CARRIERS = ['ups', 'fedex', 'dhl', 'usps'] as const

// Create
export const createOrderSchema = z.object({
  customerId: z.string().cuid(),
  items: z.array(z.object({
    productId: z.string().cuid(),
    quantity: z.number().int().positive(),
    price: z.number().positive(),
  })).min(1, 'At least one item required'),
  notes: z.string().max(5000).optional(),
})

// Update
export const updateOrderSchema = createOrderSchema.partial()

// State transitions
export const payOrderSchema = z.object({
  method: z.enum(PAYMENT_METHODS),
  transactionId: z.string().optional(),
})

export const shipOrderSchema = z.object({
  trackingNumber: z.string().min(1, 'Tracking number required'),
  carrier: z.enum(CARRIERS),
})

export const cancelOrderSchema = z.object({
  reason: z.string().min(1, 'Reason required').max(1000),
})

// Types
export type CreateOrderInput = z.infer<typeof createOrderSchema>
export type UpdateOrderInput = z.infer<typeof updateOrderSchema>
export type PayOrderInput = z.infer<typeof payOrderSchema>
export type ShipOrderInput = z.infer<typeof shipOrderSchema>
export type CancelOrderInput = z.infer<typeof cancelOrderSchema>
```

---

## Error Handling

```typescript
// lib/errors.ts

export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 400,
    public code: string = 'BAD_REQUEST'
  ) {
    super(message)
    this.name = 'AppError'
  }
}

export class NotFoundError extends AppError {
  constructor(resource = 'Resource') {
    super(`${resource} not found`, 404, 'NOT_FOUND')
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED')
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Forbidden') {
    super(message, 403, 'FORBIDDEN')
  }
}

export class ValidationError extends AppError {
  constructor(message: string, public errors?: Record<string, string[]>) {
    super(message, 400, 'VALIDATION_ERROR')
  }
}
```

---

# Part 6: Frontend — Core Patterns

## Server vs Client Components

### The Rule

**Server Components by default.** Only add `'use client'` when you need:
- Event handlers (onClick, onChange)
- useState, useEffect, useRef
- Browser APIs (window, localStorage)
- Third-party client libraries

### Decision Tree

```
Does it need interactivity (onClick, forms, state)?
├── No  → Server Component (default)
└── Yes → Does the interaction require client state?
          ├── No  → Server Component + Server Action
          └── Yes → Client Component
```

### Examples

```typescript
// ✅ SERVER COMPONENT - Data fetching, static display
// domains/orders/components/OrderList.tsx
import { Order } from '../models/Order'
import { OrderListView } from './OrderListView'
import { getCurrentUser } from '@/lib/auth'

export async function OrderList() {
  const user = await getCurrentUser()
  const { data: orders, ...pagination } = await Order.list(user.tenantId)

  return <OrderListView orders={orders} pagination={pagination} />
}

// ✅ SERVER COMPONENT - Even with forms (use Server Actions)
// domains/orders/components/OrderDetails.tsx
import { Order } from '../models/Order'
import { shipOrder, cancelOrder } from '../actions/order.actions'

export async function OrderDetails({ id }: { id: string }) {
  const user = await getCurrentUser()
  const order = await Order.findById(id, user.tenantId)

  return (
    <div>
      <h1>Order #{order.number}</h1>
      {order.canShip && (
        <form action={shipOrder.bind(null, order.id)}>
          <input name="trackingNumber" required />
          <button type="submit">Ship Order</button>
        </form>
      )}
    </div>
  )
}

// ✅ CLIENT COMPONENT - Needs local state for form
// domains/orders/components/OrderForm.tsx
'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { createOrderSchema, type CreateOrderInput } from '../models/Order.schema'
import { createOrder } from '../actions/order.actions'

export function OrderForm() {
  const [isPending, setIsPending] = useState(false)
  const form = useForm<CreateOrderInput>({
    resolver: zodResolver(createOrderSchema),
  })

  async function onSubmit(data: CreateOrderInput) {
    setIsPending(true)
    const result = await createOrder(data)
    setIsPending(false)
    // Handle result...
  }

  return <form onSubmit={form.handleSubmit(onSubmit)}>...</form>
}

// ✅ CLIENT COMPONENT - Interactive UI
// domains/orders/components/OrderSearch.tsx
'use client'

import { useState } from 'react'
import { useDebounce } from '@/hooks/useDebounce'

export function OrderSearch({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')
  const debouncedQuery = useDebounce(query, 300)

  useEffect(() => {
    onSearch(debouncedQuery)
  }, [debouncedQuery, onSearch])

  return <input value={query} onChange={e => setQuery(e.target.value)} />
}
```

---

## Data Fetching Patterns

### In Server Components (Preferred)

```typescript
// app/(dashboard)/orders/page.tsx
import { Order } from '@/domains/orders'
import { OrderList } from '@/domains/orders'
import { requireAuth } from '@/lib/auth'

export default async function OrdersPage() {
  const user = await requireAuth()
  const { data: orders, ...pagination } = await Order.list(user.tenantId)

  return <OrderList orders={orders} pagination={pagination} />
}
```

### With Search Params

```typescript
// app/(dashboard)/orders/page.tsx
import { Order } from '@/domains/orders'

interface Props {
  searchParams: { page?: string; status?: string; search?: string }
}

export default async function OrdersPage({ searchParams }: Props) {
  const user = await requireAuth()

  const { data: orders, ...pagination } = await Order.list(user.tenantId, {
    page: Number(searchParams.page) || 1,
    status: searchParams.status,
    search: searchParams.search,
  })

  return <OrderList orders={orders} pagination={pagination} />
}
```

### Parallel Data Fetching

```typescript
// app/(dashboard)/orders/[id]/page.tsx
import { Order } from '@/domains/orders'
import { Customer } from '@/domains/customers'

export default async function OrderPage({ params }: { params: { id: string } }) {
  const user = await requireAuth()

  // Parallel fetching
  const [order, recentOrders] = await Promise.all([
    Order.findById(params.id, user.tenantId),
    Order.list(user.tenantId, { limit: 5 }),
  ])

  return (
    <div>
      <OrderDetails order={order} />
      <RecentOrders orders={recentOrders.data} />
    </div>
  )
}
```

---

## Server Actions

### Basic Pattern

```typescript
// domains/orders/actions/order.actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { Order } from '../models/Order'
import {
  createOrderSchema,
  shipOrderSchema,
  cancelOrderSchema,
} from '../models/Order.schema'
import { requireAuth } from '@/lib/auth'
import { AppError } from '@/lib/errors'

// ═══════════════════════════════════════════════════════════════
// ACTION RESULT TYPE
// ═══════════════════════════════════════════════════════════════

type ActionResult<T = void> =
  | { success: true; data: T }
  | { success: false; error: string; code?: string }

// ═══════════════════════════════════════════════════════════════
// CREATE
// ═══════════════════════════════════════════════════════════════

export async function createOrder(
  formData: FormData
): Promise<ActionResult<{ id: string }>> {
  try {
    const user = await requireAuth()

    const data = createOrderSchema.parse({
      customerId: formData.get('customerId'),
      items: JSON.parse(formData.get('items') as string),
      notes: formData.get('notes'),
    })

    const order = await Order.create(data, user.tenantId, user.id)

    revalidatePath('/orders')

    return { success: true, data: { id: order.id } }
  } catch (error) {
    if (error instanceof AppError) {
      return { success: false, error: error.message, code: error.code }
    }
    console.error('createOrder error:', error)
    return { success: false, error: 'Failed to create order' }
  }
}

// ═══════════════════════════════════════════════════════════════
// STATE TRANSITIONS
// ═══════════════════════════════════════════════════════════════

export async function shipOrder(
  orderId: string,
  formData: FormData
): Promise<ActionResult> {
  try {
    const user = await requireAuth()

    const data = shipOrderSchema.parse({
      trackingNumber: formData.get('trackingNumber'),
      carrier: formData.get('carrier'),
    })

    const order = await Order.findById(orderId, user.tenantId)
    await order.ship({ shippedById: user.id, ...data })

    revalidatePath('/orders')
    revalidatePath(`/orders/${orderId}`)

    return { success: true, data: undefined }
  } catch (error) {
    if (error instanceof AppError) {
      return { success: false, error: error.message, code: error.code }
    }
    console.error('shipOrder error:', error)
    return { success: false, error: 'Failed to ship order' }
  }
}

export async function cancelOrder(
  orderId: string,
  formData: FormData
): Promise<ActionResult> {
  try {
    const user = await requireAuth()

    const data = cancelOrderSchema.parse({
      reason: formData.get('reason'),
    })

    const order = await Order.findById(orderId, user.tenantId)
    await order.cancel({ cancelledById: user.id, ...data })

    revalidatePath('/orders')
    revalidatePath(`/orders/${orderId}`)

    return { success: true, data: undefined }
  } catch (error) {
    if (error instanceof AppError) {
      return { success: false, error: error.message, code: error.code }
    }
    console.error('cancelOrder error:', error)
    return { success: false, error: 'Failed to cancel order' }
  }
}

// ═══════════════════════════════════════════════════════════════
// WITH REDIRECT
// ═══════════════════════════════════════════════════════════════

export async function createOrderAndRedirect(formData: FormData) {
  const result = await createOrder(formData)

  if (result.success) {
    redirect(`/orders/${result.data.id}`)
  }

  return result
}
```

### Using Actions in Components

```typescript
// Option 1: Form with action (Server Component compatible)
<form action={shipOrder.bind(null, order.id)}>
  <input name="trackingNumber" required />
  <select name="carrier">
    <option value="ups">UPS</option>
    <option value="fedex">FedEx</option>
  </select>
  <button type="submit">Ship Order</button>
</form>

// Option 2: With useFormStatus for pending state
'use client'
import { useFormStatus } from 'react-dom'

function SubmitButton() {
  const { pending } = useFormStatus()
  return <button disabled={pending}>{pending ? 'Shipping...' : 'Ship Order'}</button>
}

// Option 3: With useActionState for result handling
'use client'
import { useActionState } from 'react'
import { createOrder } from '../actions/order.actions'

export function OrderForm() {
  const [state, formAction, isPending] = useActionState(createOrder, null)

  return (
    <form action={formAction}>
      {state?.success === false && (
        <div className="text-red-600">{state.error}</div>
      )}
      {/* form fields */}
      <button disabled={isPending}>
        {isPending ? 'Creating...' : 'Create Order'}
      </button>
    </form>
  )
}
```

---

## Loading & Error States

### Loading UI

```typescript
// app/(dashboard)/orders/loading.tsx
import { Skeleton } from '@/components/ui/skeleton'

export default function OrdersLoading() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-8 w-48" />
      <div className="space-y-2">
        {Array.from({ length: 5 }).map((_, i) => (
          <Skeleton key={i} className="h-16 w-full" />
        ))}
      </div>
    </div>
  )
}
```

### Error Boundary

```typescript
// app/(dashboard)/orders/error.tsx
'use client'

import { useEffect } from 'react'
import { Button } from '@/components/ui/button'

interface Props {
  error: Error & { digest?: string }
  reset: () => void
}

export default function OrdersError({ error, reset }: Props) {
  useEffect(() => {
    console.error('Orders error:', error)
  }, [error])

  return (
    <div className="flex flex-col items-center justify-center py-12">
      <h2 className="text-xl font-semibold">Something went wrong</h2>
      <p className="text-gray-600 mt-2">
        {error.message || 'Failed to load orders'}
      </p>
      <Button onClick={reset} className="mt-4">
        Try again
      </Button>
    </div>
  )
}
```

### Not Found

```typescript
// app/(dashboard)/orders/[id]/not-found.tsx
import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function OrderNotFound() {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <h2 className="text-xl font-semibold">Order not found</h2>
      <p className="text-gray-600 mt-2">
        The order you're looking for doesn't exist.
      </p>
      <Button asChild className="mt-4">
        <Link href="/orders">Back to Orders</Link>
      </Button>
    </div>
  )
}

// Usage in page
import { notFound } from 'next/navigation'

export default async function OrderPage({ params }) {
  const order = await Order.findByIdOrNull(params.id, user.tenantId)

  if (!order) {
    notFound()
  }

  return <OrderDetails order={order} />
}
```

---

# Part 7: Frontend — Components

## Component Architecture

### Naming & File Structure

```
domains/{domain}/components/
├── {Model}List.tsx           # List container (fetches data)
├── {Model}ListView.tsx       # List presentational (receives props)
├── {Model}Details.tsx        # Detail view
├── {Model}Form.tsx           # Create/edit form
├── {Model}Card.tsx           # Card component
├── {Model}Table.tsx          # Table variant
├── {Model}Actions.tsx        # Action buttons/menu
├── {Model}StatusBadge.tsx    # Status indicator
└── index.ts                  # Barrel export
```

### Barrel Export

```typescript
// domains/orders/components/index.ts
export { OrderList } from './OrderList'
export { OrderListView } from './OrderListView'
export { OrderDetails } from './OrderDetails'
export { OrderForm } from './OrderForm'
export { OrderCard } from './OrderCard'
export { OrderTable } from './OrderTable'
export { OrderActions } from './OrderActions'
export { OrderStatusBadge } from './OrderStatusBadge'
```

---

## Container + Presentational

### Container (Data + Logic)

```typescript
// domains/orders/components/OrderList.tsx
import { requireAuth } from '@/lib/auth'
import { Order } from '../models/Order'
import { OrderListView } from './OrderListView'
import { orderContent } from '../constants/order.content'

interface Props {
  searchParams?: {
    page?: string
    status?: string
    search?: string
  }
}

export async function OrderList({ searchParams = {} }: Props) {
  const user = await requireAuth()

  const result = await Order.list(user.tenantId, {
    page: Number(searchParams.page) || 1,
    status: searchParams.status,
    search: searchParams.search,
  })

  return (
    <OrderListView
      orders={result.data}
      pagination={{
        page: result.page,
        totalPages: result.totalPages,
        total: result.total,
      }}
      content={orderContent}
    />
  )
}
```

### Presentational (Pure UI)

```typescript
// domains/orders/components/OrderListView.tsx
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Button } from '@/components/ui/button'
import { EmptyState } from '@/shared/components/EmptyState'
import { Pagination } from '@/shared/components/Pagination'
import { OrderStatusBadge } from './OrderStatusBadge'
import { OrderActions } from './OrderActions'
import type { Order } from '../models/Order'
import type { OrderContent } from '../constants/order.content'

interface Props {
  orders: Order[]
  pagination: {
    page: number
    totalPages: number
    total: number
  }
  content: OrderContent
}

export function OrderListView({ orders, pagination, content }: Props) {
  if (orders.length === 0) {
    return (
      <EmptyState
        icon="package"
        heading={content.emptyState.heading}
        description={content.emptyState.description}
        action={{
          label: content.actions.create,
          href: '/orders/new',
        }}
      />
    )
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>{content.meta.title}</CardTitle>
        <Button asChild>
          <Link href="/orders/new">{content.actions.create}</Link>
        </Button>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>{content.labels.number}</TableHead>
              <TableHead>{content.labels.customer}</TableHead>
              <TableHead>{content.labels.status}</TableHead>
              <TableHead>{content.labels.total}</TableHead>
              <TableHead>{content.labels.date}</TableHead>
              <TableHead className="w-12"></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {orders.map(order => (
              <TableRow key={order.id}>
                <TableCell>
                  <Link href={`/orders/${order.id}`} className="font-medium hover:underline">
                    #{order.number}
                  </Link>
                </TableCell>
                <TableCell>{order.customer.name}</TableCell>
                <TableCell>
                  <OrderStatusBadge order={order} />
                </TableCell>
                <TableCell>${order.total.toFixed(2)}</TableCell>
                <TableCell>{formatDate(order.createdAt)}</TableCell>
                <TableCell>
                  <OrderActions order={order} />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>

        <Pagination
          page={pagination.page}
          totalPages={pagination.totalPages}
          total={pagination.total}
        />
      </CardContent>
    </Card>
  )
}
```

---

## Content Constants

### Structure

```typescript
// domains/orders/constants/order.content.ts

export const orderContent = {
  meta: {
    title: 'Orders',
    description: 'Manage customer orders',
  },

  emptyState: {
    heading: 'No orders yet',
    description: 'Orders will appear here once customers start ordering.',
  },

  errorState: {
    heading: 'Error loading orders',
    description: 'Something went wrong. Please try again.',
    retry: 'Try Again',
  },

  loadingState: {
    message: 'Loading orders...',
  },

  actions: {
    create: 'Create Order',
    edit: 'Edit',
    delete: 'Delete',
    ship: 'Ship Order',
    cancel: 'Cancel Order',
    refund: 'Refund',
    viewDetails: 'View Details',
  },

  labels: {
    number: 'Order #',
    customer: 'Customer',
    status: 'Status',
    total: 'Total',
    date: 'Date',
    items: 'Items',
    notes: 'Notes',
    trackingNumber: 'Tracking Number',
    carrier: 'Carrier',
    reason: 'Reason',
  },

  status: {
    pending: 'Pending',
    paid: 'Paid',
    shipped: 'Shipped',
    cancelled: 'Cancelled',
  },

  form: {
    create: {
      title: 'Create Order',
      submit: 'Create Order',
    },
    edit: {
      title: 'Edit Order',
      submit: 'Save Changes',
    },
    ship: {
      title: 'Ship Order',
      description: 'Enter shipping details to mark this order as shipped.',
      submit: 'Ship Order',
    },
    cancel: {
      title: 'Cancel Order',
      description: 'Please provide a reason for cancellation.',
      submit: 'Cancel Order',
      warning: 'This action cannot be undone.',
    },
  },

  validation: {
    customerRequired: 'Please select a customer',
    itemsRequired: 'Add at least one item',
    trackingRequired: 'Tracking number is required',
    carrierRequired: 'Please select a carrier',
    reasonRequired: 'Please provide a reason',
  },

  success: {
    created: 'Order created successfully',
    updated: 'Order updated successfully',
    shipped: 'Order shipped successfully',
    cancelled: 'Order cancelled',
    refunded: 'Order refunded',
  },

  confirm: {
    cancel: {
      title: 'Cancel Order',
      description: 'Are you sure you want to cancel this order?',
      confirm: 'Yes, Cancel Order',
      dismiss: 'No, Keep Order',
    },
    delete: {
      title: 'Delete Order',
      description: 'This will permanently delete the order. This action cannot be undone.',
      confirm: 'Delete',
      dismiss: 'Cancel',
    },
  },
}

export type OrderContent = typeof orderContent
```

### Usage Rules

```typescript
// ❌ FORBIDDEN - Hardcoded text
<Button>Create Order</Button>
<p>No orders yet</p>

// ✅ CORRECT - Content constants
<Button>{content.actions.create}</Button>
<p>{content.emptyState.heading}</p>
```

---

# Part 8: Frontend — Forms

## Form Architecture

### Pattern

1. **Zod schema** — Single source of truth for validation
2. **react-hook-form** — Form state management
3. **Server Action** — Mutation handler
4. **useActionState** — Action result handling

### Complete Form Example

```typescript
// domains/orders/components/OrderForm.tsx
'use client'

import { useActionState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { createOrderSchema, type CreateOrderInput } from '../models/Order.schema'
import { createOrder } from '../actions/order.actions'
import { orderContent } from '../constants/order.content'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { CustomerSelect } from '@/domains/customers'
import { ProductSelector } from './ProductSelector'

const content = orderContent.form.create

export function OrderForm() {
  const form = useForm<CreateOrderInput>({
    resolver: zodResolver(createOrderSchema),
    defaultValues: {
      customerId: '',
      items: [],
      notes: '',
    },
  })

  const [state, formAction, isPending] = useActionState(
    async (prevState: any, formData: FormData) => {
      // Validate with react-hook-form first
      const isValid = await form.trigger()
      if (!isValid) return { success: false, error: 'Validation failed' }

      // Get form values and call action
      const values = form.getValues()
      formData.set('customerId', values.customerId)
      formData.set('items', JSON.stringify(values.items))
      formData.set('notes', values.notes || '')

      return createOrder(formData)
    },
    null
  )

  return (
    <Form {...form}>
      <form action={formAction} className="space-y-6">
        {state?.success === false && (
          <div className="bg-red-50 text-red-600 p-4 rounded-lg">
            {state.error}
          </div>
        )}

        <FormField
          control={form.control}
          name="customerId"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{orderContent.labels.customer}</FormLabel>
              <FormControl>
                <CustomerSelect
                  value={field.value}
                  onChange={field.onChange}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="items"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{orderContent.labels.items}</FormLabel>
              <FormControl>
                <ProductSelector
                  items={field.value}
                  onChange={field.onChange}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="notes"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{orderContent.labels.notes}</FormLabel>
              <FormControl>
                <Textarea {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="flex gap-4">
          <Button type="submit" disabled={isPending}>
            {isPending ? 'Creating...' : content.submit}
          </Button>
          <Button type="button" variant="outline" onClick={() => form.reset()}>
            Reset
          </Button>
        </div>
      </form>
    </Form>
  )
}
```

---

## Server Action Forms

### Simple Form (No Client State)

```typescript
// Can be a Server Component!
import { shipOrder } from '../actions/order.actions'
import { SubmitButton } from '@/shared/components/SubmitButton'

interface Props {
  orderId: string
}

export function ShipOrderForm({ orderId }: Props) {
  const shipOrderWithId = shipOrder.bind(null, orderId)

  return (
    <form action={shipOrderWithId} className="space-y-4">
      <div>
        <label htmlFor="trackingNumber">Tracking Number</label>
        <input
          type="text"
          name="trackingNumber"
          id="trackingNumber"
          required
          className="border rounded px-3 py-2 w-full"
        />
      </div>

      <div>
        <label htmlFor="carrier">Carrier</label>
        <select name="carrier" id="carrier" required className="border rounded px-3 py-2 w-full">
          <option value="">Select carrier...</option>
          <option value="ups">UPS</option>
          <option value="fedex">FedEx</option>
          <option value="dhl">DHL</option>
        </select>
      </div>

      <SubmitButton>Ship Order</SubmitButton>
    </form>
  )
}

// shared/components/SubmitButton.tsx
'use client'

import { useFormStatus } from 'react-dom'
import { Button } from '@/components/ui/button'

export function SubmitButton({ children }: { children: React.ReactNode }) {
  const { pending } = useFormStatus()

  return (
    <Button type="submit" disabled={pending}>
      {pending ? 'Submitting...' : children}
    </Button>
  )
}
```

---

## Optimistic Updates

```typescript
// domains/orders/components/OrderStatusToggle.tsx
'use client'

import { useOptimistic, useTransition } from 'react'
import { toggleOrderStatus } from '../actions/order.actions'
import { Button } from '@/components/ui/button'

interface Props {
  orderId: string
  initialStatus: string
}

export function OrderStatusToggle({ orderId, initialStatus }: Props) {
  const [isPending, startTransition] = useTransition()
  const [optimisticStatus, setOptimisticStatus] = useOptimistic(initialStatus)

  function handleToggle() {
    const newStatus = optimisticStatus === 'active' ? 'paused' : 'active'

    startTransition(async () => {
      setOptimisticStatus(newStatus)
      await toggleOrderStatus(orderId, newStatus)
    })
  }

  return (
    <Button
      onClick={handleToggle}
      disabled={isPending}
      variant={optimisticStatus === 'active' ? 'default' : 'secondary'}
    >
      {optimisticStatus === 'active' ? 'Pause' : 'Activate'}
    </Button>
  )
}
```

---

# Part 9: Frontend — State & Data

## State Management

### The Rule

**Minimize client state.** Use:
1. **URL state** — For filters, pagination, tabs
2. **Server state** — For data (via RSC)
3. **React Context** — For truly global UI state (theme, toast)
4. **Component state** — For local UI interactions

### URL State for Filters

```typescript
// domains/orders/components/OrderFilters.tsx
'use client'

import { useRouter, useSearchParams, usePathname } from 'next/navigation'
import { useCallback } from 'react'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'

export function OrderFilters() {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()

  const createQueryString = useCallback(
    (name: string, value: string) => {
      const params = new URLSearchParams(searchParams.toString())
      if (value) {
        params.set(name, value)
      } else {
        params.delete(name)
      }
      params.delete('page') // Reset pagination on filter change
      return params.toString()
    },
    [searchParams]
  )

  function handleFilterChange(name: string, value: string) {
    router.push(`${pathname}?${createQueryString(name, value)}`)
  }

  return (
    <div className="flex gap-4">
      <Input
        placeholder="Search orders..."
        defaultValue={searchParams.get('search') ?? ''}
        onChange={(e) => handleFilterChange('search', e.target.value)}
      />
      <Select
        value={searchParams.get('status') ?? ''}
        onValueChange={(value) => handleFilterChange('status', value)}
      >
        <option value="">All statuses</option>
        <option value="pending">Pending</option>
        <option value="paid">Paid</option>
        <option value="shipped">Shipped</option>
      </Select>
    </div>
  )
}
```

### Context for UI State

```typescript
// context/ToastContext.tsx
'use client'

import { createContext, useContext, useState, useCallback } from 'react'

interface Toast {
  id: string
  message: string
  type: 'success' | 'error' | 'info'
}

interface ToastContextType {
  toasts: Toast[]
  addToast: (message: string, type: Toast['type']) => void
  removeToast: (id: string) => void
}

const ToastContext = createContext<ToastContextType | null>(null)

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([])

  const addToast = useCallback((message: string, type: Toast['type']) => {
    const id = crypto.randomUUID()
    setToasts(prev => [...prev, { id, message, type }])
    setTimeout(() => removeToast(id), 5000)
  }, [])

  const removeToast = useCallback((id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id))
  }, [])

  return (
    <ToastContext.Provider value={{ toasts, addToast, removeToast }}>
      {children}
    </ToastContext.Provider>
  )
}

export function useToast() {
  const context = useContext(ToastContext)
  if (!context) throw new Error('useToast must be used within ToastProvider')
  return context
}
```

---

## API Client

For external APIs only (not for your own backend with Server Actions):

```typescript
// lib/api.ts

const API_BASE = process.env.NEXT_PUBLIC_API_URL

class ApiError extends Error {
  constructor(message: string, public status: number, public code?: string) {
    super(message)
    this.name = 'ApiError'
  }
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE}${endpoint}`

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })

  const data = await response.json()

  if (!response.ok) {
    throw new ApiError(
      data.error?.message || 'Request failed',
      response.status,
      data.error?.code
    )
  }

  return data
}

export const api = {
  get: <T>(endpoint: string) => request<T>(endpoint),

  post: <T>(endpoint: string, body: unknown) =>
    request<T>(endpoint, { method: 'POST', body: JSON.stringify(body) }),

  put: <T>(endpoint: string, body: unknown) =>
    request<T>(endpoint, { method: 'PUT', body: JSON.stringify(body) }),

  delete: <T>(endpoint: string) =>
    request<T>(endpoint, { method: 'DELETE' }),
}

// Typed API methods
export const ordersApi = {
  list: (params?: { page?: number; status?: string }) =>
    api.get<{ data: Order[]; pagination: Pagination }>(`/orders?${new URLSearchParams(params as any)}`),

  get: (id: string) =>
    api.get<{ data: Order }>(`/orders/${id}`),

  create: (data: CreateOrderInput) =>
    api.post<{ data: Order }>('/orders', data),
}
```

---

# Part 10: Quality & Testing

## TypeScript Standards

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

### Rules

1. **No `any`** — Use `unknown` and narrow
2. **No type assertions** — Use type guards
3. **No non-null assertions** — Handle nulls explicitly

---

## Backend Testing

### Domain Model Tests

```typescript
// tests/domains/orders/Order.test.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { Order } from '@/domains/orders/models/Order'
import { prisma } from '@/lib/prisma'
import { fixtures } from '@/tests/fixtures'

describe('Order', () => {
  beforeEach(async () => {
    await prisma.orderEvent.deleteMany()
    await prisma.orderPayment.deleteMany()
    await prisma.orderShipment.deleteMany()
    await prisma.order.deleteMany()
  })

  describe('ship', () => {
    it('creates shipment record when paid', async () => {
      const order = await Order.create(fixtures.orders.standard, fixtures.tenantId, fixtures.userId)
      await order.pay({ paidById: fixtures.userId, method: 'card' })

      await order.ship({
        shippedById: fixtures.userId,
        trackingNumber: 'TRACK123',
        carrier: 'ups',
      })

      expect(order.isShipped).toBe(true)
      expect(order.data.shipment?.trackingNumber).toBe('TRACK123')
    })

    it('throws if not paid', async () => {
      const order = await Order.create(fixtures.orders.standard, fixtures.tenantId, fixtures.userId)

      await expect(
        order.ship({ shippedById: fixtures.userId, trackingNumber: 'TRACK123', carrier: 'ups' })
      ).rejects.toThrow('Cannot ship an unpaid order')
    })

    it('throws if already shipped', async () => {
      const order = await Order.create(fixtures.orders.standard, fixtures.tenantId, fixtures.userId)
      await order.pay({ paidById: fixtures.userId, method: 'card' })
      await order.ship({ shippedById: fixtures.userId, trackingNumber: 'TRACK123', carrier: 'ups' })

      await expect(
        order.ship({ shippedById: fixtures.userId, trackingNumber: 'TRACK456', carrier: 'fedex' })
      ).rejects.toThrow('already shipped')
    })
  })
})
```

---

## Frontend Testing

### Component Tests

```typescript
// tests/domains/orders/components/OrderListView.test.tsx
import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { OrderListView } from '@/domains/orders/components/OrderListView'
import { orderContent } from '@/domains/orders/constants/order.content'
import { fixtures } from '@/tests/fixtures'

describe('OrderListView', () => {
  it('renders orders in table', () => {
    render(
      <OrderListView
        orders={fixtures.orders.list}
        pagination={{ page: 1, totalPages: 1, total: 2 }}
        content={orderContent}
      />
    )

    expect(screen.getByText('#1001')).toBeInTheDocument()
    expect(screen.getByText('John Doe')).toBeInTheDocument()
  })

  it('shows empty state when no orders', () => {
    render(
      <OrderListView
        orders={[]}
        pagination={{ page: 1, totalPages: 0, total: 0 }}
        content={orderContent}
      />
    )

    expect(screen.getByText(orderContent.emptyState.heading)).toBeInTheDocument()
  })
})
```

### Server Action Tests

```typescript
// tests/domains/orders/actions/order.actions.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createOrder, shipOrder } from '@/domains/orders/actions/order.actions'

// Mock auth
vi.mock('@/lib/auth', () => ({
  requireAuth: vi.fn().mockResolvedValue({ id: 'user_1', tenantId: 'tenant_1' }),
}))

// Mock revalidatePath
vi.mock('next/cache', () => ({
  revalidatePath: vi.fn(),
}))

describe('order.actions', () => {
  describe('createOrder', () => {
    it('creates order with valid data', async () => {
      const formData = new FormData()
      formData.set('customerId', 'customer_1')
      formData.set('items', JSON.stringify([{ productId: 'prod_1', quantity: 1, price: 10 }]))

      const result = await createOrder(formData)

      expect(result.success).toBe(true)
      expect(result.data?.id).toBeDefined()
    })

    it('returns error for invalid data', async () => {
      const formData = new FormData()
      // Missing required fields

      const result = await createOrder(formData)

      expect(result.success).toBe(false)
      expect(result.error).toBeDefined()
    })
  })
})
```

---

# Part 11: Operations

## Performance Patterns

### N+1 Prevention

```typescript
// ❌ N+1
for (const order of orders) {
  const customer = await prisma.customer.findFirst({ where: { id: order.customerId } })
}

// ✅ BATCH
const customerIds = [...new Set(orders.map(o => o.customerId))]
const customers = await prisma.customer.findMany({ where: { id: { in: customerIds } } })
const customerMap = new Map(customers.map(c => [c.id, c]))
```

### Batch Operations

```typescript
// ❌ SLOW
for (const item of items) {
  await prisma.orderItem.create({ data: item })
}

// ✅ FAST
await prisma.orderItem.createMany({ data: items })
```

---

## API Cost Optimization

### Never Call External APIs in Loops

```typescript
// ❌ EXPENSIVE
for (const address of addresses) {
  const coords = await geocode(address) // $ per call
}

// ✅ USE STORED DATA OR BATCH
const stored = await prisma.address.findMany({
  where: { id: { in: ids } },
  select: { id: true, latitude: true, longitude: true },
})
```

### Cache API Responses

```typescript
const CACHE_TTL = 30 * 24 * 60 * 60 // 30 days

async function geocodeWithCache(address: string) {
  const cacheKey = `geo:${hash(address)}`

  const cached = await cache.get(cacheKey)
  if (cached) return cached

  const result = await callGeocodingAPI(address)
  await cache.set(cacheKey, result, CACHE_TTL)
  return result
}
```

---

## Authentication

### JWT Pattern

```typescript
// lib/auth.ts
import { cookies } from 'next/headers'
import jwt from 'jsonwebtoken'
import { prisma } from '@/lib/prisma'
import { AppError } from '@/lib/errors'

const JWT_SECRET = process.env.JWT_SECRET!

export async function getCurrentUser() {
  const cookieStore = cookies()
  const token = cookieStore.get('token')?.value

  if (!token) return null

  try {
    const payload = jwt.verify(token, JWT_SECRET) as { userId: string }

    return prisma.user.findUnique({
      where: { id: payload.userId, isActive: true },
      include: { tenant: true },
    })
  } catch {
    return null
  }
}

export async function requireAuth() {
  const user = await getCurrentUser()
  if (!user) throw new AppError('Unauthorized', 401)
  return user
}

export function generateToken(userId: string): string {
  return jwt.sign({ userId }, JWT_SECRET, { expiresIn: '24h' })
}
```

---

## Security Checklist

- [ ] All pages check authentication
- [ ] `tenantId` in every database query
- [ ] Input validated with Zod
- [ ] Server Actions validate before mutating
- [ ] Sensitive data not exposed in client
- [ ] CSRF protection (automatic with Server Actions)
- [ ] Rate limiting on sensitive endpoints

---

# Part 12: Reference

## Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Files | kebab-case | `order-form.tsx` |
| Components | PascalCase | `OrderForm` |
| Functions | camelCase | `createOrder` |
| Server Actions | camelCase | `createOrder` |
| Database | snake_case | `order_items` |
| Constants | SCREAMING_SNAKE | `MAX_ITEMS` |

---

## Import Rules

```typescript
// ✅ ALLOWED
import { Order, OrderForm } from '@/domains/orders'
import { Button } from '@/components/ui'
import { prisma } from '@/lib/prisma'

// ❌ FORBIDDEN
import { Order } from '@/domains/orders/models/Order'
```

---

## What to Avoid

| Don't | Do Instead |
|---------|--------------|
| Anemic services | Rich domain models |
| `isShipped: Boolean` | `OrderShipment` record |
| `'use client'` by default | Server Components first |
| API routes for forms | Server Actions |
| fetch in client components | Server Components + RSC |
| Redux/Zustand | URL state + Context |
| Queries in loops | Batch with Map |
| `export default` | Named exports |
| Hardcoded UI text | Content constants |
| Missing `tenantId` | Always include |

---

## Checklists

### New Feature (Full-Stack)

#### Backend
- [ ] Rich domain model
- [ ] State as records
- [ ] Zod schemas
- [ ] Server Actions

#### Frontend
- [ ] Server Component for data
- [ ] Content constants
- [ ] Loading/error states
- [ ] Form with validation

### Code Review

- [ ] No `any` types
- [ ] Server Components where possible
- [ ] Server Actions for mutations
- [ ] `tenantId` in all queries
- [ ] Content constants used
- [ ] Error handling complete

---

## Quick Reference

```
SERVER COMPONENT (default)
├── Data fetching
├── Static content
├── Forms with Server Actions
└── No useState/useEffect

CLIENT COMPONENT ('use client')
├── Event handlers
├── useState/useEffect
├── Browser APIs
└── Interactive UI

SERVER ACTIONS
├── 'use server' directive
├── Form mutations
├── revalidatePath() after changes
└── Return { success, data/error }

RICH DOMAIN MODELS
├── Factory: static async create(), findById()
├── Predicates: get isPaid(), isShipped()
├── Transitions: async pay(), ship(), cancel()
└── Serialization: toJSON()
```

---

**The best code is the code you don't write. The second best is the code that's obviously correct.**

*KreativReason Full-Stack Development Guide v3.0*
