#!/usr/bin/env python3
"""
Skill packaging script.
Packages Claude Skills as .skill ZIP files for distribution.
"""

import sys
import zipfile
from pathlib import Path
from typing import List, Optional


class SkillPackager:
    """Package Claude Skills as .skill files."""
    
    # Files/directories to exclude from package
    EXCLUDE_PATTERNS = [
        '.DS_Store',
        '__pycache__',
        '*.pyc',
        '.git',
        '.gitignore',
        'node_modules',
        '.env',
        'venv',
        '.venv'
    ]
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        
    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded from package."""
        name = path.name
        
        for pattern in self.EXCLUDE_PATTERNS:
            if pattern.startswith('*'):
                # Simple suffix matching
                if name.endswith(pattern[1:]):
                    return True
            elif pattern.startswith('.'):
                # Exact match for hidden files/dirs
                if name == pattern:
                    return True
            else:
                # Exact match
                if name == pattern:
                    return True
        return False
    
    def get_files_to_package(self, skill_path: Path) -> List[Path]:
        """Get list of files to include in package."""
        files = []
        
        for item in skill_path.rglob('*'):
            if item.is_file() and not self.should_exclude(item):
                # Also check if any parent directory should be excluded
                exclude = False
                for parent in item.parents:
                    if parent == skill_path:
                        break
                    if self.should_exclude(parent):
                        exclude = True
                        break
                
                if not exclude:
                    files.append(item)
        
        return files
    
    def package_skill(self, skill_path: Path, bundle: bool = False) -> Optional[Path]:
        """Package a skill as a .skill file."""
        if not skill_path.is_dir():
            print(f"❌ Not a directory: {skill_path}")
            return None
        
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            print(f"❌ SKILL.md not found in {skill_path}")
            return None
        
        skill_name = skill_path.name
        output_file = self.output_dir / f"{skill_name}.skill"
        
        try:
            # Get files to package
            files = self.get_files_to_package(skill_path)
            
            if not files:
                print(f"❌ No files found to package in {skill_path}")
                return None
            
            # Create ZIP archive
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file_path in files:
                    arcname = file_path.relative_to(skill_path)
                    zf.write(file_path, arcname)
            
            file_size = output_file.stat().st_size
            size_kb = file_size / 1024
            
            print(f"✅ Packaged {skill_name}: {output_file} ({size_kb:.1f} KB, {len(files)} files)")
            return output_file
            
        except Exception as e:
            print(f"❌ Error packaging {skill_name}: {e}")
            return None
    
    def create_bundle(self, package_files: List[Path]) -> Optional[Path]:
        """Create a bundle of all packaged skills."""
        bundle_file = self.output_dir / "make-skills-bundle.skill"
        
        try:
            with zipfile.ZipFile(bundle_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                for pkg_file in package_files:
                    zf.write(pkg_file, pkg_file.name)
            
            file_size = bundle_file.stat().st_size
            size_kb = file_size / 1024
            
            print(f"\n✅ Created bundle: {bundle_file} ({size_kb:.1f} KB)")
            return bundle_file
            
        except Exception as e:
            print(f"❌ Error creating bundle: {e}")
            return None


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python package_skill.py <skill_directory> [<skill_directory> ...] [--bundle]")
        print("\nExamples:")
        print("  python package_skill.py skills/make-scenario-builder")
        print("  python package_skill.py skills/* --bundle")
        print("\nOptions:")
        print("  --bundle    Create a bundle of all packaged skills")
        sys.exit(1)
    
    args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    create_bundle = '--bundle' in sys.argv
    
    skill_paths = [Path(arg) for arg in args]
    
    # Expand wildcards
    expanded_paths = []
    for path in skill_paths:
        if '*' in str(path):
            parent = path.parent
            pattern = path.name
            if parent.exists():
                expanded_paths.extend([p for p in parent.glob(pattern) if p.is_dir()])
        else:
            expanded_paths.append(path)
    
    if not expanded_paths:
        print("No skills found to package")
        sys.exit(1)
    
    # Determine output directory
    script_dir = Path(__file__).parent
    workspace_dir = script_dir.parent
    output_dir = workspace_dir / "dist"
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("PACKAGING SKILLS")
    print("=" * 60)
    print()
    
    packager = SkillPackager(output_dir)
    package_files = []
    
    for skill_path in expanded_paths:
        package_file = packager.package_skill(skill_path)
        if package_file:
            package_files.append(package_file)
    
    if create_bundle and len(package_files) > 1:
        packager.create_bundle(package_files)
    
    print()
    print("=" * 60)
    print(f"COMPLETED: {len(package_files)} skills packaged")
    print("=" * 60)
    print(f"\nPackages saved to: {output_dir}")
    
    sys.exit(0 if package_files else 1)


if __name__ == "__main__":
    main()
