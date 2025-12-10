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
    feature_selections: FeatureSelections
    templates_to_apply: List[TemplateApplication] = Field(..., min_items=1)
    directory_structure: Dict[str, str] = Field(..., min_items=1)
    dependencies: Dict[str, List[str]] = Field(..., min_items=1)
    environment_variables: List[EnvironmentVariable] = Field(default_factory=list)
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
# Error Models
# ============================================================================

class ErrorModel(BaseModel):
    error: Dict[str, Any] = Field(..., description="Error details")


# ============================================================================
# Export all models
# ============================================================================

__all__ = [
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
    
    # Error
    'ErrorModel',
    
    # Enums
    'PriorityLevel', 'TaskType', 'ADRStatus', 'ValidationStatus', 'EmotionalState', 'TouchpointType'
]