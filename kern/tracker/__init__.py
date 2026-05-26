"""
Kern Tracker Package - Dependency analysis and file monitoring.

Modules:
    dependency: Static AST-based dependency tracking.
    watcher: Background thread for file change detection.
"""

from kern.tracker.dependency import DependencyTracker  # noqa: F401
from kern.tracker.watcher import FileWatcher  # noqa: F401

__all__ = ["DependencyTracker", "FileWatcher"]
