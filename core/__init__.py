"""
Kern Core Package - The main engine components.

This package contains the core functionality of the Kern hot-reloading engine:

Modules:
    engine: The main Engine class that orchestrates hot-reloading.
    main: The CLI entry point for the `kern` command.
"""

from core.engine import Engine

__all__ = ["Engine"]
