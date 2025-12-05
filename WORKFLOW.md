# Team Workflow Guide

## Context Management Strategy

This project uses a **hybrid memory system** combining local status files with git-based shared memory to maintain context across sessions and team members.

---

## The Memory System

### Local Memory (Fast Access)
**`PROJECT_STATUS.json`** - Your session-to-session memory
- Updated frequently during development
- Tracked in git for team synchronization
- Read at start of each session to understand "where we are"
- Provides instant status without parsing git history

### Shared Memory (Team Sync)
**Git Commits + GitHub** - The source of truth
- Permanent record of all changes
- Enables team collaboration across machines
- Synced to development/staging/production servers
- Provides audit trail and rollback capability

---

## Daily Workflow

### Starting Your Day

```bash
# 1. Sync with team's work
git pull origin main

# 2. Check current project status
make status

# 3. See what the team has been doing
make history

# 4. Optional: Check remote status if working on different machine
make sync-status
```

**What you'll see:**
- Current phase and sprint
- Completion percentage
- What was done in the last session
- What's next on the priority list
- Who's working on what

### During Development

**AI Updates Status Automatically**
- As tasks complete, `PROJECT_STATUS.json` gets updated
- No manual tracking required
- Timestamps and completion markers added automatically

**Manual Status Check**
```bash
# Quick check
make where-am-i

# Full status
make status
```

### End of Your Session

```bash
# Update and commit status to GitHub
make save-status
```

**This automatically:**
1. Updates timestamps in `PROJECT_STATUS.json`
2. Commits the status file with descriptive message
3. Pushes to GitHub for team visibility
4. Updates deployment servers (when configured)

---

## Team Collaboration Scenarios

### Scenario 1: Multiple Developers, Same Project

**Hermann (Morning):**
```bash
git pull                    # Get latest
make status                 # "Usama finished PRD validator"
# Works on mothership structure...
make save-status           # Commit + push
```

**Usama (Afternoon):**
```bash
git pull                    # Gets Hermann's work
make status                 # "Hermann completed mothership structure"
# Reviews Hermann's PR, starts Linear integration...
make save-status           # Commit + push
```

**Cynthia (Evening, Different Location):**
```bash
git clone <repo-url>        # Fresh clone
make status                 # Sees full day's progress
# Begins approval review process...
```

### Scenario 2: Working Across Machines

**Office Computer:**
```bash
# Work on feature
make save-status
git push origin feat/templates
```

**Home Computer:**
```bash
git pull origin feat/templates
make status                  # Picks up exactly where you left off
```

### Scenario 3: Deployment Servers

**Development Server (Automated):**
```bash
# Continuous integration pulls every 5 minutes
git pull origin develop
make status                  # Shows current team status
# Run tests, deploy if passing
```

**Staging Server:**
```bash
git pull origin staging
make status                  # Shows staging-ready features
# Deploy approved features
```

---

## Makefile Commands Reference

### Status Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `make status` | Full project status display | Start of session, checking overall progress |
| `make where-am-i` | Quick status overview | Fast check during development |
| `make history` | Recent git commits | See team's recent work |
| `make sync-status` | Fetch and compare with GitHub | Working on different machine |
| `make save-status` | Commit and push status | End of session, after significant work |
| `make update-status` | Update timestamps only | Manual status refresh (rarely needed) |

### Development Commands

| Command | Purpose | Status |
|---------|---------|--------|
| `make scaffold-plan` | Generate project plan (Stage 1) | Planned |
| `make scaffold-apply` | Execute approved plan (Stage 2) | Planned |
| `make help` | Show all commands | Available |

---

## Git Conventions

### Branch Strategy

```
main (production)
├── staging (pre-production)
├── develop (integration)
│   ├── feat/nextjs-template (feature branches)
│   ├── feat/mothership-structure
│   └── fix/prd-validator
```

### Commit Message Format

**Status Updates:**
```
Update project status: template_library [2025-10-01]
```

**Feature Work:**
```
feat: Add NextJS+Firebase template with CRUD boilerplate

- Implemented authentication flow
- Added Firestore CRUD operations
- Configured environment variables

Refs: ADR-0002
```

**Bug Fixes:**
```
fix: Correct PRD validation regex for edge cases

Resolves issue where multi-line requirements were rejected
```

### Pull Request Approval Gates

Following **ADR-0001**, PRs require approval based on phase:

| Phase | Approvers |
|-------|-----------|
| PRD | Cynthia + Hermann + Usama |
| Scaffolder Plan | Cynthia + Usama |
| ERD | Cynthia + Hassan + Usama |
| Task Breakdown | Cynthia + Hermann + Usama |
| Code Merge | Mustaffa (QA) + Usama |

---

## PROJECT_STATUS.json Structure

### Key Sections

```json
{
  "meta": {
    "last_updated": "ISO timestamp",
    "last_commit": "git hash",
    "current_branch": "branch name"
  },
  "project": {
    "phase": "current development phase",
    "sprint": "current sprint name"
  },
  "progress": {
    "overall_completion": "percentage",
    "phase_status": {
      "phase_name": {
        "status": "complete|in_progress|planned",
        "icon": "✅|🔄|📋"
      }
    }
  },
  "current_session": {
    "date": "today's date",
    "completed": ["tasks done this session"],
    "in_progress": ["current work"],
    "blocked": ["blockers"]
  },
  "team_status": {
    "member_name": {
      "current_focus": "what they're working on",
      "last_activity": "date"
    }
  },
  "next_priorities": ["ordered list of next tasks"],
  "blockers": ["current blockers"],
  "notes": ["important context"]
}
```

### Updating Status

**AI handles most updates automatically, but you can manually edit:**

```bash
# Edit the file
nano PROJECT_STATUS.json

# Save and commit
make save-status
```

---

## Best Practices

### ✅ DO

- **Run `make status`** at the start of each session
- **Run `make save-status`** at the end of significant work
- **Pull before you push** to avoid conflicts
- **Update team_status** when changing focus areas
- **Add blockers** immediately when you encounter them
- **Keep next_priorities** updated with realistic tasks

### ❌ DON'T

- Don't skip `git pull` - always sync first
- Don't manually edit git history without team agreement
- Don't commit without descriptive messages
- Don't push directly to `main` - use PRs
- Don't forget to mark tasks complete in status file

---

## Troubleshooting

### "Not a git repository"

```bash
# Initialize git
git init
git add .
git commit -m "Initial commit: Project factory system setup"
git branch -M main

# Add remote (replace with your GitHub URL)
git remote add origin https://github.com/your-org/your-repo.git
git push -u origin main
```

### Status file conflicts

```bash
# Accept remote version
git checkout --theirs PROJECT_STATUS.json
make update-status

# Or accept local version
git checkout --ours PROJECT_STATUS.json
make save-status
```

### Lost context across sessions

```bash
# Check recent history
make history

# Check full status
make status

# Sync with remote
make sync-status
```

---

## Integration with Development Servers

### Development Server Setup

Add to your dev server's cron or CI/CD:

```bash
# Every 5 minutes
*/5 * * * * cd /path/to/project && git pull origin develop && make status >> /var/log/project-status.log
```

### Staging Server Deployment

```bash
# On approved PR merge to staging branch
git pull origin staging
make status
# Run deployment scripts
```

### Production Deployment

```bash
# On approved release tag
git pull origin main
make status
# Verify status shows production-ready
# Run production deployment
```

---

## Example: Complete Development Cycle

### 1. Start Feature

```bash
git checkout develop
git pull origin develop
git checkout -b feat/linear-integration

make status
# Shows: "Next priority: Create Linear integration"
```

### 2. During Development

```bash
# AI updates PROJECT_STATUS.json as it works
# You can check anytime with:
make where-am-i
```

### 3. Complete Feature

```bash
make save-status
git push origin feat/linear-integration

# Create PR
gh pr create --title "feat: Linear integration for task sync" \
  --body "Implements Linear API integration per ADR-0001"
```

### 4. After PR Approval

```bash
# PR merged to develop
git checkout develop
git pull origin develop
make status
# Shows Linear integration as complete ✅
```

### 5. Team Member Picks Up Next

```bash
# Hassan on different machine
git pull origin develop
make status
# Sees: "Linear integration ✅, Next: Build FastAPI template"
git checkout -b feat/fastapi-template
# Continues from where team left off
```

---

## Summary

**The hybrid memory system ensures:**
- ✅ You always know where the project is
- ✅ Team members can pick up work seamlessly
- ✅ Servers stay synchronized with latest status
- ✅ Context persists across sessions and machines
- ✅ Audit trail through git history
- ✅ Fast local access through PROJECT_STATUS.json

**Key commands to remember:**
```bash
make status        # What's the current state?
make save-status   # Save my progress for the team
make history       # What has the team been doing?
```

---

*Last Updated: 2025-10-01*
