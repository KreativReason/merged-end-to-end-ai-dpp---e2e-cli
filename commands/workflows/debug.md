# Debug Session Command

## Command: `/kreativreason:debug`

Launch an interactive browser debug session to investigate issues with screenshots, console logs, and network monitoring.

## Usage

```
/kreativreason:debug <url> [issue_description]
```

**Examples:**
```
/kreativreason:debug http://localhost:3000/login "Google OAuth not redirecting"
/kreativreason:debug http://localhost:3000 "Page fails to load after auth"
```

## Workflow

### Phase 1: Session Setup

1. **Launch browser** and navigate to target URL
2. **Capture initial state**:
   - Take screenshot of landing page
   - Get accessibility snapshot
   - Capture any console errors

### Phase 2: Interactive Investigation

Use these Playwright tools to debug:

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Go to URLs |
| `browser_snapshot` | Get page structure (what's rendered) |
| `browser_take_screenshot` | Visual evidence |
| `browser_console_messages` | JS errors, warnings, logs |
| `browser_network_requests` | API calls, redirects, failures |
| `browser_click` | Interact with elements |
| `browser_type` | Fill forms |
| `browser_fill_form` | Fill multiple fields |

### Phase 3: Evidence Collection

For each step, collect:
```
1. Screenshot → evidence/step-{n}.png
2. Console logs → Look for errors
3. Network → Check API responses, redirects
4. Snapshot → What elements are visible
```

### Phase 4: Diagnosis Report

Output findings as:

```json
{
  "artifact_type": "debug_session",
  "status": "issue_found|working_as_expected|needs_more_info",
  "data": {
    "url": "http://localhost:3000/login",
    "issue": "Google OAuth not redirecting",
    "environment": {
      "browser": "Chromium",
      "timestamp": "ISO-8601"
    },
    "steps": [
      {
        "action": "Navigate to /login",
        "screenshot": "step-1.png",
        "console_errors": [],
        "network_issues": []
      },
      {
        "action": "Click Google OAuth button",
        "screenshot": "step-2.png",
        "console_errors": ["Error: redirect_uri_mismatch"],
        "network_issues": ["GET /api/auth/google → 400 Bad Request"]
      }
    ],
    "findings": {
      "root_cause": "OAuth redirect_uri not matching Google Console config",
      "evidence": "Console shows redirect_uri_mismatch error",
      "suggested_fix": "Update authorized redirect URIs in Google Cloud Console"
    }
  }
}
```

## Quick Debug Flow (OAuth Issues)

For OAuth specifically:

```
1. browser_navigate → Login page
2. browser_snapshot → Find OAuth button
3. browser_click → Click OAuth button
4. browser_network_requests → Check redirect chain
5. browser_console_messages → Check for errors
6. browser_take_screenshot → Capture error state
```

**Common OAuth issues to check:**
- `redirect_uri_mismatch` → URI not registered in provider
- `invalid_client` → Client ID wrong or not configured
- CORS errors → Backend not handling preflight
- Cookie issues → SameSite/Secure flags
- Network blocked → CSP or firewall

## Integration

- Pairs with `bug-reproduction-validator` agent for structured bug reports
- Evidence can be attached to bug tickets
- Use before `/kreativreason:bugfix` to understand the issue
