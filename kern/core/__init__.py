"""
Kern Core Package - The main engine components.

Modules:
    engine: The main Engine class that orchestrates hot-reloading.
    main: The CLI entry point for the `kern` command.
"""

from kern.core.engine import Engine  # noqa: F401

__all__ = ["Engine"]
