# E2E Test Command

> Execute end-to-end UI tests by running through all defined user flows with Playwright

## Command: `/kreativreason:e2e`

## Usage

```
/kreativreason:e2e <url> [options]
```

**Examples:**
```
/kreativreason:e2e http://localhost:3000
/kreativreason:e2e http://localhost:3000 --flow=FLOW-001
/kreativreason:e2e http://localhost:3000 --journey=JRN-001
/kreativreason:e2e https://staging.myapp.com --all
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `url` | Yes | Base URL of the application to test |
| `--flow` | No | Test specific flow by ID (e.g., FLOW-001) |
| `--journey` | No | Test specific journey by ID (e.g., JRN-001) |
| `--all` | No | Run all flows (default if no filter specified) |
| `--headless` | No | Run in headless mode (default: false for visibility) |
| `--screenshots` | No | Screenshot mode: all, failures, none (default: all) |

## Description

The E2E command reads your project's journey and flow artifacts, then systematically executes each user flow using Playwright. It validates:

- UI elements exist and are interactive
- Forms accept input and submit correctly
- Navigation works as expected
- API calls succeed (network monitoring)
- Backend responses are correct
- Error states are handled properly

## Workflow

### Phase 0: Load Test Context (A Priori Memory)

The E2E command relies on genesis artifacts that were transferred to the child project during scaffolding. These artifacts provide the "a priori memory" - the project knows its flows and journeys from birth.

```
1. Load genesis artifacts from docs/:
   - docs/flow.json    → User/system flows (FLOW-001, FLOW-002, etc.)
   - docs/journey.json → User journeys with touchpoints (JRN-001, etc.)
   - docs/prd.json     → Feature context (FR-XXX references)
   - docs/erd.json     → Entity context (for data validation)

2. Parse all defined flows and journeys
3. Build test execution plan based on:
   - Journey touchpoints → Test steps
   - Flow actions → Playwright commands
   - Expected outcomes → Assertions

4. Display summary and confirm with user
```

**Note**: If artifacts are missing, the scaffolder may not have transferred them. Run `/kreativreason:genesis` with the latest plugin version to ensure artifacts are copied to the child project.

### Phase 1: Environment Setup

```
1. Launch Playwright browser (visible by default)
2. Navigate to base URL
3. Verify application is accessible
4. Take baseline screenshot
5. Check for console errors on initial load
```

### Phase 2: Execute Flows

For each flow in the test plan:

```
┌─────────────────────────────────────────────────────────┐
│  FLOW: User Registration (FLOW-001)                     │
├─────────────────────────────────────────────────────────┤
│  Step 1: Navigate to /register                          │
│    → browser_navigate                                    │
│    → browser_snapshot (verify page elements)            │
│    → browser_take_screenshot                            │
│    → browser_console_messages (check errors)            │
│                                                          │
│  Step 2: Fill registration form                         │
│    → browser_snapshot (find form fields)                │
│    → browser_fill_form (email, password, etc.)          │
│    → browser_take_screenshot                            │
│                                                          │
│  Step 3: Submit form                                    │
│    → browser_click (submit button)                      │
│    → browser_network_requests (verify API call)         │
│    → Wait for response                                  │
│    → browser_take_screenshot                            │
│                                                          │
│  Step 4: Verify success state                           │
│    → browser_snapshot (check success message/redirect)  │
│    → browser_console_messages (no errors)               │
│    → browser_take_screenshot                            │
└─────────────────────────────────────────────────────────┘
```

### Phase 3: Validation at Each Step

| Check | Tool | Pass Criteria |
|-------|------|---------------|
| Page loads | `browser_navigate` | No timeout, status 200 |
| Elements exist | `browser_snapshot` | Required elements in accessibility tree |
| Forms work | `browser_fill_form` | Fields accept input |
| Buttons click | `browser_click` | Element responds |
| API calls succeed | `browser_network_requests` | 2xx response, correct payload |
| No JS errors | `browser_console_messages` | No error-level messages |
| Correct navigation | `browser_snapshot` | Expected URL/content after action |

### Phase 4: Generate Report

```
e2e-report/
├── summary.json           # Overall pass/fail + stats
├── flows/
│   ├── FLOW-001/
│   │   ├── result.json    # Pass/fail + details
│   │   ├── step-1.png     # Screenshots
│   │   ├── step-2.png
│   │   ├── network.json   # API calls captured
│   │   └── console.log    # Browser console
│   └── FLOW-002/
│       └── ...
└── failures/              # Failed tests only (quick review)
    └── FLOW-003-step-2.png
```

## Output Schema

### Test Summary

```json
{
  "artifact_type": "e2e_test_report",
  "status": "pass|partial|fail",
  "data": {
    "base_url": "http://localhost:3000",
    "tested_at": "ISO-8601",
    "duration": "3m 45s",
    "summary": {
      "total_flows": 8,
      "passed": 7,
      "failed": 1,
      "skipped": 0,
      "pass_rate": "87.5%"
    },
    "environment": {
      "browser": "Chromium",
      "viewport": "1280x720",
      "headless": false
    },
    "flows": [
      {
        "id": "FLOW-001",
        "name": "User Registration",
        "status": "pass",
        "duration": "12s",
        "steps_total": 5,
        "steps_passed": 5,
        "screenshots": ["step-1.png", "step-2.png", "step-3.png"]
      },
      {
        "id": "FLOW-002",
        "name": "User Login",
        "status": "fail",
        "duration": "8s",
        "steps_total": 4,
        "steps_passed": 2,
        "failed_at": {
          "step": 3,
          "action": "Click login button",
          "expected": "Redirect to /dashboard",
          "actual": "Stayed on /login with error",
          "error": "API returned 401 Unauthorized",
          "screenshot": "FLOW-002-step-3-failure.png"
        }
      }
    ],
    "api_calls": [
      {
        "flow": "FLOW-001",
        "step": 3,
        "method": "POST",
        "url": "/api/auth/register",
        "status": 201,
        "duration": "234ms"
      },
      {
        "flow": "FLOW-002",
        "step": 3,
        "method": "POST",
        "url": "/api/auth/login",
        "status": 401,
        "duration": "89ms",
        "error": "Invalid credentials"
      }
    ],
    "console_errors": [
      {
        "flow": "FLOW-002",
        "step": 3,
        "level": "error",
        "message": "Unhandled promise rejection: AuthError"
      }
    ]
  }
}
```

### Individual Flow Result

```json
{
  "flow_id": "FLOW-001",
  "name": "User Registration",
  "journey_id": "JRN-001",
  "status": "pass",
  "steps": [
    {
      "step": 1,
      "action": "Navigate to /register",
      "status": "pass",
      "checks": {
        "page_loaded": true,
        "elements_found": ["email-input", "password-input", "submit-btn"],
        "console_errors": 0,
        "screenshot": "step-1.png"
      }
    },
    {
      "step": 2,
      "action": "Fill registration form",
      "status": "pass",
      "inputs": {
        "email": "test@example.com",
        "password": "***"
      },
      "checks": {
        "fields_filled": true,
        "validation_errors": 0,
        "screenshot": "step-2.png"
      }
    },
    {
      "step": 3,
      "action": "Submit form",
      "status": "pass",
      "checks": {
        "button_clicked": true,
        "api_called": true,
        "api_response": 201,
        "screenshot": "step-3.png"
      }
    },
    {
      "step": 4,
      "action": "Verify redirect to /dashboard",
      "status": "pass",
      "checks": {
        "url_changed": true,
        "expected_url": "/dashboard",
        "actual_url": "/dashboard",
        "success_message_visible": true,
        "screenshot": "step-4.png"
      }
    }
  ]
}
```

## Flow-to-Test Mapping

The command automatically maps flow definitions to Playwright actions:

| Flow Step Type | Playwright Action |
|----------------|-------------------|
| `navigate` | `browser_navigate` |
| `click` | `browser_click` (finds element via snapshot) |
| `fill_form` | `browser_fill_form` |
| `type` | `browser_type` |
| `wait` | `browser_wait` |
| `verify_url` | Check URL after action |
| `verify_element` | `browser_snapshot` + check |
| `verify_text` | `browser_snapshot` + text match |
| `verify_api` | `browser_network_requests` |

## Test Data Handling

For form inputs and test data:

```json
{
  "test_data": {
    "user_registration": {
      "email": "e2e-test-{{timestamp}}@example.com",
      "password": "TestPassword123!",
      "name": "E2E Test User"
    },
    "user_login": {
      "email": "existing-user@example.com",
      "password": "ExistingPassword123!"
    }
  }
}
```

**Placeholders:**
- `{{timestamp}}` - Unix timestamp (unique emails)
- `{{uuid}}` - Random UUID
- `{{random}}` - Random string

## Handling Authentication

For flows requiring auth:

```
1. Check if flow requires authenticated user
2. If yes, run login flow first (or use saved session)
3. Continue with authenticated flow
4. Option to save session for reuse
```

## Example Session

```
/kreativreason:e2e http://localhost:3000

> Loading test artifacts...
>   Found: docs/flow.json (8 flows)
>   Found: docs/journey.json (3 journeys)
>
> Test Plan:
>   FLOW-001: User Registration (5 steps)
>   FLOW-002: User Login (4 steps)
>   FLOW-003: Create Campaign (7 steps)
>   FLOW-004: Connect Facebook Account (6 steps)
>   ... (4 more)
>
> Total: 8 flows, 42 steps
> Estimated time: ~4 minutes
>
> Start E2E tests? [Y/n]

> Launching browser...
> Testing FLOW-001: User Registration
>   Step 1/5: Navigate to /register ✓
>   Step 2/5: Fill email field ✓
>   Step 3/5: Fill password field ✓
>   Step 4/5: Click submit button ✓
>   Step 5/5: Verify dashboard redirect ✓
> FLOW-001: PASS (12s)
>
> Testing FLOW-002: User Login
>   Step 1/4: Navigate to /login ✓
>   Step 2/4: Fill credentials ✓
>   Step 3/4: Click login button ✗
>     ERROR: API returned 401
>     Screenshot: e2e-report/failures/FLOW-002-step-3.png
> FLOW-002: FAIL (8s)
>
> ... (continues)
>
> ═══════════════════════════════════════════
> E2E TEST RESULTS
> ═══════════════════════════════════════════
> Total:  8 flows
> Passed: 7 (87.5%)
> Failed: 1
>
> Failed Flows:
>   FLOW-002: User Login
>     - Step 3: Login API returned 401
>     - Screenshot: e2e-report/failures/FLOW-002-step-3.png
>
> Full report: e2e-report/summary.json
> ═══════════════════════════════════════════
>
> Next steps:
>   1. /kreativreason:debug http://localhost:3000/login "Login returns 401"
>   2. Review screenshots in e2e-report/
>   3. Fix and re-run: /kreativreason:e2e http://localhost:3000 --flow=FLOW-002
```

## Integration

- **Before release**: Run full E2E suite to catch regressions
- **After `/kreativreason:work`**: Verify implementation works end-to-end
- **CI/CD**: Run with `--headless` flag for automation
- **Debug failures**: Use `/kreativreason:debug` for failed flows

## Playwright Tools Used

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Go to URLs |
| `browser_snapshot` | Get accessibility tree (find elements) |
| `browser_click` | Click buttons, links |
| `browser_type` | Type into fields |
| `browser_fill_form` | Fill multiple form fields |
| `browser_take_screenshot` | Capture visual evidence |
| `browser_console_messages` | Check for JS errors |
| `browser_network_requests` | Monitor API calls |
| `browser_wait` | Wait for conditions |

## Error Recovery

If a step fails:
1. Capture screenshot immediately
2. Log console errors
3. Log network state
4. Continue to next flow (don't abort entire suite)
5. Mark flow as failed in report

## Prerequisites

- Application must be running at the base URL
- **Genesis artifacts must exist in `docs/`** (transferred during scaffolding):
  - `docs/flow.json` - Required for flow-based testing
  - `docs/journey.json` - Required for journey-based testing
  - `docs/prd.json` - Feature context (optional but recommended)
  - `docs/erd.json` - Entity context (optional but recommended)
- Playwright MCP server must be configured (already in plugin)

**If artifacts are missing**: The child project was scaffolded before artifact transfer was implemented. Either:
1. Re-run `/kreativreason:genesis` with plugin v2.3.0+
2. Manually copy artifacts from plugin's `projects/{project}/docs/` to child's `docs/`
