#!/usr/bin/env python3
"""
PRD Validation Utility

Validates Product Requirements Document JSON against Pydantic model and
business rules. Provides detailed error reporting and consistency checks.

Usage:
    python -m app.lint_prd docs/prd.json
    python -m app.lint_prd --fix docs/prd.json  # Auto-fix issues where possible
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
from pydantic import ValidationError

from app.models import PRDModel, PriorityLevel


class PRDLinter:
    """PRD validation and linting utility."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.fixes_applied = []
    
    def lint_file(self, file_path: str, auto_fix: bool = False) -> Tuple[bool, Dict[str, Any]]:
        """Lint a PRD JSON file.
        
        Returns:
            (is_valid, report_data)
        """
        try:
            prd_data = self._load_json(file_path)
            return self.lint_data(prd_data, auto_fix, file_path)
        except Exception as e:
            self.errors.append(f"Failed to load file {file_path}: {e}")
            return False, self._generate_report()
    
    def lint_data(self, data: Dict[str, Any], auto_fix: bool = False, file_path: str = None) -> Tuple[bool, Dict[str, Any]]:
        """Lint PRD data structure."""
        
        # 1. Pydantic validation
        pydantic_valid = self._validate_pydantic(data)
        
        # 2. Business rule validation
        self._validate_business_rules(data)
        
        # 3. Consistency checks
        self._validate_consistency(data)
        
        # 4. Auto-fix issues if requested
        if auto_fix and file_path:
            self._apply_fixes(data, file_path)
        
        is_valid = pydantic_valid and len(self.errors) == 0
        return is_valid, self._generate_report()
    
    def _load_json(self, file_path: str) -> Dict[str, Any]:
        """Load and parse JSON file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return json.loads(path.read_text())
    
    def _validate_pydantic(self, data: Dict[str, Any]) -> bool:
        """Validate against Pydantic model."""
        try:
            PRDModel(**data)
            return True
        except ValidationError as e:
            for error in e.errors():
                location = " -> ".join(str(loc) for loc in error['loc'])
                self.errors.append(f"Validation error at {location}: {error['msg']}")
            return False
    
    def _validate_business_rules(self, data: Dict[str, Any]):
        """Validate business-specific rules."""
        if 'data' not in data:
            return
        
        prd_data = data['data']
        
        # Rule: At least one high-priority feature
        high_priority_features = [
            f for f in prd_data.get('features', [])
            if f.get('priority') == 'high'
        ]
        if not high_priority_features:
            self.warnings.append("No high-priority features defined. Consider prioritizing critical features.")
        
        # Rule: Each feature should have at least one user story
        for feature in prd_data.get('features', []):
            if not feature.get('user_stories'):
                self.errors.append(f"Feature {feature.get('id', 'unknown')} has no user stories")
        
        # Rule: User stories should follow "As a ... I want ... so that" format
        for feature in prd_data.get('features', []):
            for story in feature.get('user_stories', []):
                desc = story.get('description', '')
                if not self._is_valid_user_story_format(desc):
                    self.warnings.append(f"Story {story.get('id')} doesn't follow standard format: {desc[:50]}...")
        
        # Rule: Technical requirements should be specific and measurable
        tech_reqs = prd_data.get('technical_requirements', {})
        for category, reqs in tech_reqs.items():
            if not reqs:
                self.warnings.append(f"Technical requirements for {category} are empty")
    
    def _validate_consistency(self, data: Dict[str, Any]):
        """Check internal consistency."""
        if 'data' not in data:
            return
        
        prd_data = data['data']
        
        # Check for duplicate IDs
        feature_ids = [f.get('id') for f in prd_data.get('features', [])]
        story_ids = []
        for f in prd_data.get('features', []):
            story_ids.extend([s.get('id') for s in f.get('user_stories', [])])
        
        # Feature ID duplicates
        if len(feature_ids) != len(set(feature_ids)):
            duplicates = [id for id in feature_ids if feature_ids.count(id) > 1]
            self.errors.append(f"Duplicate feature IDs found: {duplicates}")
        
        # Story ID duplicates
        if len(story_ids) != len(set(story_ids)):
            duplicates = [id for id in story_ids if story_ids.count(id) > 1]
            self.errors.append(f"Duplicate story IDs found: {duplicates}")
        
        # ID format validation
        for fid in feature_ids:
            if fid and not fid.startswith('FR-'):
                self.errors.append(f"Feature ID {fid} doesn't follow FR-### format")
        
        for sid in story_ids:
            if sid and not sid.startswith('ST-'):
                self.errors.append(f"Story ID {sid} doesn't follow ST-### format")
    
    def _is_valid_user_story_format(self, description: str) -> bool:
        """Check if user story follows standard format."""
        desc_lower = description.lower()
        return (
            'as a' in desc_lower and
            'i want' in desc_lower and
            'so that' in desc_lower
        )
    
    def _apply_fixes(self, data: Dict[str, Any], file_path: str):
        """Apply automatic fixes where possible."""
        # This would implement auto-fixes like:
        # - Standardizing ID formats
        # - Adding missing required fields with defaults
        # - Fixing common user story format issues
        pass
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate validation report."""
        return {
            "valid": len(self.errors) == 0,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
            "fixes_applied": self.fixes_applied
        }


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate PRD JSON files")
    parser.add_argument("file", help="Path to PRD JSON file")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues where possible")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    linter = PRDLinter()
    is_valid, report = linter.lint_file(args.file, args.fix)
    
    # Print results
    if is_valid:
        print(f"✅ PRD validation passed: {args.file}")
    else:
        print(f"❌ PRD validation failed: {args.file}")
    
    if args.verbose or not is_valid:
        print(f"\nValidation Report:")
        print(f"- Errors: {report['error_count']}")
        print(f"- Warnings: {report['warning_count']}")
        
        for error in report['errors']:
            print(f"  ERROR: {error}")
        
        for warning in report['warnings']:
            print(f"  WARNING: {warning}")
        
        if report['fixes_applied']:
            print(f"\nFixes Applied:")
            for fix in report['fixes_applied']:
                print(f"  - {fix}")
    
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()