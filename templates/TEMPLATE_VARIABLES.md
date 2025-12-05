# Template Variable System

## Overview

All templates in `templates/` use a variable substitution system to generate project-specific files during scaffolding. This document defines the available variables and conditional syntax.

## Variable Syntax

Variables use double curly braces: `{{VARIABLE_NAME}}`

Example:
```markdown
# Cursor AI Rules for {{PROJECT_NAME}}

You are an AI assistant working on the {{PROJECT_NAME}} application.
**Tech Stack:** {{FRONTEND_FRAMEWORK}} + {{DATABASE_TYPE}} + {{AUTH_PROVIDER}}
```

## Conditional Sections

Conditional blocks use special comment syntax to avoid breaking file formats:

```markdown
<!-- IF:DATABASE_TYPE=firebase -->
### Firebase-Specific Rules
- Use Firebase Admin SDK in Cloud Functions
- Use Firebase Client SDK in frontend
<!-- END:IF -->

<!-- IF:AUTH_PROVIDER=clerk -->
### Clerk Authentication
- Use middleware.ts for auth protection
- Store role in publicMetadata
<!-- END:IF -->

<!-- IF:LANGUAGE_PRIMARY=de -->
### German Language Requirements
ALL database fields MUST use German names
<!-- END:IF -->
```

## Core Variables

### Project Identity
- `{{PROJECT_NAME}}` - Full project name (e.g., "Richtungswechsel ROI Tracker - SaaS Migration")
- `{{PROJECT_SLUG}}` - URL-safe slug (e.g., "richtungswechsel-roi-tracker")
- `{{PROJECT_DESCRIPTION}}` - Brief project description
- `{{DOMAIN}}` - Business domain (e.g., "roi-tracking", "ecommerce", "crm", "chatbot")

### Technology Stack
- `{{FRONTEND_FRAMEWORK}}` - "nextjs" | "react" | "vue" | "angular" | "svelte"
- `{{FRONTEND_VERSION}}` - Version string (e.g., "14.0.4")
- `{{DATABASE_TYPE}}` - "firebase" | "postgres" | "supabase" | "mongodb" | "mysql"
- `{{AUTH_PROVIDER}}` - "clerk" | "auth0" | "nextauth" | "firebase-auth" | "supabase-auth" | "none"
- `{{STORAGE_PROVIDER}}` - "firebase-storage" | "s3" | "supabase-storage" | "cloudinary"
- `{{BACKEND_FRAMEWORK}}` - "firebase-functions" | "fastapi" | "express" | "nestjs" | "none"

### Localization
- `{{LANGUAGE_PRIMARY}}` - ISO 639-1 code (e.g., "en", "de", "es", "fr")
- `{{LANGUAGE_SECONDARY}}` - Optional secondary language
- `{{LOCALE}}` - Full locale (e.g., "en-US", "de-DE")
- `{{UI_LANGUAGE_NAME}}` - Human-readable (e.g., "German", "English")

### Multi-Tenancy
- `{{MULTI_TENANT}}` - "true" | "false"
- `{{TENANT_MODEL}}` - "organization" | "workspace" | "team" | "account"
- `{{TENANT_ISOLATION}}` - "database" | "schema" | "row-level"

### Project-Specific Features
- `{{FEATURES}}` - JSON object with boolean flags:
  ```json
  {
    "realtime": true,
    "offline_mode": false,
    "internationalization": true,
    "dark_mode": true,
    "charts": true,
    "exports": true
  }
  ```

### Mothership Connection
- `{{MOTHERSHIP_LOCATION}}` - Absolute path to parent pipeline
- `{{MOTHERSHIP_VERSION}}` - Version of pipeline that generated project
- `{{GENERATED_AT}}` - ISO-8601 timestamp of generation

### Team & Approvals
- `{{APPROVERS}}` - JSON array of approver names
- `{{PROJECT_MANAGER}}` - Name (e.g., "Cynthia")
- `{{LEAD_DEVELOPER}}` - Name (e.g., "Usama")
- `{{QA_ENGINEER}}` - Name (e.g., "Mustaffa")

## Conditional Logic Operators

### Equality
```markdown
<!-- IF:DATABASE_TYPE=firebase -->
Firebase-specific content
<!-- END:IF -->
```

### Inequality
```markdown
<!-- IF:AUTH_PROVIDER!=none -->
Authentication-specific content
<!-- END:IF -->
```

### Multiple Conditions (AND)
```markdown
<!-- IF:DATABASE_TYPE=firebase,AUTH_PROVIDER=clerk -->
Content for Firebase + Clerk combo
<!-- END:IF -->
```

### Multiple Conditions (OR)
```markdown
<!-- IF:DATABASE_TYPE=firebase|postgres|mysql -->
Content for SQL or NoSQL databases
<!-- END:IF -->
```

### Boolean Flags
```markdown
<!-- IF:MULTI_TENANT=true -->
Multi-tenancy required content
<!-- END:IF -->

<!-- IF:FEATURES.charts=true -->
Chart library configuration
<!-- END:IF -->
```

## Example: Generic vs Specific Template

### ❌ BAD: ROI-Specific Template
```markdown
# Cursor AI Rules for Richtungswechsel ROI Tracker

**Tech Stack:** NextJS 14 + Firebase + Clerk
**Domain:** Financial advisor coaching ROI tracking (German market)

### German Database Field Names (NON-NEGOTIABLE)
ALL Firestore database fields MUST use German names:
- aktuelleJaehrlicheEinnahmen
- kundengewinnungskosten
```

### ✅ GOOD: Universal Template
```markdown
# Cursor AI Rules for {{PROJECT_NAME}}

**Tech Stack:** {{FRONTEND_FRAMEWORK}} {{FRONTEND_VERSION}} + {{DATABASE_TYPE}} + {{AUTH_PROVIDER}}
**Domain:** {{PROJECT_DESCRIPTION}}

<!-- IF:LANGUAGE_PRIMARY!=en -->
### {{UI_LANGUAGE_NAME}} Database Field Names
{{#IF LANGUAGE_PRIMARY=de}}
ALL database fields MUST use German names (e.g., aktuelleJaehrlicheEinnahmen, kundengewinnungskosten)
{{/IF}}
{{#IF LANGUAGE_PRIMARY=es}}
ALL database fields MUST use Spanish names (e.g., ingresoAnualActual, costosAdquisicionClientes)
{{/IF}}
<!-- END:IF -->

<!-- IF:DATABASE_TYPE=firebase -->
### Firebase Configuration
- Use Firebase Admin SDK in Cloud Functions
- Use Firebase Client SDK in frontend
<!-- END:IF -->

<!-- IF:DATABASE_TYPE=postgres|mysql -->
### SQL Database Configuration
- Use Prisma ORM for type-safe queries
- Run migrations with Alembic/Knex
<!-- END:IF -->

<!-- IF:AUTH_PROVIDER=clerk -->
### Clerk Authentication
- Use middleware.ts for auth protection
- Store role in publicMetadata
<!-- END:IF -->

<!-- IF:MULTI_TENANT=true -->
### Multi-Tenancy ({{TENANT_MODEL}}-Based)
Every data write MUST include {{TENANT_MODEL}}Id
<!-- END:IF -->
```

## Template Processing During Scaffolding

The `scaffold_apply.py` script processes templates in two passes:

### Pass 1: Variable Substitution
Replace all `{{VARIABLE}}` patterns with actual values from scaffold plan.

### Pass 2: Conditional Block Evaluation
Evaluate all `<!-- IF:... -->` conditions and remove false blocks.

### Example Processing

**Template Input:**
```markdown
Project: {{PROJECT_NAME}}
<!-- IF:DATABASE_TYPE=firebase -->
Use Firestore
<!-- END:IF -->
<!-- IF:DATABASE_TYPE=postgres -->
Use PostgreSQL
<!-- END:IF -->
```

**Scaffold Plan Variables:**
```json
{
  "PROJECT_NAME": "My SaaS App",
  "DATABASE_TYPE": "postgres"
}
```

**Final Output:**
```markdown
Project: My SaaS App
Use PostgreSQL
```

## Adding New Variables

To add a new template variable:

1. **Define in this document** with clear description
2. **Update scaffold_apply.py** to extract from scaffold plan
3. **Add to ScaffoldPlanModel** in `app/models.py` (if needed)
4. **Document in CHANGELOG.md** as non-breaking change
5. **Update existing templates** to use new variable

## Best Practices

### DO:
✅ Use generic examples applicable to any domain
✅ Provide conditional sections for tech-specific patterns
✅ Use descriptive variable names
✅ Document domain-agnostic best practices
✅ Support multiple tech stack combinations

### DON'T:
❌ Hard-code specific project names
❌ Assume specific database types
❌ Require specific languages/locales
❌ Hard-code business domain logic
❌ Make assumptions about auth providers

## Testing Templates

Before committing template changes:

1. **Test with multiple variable sets**:
   - NextJS + Firebase + Clerk (German)
   - React + PostgreSQL + Auth0 (English)
   - Vue + Supabase + NextAuth (Spanish)

2. **Verify conditional logic**:
   - All IF blocks evaluate correctly
   - No orphaned END:IF tags
   - No conflicting conditions

3. **Check variable substitution**:
   - All {{VARIABLES}} are defined
   - No typos in variable names
   - No unsubstituted variables in output

## Related Documentation

- **[Scaffolder.agent.md](../agents/Scaffolder.agent.md)** - How scaffolding works
- **[scaffold_apply.py](../scripts/scaffold_apply.py)** - Template processing implementation
- **[app/models.py](../app/models.py)** - ScaffoldPlanModel with all variables
- **[CHANGELOG.md](../CHANGELOG.md)** - Version history of template system

---

**Version**: 1.2.0
**Last Updated**: 2025-10-16
**Maintained By**: End-to-End Agentic Development Pipeline Team
