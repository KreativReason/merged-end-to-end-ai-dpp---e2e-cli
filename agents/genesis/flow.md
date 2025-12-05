# Flow Agent (File-First, Token-Safe)

**Follow:** `_common.guardrails.md`

## Purpose
Transform the PRD into comprehensive user flows and system interaction diagrams while keeping **terminal/chat output minimal**. All large artifacts are **written to disk** in shards. Final flow size is **unlimited**; only the chat output is kept small.

## Inputs (Required)
- `prd_path`: Path to validated PRD JSON file
- **Context Files**:
  - `docs/voiceflow-ai-prd.json` (or `docs/prd.json` - primary input)
  - `app/models.py` (provides `FlowModel` for validation)
  - `docs/adr.json` (if exists, for architectural decisions)

## Directories & Files (created by this agent)
```
docs/
  flows/
    user/           # one file per user flow
      FLOW-001.json
      FLOW-002.json
      ...
    system/         # one file per system flow
      SFLOW-001.json
      ...
    integrations.json
    assumptions.json
    index.json      # small manifest for navigation (chat-safe)
    final_flow.json # optional merged artifact (unlimited size)
    validation_report.json
```

## Task
Analyze the PRD (and ADRs if present) to produce:
- User flows covering **every** user story
- System/API/backend interaction flows covering critical paths
- Error-handling branches for all critical scenarios
- Integrations and assumptions

## Process (Chunked, File-First)
1. **Load Context (no printing):** Read PRD, ADRs, and `FlowModel` from `app/models.py`.
2. **Outline (chat-safe):** Generate a concise outline (flow IDs + names + linked feature/story IDs). Print ≤ 25 lines.
3. **Generate User Flows (sharded):**
   - Create one **JSON file per flow** at `./docs/flows/user/FLOW-XXX.json`.
   - IDs: `FLOW-001`, `FLOW-002`, …
   - Step IDs: `STEP-001`, `STEP-002`, …
   - After each write, print only: `WROTE ./docs/flows/user/FLOW-XXX.json`
4. **Generate System Flows (sharded):**
   - Create one **JSON file per flow** at `./docs/flows/system/SFLOW-XXX.json`.
   - After each write, print only: `WROTE ./docs/flows/system/SFLOW-XXX.json`
5. **Integrations & Assumptions:**
   - Write `./docs/flows/integrations.json` and `./docs/flows/assumptions.json`. Print only file paths.
6. **Build Manifest (chat-safe):**
   - Create `./docs/flows/index.json` with:
     - `artifact_type: "flow_index"`
     - project name, version, timestamp
     - counts of user/system flows
     - paths to `user/`, `system/`, `final_flow.json`
     - file entries: `{id, path, sha256, bytes}` for each shard
   - Print only: `WROTE ./docs/flows/index.json`
7. **Optional Merge (unlimited size):**
   - Create `./docs/flows/final_flow.json` by merging all shards into the target schema under:
     ```json
     {
       "artifact_type": "flow",
       "status": "complete",
       "validation": "unknown",
       "approval_required": true,
       "approvers": ["Cynthia","Hassan"],
       "next_phase": "erd_design",
       "data": {
         "project_name": "...",
         "version": "...",
         "created_at": "ISO-8601",
         "user_flows": [...],
         "system_flows": [...],
         "integrations": [...],
         "assumptions": [...]
       }
     }
     ```
   - Do not print its content to chat. Print only: `WROTE ./docs/flows/final_flow.json`
8. **Validation (no bloat):**
   - Validate the **merged object** against `FlowModel`.
   - Write a detailed result to `./docs/flows/validation_report.json` with `passed|failed` and any errors.
   - Print only: `VALIDATION: passed` (or `failed`) and the path to the report.

## Validation Requirements
- JSON validates against `FlowModel` in `app/models.py`
- Flow IDs: `FLOW-001`, `FLOW-002`, etc. (never regenerate)
- Step IDs: `STEP-001`, `STEP-002`, etc.
- Every user story in PRD maps to ≥ 1 user flow
- `feature_id` and `story_ids` reference valid PRD entries
- Decision points include explicit `conditions`
- Error-handling defined for all critical paths
- Steps align with acceptance criteria; system flows feasible per ADRs

## Consistency Rules
- **Completeness:** All PRD user stories covered
- **Traceability:** Back-links to PRD feature/story IDs
- **Feasibility:** System flows match ADR constraints
- **Resilience:** Error paths for critical steps
- Flow steps must align with acceptance criteria
- System flows must be technically feasible per ADRs

## Output Management (Terminal/Chat)
- **Never print large JSON payloads to chat/terminal.**
- Only print short status lines and file paths.
- If output would exceed ~25 lines, stop and wait for the next instruction.
- Example status lines:
  - `WROTE ./docs/flows/user/FLOW-003.json`
  - `WROTE ./docs/flows/system/SFLOW-002.json`
  - `WROTE ./docs/flows/index.json`
  - `VALIDATION: passed • report ./docs/flows/validation_report.json`

## Final Chat Response (Manifest Only)
At completion, respond with this **compact JSON** (≤ 1k tokens). Do not inline large content:
```json
{
  "artifact_type": "flow_manifest",
  "status": "complete",
  "validation": "<passed|failed>",
  "approval_required": true,
  "approvers": ["Cynthia","Hassan"],
  "next_phase": "erd_design",
  "index_path": "docs/flows/index.json",
  "final_path": "docs/flows/final_flow.json",
  "validation_report_path": "docs/flows/validation_report.json",
  "counts": { "user_flows": <n>, "system_flows": <m> }
}
```

## Output Schema (target for final_flow.json)
```json
{
  "artifact_type": "flow",
  "status": "complete",
  "validation": "passed",
  "approval_required": true,
  "approvers": ["Cynthia", "Hassan"],
  "next_phase": "erd_design",
  "data": {
    "project_name": "string",
    "version": "string",
    "created_at": "ISO-8601",
    "user_flows": [
      {
        "id": "FLOW-001",
        "name": "string",
        "description": "string",
        "feature_id": "FR-001",
        "story_ids": ["ST-001"],
        "actor": "user|admin|system",
        "trigger": "string",
        "steps": [
          {
            "id": "STEP-001",
            "sequence": 1,
            "action": "string",
            "actor": "user|system",
            "inputs": [],
            "outputs": [],
            "conditions": [],
            "next_steps": ["STEP-002"]
          }
        ],
        "success_criteria": ["string"],
        "error_handling": []
      }
    ],
    "system_flows": [
      {
        "id": "SFLOW-001",
        "name": "string",
        "description": "string",
        "components": ["api", "database", "cache"],
        "steps": [],
        "data_flow": [],
        "error_handling": []
      }
    ],
    "integrations": [],
    "assumptions": []
  }
}
```

## Error Handling (file-first)
On validation failure, write:
```json
{
  "error": {
    "code": "FLOW_VALIDATION_FAILED",
    "message": "Flow does not match required schema",
    "details": ["Invalid feature_id reference: FR-999"],
    "artifact": "flow",
    "remediation": "Fix feature references and regenerate flows"
  }
}
```
to `./docs/flows/validation_report.json`, and print only:
```
VALIDATION: failed • report ./docs/flows/validation_report.json
```

## Example Usage
```
Use @agents/Flow.agent.md
prd_path: @docs/voiceflow-ai-prd.json
```

## Human Approval Gate
After successful completion, this agent requires approval from:
- **Cynthia** (Product Owner)
- **Hassan** (UX/Flow Designer)

Do not proceed to ERD design until explicit human approval is received.

## Performance Tip
To keep chat output conservative, you can export:
```bash
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=8000
```
This doesn't limit the artifact size on disk—only how much the model attempts to print to the terminal.
