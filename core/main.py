import sys
import argparse
from pathlib import Path
from core.engine import Engine
from utils.colors import paint, BLUE, RED

def main():
    parser = argparse.ArgumentParser(
        description="Kern: The Deep-Reloading Development Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: kern run <filename>
    run_parser = subparsers.add_parser("run", help="Run a script with hot-reloading")
    run_parser.add_argument("filename", help="The Python file to monitor and run")

    # Command: kern info
    subparsers.add_parser("info", help="Show engine and author information")

    args = parser.parse_args()

    if args.command == "run":
        target_path = Path(args.filename)
        
        if not target_path.exists():
            print(paint(f"Error: File '{args.filename}' not found.", RED))
            sys.exit(1)
            
        print(paint(">>> Kern Engine Ignited...", BLUE))
        # Note: Using the renamed 'Engine' class
        engine = Engine(target_path)
        engine.start()

    elif args.command == "info":
        print(paint("\n--- Kern Development Engine ---", BLUE))
        print(f"Version: 0.1.0")
        print(f"Authors: Emmanuel Obolo Oluwapelumi & Abiodun Kumuyi")
        print(f"Status: Active and Monitoring\n")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()