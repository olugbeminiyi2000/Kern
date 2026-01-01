"""
Kern Tracker Package - Dependency analysis and file monitoring.

This package contains the "eyes" layer of Kern's architecture:

Modules:
    dependency: Static AST-based dependency tracking.
    watcher: Background thread for file change detection.
"""

from tracker.dependency import DependencyTracker  # noqa: F401
from tracker.watcher import FileWatcher  # noqa: F401

__all__ = ["DependencyTracker", "FileWatcher"]
