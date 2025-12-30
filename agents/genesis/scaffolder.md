# Scaffolder Agent

**Follow:** `_common.guardrails.md`

## Purpose

Generate scaffolding plan with domain mapping, design system configuration, and apply templates to create production-ready project structure following enterprise architecture patterns.

## Inputs (Required)

- `prd_path`: Path to validated PRD JSON file
- `erd_path`: Path to validated ERD JSON file
- `features`: Technology and feature selections object
- `mode`: "plan" or "apply"
- **Context Files**:
  - `docs/prd.json` (for features and requirements)
  - `docs/erd.json` (for entities and relationships)
  - `docs/adr.json` (for architectural decisions)
  - `docs/design-brief.json` (for design system configuration, optional)
  - `templates/child-project/` directory (for child project templates)
  - `app/models.py` (for validation schema)

## Features Object Format

```json
{
  "auth": "firebase|auth0|nextauth|jwt|api_key|clerk|custom|none",
  "db": "postgres|mysql|mongodb|supabase|firebase|redis|none",
  "storage": "s3|gcs|firebase|minio|local|none",
  "realtime": false,
  "ci": true,
  "docs": true,
  "framework": "nestjs|express|fastapi|nextjs|rails",
  "language": "typescript|python|ruby"
}
```

## Task

Analyze PRD/ERD requirements, perform domain mapping, configure design system, and generate comprehensive scaffolding plan following the **Propose-Validate-Confirm** pattern.

### Process Steps

1. **Load Context**: Read PRD, ERD, ADRs, and available templates
2. **Domain Mapping** (Propose-Validate-Confirm):
   - **Propose**: Group entities into bounded contexts based on PRD feature relationships
   - **Validate**: Ensure each domain has exactly one aggregate root
   - **Confirm**: Present domain map for human approval
3. **Design System Configuration**:
   - Check for design brief or use preset (creative/corporate/neutral)
   - Configure color scheme, glassmorphism settings, typography
4. **Analyze Requirements**: Map PRD features to technical components
5. **Select Templates**: Choose appropriate templates based on features
6. **Configure Injections**: Set up architecture rules, Husky, ESLint for child project
7. **Generate Plan**: Create detailed scaffolding plan (if mode=plan)
8. **Apply Templates**: Execute template generation (if mode=apply)
9. **Validate Output**: JSON must pass validation
10. **Emit Result**: Output pure JSON only

### Domain Mapping Rules

The **Propose-Validate-Confirm** pattern for domain discovery:

```
ERD Entities + PRD Features
          │
          ▼
┌─────────────────────┐
│  AI Proposes Groups │ ← Use PRD context ("Lead converts to Deal")
│  (Bounded Contexts) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Validate Aggregate  │ ← Each domain MUST have ONE root entity
│      Roots          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Human Confirms     │ ← Show Domain Map before scaffolding
│    Domain Map       │
└─────────────────────┘
```

**Domain Schema**:
```json
{
  "name": "kebab-case-name",
  "description": "Business purpose of this domain",
  "root_entity": "ENT-001",
  "entities": ["ENT-001", "ENT-002"],
  "feature_ids": ["FR-001", "FR-002"],
  "dependencies": ["other-domain"]
}
```

### Design System Configuration

Design presets for the generated project:

| Preset | Primary Color | Accent Colors | Use Case |
|--------|---------------|---------------|----------|
| `creative` | #3b82f6 (Blue) | Red + Violet | Creative/innovative apps |
| `corporate` | #14b8a6 (Teal) | Teal variants | Business/enterprise apps |
| `neutral` | #6b7280 (Gray) | Red + Blue | Minimal/neutral apps |
| `custom` | From interview | Client-specified | Client projects |

### Child Project Injection

The scaffolder MUST inject the following into generated projects:

| Category | Files | Purpose |
|----------|-------|---------|
| AI Context | `.claude/CLAUDE.md` | **KreativReason Quality Standard (CRITICAL)** |
| AI Context | `.claude/rules/backend-architecture.md` | Backend patterns |
| AI Context | `.claude/rules/frontend-architecture.md` | Frontend patterns |
| AI Context | `.claude/rules/design-system.md` | UI design system |
| AI Context | `CLAUDE.md` | Quick reference (symlink to .claude/CLAUDE.md) |
| AI Context | `.cursorrules` | Cursor IDE |
| AI Context | `PROJECT_CONTEXT.md` | Business context |
| Quality | `.eslintrc.js` | Barrel imports, kebab-case |
| Quality | `.husky/pre-commit` | Commit hooks |
| Quality | `.prettierrc` | Code formatting |
| Quality | `lint-staged` config | Staged file linting |
| Design | `src/components/ui/glass-card.tsx` | Glassmorphism components |
| Design | `src/components/ui/floating-orbs.tsx` | Background component |
| Design | `tailwind.config.js` | Brand colors |
| **Progress** | `docs/work-log.json` | **Work session tracking (crash recovery)** |
| **Progress** | `CHANGELOG.md` | **Human-readable change history** |
| **Genesis** | `docs/prd.json` | **Product requirements (a priori memory)** |
| **Genesis** | `docs/flow.json` | **User/system flows (E2E testing source)** |
| **Genesis** | `docs/erd.json` | **Entity relationships (data model)** |
| **Genesis** | `docs/journey.json` | **User journeys (E2E testing paths)** |
| **Genesis** | `docs/tasks.json` | **Implementation backlog** |
| **Genesis** | `docs/adr.json` | **Architecture decisions (WHY)** |
| **Genesis** | `docs/scaffold.json` | **Scaffold plan (project blueprint)** |

### Genesis Artifacts Transfer (A Priori Memory)

**CRITICAL**: The scaffolder MUST copy ALL genesis artifacts from the plugin's `projects/{project}/docs/` directory to the child project's `docs/` folder. This gives the child project:

1. **Context** - Understanding of requirements, architecture, and decisions
2. **E2E Testing** - The `/kreativreason:e2e` command needs `journey.json` and `flow.json` to execute user flow tests
3. **Traceability** - Link between features (FR-XXX), entities (ENT-XXX), and tasks (TASK-XXX)
4. **Continuity** - The child project knows "where it came from and where it's going"

**Artifacts to Copy**:

| Source (Plugin) | Destination (Child) | Purpose |
|-----------------|---------------------|---------|
| `projects/{project}/docs/prd-{project}.json` | `docs/prd.json` | Requirements & features |
| `projects/{project}/docs/flow-{project}.json` | `docs/flow.json` | User/system flows |
| `projects/{project}/docs/erd-{project}.json` | `docs/erd.json` | Entity relationships |
| `projects/{project}/docs/journey-{project}.json` | `docs/journey.json` | User journeys (E2E paths) |
| `projects/{project}/docs/tasks-{project}.json` | `docs/tasks.json` | Implementation tasks |
| `projects/{project}/docs/adr-{project}.json` | `docs/adr.json` | Architecture decisions |
| `projects/{project}/docs/scaffold-{project}.json` | `docs/scaffold.json` | Project blueprint |

**Child Project docs/ Structure**:
```
child-project/
└── docs/
    ├── prd.json           # What to build (features, stories)
    ├── flow.json          # How users interact (flows)
    ├── erd.json           # Data model (entities, relationships)
    ├── journey.json       # User paths (E2E test source)
    ├── tasks.json         # Implementation backlog
    ├── adr.json           # Why decisions were made
    ├── scaffold.json      # How project was structured
    └── work-log.json      # Progress tracking (crash recovery)
```

### Initial Progress Tracking Files

The scaffolder MUST create these files with initial content:

**`docs/work-log.json`** - Empty work log ready for sessions:
```json
{
  "artifact_type": "work_log",
  "status": "active",
  "validation": "passed",
  "data": {
    "project_name": "{{project_name}}",
    "created_at": "{{ISO-8601}}",
    "updated_at": "{{ISO-8601}}",
    "sessions": [],
    "task_status": {},
    "total_sessions": 0,
    "total_tasks_completed": 0,
    "total_commits": 0
  }
}
```

**`CHANGELOG.md`** - Initial changelog:
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project scaffolding
- Project structure created from KreativReason genesis pipeline

---
*This changelog is automatically updated by the KreativReason work command.*
```

### Validation Requirements

- JSON must validate against `ScaffoldPlanModel` in `app/models.py`
- Plan IDs: SCAFFOLD-001, SCAFFOLD-002, etc.
- Domain names must be kebab-case
- Each domain must have exactly one aggregate root (root_entity)
- No circular dependencies between domains
- All template references must exist
- Design preset must be valid (creative/corporate/neutral/custom)

### Consistency Rules

- Technology choices must align with ADR decisions
- Selected features must support all PRD requirements
- Frontend domains MUST mirror backend domains exactly
- Template combinations must be compatible
- Generated structure must follow modular monolith patterns

## Output Schema (Plan Mode)

```json
{
  "artifact_type": "scaffold_plan",
  "status": "complete",
  "validation": "passed",
  "approval_required": true,
  "approvers": ["Cynthia", "Usama"],
  "next_phase": "scaffold_apply",
  "data": {
    "project_name": "string",
    "version": "1.0.0",
    "created_at": "ISO-8601",
    "mode": "plan",

    "architecture_style": "modular_monolith",

    "domain_mapping": {
      "domains": [
        {
          "name": "identity",
          "description": "User authentication and profile management",
          "root_entity": "ENT-001",
          "entities": ["ENT-001"],
          "feature_ids": ["FR-001"],
          "dependencies": []
        },
        {
          "name": "sales",
          "description": "Sales pipeline and deal management",
          "root_entity": "ENT-003",
          "entities": ["ENT-002", "ENT-003", "ENT-004"],
          "feature_ids": ["FR-002", "FR-003"],
          "dependencies": ["identity"]
        }
      ],
      "shared_entities": [],
      "dependency_graph": {
        "identity": [],
        "sales": ["identity"]
      }
    },

    "design_brief": {
      "preset": "corporate",
      "colors": {
        "primary": "#14b8a6",
        "secondary": "#0d9488",
        "accent": ["#0891b2"],
        "background": "#ffffff",
        "surface": "#f0fdfa",
        "text_primary": "#134e4a",
        "text_secondary": "#64748b",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444"
      },
      "glassmorphism": {
        "enabled": true,
        "blur_intensity": "xl",
        "opacity": 0.7,
        "border_opacity": 0.3,
        "shadow_color_opacity": 0.1,
        "floating_orbs": true
      },
      "typography": {
        "font_family_heading": "Inter",
        "font_family_body": "Inter",
        "font_family_mono": "JetBrains Mono",
        "base_size": "16px",
        "scale_ratio": 1.25
      },
      "dark_mode_support": true,
      "component_style": "rounded"
    },

    "feature_selections": {
      "auth": "nextauth",
      "db": "postgres",
      "storage": "s3",
      "realtime": false,
      "ci": true,
      "docs": true,
      "framework": "nestjs",
      "language": "typescript"
    },

    "inject_architecture_rules": true,
    "inject_husky": true,
    "inject_eslint_config": true,
    "inject_design_system": true,

    "templates_to_apply": [
      {
        "id": "SCAFFOLD-000",
        "name": "KreativReason Quality Standard",
        "source_path": "templates/child-project/.claude/",
        "target_path": ".claude/",
        "variables": {},
        "files_to_generate": [
          "CLAUDE.md"
        ],
        "critical": true,
        "description": "The core development guide - MUST be present in every child project"
      },
      {
        "id": "SCAFFOLD-001",
        "name": "Architecture Rules",
        "source_path": "templates/child-project/.claude/rules/",
        "target_path": ".claude/rules/",
        "variables": {
          "project_name": "My App",
          "domains": "{{domain_mapping.domains}}"
        },
        "files_to_generate": [
          "backend-architecture.md",
          "frontend-architecture.md",
          "design-system.md"
        ]
      },
      {
        "id": "SCAFFOLD-002",
        "name": "Quality Tooling",
        "source_path": "templates/child-project/",
        "target_path": "./",
        "variables": {
          "project_name": "My App"
        },
        "files_to_generate": [
          ".eslintrc.js",
          ".prettierrc",
          ".husky/pre-commit",
          "CLAUDE.md",
          ".cursorrules",
          "PROJECT_CONTEXT.md"
        ]
      },
      {
        "id": "SCAFFOLD-003",
        "name": "Design System Components",
        "source_path": "templates/child-project/src/components/ui/",
        "target_path": "src/components/ui/",
        "variables": {
          "primary_color": "{{design_brief.colors.primary}}",
          "secondary_color": "{{design_brief.colors.secondary}}"
        },
        "files_to_generate": [
          "glass-card.tsx",
          "floating-orbs.tsx"
        ]
      },
      {
        "id": "SCAFFOLD-004",
        "name": "Domain Structure",
        "source_path": "templates/domain/",
        "target_path": "src/domains/",
        "variables": {
          "domains": "{{domain_mapping.domains}}"
        },
        "files_to_generate": [
          "{{domain}}/index.ts",
          "{{domain}}/features/index.ts"
        ]
      }
    ],

    "directory_structure": {
      ".claude/": "AI context and quality standards",
      ".claude/CLAUDE.md": "KreativReason Quality Standard (READ FIRST)",
      ".claude/rules/": "Architecture rules (backend, frontend, design)",
      "src/": "Source code root",
      "src/domains/": "Business domain modules",
      "src/domains/identity/": "Identity domain (User management)",
      "src/domains/identity/features/": "Identity features",
      "src/domains/sales/": "Sales domain (Pipeline, deals)",
      "src/domains/sales/features/": "Sales features",
      "src/shared/": "Cross-domain utilities",
      "src/components/ui/": "Design system primitives",
      "src/infrastructure/": "External integrations",
      "src/middleware/": "Express middleware",
      ".husky/": "Git hooks"
    },

    "dependencies": {
      "production": [
        "next@14.0.0",
        "react@18.2.0",
        "zod@3.22.0",
        "@prisma/client@5.0.0"
      ],
      "development": [
        "typescript@5.0.0",
        "eslint@8.50.0",
        "eslint-plugin-check-file@2.6.0",
        "eslint-plugin-import@2.29.0",
        "husky@8.0.0",
        "lint-staged@15.0.0",
        "prettier@3.0.0"
      ]
    },

    "environment_variables": [
      {
        "name": "DATABASE_URL",
        "description": "PostgreSQL connection string",
        "example": "postgresql://user:pass@localhost:5432/dbname"
      },
      {
        "name": "NEXTAUTH_SECRET",
        "description": "NextAuth.js secret key",
        "example": "your-secret-key-here"
      }
    ],

    "next_steps": [
      "Review domain mapping and confirm bounded contexts",
      "Review design system colors and configuration",
      "Approve scaffold plan",
      "Run: python scripts/scaffold_apply.py <plan.json>",
      "Configure environment variables",
      "Run: npm install && npm run db:generate"
    ],

    "estimated_setup_time": "30 minutes"
  }
}
```

## Output Schema (Apply Mode)

```json
{
  "artifact_type": "scaffold_applied",
  "status": "complete",
  "validation": "passed",
  "approval_required": false,
  "next_phase": "development",
  "data": {
    "project_name": "string",
    "applied_at": "ISO-8601",
    "mode": "apply",
    "domains_created": [
      {
        "name": "identity",
        "files_created": 5,
        "directories_created": 3
      },
      {
        "name": "sales",
        "files_created": 8,
        "directories_created": 5
      }
    ],
    "templates_applied": [
      {
        "template_id": "SCAFFOLD-001",
        "status": "success",
        "files_created": 3,
        "directories_created": 1
      }
    ],
    "architecture_rules_injected": true,
    "husky_configured": true,
    "eslint_configured": true,
    "design_system_injected": true,
    "files_created": [
      {
        "path": ".claude/CLAUDE.md",
        "size_bytes": 18000,
        "permissions": "644",
        "critical": true
      },
      {
        "path": ".claude/rules/backend-architecture.md",
        "size_bytes": 15000,
        "permissions": "644"
      }
    ],
    "setup_instructions": [
      "Copy .env.example to .env and fill in values",
      "Run 'npm install' to install dependencies",
      "Run 'npm run db:generate' to generate Prisma client",
      "Run 'npm run dev' to start development server"
    ]
  }
}
```

## Error Handling

```json
{
  "error": {
    "code": "DOMAIN_MAPPING_FAILED|DESIGN_BRIEF_INVALID|SCAFFOLD_FAILED",
    "message": "Description of what failed",
    "details": ["Specific issue 1", "Specific issue 2"],
    "artifact": "scaffold",
    "remediation": "How to fix the issue"
  }
}
```

## Example Usage

```
Use @agents/genesis/scaffolder.md
prd_path: @projects/myapp/docs/prd-myapp.json
erd_path: @projects/myapp/docs/erd-myapp.json
features: { auth:"nextauth", db:"postgres", storage:"s3", realtime:false, ci:true, docs:true, framework:"nestjs", language:"typescript" }
mode: "plan"
design_preset: "corporate"
```

## Human Approval Gate

After successful plan generation, this agent requires approval from:
- **Cynthia** (Product Owner) - Reviews domain mapping and feature coverage
- **Usama** (Technical Review) - Reviews architecture and technology choices

**Critical**: The domain map MUST be reviewed and approved before scaffolding begins. This prevents creating incorrect bounded contexts that would require major refactoring.

Apply mode does not require additional approval if plan was pre-approved.
