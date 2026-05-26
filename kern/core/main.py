"""
Kern CLI - Command-line interface for the Kern engine.

Commands:
    kern run <file>  - Start the hot-reload engine on a specific file.
    kern info        - Display engine version and author information.
"""

import sys
import argparse
from pathlib import Path
from kern.core.engine import Engine
from kern.utils.colors import paint, BLUE, RED

__version__ = "0.1.0"
__authors__ = "Emmanuel Obolo Oluwapelumi & Abiodun Kumuyi"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="kern",
        description="Kern: The Deep-Reloading Development Engine",
        epilog=f"Version {__version__} | Authors: {__authors__}"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    run_parser = subparsers.add_parser("run", help="Run a script with hot-reloading")
    run_parser.add_argument("filename", help="The Python file to monitor and run")

    subparsers.add_parser("info", help="Show engine and author information")

    args = parser.parse_args()

    if args.command == "run":
        _handle_run(args.filename)
    elif args.command == "info":
        _handle_info()
    else:
        parser.print_help()


def _handle_run(filename: str) -> None:
    target_path = Path(filename)
    if not target_path.exists():
        print(paint(f"Error: File '{filename}' not found.", RED))
        sys.exit(1)
    print(paint(">>> Kern Engine Ignited...", BLUE))
    engine = Engine(target_path)
    engine.start()


def _handle_info() -> None:
    print(paint("\n--- Kern Development Engine ---", BLUE))
    print(f"Version: {__version__}")
    print(f"Authors: {__authors__}")
    print(f"Status: Active and Monitoring\n")


if __name__ == "__main__":
    main()
