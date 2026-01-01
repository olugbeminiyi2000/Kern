"""
Kern Colors - Terminal color utilities for styled output.

This module provides ANSI color codes and a helper function for
colorizing terminal output. Used throughout Kern for user feedback.

Example:
    >>> from utils.colors import paint, GREEN
    >>> print(paint("Success!", GREEN))
"""

# ANSI escape codes for terminal colors
RED: str = "\033[91m"
GREEN: str = "\033[92m"
YELLOW: str = "\033[93m"
BLUE: str = "\033[94m"
RESET: str = "\033[0m"


def paint(text: str, color: str) -> str:
    """
    Wrap text with ANSI color codes for terminal output.
    
    Args:
        text: The text to colorize.
        color: An ANSI color code (e.g., RED, GREEN, YELLOW, BLUE).
        
    Returns:
        The text wrapped with the color code and reset sequence.
        
    Example:
        >>> paint("Hello", GREEN)
        '\\033[92mHello\\033[0m'
    """
    return f"{color}{text}{RESET}"