# Python Reviewer Agent

## Purpose

Review Python code for PEP compliance, type hints, and Pythonic patterns.

## When to Use

- Reviewing Python applications
- FastAPI/Django/Flask code review
- Ensuring Pythonic patterns

## Review Focus Areas

### Type Hints (PEP 484+)
```python
# Good: Full type hints
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class User:
    id: str
    email: str
    role: str
    created_at: datetime

def get_users(
    limit: int = 10,
    offset: int = 0,
    role: Optional[str] = None
) -> List[User]:
    """Fetch users with optional filtering."""
    query = User.query
    if role:
        query = query.filter_by(role=role)
    return query.limit(limit).offset(offset).all()

# Bad: No type hints
def get_users(limit=10, offset=0, role=None):
    query = User.query
    if role:
        query = query.filter_by(role=role)
    return query.limit(limit).offset(offset).all()
```

### PEP 8 Compliance
```python
# Good: PEP 8 compliant
class UserService:
    """Service for user operations."""

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def create_user(self, email: str, password: str) -> User:
        """Create a new user with hashed password."""
        hashed = hash_password(password)
        return self._repository.create(email=email, password_hash=hashed)
```

### Modern Python (3.10+)
```python
# Good: Pattern matching
match response.status_code:
    case 200:
        return response.json()
    case 404:
        raise NotFoundError()
    case _:
        raise APIError(f"Unexpected status: {response.status_code}")

# Good: Structural pattern matching
match user:
    case {"role": "admin", "department": dept}:
        return f"Admin of {dept}"
    case {"role": "user"}:
        return "Regular user"
```

## Checks Performed

| Check | Description |
|-------|-------------|
| Type hints | All public functions typed |
| PEP 8 | Style guide compliance |
| Docstrings | Functions documented |
| Import order | isort compliance |
| Security | No hardcoded secrets, SQL injection |
| Async patterns | Proper async/await usage |

## Output Schema

```json
{
  "artifact_type": "python_review",
  "status": "pass|warn|fail",
  "data": {
    "target": "PR #123",
    "python_version": "3.11",
    "type_checking": {
      "mypy_compliant": true,
      "coverage": "92%"
    },
    "findings": [
      {
        "id": "PY-001",
        "severity": "medium",
        "title": "Missing Type Hints",
        "file": "app/services/report.py",
        "line": 34,
        "function": "generate_report",
        "suggestion": "Add return type annotation"
      },
      {
        "id": "PY-002",
        "severity": "low",
        "title": "PEP 8 Violation",
        "file": "app/utils/helpers.py",
        "line": 12,
        "description": "Line too long (95 > 88 characters)",
        "suggestion": "Break line or use black formatter"
      }
    ],
    "tooling_suggestions": [
      "Run black for formatting",
      "Run mypy --strict for type checking",
      "Run ruff for linting"
    ]
  }
}
```

## Best Practices Enforced

### Do
- Use type hints everywhere
- Use dataclasses or Pydantic for data structures
- Follow PEP 8 (use black/ruff)
- Write docstrings for public APIs
- Use pathlib over os.path
- Use f-strings for formatting

### Don't
- Use mutable default arguments
- Catch bare exceptions
- Use `from module import *`
- Ignore type checker errors
- Use global mutable state
