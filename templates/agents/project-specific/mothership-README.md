# Mothership Connection

This directory maintains the "umbilical cord" connection between this generated project and its parent pipeline (mothership).

## What is the Mothership?

The **mothership** is the End-to-End Agentic Development Pipeline that generated this project. It contains:

- **Agent specifications** - Templates for Feature, Coding, Bugfix agents
- **Pydantic models** - Validation schemas for all artifacts
- **ADR decisions** - Architecture decisions about the pipeline itself
- **Scaffolding system** - Templates and scripts for project generation
- **Common guardrails** - Shared rules for AI agent behavior

## Umbilical Cord Architecture (ADR-0003)

This project follows the **Genetic Information Architecture** pattern:

### Inherited (Read-Only)
These artifacts are **inherited** from the mothership and should not be modified:

- `docs/adr/mothership.json` - Pipeline architecture decisions
  - ADR-0001: Meta-Development Project Factory System
  - ADR-0002: Two-Stage Scaffolding Architecture
  - ADR-0003: Agent Inheritance and Project Lifecycle Management
  - ADR-0004: Beta Testing Improvements and Production Readiness
  - ADR-0010: ADR Separation Architecture (Mothership vs Project)

### Project-Specific (Mutable)
These artifacts are **specific to this project** and can be modified:

- `docs/adr/project.json` - Project architecture decisions
- `docs/prd.json` - Product requirements
- `docs/erd.json` - Database schema (German field names)
- `docs/flow.json` - User and system flows
- `docs/journey.json` - User journeys
- `docs/tasks.json` - Implementation tasks

### Customized (Derived from Mothership)
These files are **based on mothership templates** but customized for this project:

- `agents/*.agent.md` - Project-specific agent specifications
- `.cursorrules` - AI behavior rules for this project
- `app/models.py` (if copied) - Pydantic validation models

## Connection Information

**Mothership Location:**
```
/Users/hermannrohr/Documents/End to End Pipeline Human in the Loop
```

**Generated At:** 2025-10-16T15:05:42Z

**Pipeline Version:** 1.0.0

## ADR Pattern (Approach B)

This project uses **Approach B: Directory-Based ADR Separation**:

```
docs/adr/
├── mothership.json    ← Inherited pipeline decisions (READ-ONLY)
├── project.json       ← Project-specific decisions (MUTABLE)
└── README.md          ← Pattern documentation
```

**Why two files?**
- **Separation of concerns**: Framework decisions vs application decisions
- **Independent ID namespaces**: Each file has its own ADR-0001, ADR-0002, etc.
- **Clear boundaries**: File name shows scope (inherited vs custom)
- **Scalability**: Supports multi-layer project hierarchies

See `docs/adr/README.md` for complete documentation.

## Syncing with Mothership

### Checking for Updates

The mothership may release updates to:
- Agent specifications (improved prompts, new features)
- Pydantic models (new validation rules)
- Common guardrails (new best practices)
- Scaffolding templates (bug fixes, enhancements)

To check for updates:
```bash
# (Not yet implemented - future feature)
make mothership-sync --check
```

### Applying Updates

When mothership updates are available:
```bash
# Review changes
make mothership-sync --preview

# Apply updates
make mothership-sync --apply

# Review changelog
cat mothership/CHANGELOG.md
```

### Breaking Changes

The mothership will notify of breaking changes that may require:
- Pydantic model migrations
- Agent specification updates
- ADR pattern changes
- Security rule updates

**Action Required:** Review `mothership/CHANGELOG.md` and follow migration guides.

## Reporting (Future Feature)

This project can report progress back to the mothership for:
- Linear project management integration
- Cross-project analytics
- Resource allocation tracking
- Pipeline improvement insights

**Currently disabled** - See `connection.json` for configuration.

## Self-Replicating Capability

This project inherits the ability to spawn sub-agents for feature development:

1. **Feature Agent** - Generates new feature specifications
2. **Coding Agent** - Implements tasks with tests
3. **Bugfix Agent** - Diagnoses and fixes bugs

These agents follow the same patterns as the mothership, creating a **distributed development model**.

## Project-Specific Customizations

This project has customizations beyond the mothership template:

### German-Language-First Architecture
- **Database fields**: German names (aktuelleJaehrlicheEinnahmen, kundengewinnungskosten)
- **UI labels**: All German text
- **Code variables**: English for developer readability
- **Comments**: German field explanations in JSDoc

### Multi-Tenancy Pattern
- **organizationId**: Required in all data entities
- **Firestore security rules**: Enforce organization isolation
- **Clerk organizations**: Map 1:1 to coaching companies
- **Admin access**: Role-based cross-org queries

### Formula Preservation Protocol
- **ROI calculations**: Exact MVP formulas preserved
- **Verification**: Tested against Excel spreadsheet reference
- **No refactoring**: Formula changes require explicit approval
- **Documentation**: Business logic commented in code

## Technology Stack Decisions

Decisions made by this project (see `docs/adr/project.json`):

| Decision | ADR | Rationale |
|----------|-----|-----------|
| Clerk Authentication | ADR-0001 | Built-in organization management, NextJS 14 integration |
| Firebase Backend | ADR-0002 | NoSQL for German fields, serverless functions, storage |
| German-First Architecture | ADR-0003 | Preserves spreadsheet field names, eliminates translation errors |
| Org-Advisor Multi-Tenancy | ADR-0004 | Security, performance, Clerk integration |
| Formula Preservation | ADR-0005 | Verified accuracy, user trust, minimal migration risk |

## Support

**Mothership Documentation:**
- https://docs.claude.com/claude-code

**Issues & Bugs:**
- https://github.com/anthropics/claude-code/issues

**Mothership Contact:**
- hermann@kreativreason.com

## Version History

- **v1.0.0** (2025-10-16) - Initial project generation
  - 80 files created
  - 43 directories established
  - Complete planning artifacts (PRD, ERD, Flow, Journey, Tasks, ADR)
  - Project-specific agents (Feature, Coding, Bugfix)
  - .cursorrules configured
  - Mothership connection established

## Next Steps

1. **Environment Setup** - Configure Firebase and Clerk
2. **Install Dependencies** - Run `npm install`
3. **Deploy Infrastructure** - Firebase rules, indexes, functions
4. **Implement Features** - Follow `docs/tasks.json` sprint plan
5. **Maintain Connection** - Periodically sync with mothership updates

---

**This project was generated by the End-to-End Agentic Development Pipeline.**

*From client transcript to deployable structure in a single pipeline execution.* 🚀
