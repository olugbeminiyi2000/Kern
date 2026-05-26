"""
Kern File Watcher - Background thread for monitoring file changes.

Runs as a daemon thread, continuously polling file modification times.
When a change is detected, it signals the main engine loop to trigger a reload.
"""

import os
import threading
import time
from pathlib import Path
from typing import Dict, Set, List


class FileWatcher(threading.Thread):
    """
    Background thread that monitors files for changes.

    Attributes:
        tracker: The DependencyTracker instance for getting files to monitor.
        dependencies: Set of file paths currently being monitored.
        last_mtimes: Dictionary mapping file paths to their last modification times.
        changed_files: Set of files that have changed since last check.
        change_detected: Flag indicating if any changes have been detected.
        last_change_time: Timestamp of the most recent change detection.
    """

    def __init__(self, tracker) -> None:
        super().__init__(daemon=True)
        self.tracker = tracker
        self.dependencies: Set[Path] = self.tracker.get_local_dependencies()
        self.last_mtimes: Dict[Path, float] = self._get_mtimes()
        self.changed_files: Set[Path] = set()
        self.change_detected: bool = False
        self.last_change_time: float = 0.0

    def _get_mtimes(self) -> Dict[Path, float]:
        mtimes: Dict[Path, float] = {}
        for p in self.dependencies:
            try:
                mtimes[p] = os.stat(p).st_mtime
            except FileNotFoundError:
                continue
        return mtimes

    def get_and_clear_dirty(self) -> List[Path]:
        """
        Get the list of changed files and reset the change detection state.

        Returns:
            List of file paths that have been modified since the last call.
        """
        dirty = list(self.changed_files)
        self.changed_files.clear()
        self.change_detected = False
        return dirty

    def run(self) -> None:
        while True:
            current_mtimes = self._get_mtimes()
            for path, mtime in current_mtimes.items():
                if mtime > self.last_mtimes.get(path, 0):
                    self.last_mtimes[path] = mtime
                    self.changed_files.add(path)
                    self.dependencies = self.tracker.get_local_dependencies()
                    self.change_detected = True
                    self.last_change_time = time.time()
            time.sleep(0.3)
