#!/usr/bin/env python3
"""
Quick validation script for Claude Skills.
Validates SKILL.md frontmatter and structure without heavy dependencies.
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class SkillValidator:
    """Validates Claude Skills structure and frontmatter."""
    
    # Validation constraints
    MAX_NAME_LENGTH = 64
    MAX_DESCRIPTION_LENGTH = 1024
    VALID_NAME_PATTERN = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
    
    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def validate(self) -> bool:
        """Run all validations. Returns True if valid."""
        if not self.skill_path.exists():
            self.errors.append(f"Skill directory not found: {self.skill_path}")
            return False
            
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            self.errors.append(f"SKILL.md not found in {self.skill_path}")
            return False
            
        frontmatter = self._extract_frontmatter(skill_md)
        if frontmatter is None:
            self.errors.append("Invalid YAML frontmatter in SKILL.md")
            return False
            
        self._validate_frontmatter(frontmatter)
        self._validate_structure()
        
        return len(self.errors) == 0
    
    def _extract_frontmatter(self, skill_md: Path) -> Optional[Dict[str, str]]:
        """Extract YAML frontmatter from SKILL.md."""
        content = skill_md.read_text(encoding='utf-8')
        
        # Match YAML frontmatter between --- delimiters
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return None
            
        yaml_content = match.group(1)
        frontmatter = {}
        
        # Simple YAML parsing (key: value)
        for line in yaml_content.split('\n'):
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip().strip('"\'')
                
        return frontmatter
    
    def _validate_frontmatter(self, frontmatter: Dict[str, str]):
        """Validate frontmatter fields."""
        # Check required fields
        if 'name' not in frontmatter:
            self.errors.append("Missing required field: name")
        else:
            name = frontmatter['name']
            # Check name length
            if len(name) > self.MAX_NAME_LENGTH:
                self.errors.append(f"Name too long: {len(name)} chars (max {self.MAX_NAME_LENGTH})")
            # Check name format (kebab-case)
            if not self.VALID_NAME_PATTERN.match(name):
                self.errors.append(f"Invalid name format: '{name}' (use kebab-case)")
                
        if 'description' not in frontmatter:
            self.errors.append("Missing required field: description")
        else:
            description = frontmatter['description']
            if len(description) > self.MAX_DESCRIPTION_LENGTH:
                self.errors.append(
                    f"Description too long: {len(description)} chars (max {self.MAX_DESCRIPTION_LENGTH})"
                )
    
    def _validate_structure(self):
        """Validate skill directory structure."""
        skill_md = self.skill_path / "SKILL.md"
        
        # Check SKILL.md is not empty
        content = skill_md.read_text(encoding='utf-8')
        # Remove frontmatter
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
        if not content.strip():
            self.warnings.append("SKILL.md has no content after frontmatter")
            
        # Check for optional directories
        optional_dirs = ['references', 'scripts', 'assets']
        for dir_name in optional_dirs:
            dir_path = self.skill_path / dir_name
            if dir_path.exists() and not dir_path.is_dir():
                self.errors.append(f"{dir_name} exists but is not a directory")
    
    def print_results(self):
        """Print validation results."""
        skill_name = self.skill_path.name
        
        if self.errors:
            print(f"❌ {skill_name}: FAILED")
            for error in self.errors:
                print(f"   ERROR: {error}")
        else:
            print(f"✅ {skill_name}: VALID")
            
        if self.warnings:
            for warning in self.warnings:
                print(f"   WARNING: {warning}")


def validate_skill(skill_path: Path) -> bool:
    """Validate a single skill."""
    validator = SkillValidator(skill_path)
    is_valid = validator.validate()
    validator.print_results()
    return is_valid


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python quick_validate.py <skill_directory> [<skill_directory> ...]")
        print("\nExample:")
        print("  python quick_validate.py skills/make-scenario-builder")
        print("  python quick_validate.py skills/*")
        sys.exit(1)
    
    skill_paths = [Path(arg) for arg in sys.argv[1:]]
    
    # Expand wildcards
    expanded_paths = []
    for path in skill_paths:
        if '*' in str(path):
            # Simple wildcard expansion for skills/*
            parent = path.parent
            pattern = path.name
            if parent.exists():
                expanded_paths.extend(parent.glob(pattern))
        else:
            expanded_paths.append(path)
    
    if not expanded_paths:
        print("No skills found to validate")
        sys.exit(1)
    
    print("=" * 60)
    print("SKILL VALIDATION REPORT")
    print("=" * 60)
    print()
    
    results = []
    for skill_path in expanded_paths:
        if skill_path.is_dir():
            is_valid = validate_skill(skill_path)
            results.append((skill_path.name, is_valid))
            print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for _, valid in results if valid)
    failed = total - passed
    
    print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
    
    if failed > 0:
        print("\nFailed skills:")
        for name, valid in results:
            if not valid:
                print(f"  - {name}")
        sys.exit(1)
    else:
        print("\n✅ All skills are valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
