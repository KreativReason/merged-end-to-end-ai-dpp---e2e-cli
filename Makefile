.PHONY: help status history sync-status save-status update-status where-am-i

# Default target
help:
	@echo "End-to-End Agentic Development Pipeline - Commands"
	@echo ""
	@echo "Status Management:"
	@echo "  make status         - Show current project status (local)"
	@echo "  make where-am-i     - Quick status overview"
	@echo "  make history        - Show recent git commit history"
	@echo "  make sync-status    - Sync status from GitHub (fetch + compare)"
	@echo "  make save-status    - Commit and push status updates to GitHub"
	@echo "  make update-status  - Update status file timestamp"
	@echo ""
	@echo "Development:"
	@echo "  make scaffold-plan  - Generate scaffolding plan (Stage 1)"
	@echo "  make scaffold-apply - Execute approved plan (Stage 2)"
	@echo ""

# Show full project status
status:
	@echo "📊 Project Status"
	@echo "=================="
	@cat PROJECT_STATUS.json | jq -r '"\nPhase: \(.project.phase)\nSprint: \(.project.sprint)\nCompletion: \(.progress.overall_completion)\n"'
	@echo "Phase Status:"
	@cat PROJECT_STATUS.json | jq -r '.progress.phase_status | to_entries[] | "\(.value.icon) \(.key): \(.value.status)"'
	@echo ""
	@echo "Current Session ($(shell cat PROJECT_STATUS.json | jq -r '.current_session.date')):"
	@cat PROJECT_STATUS.json | jq -r '.current_session.completed[] | "  ✓ \(.)"'
	@echo ""
	@echo "Next Priorities:"
	@cat PROJECT_STATUS.json | jq -r '.next_priorities[0:3][] | "  → \(.)"'

# Quick status overview
where-am-i:
	@echo "🎯 Quick Status"
	@echo "==============="
	@echo "Phase: $(shell cat PROJECT_STATUS.json | jq -r '.project.phase')"
	@echo "Last updated: $(shell cat PROJECT_STATUS.json | jq -r '.meta.last_updated')"
	@echo "Current branch: $(shell git branch --show-current 2>/dev/null || echo 'not in git repo')"
	@echo ""
	@echo "Next up:"
	@cat PROJECT_STATUS.json | jq -r '.next_priorities[0]'

# Show git history (shared memory)
history:
	@echo "📜 Recent Git History (Shared Memory)"
	@echo "====================================="
	@if git rev-parse --git-dir > /dev/null 2>&1; then \
		git log --oneline --graph --decorate -20; \
	else \
		echo "Not a git repository yet. Run 'git init' to initialize."; \
	fi

# Sync status from GitHub
sync-status:
	@echo "🔄 Syncing Status from GitHub"
	@echo "============================="
	@if git rev-parse --git-dir > /dev/null 2>&1; then \
		git fetch origin 2>/dev/null || echo "No remote configured yet"; \
		echo ""; \
		echo "Remote commits (origin/main):"; \
		git log origin/main --oneline -10 2>/dev/null || echo "No remote branch yet"; \
		echo ""; \
		echo "Local status:"; \
		cat PROJECT_STATUS.json | jq -r '"\nPhase: \(.project.phase)\nLast updated: \(.meta.last_updated)\nCompletion: \(.progress.overall_completion)"'; \
	else \
		echo "Not a git repository. Run 'git init' to initialize."; \
	fi

# Update status timestamp
update-status:
	@echo "⏰ Updating status timestamp..."
	@cat PROJECT_STATUS.json | jq '.meta.last_updated = "$(shell date -u +"%Y-%m-%dT%H:%M:%SZ")" | .meta.last_commit = "$(shell git rev-parse --short HEAD 2>/dev/null || echo 'no_commit')" | .meta.current_branch = "$(shell git branch --show-current 2>/dev/null || echo 'no_branch')"' > PROJECT_STATUS.tmp.json
	@mv PROJECT_STATUS.tmp.json PROJECT_STATUS.json
	@echo "✓ Status updated"

# Commit and push status to GitHub
save-status: update-status
	@echo "💾 Saving Status to GitHub"
	@echo "=========================="
	@if git rev-parse --git-dir > /dev/null 2>&1; then \
		git add PROJECT_STATUS.json; \
		PHASE=$$(cat PROJECT_STATUS.json | jq -r '.project.phase'); \
		git commit -m "Update project status: $$PHASE [$(shell date +"%Y-%m-%d")]" || echo "No changes to commit"; \
		BRANCH=$$(git branch --show-current); \
		echo "Pushing to origin/$$BRANCH..."; \
		git push origin $$BRANCH 2>/dev/null || echo "⚠ Push failed. Check remote configuration."; \
		echo "✓ Status saved and pushed"; \
	else \
		echo "⚠ Not a git repository. Initialize with 'git init' first."; \
	fi

# Scaffolding commands (placeholder for future implementation)
scaffold-plan:
	@echo "🏗️  Stage 1: Generating Scaffolding Plan"
	@echo "========================================"
	@echo "⚠ Not yet implemented"
	@echo "This will invoke the Planning Agent to generate project structure"

scaffold-apply:
	@echo "🚀 Stage 2: Executing Scaffolding Plan"
	@echo "======================================"
	@echo "📁 Project will be generated in: ../generated-projects/{project-name}/"
	@echo ""
	@python3 scripts/scaffold_apply.py \
		--plan docs/scaffold_plan.json \
		--prd docs/prd.json \
		--erd docs/erd.json \
		--approved-by Cynthia \
		--approved-by Usama \
		--output docs/scaffold_applied.json
	@echo ""
	@echo "✅ Project generated! Next steps:"
	@echo "   cd ../generated-projects/{project-name}/"
	@echo "   git init"
	@echo "   gh repo create"
