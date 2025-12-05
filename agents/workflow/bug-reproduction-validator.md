# Bug Reproduction Validator Agent

## Purpose

Systematically validate bug reproductions by following reproduction steps and confirming the bug exists before attempting fixes.

## When to Use

- Before starting bug fixes
- Validating reported bugs
- Creating reproduction steps
- QA verification

## Workflow

```
1. Read bug report
2. Set up environment
3. Follow reproduction steps
4. Capture evidence (screenshots, logs)
5. Confirm or invalidate bug
6. Document findings
```

## Process Steps

### 1. Environment Setup
```bash
# Ensure clean state
git stash
git checkout main
git pull

# Set up test environment
npm install
npm run dev
```

### 2. Step-by-Step Reproduction

For each step in the bug report:
```
1. Execute the step
2. Screenshot the result
3. Capture console/network logs
4. Note any deviations
```

### 3. Evidence Collection

Gather:
- Screenshots at each step
- Browser console logs
- Network request/response
- Database state (if relevant)
- Error messages

### 4. Validation Decision

| Outcome | Criteria |
|---------|----------|
| **Confirmed** | Bug reproduces as described |
| **Partially Confirmed** | Bug exists but different from report |
| **Cannot Reproduce** | Steps don't produce the bug |
| **Environment Specific** | Only reproduces in certain conditions |

## Output Schema

```json
{
  "artifact_type": "bug_validation",
  "status": "confirmed|partial|cannot_reproduce|environment_specific",
  "data": {
    "bug_id": "BUG-123",
    "title": "Login button unresponsive on mobile",
    "reported_by": "user@example.com",
    "validated_at": "ISO-8601",
    "environment": {
      "os": "macOS 14.0",
      "browser": "Chrome 120",
      "viewport": "375x667",
      "node_version": "20.10.0"
    },
    "reproduction": {
      "steps_attempted": 5,
      "steps_successful": 5,
      "deviation_notes": []
    },
    "evidence": {
      "screenshots": [
        {
          "step": 1,
          "file": "evidence/step-1-homepage.png",
          "notes": "Homepage loads correctly"
        },
        {
          "step": 4,
          "file": "evidence/step-4-button-click.png",
          "notes": "Button does not respond to tap"
        }
      ],
      "console_logs": "evidence/console.log",
      "network_log": "evidence/network.har"
    },
    "findings": {
      "bug_confirmed": true,
      "root_cause_hypothesis": "Touch event handler not attached on mobile",
      "affected_users": "All mobile users",
      "workaround": "Use desktop site"
    },
    "recommendation": "Proceed with fix - add touch event handling"
  }
}
```

## Reproduction Template

```markdown
## Bug Reproduction Report: [BUG-ID]

### Environment
- OS:
- Browser:
- Viewport:
- Commit:

### Steps Attempted

| Step | Action | Expected | Actual | Screenshot |
|------|--------|----------|--------|------------|
| 1 | Navigate to /login | Login page displays | ✓ Same | step-1.png |
| 2 | Enter credentials | Fields accept input | ✓ Same | step-2.png |
| 3 | Tap login button | Form submits | ✗ Nothing happens | step-3.png |

### Verdict: CONFIRMED

### Evidence
- Screenshots: evidence/
- Console log: Shows no click event fired
- Network: No login request sent

### Hypothesis
Touch events not handled on mobile Safari.
```

## Integration

- Used by `/kreativreason:bugfix` before starting fixes
- Generates evidence for bug tickets
- Creates baseline for regression testing
