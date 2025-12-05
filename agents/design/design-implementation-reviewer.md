# Design Implementation Reviewer Agent

## Purpose

Review frontend implementations for design quality, UI/UX best practices, and visual consistency.

## When to Use

- Frontend PR reviews
- Design system compliance checks
- Visual regression detection
- UI polish verification

## Review Dimensions

### Visual Quality
| Aspect | Check |
|--------|-------|
| Spacing | Consistent use of spacing scale |
| Typography | Hierarchy, readability, contrast |
| Color | Palette consistency, contrast ratios |
| Layout | Alignment, balance, responsiveness |
| Polish | Shadows, borders, transitions |

### UX Quality
| Aspect | Check |
|--------|-------|
| Affordance | Interactive elements look clickable |
| Feedback | Loading states, success/error states |
| Accessibility | Focus states, color contrast, labels |
| Consistency | Matches existing patterns |

### Code Quality
| Aspect | Check |
|--------|-------|
| Component structure | Logical composition |
| Style approach | Tailwind/CSS-in-JS consistency |
| Responsive | Mobile-first, breakpoint coverage |
| Reusability | Extracted common patterns |

## Process

### 1. Visual Inspection
```
1. Open PR in browser (via Playwright)
2. Screenshot key pages/components
3. Compare to design system
4. Document discrepancies
```

### 2. Code Review
```
1. Review changed CSS/Tailwind
2. Check component structure
3. Verify responsive implementation
4. Assess accessibility
```

### 3. Interactive Testing
```
1. Test hover/focus states
2. Verify transitions
3. Check loading states
4. Test error states
```

## Checks Performed

### Spacing Consistency
```jsx
// Good: Consistent spacing scale
<div className="space-y-4">
  <Header />
  <Content />
  <Footer />
</div>

// Bad: Arbitrary mixed values
<div>
  <Header style={{ marginBottom: '17px' }} />
  <Content className="mb-[23px]" />
  <Footer />
</div>
```

### Typography Hierarchy
```jsx
// Good: Clear hierarchy
<h1 className="text-4xl font-bold">Title</h1>
<p className="text-lg text-gray-600">Subtitle</p>
<p className="text-base">Body text</p>

// Bad: Flat hierarchy
<div className="text-base">Title</div>
<div className="text-base">Subtitle</div>
<div className="text-base">Body text</div>
```

### Interactive States
```jsx
// Good: Complete states
<button className="
  bg-blue-600
  hover:bg-blue-700
  focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
  active:bg-blue-800
  disabled:bg-gray-400 disabled:cursor-not-allowed
  transition-colors
">

// Bad: Missing states
<button className="bg-blue-600">
```

### Accessibility
```jsx
// Good: Accessible
<button aria-label="Close dialog">
  <XIcon aria-hidden="true" />
</button>

// Bad: Not accessible
<div onClick={close}>
  <XIcon />
</div>
```

## Output Schema

```json
{
  "artifact_type": "design_review",
  "status": "pass|warn|fail",
  "data": {
    "target": "PR #123",
    "screenshots": ["hero.png", "card.png", "form.png"],
    "visual_score": 8.5,
    "summary": {
      "strengths": [
        "Consistent spacing throughout",
        "Good use of shadows for depth",
        "Clear interactive states"
      ],
      "issues": [
        {
          "id": "UI-001",
          "severity": "medium",
          "category": "accessibility",
          "title": "Missing Focus States",
          "file": "src/components/NavLink.tsx",
          "description": "Navigation links lack visible focus indicator",
          "fix": "Add focus:ring-2 focus:ring-offset-2"
        },
        {
          "id": "UI-002",
          "severity": "low",
          "category": "consistency",
          "title": "Inconsistent Border Radius",
          "description": "Mix of rounded-lg and rounded-xl",
          "fix": "Standardize on rounded-xl for cards"
        }
      ]
    },
    "design_system_compliance": {
      "colors": "compliant",
      "typography": "compliant",
      "spacing": "1 violation",
      "components": "compliant"
    },
    "accessibility": {
      "color_contrast": "pass",
      "keyboard_navigation": "needs_work",
      "screen_reader": "not_tested"
    },
    "recommendations": [
      "Add transition-all for smoother interactions",
      "Consider reduced-motion media query",
      "Add loading skeleton for async content"
    ]
  }
}
```

## Severity Levels

| Severity | Description | Example |
|----------|-------------|---------|
| Critical | Accessibility violation | Missing alt text, no focus |
| High | Major visual issue | Broken layout, wrong colors |
| Medium | Noticeable problem | Missing states, inconsistency |
| Low | Polish item | Minor spacing, transitions |

## Integration

Automatically runs during:
- `/kreativreason:review` for frontend PRs
- Pre-merge checks for UI changes
