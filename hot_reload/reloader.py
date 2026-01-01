"""
Kern Module Reloader - Surgical module eviction from sys.modules.

This module provides the ModuleReloader class which handles the "muscle"
layer of Kern's architecture. It identifies and evicts affected modules
from Python's module cache to force clean re-imports.
"""

import sys
from pathlib import Path
from typing import Set, List, Optional

from utils.colors import paint, YELLOW


class ModuleReloader:
    """
    Handles surgical eviction of modules from sys.modules.
    
    When a file changes, this class identifies all modules that depend on
    the changed file and removes them from sys.modules. This forces Python
    to perform a fresh import from disk on the next import statement.
    
    Attributes:
        tracker: The DependencyTracker instance used to resolve dependencies.
        base_dir: The base directory of the project being monitored.
    """
    
    def __init__(self, tracker) -> None:
        """
        Initialize the ModuleReloader with a DependencyTracker.
        
        Args:
            tracker: A DependencyTracker instance for resolving dependencies.
        """
        self.tracker = tracker
        self.base_dir: Path = self.tracker.base_dir

    def _get_module_name(self, file_path: Path) -> Optional[str]:
        """
        Convert a file path to its corresponding Python module name.
        
        Args:
            file_path: Absolute path to a Python file.
            
        Returns:
            The dotted module name (e.g., "package.module"), or None if
            the path cannot be converted.
        """
        try:
            rel_path = file_path.relative_to(self.base_dir)
            parts = list(rel_path.with_suffix("").parts)
            if parts and parts[-1] == "__init__":
                parts.pop()
            return ".".join(parts)
        except Exception:
            return None

    def _get_all_dependents_iterative(
        self,
        initial_dirty_files: Set[Path],
        all_project_files: Set[Path]
    ) -> Set[Path]:
        """
        Find all files that depend on the dirty files (iteratively).
        
        Uses a stack-based approach to traverse the dependency graph and
        identify all modules that need to be evicted.
        
        Args:
            initial_dirty_files: Set of file paths that have changed.
            all_project_files: Set of all Python files in the project.
            
        Returns:
            Set of all file paths that need to be evicted, including the
            initial dirty files and all their dependents.
        """
        to_evict = set(initial_dirty_files)
        stack = list(initial_dirty_files)

        while stack:
            current_file = stack.pop()
            for candidate_file in all_project_files:
                if candidate_file in to_evict:
                    continue
                
                # Check parents using the tracker logic
                tracker_temp = self.tracker.__class__(candidate_file)
                try:
                    if current_file in tracker_temp.get_local_dependencies():
                        to_evict.add(candidate_file)
                        stack.append(candidate_file)
                except Exception:
                    continue
        return to_evict

    def reload_affected_modules(self, dirty_paths: List[Path]) -> List[str]:
        """
        Evict all modules affected by the given dirty file paths.
        
        This is the main entry point for the reloader. It identifies all
        dependent modules and removes them from sys.modules in the correct
        order (children before parents).
        
        Args:
            dirty_paths: List of file paths that have been modified.
            
        Returns:
            List of module names that were evicted from sys.modules.
        """
        if not dirty_paths:
            return []

        all_project_files = self.tracker.get_local_dependencies()
        to_evict_paths = self._get_all_dependents_iterative(
            set(dirty_paths),
            all_project_files
        )
        evicted_names: List[str] = []

        # Sort by depth to ensure children are evicted before parents
        sorted_eviction = sorted(
            list(to_evict_paths),
            key=lambda x: len(x.parts),
            reverse=True
        )

        for path in sorted_eviction:
            module_name = self._get_module_name(path)
            if module_name and module_name in sys.modules:
                print(paint(f"[Reloader] Evicting: {module_name}", YELLOW))
                del sys.modules[module_name]
                evicted_names.append(module_name)
            
            # Catch the __main__ entry point stem
            if path.resolve() == self.tracker.entry_point.resolve():
                entry_name = self.tracker.entry_point.stem
                if entry_name in sys.modules:
                    del sys.modules[entry_name]
                    evicted_names.append(entry_name)

        return list(set(evicted_names))