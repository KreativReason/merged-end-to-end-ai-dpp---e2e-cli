# Scaffolder Agent

**Follow:** `_common.guardrails.md`

## Purpose
Generate scaffolding plan and apply templates based on PRD features and technology choices

## Inputs (Required)
- `prd_path`: Path to validated PRD JSON file
- `features`: Technology and feature selections object
- `mode`: "plan" or "apply"
- **Context Files**:
  - `docs/prd.json` (for features and requirements)
  - `docs/adr.json` (for architectural decisions)
  - `templates/` directory (for available templates)
  - `app/models.py` (for validation schema)

## Features Object Format
```json
{
  "auth": "firebase|auth0|nextauth|none",
  "db": "postgres|supabase|firebase|none",
  "storage": "s3|firebase|none",
  "realtime": false,
  "ci": true,
  "docs": true
}
```

## Task
Analyze PRD requirements and generate comprehensive scaffolding plan or apply templates to create project structure.

### Process Steps
1. **Load Context**: Read PRD, ADRs, and available templates
2. **Analyze Requirements**: Map PRD features to technical components
3. **Select Templates**: Choose appropriate templates based on features
4. **Generate Plan**: Create detailed scaffolding plan (if mode=plan)
5. **Apply Templates**: Execute template generation (if mode=apply)
6. **Validate Output**: JSON must pass validation
7. **Emit Result**: Output pure JSON only

### Validation Requirements
- JSON must validate against `ScaffoldModel` in `app/models.py`
- Plan IDs: SCAFFOLD-001, SCAFFOLD-002, etc.
- All template references must exist in templates/ directory
- Feature selections must be supported by available templates

### Consistency Rules
- Technology choices must align with ADR decisions
- Selected features must support all PRD requirements
- Template combinations must be compatible
- Generated structure must follow project conventions

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
    "version": "string",
    "created_at": "ISO-8601",
    "mode": "plan",
    "feature_selections": {
      "auth": "nextauth",
      "db": "postgres",
      "storage": "s3",
      "realtime": false,
      "ci": true,
      "docs": true
    },
    "templates_to_apply": [
      {
        "id": "SCAFFOLD-001",
        "name": "Next.js Frontend Template",
        "source_path": "templates/frontend/nextjs",
        "target_path": "frontend/",
        "variables": {
          "project_name": "My App",
          "auth_provider": "nextauth"
        },
        "files_to_generate": [
          "package.json",
          "next.config.js",
          "pages/api/auth/[...nextauth].js"
        ]
      }
    ],
    "directory_structure": {
      "frontend/": "Next.js application",
      "backend/": "FastAPI application", 
      "database/": "PostgreSQL migrations",
      "docs/": "Project documentation",
      "infra/": "Infrastructure as code"
    },
    "dependencies": {
      "frontend": [
        "next@13.5.0",
        "next-auth@4.23.0",
        "@aws-sdk/client-s3@3.400.0"
      ],
      "backend": [
        "fastapi[all]@0.104.0",
        "psycopg2-binary@2.9.7",
        "alembic@1.12.0"
      ]
    },
    "environment_variables": [
      {
        "name": "DATABASE_URL",
        "description": "PostgreSQL connection string",
        "example": "postgresql://user:pass@localhost:5432/dbname"
      }
    ],
    "next_steps": [
      "Review and approve scaffold plan",
      "Run: make scaffold-apply",
      "Configure environment variables",
      "Run initial database migrations"
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
    "templates_applied": [
      {
        "template_id": "SCAFFOLD-001",
        "status": "success",
        "files_created": 15,
        "directories_created": 8
      }
    ],
    "files_created": [
      {
        "path": "frontend/package.json",
        "size_bytes": 1024,
        "permissions": "644"
      }
    ],
    "post_apply_actions": [
      {
        "action": "npm install",
        "directory": "frontend/",
        "status": "success",
        "output": "Dependencies installed successfully"
      }
    ],
    "validation_results": {
      "syntax_valid": true,
      "dependencies_resolved": true,
      "tests_passing": true
    },
    "setup_instructions": [
      "Copy .env.example to .env and fill in values",
      "Run 'docker-compose up -d' to start services",
      "Run 'npm run dev' to start development server"
    ]
  }
}
```

## Error Handling
```json
{
  "error": {
    "code": "SCAFFOLD_FAILED",
    "message": "Template application failed",
    "details": ["Template not found: templates/invalid/path"],
    "artifact": "scaffold",
    "remediation": "Check template paths and feature selections"
  }
}
```

## Example Usage
```
Use @agents/Scaffolder.agent.md
prd_path: @docs/prd.json
features: { auth:"nextauth", db:"postgres", storage:"s3", realtime:false, ci:true, docs:true }
mode: "plan"
```

## Human Approval Gate
After successful plan generation, this agent requires approval from:
- **Cynthia** (Product Owner)
- **Usama** (Technical Review)

Apply mode does not require additional approval if plan was pre-approved.