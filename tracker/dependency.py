"""
Kern Dependency Tracker - Static analysis of Python imports.

This module provides the DependencyTracker class which uses Python's AST
(Abstract Syntax Tree) to statically analyze import statements and build
a dependency graph of the project without executing any code.
"""

import os
import ast
from pathlib import Path
from typing import Set, Optional


class DependencyTracker:
    """
    Tracks project dependencies using static AST analysis.
    
    This class parses Python files and extracts import statements to build
    a complete dependency graph of the project. It uses static analysis
    (AST parsing) rather than dynamic imports, making it safe to use even
    when files contain syntax errors.
    
    Attributes:
        entry_point: Absolute path to the main entry point file.
        base_dir: The parent directory of the entry point (project root).
        seen_modules: Set of already-scanned file paths to prevent cycles.
    """
    
    def __init__(self, entry_point: str | Path) -> None:
        """
        Initialize the DependencyTracker with an entry point file.
        
        Args:
            entry_point: Path to the main Python file to analyze.
        """
        self.entry_point: Path = Path(entry_point).resolve()
        self.base_dir: Path = self.entry_point.parent
        self.seen_modules: Set[Path] = set()

    def get_local_dependencies(self) -> Set[Path]:
        """
        Get all local Python files that the entry point depends on.
        
        This method recursively scans the entry point and all its imports
        to build a complete set of local dependencies.
        
        Returns:
            Set of absolute Path objects representing all project files.
        """
        self.seen_modules = set()
        dependencies: Set[Path] = {self.entry_point}
        # We wrap the scan to ensure one broken file doesn't stop the engine
        try:
            self._scan(self.entry_point, dependencies)
        except Exception:
            pass  # Keep existing dependencies if current scan fails
        return dependencies

    def _resolve_import_to_path(
        self,
        base_name: str,
        item_name: Optional[str] = None,
        level: int = 0,
        current_file: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Resolve an import statement to an absolute file path.
        
        Args:
            base_name: The module name from the import (e.g., "package.module").
            item_name: The specific item being imported (e.g., "Class" in
                      "from module import Class").
            level: The relative import level (0 for absolute, 1+ for relative).
            current_file: The file containing the import statement.
            
        Returns:
            Absolute Path to the resolved file, or None if not found locally.
        """
        anchor_dir = self.base_dir
        if level > 0 and current_file:
            anchor_dir = current_file.parent
            for _ in range(level - 1):
                anchor_dir = anchor_dir.parent

        base_rel_path = base_name.replace(".", os.sep) if base_name else ""
        
        search_paths = []
        if item_name:
            search_paths.append(anchor_dir / base_rel_path / f"{item_name}.py")
        search_paths.append(anchor_dir / f"{base_rel_path}.py")
        search_paths.append(anchor_dir / base_rel_path / "__init__.py")

        for p in search_paths:
            if p and p.exists():
                return p.resolve()
        return None

    def _scan(self, file_path: Path, dependencies: Set[Path]) -> None:
        """
        Recursively scan a file for import statements.
        
        Args:
            file_path: The file to scan.
            dependencies: Set to add discovered dependencies to (modified in place).
        """
        if file_path in self.seen_modules:
            return
        self.seen_modules.add(file_path)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
                # If this fails (SyntaxError), we stop scanning this branch
                # but keep the file itself in dependencies.
                tree = ast.parse(source)
        except Exception:
            return

        for node in ast.walk(tree):
            found_paths = []
            if isinstance(node, ast.Import):
                for alias in node.names:
                    path = self._resolve_import_to_path(alias.name)
                    if path:
                        found_paths.append(path)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        path = self._resolve_import_to_path(
                            node.module, alias.name, node.level, file_path
                        )
                        if path:
                            found_paths.append(path)
                    parent_path = self._resolve_import_to_path(
                        node.module, None, node.level, file_path
                    )
                    if parent_path:
                        found_paths.append(parent_path)
                elif node.level > 0:
                    for alias in node.names:
                        path = self._resolve_import_to_path(
                            "", alias.name, node.level, file_path
                        )
                        if path:
                            found_paths.append(path)

            for p in found_paths:
                if p not in dependencies:
                    dependencies.add(p)
                    self._scan(p, dependencies)