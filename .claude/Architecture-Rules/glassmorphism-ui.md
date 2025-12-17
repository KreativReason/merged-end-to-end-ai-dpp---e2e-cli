# Glassmorphism UI Design System

**Vivavolt 2.0 - Pink Brand Theme**

This document defines the glassmorphism design patterns and conventions for the frontend. **All UI components must follow these guidelines.**

---

## Brand Colors

### Primary Pink Brand Color

```
#ff206e - Primary pink (use for titles, accents, icons, badges)
```

### Color Usage

```css
/* Text colors */
text-[#ff206e]              /* Primary titles, headers */
text-[#ff206e]/60           /* Secondary icons, subtle accents */
text-gray-800               /* Primary body text */
text-gray-600               /* Secondary text */
text-gray-500               /* Muted text */

/* Background tints */
bg-[#ff206e]/5              /* Very subtle pink background */
bg-[#ff206e]/10             /* Light pink background for badges */
bg-pink-50/50               /* Table header background */
bg-pink-50/30               /* Hover states */

/* Border colors */
border-[#ff206e]/20         /* Pink accent borders */
border-[#ff206e]/30         /* Stronger pink borders */
border-pink-200/30          /* Subtle pink borders */
border-pink-100/30          /* Very subtle dividers */
border-pink-100/20          /* Table row borders */
```

---

## Core Components

### 1. FloatingOrbs Background

Always include the `FloatingOrbs` component for pages using glassmorphism:

```jsx
import FloatingOrbs from '@/components/ui/FloatingOrbs'

// Usage - wrap content in relative container
;<div className="relative">
  <FloatingOrbs />
  <GlassCard className="relative z-10">{/* Content */}</GlassCard>
</div>
```

### 2. GlassCard Container

Primary container for content sections:

```jsx
import { GlassCard } from '@/components/ui/glass-card'

;<GlassCard className="relative z-10 bg-white/70 backdrop-blur-xl border-pink-200/30 shadow-xl shadow-pink-500/10">
  {/* Content */}
</GlassCard>
```

**Required classes for glass containers:**

- `bg-white/70` - Semi-transparent white
- `backdrop-blur-xl` - Frosted glass blur effect
- `border-pink-200/30` - Subtle pink border
- `shadow-xl shadow-pink-500/10` - Pink glow shadow for 3D depth
- `relative z-10` - Ensure content appears above FloatingOrbs

### 3. GlassBadge

Use `GlassBadge` instead of standard `Badge`:

```jsx
import { GlassBadge } from '@/components/ui/glass-card'

// Variants
<GlassBadge variant="default">Default</GlassBadge>
<GlassBadge variant="success">Success</GlassBadge>
<GlassBadge variant="danger">Danger</GlassBadge>
<GlassBadge variant="warning">Warning</GlassBadge>
<GlassBadge variant="info">Info</GlassBadge>
<GlassBadge variant="pink">Pink Accent</GlassBadge>

// Custom pink brand styling
<GlassBadge variant="pink" className="bg-[#ff206e]/10 text-[#ff206e] border-[#ff206e]/30">
  Custom Pink
</GlassBadge>
```

---

## UI Patterns

### Table Styling

```jsx
<Table>
  <TableHeader>
    <TableRow className="bg-pink-50/50 hover:bg-pink-50/70 border-b border-pink-100/30">
      <TableHead className="text-[#ff206e] font-semibold">Column</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow className="hover:bg-pink-50/30 transition-colors border-b border-pink-100/20">
      <TableCell className="text-gray-600">Content</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

### Dialog/Modal Styling

```jsx
<DialogContent className="bg-white/90 backdrop-blur-xl border-pink-200/30 shadow-2xl shadow-pink-500/10">
  <DialogHeader>
    <DialogTitle className="text-[#ff206e]">Title</DialogTitle>
    <DialogDescription className="text-gray-600">Description</DialogDescription>
  </DialogHeader>
</DialogContent>
```

### Button Styling

**Primary Action Button (Green gradient for approve/confirm):**

```jsx
<Button className="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white shadow-lg shadow-green-500/25 hover:shadow-green-500/40 transition-all transform hover:scale-[1.02] active:scale-[0.98]">
  Approve
</Button>
```

**Ghost/Secondary Button (Pink accent):**

```jsx
<Button
  variant="ghost"
  className="text-[#ff206e] hover:bg-[#ff206e]/10 hover:text-[#ff206e] transition-all"
>
  View
</Button>
```

**Outline Button (Neutral):**

```jsx
<Button variant="outline" className="border-gray-300 hover:bg-gray-50 transition-all">
  Cancel
</Button>
```

**Pink Gradient Button (for pink brand actions):**

```jsx
<Button className="bg-gradient-to-r from-[#ff206e] to-pink-600 hover:from-pink-600 hover:to-pink-700 text-white shadow-lg shadow-pink-500/25 hover:shadow-pink-500/40 transition-all transform hover:scale-[1.02] active:scale-[0.98]">
  Action
</Button>
```

### Card Sections (in dialogs/details)

```jsx
<div className="p-4 rounded-xl bg-[#ff206e]/5 border border-[#ff206e]/20 backdrop-blur-sm">
  <h4 className="font-semibold text-[#ff206e]">Section Title</h4>
  <p className="text-gray-700">Content</p>
</div>
```

### Lead/Detail Cards

```jsx
<div
  className={`p-4 rounded-xl border-2 backdrop-blur-sm transition-all ${
    isHighlighted
      ? 'border-green-400/50 bg-green-50/50 shadow-lg shadow-green-500/10'
      : 'border-gray-200/50 bg-gray-50/50 shadow-lg shadow-gray-500/5'
  }`}
>
  {/* Card content */}
</div>
```

### Icons with Pink Accent

```jsx
<User className="h-4 w-4 text-[#ff206e]" />        {/* Primary icon */}
<Mail className="h-3 w-3 text-[#ff206e]/60" />     {/* Secondary icon */}
```

---

## Loading States

```jsx
<div className="relative min-h-[400px]">
  <FloatingOrbs />
  <GlassCard className="relative z-10 bg-white/70 backdrop-blur-xl border-pink-200/30 shadow-lg shadow-pink-500/5">
    <CardContent className="flex justify-center items-center py-12">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-pink-500"></div>
    </CardContent>
  </GlassCard>
</div>
```

---

## Empty States

```jsx
<div className="relative min-h-[400px]">
  <FloatingOrbs />
  <GlassCard className="relative z-10 bg-white/70 backdrop-blur-xl border-pink-200/30 shadow-lg shadow-pink-500/5">
    <CardHeader>
      <CardTitle className="text-[#ff206e]">Title</CardTitle>
    </CardHeader>
    <CardContent>
      <div className="text-center py-8 text-gray-500">
        <Icon className="h-12 w-12 mx-auto mb-4 text-green-500" />
        <p className="text-lg font-medium">Empty State Message</p>
        <p className="text-sm text-gray-400 mt-2">Description</p>
      </div>
    </CardContent>
  </GlassCard>
</div>
```

---

## Required Imports

```jsx
// Glass components
import { GlassCard, GlassBadge } from '@/components/ui/glass-card'
import FloatingOrbs from '@/components/ui/FloatingOrbs'

// Standard components (still needed for structure)
import { CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from '@/components/ui/dialog'
```

---

## Checklist for New UI Components

- [ ] Import `FloatingOrbs` and wrap content appropriately
- [ ] Use `GlassCard` instead of plain `Card` for main containers
- [ ] Apply `bg-white/70 backdrop-blur-xl` for glass effect
- [ ] Use `border-pink-200/30` for pink-tinted borders
- [ ] Add `shadow-xl shadow-pink-500/10` for pink glow depth
- [ ] Use `text-[#ff206e]` for titles and accents
- [ ] Replace `Badge` with `GlassBadge` variants
- [ ] Style buttons with gradient backgrounds and hover effects
- [ ] Add `transition-all` for smooth animations
- [ ] Include `hover:scale-[1.02] active:scale-[0.98]` for 3D button effects
- [ ] Use pink-tinted table headers and row hover states
- [ ] Apply glassmorphism to dialogs/modals

---

## Anti-Patterns (Do NOT Do)

```jsx
// WRONG - Plain card without glass effect
<Card>
  <CardContent>...</CardContent>
</Card>

// CORRECT - Glass card with proper styling
<GlassCard className="bg-white/70 backdrop-blur-xl border-pink-200/30 shadow-xl shadow-pink-500/10">
  <CardContent>...</CardContent>
</GlassCard>

// WRONG - Standard Badge
<Badge variant="destructive">Error</Badge>

// CORRECT - GlassBadge
<GlassBadge variant="danger">Error</GlassBadge>

// WRONG - Hardcoded colors without brand
<div className="text-amber-600">Title</div>

// CORRECT - Brand pink color
<div className="text-[#ff206e]">Title</div>

// WRONG - Flat button without depth
<Button className="bg-green-600">Submit</Button>

// CORRECT - 3D gradient button with shadow
<Button className="bg-gradient-to-r from-green-500 to-green-600 shadow-lg shadow-green-500/25 hover:scale-[1.02]">
  Submit
</Button>
```

---

## File Locations

| Component                  | Path                               |
| -------------------------- | ---------------------------------- |
| FloatingOrbs               | `@/components/ui/FloatingOrbs.jsx` |
| GlassCard, GlassBadge      | `@/components/ui/glass-card.jsx`   |
| Global CSS (glass classes) | `@/app/globals.css`                |

---

## Summary

1. **Always use FloatingOrbs** background for glassmorphism pages
2. **Use GlassCard** instead of Card for containers
3. **Apply pink brand color** (#ff206e) for accents
4. **Use GlassBadge** variants instead of Badge
5. **Style buttons with gradients** and 3D hover effects
6. **Add backdrop-blur** for frosted glass effect
7. **Include pink shadows** for depth and glow
8. **Use transitions** for smooth interactions
