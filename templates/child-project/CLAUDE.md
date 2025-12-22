# CLAUDE.md — KreativReason Full-Stack Guide

> Drop this file in your project root. AI agents read this first.

## Philosophy

**"Vanilla frameworks are plenty."** Rich domain models, Server Components first, Server Actions for mutations, state as records, tenant isolation always.

## Stack

```
Full-Stack: Next.js 14+ (App Router) + Prisma + PostgreSQL + Zod + TypeScript
Styling:    Tailwind CSS + shadcn/ui
Testing:    Vitest + Testing Library
```

## What We Avoid → Use Instead

| Avoid | Use Instead |
|-------|-------------|
| NextAuth | Custom JWT (~200 lines) |
| Redux, Zustand | URL state + React Context |
| TanStack Query | Server Components + RSC |
| tRPC, GraphQL | Server Actions + Zod |
| API routes for forms | Server Actions |
| `'use client'` by default | Server Components first |

---

## Project Structure

```
src/
├── app/                        # Next.js App Router
│   ├── (auth)/login/
│   ├── (dashboard)/
│   │   ├── layout.tsx
│   │   ├── orders/
│   │   │   ├── page.tsx        # List (Server Component)
│   │   │   ├── loading.tsx     # Loading state
│   │   │   ├── error.tsx       # Error boundary
│   │   │   ├── [id]/page.tsx   # Detail
│   │   │   └── new/page.tsx    # Create form
│   │   └── ...
│   └── api/webhooks/           # External webhooks only
│
├── domains/                    # Business logic (THE HEART)
│   └── orders/
│       ├── models/
│       │   ├── Order.ts        # Rich domain model
│       │   ├── Order.schema.ts # Zod schemas
│       │   └── Order.queries.ts
│       ├── actions/
│       │   └── order.actions.ts # Server Actions
│       ├── components/
│       │   ├── OrderList.tsx    # Container
│       │   ├── OrderListView.tsx # Presentational
│       │   └── OrderForm.tsx
│       ├── constants/
│       │   └── order.content.ts # UI text
│       └── index.ts
│
├── components/ui/              # shadcn/ui components
├── shared/                     # Layout, icons
├── lib/                        # prisma, auth, errors
└── hooks/                      # Global hooks
```

---

## The 8 Core Patterns

### 1. Server Components by Default

```typescript
// ✅ SERVER COMPONENT (default) - no 'use client'
export async function OrderList() {
  const user = await requireAuth()
  const orders = await Order.list(user.tenantId)
  return <OrderListView orders={orders} />
}

// ❌ WRONG - unnecessary client component
'use client'
export function OrderList() { ... }
```

### 2. Server Actions for Mutations

```typescript
// domains/orders/actions/order.actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { Order } from '../models/Order'
import { shipOrderSchema } from '../models/Order.schema'
import { requireAuth } from '@/lib/auth'

export async function shipOrder(orderId: string, formData: FormData) {
  const user = await requireAuth()
  const data = shipOrderSchema.parse(Object.fromEntries(formData))

  const order = await Order.findById(orderId, user.tenantId)
  await order.ship({ shippedById: user.id, ...data })

  revalidatePath('/orders')
  return { success: true }
}

// Usage in component (can be Server Component!)
<form action={shipOrder.bind(null, order.id)}>
  <input name="trackingNumber" required />
  <button type="submit">Ship</button>
</form>
```

### 3. Rich Domain Models

```typescript
// domains/orders/models/Order.ts
export class Order {
  constructor(private data: OrderWithRelations) {}

  // Factory methods
  static async findById(id: string, tenantId: string): Promise<Order> {
    const data = await prisma.order.findFirst({
      where: { id, tenantId },
      include: orderWithRelations,
    })
    if (!data) throw new NotFoundError('Order')
    return new Order(data)
  }

  // State predicates
  get isPaid(): boolean { return this.data.payment !== null }
  get isShipped(): boolean { return this.data.shipment !== null }
  get canShip(): boolean { return this.isPaid && !this.isShipped }

  // State transitions (business logic here!)
  async ship(opts: { shippedById: string; trackingNumber: string }) {
    if (this.isShipped) throw new AppError('Already shipped', 400)
    if (!this.isPaid) throw new AppError('Cannot ship unpaid', 400)

    await prisma.$transaction([
      prisma.orderShipment.create({ data: { orderId: this.id, ...opts } }),
      prisma.orderEvent.create({ data: { orderId: this.id, action: 'shipped' } }),
    ])
    await this.reload()
  }

  private async reload() { ... }
  toJSON() { ... }
}
```

### 4. State as Records (NOT Booleans)

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
  carrier        String
  createdAt      DateTime // WHEN
}
```

Query: `where: { shipment: { isNot: null } }`

### 5. Tenant Isolation (ALWAYS)

```typescript
// ❌ SECURITY BREACH
prisma.order.findMany({ where: { status: 'pending' } })

// ✅ ALWAYS INCLUDE TENANT
prisma.order.findMany({ where: { tenantId, status: 'pending' } })
```

### 6. Container + Presentational Components

```typescript
// Container (Server Component - fetches data)
export async function OrderList() {
  const user = await requireAuth()
  const orders = await Order.list(user.tenantId)
  return <OrderListView orders={orders} content={orderContent} />
}

// Presentational (receives props - can be server or client)
export function OrderListView({ orders, content }: Props) {
  if (orders.length === 0) {
    return <EmptyState heading={content.emptyState.heading} />
  }
  return <Table>...</Table>
}
```

### 7. Content Constants (No Hardcoded Text)

```typescript
// domains/orders/constants/order.content.ts
export const orderContent = {
  meta: { title: 'Orders' },
  emptyState: { heading: 'No orders yet' },
  actions: { create: 'Create Order', ship: 'Ship Order' },
  success: { shipped: 'Order shipped successfully' },
}

// Usage
<Button>{content.actions.ship}</Button>  // ✅
<Button>Ship Order</Button>              // ❌ FORBIDDEN
```

### 8. Loading & Error States

```typescript
// app/(dashboard)/orders/loading.tsx
export default function Loading() {
  return <Skeleton className="h-64" />
}

// app/(dashboard)/orders/error.tsx
'use client'
export default function Error({ error, reset }) {
  return (
    <div>
      <p>Error: {error.message}</p>
      <Button onClick={reset}>Try again</Button>
    </div>
  )
}
```

---

## What NOT To Do

| ❌ Don't | ✅ Do Instead |
|---------|--------------|
| `'use client'` by default | Server Components first |
| API routes for forms | Server Actions |
| fetch in useEffect | Data fetching in Server Components |
| Anemic services | Rich domain model classes |
| `isShipped: Boolean` | `OrderShipment` record |
| Business logic in actions | Logic in domain models |
| Queries in loops | Batch with Map |
| `export default` | Named exports only |
| Hardcoded UI text | Content constants |
| Missing `tenantId` | Always include in queries |

---

## Server Component vs Client Component

```
Does it need interactivity?
├── No  → Server Component ✅
└── Yes → Does it need client state (useState)?
          ├── No  → Server Component + Server Action ✅
          └── Yes → Client Component ('use client')
```

### When to Use 'use client'

- useState, useEffect, useRef
- Event handlers that need local state
- Browser APIs (window, localStorage)
- Third-party client libraries

---

## Form Patterns

### Simple Form (Server Component)

```typescript
// No 'use client' needed!
import { createOrder } from '../actions/order.actions'
import { SubmitButton } from '@/shared/components/SubmitButton'

export function CreateOrderForm() {
  return (
    <form action={createOrder}>
      <input name="customerId" required />
      <SubmitButton>Create Order</SubmitButton>
    </form>
  )
}

// shared/components/SubmitButton.tsx
'use client'
import { useFormStatus } from 'react-dom'

export function SubmitButton({ children }) {
  const { pending } = useFormStatus()
  return <button disabled={pending}>{pending ? 'Submitting...' : children}</button>
}
```

### Complex Form (Client Component)

```typescript
'use client'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useActionState } from 'react'

export function OrderForm() {
  const form = useForm({ resolver: zodResolver(createOrderSchema) })
  const [state, formAction, isPending] = useActionState(createOrder, null)

  return (
    <form action={formAction}>
      {state?.success === false && <div className="text-red-600">{state.error}</div>}
      {/* form fields */}
      <button disabled={isPending}>{isPending ? 'Creating...' : 'Create'}</button>
    </form>
  )
}
```

---

## Server Action Template

```typescript
// domains/{domain}/actions/{model}.actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { Model } from '../models/Model'
import { createSchema } from '../models/Model.schema'
import { requireAuth } from '@/lib/auth'

type ActionResult<T = void> =
  | { success: true; data: T }
  | { success: false; error: string }

export async function createModel(formData: FormData): Promise<ActionResult<{ id: string }>> {
  try {
    const user = await requireAuth()
    const data = createSchema.parse(Object.fromEntries(formData))

    const model = await Model.create(data, user.tenantId, user.id)

    revalidatePath('/models')
    return { success: true, data: { id: model.id } }
  } catch (error) {
    return { success: false, error: error.message }
  }
}
```

---

## Domain Model Template

```typescript
export class Order {
  constructor(private data: OrderWithRelations) {}

  // ═══════════════════════════════════════════════════
  // FACTORY METHODS
  // ═══════════════════════════════════════════════════

  static async findById(id: string, tenantId: string): Promise<Order> { ... }
  static async create(input: CreateInput, tenantId: string, userId: string): Promise<Order> { ... }
  static async list(tenantId: string, options?: ListOptions) { ... }

  // ═══════════════════════════════════════════════════
  // STATE PREDICATES
  // ═══════════════════════════════════════════════════

  get isPaid(): boolean { return this.data.payment !== null }
  get isShipped(): boolean { return this.data.shipment !== null }
  get canShip(): boolean { return this.isPaid && !this.isShipped && !this.isCancelled }

  // ═══════════════════════════════════════════════════
  // STATE TRANSITIONS
  // ═══════════════════════════════════════════════════

  async pay(opts: { paidById: string; method: string }) {
    if (this.isPaid) throw new AppError('Already paid', 400)
    await prisma.$transaction([...])
    await this.reload()
  }

  async ship(opts: { shippedById: string; trackingNumber: string }) {
    if (!this.canShip) throw new AppError('Cannot ship', 400)
    await prisma.$transaction([...])
    await this.reload()
  }

  // ═══════════════════════════════════════════════════
  // HELPERS
  // ═══════════════════════════════════════════════════

  private async reload() { ... }
  toJSON() { ... }
}
```

---

## URL State for Filters

```typescript
// domains/orders/components/OrderFilters.tsx
'use client'

import { useRouter, useSearchParams, usePathname } from 'next/navigation'

export function OrderFilters() {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()

  function updateFilter(name: string, value: string) {
    const params = new URLSearchParams(searchParams)
    value ? params.set(name, value) : params.delete(name)
    router.push(`${pathname}?${params}`)
  }

  return (
    <select onChange={e => updateFilter('status', e.target.value)}>
      <option value="">All</option>
      <option value="pending">Pending</option>
      <option value="shipped">Shipped</option>
    </select>
  )
}
```

---

## Checklists

### New Feature (Full-Stack)

**Backend:**
- [ ] Rich domain model with state predicates
- [ ] State as records (not booleans)
- [ ] Zod schemas for validation
- [ ] Server Actions (not API routes)

**Frontend:**
- [ ] Server Component for data fetching
- [ ] Content constants (no hardcoded text)
- [ ] loading.tsx and error.tsx
- [ ] Form with validation

### Code Review

- [ ] Server Components where possible
- [ ] No unnecessary `'use client'`
- [ ] Server Actions for mutations
- [ ] `tenantId` in all queries
- [ ] Content constants used
- [ ] Input validated with Zod

---

## Quick Reference

```
SERVER COMPONENT (default)
├── Async data fetching
├── Direct database access
├── No useState/useEffect
└── Forms with Server Actions

CLIENT COMPONENT ('use client')
├── useState, useEffect
├── Event handlers with state
├── useFormStatus, useActionState
└── Browser APIs

SERVER ACTIONS ('use server')
├── Mutations
├── revalidatePath() after changes
├── requireAuth() for protection
└── Return { success, data/error }

RICH DOMAIN MODELS
├── Factory: static findById(), create()
├── Predicates: get isPaid(), canShip()
├── Transitions: pay(), ship(), cancel()
└── Reload: private reload()
```

---

## Commands

```bash
npm run dev           # Development
npm run build         # Production build
npm run type-check    # TypeScript check
npm run test          # Run tests
npx prisma studio     # Database GUI
npx prisma migrate dev # Run migrations
```

---

**Full guide:** See `KREATIVREASON-GUIDE.md` for comprehensive documentation.
