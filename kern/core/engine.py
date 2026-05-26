"""
Kern Engine - The core hot-reloading engine.

Contains the main Engine class that orchestrates file watching,
module reloading, and user code execution.
"""

import importlib
import sys
import traceback
import time
from pathlib import Path
from typing import Optional, Union
from types import ModuleType

from kern.utils.colors import paint, RED, GREEN, YELLOW, BLUE
from kern.tracker.dependency import DependencyTracker
from kern.tracker.watcher import FileWatcher
from kern.hot_reload.reloader import ModuleReloader


class Engine:
    """
    The main hot-reloading engine for Kern.

    Coordinates between DependencyTracker, FileWatcher, and ModuleReloader
    to provide seamless hot-reloading of Python scripts.

    Attributes:
        tracker: DependencyTracker instance for mapping project dependencies.
        reloader: ModuleReloader instance for evicting stale modules.
        watcher: FileWatcher instance for detecting file changes.
        entry_name: The stem name of the entry point file.
        user_module: The currently loaded user module, or None if not loaded.
        log_file: Path to the error log file.
        DEBOUNCE_SECONDS: Time to wait after a file change before reloading.
    """

    def __init__(self, entry_file: Union[str, Path]) -> None:
        self.tracker: DependencyTracker = DependencyTracker(entry_file)
        self.reloader: ModuleReloader = ModuleReloader(self.tracker)
        self.watcher: FileWatcher = FileWatcher(self.tracker)
        self.entry_name: str = self.tracker.entry_point.stem
        self.user_module: Optional[ModuleType] = None
        self.log_file: str = "engine_error.log"
        self.DEBOUNCE_SECONDS: float = 0.5

    def _log_error(self, error_traceback: str) -> None:
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(error_traceback)
        print(paint(f"\n[!] EXECUTION/RECONSTRUCTION FAILED", RED))
        print(paint(f"Detailed traceback saved to: {self.log_file}", YELLOW))

    def _safe_import(self) -> bool:
        """
        Attempt to import or reload the user's module.

        Returns:
            True if the import was successful, False otherwise.
        """
        try:
            script_dir = str(self.tracker.base_dir)
            if script_dir not in sys.path:
                sys.path.insert(0, script_dir)

            if self.entry_name in sys.modules:
                self.user_module = importlib.reload(sys.modules[self.entry_name])
            else:
                self.user_module = importlib.import_module(self.entry_name)

            print(paint(f"[*] {self.entry_name} reconstructed successfully.", GREEN))
            return True
        except Exception:
            self._log_error(traceback.format_exc())
            self.user_module = None
            return False

    def start(self) -> None:
        """
        Start the engine in non-blocking auto-reload mode.

        Enters an infinite monitoring loop until interrupted by Ctrl+C.
        """
        self.watcher.start()
        print(paint(f"\n--- Kern Engine Ignited ---", BLUE))
        print(paint(f"Monitoring: {self.entry_name}. Press Ctrl+C to stop.", BLUE))

        self._safe_import()
        self._execute_user_code()

        try:
            while True:
                if self.watcher.change_detected:
                    time_since_last_save = time.time() - self.watcher.last_change_time
                    if time_since_last_save >= self.DEBOUNCE_SECONDS:
                        dirty = self.watcher.get_and_clear_dirty()
                        self.reloader.reload_affected_modules(dirty)
                        print(paint(f"\n[v] Stable change detected. Attempting recovery...", YELLOW))
                        if self._safe_import():
                            self._execute_user_code()
                time.sleep(0.1)
        except KeyboardInterrupt:
            print(paint("\n[!] Engine stopped by user. Goodbye!", BLUE))
            sys.exit(0)

    def _execute_user_code(self) -> None:
        """Execute the user's run() function if it exists."""
        if self.user_module:
            try:
                if hasattr(self.user_module, "run"):
                    print(paint(f"--- Executing {self.entry_name}.run() ---", BLUE))
                    self.user_module.run()
                    print(paint("-" * 30, BLUE))
                else:
                    print(paint(f"\n[?] Warning: No 'run()' function found in {self.entry_name}.py", YELLOW))
            except Exception:
                self._log_error(traceback.format_exc())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(paint("Usage: kern run <script.py>", RED))
    else:
        engine = Engine(sys.argv[1])
        engine.start()
