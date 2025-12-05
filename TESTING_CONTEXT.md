# Testing Context & Handoff

This document captures the current state and provides a test plan for validating the merged E2E Pipeline.

---

## Current State

### What Was Merged

Two systems were combined:

1. **End-to-End Pipeline Human in the Loop** (the original)
   - Python validation layer (Pydantic models, linters)
   - Deterministic scaffolding execution
   - 11 genesis/development agents
   - JSON artifact storage
   - Human approval gates

2. **KreativReason E2E CLI Plugin** (the expansion)
   - 11 code review agents
   - 3 design agents
   - 5 workflow agents
   - 3 research agents
   - 6 command workflows
   - 8 skills

### Final Counts

| Component | Count |
|-----------|-------|
| Agents | 36 |
| Commands | 6 |
| Skills | 8 |
| Python files | 4 |
| Total files | 85 |

---

## Test Plan

### Test 1: Verify Python Validation Works

```bash
cd /path/to/merged-end-to-end-ai-dpp---e2e-cli

# Install dependency
pip install pydantic

# Test PRD validation (should pass - uses existing docs/prd.json)
python app/lint_prd.py docs/prd.json

# Test ERD validation (should pass - uses existing docs/erd.json)
python app/lint_erd.py docs/erd.json
```

**Expected**: Both validators run without errors on the existing sample artifacts.

---

### Test 2: Verify Agents Are Readable

```bash
# Check genesis agents exist and have content
head -20 agents/genesis/prd.md
head -20 agents/genesis/erd.md

# Check review agents exist
ls agents/review/

# Check all 11 review agents
wc -l agents/review/*.md
```

**Expected**: All agents exist with substantial content (100+ lines each).

---

### Test 3: Test a Simple Agent Invocation

In Claude Code, from the repo directory:

```
@agents/genesis/prd.md

Analyze this interview excerpt and identify 3 key features:

"We need a booking system where customers can schedule appointments
with service providers. Providers should be able to set their
availability and customers should get email confirmations."
```

**Expected**: The PRD agent responds with structured feature extraction following its defined format.

---

### Test 4: Test the /kreativreason:plan Command

```
/kreativreason:plan "Add a simple health check endpoint to an Express app"
```

**Expected**: Creates a structured implementation plan with tasks.

---

### Test 5: Test the /kreativreason:review Command (if you have a PR)

```
/kreativreason:review #1
```

Or test on local changes:

```
/kreativreason:review
```

**Expected**: Multiple review agents analyze the code and provide findings.

---

### Test 6: Full Genesis Pipeline (Most Comprehensive)

Create a test interview file:

```bash
mkdir -p interview
cat > interview/test-interview.md << 'EOF'
# Test Interview - Simple Todo App

**Q: What do you want to build?**
A: A simple todo list application where users can add, complete, and delete tasks.

**Q: Who will use it?**
A: Individual users who want to track their personal tasks.

**Q: What features are must-have?**
A:
- Add new tasks with a title
- Mark tasks as complete
- Delete tasks
- View all tasks (completed and incomplete)

**Q: Any technical preferences?**
A: Keep it simple. A single-page web app is fine.
EOF
```

Then run:

```
/kreativreason:genesis

Interview: interview/test-interview.md
Project name: "Simple Todo App"
Output: ~/Projects/test-todo-app
```

**Expected**:
1. PRD generated → validation passes → asks for approval
2. Flow generated
3. ERD generated → validation passes → asks for approval
4. Journey generated
5. Tasks generated → asks for approval
6. ADR generated
7. Scaffold plan generated → asks for approval
8. Project files created in output directory

---

## Known Issues to Watch For

1. **Command not found**: If `/kreativreason:*` commands don't work, the plugin may not be loaded. Try invoking agents directly with `@agents/...`

2. **Pydantic version**: Requires Pydantic v2. If you have v1, run `pip install --upgrade pydantic`

3. **MCP servers**: Playwright and Context7 are optional. Tests should work without them.

---

## Files to Check If Something Breaks

| Issue | Check This File |
|-------|-----------------|
| PRD validation fails | `app/lint_prd.py`, `app/models.py` |
| ERD validation fails | `app/lint_erd.py`, `app/models.py` |
| Agent not working | `agents/genesis/*.md` or relevant agent file |
| Command not found | `.claude-plugin/plugin.json` |
| Scaffolding fails | `scripts/scaffold_apply.py` |

---

## How to Report Issues

If a test fails:

1. Note which test failed
2. Copy the exact error message
3. Check if the relevant file exists and has content
4. Create an issue at: https://github.com/KreativReason/merged-end-to-end-ai-dpp---e2e-cli/issues

---

## Quick Smoke Test

The fastest way to verify the system works:

```bash
# 1. Clone fresh
git clone https://github.com/KreativReason/merged-end-to-end-ai-dpp---e2e-cli.git
cd merged-end-to-end-ai-dpp---e2e-cli

# 2. Install
pip install pydantic

# 3. Validate existing artifacts
python app/lint_prd.py docs/prd.json && echo "PRD OK"
python app/lint_erd.py docs/erd.json && echo "ERD OK"

# 4. Count agents
find agents -name "*.md" | wc -l  # Should be 36

# 5. Open Claude Code and test an agent
claude
# Then: @agents/genesis/prd.md --help
```

If all 5 steps pass, the merge is working correctly.
