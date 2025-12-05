# Frontend Design Skill

## Purpose

Provide design system knowledge, component patterns, and UI best practices for frontend development.

## Capabilities

### Design System Reference

Access to common design patterns:
- Component libraries (shadcn/ui, Radix, Headless UI)
- CSS frameworks (Tailwind, CSS Modules)
- Animation libraries (Framer Motion, CSS transitions)
- Icon systems (Lucide, Heroicons)

### Component Patterns

```jsx
// Card Pattern
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>Content</CardContent>
  <CardFooter>Actions</CardFooter>
</Card>

// Form Pattern
<Form onSubmit={handleSubmit}>
  <FormField>
    <FormLabel>Label</FormLabel>
    <FormInput />
    <FormError />
  </FormField>
  <Button type="submit">Submit</Button>
</Form>
```

### Layout Patterns

```jsx
// Page Layout
<div className="min-h-screen flex flex-col">
  <Header />
  <main className="flex-1">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {children}
    </div>
  </main>
  <Footer />
</div>

// Sidebar Layout
<div className="flex h-screen">
  <aside className="w-64 border-r">Sidebar</aside>
  <main className="flex-1 overflow-auto">Content</main>
</div>
```

### Spacing System

| Name | Value | Use Case |
|------|-------|----------|
| `space-1` | 4px | Tight grouping |
| `space-2` | 8px | Related elements |
| `space-4` | 16px | Section padding |
| `space-6` | 24px | Card padding |
| `space-8` | 32px | Section gaps |
| `space-12` | 48px | Major sections |

### Color Usage

```jsx
// Semantic Colors
text-foreground     // Primary text
text-muted-foreground // Secondary text
bg-background       // Page background
bg-card            // Card background
bg-primary         // Primary actions
bg-destructive     // Destructive actions
border             // Default borders
ring               // Focus rings
```

### Typography Scale

```jsx
// Headings
<h1 className="text-4xl font-bold tracking-tight">H1</h1>
<h2 className="text-3xl font-semibold">H2</h2>
<h3 className="text-2xl font-semibold">H3</h3>
<h4 className="text-xl font-semibold">H4</h4>

// Body
<p className="text-base leading-7">Body</p>
<p className="text-sm text-muted-foreground">Small</p>
<p className="text-xs">Extra small</p>
```

### Interactive States

```jsx
// Button States
<button className="
  bg-primary text-primary-foreground
  hover:bg-primary/90
  focus-visible:outline-none focus-visible:ring-2
  focus-visible:ring-ring focus-visible:ring-offset-2
  disabled:pointer-events-none disabled:opacity-50
  transition-colors
">
  Button
</button>
```

### Animation Patterns

```jsx
// Fade in
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.3 }}
>

// Slide up
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
>

// CSS Transition
<div className="transition-all duration-200 ease-in-out">
```

### Responsive Patterns

```jsx
// Mobile-first
<div className="
  flex flex-col
  sm:flex-row
  lg:grid lg:grid-cols-3
  gap-4 sm:gap-6 lg:gap-8
">

// Hide/Show
<div className="hidden md:block">Desktop only</div>
<div className="md:hidden">Mobile only</div>
```

## Usage

```javascript
// Access design tokens
skill.getSpacing('lg')      // Returns '32px'
skill.getColor('primary')   // Returns color value
skill.getComponent('Card')  // Returns component pattern
```

## Integration

Used by:
- `design-iterator` agent for UI refinement
- `design-implementation-reviewer` for pattern checking
- `/kreativreason:work` for frontend tasks
