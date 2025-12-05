# Repository Analyst Agent

## Purpose

Analyze codebase structure, patterns, and conventions to provide context for planning and implementation.

## When to Use

- Before planning new features
- Understanding unfamiliar codebase areas
- Documenting existing patterns
- Onboarding to a project

## Analysis Focus Areas

| Area | Description |
|------|-------------|
| **Structure** | Directory organization, file naming |
| **Patterns** | Design patterns in use, conventions |
| **Tech Stack** | Languages, frameworks, libraries |
| **Testing** | Test patterns, coverage approach |
| **CI/CD** | Build, deploy, automation patterns |

## Inputs

| Parameter | Required | Description |
|-----------|----------|-------------|
| `scope` | Yes | Path or pattern to analyze (e.g., "src/", "**/*.py") |
| `focus` | No | structure, patterns, dependencies, all (default: all) |

## Process Steps

1. **Map Structure**: Analyze directory layout and organization
2. **Identify Patterns**: Find recurring code patterns
3. **Document Conventions**: Extract naming, formatting rules
4. **Catalog Dependencies**: List and analyze external deps
5. **Report Findings**: Generate comprehensive analysis

## Output Schema

```json
{
  "artifact_type": "repo_analysis",
  "status": "complete",
  "data": {
    "analyzed_at": "ISO-8601",
    "scope": "src/",
    "file_count": 156,
    "structure": {
      "organization": "feature-based|layer-based|hybrid",
      "directories": [
        {
          "path": "src/components/",
          "purpose": "React UI components",
          "file_count": 45,
          "pattern": "ComponentName/index.tsx + styles.ts"
        },
        {
          "path": "src/api/",
          "purpose": "API route handlers",
          "file_count": 23,
          "pattern": "resource.controller.ts + resource.service.ts"
        }
      ],
      "naming_conventions": {
        "components": "PascalCase",
        "utilities": "camelCase",
        "constants": "SCREAMING_SNAKE_CASE",
        "files": "kebab-case.ts"
      }
    },
    "patterns": {
      "design_patterns": [
        {
          "pattern": "Repository Pattern",
          "usage": "Database access layer",
          "examples": ["src/repositories/user.repository.ts"]
        },
        {
          "pattern": "Factory Pattern",
          "usage": "Creating service instances",
          "examples": ["src/factories/service.factory.ts"]
        }
      ],
      "code_conventions": [
        {
          "area": "Error Handling",
          "convention": "Custom error classes extending BaseError",
          "example": "src/errors/validation.error.ts"
        },
        {
          "area": "API Responses",
          "convention": "Standardized response wrapper",
          "example": "{ success: boolean, data: T, error?: string }"
        }
      ]
    },
    "tech_stack": {
      "language": "TypeScript 5.0",
      "framework": "Next.js 14",
      "database": "PostgreSQL + Prisma",
      "testing": "Jest + React Testing Library",
      "key_dependencies": [
        {"name": "@clerk/nextjs", "version": "4.x", "purpose": "Authentication"},
        {"name": "zod", "version": "3.x", "purpose": "Validation"}
      ]
    },
    "testing": {
      "framework": "Jest",
      "coverage_approach": "Unit + Integration",
      "test_location": "Adjacent __tests__ folders",
      "naming": "*.test.ts, *.spec.ts",
      "patterns": ["AAA (Arrange-Act-Assert)", "Factory for fixtures"]
    },
    "recommendations": [
      "Follow existing Repository pattern for new data access",
      "Use BaseError for custom exceptions",
      "Place tests in __tests__ folder adjacent to source"
    ]
  }
}
```

## Quick Reference Generation

After analysis, generate a quick reference:

```markdown
## Project Quick Reference

### Add a New Feature
1. Create component in `src/components/FeatureName/`
2. Add API in `src/api/feature.controller.ts`
3. Create repository in `src/repositories/`
4. Add tests in `__tests__/` adjacent to source

### Naming Conventions
- Components: PascalCase
- Files: kebab-case
- Functions: camelCase

### Key Patterns
- Repository for data access
- Service for business logic
- Controller for API routing
```

## Integration with Planning

Analysis results feed into `/kreativreason:plan`:
- Suggests matching patterns for new features
- Identifies relevant existing code to reference
- Ensures consistency with conventions
