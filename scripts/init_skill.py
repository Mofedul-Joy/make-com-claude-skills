#!/usr/bin/env python3
"""
Skill initialization script.
Creates a new skill directory with SKILL.md template.
"""

import sys
import re
from pathlib import Path
from typing import Optional


SKILL_MD_TEMPLATE = """---
name: {name}
description: {description}
---

# {title}

## Overview

{description}

## When to Use This Skill

[Describe when Claude should use this skill]

## Key Concepts

[List and explain key concepts]

## Best Practices

[List best practices and guidelines]

## Common Patterns

[Provide common usage patterns and examples]

## Examples

[Include practical examples]

## References

[Link to reference materials if applicable]
"""


class SkillInitializer:
    """Initialize a new Claude Skill."""
    
    VALID_NAME_PATTERN = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
    MAX_NAME_LENGTH = 64
    MAX_DESCRIPTION_LENGTH = 1024
    
    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        
    def validate_name(self, name: str) -> Optional[str]:
        """Validate skill name. Returns error message if invalid."""
        if not name:
            return "Skill name cannot be empty"
        if len(name) > self.MAX_NAME_LENGTH:
            return f"Skill name too long (max {self.MAX_NAME_LENGTH} chars)"
        if not self.VALID_NAME_PATTERN.match(name):
            return "Skill name must be kebab-case (lowercase, hyphens only)"
        return None
    
    def validate_description(self, description: str) -> Optional[str]:
        """Validate description. Returns error message if invalid."""
        if not description:
            return "Description cannot be empty"
        if len(description) > self.MAX_DESCRIPTION_LENGTH:
            return f"Description too long (max {self.MAX_DESCRIPTION_LENGTH} chars)"
        return None
    
    def create_skill(self, name: str, description: str, create_references: bool = False) -> bool:
        """Create a new skill directory and SKILL.md file."""
        # Validate input
        name_error = self.validate_name(name)
        if name_error:
            print(f"❌ Invalid name: {name_error}")
            return False
            
        desc_error = self.validate_description(description)
        if desc_error:
            print(f"❌ Invalid description: {desc_error}")
            return False
        
        # Create skill directory
        skill_path = self.skills_dir / name
        if skill_path.exists():
            print(f"❌ Skill already exists: {skill_path}")
            return False
        
        try:
            skill_path.mkdir(parents=True)
            print(f"✅ Created skill directory: {skill_path}")
            
            # Create SKILL.md
            title = name.replace('-', ' ').title()
            skill_md_content = SKILL_MD_TEMPLATE.format(
                name=name,
                description=description,
                title=title
            )
            
            skill_md_path = skill_path / "SKILL.md"
            skill_md_path.write_text(skill_md_content, encoding='utf-8')
            print(f"✅ Created SKILL.md")
            
            # Create references directory if requested
            if create_references:
                references_path = skill_path / "references"
                references_path.mkdir()
                print(f"✅ Created references/ directory")
            
            print(f"\n🎉 Skill '{name}' initialized successfully!")
            print(f"\nNext steps:")
            print(f"  1. Edit {skill_md_path}")
            print(f"  2. Add content and examples")
            if create_references:
                print(f"  3. Add reference files to references/")
            print(f"  4. Validate with: python scripts/quick_validate.py {skill_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating skill: {e}")
            return False


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python init_skill.py <skill-name> <description> [--references]")
        print("\nExample:")
        print('  python init_skill.py make-scenario-builder "Core skill for building Make.com scenarios"')
        print('  python init_skill.py my-skill "Description" --references')
        sys.exit(1)
    
    name = sys.argv[1]
    description = sys.argv[2]
    create_references = '--references' in sys.argv
    
    # Determine skills directory
    script_dir = Path(__file__).parent
    workspace_dir = script_dir.parent
    skills_dir = workspace_dir / "skills"
    
    # Ensure skills directory exists
    skills_dir.mkdir(exist_ok=True)
    
    # Initialize skill
    initializer = SkillInitializer(skills_dir)
    success = initializer.create_skill(name, description, create_references)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
