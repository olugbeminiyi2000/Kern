"""
Kern Hot Reload Package - Module reloading functionality.

This package contains the "muscle" layer of Kern's architecture:

Modules:
    reloader: Surgical module eviction from sys.modules.
"""

from hot_reload.reloader import ModuleReloader

__all__ = ["ModuleReloader"]
