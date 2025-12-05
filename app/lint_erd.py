#!/usr/bin/env python3
"""
ERD Validation Utility

Validates Entity Relationship Diagram JSON against Pydantic model and
database design best practices. Checks relationships, constraints, and naming.

Usage:
    python -m app.lint_erd docs/erd.json
    python -m app.lint_erd --generate-sql docs/erd.json
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
from pydantic import ValidationError

from app.models import ERDModel


class ERDLinter:
    """ERD validation and linting utility."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.suggestions = []
    
    def lint_file(self, file_path: str) -> Tuple[bool, Dict[str, Any]]:
        """Lint an ERD JSON file."""
        try:
            erd_data = self._load_json(file_path)
            return self.lint_data(erd_data)
        except Exception as e:
            self.errors.append(f"Failed to load file {file_path}: {e}")
            return False, self._generate_report()
    
    def lint_data(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Lint ERD data structure."""
        
        # 1. Pydantic validation
        pydantic_valid = self._validate_pydantic(data)
        
        # 2. Database design validation
        self._validate_database_design(data)
        
        # 3. Relationship validation
        self._validate_relationships(data)
        
        # 4. Naming convention validation
        self._validate_naming_conventions(data)
        
        # 5. Performance considerations
        self._check_performance_considerations(data)
        
        is_valid = pydantic_valid and len(self.errors) == 0
        return is_valid, self._generate_report()
    
    def generate_sql_schema(self, data: Dict[str, Any]) -> str:
        """Generate SQL schema from ERD data."""
        if 'data' not in data:
            return "-- No data found"
        
        erd_data = data['data']
        database_type = erd_data.get('database_type', 'postgres')
        
        sql_parts = []
        sql_parts.append(f"-- Generated schema for {erd_data.get('project_name', 'Unknown Project')}")
        sql_parts.append(f"-- Database type: {database_type}")
        sql_parts.append(f"-- Generated at: {erd_data.get('created_at', 'Unknown')}")
        sql_parts.append("")
        
        # Generate table creation statements
        for entity in erd_data.get('entities', []):
            sql_parts.append(self._generate_table_sql(entity, database_type))
            sql_parts.append("")
        
        # Generate indexes
        for entity in erd_data.get('entities', []):
            for index in entity.get('indexes', []):
                sql_parts.append(self._generate_index_sql(entity, index, database_type))
        
        # Generate foreign key constraints
        for relationship in erd_data.get('relationships', []):
            sql_parts.append(self._generate_foreign_key_sql(relationship, erd_data))
        
        return "\n".join(sql_parts)
    
    def _load_json(self, file_path: str) -> Dict[str, Any]:
        """Load and parse JSON file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return json.loads(path.read_text())
    
    def _validate_pydantic(self, data: Dict[str, Any]) -> bool:
        """Validate against Pydantic model."""
        try:
            ERDModel(**data)
            return True
        except ValidationError as e:
            for error in e.errors():
                location = " -> ".join(str(loc) for loc in error['loc'])
                self.errors.append(f"Validation error at {location}: {error['msg']}")
            return False
    
    def _validate_database_design(self, data: Dict[str, Any]):
        """Validate database design principles."""
        if 'data' not in data:
            return
        
        erd_data = data['data']
        entities = erd_data.get('entities', [])
        
        # Check for entities without primary keys
        for entity in entities:
            has_pk = any(attr.get('primary_key', False) for attr in entity.get('attributes', []))
            if not has_pk:
                self.errors.append(f"Entity {entity.get('name')} has no primary key")
        
        # Check for missing timestamps (common pattern)
        for entity in entities:
            attrs = [attr['name'] for attr in entity.get('attributes', [])]
            if 'created_at' not in attrs:
                self.warnings.append(f"Entity {entity.get('name')} missing created_at timestamp")
            if 'updated_at' not in attrs:
                self.warnings.append(f"Entity {entity.get('name')} missing updated_at timestamp")
        
        # Check for single-column entities (usually design smell)
        for entity in entities:
            if len(entity.get('attributes', [])) <= 2:  # PK + one other field
                self.warnings.append(f"Entity {entity.get('name')} has very few attributes - consider if it's needed")
    
    def _validate_relationships(self, data: Dict[str, Any]):
        """Validate entity relationships."""
        if 'data' not in data:
            return
        
        erd_data = data['data']
        entities = {e['id']: e for e in erd_data.get('entities', [])}
        relationships = erd_data.get('relationships', [])
        
        for rel in relationships:
            from_id = rel.get('from_entity')
            to_id = rel.get('to_entity')
            
            # Check entity references exist
            if from_id not in entities:
                self.errors.append(f"Relationship {rel.get('id')} references non-existent entity {from_id}")
            if to_id not in entities:
                self.errors.append(f"Relationship {rel.get('id')} references non-existent entity {to_id}")
            
            # Check foreign key exists in from_entity
            if from_id in entities:
                from_entity = entities[from_id]
                fk_field = rel.get('foreign_key')
                attr_names = [attr['name'] for attr in from_entity.get('attributes', [])]
                if fk_field not in attr_names:
                    self.errors.append(f"Foreign key {fk_field} not found in entity {from_entity.get('name')}")
        
        # Check for orphaned entities (no relationships)
        entity_ids_in_rels = set()
        for rel in relationships:
            entity_ids_in_rels.add(rel.get('from_entity'))
            entity_ids_in_rels.add(rel.get('to_entity'))
        
        for entity_id, entity in entities.items():
            if entity_id not in entity_ids_in_rels and len(entities) > 1:
                self.warnings.append(f"Entity {entity.get('name')} has no relationships - is this intentional?")
    
    def _validate_naming_conventions(self, data: Dict[str, Any]):
        """Validate naming conventions."""
        if 'data' not in data:
            return
        
        erd_data = data['data']
        
        # Entity naming
        for entity in erd_data.get('entities', []):
            name = entity.get('name', '')
            table_name = entity.get('table_name', '')
            
            # Entity names should be PascalCase
            if not name[0].isupper() or '_' in name:
                self.warnings.append(f"Entity name '{name}' should be PascalCase (e.g., 'UserProfile')")
            
            # Table names should be snake_case and plural
            if table_name.lower() != table_name or ' ' in table_name:
                self.warnings.append(f"Table name '{table_name}' should be lowercase snake_case")
            
            # Attribute naming
            for attr in entity.get('attributes', []):
                attr_name = attr.get('name', '')
                if attr_name.lower() != attr_name or ' ' in attr_name:
                    self.warnings.append(f"Attribute '{attr_name}' in {name} should be lowercase snake_case")
    
    def _check_performance_considerations(self, data: Dict[str, Any]):
        """Check for performance issues."""
        if 'data' not in data:
            return
        
        erd_data = data['data']
        
        # Check for missing indexes on foreign keys
        entities = {e['id']: e for e in erd_data.get('entities', [])}
        relationships = erd_data.get('relationships', [])
        
        for rel in relationships:
            from_id = rel.get('from_entity')
            fk_field = rel.get('foreign_key')
            
            if from_id in entities:
                entity = entities[from_id]
                indexed_columns = set()
                for index in entity.get('indexes', []):
                    indexed_columns.update(index.get('columns', []))
                
                if fk_field not in indexed_columns:
                    self.suggestions.append(f"Consider adding index on foreign key '{fk_field}' in {entity.get('name')} for better performance")
        
        # Check for very wide tables (normalization issue)
        for entity in erd_data.get('entities', []):
            attr_count = len(entity.get('attributes', []))
            if attr_count > 15:
                self.warnings.append(f"Entity {entity.get('name')} has {attr_count} attributes - consider normalization")
    
    def _generate_table_sql(self, entity: Dict[str, Any], db_type: str) -> str:
        """Generate CREATE TABLE SQL for entity."""
        table_name = entity.get('table_name', entity.get('name', '').lower())
        sql = [f"CREATE TABLE {table_name} ("]
        
        for attr in entity.get('attributes', []):
            col_def = self._generate_column_definition(attr, db_type)
            sql.append(f"    {col_def},")
        
        # Remove trailing comma
        if sql[-1].endswith(','):
            sql[-1] = sql[-1][:-1]
        
        sql.append(");")
        return "\n".join(sql)
    
    def _generate_column_definition(self, attr: Dict[str, Any], db_type: str) -> str:
        """Generate column definition SQL."""
        name = attr.get('name')
        data_type = attr.get('type', 'TEXT')
        
        # Map generic types to database-specific types
        type_mapping = {
            'postgres': {
                'UUID': 'UUID',
                'INTEGER': 'INTEGER',
                'STRING': 'VARCHAR(255)',
                'TEXT': 'TEXT',
                'BOOLEAN': 'BOOLEAN',
                'DATETIME': 'TIMESTAMP WITH TIME ZONE'
            }
        }
        
        mapped_type = type_mapping.get(db_type, {}).get(data_type, data_type)
        col_def = f"{name} {mapped_type}"
        
        if attr.get('primary_key'):
            col_def += " PRIMARY KEY"
        
        if not attr.get('nullable', True):
            col_def += " NOT NULL"
        
        if attr.get('unique'):
            col_def += " UNIQUE"
        
        if attr.get('default') is not None:
            col_def += f" DEFAULT {attr['default']}"
        
        return col_def
    
    def _generate_index_sql(self, entity: Dict[str, Any], index: Dict[str, Any], db_type: str) -> str:
        """Generate CREATE INDEX SQL."""
        table_name = entity.get('table_name')
        index_name = index.get('name')
        columns = ', '.join(index.get('columns', []))
        
        unique = "UNIQUE " if index.get('unique') else ""
        return f"CREATE {unique}INDEX {index_name} ON {table_name} ({columns});"
    
    def _generate_foreign_key_sql(self, relationship: Dict[str, Any], erd_data: Dict[str, Any]) -> str:
        """Generate foreign key constraint SQL."""
        entities = {e['id']: e for e in erd_data.get('entities', [])}
        
        from_entity = entities.get(relationship.get('from_entity'))
        to_entity = entities.get(relationship.get('to_entity'))
        
        if not from_entity or not to_entity:
            return "-- Missing entity for foreign key"
        
        from_table = from_entity.get('table_name')
        to_table = to_entity.get('table_name')
        fk_field = relationship.get('foreign_key')
        
        # Assume primary key of target table (usually 'id')
        pk_field = 'id'  # Could be made smarter by finding actual PK
        
        cascade = ""
        if relationship.get('cascade_delete'):
            cascade = " ON DELETE CASCADE"
        
        return f"ALTER TABLE {from_table} ADD FOREIGN KEY ({fk_field}) REFERENCES {to_table}({pk_field}){cascade};"
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate validation report."""
        return {
            "valid": len(self.errors) == 0,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "suggestion_count": len(self.suggestions),
            "errors": self.errors,
            "warnings": self.warnings,
            "suggestions": self.suggestions
        }


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate ERD JSON files")
    parser.add_argument("file", help="Path to ERD JSON file")
    parser.add_argument("--generate-sql", action="store_true", help="Generate SQL schema")
    parser.add_argument("--output", "-o", help="Output file for generated SQL")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    linter = ERDLinter()
    is_valid, report = linter.lint_file(args.file)
    
    # Print results
    if is_valid:
        print(f"✅ ERD validation passed: {args.file}")
    else:
        print(f"❌ ERD validation failed: {args.file}")
    
    if args.verbose or not is_valid:
        print(f"\nValidation Report:")
        print(f"- Errors: {report['error_count']}")
        print(f"- Warnings: {report['warning_count']}")
        print(f"- Suggestions: {report['suggestion_count']}")
        
        for error in report['errors']:
            print(f"  ERROR: {error}")
        
        for warning in report['warnings']:
            print(f"  WARNING: {warning}")
        
        for suggestion in report['suggestions']:
            print(f"  SUGGESTION: {suggestion}")
    
    # Generate SQL if requested
    if args.generate_sql:
        try:
            erd_data = json.loads(Path(args.file).read_text())
            sql_schema = linter.generate_sql_schema(erd_data)
            
            if args.output:
                Path(args.output).write_text(sql_schema)
                print(f"\n📄 SQL schema generated: {args.output}")
            else:
                print("\n--- Generated SQL Schema ---")
                print(sql_schema)
        except Exception as e:
            print(f"\n❌ Failed to generate SQL: {e}")
    
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()