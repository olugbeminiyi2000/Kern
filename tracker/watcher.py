"""
Kern File Watcher - Background thread for monitoring file changes.

This module provides the FileWatcher class which runs as a daemon thread,
continuously monitoring project files for modifications. When a change is
detected, it signals the main engine loop to trigger a reload.
"""

import os
import threading
import time
from pathlib import Path
from typing import Dict, Set, List


class FileWatcher(threading.Thread):
    """
    Background thread that monitors files for changes.
    
    This class polls file modification times to detect changes. It runs as
    a daemon thread so it automatically terminates when the main program exits.
    
    Attributes:
        tracker: The DependencyTracker instance for getting files to monitor.
        dependencies: Set of file paths currently being monitored.
        last_mtimes: Dictionary mapping file paths to their last modification times.
        changed_files: Set of files that have changed since last check.
        change_detected: Flag indicating if any changes have been detected.
        last_change_time: Timestamp of the most recent change detection.
    """
    
    def __init__(self, tracker) -> None:
        """
        Initialize the FileWatcher with a DependencyTracker.
        
        Args:
            tracker: A DependencyTracker instance for resolving which files
                    to monitor.
        """
        super().__init__(daemon=True)
        self.tracker = tracker
        self.dependencies: Set[Path] = self.tracker.get_local_dependencies()
        self.last_mtimes: Dict[Path, float] = self._get_mtimes()
        self.changed_files: Set[Path] = set()
        self.change_detected: bool = False
        self.last_change_time: float = 0.0

    def _get_mtimes(self) -> Dict[Path, float]:
        """
        Get the current modification times of all monitored files.
        
        Returns:
            Dictionary mapping file paths to their modification timestamps.
        """
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
        
        This method is typically called by the main engine loop after it
        has detected that changes occurred.
        
        Returns:
            List of file paths that have been modified since the last call.
        """
        dirty = list(self.changed_files)
        self.changed_files.clear()
        self.change_detected = False
        return dirty

    def run(self) -> None:
        """
        Main loop that continuously monitors files for changes.
        
        This method runs in a separate thread and polls file modification
        times every 0.3 seconds. When a change is detected, it:
        1. Updates the last known modification time
        2. Adds the file to the changed_files set
        3. Re-scans dependencies (in case new imports were added)
        4. Sets the change_detected flag
        5. Records the change timestamp for debouncing
        """
        while True:
            current_mtimes = self._get_mtimes()
            for path, mtime in current_mtimes.items():
                if mtime > self.last_mtimes.get(path, 0):
                    self.last_mtimes[path] = mtime
                    self.changed_files.add(path)
                    
                    # Re-scan in case the user added a new import
                    self.dependencies = self.tracker.get_local_dependencies()
                    
                    # Signal detection and update the timestamp
                    self.change_detected = True
                    self.last_change_time = time.time()
            
            time.sleep(0.3)