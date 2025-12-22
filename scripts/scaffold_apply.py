#!/usr/bin/env python3
"""
Scaffold Apply Script (Stage 2)

Applies an approved scaffolding plan to the repository by creating the
declared directory structure, generating domain-based folders, applying
template variable substitution, and injecting architecture rules.

Features:
- Domain mapping: Creates src/domains/{domain}/ structure based on bounded contexts
- Design system: Applies color scheme from design brief to templates
- Template substitution: Replaces {{VARIABLE}} placeholders with actual values
- Architecture rules injection: Copies .claude/rules/, .eslintrc.js, .husky/, etc.

This script enforces human approval gates and validates inputs against
Pydantic models defined in app.models.
"""

import argparse
import json
import os
import re
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from pydantic import ValidationError

try:
    from app.models import ScaffoldPlanModel, PRDModel, ERDModel, ErrorModel
except Exception:
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from app.models import ScaffoldPlanModel, PRDModel, ERDModel, ErrorModel


REQUIRED_APPROVERS = {"Cynthia", "Usama"}
TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates" / "child-project"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())


def validate_inputs(prd_path: Path, erd_path: Path, plan_path: Path) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    prd = load_json(prd_path)
    erd = load_json(erd_path)
    plan = load_json(plan_path)

    try:
        PRDModel(**prd)
    except ValidationError as e:
        raise ValueError(f"PRD validation failed: {e}")

    try:
        ERDModel(**erd)
    except ValidationError as e:
        raise ValueError(f"ERD validation failed: {e}")

    try:
        ScaffoldPlanModel(**plan)
    except ValidationError as e:
        raise ValueError(f"Scaffold plan validation failed: {e}")

    prj_prd = prd.get("data", {}).get("project_name")
    prj_erd = erd.get("data", {}).get("project_name")
    prj_plan = plan.get("data", {}).get("project_name")
    if len({prj_prd, prj_erd, prj_plan}) != 1:
        raise ValueError("Inconsistent project_name across PRD, ERD, and scaffold plan")

    return prd, erd, plan


def require_approval(provided_approvers: List[str]) -> None:
    provided = set(a.strip() for a in provided_approvers)
    missing = REQUIRED_APPROVERS - provided
    if missing:
        raise PermissionError(f"Missing required approvers: {', '.join(sorted(missing))}")


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def build_template_variables(plan: Dict[str, Any], prd: Dict[str, Any], erd: Dict[str, Any]) -> Dict[str, Any]:
    """Build the complete set of template variables from plan, PRD, and ERD."""
    data = plan.get("data", {})
    prd_data = prd.get("data", {})
    erd_data = erd.get("data", {})

    project_name = data.get("project_name", "Project")
    project_slug = project_name.lower().replace(" ", "-").replace("_", "-")

    # Extract design brief
    design_brief = data.get("design_brief", {})
    colors = design_brief.get("colors", {})
    glassmorphism = design_brief.get("glassmorphism", {})
    typography = design_brief.get("typography", {})

    # Extract domain mapping
    domain_mapping = data.get("domain_mapping", {})
    domains = domain_mapping.get("domains", [])

    # Extract feature selections
    features = data.get("feature_selections", {})

    # Build variables dict
    variables = {
        # Project identity
        "PROJECT_NAME": project_name,
        "PROJECT_SLUG": project_slug,
        "VERSION": data.get("version", "1.0.0"),
        "CREATED_AT": datetime.now(timezone.utc).isoformat(),
        "GENERATED_AT": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),

        # Architecture
        "ARCHITECTURE_STYLE": data.get("architecture_style", "modular_monolith"),

        # Design preset
        "DESIGN_PRESET": design_brief.get("preset", "corporate"),
        "PRESET_CREATIVE": design_brief.get("preset") == "creative",
        "PRESET_CORPORATE": design_brief.get("preset") == "corporate",
        "PRESET_NEUTRAL": design_brief.get("preset") == "neutral",
        "PRESET_CUSTOM": design_brief.get("preset") == "custom",

        # Colors
        "PRIMARY_COLOR": colors.get("primary", "#14b8a6"),
        "SECONDARY_COLOR": colors.get("secondary", "#0d9488"),
        "ACCENT_COLOR_1": colors.get("accent", ["#0891b2"])[0] if colors.get("accent") else "#0891b2",
        "ACCENT_COLOR_2": colors.get("accent", ["#0891b2", "#0891b2"])[1] if len(colors.get("accent", [])) > 1 else "#0891b2",
        "BACKGROUND_COLOR": colors.get("background", "#ffffff"),
        "SURFACE_COLOR": colors.get("surface", "#f0fdfa"),
        "TEXT_PRIMARY": colors.get("text_primary", "#134e4a"),
        "TEXT_SECONDARY": colors.get("text_secondary", "#64748b"),
        "SUCCESS_COLOR": colors.get("success", "#10b981"),
        "WARNING_COLOR": colors.get("warning", "#f59e0b"),
        "ERROR_COLOR": colors.get("error", "#ef4444"),

        # Glassmorphism
        "GLASSMORPHISM_ENABLED": glassmorphism.get("enabled", True),
        "BLUR_INTENSITY": glassmorphism.get("blur_intensity", "xl"),
        "GLASS_OPACITY": int(glassmorphism.get("opacity", 0.7) * 100),
        "BORDER_OPACITY": int(glassmorphism.get("border_opacity", 0.3) * 100),
        "SHADOW_OPACITY": int(glassmorphism.get("shadow_color_opacity", 0.1) * 100),

        # Typography
        "FONT_HEADING": typography.get("font_family_heading", "Inter"),
        "FONT_BODY": typography.get("font_family_body", "Inter"),
        "FONT_MONO": typography.get("font_family_mono", "JetBrains Mono"),
        "FONT_BASE_SIZE": typography.get("base_size", "16px"),
        "FONT_SCALE_RATIO": typography.get("scale_ratio", 1.25),

        # Breakpoints
        "BREAKPOINT_SM": design_brief.get("responsive_breakpoints", {}).get("sm", "640px"),
        "BREAKPOINT_MD": design_brief.get("responsive_breakpoints", {}).get("md", "768px"),
        "BREAKPOINT_LG": design_brief.get("responsive_breakpoints", {}).get("lg", "1024px"),
        "BREAKPOINT_XL": design_brief.get("responsive_breakpoints", {}).get("xl", "1280px"),
        "BREAKPOINT_2XL": design_brief.get("responsive_breakpoints", {}).get("2xl", "1536px"),

        # Component style
        "COMPONENT_STYLE": design_brief.get("component_style", "rounded"),
        "STYLE_ROUNDED": design_brief.get("component_style") == "rounded",
        "STYLE_SHARP": design_brief.get("component_style") == "sharp",
        "STYLE_PILL": design_brief.get("component_style") == "pill",

        # Dark mode
        "DARK_MODE_ENABLED": design_brief.get("dark_mode_support", True),

        # Tech stack
        "DATABASE_TYPE": features.get("db", "postgres"),
        "AUTH_PROVIDER": features.get("auth", "nextauth"),
        "STORAGE_PROVIDER": features.get("storage", "s3"),
        "FRAMEWORK": features.get("framework", "nestjs"),
        "LANGUAGE": features.get("language", "typescript"),

        # Domains (for iteration in templates)
        "domains": domains,
    }

    return variables


def substitute_variables(content: str, variables: Dict[str, Any]) -> str:
    """Replace {{VARIABLE}} placeholders with actual values."""

    def replace_var(match):
        var_name = match.group(1)
        value = variables.get(var_name, match.group(0))
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (int, float)):
            return str(value)
        return str(value) if value is not None else ""

    # Replace simple {{VARIABLE}} patterns
    content = re.sub(r"\{\{([A-Z_0-9]+)\}\}", replace_var, content)

    # Handle conditional blocks: {{#if VAR}}...{{/if}}
    def process_conditionals(text: str) -> str:
        pattern = r"\{\{#if\s+([A-Z_0-9]+)\}\}(.*?)\{\{/if\}\}"
        while re.search(pattern, text, re.DOTALL):
            def replace_conditional(m):
                var_name = m.group(1)
                inner_content = m.group(2)
                var_value = variables.get(var_name, False)
                if var_value:
                    return inner_content
                return ""
            text = re.sub(pattern, replace_conditional, text, flags=re.DOTALL)
        return text

    content = process_conditionals(content)

    # Handle {{#each domains}}...{{/each}} blocks
    def process_each_domains(text: str) -> str:
        pattern = r"\{\{#each domains\}\}(.*?)\{\{/each\}\}"
        domains = variables.get("domains", [])

        def replace_each(m):
            template = m.group(1)
            result = []
            for domain in domains:
                item = template
                item = item.replace("{{name}}", domain.get("name", ""))
                item = item.replace("{{description}}", domain.get("description", ""))
                item = item.replace("{{root_entity}}", domain.get("root_entity", ""))
                item = item.replace("{{entities}}", ", ".join(domain.get("entities", [])))
                item = item.replace("{{dependencies}}", ", ".join(domain.get("dependencies", [])) or "None")
                features = domain.get("feature_ids", [])
                item = item.replace("{{features}}", ", ".join(features))
                result.append(item)
            return "".join(result)

        return re.sub(pattern, replace_each, text, flags=re.DOTALL)

    content = process_each_domains(content)

    return content


def apply_template_file(source_path: Path, target_path: Path, variables: Dict[str, Any], dry_run: bool) -> bool:
    """Apply a single template file with variable substitution."""
    if not source_path.exists():
        return False

    content = source_path.read_text()
    content = substitute_variables(content, variables)

    if not dry_run:
        ensure_directory(target_path.parent)
        # Remove .template extension if present
        final_path = target_path
        if final_path.suffix == ".template":
            final_path = final_path.with_suffix("")
        final_path.write_text(content)
        return True
    return True


def create_domain_structure(project_root: Path, domains: List[Dict[str, Any]], dry_run: bool) -> List[Dict[str, Any]]:
    """Create the domain directory structure for both frontend and backend."""
    domains_created = []

    for domain in domains:
        domain_name = domain.get("name", "unknown")
        files_created = 0
        dirs_created = 0

        # Frontend domain structure
        frontend_domain_path = project_root / "src" / "domains" / domain_name
        frontend_dirs = [
            frontend_domain_path,
            frontend_domain_path / "components",
            frontend_domain_path / "constants",
            frontend_domain_path / "hooks",
        ]

        for dir_path in frontend_dirs:
            if not dry_run:
                ensure_directory(dir_path)
                dirs_created += 1

        # Create barrel exports for frontend
        frontend_files = {
            frontend_domain_path / "index.ts": f"// {domain_name} domain barrel export\nexport * from './components'\nexport * from './constants'\n",
            frontend_domain_path / "components" / "index.ts": f"// {domain_name} components barrel\n// Export components as they are created\n",
            frontend_domain_path / "constants" / "index.ts": f"// {domain_name} constants barrel\n// Export content constants as they are created\n",
            frontend_domain_path / "hooks" / "index.ts": f"// {domain_name} hooks barrel\n// Export hooks as they are created\n",
        }

        for file_path, content in frontend_files.items():
            if not dry_run:
                ensure_directory(file_path.parent)
                file_path.write_text(content)
                files_created += 1

        # Backend domain structure (if TypeScript backend)
        backend_domain_path = project_root / "src" / "domains" / domain_name
        if not backend_domain_path.exists() or not (backend_domain_path / "features").exists():
            backend_dirs = [
                backend_domain_path / "features",
            ]
            for dir_path in backend_dirs:
                if not dry_run:
                    ensure_directory(dir_path)
                    dirs_created += 1

            # Backend barrel exports
            backend_files = {
                backend_domain_path / "features" / "index.ts": f"// {domain_name} features barrel export\n// Export features as they are created\n",
            }

            # Only create if doesn't exist (don't overwrite frontend index.ts)
            for file_path, content in backend_files.items():
                if not file_path.exists():
                    if not dry_run:
                        ensure_directory(file_path.parent)
                        file_path.write_text(content)
                        files_created += 1

        domains_created.append({
            "name": domain_name,
            "files_created": files_created,
            "directories_created": dirs_created,
        })

    return domains_created


def inject_architecture_rules(project_root: Path, variables: Dict[str, Any], dry_run: bool) -> int:
    """Inject .claude/rules/ files into the project."""
    files_injected = 0
    rules_source = TEMPLATES_DIR / ".claude" / "rules"
    rules_target = project_root / ".claude" / "rules"

    if rules_source.exists():
        for template_file in rules_source.glob("*.template"):
            target_file = rules_target / template_file.name.replace(".template", "")
            if apply_template_file(template_file, target_file, variables, dry_run):
                files_injected += 1

    return files_injected


def inject_quality_tools(project_root: Path, variables: Dict[str, Any], dry_run: bool) -> int:
    """Inject ESLint, Prettier, Husky configurations."""
    files_injected = 0

    # ESLint
    eslint_source = TEMPLATES_DIR / ".eslintrc.js.template"
    if eslint_source.exists():
        target = project_root / ".eslintrc.js"
        if apply_template_file(eslint_source, target, variables, dry_run):
            files_injected += 1

    # Prettier
    prettier_source = TEMPLATES_DIR / ".prettierrc.template"
    if prettier_source.exists():
        target = project_root / ".prettierrc"
        if apply_template_file(prettier_source, target, variables, dry_run):
            files_injected += 1

    # Husky
    husky_source = TEMPLATES_DIR / ".husky" / "pre-commit.template"
    if husky_source.exists():
        target = project_root / ".husky" / "pre-commit"
        if apply_template_file(husky_source, target, variables, dry_run):
            files_injected += 1
            # Make pre-commit executable
            if not dry_run and target.exists():
                target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # Tailwind config
    tailwind_source = TEMPLATES_DIR / "tailwind.config.js.template"
    if tailwind_source.exists():
        target = project_root / "tailwind.config.js"
        if apply_template_file(tailwind_source, target, variables, dry_run):
            files_injected += 1

    return files_injected


def inject_ai_context(project_root: Path, variables: Dict[str, Any], dry_run: bool) -> int:
    """Inject CLAUDE.md, KREATIVREASON-GUIDE.md, .cursorrules, PROJECT_CONTEXT.md.

    Direct copy files (CLAUDE.md, KREATIVREASON-GUIDE.md) are copied as-is without
    variable substitution - these are the canonical architecture guides that should
    be used "without change" in every child project.
    """
    files_injected = 0

    # Direct copy files FIRST - canonical architecture guides (no variable substitution)
    # These files are intentionally copied without modification
    direct_copy_files = [
        "CLAUDE.md",
        "KREATIVREASON-GUIDE.md",
    ]

    for filename in direct_copy_files:
        source = TEMPLATES_DIR / filename
        target = project_root / filename
        if source.exists():
            if not dry_run:
                ensure_directory(target.parent)
                target.write_text(source.read_text())
            files_injected += 1

    # Template files (with variable substitution) - for project-specific context
    templates = [
        (".cursorrules.template", ".cursorrules"),
        ("PROJECT_CONTEXT.md.template", "PROJECT_CONTEXT.md"),
    ]

    for source_name, target_name in templates:
        source = TEMPLATES_DIR / source_name
        if source.exists():
            target = project_root / target_name
            if apply_template_file(source, target, variables, dry_run):
                files_injected += 1

    return files_injected


def inject_design_system(project_root: Path, variables: Dict[str, Any], dry_run: bool) -> int:
    """Inject glassmorphism UI components."""
    files_injected = 0
    ui_source = TEMPLATES_DIR / "src" / "components" / "ui"
    ui_target = project_root / "src" / "components" / "ui"

    if ui_source.exists():
        for template_file in ui_source.glob("*.template"):
            target_file = ui_target / template_file.name.replace(".template", "")
            if apply_template_file(template_file, target_file, variables, dry_run):
                files_injected += 1

    # Also inject utils/cn.ts
    utils_source = TEMPLATES_DIR / "src" / "utils" / "cn.ts.template"
    if utils_source.exists():
        target = project_root / "src" / "utils" / "cn.ts"
        if apply_template_file(utils_source, target, variables, dry_run):
            files_injected += 1

    return files_injected


def write_placeholder_file(path: Path, project_name: str) -> None:
    ensure_directory(path.parent)
    content = generate_placeholder_content(path, project_name)
    if not path.exists():
        path.write_text(content)


def generate_placeholder_content(path: Path, project_name: str) -> str:
    """Generate placeholder content appropriate for the file type."""
    suffix = path.suffix.lower()
    filename = path.name.lower()

    if suffix in {".py"}:
        return (
            '"""\nAuto-generated placeholder file.\n"""\n\n'
            f'if __name__ == "__main__":\n'
            f'    print("{project_name} placeholder: {path}")\n'
        )

    if suffix in {".ts", ".js"}:
        if any(pattern in filename for pattern in ['.module.', '.service.', '.controller.', '.entity.', '.dto.']):
            return _generate_nestjs_placeholder(path, project_name, filename)
        return f"// Auto-generated placeholder for {project_name}\nexport {{}}\n"

    if suffix in {".tsx", ".jsx"}:
        return f"// Auto-generated placeholder for {project_name}\nexport default function Placeholder() {{\n  return (<div>Placeholder: {path}</div>);\n}}\n"

    if suffix in {".sql"}:
        return f"-- Auto-generated placeholder migration for {project_name}\n-- File: {path}\n"

    if suffix in {".json"}:
        return json.dumps({"placeholder": True, "project": project_name}, indent=2)

    if suffix in {".md"}:
        return f"# Placeholder\n\nFile: {path}\nProject: {project_name}\n"

    if path.name == "Makefile":
        return "# Placeholder Makefile\n\n.DEFAULT_GOAL := help\n\nhelp:\n\t@echo 'Replace with real Makefile content.'\n"

    return f"// Placeholder for {project_name}: {path}\n"


def _generate_nestjs_placeholder(path: Path, project_name: str, filename: str) -> str:
    """Generate appropriate NestJS placeholder based on file type."""
    parts = filename.replace('.ts', '').replace('.js', '').split('.')
    if len(parts) >= 2:
        base_name = ''.join(word.capitalize() for word in parts[0].split('-'))
        file_type = parts[1].capitalize()
        class_name = f"{base_name}{file_type}"
    else:
        class_name = "Placeholder"

    if '.module.' in filename:
        return f"import {{ Module }} from '@nestjs/common';\n\n@Module({{}})\nexport class {class_name} {{}}\n"
    elif '.service.' in filename:
        return f"import {{ Injectable }} from '@nestjs/common';\n\n@Injectable()\nexport class {class_name} {{}}\n"
    elif '.controller.' in filename:
        return f"import {{ Controller }} from '@nestjs/common';\n\n@Controller()\nexport class {class_name} {{}}\n"
    elif '.entity.' in filename:
        return f"import {{ Entity, PrimaryGeneratedColumn }} from 'typeorm';\n\n@Entity()\nexport class {class_name} {{\n  @PrimaryGeneratedColumn('uuid')\n  id!: string;\n}}\n"
    elif '.dto.' in filename:
        return f"export class {class_name} {{}}\n"
    else:
        return f"export class {class_name} {{}}\n"


def collect_fs_metadata(path: Path) -> Dict[str, Any]:
    st = path.stat()
    perm = stat.S_IMODE(st.st_mode)
    return {
        "path": str(path).replace("\\", "/"),
        "size_bytes": st.st_size,
        "permissions": f"{perm:o}",
    }


def apply_plan(plan: Dict[str, Any], prd: Dict[str, Any], erd: Dict[str, Any], project_root: Path, dry_run: bool) -> Dict[str, Any]:
    """Apply the complete scaffolding plan."""
    data = plan.get("data", {})
    project_name = data.get("project_name", "Project")

    # Build template variables
    variables = build_template_variables(plan, prd, erd)

    # Results tracking
    files_created: List[Dict[str, Any]] = []
    templates_applied: List[Dict[str, Any]] = []

    # 1. Create directory structure
    directory_structure = data.get("directory_structure", {})
    for dir_path in directory_structure.keys():
        target_dir = (project_root / dir_path).resolve()
        if not dry_run:
            ensure_directory(target_dir)

    # 2. Create domain structure
    domains = data.get("domain_mapping", {}).get("domains", [])
    domains_created = create_domain_structure(project_root, domains, dry_run)

    # 3. Inject architecture rules (if enabled)
    arch_files = 0
    if data.get("inject_architecture_rules", True):
        arch_files = inject_architecture_rules(project_root, variables, dry_run)
        templates_applied.append({
            "template_id": "ARCH-RULES",
            "status": "success",
            "files_created": arch_files,
            "directories_created": 1,
        })

    # 4. Inject quality tools (if enabled)
    quality_files = 0
    if data.get("inject_husky", True) or data.get("inject_eslint_config", True):
        quality_files = inject_quality_tools(project_root, variables, dry_run)
        templates_applied.append({
            "template_id": "QUALITY-TOOLS",
            "status": "success",
            "files_created": quality_files,
            "directories_created": 1,
        })

    # 5. Inject AI context files
    ai_files = inject_ai_context(project_root, variables, dry_run)
    templates_applied.append({
        "template_id": "AI-CONTEXT",
        "status": "success",
        "files_created": ai_files,
        "directories_created": 0,
    })

    # 6. Inject design system (if enabled)
    design_files = 0
    if data.get("inject_design_system", True):
        design_files = inject_design_system(project_root, variables, dry_run)
        templates_applied.append({
            "template_id": "DESIGN-SYSTEM",
            "status": "success",
            "files_created": design_files,
            "directories_created": 2,
        })

    # 7. Apply additional templates from plan
    for template in data.get("templates_to_apply", []):
        template_id = template.get("id")
        target_path = template.get("target_path", "")
        files = template.get("files_to_generate", [])

        created_count = 0
        for rel_file in files:
            normalized_target = target_path.lstrip('/').rstrip('/')
            if normalized_target and not rel_file.startswith(normalized_target):
                full_path = f"{normalized_target}/{rel_file}"
            else:
                full_path = rel_file

            file_path = (project_root / full_path).resolve()
            if not dry_run:
                write_placeholder_file(file_path, project_name)
            if file_path.exists():
                files_created.append(collect_fs_metadata(file_path))
                created_count += 1

        templates_applied.append({
            "template_id": template_id,
            "status": "success" if created_count == len(files) else "partial",
            "files_created": created_count,
            "directories_created": 0,
        })

    return {
        "files_created": files_created,
        "templates_applied": templates_applied,
        "domains_created": domains_created,
        "architecture_rules_injected": data.get("inject_architecture_rules", True),
        "husky_configured": data.get("inject_husky", True),
        "eslint_configured": data.get("inject_eslint_config", True),
        "design_system_injected": data.get("inject_design_system", True),
    }


def emit_error(code: str, message: str, details: List[str]) -> None:
    err = {
        "error": {
            "code": code,
            "message": message,
            "details": details,
            "artifact": "scaffold",
            "remediation": "Check template paths, approvals, and input artifacts"
        }
    }
    print(json.dumps(err, indent=2))
    sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply an approved scaffold plan with domain mapping and design system")
    parser.add_argument("--plan", required=True, help="Path to scaffold_plan.json")
    parser.add_argument("--prd", required=True, help="Path to PRD JSON")
    parser.add_argument("--erd", required=True, help="Path to ERD JSON")
    parser.add_argument("--approved-by", action="append", default=[], help="Approver name (can be repeated)")
    parser.add_argument("--output", required=True, help="Path to write scaffold_applied JSON result")
    parser.add_argument("--project-dir", help="Target directory for generated project")
    parser.add_argument("--dry-run", action="store_true", help="Validate and report without creating files")

    args = parser.parse_args()

    plan_path = Path(args.plan).resolve()
    prd_path = Path(args.prd).resolve()
    erd_path = Path(args.erd).resolve()
    output_path = Path(args.output).resolve()

    plan_data = load_json(plan_path)
    project_name = plan_data.get("data", {}).get("project_name", "unknown-project")
    project_name_slug = project_name.lower().replace(" ", "-")

    if args.project_dir:
        project_root = Path(args.project_dir).resolve()
    else:
        factory_root = Path(__file__).resolve().parents[1]
        project_root = (factory_root / ".." / "generated-projects" / project_name_slug).resolve()

    try:
        prd, erd, plan = validate_inputs(prd_path, erd_path, plan_path)
        require_approval(args.approved_by)

        apply_results = apply_plan(plan, prd, erd, project_root, args.dry_run)

        now = datetime.now(timezone.utc).isoformat()
        result = {
            "artifact_type": "scaffold_applied",
            "status": "complete",
            "validation": "passed",
            "approval_required": False,
            "next_phase": "development",
            "data": {
                "project_name": plan.get("data", {}).get("project_name"),
                "project_root": str(project_root),
                "applied_at": now,
                "mode": "apply",
                **apply_results,
                "setup_instructions": [
                    "Run 'npm install' to install dependencies",
                    "Run 'npx husky install' to set up git hooks",
                    "Copy .env.example to .env and fill in values",
                    "Run 'npm run db:generate' to generate Prisma client",
                    "Run 'npm run dev' to start development server"
                ]
            }
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2))
        print(json.dumps(result, indent=2))
        sys.exit(0)

    except PermissionError as e:
        emit_error("APPROVAL_REQUIRED", str(e), ["Provide --approved-by Cynthia --approved-by Usama"])
    except FileNotFoundError as e:
        emit_error("FILE_NOT_FOUND", str(e), ["Verify input paths exist"])
    except ValueError as e:
        emit_error("VALIDATION_FAILED", str(e), ["Run linters: python -m app.lint_prd, python -m app.lint_erd"])
    except Exception as e:
        emit_error("SCAFFOLD_FAILED", f"Unexpected error: {e}", [])


if __name__ == "__main__":
    main()
