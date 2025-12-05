# Lint Agent

## Purpose

Run and analyze linting results across the codebase, fixing auto-fixable issues and documenting others.

## When to Use

- Pre-commit validation
- PR quality checks
- Codebase health audits
- Onboarding code cleanup

## Supported Linters

### JavaScript/TypeScript
- ESLint
- Prettier
- TypeScript compiler

### Python
- Ruff (recommended)
- Black
- Flake8
- mypy

### Ruby
- RuboCop
- StandardRB

### General
- EditorConfig
- Markdownlint

## Workflow

```
1. Detect project linters (from config files)
2. Run all applicable linters
3. Auto-fix what's possible
4. Report remaining issues
5. Suggest configuration improvements
```

## Process Steps

### 1. Linter Detection

Scan for config files:
```
.eslintrc.* → ESLint
.prettierrc.* → Prettier
tsconfig.json → TypeScript
pyproject.toml → Ruff/Black/mypy
.rubocop.yml → RuboCop
```

### 2. Run Linters

```bash
# JavaScript/TypeScript
npx eslint . --ext .js,.jsx,.ts,.tsx
npx prettier --check .

# Python
ruff check .
black --check .
mypy .

# Ruby
rubocop
```

### 3. Auto-Fix

```bash
# Safe auto-fixes
npx eslint . --fix
npx prettier --write .
ruff check . --fix
black .
rubocop -a
```

### 4. Report Results

## Output Schema

```json
{
  "artifact_type": "lint_report",
  "status": "pass|warn|fail",
  "data": {
    "ran_at": "ISO-8601",
    "linters_run": ["eslint", "prettier", "typescript"],
    "summary": {
      "total_issues": 45,
      "auto_fixed": 38,
      "remaining": 7,
      "errors": 2,
      "warnings": 5
    },
    "by_linter": {
      "eslint": {
        "issues": 25,
        "fixed": 20,
        "remaining": 5
      },
      "prettier": {
        "issues": 18,
        "fixed": 18,
        "remaining": 0
      },
      "typescript": {
        "issues": 2,
        "fixed": 0,
        "remaining": 2
      }
    },
    "remaining_issues": [
      {
        "linter": "eslint",
        "rule": "no-unused-vars",
        "severity": "error",
        "file": "src/utils/legacy.ts",
        "line": 45,
        "message": "'oldFunction' is defined but never used",
        "suggestion": "Remove unused function or add eslint-disable comment"
      },
      {
        "linter": "typescript",
        "code": "TS2322",
        "severity": "error",
        "file": "src/types/api.ts",
        "line": 23,
        "message": "Type 'string' is not assignable to type 'number'",
        "suggestion": "Fix type mismatch"
      }
    ],
    "auto_fixes_applied": {
      "files_modified": 12,
      "changes": [
        "Formatted 18 files with Prettier",
        "Fixed 15 ESLint auto-fixable rules",
        "Sorted 5 import statements"
      ]
    },
    "recommendations": [
      "Add 'unused-vars' to pre-commit hook",
      "Consider enabling stricter TypeScript settings",
      "Update ESLint to latest version"
    ]
  }
}
```

## Common Issues & Fixes

### ESLint
| Rule | Auto-fix | Manual Action |
|------|----------|---------------|
| `semi` | ✓ | - |
| `quotes` | ✓ | - |
| `no-unused-vars` | ✗ | Remove or use |
| `no-explicit-any` | ✗ | Add proper type |

### Prettier
All issues auto-fixable with `--write`

### TypeScript
| Error | Auto-fix | Manual Action |
|-------|----------|---------------|
| Type mismatch | ✗ | Fix types |
| Missing types | ✗ | Add types |
| Unused imports | ✓ (with plugin) | Remove |

## Integration

- Runs automatically in `/kreativreason:work` before commits
- Part of `/kreativreason:review` quality checks
- Can be run standalone for codebase cleanup
