"""
Pydantic models for all artifacts in the agentic development pipeline.

These models enforce JSON validation for:
- PRD (Product Requirements Document)
- Flow (User and System Flows)
- ERD (Entity Relationship Diagram)
- Journey (User Journey Maps)
- Tasks (Implementation Task Breakdown)
- ADR (Architecture Decision Records)
- Scaffold (Scaffolding Plans and Results)
- Implementation (Coding Results)

All models follow the stable ID conventions:
- Features: FR-###
- Stories: ST-###
- Tasks: TASK-###
- ADRs: ADR-####
- Entities: ENT-###
- Flows: FLOW-###
- etc.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, EmailStr, field_validator


# ============================================================================
# Enums for controlled vocabularies
# ============================================================================

class PriorityLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskType(str, Enum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    DATABASE = "database"
    DEVOPS = "devops"
    TESTING = "testing"
    DOCUMENTATION = "documentation"


class ADRStatus(str, Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"


class ValidationStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"


class EmotionalState(str, Enum):
    CURIOUS = "curious"
    FRUSTRATED = "frustrated"
    CONFIDENT = "confident"
    CONFUSED = "confused"
    SATISFIED = "satisfied"


class TouchpointType(str, Enum):
    WEB = "web"
    MOBILE = "mobile"
    EMAIL = "email"
    SUPPORT = "support"


class DesignPreset(str, Enum):
    """Design color presets for generated projects."""
    CREATIVE = "creative"      # Blue + Red + Violet accents
    CORPORATE = "corporate"    # Teal Green
    NEUTRAL = "neutral"        # White + Red + Blue, gray tones
    CUSTOM = "custom"          # Client-specified colors


class ArchitectureStyle(str, Enum):
    """Architecture patterns for generated projects."""
    MODULAR_MONOLITH = "modular_monolith"  # Default: Domain-driven with modules
    MICROSERVICES = "microservices"         # Service-oriented
    LAYERED = "layered"                     # Traditional layers


# ============================================================================
# Domain Mapping Models (for Propose-Validate-Confirm pattern)
# ============================================================================

class DomainSchema(BaseModel):
    """
    Represents a bounded context/domain in the modular monolith.
    Used for grouping related entities into cohesive modules.

    The Propose-Validate-Confirm pattern:
    1. AI proposes domain groupings based on PRD context
    2. Aggregate root convention validates each domain has one entry point
    3. Human confirms the domain map before scaffolding
    """
    name: str = Field(..., min_length=2, max_length=50, description="Domain name in kebab-case, e.g., 'sales', 'user-management'")
    description: str = Field(..., min_length=10, description="Business purpose of this domain")
    root_entity: str = Field(..., pattern=r"^ENT-\d{3}$", description="Aggregate root entity ID - the domain's entry point")
    entities: List[str] = Field(..., min_items=1, description="List of entity IDs belonging to this domain")
    feature_ids: List[str] = Field(default_factory=list, description="PRD features this domain implements")
    dependencies: List[str] = Field(default_factory=list, description="Other domain names this domain depends on")

    @field_validator('name', mode='after')
    def validate_kebab_case(cls, v):
        """Ensure domain name is kebab-case."""
        import re
        if not re.match(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$', v):
            raise ValueError(f"Domain name must be kebab-case: {v}")
        return v


class DomainMapping(BaseModel):
    """
    Complete domain map for a project.
    Generated during PRD→ERD phase, validated before scaffolding.
    """
    domains: List[DomainSchema] = Field(..., min_items=1, description="All domains in the project")
    shared_entities: List[str] = Field(default_factory=list, description="Entity IDs shared across domains")
    dependency_graph: Dict[str, List[str]] = Field(default_factory=dict, description="Domain dependency relationships")

    @field_validator('domains', mode='after')
    def validate_unique_domain_names(cls, v):
        """Ensure domain names are unique."""
        names = [d.name for d in v]
        if len(names) != len(set(names)):
            raise ValueError("Domain names must be unique")
        return v

    @field_validator('domains', mode='after')
    def validate_no_circular_dependencies(cls, v):
        """Detect circular dependencies between domains."""
        # Build dependency graph
        deps = {d.name: d.dependencies for d in v}

        def has_cycle(node, visited, rec_stack):
            visited.add(node)
            rec_stack.add(node)
            for neighbor in deps.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        visited = set()
        for domain in v:
            if domain.name not in visited:
                if has_cycle(domain.name, visited, set()):
                    raise ValueError(f"Circular dependency detected involving domain: {domain.name}")
        return v


# ============================================================================
# Design Brief Models (for UI/UX configuration)
# ============================================================================

class ColorScheme(BaseModel):
    """Color configuration for the design system."""
    primary: str = Field(..., pattern=r"^#[0-9a-fA-F]{6}$", description="Primary brand color in hex")
    secondary: Optional[str] = Field(None, pattern=r"^#[0-9a-fA-F]{6}$", description="Secondary color")
    accent: List[str] = Field(default_factory=list, description="Accent colors in hex")
    background: str = Field(default="#ffffff", pattern=r"^#[0-9a-fA-F]{6}$")
    surface: str = Field(default="#f8f9fa", pattern=r"^#[0-9a-fA-F]{6}$")
    text_primary: str = Field(default="#1a1a1a", pattern=r"^#[0-9a-fA-F]{6}$")
    text_secondary: str = Field(default="#6b7280", pattern=r"^#[0-9a-fA-F]{6}$")
    success: str = Field(default="#10b981", pattern=r"^#[0-9a-fA-F]{6}$")
    warning: str = Field(default="#f59e0b", pattern=r"^#[0-9a-fA-F]{6}$")
    error: str = Field(default="#ef4444", pattern=r"^#[0-9a-fA-F]{6}$")


class GlassmorphismConfig(BaseModel):
    """Glassmorphism UI configuration."""
    enabled: bool = Field(default=True, description="Whether to use glassmorphism effects")
    blur_intensity: str = Field(default="xl", pattern=r"^(sm|md|lg|xl|2xl|3xl)$")
    opacity: float = Field(default=0.7, ge=0.1, le=1.0, description="Background opacity for glass effect")
    border_opacity: float = Field(default=0.3, ge=0.1, le=1.0)
    shadow_color_opacity: float = Field(default=0.1, ge=0.0, le=0.5)
    floating_orbs: bool = Field(default=True, description="Include FloatingOrbs background component")


class TypographyConfig(BaseModel):
    """Typography configuration."""
    font_family_heading: str = Field(default="Inter", description="Font for headings")
    font_family_body: str = Field(default="Inter", description="Font for body text")
    font_family_mono: str = Field(default="JetBrains Mono", description="Font for code")
    base_size: str = Field(default="16px")
    scale_ratio: float = Field(default=1.25, ge=1.0, le=2.0, description="Type scale ratio")


class DesignBrief(BaseModel):
    """
    Complete design system configuration for a generated project.
    Captured during PRD generation if not specified in interview.

    Preset color schemes:
    - CREATIVE: Blue (#3b82f6) + Red (#ef4444) + Violet (#8b5cf6) - for creative apps
    - CORPORATE: Teal Green (#14b8a6) - for business/enterprise apps
    - NEUTRAL: White/Gray + Red/Blue patches - for minimal/neutral apps
    - CUSTOM: Client-specified colors
    """
    preset: DesignPreset = Field(default=DesignPreset.NEUTRAL, description="Color preset to use")
    colors: ColorScheme = Field(default_factory=ColorScheme)
    glassmorphism: GlassmorphismConfig = Field(default_factory=GlassmorphismConfig)
    typography: TypographyConfig = Field(default_factory=TypographyConfig)
    dark_mode_support: bool = Field(default=True)
    responsive_breakpoints: Dict[str, str] = Field(
        default_factory=lambda: {
            "sm": "640px",
            "md": "768px",
            "lg": "1024px",
            "xl": "1280px",
            "2xl": "1536px"
        }
    )
    component_style: str = Field(
        default="rounded",
        pattern=r"^(rounded|sharp|pill)$",
        description="Border radius style for components"
    )

    @classmethod
    def from_preset(cls, preset: DesignPreset) -> "DesignBrief":
        """Factory method to create DesignBrief from preset."""
        presets = {
            DesignPreset.CREATIVE: ColorScheme(
                primary="#3b82f6",      # Blue
                secondary="#8b5cf6",    # Violet
                accent=["#ef4444", "#8b5cf6"],  # Red + Violet
                background="#ffffff",
                surface="#f0f9ff",
                text_primary="#1e3a5f",
                text_secondary="#64748b"
            ),
            DesignPreset.CORPORATE: ColorScheme(
                primary="#14b8a6",      # Teal Green
                secondary="#0d9488",
                accent=["#0891b2"],
                background="#ffffff",
                surface="#f0fdfa",
                text_primary="#134e4a",
                text_secondary="#64748b"
            ),
            DesignPreset.NEUTRAL: ColorScheme(
                primary="#6b7280",       # Gray
                secondary="#3b82f6",     # Blue
                accent=["#ef4444", "#3b82f6"],  # Red + Blue patches
                background="#ffffff",
                surface="#f9fafb",
                text_primary="#1f2937",
                text_secondary="#6b7280"
            )
        }

        if preset == DesignPreset.CUSTOM:
            return cls(preset=preset)

        return cls(preset=preset, colors=presets.get(preset, presets[DesignPreset.NEUTRAL]))


class DesignBriefModel(BaseModel):
    """Artifact wrapper for design brief."""
    artifact_type: str = Field(default="design_brief")
    status: str = Field(default="complete")
    validation: ValidationStatus
    approval_required: bool = Field(default=True)
    approvers: List[str] = Field(default=["Cynthia", "Hermann"])
    next_phase: str = Field(default="scaffolding")
    data: DesignBrief


# ============================================================================
# PRD Models
# ============================================================================

class AcceptanceCriteria(BaseModel):
    criteria: str = Field(..., description="Testable acceptance criteria")
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM)


class UserStory(BaseModel):
    id: str = Field(..., pattern=r"^ST-\d{3}$", description="Story ID format: ST-001")
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., description="As a [user], I want [goal] so that [benefit]")
    acceptance_criteria: List[str] = Field(..., min_items=1)
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM)


class Feature(BaseModel):
    id: str = Field(..., pattern=r"^FR-\d{3}$", description="Feature ID format: FR-001")
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=20)
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM)
    user_stories: List[UserStory] = Field(..., min_items=1)


class TechnicalRequirement(BaseModel):
    performance: Dict[str, Any] = Field(default_factory=dict)
    security: Dict[str, Any] = Field(default_factory=dict)
    scalability: Dict[str, Any] = Field(default_factory=dict)
    compatibility: Dict[str, Any] = Field(default_factory=dict)


class PRDData(BaseModel):
    project_name: str = Field(..., min_length=3, max_length=100)
    owner_email: EmailStr
    created_at: datetime
    version: str = Field(default="1.0.0")
    features: List[Feature] = Field(..., min_items=1)
    technical_requirements: TechnicalRequirement = Field(default_factory=TechnicalRequirement)
    dependencies: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)

    @field_validator('features', mode='after')
    def validate_unique_feature_ids(cls, v):
        ids = [f.id for f in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Feature IDs must be unique")
        return v


class PRDModel(BaseModel):
    artifact_type: str = Field(default="prd")
    status: str = Field(default="complete")
    validation: ValidationStatus
    approval_required: bool = Field(default=True)
    approvers: List[str] = Field(default=["Cynthia", "Hermann", "Usama"])
    next_phase: str = Field(default="flow_design")
    data: PRDData


# ============================================================================
# Flow Models
# ============================================================================

class FlowStep(BaseModel):
    id: str = Field(..., pattern=r"^STEP-\d{3}$", description="Step ID format: STEP-001")
    sequence: int = Field(..., ge=1)
    action: str = Field(..., min_length=5)
    actor: str = Field(..., description="user|system|admin")
    inputs: List[str] = Field(default_factory=list)
    outputs: List[str] = Field(default_factory=list)
    conditions: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)


class UserFlow(BaseModel):
    id: str = Field(..., pattern=r"^FLOW-\d{3}$", description="Flow ID format: FLOW-001")
    name: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    feature_id: str = Field(..., pattern=r"^FR-\d{3}$")
    story_ids: List[str] = Field(..., min_items=1)
    actor: str = Field(..., description="user|admin|system")
    trigger: str = Field(..., min_length=5)
    steps: List[FlowStep] = Field(..., min_items=1)
    success_criteria: List[str] = Field(..., min_items=1)
    error_handling: List[str] = Field(default_factory=list)


class SystemFlow(BaseModel):
    id: str = Field(..., pattern=r"^SFLOW-\d{3}$", description="System Flow ID format: SFLOW-001")
    name: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    components: List[str] = Field(..., min_items=1)
    steps: List[FlowStep] = Field(..., min_items=1)
    data_flow: List[str] = Field(default_factory=list)
    error_handling: List[str] = Field(default_factory=list)


class FlowData(BaseModel):
    project_name: str = Field(..., min_length=3, max_length=100)
    version: str = Field(default="1.0.0")
    created_at: datetime
    user_flows: List[UserFlow] = Field(..., min_items=1)
    system_flows: List[SystemFlow] = Field(default_factory=list)
    integrations: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)


class FlowModel(BaseModel):
    artifact_type: str = Field(default="flow")
    status: str = Field(default="complete")
    validation: ValidationStatus
    approval_required: bool = Field(default=True)
    approvers: List[str] = Field(default=["Cynthia", "Hassan"])
    next_phase: str = Field(default="erd_design")
    data: FlowData


# ============================================================================
# ERD Models
# ============================================================================

class EntityAttribute(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    type: str = Field(..., description="UUID|INTEGER|STRING|BOOLEAN|DATETIME|etc")
    primary_key: bool = Field(default=False)
    nullable: bool = Field(default=True)
    unique: bool = Field(default=False)
    default: Optional[Union[str, int, bool]] = None
    constraints: List[str] = Field(default_factory=list)


class EntityIndex(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    columns: List[str] = Field(..., min_items=1)
    unique: bool = Field(default=False)


class Entity(BaseModel):
    id: str = Field(..., pattern=r"^ENT-\d{3}$", description="Entity ID format: ENT-001")
    name: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=10)
    table_name: str = Field(..., min_length=1, max_length=50)
    attributes: List[EntityAttribute] = Field(..., min_items=1)
    indexes: List[EntityIndex] = Field(default_factory=list)


class Relationship(BaseModel):
    id: str = Field(..., pattern=r"^REL-\d{3}$", description="Relationship ID format: REL-001")
    name: str = Field(..., min_length=1, max_length=100)
    from_entity: str = Field(..., pattern=r"^ENT-\d{3}$")
    to_entity: str = Field(..., pattern=r"^ENT-\d{3}$")
    from_cardinality: str = Field(..., description="1|many")
    to_cardinality: str = Field(..., description="1|many")
    relationship_type: str = Field(..., description="one-to-one|one-to-many|many-to-many")
    foreign_key: str = Field(..., min_length=1)
    cascade_delete: bool = Field(default=False)


class ERDConstraint(BaseModel):
    type: str = Field(..., description="check|unique|foreign_key")
    entity: str = Field(..., pattern=r"^ENT-\d{3}$")
    name: str = Field(..., min_length=1)
    expression: str = Field(..., min_length=1)


class ERDMigrations(BaseModel):
    initial_schema: str = Field(..., min_length=10)
    seed_data: List[Dict[str, Any]] = Field(default_factory=list)


class ERDData(BaseModel):
    project_name: str = Field(..., min_length=3, max_length=100)
    version: str = Field(default="1.0.0")
    created_at: datetime
    database_type: str = Field(..., description="postgres|mysql|mongodb|etc")
    entities: List[Entity] = Field(..., min_items=1)
    relationships: List[Relationship] = Field(default_factory=list)
    constraints: List[ERDConstraint] = Field(default_factory=list)
    migrations: ERDMigrations


class ERDModel(BaseModel):
    artifact_type: str = Field(default="erd")
    status: str = Field(default="complete")
    validation: ValidationStatus
    approval_required: bool = Field(default=True)
    approvers: List[str] = Field(default=["Cynthia", "Hassan", "Usama"])
    next_phase: str = Field(default="journey_mapping")
    data: ERDData


# ============================================================================
# Journey Models
# ============================================================================

class Persona(BaseModel):
    id: str = Field(..., pattern=r"^PERSONA-\d{3}$", description="Persona ID format: PERSONA-001")
    name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=10)
    goals: List[str] = Field(..., min_items=1)
    pain_points: List[str] = Field(default_factory=list)
    context: str = Field(..., min_length=10)


class Touchpoint(BaseModel):
    id: str = Field(..., pattern=r"^TP-\d{3}$", description="Touchpoint ID format: TP-001")
    name: str = Field(..., min_length=3, max_length=100)
    type: TouchpointType
    description: str = Field(..., min_length=10)
    flow_step_id: Optional[str] = Field(None, pattern=r"^STEP-\d{3}$")
    data_entities: List[str] = Field(default_factory=list)
    user_actions: List[str] = Field(default_factory=list)
    system_actions: List[str] = Field(default_factory=list)
    emotional_state: EmotionalState
    pain_points: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)


class JourneyPhase(BaseModel):
    id: str = Field(..., pattern=r"^PHASE-\d{3}$", description="Phase ID format: PHASE-001")
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10)
    duration_estimate: str = Field(..., description="e.g., '5 minutes', '1 hour'")
    touchpoints: List[Touchpoint] = Field(..., min_items=1)


class SuccessMetric(BaseModel):
    metric: str = Field(..., min_length=3)
    target: str = Field(..., min_length=1)
    measurement: str = Field(..., min_length=5)


class Journey(BaseModel):
    id: str = Field(..., pattern=r"^JRN-\d{3}$", description="Journey ID format: JRN-001")
    name: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    persona_id: str = Field(..., pattern=r"^PERSONA-\d{3}$")
    flow_ids: List[str] = Field(..., min_items=1)
    story_ids: List[str] = Field(..., min_items=1)
    phases: List[JourneyPhase] = Field(..., min_items=1)
    success_metrics: List[SuccessMetric] = Field(..., min_items=1)


class OptimizationOpportunity(BaseModel):
    id: str = Field(..., pattern=r"^OPP-\d{3}$", description="Opportunity ID format: OPP-001")
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    impact: PriorityLevel
    effort: PriorityLevel
    touchpoint_ids: List[str] = Field(..., min_items=1)
    expected_improvement: str = Field(..., min_length=10)


class JourneyData(BaseModel):
    project_name: str = Field(..., min_length=3, max_length=100)
    version: str = Field(default="1.0.0")
    created_at: datetime
    personas: List[Persona] = Field(..., min_items=1)
    journeys: List[Journey] = Field(..., min_items=1)
    optimization_opportunities: List[OptimizationOpportunity] = Field(default_factory=list)


class JourneyModel(BaseModel):
    artifact_type: str = Field(default="journey")
    status: str = Field(default="complete")
    validation: ValidationStatus
    approval_required: bool = Field(default=True)
    approvers: List[str] = Field(default=["Cynthia", "Hassan"])
    next_phase: str = Field(default="task_planning")
    data: JourneyData


# ============================================================================
# Tasks Models
# ============================================================================

class Epic(BaseModel):
    id: str = Field(..., pattern=r"^EPIC-\d{3}$", description="Epic ID format: EPIC-001")
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    feature_ids: List[str] = Field(..., min_items=1)
    priority: PriorityLevel
    estimated_sprints: int = Field(..., ge=1)
    success_criteria: List[str] = Field(..., min_items=1)


class ContextPlan(BaseModel):
    """Context planning for task execution."""
    beginning_context: List[str] = Field(..., min_items=1, description="Files to load at task start")
    end_state_files: List[str] = Field(..., min_items=1, description="Files that must exist after completion")
    read_only_files: List[str] = Field(default_factory=list, description="Files to read but not modify")

class TestingStrategy(BaseModel):
    """Testing approach for task validation."""
    strategy_type: str = Field(..., pattern=r"^(integration|unit|e2e|manual)$")
    test_files: List[str] = Field(default_factory=list)  # Can be empty for manual testing
    success_criteria: List[str] = Field(..., min_items=1)
    test_command: Optional[str] = None

    @field_validator('test_files', mode='after')
    def validate_test_files_for_automated_testing(cls, v, info):
        """For automated testing (unit, integration, e2e), test_files is required."""
        data = info.data
        strategy_type = data.get('strategy_type', '')
        if strategy_type in ('unit', 'integration', 'e2e') and len(v) == 0:
            raise ValueError(f"test_files required for {strategy_type} testing strategy")
        return v

class Task(BaseModel):
    id: str = Field(..., pattern=r"^TASK-\d{3}$", description="Task ID format: TASK-001")
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    type: TaskType
    epic_id: Optional[str] = Field(None, pattern=r"^EPIC-\d{3}$")
    feature_id: Optional[str] = Field(None, pattern=r"^FR-\d{3}$")
    story_ids: List[str] = Field(default_factory=list)
    entity_ids: List[str] = Field(default_factory=list)
    flow_ids: List[str] = Field(default_factory=list)
    journey_ids: List[str] = Field(default_factory=list)
    priority: PriorityLevel
    story_points: int = Field(..., ge=1, le=8, description="Story points 1-8")
    estimated_hours: int = Field(..., ge=1)
    assignee: str = Field(..., min_length=3)
    dependencies: List[str] = Field(default_factory=list, description="List of TASK-### IDs")
    blocked_by: List[str] = Field(default_factory=list)
    acceptance_criteria: List[str] = Field(..., min_items=1)
    definition_of_done: List[str] = Field(..., min_items=1)
    technical_notes: Optional[str] = None
    risks: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    
    # Enhanced context planning
    context_plan: ContextPlan
    testing_strategy: TestingStrategy
    estimated_time: str = Field(..., description="Human readable time estimate, e.g., '2 hours', '1 day'")
    scope_boundaries: List[str] = Field(default_factory=list, description="What is explicitly out of scope")


class Sprint(BaseModel):
    id: str = Field(..., pattern=r"^SPRINT-\d{3}$", description="Sprint ID format: SPRINT-001")
    name: str = Field(..., min_length=3, max_length=50)
    start_date: datetime
    end_date: datetime
    capacity: int = Field(..., ge=1, description="Total story points capacity")
    task_ids: List[str] = Field(..., min_items=1)
    goals: List[str] = Field(..., min_items=1)


class TaskDependency(BaseModel):
    from_task: str = Field(..., pattern=r"^TASK-\d{3}$")
    to_task: str = Field(..., pattern=r"^TASK-\d{3}$")
    type: str = Field(..., description="finish_to_start|start_to_start")
    description: str = Field(..., min_length=10)


class TasksData(BaseModel):
    project_name: str = Field(..., min_length=3, max_length=100)
    version: str = Field(default="1.0.0")
    created_at: datetime
    methodology: str = Field(default="agile", description="agile|scrum|kanban")
    sprint_duration: str = Field(default="2 weeks")
    team_capacity: int = Field(..., ge=1)
    epics: List[Epic] = Field(..., min_items=1)
    tasks: List[Task] = Field(..., min_items=1)
    sprints: List[Sprint] = Field(..., min_items=1)
    dependencies: List[TaskDependency] = Field(default_factory=list)


class TasksModel(BaseModel):
    artifact_type: str = Field(default="tasks")
    status: str = Field(default="complete")
    validation: ValidationStatus
    approval_required: bool = Field(default=True)
    approvers: List[str] = Field(default=["Cynthia", "Hermann", "Usama"])
    next_phase: str = Field(default="adr_documentation")
    data: TasksData


# ============================================================================
# ADR Models
# ============================================================================

class Alternative(BaseModel):
    option: str = Field(..., min_length=3, max_length=100)
    pros: List[str] = Field(..., min_items=1)
    cons: List[str] = Field(..., min_items=1)
    cost_estimate: Optional[str] = None


class DecisionContext(BaseModel):
    description: str = Field(..., min_length=10)
    requirements: List[str] = Field(..., min_items=1)
    constraints: List[str] = Field(default_factory=list)


class DecisionConsequences(BaseModel):
    positive: List[str] = Field(..., min_items=1)
    negative: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)


class ArtifactReferences(BaseModel):
    features: List[str] = Field(default_factory=list)
    entities: List[str] = Field(default_factory=list)
    tasks: List[str] = Field(default_factory=list)


class Decision(BaseModel):
    id: str = Field(..., pattern=r"^ADR-\d{4}$", description="ADR ID format: ADR-0001")
    title: str = Field(..., min_length=5, max_length=100)
    status: ADRStatus
    date: datetime
    author: str = Field(..., min_length=3)
    context: DecisionContext
    decision: str = Field(..., min_length=10)
    alternatives: List[Alternative] = Field(..., min_items=2)
    rationale: str = Field(..., min_length=20)
    consequences: DecisionConsequences
    related_decisions: List[str] = Field(default_factory=list)
    superseded_by: Optional[str] = Field(None, pattern=r"^ADR-\d{4}$")
    artifact_references: ArtifactReferences = Field(default_factory=ArtifactReferences)


class DecisionMetadata(BaseModel):
    """Metadata for decisions when using markdown format."""
    id: str = Field(..., pattern=r"^ADR-\d{4}$")
    title: str = Field(..., min_length=5)
    status: str
    anchor_id: str
    index_updated: bool


class IndexEntry(BaseModel):
    """Index entry for markdown ADR format."""
    id: str = Field(..., pattern=r"^ADR-\d{4}$")
    title: str
    date: str
    status: str
    supersedes: str
    superseded_by: str


class ADRData(BaseModel):
    project_name: str = Field(..., min_length=3, max_length=100)
    version: str = Field(default="1.0.0")
    created_at: Optional[datetime] = None

    # Structured JSON format (project ADRs)
    decisions: Optional[List[Decision]] = Field(None, min_items=1)

    # Markdown format (mothership ADRs)
    adr_file_content: Optional[str] = Field(None, min_length=10)
    protocol_version: Optional[str] = None
    decisions_added: Optional[List[DecisionMetadata]] = None
    index_entries: Optional[List[IndexEntry]] = None

    @field_validator('decisions', 'adr_file_content', mode='after')
    def validate_at_least_one_format(cls, v, info):
        """Ensure at least one of decisions or adr_file_content is provided."""
        if info.field_name == 'adr_file_content':
            # Check if we're validating the last field
            data = info.data
            if not data.get('decisions') and not v:
                raise ValueError("Either 'decisions' or 'adr_file_content' must be provided")
        return v


class ADRModel(BaseModel):
    artifact_type: str = Field(default="adr")
    scope: Optional[str] = Field(None, pattern=r"^(mothership|project)$", description="Scope: mothership (read-only) or project (mutable)")
    status: str = Field(default="complete")
    validation: ValidationStatus
    approval_required: bool = Field(default=True)
    approvers: List[str] = Field(default=["Hermann", "Usama"])
    next_phase: str = Field(default="scaffolding")
    data: ADRData


# ============================================================================
# Scaffold Models
# ============================================================================

class TemplateVariables(BaseModel):
    project_name: str = Field(..., min_length=3)
    auth_provider: Optional[str] = None
    database_type: Optional[str] = None
    additional_vars: Dict[str, Any] = Field(default_factory=dict)


class TemplateApplication(BaseModel):
    id: str = Field(..., pattern=r"^SCAFFOLD-\d{3}$", description="Scaffold ID format: SCAFFOLD-001")
    name: str = Field(..., min_length=5, max_length=100)
    source_path: str = Field(..., min_length=5)
    target_path: str = Field(..., min_length=1)
    variables: TemplateVariables
    files_to_generate: List[str] = Field(..., min_items=1)


class EnvironmentVariable(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=10)
    example: str = Field(..., min_length=1)


class FeatureSelections(BaseModel):
    """
    Feature selections for scaffolding. Now supports extensible options
    for different project types (frontend, backend, full-stack).
    """
    auth: str = Field(..., pattern=r"^(firebase|auth0|nextauth|jwt|api_key|clerk|custom|none)$")
    db: str = Field(..., pattern=r"^(postgres|mysql|mongodb|supabase|firebase|redis|none)$")
    storage: str = Field(..., pattern=r"^(s3|gcs|firebase|minio|local|none)$")
    realtime: bool = Field(default=False)
    ci: bool = Field(default=True)
    docs: bool = Field(default=True)
    # Additional optional fields for extensibility
    framework: Optional[str] = Field(None, description="Framework: nestjs|express|fastapi|nextjs|rails|etc")
    language: Optional[str] = Field(None, description="Primary language: typescript|python|ruby|etc")
    additional: Dict[str, Any] = Field(default_factory=dict, description="Additional feature flags")


class ScaffoldPlanData(BaseModel):
    project_name: str = Field(..., min_length=3, max_length=100)
    version: str = Field(default="1.0.0")
    created_at: datetime
    mode: str = Field(default="plan")

    # Architecture configuration
    architecture_style: ArchitectureStyle = Field(
        default=ArchitectureStyle.MODULAR_MONOLITH,
        description="Architecture pattern for the project"
    )
    domain_mapping: DomainMapping = Field(
        ...,
        description="Domain structure - entities grouped into bounded contexts"
    )

    # Design system configuration
    design_brief: DesignBrief = Field(
        default_factory=DesignBrief,
        description="UI/UX design system configuration"
    )

    # Feature selections (tech stack)
    feature_selections: FeatureSelections
    templates_to_apply: List[TemplateApplication] = Field(..., min_items=1)
    directory_structure: Dict[str, str] = Field(..., min_items=1)
    dependencies: Dict[str, List[str]] = Field(..., min_items=1)
    environment_variables: List[EnvironmentVariable] = Field(default_factory=list)

    # Child project injection configuration
    inject_architecture_rules: bool = Field(
        default=True,
        description="Inject .claude/rules/ files into generated project"
    )
    inject_husky: bool = Field(
        default=True,
        description="Inject Husky + lint-staged for commit hooks"
    )
    inject_eslint_config: bool = Field(
        default=True,
        description="Inject ESLint config with barrel import rules"
    )
    inject_design_system: bool = Field(
        default=True,
        description="Inject glassmorphism UI components"
    )

    next_steps: List[str] = Field(..., min_items=1)
    estimated_setup_time: str = Field(..., min_length=3)


class ScaffoldPlanModel(BaseModel):
    artifact_type: str = Field(default="scaffold_plan")
    status: str = Field(default="complete")
    validation: ValidationStatus
    approval_required: bool = Field(default=True)
    approvers: List[str] = Field(default=["Cynthia", "Usama"])
    next_phase: str = Field(default="scaffold_apply")
    data: ScaffoldPlanData


# ============================================================================
# Implementation Models
# ============================================================================

class FileChange(BaseModel):
    path: str = Field(..., min_length=1)
    action: str = Field(..., pattern=r"^(created|modified|deleted)$")
    lines_added: int = Field(default=0, ge=0)
    lines_removed: int = Field(default=0, ge=0)
    description: str = Field(..., min_length=10)


class TestResult(BaseModel):
    path: str = Field(..., min_length=1)
    type: str = Field(..., pattern=r"^(unit|integration|e2e)$")
    test_count: int = Field(..., ge=1)
    coverage_percentage: Optional[int] = Field(None, ge=0, le=100)


class AcceptanceCriteriaStatus(BaseModel):
    criteria: str = Field(..., min_length=5)
    status: str = Field(..., pattern=r"^(satisfied|not_satisfied|partial)$")
    evidence: str = Field(..., min_length=10)


class DefinitionOfDoneItem(BaseModel):
    item: str = Field(..., min_length=5)
    completed: bool
    notes: Optional[str] = None


class TechnicalDecision(BaseModel):
    decision: str = Field(..., min_length=10)
    rationale: str = Field(..., min_length=20)
    adr_reference: Optional[str] = Field(None, pattern=r"^ADR-\d{4}$")


class DependencyVerification(BaseModel):
    task_id: str = Field(..., pattern=r"^TASK-\d{3}$")
    status: str = Field(..., pattern=r"^(completed|blocked|in_progress)$")
    verified_at: datetime


class TestSummary(BaseModel):
    total: int = Field(..., ge=0)
    passed: int = Field(..., ge=0)
    failed: int = Field(..., ge=0)
    coverage: Optional[int] = Field(None, ge=0, le=100)


class TestResults(BaseModel):
    unit_tests: TestSummary
    integration_tests: TestSummary
    linting: Dict[str, Any] = Field(default_factory=dict)


class PerformanceMetrics(BaseModel):
    response_time_ms: Optional[int] = Field(None, ge=0)
    memory_usage_mb: Optional[int] = Field(None, ge=0)
    cpu_usage_percent: Optional[int] = Field(None, ge=0, le=100)


class SecurityChecklistItem(BaseModel):
    item: str = Field(..., min_length=5)
    status: str = Field(..., pattern=r"^(completed|not_applicable|pending)$")
    details: Optional[str] = None


class DocumentationUpdate(BaseModel):
    file: str = Field(..., min_length=1)
    description: str = Field(..., min_length=10)


class ImplementationData(BaseModel):
    task_id: str = Field(..., pattern=r"^TASK-\d{3}$")
    title: str = Field(..., min_length=5, max_length=100)
    implementation_date: datetime
    developer: str = Field(..., min_length=3)
    files_changed: List[FileChange] = Field(..., min_items=1)
    tests_added: List[TestResult] = Field(default_factory=list)
    acceptance_criteria_status: List[AcceptanceCriteriaStatus] = Field(..., min_items=1)
    definition_of_done_checklist: List[DefinitionOfDoneItem] = Field(..., min_items=1)
    technical_decisions: List[TechnicalDecision] = Field(default_factory=list)
    dependencies_verified: List[DependencyVerification] = Field(default_factory=list)
    test_results: TestResults
    performance_metrics: PerformanceMetrics = Field(default_factory=PerformanceMetrics)
    security_checklist: List[SecurityChecklistItem] = Field(default_factory=list)
    documentation_updates: List[DocumentationUpdate] = Field(default_factory=list)
    known_issues: List[str] = Field(default_factory=list)
    future_considerations: List[str] = Field(default_factory=list)


class ImplementationModel(BaseModel):
    artifact_type: str = Field(default="implementation")
    status: str = Field(default="complete")
    validation: ValidationStatus
    approval_required: bool = Field(default=True)
    approvers: List[str] = Field(default=["Mustaffa", "Usama"])
    next_phase: str = Field(default="integration")
    data: ImplementationData


# ============================================================================
# Work Session & Progress Tracking Models
# ============================================================================

class TaskProgressStatus(str, Enum):
    """Status of a task in the work session."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


class TaskProgress(BaseModel):
    """Tracks the progress of a single task."""
    task_id: str = Field(..., pattern=r"^TASK-\d{3}$")
    status: TaskProgressStatus = Field(default=TaskProgressStatus.PENDING)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    attempt_count: int = Field(default=0, ge=0)
    last_error: Optional[str] = None
    files_modified: List[str] = Field(default_factory=list)
    commits: List[str] = Field(default_factory=list, description="Commit SHAs for this task")
    notes: Optional[str] = None


class WorkSessionStatus(str, Enum):
    """Status of a work session."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CRASHED = "crashed"
    ABORTED = "aborted"


class WorkSession(BaseModel):
    """
    Represents a single work session.
    Persisted to docs/work-log.json for crash recovery.
    """
    session_id: str = Field(..., description="Unique session ID: WS-{timestamp}")
    started_at: datetime
    ended_at: Optional[datetime] = None
    status: WorkSessionStatus = Field(default=WorkSessionStatus.ACTIVE)
    plan_file: Optional[str] = Field(None, description="Path to plan file being executed")
    branch_name: Optional[str] = None
    worktree_path: Optional[str] = None

    # Progress tracking
    tasks_attempted: List[TaskProgress] = Field(default_factory=list)
    current_task_id: Optional[str] = Field(None, pattern=r"^TASK-\d{3}$")

    # Summary stats (updated on completion/crash)
    tasks_completed: int = Field(default=0, ge=0)
    tasks_failed: int = Field(default=0, ge=0)
    total_commits: int = Field(default=0, ge=0)
    total_files_changed: int = Field(default=0, ge=0)

    # Error recovery
    last_checkpoint: Optional[datetime] = None
    crash_reason: Optional[str] = None
    recovery_notes: Optional[str] = None


class WorkLogData(BaseModel):
    """
    Complete work log for a project.
    Stored at: {child-project}/docs/work-log.json
    """
    project_name: str = Field(..., min_length=3, max_length=100)
    created_at: datetime
    updated_at: datetime

    # All work sessions (newest first)
    sessions: List[WorkSession] = Field(default_factory=list)

    # Aggregated task status (source of truth for task completion)
    task_status: Dict[str, TaskProgress] = Field(
        default_factory=dict,
        description="Map of task_id -> TaskProgress for all tasks ever worked on"
    )

    # Quick stats
    total_sessions: int = Field(default=0, ge=0)
    total_tasks_completed: int = Field(default=0, ge=0)
    total_commits: int = Field(default=0, ge=0)


class WorkLogModel(BaseModel):
    """Artifact wrapper for work log."""
    artifact_type: str = Field(default="work_log")
    status: str = Field(default="active")
    validation: ValidationStatus
    data: WorkLogData


class ChangelogEntry(BaseModel):
    """Single entry in the changelog."""
    version: str = Field(..., description="Semantic version or session reference")
    date: datetime
    session_id: str = Field(..., description="Reference to work session")
    summary: str = Field(..., min_length=10)
    changes: List[str] = Field(..., min_items=1, description="List of changes made")
    tasks_completed: List[str] = Field(default_factory=list, description="TASK-### IDs completed")
    breaking_changes: List[str] = Field(default_factory=list)
    contributors: List[str] = Field(default_factory=list)


class ChangelogData(BaseModel):
    """
    Human-readable changelog for a project.
    Stored at: {child-project}/CHANGELOG.md (generated from this)
    """
    project_name: str = Field(..., min_length=3, max_length=100)
    entries: List[ChangelogEntry] = Field(default_factory=list)


class ChangelogModel(BaseModel):
    """Artifact wrapper for changelog."""
    artifact_type: str = Field(default="changelog")
    status: str = Field(default="active")
    data: ChangelogData


# ============================================================================
# Error Models
# ============================================================================

class ErrorModel(BaseModel):
    error: Dict[str, Any] = Field(..., description="Error details")


# ============================================================================
# Export all models
# ============================================================================

__all__ = [
    # Domain Mapping (Propose-Validate-Confirm pattern)
    'DomainSchema', 'DomainMapping',

    # Design Brief (UI/UX configuration)
    'DesignBrief', 'DesignBriefModel', 'ColorScheme', 'GlassmorphismConfig', 'TypographyConfig',

    # PRD
    'PRDModel', 'PRDData', 'Feature', 'UserStory', 'TechnicalRequirement',

    # Flow
    'FlowModel', 'FlowData', 'UserFlow', 'SystemFlow', 'FlowStep',

    # ERD
    'ERDModel', 'ERDData', 'Entity', 'Relationship', 'EntityAttribute', 'EntityIndex',

    # Journey
    'JourneyModel', 'JourneyData', 'Journey', 'JourneyPhase', 'Touchpoint', 'Persona',

    # Tasks
    'TasksModel', 'TasksData', 'Task', 'Epic', 'Sprint', 'TaskDependency', 'ContextPlan', 'TestingStrategy',

    # ADR
    'ADRModel', 'ADRData', 'Decision', 'DecisionMetadata', 'IndexEntry', 'Alternative', 'DecisionContext',

    # Scaffold
    'ScaffoldPlanModel', 'ScaffoldPlanData', 'TemplateApplication', 'FeatureSelections',

    # Implementation
    'ImplementationModel', 'ImplementationData', 'FileChange', 'TestResult',

    # Work Session & Progress Tracking
    'WorkLogModel', 'WorkLogData', 'WorkSession', 'TaskProgress',
    'ChangelogModel', 'ChangelogData', 'ChangelogEntry',
    'TaskProgressStatus', 'WorkSessionStatus',

    # Error
    'ErrorModel',

    # Enums
    'PriorityLevel', 'TaskType', 'ADRStatus', 'ValidationStatus', 'EmotionalState', 'TouchpointType',
    'DesignPreset', 'ArchitectureStyle', 'TaskProgressStatus', 'WorkSessionStatus'
]