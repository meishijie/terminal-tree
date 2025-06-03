#!/usr/bin/env python3
"""Main entry point for the terminal tree plugin."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .app import TerminalTreeApp


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Terminal filesystem navigator",
        prog="terminal-tree",
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Starting directory path (default: current directory)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )

    return parser.parse_args()


def validate_path(path_str: str) -> Optional[Path]:
    """Validate and return a Path object if the path exists."""
    try:
        path = Path(path_str).resolve()
        if not path.exists():
            print(f"Error: Path '{path_str}' does not exist.", file=sys.stderr)
            return None
        if not path.is_dir():
            print(f"Error: Path '{path_str}' is not a directory.", file=sys.stderr)
            return None
        return path
    except (OSError, ValueError) as e:
        print(f"Error: Invalid path '{path_str}': {e}", file=sys.stderr)
        return None


def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Validate the starting path
    start_path = validate_path(args.path)
    if start_path is None:
        return 1

    try:
        # Create and run the app
        app = TerminalTreeApp(start_path=start_path, debug=args.debug)
        app.run()
        return 0
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        if args.debug:
            raise
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())