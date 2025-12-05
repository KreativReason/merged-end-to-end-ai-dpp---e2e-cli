# Changelog

All notable changes to the End-to-End Agentic Development Pipeline (Mothership) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Linear integration for task synchronization
- Template library expansion (React Native, ChatBot, E-commerce)
- Automated testing for generated projects
- Performance monitoring dashboard

---

## [1.2.0] - 2025-10-16

### Added - Agent System & Migration Protocol
- **ADR-0012**: Migration Agent and Project Update Protocol
  - Created `agents/Migration.agent.md` for managing project updates
  - Update protocol: check → preview → apply workflow
  - Breaking change management with migration scripts
  - Template conflict resolution strategies
  - Backup and rollback mechanisms
- **ADR-0011**: Agent System Template Implementation (SCAFFOLD-012)
  - Created `templates/agents/project-specific/` directory
  - 7 new template files for project agent systems:
    - `_common.guardrails.md` - Shared rules (JSON-only, German fields, multi-tenancy)
    - `Feature.agent.md` - Feature addition agent
    - `Coding.agent.md` - Implementation agent with TypeScript/Firebase patterns
    - `Bugfix.agent.md` - Bug fix agent with severity levels
    - `.cursorrules` - AI behavior configuration
    - `connection.json` - Umbilical cord connection metadata
    - `mothership-README.md` - Connection documentation
  - SCAFFOLD-012 now included in all scaffolding plans
- **CHANGELOG.md**: This file for tracking mothership improvements

### Fixed
- **scaffold_apply.py** (Lines 159-173): Fixed file placement bug
  - Files now correctly placed according to `target_path` in templates
  - Proper path combination logic prevents duplicate path segments
  - Affected 16 files in Richtungswechsel ROI Tracker project

### Changed
- **Mothership ADR**: Updated with 2 new architectural decisions
  - Total ADRs: 7 (was 5)
  - Index table updated with descending date order
  - decisions_added and index_entries arrays updated

### Impact on Generated Projects
- **Breaking Change**: Projects generated before v1.2.0 lack agent system
- **Migration Path**: Use Migration.agent.md to add agent system to existing projects
- **Benefit**: All new projects now autonomous development environments per ADR-0003

---

## [1.1.0] - 2025-10-16

### Added - ADR Separation Architecture
- **ADR-0010**: ADR Separation Architecture (Mothership vs Project)
  - Dual-file pattern: `docs/adr/mothership.json` + `docs/adr/project.json`
  - Independent ID namespaces (no more conflicts)
  - `scope` field distinguishes mothership vs project ADRs
  - Dual format support: markdown (mothership) + JSON (project)
- **Pydantic Models**: Updated for dual-format ADR support
  - Added `scope` field: `"mothership" | "project"`
  - Made `decisions` optional (for markdown format)
  - Added `adr_file_content`, `decisions_added`, `index_entries`

### Fixed
- **ID Conflicts**: Eliminated overlapping ADR IDs between mothership and projects
- **Scaffolder Ambiguity**: Clear distinction which ADRs to copy to generated projects

### Changed
- **File Structure**: ADRs now in `docs/adr/` directory (was `docs/adr.json`)
- **Agent Behavior**: ADR.agent.md and Scaffolder.agent.md updated for new pattern

### Impact on Generated Projects
- **Non-Breaking**: Existing projects continue to work
- **Recommendation**: Migrate existing projects to use Approach B pattern
- **Benefit**: Clear inheritance model, no ID conflicts

---

## [1.0.0] - 2025-10-12

### Added - Production Readiness (Beta Testing Improvements)
- **ADR-0004**: Beta Testing Improvements and Production Readiness
  - Token-safe Flow.agent.md with file-first sharding
  - Pydantic 2.0 migration (regex → pattern, @validator → @field_validator)
  - Scaffolder directory separation (`../generated-projects/`)
  - Coding.agent.md for implementation guidance
  - .cursorrules for consistent AI behavior
  - Role clarification across all documentation
- **scripts/scaffold_apply.py**: Two-stage scaffolding execution
  - Human approval gate enforcement (Cynthia + Usama)
  - Placeholder file generation for all file types
  - Pydantic validation of PRD/ERD/Plan inputs
- **Validation Results**: Tested on Nonna Call Center Voice Agent AI
  - 20 entities, 23 relationships (ERD)
  - 11 user flows + 8 system flows (149 steps)
  - Zero token limit errors
  - Zero Pydantic validation errors

### Changed
- **app/models.py**: Pydantic 2.0 compatibility (40+ field updates)
- **agents/Flow.agent.md**: File-first architecture (docs/flows/user/, docs/flows/system/)
- **Makefile**: Added scaffold-plan and scaffold-apply targets
- **README.md**: Updated team roles and pipeline status

### Fixed
- **Token Limits**: Flow artifacts no longer exceed chat output limits
- **Directory Pollution**: Scaffolding creates files in correct directory
- **Role Inconsistency**: Standardized team roles across all documentation

### Impact on Generated Projects
- **Breaking Change**: Pydantic 2.0 required (Python 3.9+)
- **Migration Path**: Update imports and validators in existing projects
- **Benefit**: Production-ready, scalable, consistent behavior

---

## [0.9.0] - 2024-09-12

### Added - Core Pipeline Architecture
- **ADR-0001**: Meta-Development Project Factory System
  - Core pipeline: Client Transcript → PRD → Flow → ERD → Journey → Tasks → ADR → Scaffolded Project
  - Human approval gates for each phase
  - Reference architecture: nextjs-firebase-ai-coding-template
- **ADR-0002**: Two-Stage Scaffolding Architecture
  - Stage 1: Planning agent (suggestion only)
  - Stage 2: Build agent (execution only)
  - Approval gate: Cynthia + Usama
- **ADR-0003**: Agent Inheritance and Project Lifecycle Management
  - Genetic Information Architecture
  - Umbilical cord connection (mothership/ directory)
  - Self-replicating capability
- **Core Agents**: 9 specialized agents
  - PRD.agent.md - Product requirements
  - Flow.agent.md - User/system flows
  - ERD.agent.md - Database schema
  - Journey.agent.md - User journeys
  - Planner.agent.md - Task breakdown
  - ADR.agent.md - Architecture decisions
  - Scaffolder.agent.md - Project generation
  - Coding.agent.md - Implementation
  - _common.guardrails.md - Shared rules

### Security
- **Approval Gates**: Human review required for PRD, ERD, Tasks, Scaffolding, Code
- **Validation**: Pydantic models enforce artifact structure
- **Stable IDs**: Prevent duplicate features/stories/tasks

---

## [0.1.0] - 2024-09-10

### Added - Initial Pipeline Prototype
- Project factory concept
- Basic PRD generation
- Template directory structure
- Agent specification framework

---

## Update Categories

### Breaking Changes 🔴
Changes that require migration scripts or manual intervention:
- Pydantic model schema changes
- Required field additions
- File path relocations
- Agent specification structural changes

### Non-Breaking Changes 🟢
Changes that can be auto-applied with backup:
- Template improvements
- Documentation updates
- Optional new features
- Performance optimizations

### Security Updates 🟡
Critical vulnerability fixes requiring immediate attention:
- Dependency version bumps
- Authentication improvements
- Validation enhancements

---

## Migration Guide

### From 1.1.0 to 1.2.0
**Agent System Addition** (Non-breaking for new projects, manual for existing)

1. **Check mothership version**:
   ```bash
   cat mothership/connection.json | grep version
   ```

2. **Preview migration**:
   ```bash
   # (Future) Use Migration.agent.md
   # For now, manually copy templates:
   cp -r /path/to/mothership/templates/agents/project-specific/* ./
   ```

3. **Update files**:
   - Copy 7 agent system files to project root
   - Update mothership/connection.json version to 1.2.0
   - Update last_sync timestamp

### From 1.0.0 to 1.1.0
**ADR Separation** (Non-breaking)

1. **Check ADR structure**:
   ```bash
   ls docs/adr/
   ```

2. **If using old structure** (docs/adr.json):
   ```bash
   # Backup existing
   cp docs/adr.json docs/adr-backup.json

   # Create new structure
   mkdir -p docs/adr/
   # Split ADRs by scope (manual review recommended)
   ```

### From 0.9.0 to 1.0.0
**Pydantic 2.0 Migration** (Breaking)

1. **Update Python**: Requires Python 3.9+
2. **Update dependencies**:
   ```bash
   pip install pydantic==2.0+
   ```
3. **Update imports**:
   ```python
   # Change:
   from pydantic import validator
   # To:
   from pydantic import field_validator
   ```
4. **Update validators**:
   ```python
   # Change:
   @validator('field_name')
   # To:
   @field_validator('field_name', mode='after')
   ```
5. **Update Field definitions**:
   ```python
   # Change:
   Field(regex=r'^[A-Z]')
   # To:
   Field(pattern=r'^[A-Z]')
   ```

---

## Reporting Issues

Found a bug or have a suggestion? Please report it:

1. **GitHub Issues**: https://github.com/anthropics/claude-code/issues
2. **Email**: hermann@kreativreason.com
3. **Include**:
   - Mothership version (from connection.json)
   - Generated project details
   - Steps to reproduce
   - Error messages

---

## Versioning Strategy

- **MAJOR** (X.0.0): Breaking changes requiring migration
- **MINOR** (1.X.0): New features, non-breaking changes
- **PATCH** (1.0.X): Bug fixes, documentation updates

---

**Last Updated**: 2025-10-16
**Current Version**: 1.2.0
**Maintainers**: Hermann Rohr (hermann@kreativreason.com)
