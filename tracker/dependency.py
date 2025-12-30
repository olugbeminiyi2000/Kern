import os
import ast
from pathlib import Path

class DependencyTracker:
    def __init__(self, entry_point):
        self.entry_point = Path(entry_point).resolve()
        self.base_dir = self.entry_point.parent
        self.seen_modules = set()

    def get_local_dependencies(self):
        self.seen_modules = set() 
        dependencies = {self.entry_point}
        # We wrap the scan to ensure one broken file doesn't stop the engine
        try:
            self._scan(self.entry_point, dependencies)
        except Exception:
            pass # Keep existing dependencies if current scan fails
        return dependencies

    def _resolve_import_to_path(self, base_name, item_name=None, level=0, current_file=None):
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

    def _scan(self, file_path, dependencies):
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
                    if path: found_paths.append(path)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        path = self._resolve_import_to_path(node.module, alias.name, node.level, file_path)
                        if path: found_paths.append(path)
                    parent_path = self._resolve_import_to_path(node.module, None, node.level, file_path)
                    if parent_path: found_paths.append(parent_path)
                elif node.level > 0:
                    for alias in node.names:
                        path = self._resolve_import_to_path("", alias.name, node.level, file_path)
                        if path: found_paths.append(path)

            for p in found_paths:
                if p not in dependencies:
                    dependencies.add(p)
                    self._scan(p, dependencies)