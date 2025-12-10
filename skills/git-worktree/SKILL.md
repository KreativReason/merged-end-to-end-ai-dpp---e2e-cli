# Git Worktree Skill

## Purpose

Manage git worktrees for isolated feature development, enabling parallel work without affecting the main working directory.

## Overview

Git worktrees allow you to have multiple working directories attached to the same repository. This skill provides utilities for creating, managing, and cleaning up worktrees during the development workflow.

## Commands

### Create Worktree

```bash
# Create worktree for a feature
git worktree add .worktrees/feat-user-auth -b feature/user-auth

# Create from existing branch
git worktree add .worktrees/fix-bug-123 bugfix/123
```

### List Worktrees

```bash
git worktree list
# Output:
# /path/to/repo                 abc1234 [main]
# /path/to/repo/.worktrees/feat-user-auth  def5678 [feature/user-auth]
```

### Remove Worktree

```bash
# Remove worktree (keeps branch)
git worktree remove .worktrees/feat-user-auth

# Force remove (discards changes)
git worktree remove --force .worktrees/feat-user-auth

# Prune stale worktree references
git worktree prune
```

## Skill Functions

### `create_worktree(feature_name, base_branch='main')`

Creates an isolated worktree for feature development.

**Input:**
```json
{
  "feature_name": "user-auth",
  "base_branch": "main"
}
```

**Output:**
```json
{
  "status": "created",
  "worktree_path": ".worktrees/user-auth",
  "branch": "feature/user-auth",
  "base": "main"
}
```

**Process:**
1. Ensure clean working directory
2. Create worktree directory
3. Create and checkout feature branch
4. Return path for navigation

### `switch_to_worktree(worktree_name)`

Changes context to specified worktree.

**Input:**
```json
{
  "worktree_name": "user-auth"
}
```

**Output:**
```json
{
  "status": "switched",
  "previous": "/path/to/repo",
  "current": "/path/to/repo/.worktrees/user-auth",
  "branch": "feature/user-auth"
}
```

### `cleanup_worktree(worktree_name, force=false)`

Removes worktree after feature completion.

**Input:**
```json
{
  "worktree_name": "user-auth",
  "force": false
}
```

**Output:**
```json
{
  "status": "removed",
  "worktree_path": ".worktrees/user-auth",
  "branch_preserved": true,
  "uncommitted_changes": false
}
```

### `list_worktrees()`

Lists all active worktrees.

**Output:**
```json
{
  "worktrees": [
    {
      "path": "/path/to/repo",
      "branch": "main",
      "commit": "abc1234",
      "is_main": true
    },
    {
      "path": "/path/to/repo/.worktrees/user-auth",
      "branch": "feature/user-auth",
      "commit": "def5678",
      "is_main": false
    }
  ]
}
```

## Workflow Integration

### With /kreativreason:work

```
1. /kreativreason:work plans/feat-user-auth.md
   ↓
2. Skill: create_worktree("user-auth")
   ↓
3. Work happens in .worktrees/user-auth/
   ↓
4. PR created from feature branch
   ↓
5. Skill: cleanup_worktree("user-auth")
```

### Parallel Development

```
Main repo: /project
  ├── .worktrees/
  │   ├── feat-user-auth/      # Working on auth
  │   ├── feat-dark-mode/      # Working on UI
  │   └── fix-bug-123/         # Fixing bug
  └── (main branch untouched)
```

## Best Practices

1. **Always use worktrees for features** - Keep main branch clean
2. **One feature per worktree** - Avoid mixing concerns
3. **Clean up after merge** - Remove worktrees once PR merged
4. **Don't share worktrees** - Each developer creates their own

## Gitignore Setup

Add to `.gitignore`:
```
.worktrees/
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `worktree already exists` | Name collision | Use different name or remove existing |
| `branch already checked out` | Branch in another worktree | Use that worktree instead |
| `uncommitted changes` | Dirty worktree | Commit or stash before removal |
