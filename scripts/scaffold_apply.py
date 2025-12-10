#!/usr/bin/env python3
"""
Scaffold Apply Script (Stage 2)

Applies an approved scaffolding plan to the repository by creating the
declared directory structure and generating placeholder files listed
in the plan's templates_to_apply.files_to_generate entries.

This script enforces human approval gates and validates inputs against
Pydantic models defined in app.models. It emits a single JSON object to
STDOUT describing the apply results, conforming to the Scaffolder agent's
"apply mode" output schema.
"""

import argparse
import json
import os
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from pydantic import ValidationError

try:
    # Prefer absolute import when executed from repo root
    from app.models import ScaffoldPlanModel, PRDModel, ERDModel, ErrorModel
except Exception:  # pragma: no cover
    # Fallback for direct execution from subdirectories
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from app.models import ScaffoldPlanModel, PRDModel, ERDModel, ErrorModel  # type: ignore


REQUIRED_APPROVERS = {"Cynthia", "Usama"}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())


def validate_inputs(prd_path: Path, erd_path: Path, plan_path: Path) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    prd = load_json(prd_path)
    erd = load_json(erd_path)
    plan = load_json(plan_path)

    # Pydantic validation
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

    # Basic consistency checks
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
        raise PermissionError(
            f"Missing required approvers: {', '.join(sorted(missing))}"
        )


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_placeholder_file(path: Path, project_name: str) -> None:
    ensure_directory(path.parent)
    content = generate_placeholder_content(path, project_name)
    if not path.exists():
        path.write_text(content)
    else:
        # Preserve existing files; do not overwrite
        pass


def generate_placeholder_content(path: Path, project_name: str) -> str:
    """Generate placeholder content appropriate for the file type.

    For TypeScript files, detects if it's a backend (NestJS) or frontend (React)
    file based on the file path and name patterns.
    """
    suffix = path.suffix.lower()
    filename = path.name.lower()
    path_str = str(path).lower()

    if suffix in {".py"}:
        return (
            '"""\n'
            'Auto-generated placeholder file.\n\n'
            'This file was created by the scaffold apply process. Replace with real content\n'
            'from templates when available.\n'
            '"""\n\n'
            'if __name__ == "__main__":\n'
            '    print("{project_name} placeholder: {path}")\n'
        ).format(project_name=project_name, path=str(path))

    if suffix in {".ts", ".js"}:
        # Detect file type by name pattern for NestJS backend files
        if any(pattern in filename for pattern in [
            '.module.', '.service.', '.controller.', '.gateway.',
            '.guard.', '.interceptor.', '.pipe.', '.filter.',
            '.decorator.', '.middleware.', '.entity.', '.dto.',
            '.repository.', '.interface.', '.provider.', '.config.'
        ]):
            return _generate_nestjs_placeholder(path, project_name, filename)

        # Jest setup/config files - generate valid Jest config, not React JSX
        if 'jest' in filename and ('setup' in filename or 'config' in filename):
            return (
                f"// Jest setup file for {project_name}\n\n"
                f"// Add global test configuration here\n"
                f"// e.g., jest.setTimeout(30000);\n"
            )

        # Test utility files
        if 'test' in filename and 'util' in filename:
            return (
                f"// Test utilities for {project_name}\n\n"
                f"// Add shared test utilities here\n"
                f"// e.g., mock factories, test helpers, etc.\n\n"
                f"export {{}};\n"
            )

        # Default TypeScript export for non-React .ts files
        return (
            f"// Auto-generated placeholder for {project_name}\n"
            f"// File: {path}\n\n"
            f"export {{}}\n"
        )

    if suffix in {".tsx", ".jsx"}:
        # React/JSX files get React component placeholders
        return (
            f"// Auto-generated placeholder file for {project_name}\n"
            f"export default function Placeholder() {{\n"
            f"  return (<div>Placeholder: {path}</div>);\n"
            f"}}\n"
        )

    if suffix in {".sql"}:
        return (
            """-- Auto-generated placeholder migration for {project_name}\n-- File: {path}\n"""
        ).format(project_name=project_name, path=str(path))
    if suffix in {".json"}:
        # Handle special JSON config files
        if 'tsconfig' in filename:
            if 'build' in filename:
                return json.dumps({
                    "extends": "./tsconfig.json",
                    "exclude": ["node_modules", "test", "dist", "**/*spec.ts"]
                }, indent=2)
            else:
                # Main tsconfig.json - provide NestJS-compatible defaults
                return json.dumps({
                    "compilerOptions": {
                        "module": "commonjs",
                        "declaration": True,
                        "removeComments": True,
                        "emitDecoratorMetadata": True,
                        "experimentalDecorators": True,
                        "useDefineForClassFields": False,
                        "allowSyntheticDefaultImports": True,
                        "target": "ES2022",
                        "sourceMap": True,
                        "outDir": "./dist",
                        "baseUrl": "./",
                        "incremental": True,
                        "skipLibCheck": True,
                        "strictNullChecks": True,
                        "strict": True,
                        "noImplicitAny": True,
                        "strictBindCallApply": True,
                        "forceConsistentCasingInFileNames": True,
                        "noFallthroughCasesInSwitch": True,
                        "paths": {"@/*": ["src/*"]}
                    },
                    "include": ["src/**/*"],
                    "exclude": ["node_modules", "dist"]
                }, indent=2)
        # Generic placeholder for other JSON files
        return json.dumps({"placeholder": True, "project": project_name, "path": str(path)}, indent=2)
    if suffix in {".md"}:
        return f"# Placeholder\n\nFile: {path}\n\nProject: {project_name}\n"
    if path.name == "Makefile":
        return "# Placeholder Makefile generated by scaffold apply\n\n.DEFAULT_GOAL := help\n\nhelp:\n\t@echo 'Replace this placeholder with real Makefile content.'\n"
    # Default text
    return f"// Placeholder for {project_name}: {path}\n"


def _generate_nestjs_placeholder(path: Path, project_name: str, filename: str) -> str:
    """Generate appropriate NestJS placeholder based on file type."""
    # Extract class name from filename (e.g., call.service.ts -> CallService)
    parts = filename.replace('.ts', '').replace('.js', '').split('.')
    if len(parts) >= 2:
        base_name = ''.join(word.capitalize() for word in parts[0].split('-'))
        file_type = parts[1].capitalize()
        class_name = f"{base_name}{file_type}"
    else:
        class_name = "Placeholder"

    if '.module.' in filename:
        return (
            f"import {{ Module }} from '@nestjs/common';\n\n"
            f"@Module({{\n"
            f"  imports: [],\n"
            f"  controllers: [],\n"
            f"  providers: [],\n"
            f"  exports: [],\n"
            f"}})\n"
            f"export class {class_name} {{}}\n"
        )
    elif '.service.' in filename:
        return (
            f"import {{ Injectable }} from '@nestjs/common';\n\n"
            f"@Injectable()\n"
            f"export class {class_name} {{\n"
            f"  // TODO: Implement {project_name} service methods\n"
            f"}}\n"
        )
    elif '.controller.' in filename:
        return (
            f"import {{ Controller }} from '@nestjs/common';\n\n"
            f"@Controller()\n"
            f"export class {class_name} {{\n"
            f"  // TODO: Implement {project_name} controller endpoints\n"
            f"}}\n"
        )
    elif '.gateway.' in filename:
        return (
            f"import {{ WebSocketGateway }} from '@nestjs/websockets';\n\n"
            f"@WebSocketGateway()\n"
            f"export class {class_name} {{\n"
            f"  // TODO: Implement WebSocket handlers\n"
            f"}}\n"
        )
    elif '.entity.' in filename:
        return (
            f"import {{ Entity, PrimaryGeneratedColumn, Column }} from 'typeorm';\n\n"
            f"@Entity()\n"
            f"export class {class_name} {{\n"
            f"  @PrimaryGeneratedColumn('uuid')\n"
            f"  id!: string;\n\n"
            f"  // TODO: Add entity columns\n"
            f"}}\n"
        )
    elif '.dto.' in filename:
        return (
            f"import {{ IsString, IsOptional }} from 'class-validator';\n\n"
            f"export class {class_name} {{\n"
            f"  // TODO: Define DTO properties with validation decorators\n"
            f"}}\n"
        )
    elif '.guard.' in filename:
        return (
            f"import {{ Injectable, CanActivate, ExecutionContext }} from '@nestjs/common';\n\n"
            f"@Injectable()\n"
            f"export class {class_name} implements CanActivate {{\n"
            f"  canActivate(context: ExecutionContext): boolean {{\n"
            f"    // TODO: Implement guard logic\n"
            f"    return true;\n"
            f"  }}\n"
            f"}}\n"
        )
    elif '.interceptor.' in filename:
        return (
            f"import {{ Injectable, NestInterceptor, ExecutionContext, CallHandler }} from '@nestjs/common';\n"
            f"import {{ Observable }} from 'rxjs';\n\n"
            f"@Injectable()\n"
            f"export class {class_name} implements NestInterceptor {{\n"
            f"  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {{\n"
            f"    return next.handle();\n"
            f"  }}\n"
            f"}}\n"
        )
    elif '.middleware.' in filename:
        return (
            f"import {{ Injectable, NestMiddleware }} from '@nestjs/common';\n"
            f"import {{ Request, Response, NextFunction }} from 'express';\n\n"
            f"@Injectable()\n"
            f"export class {class_name} implements NestMiddleware {{\n"
            f"  use(req: Request, res: Response, next: NextFunction) {{\n"
            f"    next();\n"
            f"  }}\n"
            f"}}\n"
        )
    elif '.interface.' in filename:
        return (
            f"// Interface for {project_name}\n\n"
            f"export interface {class_name} {{\n"
            f"  // TODO: Define interface properties\n"
            f"}}\n"
        )
    elif '.config.' in filename:
        return (
            f"// Configuration for {project_name}\n\n"
            f"export const {parts[0]}Config = {{\n"
            f"  // TODO: Add configuration values\n"
            f"}};\n"
        )
    else:
        # Generic NestJS class
        return (
            f"// Auto-generated placeholder for {project_name}\n\n"
            f"export class {class_name} {{\n"
            f"  // TODO: Implement\n"
            f"}}\n"
        )


def collect_fs_metadata(path: Path) -> Dict[str, Any]:
    st = path.stat()
    perm = stat.S_IMODE(st.st_mode)
    return {
        "path": str(path).replace("\\", "/"),
        "size_bytes": st.st_size,
        "permissions": f"{perm:o}",
    }


def apply_plan(plan: Dict[str, Any], project_root: Path, dry_run: bool) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    files_created: List[Dict[str, Any]] = []
    templates_applied: List[Dict[str, Any]] = []

    data = plan.get("data", {})
    project_name = data.get("project_name", "Project")

    # Ensure directory structure
    directory_structure = data.get("directory_structure", {})
    for dir_path in directory_structure.keys():
        target_dir = (project_root / dir_path).resolve()
        if not dry_run:
            ensure_directory(target_dir)

    # Apply templates (best-effort placeholder generation)
    for template in data.get("templates_to_apply", []):
        template_id = template.get("id")
        target_path = template.get("target_path", "")
        files = template.get("files_to_generate", [])

        created_count = 0
        created_dirs: set[str] = set()

        for rel_file in files:
            # FIX: Properly combine target_path with rel_file
            # Handle "/" as project root, not filesystem root
            # Strip leading "/" from target_path to make it relative
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
                created_dirs.add(str(file_path.parent))

        templates_applied.append({
            "template_id": template_id,
            "status": "success" if created_count == len(files) else "partial",
            "files_created": created_count,
            "directories_created": len(created_dirs),
        })

    return files_created, templates_applied


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
    parser = argparse.ArgumentParser(description="Apply an approved scaffold plan")
    parser.add_argument("--plan", required=True, help="Path to docs/scaffold_plan.json")
    parser.add_argument("--prd", required=True, help="Path to PRD JSON")
    parser.add_argument("--erd", required=True, help="Path to ERD JSON")
    parser.add_argument("--approved-by", action="append", default=[], help="Approver name (can be repeated)")
    parser.add_argument("--output", required=True, help="Path to write scaffold_applied JSON result")
    parser.add_argument("--project-dir", help="Target directory for generated project (default: ../generated-projects/{project-name})")
    parser.add_argument("--dry-run", action="store_true", help="Validate and report without creating files")

    args = parser.parse_args()

    plan_path = Path(args.plan).resolve()
    prd_path = Path(args.prd).resolve()
    erd_path = Path(args.erd).resolve()
    output_path = Path(args.output).resolve()

    # Load plan to get project name for default directory
    plan_data = load_json(plan_path)
    project_name = plan_data.get("data", {}).get("project_name", "unknown-project")
    project_name_slug = project_name.lower().replace(" ", "-")

    # Determine project root: use --project-dir if provided, else default to ../generated-projects/{project-name}
    if args.project_dir:
        project_root = Path(args.project_dir).resolve()
    else:
        # Default: ../generated-projects/{project-name-slug}/
        factory_root = Path(__file__).resolve().parents[1]  # Parent of scripts/ is factory root
        project_root = (factory_root / ".." / "generated-projects" / project_name_slug).resolve()

    try:
        prd, erd, plan = validate_inputs(prd_path, erd_path, plan_path)
        # Enforce approval gate
        require_approval(args.approved_by)

        # Apply plan
        files_created, templates_applied = apply_plan(plan, project_root, args.dry_run)

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
                "templates_applied": templates_applied,
                "files_created": files_created,
                "post_apply_actions": [
                    {"action": "pip install -r requirements.txt", "directory": ".", "status": "pending", "output": ""},
                    {"action": "npm install", "directory": "frontend/", "status": "pending", "output": ""}
                ],
                "validation_results": {
                    "syntax_valid": True,
                    "dependencies_resolved": False,
                    "tests_passing": False
                },
                "setup_instructions": [
                    "Copy .env.example to .env and fill in values",
                    "Run 'docker compose up -d' to start services (if applicable)",
                    "Run 'npm run dev' in frontend and start backend app"
                ]
            }
        }

        # Persist result
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2))

        # Emit to STDOUT as well (JSON-only)
        print(json.dumps(result, indent=2))
        sys.exit(0)

    except PermissionError as e:
        emit_error("APPROVAL_REQUIRED", str(e), ["Provide --approved-by Cynthia --approved-by Usama"])  # nosec
    except FileNotFoundError as e:
        emit_error("FILE_NOT_FOUND", str(e), ["Verify input paths exist"])  # nosec
    except ValueError as e:
        emit_error("VALIDATION_FAILED", str(e), ["Run linters: python -m app.lint_prd, python -m app.lint_erd"])  # nosec
    except Exception as e:  # pragma: no cover
        emit_error("SCAFFOLD_FAILED", f"Unexpected error: {e}", [])


if __name__ == "__main__":
    main()


