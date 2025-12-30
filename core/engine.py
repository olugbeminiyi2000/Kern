import importlib
import sys
import traceback
import time
from pathlib import Path

# --- BOOTSTRAP: Root path injection ---
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from utils.colors import paint, RED, GREEN, YELLOW, BLUE
from tracker.dependency import DependencyTracker
from tracker.watcher import FileWatcher
from hot_reload.reloader import ModuleReloader

class Engine:
    def __init__(self, entry_file):
        self.tracker = DependencyTracker(entry_file)
        self.reloader = ModuleReloader(self.tracker)
        self.watcher = FileWatcher(self.tracker)
        self.entry_name = self.tracker.entry_point.stem
        self.user_module = None
        self.log_file = "engine_error.log"
        self.DEBOUNCE_SECONDS = 0.5 

    def _log_error(self, error_traceback):
        """Overwrites the log file and alerts the user."""
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(error_traceback)
        print(paint(f"\n[!] EXECUTION/RECONSTRUCTION FAILED", RED))
        print(paint(f"Detailed traceback saved to: {self.log_file}", YELLOW))

    def _safe_import(self):
        """Attempts to load the project. Returns True if successful."""
        try:
            script_dir = str(self.tracker.base_dir)
            if script_dir not in sys.path:
                sys.path.insert(0, script_dir)
            
            # Reconstruction Logic: Force reload if already in sys.modules
            if self.entry_name in sys.modules:
                self.user_module = importlib.reload(sys.modules[self.entry_name])
            else:
                self.user_module = importlib.import_module(self.entry_name)
                
            print(paint(f"[*] {self.entry_name} reconstructed successfully.", GREEN))
            return True
        except Exception:
            # Catch SyntaxError and others to keep the engine alive
            self._log_error(traceback.format_exc())
            self.user_module = None
            return False

    def start(self):
        """Starts the engine in non-blocking auto-reload mode."""
        self.watcher.start()
        print(paint(f"\n--- Kern Engine Ignited (AUTO-MODE) ---", BLUE))
        print(paint(f"Monitoring: {self.entry_name}. Press Ctrl+C to stop.", BLUE))
        
        # Initial run attempt
        self._safe_import()
        self._execute_user_code()

        try:
            while True:
                # 1. Passive Change Detection
                if self.watcher.change_detected:
                    
                    # 2. Debounce Check: Has enough time passed since the last save?
                    time_since_last_save = time.time() - self.watcher.last_change_time
                    
                    if time_since_last_save >= self.DEBOUNCE_SECONDS:
                        # Grab the changed files
                        dirty = self.watcher.get_and_clear_dirty()
                        
                        # Surgery removes poisoned modules from sys.modules
                        self.reloader.reload_affected_modules(dirty)
                        
                        # Always try to re-import when a stable change is detected
                        print(paint(f"\n[v] Stable change detected. Attempting recovery...", YELLOW))
                        if self._safe_import():
                            self._execute_user_code()
                
                # 3. Heartbeat Sleep (Prevents high CPU usage)
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print(paint("\n[!] Engine stopped by user. Goodbye!", BLUE))
            sys.exit(0)

    def _execute_user_code(self):
        """Encapsulated execution of the user's run() function."""
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