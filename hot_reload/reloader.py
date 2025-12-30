import sys
from utils.colors import paint, YELLOW

class ModuleReloader:
    def __init__(self, tracker):
        self.tracker = tracker
        self.base_dir = self.tracker.base_dir

    def _get_module_name(self, file_path):
        try:
            rel_path = file_path.relative_to(self.base_dir)
            parts = list(rel_path.with_suffix("").parts)
            if parts and parts[-1] == "__init__":
                parts.pop()
            return ".".join(parts)
        except Exception:
            return None

    def _get_all_dependents_iterative(self, initial_dirty_files, all_project_files):
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

    def reload_affected_modules(self, dirty_paths):
        if not dirty_paths:
            return []

        all_project_files = self.tracker.get_local_dependencies()
        to_evict_paths = self._get_all_dependents_iterative(dirty_paths, all_project_files)
        evicted_names = []

        # Sort by depth to ensure children are evicted before parents
        sorted_eviction = sorted(list(to_evict_paths), key=lambda x: len(x.parts), reverse=True)

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