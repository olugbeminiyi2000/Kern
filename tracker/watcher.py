import os
import threading
import time

class FileWatcher(threading.Thread):
    def __init__(self, tracker):
        super().__init__(daemon=True)
        self.tracker = tracker
        self.dependencies = self.tracker.get_local_dependencies()
        self.last_mtimes = self._get_mtimes()
        self.changed_files = set()
        self.change_detected = False
        self.last_change_time = 0

    def _get_mtimes(self):
        mtimes = {}
        for p in self.dependencies:
            try:
                mtimes[p] = os.stat(p).st_mtime
            except FileNotFoundError:
                continue
        return mtimes

    def get_and_clear_dirty(self):
        dirty = list(self.changed_files)
        self.changed_files.clear()
        self.change_detected = False
        return dirty

    def run(self):
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