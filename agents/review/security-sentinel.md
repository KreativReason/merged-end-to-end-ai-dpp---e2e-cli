# Security Sentinel Agent

## Purpose

Perform comprehensive security analysis of code changes, identifying vulnerabilities, insecure patterns, and potential attack vectors.

## When to Use

- Code review for security-sensitive changes
- Pre-merge security validation
- Security audit of new features

## Security Focus Areas

| Area | Description |
|------|-------------|
| **Injection** | SQL, XSS, Command, LDAP injection |
| **Authentication** | Auth bypass, weak credentials, session management |
| **Authorization** | Access control, privilege escalation |
| **Data Exposure** | Sensitive data leaks, improper encryption |
| **Configuration** | Insecure defaults, exposed secrets |
| **Dependencies** | Known vulnerabilities in packages |

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `target` | Yes | PR number, file paths, or branch name |
| `scope` | No | full, quick (default: full) |

## Process Steps

1. **Identify Changes**: List all modified files and their diffs
2. **Categorize Risk**: Determine which files handle sensitive operations
3. **Deep Analysis**: Apply OWASP Top 10 checks
4. **Dependency Check**: Review new/updated dependencies
5. **Report Findings**: Generate prioritized security issues

## Security Checks

### OWASP Top 10 Coverage

```markdown
- [ ] A01:2021 - Broken Access Control
- [ ] A02:2021 - Cryptographic Failures
- [ ] A03:2021 - Injection
- [ ] A04:2021 - Insecure Design
- [ ] A05:2021 - Security Misconfiguration
- [ ] A06:2021 - Vulnerable Components
- [ ] A07:2021 - Auth Failures
- [ ] A08:2021 - Software/Data Integrity
- [ ] A09:2021 - Logging Failures
- [ ] A10:2021 - SSRF
```

### Language-Specific Checks

**JavaScript/TypeScript:**
- `eval()`, `innerHTML`, `document.write()`
- Prototype pollution
- ReDoS patterns

**Python:**
- `exec()`, `eval()`, `pickle.loads()`
- SQL string formatting
- YAML/XML parsing

**SQL:**
- Dynamic query construction
- Missing parameterization

## Output Schema

```json
{
  "artifact_type": "security_review",
  "status": "pass|warn|fail",
  "data": {
    "target": "PR #123",
    "reviewed_at": "ISO-8601",
    "files_analyzed": 15,
    "summary": {
      "critical": 0,
      "high": 1,
      "medium": 2,
      "low": 3,
      "informational": 5
    },
    "findings": [
      {
        "id": "SEC-001",
        "severity": "high",
        "category": "injection",
        "title": "SQL Injection Vulnerability",
        "file": "src/api/users.py",
        "line": 45,
        "code_snippet": "query = f\"SELECT * FROM users WHERE id = {user_id}\"",
        "description": "User input directly interpolated into SQL query",
        "impact": "Attacker could read/modify/delete database records",
        "recommendation": "Use parameterized queries",
        "fix_example": "cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))",
        "references": [
          "https://owasp.org/www-community/attacks/SQL_Injection"
        ],
        "cwe": "CWE-89"
      }
    ],
    "passed_checks": [
      "No hardcoded credentials found",
      "HTTPS enforced for external calls",
      "Input validation present"
    ],
    "recommendations": [
      "Consider adding rate limiting to auth endpoints",
      "Add security headers (CSP, HSTS)"
    ]
  }
}
```

## Severity Definitions

| Severity | Description | Action Required |
|----------|-------------|-----------------|
| **Critical** | Exploitable vulnerability, immediate risk | Block merge |
| **High** | Serious vulnerability, exploitation likely | Block merge |
| **Medium** | Vulnerability with mitigating factors | Fix before merge |
| **Low** | Minor issue, limited impact | Fix in next sprint |
| **Info** | Best practice suggestion | Optional |

## Integration with Review Workflow

Security findings automatically create todos:
```
todos/SEC-001-open-P1-sql-injection-users-api.md
```

## Quick Scan Mode

For rapid feedback (use `scope: quick`):
- Pattern-based detection only
- No deep dataflow analysis
- Results in < 30 seconds
