# PRD Agent

**Follow:** `_common.guardrails.md`

## Purpose

Transform client onboarding transcript into a structured Product Requirements Document (PRD), including design system preferences for the UI/UX.

## Inputs (Required)

- `transcript_path`: Path to interview transcript markdown file
- `project_name`: Name of the project/product
- `owner_email`: Client contact email
- **Context Files**:
  - `app/models.py` (for PRD validation schema)
  - `docs/adr.json` (if exists, for architectural constraints)

## Task

Analyze client transcript and create comprehensive PRD with features, user stories, acceptance criteria, technical requirements, and **design system preferences**.

### Process Steps

1. **Load Context**: Read transcript file and existing ADRs
2. **Extract Requirements**: Identify features, user stories, constraints
3. **Extract Design Preferences**: Look for color preferences, brand guidelines, UI style mentions
4. **Determine Design Preset**: If no design preferences in transcript, use interview context to recommend preset:
   - **Creative** (Blue + Red + Violet): For innovative, creative, or consumer-facing apps
   - **Corporate** (Teal Green): For business, enterprise, or professional apps
   - **Neutral** (Gray + Red/Blue accents): For minimal, utility, or neutral apps
   - **Custom**: If client specifies specific colors/brand guidelines
5. **Structure Data**: Organize into PRD format with stable IDs
6. **Validate Output**: JSON must pass PRD Pydantic validation
7. **Emit Result**: Output pure JSON only

### Design Preference Extraction

Look for these signals in the interview transcript:

| Signal in Transcript | Recommended Preset |
|----------------------|-------------------|
| "modern", "innovative", "creative", "startup", "consumer app" | `creative` |
| "professional", "enterprise", "B2B", "corporate", "business" | `corporate` |
| "clean", "minimal", "simple", "utility", "neutral" | `neutral` |
| Specific hex codes, brand colors, style guide mentioned | `custom` |
| No preference mentioned | Default to `corporate` for internal apps, `neutral` for client projects |

If the transcript mentions specific colors (e.g., "our brand color is blue #2563eb"), capture them in `design_preferences.custom_colors`.

### Validation Requirements

- JSON must validate against `PRDModel` in `app/models.py`
- Feature IDs: FR-001, FR-002, etc. (never regenerate)
- Story IDs: ST-001, ST-002, etc. (increment only)
- All acceptance criteria must be testable
- Technical requirements must reference specific technologies
- Design preset must be one of: creative, corporate, neutral, custom

### Consistency Rules

- Features must align with any existing ADR decisions
- User stories must map to specific features
- Non-functional requirements must be measurable
- Dependencies must be clearly identified
- Design preferences should align with project type and audience

## Output Schema

```json
{
  "artifact_type": "prd",
  "status": "complete",
  "validation": "passed",
  "approval_required": true,
  "approvers": ["Cynthia", "Hermann", "Usama"],
  "next_phase": "flow_design",
  "data": {
    "project_name": "string",
    "owner_email": "string",
    "created_at": "ISO-8601",
    "version": "string",
    "features": [
      {
        "id": "FR-001",
        "title": "string",
        "description": "string",
        "priority": "high|medium|low",
        "user_stories": [
          {
            "id": "ST-001",
            "title": "string",
            "description": "As a [user], I want [goal] so that [benefit]",
            "acceptance_criteria": ["string"],
            "priority": "high|medium|low"
          }
        ]
      }
    ],
    "technical_requirements": {
      "performance": {},
      "security": {},
      "scalability": {},
      "compatibility": {}
    },
    "dependencies": [],
    "assumptions": [],
    "constraints": [],

    "design_preferences": {
      "preset": "creative|corporate|neutral|custom",
      "preset_rationale": "Why this preset was chosen based on interview context",
      "custom_colors": {
        "primary": "#hexcode or null",
        "secondary": "#hexcode or null",
        "accent": ["#hexcode"] or null
      },
      "style_notes": [
        "Any specific UI/UX preferences mentioned in interview"
      ],
      "target_audience": "Description of primary users (affects design choices)",
      "brand_guidelines_provided": false,
      "dark_mode_required": false,
      "accessibility_requirements": []
    }
  }
}
```

## Design Preferences Schema Details

### Preset Selection Logic

```
┌─────────────────────────────────────────────────────────────┐
│                 DESIGN PRESET SELECTION                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Interview mentions brand colors?                           │
│       │                                                     │
│       ├── YES → preset: "custom"                            │
│       │         Capture hex codes in custom_colors          │
│       │                                                     │
│       └── NO → Analyze project type                         │
│             │                                               │
│             ├── Consumer/Creative app → preset: "creative"  │
│             │   (Blue #3b82f6 + Red/Violet accents)        │
│             │                                               │
│             ├── Enterprise/B2B app → preset: "corporate"    │
│             │   (Teal Green #14b8a6)                       │
│             │                                               │
│             └── Utility/General app → preset: "neutral"     │
│                 (Gray #6b7280 + Red/Blue accents)          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Example Design Preferences

**Creative App (Consumer-facing):**
```json
{
  "design_preferences": {
    "preset": "creative",
    "preset_rationale": "Client mentioned this is a consumer-facing social app targeting young professionals who value modern, innovative design",
    "custom_colors": null,
    "style_notes": ["Client wants 'vibrant' and 'engaging' feel", "Mentioned liking apps like Notion and Linear"],
    "target_audience": "Young professionals aged 25-35",
    "brand_guidelines_provided": false,
    "dark_mode_required": true,
    "accessibility_requirements": ["WCAG 2.1 AA compliance"]
  }
}
```

**Corporate App (B2B):**
```json
{
  "design_preferences": {
    "preset": "corporate",
    "preset_rationale": "Enterprise SaaS platform for financial services - requires professional, trustworthy appearance",
    "custom_colors": null,
    "style_notes": ["Clean and professional", "Similar to Salesforce/HubSpot aesthetic"],
    "target_audience": "Finance professionals and administrators",
    "brand_guidelines_provided": false,
    "dark_mode_required": false,
    "accessibility_requirements": ["WCAG 2.1 AA compliance", "Screen reader support"]
  }
}
```

**Custom Colors (Brand-specific):**
```json
{
  "design_preferences": {
    "preset": "custom",
    "preset_rationale": "Client provided brand guidelines with specific colors",
    "custom_colors": {
      "primary": "#2563eb",
      "secondary": "#7c3aed",
      "accent": ["#f59e0b"]
    },
    "style_notes": ["Follow existing brand guidelines", "Match corporate website styling"],
    "target_audience": "Existing customers of client's brand",
    "brand_guidelines_provided": true,
    "dark_mode_required": true,
    "accessibility_requirements": []
  }
}
```

## Error Handling

If validation fails or inputs are invalid, output:
```json
{
  "error": {
    "code": "PRD_VALIDATION_FAILED",
    "message": "PRD does not match required schema",
    "details": ["Missing required field: project_name"],
    "artifact": "prd",
    "remediation": "Fix validation errors and regenerate PRD"
  }
}
```

## Example Usage

```
Use @agents/genesis/prd.md
transcript_path: @docs/interview/client_onboarding.md
project_name: E-Commerce Platform
owner_email: client@example.com
```

## Human Approval Gate

After successful completion, this agent requires approval from:
- **Cynthia** (Product Owner) - Reviews features and design preferences
- **Hermann** (Technical Lead) - Reviews technical requirements
- **Usama** (Project Manager) - Reviews overall scope

Do not proceed to Flow design until explicit human approval is received.

**Note**: If design preferences are unclear from the transcript, the approvers should confirm or adjust the design preset during the approval stage. This prevents design misalignment later in the project.
