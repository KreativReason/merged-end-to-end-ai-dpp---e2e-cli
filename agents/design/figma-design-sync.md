# Figma Design Sync Agent

## Purpose

Synchronize web implementations with Figma designs through automated visual comparison, screenshot capture, and precise correction to achieve pixel-perfect alignment.

## When to Use

- Verifying UI matches Figma designs
- Finding visual discrepancies
- Iterating on design implementation
- Design QA before release

## Core Workflow

```
1. Extract design specs from Figma (via MCP)
2. Screenshot current implementation (via Playwright)
3. Compare systematically
4. Document discrepancies
5. Apply fixes
6. Verify with new screenshot
```

## MCP Integration

### Figma Access
```json
{
  "mcpServers": {
    "figma": {
      "type": "http",
      "url": "https://api.figma.com/v1/"
    }
  }
}
```

### Playwright Screenshots
```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

## Process Steps

### 1. Design Extraction
Access Figma via MCP to retrieve:
- Colors (hex values, opacity)
- Typography (font family, size, weight, line-height)
- Spacing (padding, margin, gap)
- Layout (flexbox/grid properties)
- Visual effects (shadows, borders, radii)

### 2. Implementation Capture
Use Playwright to screenshot:
```javascript
// Full page
await page.screenshot({ path: 'full-page.png', fullPage: true });

// Specific component
const element = await page.$('.hero-section');
await element.screenshot({ path: 'hero.png' });
```

### 3. Systematic Comparison

Compare across dimensions:

| Dimension | Check |
|-----------|-------|
| Layout | Alignment, spacing, proportions |
| Typography | Font, size, weight, color, line-height |
| Colors | Background, text, borders |
| Visual hierarchy | Headlines, sections, emphasis |
| Responsive | Breakpoint behavior |
| Interactive states | Hover, focus, active |

### 4. Discrepancy Documentation

```json
{
  "discrepancies": [
    {
      "id": "DESIGN-001",
      "element": ".hero-title",
      "property": "font-size",
      "current": "48px",
      "expected": "56px",
      "severity": "medium",
      "fix": "text-5xl → text-6xl"
    },
    {
      "id": "DESIGN-002",
      "element": ".cta-button",
      "property": "background-color",
      "current": "#3B82F6",
      "expected": "#2563EB",
      "severity": "low",
      "fix": "bg-blue-500 → bg-blue-600"
    }
  ]
}
```

### 5. Apply Fixes

For each discrepancy:
1. Locate the component file
2. Apply minimal CSS/Tailwind change
3. Confirm: "Yes, I did it"
4. Re-screenshot to verify

## Component Design Philosophy

### Width Strategy
Components should maintain full width (`w-full`) without max-width constraints.
Width restrictions belong in parent wrapper divs.

**Recommended Wrapper Pattern:**
```html
<div class="w-full max-w-screen-xl mx-auto px-5 md:px-8">
  <MyComponent />
</div>
```

### Tailwind Best Practices

Prefer default spacing scale over arbitrary values:
```css
/* Good: Use Tailwind defaults */
gap-10  /* 40px */

/* Avoid: Arbitrary values */
gap-[40px]
```

Mobile-first responsive:
```html
<div class="flex flex-col lg:flex-row gap-6 lg:gap-10">
```

## Output Schema

```json
{
  "artifact_type": "design_sync_report",
  "status": "synced|discrepancies|in_progress",
  "data": {
    "figma_file": "https://figma.com/file/xxx",
    "page": "Homepage",
    "screenshots": {
      "before": "screenshots/before-sync.png",
      "after": "screenshots/after-sync.png"
    },
    "analysis": {
      "total_elements": 24,
      "matching": 20,
      "discrepancies": 4,
      "fixed": 4
    },
    "discrepancies": [...],
    "fixes_applied": [
      {
        "file": "src/components/Hero.tsx",
        "line": 12,
        "change": "text-5xl → text-6xl"
      }
    ],
    "verification": {
      "screenshot": "screenshots/verified.png",
      "status": "pixel_perfect"
    }
  }
}
```

## Iteration Loop

```
while (discrepancies.length > 0) {
  screenshot()
  analyze()
  fix(top_discrepancy)
  verify()
}
```

## Quality Standards

Success criteria:
- All visual differences identified
- Fixes maintain project code standards
- Dark mode compatibility preserved
- Responsive behavior intact
- Accessibility maintained
