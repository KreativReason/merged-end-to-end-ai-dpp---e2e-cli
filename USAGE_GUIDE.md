# Usage Guide

Step-by-step examples for using the KreativReason E2E Pipeline.

---

## Prerequisites

1. Plugin installed: `/plugin install github:KreativReason/merged-end-to-end-ai-dpp---e2e-cli`
2. Plugin enabled: `/plugin enable kreativreason-e2e-pipeline`
3. Python with Pydantic: `pip install pydantic`

---

## Phase 1: Genesis (New Project from Interview)

### Step 1: Prepare Interview Transcript

Create a markdown file with the client interview:

```bash
mkdir -p interviews
```

**Example: `interviews/booking-platform.md`**
```markdown
# Client Interview - Booking Platform
Date: 2025-01-15
Client: John Doe (john@example.com)

## Requirements Discussed

**Q: What problem are you trying to solve?**
A: We need a platform where users can book appointments with service providers...

**Q: Who are your target users?**
A: Both service providers and customers looking for services...

**Q: What features are essential for launch?**
A: User registration, provider profiles, booking calendar, payment processing...
```

### Step 2: Run Genesis Pipeline

```bash
/kreativreason:genesis
```

The pipeline will prompt you for:
- Interview transcript path
- Project name
- Output directory

**What happens:**

| Step | Agent | Output | Approval |
|------|-------|--------|----------|
| 1 | PRD | `docs/prd.json` | Required |
| 2 | Flow | `docs/flow.json` | - |
| 3 | ERD | `docs/erd.json` | Required |
| 4 | Journey | `docs/journey.json` | - |
| 5 | Planner | `docs/tasks.json` | Required |
| 6 | ADR | `docs/adr.json` | - |
| 7 | Scaffolder | `docs/scaffold-plan.json` | Required |
| 8 | Build | Complete project | - |

### Step 3: Review and Approve Artifacts

At each approval gate, review the generated JSON:

```bash
# View PRD
cat docs/prd.json | jq .

# Validate PRD
python app/lint_prd.py docs/prd.json

# View ERD
cat docs/erd.json | jq .

# Validate ERD
python app/lint_erd.py docs/erd.json
```

### Step 4: Generated Project

After scaffolding, your project is ready:

```
~/Projects/booking-platform/
├── src/                      # Application code
├── docs/                     # Copied artifacts
│   ├── prd.json
│   ├── erd.json
│   └── tasks.json
├── CLAUDE.md                 # Claude Code context
├── package.json              # Dependencies
└── ...
```

### Step 5: Push to GitHub

```bash
cd ~/Projects/booking-platform
git init
git add .
git commit -m "Initial scaffold from Genesis pipeline"
git remote add origin https://github.com/yourorg/booking-platform.git
git push -u origin main
```

---

## Phase 2: Development (Existing Project)

### Plan a Feature

```bash
/kreativreason:plan "Add OAuth authentication with Google and GitHub"
```

Creates a structured implementation plan with:
- Task breakdown
- File modifications needed
- Testing strategy
- Dependencies

### Execute the Plan

```bash
/kreativreason:work
```

Executes the plan:
- Creates git worktree for isolation
- Implements changes step by step
- Runs tests continuously
- Creates PR when complete

### Code Review

```bash
/kreativreason:review
```

Runs 11 specialized reviewers in parallel:

| Reviewer | Focus |
|----------|-------|
| Security Sentinel | OWASP, injection, auth vulnerabilities |
| Performance Oracle | N+1 queries, memory leaks, caching |
| Architecture Strategist | ADR alignment, coupling, patterns |
| Code Simplicity | YAGNI, over-engineering |
| Data Integrity | Schema safety, migrations |
| TypeScript Reviewer | TS patterns, type safety |
| Python Reviewer | PEP standards, Pythonic code |
| Rails Reviewer | Rails conventions |
| Frontend Races | Async bugs, race conditions |
| Pattern Recognition | Design pattern issues |
| DHH Rails | Rails best practices |

### Process Review Findings

```bash
/kreativreason:triage
```

Organizes findings into actionable todos by priority.

---

## Common Workflows

### Adding a New Feature

```bash
# 1. Plan the feature
/kreativreason:plan "Add user notification system with email and push"

# 2. Execute the plan
/kreativreason:work

# 3. Review before merge
/kreativreason:review

# 4. Fix any issues
/kreativreason:triage
```

### Fixing a Bug

```bash
# 1. Plan the fix
/kreativreason:plan "Fix payment processing timeout on slow connections"

# 2. Execute
/kreativreason:work

# 3. Review
/kreativreason:review
```

### Transitioning from Genesis

After running genesis, set up for ongoing development:

```bash
/kreativreason:handoff
```

This:
- Copies necessary artifacts
- Sets up project-specific agents
- Configures development environment

---

## Manual Validation

Run validators outside the pipeline:

```bash
# Validate PRD
python app/lint_prd.py docs/prd.json

# Validate ERD
python app/lint_erd.py docs/erd.json

# Apply scaffold manually
python scripts/scaffold_apply.py \
  --plan docs/scaffold-plan.json \
  --prd docs/prd.json \
  --erd docs/erd.json \
  --approved-by "ProductOwner" \
  --approved-by "TechLead" \
  --output docs/scaffold-applied.json \
  --project-dir ~/Projects/my-app
```

---

## Using Individual Agents

Invoke specific agents directly:

```bash
# Security review only
@agents/review/security-sentinel.md

# Performance analysis
@agents/review/performance-oracle.md

# TypeScript code review
@agents/review/kieran-typescript-reviewer.md
```

---

## Skills

Skills provide reusable capabilities:

| Skill | Purpose |
|-------|---------|
| `git-worktree` | Isolated branch development |
| `file-todos` | Structured todo management |
| `validation` | JSON/Pydantic validation |
| `artifact-sync` | Cross-artifact consistency |
| `frontend-design` | Design system reference |
| `gemini-imagegen` | Mockup generation |
| `compound-docs` | Pattern documentation |
| `skill-creator` | Create new skills |

---

## Troubleshooting

### "Approval required"

The pipeline pauses at approval gates. Review the artifact and continue:

```bash
# Check artifact
cat docs/prd.json | jq '.data.features'

# Continue after review (the pipeline will prompt)
```

### "Validation failed"

```bash
# Check specific errors
python app/lint_prd.py docs/prd.json

# Common issues:
# - Missing required fields
# - Invalid ID format (should be FR-001, not fr-001)
# - Duplicate IDs
```

### "Agent not found"

```bash
# Verify plugin is enabled
/plugin list

# Re-enable if needed
/plugin enable kreativreason-e2e-pipeline
```

---

## Example: Complete Genesis Run

```bash
# 1. Start Claude Code in any directory
claude

# 2. Enable plugin
/plugin enable kreativreason-e2e-pipeline

# 3. Run genesis
/kreativreason:genesis

# Provide when prompted:
# - Interview: interviews/saas-platform.md
# - Project name: "SaaS Platform"
# - Output: ~/Projects/saas-platform

# 4. Review PRD when generated
# (Pipeline pauses for approval)

# 5. Continue through each stage
# (Approving at each gate)

# 6. Final output
cd ~/Projects/saas-platform
npm install
npm run dev
```

---

## Next Steps

- [SETUP.md](SETUP.md) - Installation and configuration
- [WORKFLOW.md](WORKFLOW.md) - Team collaboration patterns
- [CLAUDE.md](CLAUDE.md) - Claude Code project instructions
