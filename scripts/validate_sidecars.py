#!/usr/bin/env python3
"""
Validate that all Pipes, Services, and Triggers have corresponding sidecar files.
"""
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple


class Component(NamedTuple):
    """Represents a component that needs a sidecar."""
    name: str
    type: str  # 'pipe', 'service', 'trigger'
    class_name: str
    file_path: str
    expected_sidecar: str


def find_components(root_dir: Path) -> list[Component]:
    """Find all Pipe, Service, and Trigger components in the codebase."""
    components = []
    
    # Search in src and packages directories
    for search_dir in ['src', 'packages']:
        search_path = root_dir / search_dir
        if not search_path.exists():
            continue
            
        for py_file in search_path.rglob('*.py'):
            # Skip test files
            if 'test' in py_file.name or '__pycache__' in str(py_file):
                continue
                
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                    
                # Find Pipe classes
                pipe_matches = re.findall(r'class (\w+Pipe)\(Pipe\[', content)
                for match in pipe_matches:
                    if 'Config' not in match and 'Result' not in match:
                        sidecar_name = to_snake_case(match) + '.sidecar.yml'
                        components.append(Component(
                            name=match,
                            type='pipe',
                            class_name=match,
                            file_path=str(py_file.relative_to(root_dir)),
                            expected_sidecar=f'docs/_internal/man_structured/pipes/{sidecar_name}'
                        ))
                
                # Find Service classes
                service_matches = re.findall(r'class (\w+Service)\(.*Service\)', content)
                for match in service_matches:
                    if 'Config' not in match and 'Result' not in match and match != 'TicketSystemService':
                        sidecar_name = to_snake_case(match) + '.sidecar.yml'
                        components.append(Component(
                            name=match,
                            type='service',
                            class_name=match,
                            file_path=str(py_file.relative_to(root_dir)),
                            expected_sidecar=f'docs/_internal/man_structured/services/{sidecar_name}'
                        ))
                
                # Find Trigger classes
                trigger_matches = re.findall(r'class (\w+Trigger)\(Trigger\[', content)
                for match in trigger_matches:
                    if 'Config' not in match and 'Result' not in match:
                        sidecar_name = to_snake_case(match) + '.sidecar.yml'
                        components.append(Component(
                            name=match,
                            type='trigger',
                            class_name=match,
                            file_path=str(py_file.relative_to(root_dir)),
                            expected_sidecar=f'docs/_internal/man_structured/triggers/{sidecar_name}'
                        ))
            except Exception as e:
                print(f"Warning: Could not read {py_file}: {e}", file=sys.stderr)
    
    return components


def to_snake_case(name: str) -> str:
    """Convert CamelCase to snake_case."""
    # Insert underscore before uppercase letters
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    # Insert underscore before uppercase letters that follow lowercase letters
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def validate_sidecars(root_dir: Path) -> tuple[list[Component], list[Component]]:
    """
    Validate that all components have sidecars.
    
    Returns:
        Tuple of (components_with_sidecars, components_without_sidecars)
    """
    components = find_components(root_dir)
    
    with_sidecars = []
    without_sidecars = []
    
    for component in components:
        sidecar_path = root_dir / component.expected_sidecar
        if sidecar_path.exists():
            with_sidecars.append(component)
        else:
            without_sidecars.append(component)
    
    return with_sidecars, without_sidecars


def main() -> int:
    """Main entry point."""
    root_dir = Path(__file__).parent.parent
    
    print("🔍 Validating sidecar files...")
    print()
    
    with_sidecars, without_sidecars = validate_sidecars(root_dir)
    
    # Print summary
    total = len(with_sidecars) + len(without_sidecars)
    print(f"Found {total} components:")
    print(f"  ✅ {len(with_sidecars)} with sidecars")
    print(f"  ❌ {len(without_sidecars)} without sidecars")
    print()
    
    # List components by type
    if with_sidecars:
        print("Components with sidecars:")
        by_type = {}
        for component in with_sidecars:
            by_type.setdefault(component.type, []).append(component)
        
        for comp_type in sorted(by_type.keys()):
            print(f"\n  {comp_type.upper()}S:")
            for component in sorted(by_type[comp_type], key=lambda c: c.name):
                print(f"    ✅ {component.name}")
    
    # List missing sidecars
    if without_sidecars:
        print("\n⚠️  Missing sidecars:")
        by_type = {}
        for component in without_sidecars:
            by_type.setdefault(component.type, []).append(component)
        
        for comp_type in sorted(by_type.keys()):
            print(f"\n  {comp_type.upper()}S:")
            for component in sorted(by_type[comp_type], key=lambda c: c.name):
                print(f"    ❌ {component.name}")
                print(f"       Expected: {component.expected_sidecar}")
                print(f"       Source: {component.file_path}")
    
    print()
    
    if without_sidecars:
        print("❌ Validation failed: Some components are missing sidecars.")
        print(f"   Please create sidecar files for the {len(without_sidecars)} component(s) listed above.")
        return 1
    else:
        print("✅ Validation passed: All components have sidecars!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
